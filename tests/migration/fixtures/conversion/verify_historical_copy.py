"""Diagnostic: compare converted frozen presentations to captured historical bytes.

This is not full historical site acceptance. Originals are read from local Git
objects; expected code comes only from hash-checked capture files and the exact
source-pinned restored pair. No presentation normalization is used in the oracle.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT/'tests/migration'))
from scripts.migration.inventory import _git
from scripts.migration.markdown_converter import convert_document, LEGACY_CORRESPONDENCE_TEMPLATES
from test_converter import active_blocks, legacy_blocks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline-root', required=True, type=Path)
    parser.add_argument('--report', required=True, type=Path)
    args = parser.parse_args()
    baseline_root = args.baseline_root.resolve()
    index_path = baseline_root/'migration/releases/baselines/index.json'
    index = json.loads(index_path.read_bytes())
    report = dict(schema_version=1, status='pass',
                  inputs=dict(catalog_sha256=hashlib.sha256(index_path.read_bytes()).hexdigest(),
                              scope='Presentation-byte diagnostic; full historical site acceptance remains separate'),
                  checks=[], issues=[])
    restored = legacy_blocks('/creating-manifest/handling-custom-responses/')[4:6]
    for snapshot in index['snapshots']:
        if not snapshot['release_ids']:
            continue
        revision = snapshot['source_commit']
        baseline_path = baseline_root/snapshot['baseline']
        baseline = json.loads(baseline_path.read_bytes())
        mapping = json.loads((baseline_root/snapshot['page_map']).read_bytes())
        count = 0
        for page in mapping['pages']:
            if page['published'] is not True:
                continue
            raw = _git(ROOT, 'show', revision+':'+page['source_path'])
            assert hashlib.sha256(raw).hexdigest() == page['source_sha256']
            if page['source_path'] in LEGACY_CORRESPONDENCE_TEMPLATES:
                template = _git(ROOT, 'show', revision+':'+LEGACY_CORRESPONDENCE_TEMPLATES[page['source_path']])
                page = dict(page, legacy_correspondence_template=template)
            converted, _ = convert_document(raw, page)
            actual = active_blocks(converted)
            expected = []
            captured = baseline['pages'][page['old_url']]
            for block in captured['code_blocks']:
                body = (baseline_path.parent/block['text_path']).read_bytes()
                assert hashlib.sha256(body).hexdigest() == block['sha256']
                expected.append((block['language'] or '', body))
            if page['source_path'] == 'docs/creating-manifest/handling-custom-responses.md':
                group = b''.join(raw.splitlines(keepends=True)[75:100])
                assert hashlib.sha256(group).hexdigest() == '312f82d1b0ba94670f2ade6ccdfa06564e63ccdb9d9fc408b5b9bb257d98cf00'
                assert len(expected) == 20
                expected[4:4] = restored
            count += len(expected)
            if actual != expected:
                report['status'] = 'fail'
                report['issues'].append(dict(id='historical-copy-bytes', source_path=page['source_path'],
                    severity='error', evidence=dict(source_commit=revision, expected_count=len(expected),
                        actual_count=len(actual), indices=[i for i,(a,b) in enumerate(zip(actual,expected)) if a!=b])))
        report['checks'].append(dict(source_commit=revision, release_ids=snapshot['release_ids'],
            baseline_sha256=hashlib.sha256(baseline_path.read_bytes()).hexdigest(),
            expected_blocks_including_exact_restoration=count))
    report['snapshots'] = len(report['checks'])
    report['expected_blocks'] = sum(c['expected_blocks_including_exact_restoration'] for c in report['checks'])
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','snapshots','expected_blocks','issues']}))
    return 0 if report['status'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
