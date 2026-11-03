"""Compare real Hugo copy text to captured legacy bytes using the current overrides.

--converter-root selects the repository containing frozen sources and converter
tooling. Expected bytes and renderer results are never normalized; originals stay immutable.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import yaml

ROOT = Path(__file__).resolve().parents[3]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--converter-root', type=Path, default=ROOT)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--base-url', help='Optional root/staging build context; existing CLI defaults are unchanged')
    args = parser.parse_args()
    source = args.converter_root.resolve()
    sys.path.insert(0, str(source))
    sys.path.insert(0, str(source / 'tests/migration'))
    from scripts.migration.convert import convert_tree
    from scripts.migration.inventory import _git
    from scripts.migration.markdown_converter import LEGACY_CORRESPONDENCE_TEMPLATES
    from test_converter import legacy_blocks
    module_spec = importlib.util.spec_from_file_location('theme_test', ROOT / 'tests/migration/test_theme_compatibility.py')
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    page_map = json.loads((source / 'migration/page-map.json').read_text())
    originals = {p['source_path']: _git(source, 'show', page_map['source_commit'] + ':' + p['source_path'])
                 for p in page_map['pages']}
    assert all(hashlib.sha256(originals[p['source_path']]).hexdigest() == p['source_sha256']
               for p in page_map['pages'])
    for page in page_map['pages']:
        template = LEGACY_CORRESPONDENCE_TEMPLATES.get(page['source_path'])
        if template:
            originals[template] = _git(source, 'show', page_map['source_commit'] + ':' + template)
    base_url = args.base_url or yaml.safe_load((ROOT/'config.yaml').read_text())['baseURL']
    baseline_path = source/'tests/migration/fixtures/baseline/legacy-root.json'
    report = {'schema_version': 1, 'status': 'pass', 'inputs': {
        'source_commit': page_map['source_commit'], 'base_url': base_url,
        'expected_copy_oracle': '564 captured legacy blocks plus only the exact source-pinned restored Custom Responses pair',
        'baseline_sha256': hashlib.sha256(baseline_path.read_bytes()).hexdigest(),
        'config_sha256': hashlib.sha256((ROOT / 'config.yaml').read_bytes()).hexdigest(), 'converter_commit': subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip(),
        'converter_inputs_sha256': {name: hashlib.sha256((source / name).read_bytes()).hexdigest() for name in ('scripts/migration/convert.py', 'scripts/migration/markdown_converter.py', 'tests/migration/test_converter.py')}, 'theme_commit': subprocess.check_output(['git', '-C', str(ROOT / 'themes'), 'rev-parse', 'HEAD'], text=True).strip(),
        'clipboard_parser': 'html5lib 1.1 (HTML5 DOM textarea initial-LF semantics)',
        'hugo': subprocess.check_output([module.HUGO, 'version'], text=True).strip()}, 'checks': [], 'issues': []}
    with tempfile.TemporaryDirectory(prefix='cs-theme-corpus-') as temp:
        work = Path(temp)
        frozen = work / 'frozen-source'
        for name, raw in originals.items():
            path = frozen / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        converted = convert_tree(frozen, page_map, work)
        if converted['status'] != 'pass': raise AssertionError(converted)
        (work / 'themes').symlink_to(ROOT / 'themes')
        for directory in ('layouts', 'data', 'assets'):
            shutil.copytree(ROOT / directory, work / directory)
        shutil.copy(ROOT / 'config.yaml', work / 'config.yaml')
        shutil.copy(ROOT / 'redirects.htaccess', work / 'redirects.htaccess')
        shutil.copy(ROOT / 'content/search.md', work / 'content/search.md')
        subprocess.run([module.HUGO, '--source', str(work), '--baseURL', base_url], check=True, capture_output=True, text=True)
        totals = {'pages': 0, 'blocks': 0, 'groups': 0}
        for page in page_map['pages']:
            if not page['published']: continue
            route = page['old_url']
            text = (work / 'public' / route.lstrip('/') / 'index.html').read_text()
            actual = module.Capture(text)
            legacy = legacy_blocks(route)
            expected = [body.decode() for _, body in legacy]
            for kind, values in [('display', actual.pre), ('clipboard', actual.copies)]:
                if values != expected:
                    report['status'] = 'fail'
                    report['issues'].append({'id': 'code-bytes', 'source_path': page['source_path'], 'severity': 'error',
                        'evidence': {'kind': kind, 'actual_count': len(values), 'expected_count': len(expected),
                        'mismatches': [i for i, (a,b) in enumerate(zip(values, expected)) if a != b]}})
            totals['pages'] += 1
            totals['blocks'] += len(expected)
            totals['groups'] += text.count('class="tabs-container"')
            report['checks'].append({'url': route, 'blocks': len(expected), 'html_sha256': hashlib.sha256(text.encode()).hexdigest(),
                                     'exact_visible_and_clipboard': actual.pre == expected and actual.copies == expected})
        unchanged = all((frozen/name).read_bytes() == raw for name,raw in originals.items())
        report['original_sources_unchanged'] = unchanged
        if not unchanged:
            report['status'] = 'fail'
            report['issues'].append({'id':'original-source-mutated','severity':'error','evidence':'Source bytes changed during conversion/render'})
        report['totals'] = totals
        if totals != {'pages': 16, 'blocks': 566, 'groups': 269}:
            report['status'] = 'fail'
            report['issues'].append({'id': 'corpus-cardinality', 'severity': 'error', 'evidence': totals})
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'totals': report['totals'], 'issues': report['issues']}))
    return 0 if report['status'] == 'pass' else 1


if __name__ == '__main__': raise SystemExit(main())
