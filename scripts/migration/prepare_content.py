"""Prepare published converted content and exact-case static/bundle assets."""
import argparse
import json
from pathlib import Path
import sys
import subprocess

from .assets import build_asset_map, materialize, snapshot_workspace, _safe_path, require_case_sensitive
from .content_urls import normalize_document, bundle_markdown_images


def prepare(source_root, converted_dir, page_map, baseline, destination, report_path):
    source_root, converted_dir, destination, report_path = map(Path, (source_root, converted_dir, destination, report_path))
    report = {'schema_version': 1, 'status': 'fail', 'inputs': {'source_commit': page_map.get('source_commit'), 'baseline_source_commit': baseline.get('inputs', {}).get('source_commit')}, 'checks': [], 'issues': []}
    try:
        revision = page_map.get('source_commit')
        if not revision or page_map.get('source_kind') != 'git':
            raise ValueError('Asset preparation requires a frozen Git page map')
        if baseline.get('status') != 'pass' or baseline.get('inputs', {}).get('source_commit') != revision:
            raise ValueError('Rendered baseline source identity must match the page map')
        if destination.exists() and any(destination.iterdir()):
            raise ValueError('Content preparation requires an empty destination to exclude stale publication')
        require_case_sensitive(destination)
        asset_map = build_asset_map(source_root, revision, page_map, baseline)
        documents = []
        for page in page_map['pages']:
            if not page['published']:
                continue
            target = _safe_path(page['target_path'])
            if target.parts[0] != 'content' or target.suffix != '.md':
                raise ValueError('Invalid published content destination: ' + str(target))
            original = (converted_dir / target).read_bytes()
            normalized = normalize_document(original, page, baseline)
            resources = [r for a in asset_map['assets'] for r in a['bundle_resources'] if r['page_url'] == page['old_url']]
            documents.append((destination / target, bundle_markdown_images(normalized, resources)))
        snapshot_dir = report_path.parent / (report_path.stem + '-workspace-snapshot')
        observations = snapshot_workspace(source_root, asset_map, snapshot_dir)
        materialize(source_root, asset_map, destination)
        for path, document in documents:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(document)
        (destination / 'asset-map.json').write_text(json.dumps(asset_map, indent=2) + '\n')
        report['checks'] = [{'id': 'frozen-assets', 'status': 'pass', 'count': len(asset_map['assets'])}, {'id': 'published-documents', 'status': 'pass', 'count': len(documents)}, {'id': 'workspace-snapshot', 'status': 'pass', 'path': str(snapshot_dir), 'observations': len(observations)}]
        report['status'] = 'pass'
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        report['issues'].append({'id': 'content-preparation', 'source_path': str(source_root), 'severity': 'error', 'evidence': str(error)})
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for argument in ('source-root', 'converted-dir', 'page-map', 'baseline', 'destination', 'report'):
        parser.add_argument('--' + argument, required=True, type=Path)
    args = parser.parse_args()
    try:
        result = prepare(args.source_root, args.converted_dir, json.loads(args.page_map.read_text()), json.loads(args.baseline.read_text()), args.destination, args.report)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    if result['status'] != 'pass':
        print(result['issues'][0]['evidence'], file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
