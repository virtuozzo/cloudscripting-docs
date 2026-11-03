"""Pin release provenance and inventory Git objects without changing repository state.

The legacy config is an import input only. Subsequent audits should use the pinned
manifest as --config. Rendering consumes the manifest, never moving source refs.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

import jsonschema
import yaml

ROOT_BASELINE = '76628f8aa01571fbc348211cb7df726cf408cd17'
SCHEMA = Path(__file__).resolve().parents[2] / 'migration/schemas/release-sources.schema.json'
SHA = re.compile(r'^[0-9a-f]{40}$')
RELEASE = re.compile(r'^[0-9]+(?:\.[0-9]+)+(?:-[0-9]+)?$')


def git(repo, *args):
    """Invoke a read-only Git command with explicit arguments and no shell."""
    environment = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1',
                       GIT_NO_LAZY_FETCH='1', GIT_OPTIONAL_LOCKS='0')
    result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, env=environment)
    if result.returncode:
        raise ValueError(result.stderr.decode('utf-8', errors='replace').strip())
    return result.stdout


def numeric_key(identity):
    # Identity stays untouched, including the old 6.0-2 spelling.
    return tuple(int(part) for part in re.split(r'[.-]', identity)), identity


def pinned_commit(repo, revision):
    resolved = git(repo, 'rev-parse', '--verify', revision + '^{commit}').decode().strip()
    if not SHA.fullmatch(resolved):
        raise ValueError('expected a full SHA-1 commit identity')
    return resolved


def decision(basis, evidence):
    return {'basis': basis, 'evidence': evidence}


def build_manifest(repo: Path, config: Path) -> dict:
    """Import legacy mappings once, or retain every pin in an existing manifest."""
    raw = config.read_bytes()
    # BaseLoader treats Python tags as inert data and preserves legacy scalar text.
    parsed = yaml.load(raw, Loader=yaml.BaseLoader)
    if isinstance(parsed, dict) and 'schema_version' in parsed:
        manifest = yaml.safe_load(raw)
        validate_manifest(manifest)
        return manifest
    try:
        versions = parsed['extra']['versions']
    except (KeyError, TypeError) as error:
        raise ValueError('config must be a release manifest or contain extra.versions') from error
    if not isinstance(versions, dict) or not versions:
        raise ValueError('extra.versions must be a nonempty mapping')
    releases = []
    for identity, platform in sorted(versions.items(), key=lambda pair: numeric_key(pair[0])):
        ref = 'refs/remotes/origin/' + identity
        releases.append({
            'id': identity, 'platform_version': platform,
            'source_ref': ref, 'source_commit': pinned_commit(repo, ref),
            'source_format': 'mkdocs', 'publication': 'retained',
            'output_prefix': identity + '/', 'decision_status': 'provisional',
            'decision_provenance': decision('configured-release-preservation',
                'legacy extra.versions; config_sha256=' + hashlib.sha256(raw).hexdigest()
                + '; live publication not verified'),
        })
    manifest = {
        'schema_version': 1, 'production_base_url': 'https://www.virtuozzo.com/cloudscripting-docs/',
        'default_version': max(versions, key=numeric_key),
        'root': {
            'source_commit': ROOT_BASELINE, 'source_format': 'mkdocs',
            'output_prefix': '', 'decision_status': 'approved',
            'decision_provenance': decision('user-decision-2026-10-31',
                'User selected current repository content for the unversioned root, including ubuntu24; '
                'frozen releases retain historical content. This pins the authored MkDocs baseline; '
                'Task 09 will pin the reviewed Hugo conversion, not an execution-branch HEAD.'),
        },
        'releases': releases,
        'candidate_publication': {
            'decision_status': 'unresolved',
            'decision_provenance': decision('local-ref-candidates-only',
                'Additional numeric refs require live route and retained-scope evidence; not automatically published'),
        },
    }
    validate_manifest(manifest)
    return manifest


def validate_manifest(manifest: dict) -> None:
    """Enforce schema and cross-record routing/ordering invariants."""
    try:
        jsonschema.Draft202012Validator(json.loads(SCHEMA.read_text())).validate(manifest)
        releases = manifest['releases']
        ids = [release['id'] for release in releases]
        if len(ids) != len(set(ids)) or ids != sorted(ids, key=numeric_key):
            raise ValueError('release IDs must be unique and numerically ordered')
        if manifest['default_version'] not in ids:
            raise ValueError('default_version must name a retained release')
        for release in releases:
            if release['output_prefix'] != release['id'] + '/':
                raise ValueError('release output_prefix must be its exact ID plus /')
    except jsonschema.ValidationError as error:
        raise ValueError('invalid release manifest: ' + error.message) from error


def discover_candidates(repo: Path) -> list:
    """Snapshot locally present remote refs; never fetch or normalize identities."""
    candidates = []
    lines = git(repo, 'for-each-ref', '--format=%(refname) %(objectname)', 'refs/remotes/origin/').decode().splitlines()
    for line in lines:
        ref, commit = line.split(' ', 1)
        identity = ref.removeprefix('refs/remotes/origin/')
        if RELEASE.fullmatch(identity):
            candidates.append({'id': identity, 'source_ref': ref,
                               'source_commit': commit, 'publication': 'unknown'})
    return sorted(candidates, key=lambda item: numeric_key(item['id']))


def issue(identity, evidence, source_path=None):
    return {'id': identity, 'source_path': source_path, 'severity': 'error', 'evidence': evidence}


def check_production_completeness(repo: Path, manifest: dict) -> dict:
    """Fail closed for unavailable objects and unresolved publication decisions."""
    validate_manifest(manifest)
    issues = []
    if manifest['root']['decision_status'] != 'approved':
        issues.append(issue('root-policy-unresolved', 'Root source policy is provisional.'))
    if manifest['candidate_publication']['decision_status'] != 'approved':
        issues.append(issue('extra-publication-unresolved', 'Additional release candidate publication scope is unresolved.'))
    for release in manifest['releases']:
        if release['decision_status'] != 'approved':
            issues.append(issue('release-publication-unresolved', 'Publication evidence is provisional.', release['id']))
    missing = False
    for identity, record in [('root', manifest['root'])] + [(r['id'], r) for r in manifest['releases']]:
        try:
            commit = record['source_commit']
            if pinned_commit(repo, commit) != commit:
                raise ValueError('object is not the specified commit')
            git(repo, 'cat-file', '-e', commit + (':mkdocs.yml' if record['source_format'] == 'mkdocs' else ':config.yaml'))
        except ValueError as error:
            missing = True
            issues.append(issue('missing-source-object', str(error), identity))
    return {
        'schema_version': 1, 'status': 'fail' if missing else ('incomplete' if issues else 'pass'),
        'inputs': {'root_commit': manifest['root']['source_commit'],
                   'release_commits': {r['id']: r['source_commit'] for r in manifest['releases']}},
        'checks': {'required_sources': 1 + len(manifest['releases'])}, 'issues': issues,
    }


def inventory_sources(repo: Path, manifest: dict) -> dict:
    """Inventory each required source from exact-case immutable Git tree/blob objects."""
    report = check_production_completeness(repo, manifest)
    candidates = discover_candidates(repo)
    configured = {release['id'] for release in manifest['releases']}
    for candidate in candidates:
        candidate['configured'] = candidate['id'] in configured
    report['candidates'] = candidates
    report['checks'].update({
        'candidate_count': len(candidates), 'configured_count': len(configured),
        'configured_source_commits': len({r['source_commit'] for r in manifest['releases']}),
        'additional_candidates': len([c for c in candidates if not c['configured']]),
    })
    report['sources'] = {}
    trees = {}
    report['inventories'] = trees
    blobs = {}
    for identity, record in [('root', manifest['root'])] + [(r['id'], r) for r in manifest['releases']]:
        commit = record['source_commit']
        if commit not in trees:
            editorial, assets, tree_entries = [], [], {}
            for item in git(repo, 'ls-tree', '-r', '-z', '--full-tree', commit).split(b'\0'):
                if not item:
                    continue
                metadata, raw_path = item.split(b'\t', 1)
                mode, kind, blob = metadata.decode().split()
                path = raw_path.decode('utf-8')
                if kind != 'blob':
                    continue
                tree_entries[path] = blob
                is_editorial = path.startswith('docs/') and path.endswith('.md') and not path.startswith('docs/superpowers/')
                is_asset = path.startswith('theme/readthedocs/img/')
                if not (is_editorial or is_asset):
                    continue
                if blob not in blobs:
                    content = git(repo, 'cat-file', 'blob', blob)
                    blobs[blob] = {'sha256': hashlib.sha256(content).hexdigest(), 'size': len(content)}
                entry = {'path': path, 'git_blob': blob, **blobs[blob]}
                (editorial if is_editorial else assets).append(entry)
            # Legacy tags stay inert: no arbitrary Python constructors run.
            config = yaml.load(git(repo, 'show', commit + ':mkdocs.yml'), Loader=yaml.BaseLoader)
            navigation = []

            def walk(items, parents):
                if not isinstance(items, list):
                    raise ValueError('invalid legacy pages navigation')
                for item in items:
                    for title, value in item.items():
                        if isinstance(value, list):
                            walk(value, parents + [title])
                        else:
                            source_path = 'docs/' + value
                            navigation.append({'title': title, 'parents': parents,
                                               'source_path': source_path,
                                               'git_blob': tree_entries.get(source_path)})
                            if source_path not in tree_entries:
                                raise ValueError('navigation source missing at ' + commit + ':' + source_path)

            walk(config.get('pages', []), [])
            trees[commit] = {'source_commit': commit, 'editorial': editorial,
                             'navigation': navigation, 'assets': assets,
                             'config_git_blob': tree_entries.get('mkdocs.yml')}
        report['sources'][identity] = {'source_commit': commit, 'inventory_key': commit}
    return report


class QuotedStringsDumper(yaml.SafeDumper):
    """Keep IDs and platform values visibly quoted for future editors."""


QuotedStringsDumper.add_representer(str, lambda dumper, value: dumper.represent_scalar('tag:yaml.org,2002:str', value, style="'"))


def write_yaml(value, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(yaml.dump(value, Dumper=QuotedStringsDumper, sort_keys=False, allow_unicode=True), encoding='utf-8')


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--production', action='store_true', help='require complete approved production evidence')
    args = parser.parse_args(argv)
    try:
        manifest = build_manifest(args.repo, args.config)
        report = inventory_sources(args.repo, manifest)
        write_yaml(manifest, args.output)
    except (ValueError, OSError, yaml.YAMLError) as error:
        report = {'schema_version': 1, 'status': 'fail',
                  'inputs': {'config': str(args.config)}, 'checks': {},
                  'issues': [issue('inventory-failed', str(error))]}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    return int(report['status'] == 'fail' or (args.production and report['status'] != 'pass'))


if __name__ == '__main__':
    raise SystemExit(main())
