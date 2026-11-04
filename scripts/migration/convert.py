"""Convert explicitly published page-map records, validating before any writes."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys

from .markdown_converter import ConversionError, LEGACY_CORRESPONDENCE_TEMPLATES, convert_document


def _contained(root, relative, prefix):
    path = PurePosixPath(relative)
    if path.is_absolute() or '..' in path.parts or not path.parts or path.parts[0] != prefix:
        raise ValueError('Unsafe ' + prefix + ' path: ' + relative)
    resolved = (root / relative).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError('Path escapes root through a symlink: ' + relative)
    return resolved


def convert_tree(source_root, page_map, destination, sources=None):
    root, destination = Path(source_root).resolve(), Path(destination).resolve()
    metadata = page_map if isinstance(page_map, dict) else {}
    report = dict(schema_version=1, status='fail', inputs=dict(source_root=str(root.resolve()),
                  source_commit=metadata.get('source_commit'), source_kind=metadata.get('source_kind')),
                  checks=[], issues=[])
    outputs = []
    selected = set(sources or [])
    seen = set()
    try:
        if not isinstance(page_map, dict):
            raise ValueError('Page map must be an object')
        if page_map.get('schema_version') != 1:
            raise ValueError('Unsupported page-map schema')
        records = page_map['pages']
        by_source = {p['source_path']: p for p in records}
        if len(by_source) != len(records):
            raise ValueError('Duplicate source paths in page map')
        if selected - by_source.keys():
            raise ValueError('Unknown selected sources: ' + ', '.join(sorted(selected - by_source.keys())))
        for page in records:
            source_path = page['source_path']
            if type(page.get('published')) is not bool:
                report['issues'].append(dict(id='invalid-publication', source_path=source_path, severity='error',
                                             evidence='published must be a JSON boolean'))
                continue
            if selected and source_path not in selected:
                continue
            if not page['published'] and source_path not in selected:
                continue
            try:
                source = _contained(root, source_path, 'docs')
                if source_path.startswith('docs/superpowers/'):
                    raise ValueError('Engineering documentation is excluded')
                target = _contained(destination, page.get('target_path') or '', 'content')
                if target in seen:
                    raise ValueError('Duplicate target path: ' + page['target_path'])
                if target == source or target.is_relative_to(root / 'docs'):
                    raise ValueError('Destination would overwrite source content')
                seen.add(target)
                raw = source.read_bytes()
                digest = hashlib.sha256(raw).hexdigest()
                if digest != page.get('source_sha256'):
                    raise ValueError('Source SHA-256 differs from page map')
                context = {}
                if source_path in LEGACY_CORRESPONDENCE_TEMPLATES:
                    template_path = LEGACY_CORRESPONDENCE_TEMPLATES[source_path]
                    template = _contained(root, template_path, 'theme').read_bytes()
                    page = dict(page, legacy_correspondence_template=template)
                    context['legacy_template_sha256'] = hashlib.sha256(template).hexdigest()
                    context['legacy_template_path'] = template_path
                converted, issues = convert_document(raw, page)
                report['issues'].extend(issues)
                outputs.append((target, converted))
                report['checks'].append(dict(source_path=source_path, source_sha256=digest,
                                             target_path=page['target_path'], output_sha256=hashlib.sha256(converted).hexdigest(), status='pass', **context))
            except ConversionError as error:
                report['issues'].extend(error.issues)
            except (ValueError, OSError, KeyError, TypeError) as error:
                report['issues'].append(dict(id='conversion-input', source_path=source_path, severity='error', evidence=str(error)))
        if report['issues']:
            return report
        for target, converted in outputs:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(converted)
        report['status'] = 'pass'
        return report
    except (ValueError, OSError, KeyError, TypeError) as error:
        report['issues'].append(dict(id='conversion-input', source_path=None, severity='error', evidence=str(error)))
        return report


def _report_destination(args, page_map):
    """Resolve and reject file/directory aliases before any conversion writes."""
    report = args.report.resolve()
    protected = [args.page_map.resolve(), (args.source_root / 'docs').resolve(),
                 (args.destination / 'content').resolve()]
    protected.extend((args.source_root / path).resolve() for path in LEGACY_CORRESPONDENCE_TEMPLATES.values())
    if isinstance(page_map, dict) and isinstance(page_map.get('pages'), list):
        for page in page_map['pages']:
            if not isinstance(page, dict):
                continue
            for field, root in [('source_path', args.source_root), ('target_path', args.destination)]:
                if isinstance(page.get(field), str):
                    protected.append((root / page[field]).resolve())
    for path in protected:
        if (report == path or report.is_relative_to(path) or path.is_relative_to(report)
                or (report.exists() and path.exists() and report.samefile(path))):
            raise ValueError('Report destination overlaps an input or converted content: ' + str(path))
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', required=True, type=Path)
    parser.add_argument('--page-map', required=True, type=Path)
    parser.add_argument('--destination', required=True, type=Path)
    parser.add_argument('--report', required=True, type=Path)
    parser.add_argument('--source', action='append', default=[])
    args = parser.parse_args(argv)
    page_map = None
    raw_map = None
    input_error = None
    try:
        raw_map = args.page_map.read_bytes()
        page_map = json.loads(raw_map)
    except (OSError, ValueError) as error:
        input_error = error
    try:
        report_path = _report_destination(args, page_map)
    except (OSError, ValueError, RuntimeError) as error:
        # The requested report aliases protected data; writing a JSON failure to
        # that path would itself cause the damage being rejected.
        print('Report destination rejected: ' + str(error), file=sys.stderr)
        return 1
    if input_error is None:
        report = convert_tree(args.source_root, page_map, args.destination, args.source)
    else:
        report = dict(schema_version=1, status='fail', inputs=dict(page_map=str(args.page_map)), checks=[],
                      issues=[dict(id='page-map-input', source_path=None, severity='error', evidence=str(input_error))])
    report['inputs']['page_map_sha256'] = hashlib.sha256(raw_map).hexdigest() if raw_map is not None else None
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    if report['status'] != 'pass':
        for issue in report['issues']:
            print(str(issue.get('source_path')) + ': ' + issue['evidence'], file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
