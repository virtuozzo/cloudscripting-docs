"""Build/serve working Hugo content with frozen exact-case compatibility assets.

These are current-page previews, never complete promotable release artifacts.
"""
import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import signal
import subprocess
import tempfile
from urllib.parse import urlsplit

import yaml

from .assets import build_asset_map, materialize, require_case_sensitive
from .version_data import write_theme_data


def accepted_file(root, relative):
    value = PurePosixPath(relative)
    if value.is_absolute() or '..' in value.parts:
        raise ValueError('unsafe root acceptance input path')
    path = root / value
    parents = [root / Path(*value.parts[:i]) for i in range(1, len(value.parts) + 1)]
    if not path.resolve().is_relative_to(root) or any(p.is_symlink() for p in parents) or not path.is_file():
        raise ValueError('root acceptance input must be a safe regular file: ' + relative)
    return json.loads(path.read_text())


def prepare(source, stage, manifest, catalog, base):
    roots = [record for record in catalog.get('builds', []) if record.get('id') == 'root']
    if catalog.get('schema_version') != 1 or len(roots) != 1:
        raise ValueError('exactly one reviewed root acceptance record is required')
    record = roots[0]
    revision = record.get('validation_source_commit', '')
    if (not re.fullmatch('[0-9a-f]{40}', revision)
            or record.get('source_commit') != manifest['root']['source_commit']):
        raise ValueError('root acceptance source pins do not match the release manifest')
    if manifest['root']['source_format'] != 'hugo':
        raise ValueError('current authoring requires the reviewed Hugo root source pin')
    page_map = accepted_file(source, record['page_map'])
    baseline = accepted_file(source, record['baseline'])
    if page_map.get('source_commit') != revision or baseline.get('inputs', {}).get('source_commit') != revision:
        raise ValueError('root acceptance map/baseline legacy identities differ')
    assets = build_asset_map(source, revision, page_map, baseline)
    materialize(source, assets, stage)
    # Mount working authored files directly. Frozen assets are only fallback
    # resources; differing duplicates require an explicit editorial asset decision.
    for component in ('content', 'static'):
        authored = source / component
        for path in authored.rglob('*'):
            if path.is_symlink() or not (path.is_file() or path.is_dir()):
                raise ValueError('unsupported authored symlink/special file: ' + str(path))
        for generated in (stage / component).rglob('*'):
            if generated.is_file():
                existing = authored / generated.relative_to(stage / component)
                if existing.exists() and (not existing.is_file() or existing.read_bytes() != generated.read_bytes()):
                    raise ValueError('authored asset differs from frozen compatibility/bundle output: ' + str(existing))
    write_theme_data(manifest, stage / 'data/versions.yaml')
    config = yaml.safe_load((source / 'config.yaml').read_text())
    mounts = []
    def mount(path, target, watch=True):
        if path.is_dir():
            mounts.append({'source': str(path), 'target': target, 'disableWatch': not watch})
    mount(source / 'content', 'content')
    mount(stage / 'content', 'content', False)
    mount(source / 'static', 'static')
    mount(stage / 'static', 'static', False)
    mount(stage / 'data', 'data', False)
    mount(source / 'data', 'data')
    mount(source / 'assets', 'assets')
    asset_dir = source / config.get('assetDir', 'assets')
    if asset_dir != source / 'assets':
        mount(asset_dir, 'assets')
    for component in ('layouts', 'i18n', 'archetypes'):
        mount(source / component, component)
    releases = [r for r in manifest['releases'] if r['publication'] == 'retained']
    urls = {'root': base, **{r['id']: manifest['production_base_url'] + r['output_prefix'] for r in releases}}
    overlay = {'module': {'mounts': mounts}, 'resourceDir': str(stage / 'resources'),
               'cacheDir': str(stage / 'cache'), 'params': {'version': manifest['default_version'],
               'defaultVersion': manifest['default_version'], 'csBuildID': 'root',
               'versions': [r['id'] for r in releases], 'csVersionURLs': urls, 'archived': False,
               'errorPage': urlsplit(base).path + '404.html'}}
    overlay_path = stage / 'authoring.json'
    overlay_path.write_text(json.dumps(overlay, indent=2) + '\n')
    return overlay_path, revision, len(assets['assets'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('build', 'serve'))
    parser.add_argument('--source-root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--work-dir', type=Path, default=Path(os.environ.get('CS_BUILD_ROOT', 'build')))
    parser.add_argument('--manifest', type=Path, default=Path('migration/release-sources.yaml'))
    parser.add_argument('--acceptance-catalog', type=Path, default=Path('migration/releases/acceptance.json'))
    parser.add_argument('--hugo', default=os.environ.get('HUGO_BIN', 'hugo'))
    parser.add_argument('--base-url')
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--bind', default='127.0.0.1')
    args = parser.parse_args()
    try:
        source, work = args.source_root.resolve(), args.work_dir.resolve()
        if work == source or (work.is_relative_to(source) and not work.is_relative_to(source / 'build')):
            raise ValueError('authoring work directory must be outside sources or under the ignored build/ directory')
        if not 1 <= args.port <= 65535:
            raise ValueError('port must be between 1 and 65535')
        require_case_sensitive(work)
        work.mkdir(parents=True, exist_ok=True)
        manifest_path = args.manifest if args.manifest.is_absolute() else source / args.manifest
        catalog_path = args.acceptance_catalog if args.acceptance_catalog.is_absolute() else source / args.acceptance_catalog
        manifest = yaml.safe_load(manifest_path.read_text())
        catalog = json.loads(catalog_path.read_text())
        version = subprocess.run([args.hugo, 'version'], check=True, capture_output=True, text=True).stdout
        if not re.search(r'\bv0\.124\.1(?:-[0-9a-f]+)?\+extended(?=\s|$)', version):
            raise ValueError('Hugo Extended 0.124.1 is required')
        base = args.base_url or manifest['production_base_url']
        codespace = os.environ.get('CODESPACE_NAME')
        if args.operation == 'serve' and not args.base_url:
            base = ('https://' + codespace + '-' + str(args.port) + '.app.github.dev/' if codespace
                    else 'http://127.0.0.1:' + str(args.port) + '/')
        if not base.endswith('/') or urlsplit(base).scheme not in ('http', 'https') or not urlsplit(base).netloc:
            raise ValueError('base URL must be an absolute HTTP(S) URL ending with /')
        destination = work / 'current-site'
        marker = work / 'current-preview.json'
        if destination.exists() or destination.is_symlink():
            owner = json.loads(marker.read_text()) if marker.is_file() and not marker.is_symlink() else {}
            if (destination.is_symlink() or not destination.is_dir() or owner.get('kind') != 'preview'
                    or owner.get('source_dir') != str(source) or owner.get('site_dir') != str(destination)):
                raise ValueError('existing output is not an owned preview; choose a new task-specific work directory')
        with tempfile.TemporaryDirectory(prefix='cs-authoring-', dir=work) as temporary:
            overlay, reference, count = prepare(source, Path(temporary), manifest, catalog, base)
            report = {'schema_version': 1, 'kind': 'preview', 'source_kind': 'worktree',
                      'source_dir': str(source), 'validation_source_commit': reference, 'compatibility_assets': count,
                      'drafts': args.operation == 'serve', 'base_url': base, 'site_dir': str(destination)}
            (work / 'current-preview.json').write_text(json.dumps(report, indent=2) + '\n')
            command = [args.hugo] + (['server'] if args.operation == 'serve' else [])
            command += ['--source', str(source), '--config', 'config.yaml,' + str(overlay),
                        '--baseURL', base, '--destination', str(destination), '--cleanDestinationDir']
            if args.operation == 'serve':
                command += ['--port', str(args.port), '--bind', args.bind, '--buildDrafts', '--watch', '--disableFastRender']
                if codespace:
                    command += ['--appendPort=false', '--liveReloadPort', '443']
            process = subprocess.Popen(command)
            def stop(signum, frame):
                process.terminate()
            previous = signal.signal(signal.SIGTERM, stop)
            try:
                returncode = process.wait()
            except KeyboardInterrupt:
                process.terminate()
                returncode = process.wait()
            finally:
                signal.signal(signal.SIGTERM, previous)
            if returncode:
                raise ValueError('Hugo authoring command failed with exit ' + str(returncode))
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError, yaml.YAMLError) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
