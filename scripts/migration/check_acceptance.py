"""Verify reviewed historical publication inputs without rendering legacy or Hugo.

This command checks historical publication inputs; served-site acceptance is
separate. Canonical captured maps/baselines/code remain immutable inputs.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
import yaml
from scripts.migration.inventory import build_inventory


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_file(root, value):
    if not isinstance(value, str) or not value or '\\' in value or value.startswith('/') or any(c in value for c in ('\x00', '\r', '\n')) or any(x in {'', '.', '..'} for x in value.split('/')):
        raise ValueError('Unsafe repository-relative input path: '+str(value))
    path = root/value
    if not path.is_file() or any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError('Input must be a regular file without symlink traversal: '+value)
    return path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify(root, catalog_path):
    result = {'schema_version': 1, 'status': 'pass', 'inputs': {'catalog': str(catalog_path), 'catalog_sha256': digest(catalog_path)}, 'checks': [], 'issues': [], 'summary': {}}
    try:
        catalog = json.loads(catalog_path.read_text())
        manifest = yaml.safe_load((root/'migration/release-sources.yaml').read_text())
        index = json.loads((root/'migration/releases/baselines/index.json').read_text())
        correspondence = json.loads((root/'migration/releases/correspondence-inventory.json').read_text())
        contexts = {s['source_commit']: s for s in correspondence['snapshots']}
        snapshots = {s['source_commit']: s for s in index['snapshots'] if s.get('role') != 'current-reference'}
        releases = {r['id']: r for r in manifest['releases'] if r['publication'] == 'retained'}
        require(catalog.get('schema_version') == 1 and isinstance(catalog.get('builds'), list), 'Invalid acceptance catalog schema')
        builds = [b for b in catalog['builds'] if b.get('id') != 'root']
        require(len(builds) == len(releases) == 24 and {b.get('id') for b in builds} == set(releases), 'Require exactly the 24 retained historical release IDs without duplicates or omissions')
        require(len(snapshots) == 19, 'Require the reviewed 19 historical sources')
        result['checks'].append({'id': 'historical-release-coverage', 'status': 'pass'})
        verified = set()
        for build in builds:
            identity = build['id']
            try:
                release = releases[identity]
                sha = release['source_commit']
                require(build.get('source_commit') == build.get('validation_source_commit') == sha, 'Actual, validation and manifest pins differ')
                snapshot = snapshots[sha]
                require(identity in snapshot['release_ids'], 'Release does not belong to this captured source')
                files = {key: regular_file(root, build[key]) for key in ('page_map', 'baseline', 'exceptions')}
                require(build['baseline'] == snapshot['baseline'], 'Baseline must be the immutable captured catalog entry')
                cache_key = (sha, *(str(files[k]) for k in ('page_map', 'baseline', 'exceptions')))
                if cache_key in verified:
                    continue
                captured_map = json.loads(regular_file(root, snapshot['page_map']).read_text())
                page_map = json.loads(files['page_map'].read_text())
                baseline = json.loads(files['baseline'].read_text())
                exceptions = json.loads(files['exceptions'].read_text())
                require(page_map.get('source_kind') == 'git' and page_map.get('source_commit') == baseline['inputs']['source_commit'] == baseline['build_provenance']['source_commit'] == sha, 'Map/baseline source provenance differs')
                require(baseline['status'] == 'pass' and snapshot['status'] == 'pass', 'Baseline capture must pass')
                fresh = build_inventory(root, sha)
                require(fresh == captured_map, 'Immutable captured inventory differs from a fresh Git inventory')
                require(page_map.get('navigation') == captured_map['navigation'], 'Navigation differs from immutable inventory')
                original = {p['source_path']: p for p in captured_map['pages']}
                reviewed = {p['source_path']: p for p in page_map['pages']}
                require(len(reviewed) == len(page_map['pages']) == len(original) == 34 and set(reviewed) == set(original), 'Source map has missing, duplicate or added sources')
                context = contexts[sha]
                title = correspondence['variants'][context['template_sha256']]['generated_h1']
                for source_path, old in original.items():
                    page = reviewed[source_path]
                    for key, value in old.items():
                        if key == 'disposition' and not old['published']:
                            require(page.get(key) == 'candidate-for-restoration', 'Unlisted disposition must remain an unpublished restoration candidate')
                        elif key == 'title' and source_path == context['source_path']:
                            require(page.get(key) == title, 'Generated correspondence title must match the exact pinned template')
                        else:
                            require(page.get(key) == value, 'Immutable source/navigation/route identity changed: '+source_path+'/'+key)
                    if not old['published']:
                        evidence = page.get('disposition_evidence', {})
                        require(evidence.get('source_commit') == sha and evidence.get('source_path') == source_path and evidence.get('source_sha256') == old['source_sha256'] and evidence.get('captured_map') == snapshot['page_map'] and evidence.get('baseline') == snapshot['baseline'] and evidence.get('facts') and evidence.get('decision'), 'Missing source/build rationale for unpublished source')
                published = {p['old_url'] for p in reviewed.values() if p['published']}
                require(len(published) == 16 and published == set(baseline['pages']), 'Only the captured 16 configured pages may be published')
                review = page_map.get('acceptance_review', {})
                require(review.get('captured_map') == snapshot['page_map'] and review.get('captured_map_sha256') == digest(root/snapshot['page_map']) and review.get('baseline') == snapshot['baseline'] and review.get('baseline_sha256') == digest(files['baseline']), 'Acceptance map capture references differ')
                require(exceptions.get('schema_version') == 1 and exceptions.get('status') == 'pass' and exceptions.get('inputs', {}).get('source_commit') == sha and exceptions['inputs'].get('baseline') == snapshot['baseline'] and exceptions['inputs'].get('baseline_sha256') == digest(files['baseline']), 'Exception file provenance differs')
                expected = {}
                for route, page in baseline['pages'].items():
                    for index, link in enumerate(page.get('links', [])):
                        target = link['resolved_url'];parts = urlsplit(target)
                        if parts.scheme or parts.netloc or re.search(r'[\x00-\x20\\{}*]', target):
                            continue
                        target_route = parts.path
                        if target_route+'/' in baseline['pages']:
                            target_route += '/'
                        destination = baseline['pages'].get(target_route)
                        kind = 'broken-link' if destination is None else 'missing-fragment' if parts.fragment and unquote(parts.fragment) not in destination['ids'] else None
                        if kind:
                            expected.setdefault((kind, route, target), []).append({'link_index': index, 'href': link['href'], 'resolved_url': target, 'text': link.get('text', '')})
                seen = set()
                for entry in exceptions['exceptions']:
                    key = (entry.get('check'), entry.get('url'), entry.get('target'))
                    require(key in expected and key not in seen and entry.get('source_commit') == sha and entry.get('reason'), 'Exception is duplicate, unobserved, valid-target or different-source')
                    seen.add(key)
                    evidence = entry.get('evidence', {})
                    require(evidence.get('baseline') == snapshot['baseline'] and evidence.get('baseline_sha256') == digest(files['baseline']) and evidence.get('source_path') == baseline['pages'][entry['url']]['source_path'] and evidence.get('occurrences') == expected[key], 'Exception occurrence evidence differs from exact captured href/target/origin/count')
                require(seen == set(expected), 'Missing exact inherited defect review')
                verified.add(cache_key)
                result['checks'].append({'id': 'historical-input-identity', 'status': 'pass', 'source_commit': sha, 'release_id': identity, 'published': 16, 'unpublished_candidates': 18, 'exact_exception_records': len(seen)})
            except (KeyError, TypeError, ValueError, OSError) as error:
                result['status'] = 'fail'
                result['issues'].append({'id': 'historical-acceptance-input', 'url': '/'+str(identity)+'/', 'severity': 'error', 'evidence': str(error)})
        result['summary'] = {'historical_releases': len(builds), 'historical_sources': len({b['source_commit'] for b in builds}), 'root_record_present': any(b.get('id') == 'root' for b in catalog['builds']), 'full_task_10': 'incomplete', 'scope': 'Reviewed historical inputs only; full build/browser/http/hosting/table/malformed-link acceptance remains open'}
    except (KeyError, TypeError, ValueError, OSError) as error:
        result['status'] = 'fail'
        result['issues'].append({'id': 'historical-acceptance-catalog', 'url': '/', 'severity': 'error', 'evidence': str(error)})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, default=REPO/'migration/releases/acceptance.json')
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    try:
        report = verify(REPO, args.catalog)
    except (OSError, ValueError) as error:
        report = {'schema_version': 1, 'status': 'fail', 'inputs': {'catalog': str(args.catalog)}, 'checks': [], 'issues': [{'id': 'catalog-read', 'url': '/', 'severity': 'error', 'evidence': str(error)}]}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2)+'\n')
    print(report['status']+': historical acceptance inputs (offline check only)')
    return 0 if report['status'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
