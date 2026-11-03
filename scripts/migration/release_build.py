"""Build isolated pinned Hugo releases using captured acceptance evidence only.

All source reads use local immutable Git objects. The sole acceptance catalog
maps build IDs to reviewed maps/baselines/exceptions relative to the tooling repo.
No legacy runtime, branch checkout, fetching, or contributor-tree writes occur.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import html
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit

import yaml

from .assemble_artifact import assemble_artifact, cleanup_after_publication, copy_regular_tree, publish_artifact, write_json
from .assets import build_asset_map, materialize, require_case_sensitive
from .check_artifact import THEME
from .check_site import check_site, digest, safe_relative
from .convert import convert_tree
from .markdown_converter import LEGACY_CORRESPONDENCE_TEMPLATES, _SUPPORTED_CORRESPONDENCE_TEMPLATES
from .inventory import _git, build_inventory
from .inventory_releases import check_production_completeness, validate_manifest
from .prepare_content import prepare
from .version_data import write_theme_data

REPO = Path(__file__).resolve().parents[2]
SHA = re.compile(r'[0-9a-f]{40}')


class IncompleteInputs(ValueError):
    """A reviewed publication or captured acceptance input is still missing."""


def select_builds(manifest, release=None):
    validate_manifest(manifest)
    records = [dict(manifest['root'], id='root')]+[dict(r) for r in manifest['releases'] if r['publication']=='retained']
    prefixes = []
    for record in records:
        prefix = record['output_prefix']
        if prefix:
            if not safe_relative(prefix) or unquote(prefix) != prefix or not prefix.endswith('/'):
                raise ValueError('Unsafe release output prefix: '+prefix)
            if any(prefix.startswith(p) or p.startswith(prefix) for p in prefixes):
                raise ValueError('Overlapping release prefixes: '+prefix)
            prefixes.append(prefix)
    if release is not None:
        matches = [r for r in records if r['id']==release]
        if not matches:
            raise ValueError('Unknown --release ID: '+release)
        return matches
    return records


def export_tree(repo, revision, destination, paths=None):
    """Export exact regular Git blobs; reject links/traversal before any writes."""
    if not isinstance(revision, str) or not SHA.fullmatch(revision):
        raise ValueError('Export requires a full immutable commit SHA')
    try:
        resolved = _git(repo, 'rev-parse', '--verify', revision+'^{commit}').decode().strip()
        if resolved != revision:
            raise ValueError('Source object is not the specified commit')
        rows = _git(repo, 'ls-tree', '-r', '-z', revision, '--', *(paths or [])).split(b'\0')
    except subprocess.CalledProcessError as error:
        raise ValueError('Unresolved source object: '+revision) from error
    destination = Path(destination)
    require_case_sensitive(destination)
    planned = []
    for row in rows:
        if not row:
            continue
        identity, raw_path = row.split(b'\t', 1)
        mode, kind, blob = identity.decode().split()
        path = raw_path.decode('utf-8')
        if mode=='160000': # Theme gitlink is applied separately at its exact pin.
            continue
        if mode not in {'100644', '100755'} or kind!='blob':
            raise ValueError('Only regular Git source blobs are allowed: '+path)
        if not safe_relative(path):
            raise ValueError('Unsafe Git source path: '+path)
        planned.append((path, blob, mode))
    if destination.exists() and any(destination.iterdir()):
        raise ValueError('Source export requires an empty destination')
    destination.mkdir(parents=True, exist_ok=True)
    for path, blob, mode in planned:
        target = destination/path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(_git(repo, 'cat-file', 'blob', blob))
        if mode=='100755':
            target.chmod(0o755)
    return destination


def _safe_input(repo, value):
    if not isinstance(value, str) or not safe_relative(value) or value.endswith('/'):
        raise ValueError('Acceptance input must be a safe tooling-root-relative file: '+str(value))
    root = Path(repo).resolve()
    path = root/value
    current = root
    for part in PurePosixPath(value).parts:
        current /= part
        if current.is_symlink():
            raise ValueError('Acceptance inputs must be regular, without symlinks: '+value)
    if not path.is_file() or not path.resolve().is_relative_to(root):
        raise IncompleteInputs('Missing regular acceptance input: '+value)
    return path


def load_acceptance_catalog(repo, catalog_file, records):
    path = Path(catalog_file)
    if not path.is_file() or path.is_symlink():
        raise IncompleteInputs('Missing reviewed acceptance catalog: '+str(path))
    catalog = json.loads(path.read_text())
    if catalog.get('schema_version') != 1 or not isinstance(catalog.get('builds'), list):
        raise ValueError('Acceptance catalog requires schema_version 1 and builds array')
    entries = {}
    for entry in catalog['builds']:
        name = entry.get('id')
        if not isinstance(name, str) or name in entries:
            raise ValueError('Duplicate or invalid acceptance build ID: '+str(name))
        entries[name] = entry
    result = {}
    for record in records:
        name = record['id']
        if name not in entries:
            raise IncompleteInputs('Missing reviewed acceptance inputs for '+name)
        entry = entries[name]
        if entry.get('source_commit') != record['source_commit'] or not SHA.fullmatch(entry.get('validation_source_commit','')):
            raise ValueError('Acceptance source pin mismatch: '+name)
        if record['source_format']=='mkdocs' and entry['validation_source_commit'] != record['source_commit']:
            raise ValueError('MkDocs source and validation pins must match: '+name)
        result[name] = dict(entry, **{key:_safe_input(repo, entry.get(key)) for key in ('page_map','baseline','exceptions')})
    return result


def validate_publication_map(repo, revision, accepted):
    original = build_inventory(repo, revision)
    if accepted.get('source_commit') != revision or accepted.get('source_kind') != 'git' or accepted.get('scope','complete') != 'complete':
        raise IncompleteInputs('Publication map must cover its complete immutable source')
    expected = {p['source_path']:p for p in original['pages']}
    actual = {p['source_path']:p for p in accepted.get('pages',[])}
    if len(actual) != len(accepted.get('pages',[])) or set(actual) != set(expected):
        raise ValueError('Acceptance map changed the source inventory')
    fields = ('source_sha256','published','old_url','target_path','title','nav_title','menu_id','menu_parent','weight')
    for path, page in actual.items():
        if page.get('disposition') in {None, '', 'pending'}:
            raise IncompleteInputs('Unresolved publication disposition: '+path)
        reference = dict(expected[path])
        if page.get('title') != reference.get('title') and path in LEGACY_CORRESPONDENCE_TEMPLATES:
            template = _git(repo, 'show', revision+':'+LEGACY_CORRESPONDENCE_TEMPLATES[path])
            if hashlib.sha256(template).hexdigest() != _SUPPORTED_CORRESPONDENCE_TEMPLATES[path]:
                raise ValueError('Unrecognized pinned correspondence template: '+path)
            heading = re.match(r'<h1 id="[^"]+">([^<]+)</h1>', template.decode('utf-8'))
            if heading is None:
                raise ValueError('Missing literal correspondence title: '+path)
            reference['title'] = html.unescape(heading[1])
        if any(page.get(key) != reference.get(key) for key in fields):
            raise ValueError('Acceptance map changed frozen source metadata: '+path)
    if accepted.get('navigation') != original.get('navigation'):
        raise ValueError('Acceptance map changed frozen navigation')
    return original


def verify_tools(hugo, task):
    version = subprocess.check_output([str(hugo), 'version'], text=True).strip()
    if not re.search(r'\bv0\.124\.1(?:-[0-9a-f]+)?\+extended(?=\s|$)', version):
        raise ValueError('Require Hugo Extended 0.124.1; actual: '+version)
    task_version = subprocess.check_output([str(task), '--version'], text=True).strip()
    if not re.search(r'(?<![\d.])3\.44\.1(?![\d.])', task_version):
        raise ValueError('Require Task 3.44.1; actual: '+task_version)
    return {'hugo':'0.124.1', 'hugo_extended':True, 'task':'3.44.1'}


def build_and_publish(manifest_file, output_dir, work_dir, base_url, build_one, provenance, release=None, jobs=1):
    manifest_file, output_dir, work_dir = map(Path, (manifest_file, output_dir, work_dir))
    if work_dir.resolve().is_relative_to(output_dir.resolve()):
        raise ValueError('Work storage must be outside the artifact directory')
    manifest = yaml.safe_load(manifest_file.read_text())
    records = select_builds(manifest, release)
    if type(jobs) is not int or jobs < 1:
        raise ValueError('--jobs must be a positive integer')
    kind = 'preview' if release is not None or base_url != manifest['production_base_url'] else 'production'
    require_case_sensitive(work_dir)
    require_case_sensitive(output_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(prefix='release-build-', dir=work_dir))
    staging, publication = None, None
    try:
        def run(record):
            return build_one(record, workspace/record['id'])
        with ThreadPoolExecutor(max_workers=jobs) as executor:
            builds = list(executor.map(run, records))
        # Assembly lives beside the destination, so its final rename never crosses
        # devices even when source exports use a separately mounted volume.
        staging = Path(tempfile.mkdtemp(prefix='.'+output_dir.name+'-new-', dir=output_dir.parent))
        staging.rmdir()
        metadata = assemble_artifact(staging, manifest_file, manifest, builds, base_url, kind, provenance)
        checksums_sha256 = digest(staging/'checksums.sha256')
        publication = publish_artifact(staging, output_dir)
        publication['checksums_sha256'] = checksums_sha256
    finally:
        if publication is None:
            # No commit occurred: failure cleanup may fail, but the old artifact
            # is still untouched. Never retry deletion of an exchanged old tree.
            try:
                if staging is not None and staging.exists():
                    shutil.rmtree(staging)
            finally:
                shutil.rmtree(workspace)
        else:
            cleanup_after_publication(workspace, publication['cleanup_warnings'], 'build-workspace')
    return metadata, publication


class ReleaseBuilder:
    def __init__(self, repo, manifest, records, catalog, tooling_commit, tooling, hugo):
        self.repo, self.manifest, self.records, self.catalog = Path(repo), manifest, records, catalog
        self.tooling_commit, self.tooling, self.hugo = tooling_commit, Path(tooling), hugo

    def __call__(self, record, destination):
        destination.mkdir()
        source = export_tree(self.repo, record['source_commit'], destination/'source')
        accepted = self.catalog[record['id']]
        page_map = json.loads(accepted['page_map'].read_text())
        baseline = json.loads(accepted['baseline'].read_text())
        validation_pin = accepted['validation_source_commit']
        if baseline.get('status') != 'pass' or baseline.get('inputs',{}).get('source_commit') != validation_pin:
            raise IncompleteInputs('Baseline does not bind passing legacy reference: '+record['id'])
        validate_publication_map(self.repo, validation_pin, page_map)
        prepared = destination/'prepared'
        prepared.mkdir()
        # Each build gets its own persisted copy of the approved inventory; legacy
        # code text paths stay anchored at the untouched captured baseline file.
        map_file = destination/'page-map.json'
        shutil.copyfile(accepted['page_map'], map_file)
        if record['source_format']=='mkdocs':
            converted = destination/'converted'
            converted.mkdir()
            converted_report = convert_tree(source, page_map, converted)
            write_json(destination/'conversion.json', converted_report)
            if converted_report['status'] != 'pass':
                raise ValueError('Conversion failed for '+record['id']+': '+json.dumps(converted_report['issues']))
            # Preparation reads immutable assets from the original local object
            # database, not a fabricated Git repository inside the source export.
            report = prepare(self.repo, converted, page_map, baseline, prepared, destination/'preparation.json')
            if report['status'] != 'pass':
                raise ValueError('Preparation failed for '+record['id']+': '+json.dumps(report['issues']))
        else:
            asset_map = build_asset_map(self.repo, validation_pin, page_map, baseline)
            materialize(self.repo, asset_map, prepared)
            write_json(prepared/'asset-map.json', asset_map)
            if not (source/'content/_index.md').is_file():
                raise ValueError('Authored Hugo source is missing its homepage')
            copy_regular_tree(source/'content', prepared/'content', exclude=('search.md',))
            if (source/'static').is_dir():
                copy_regular_tree(source/'static', prepared/'static')
        stage = destination/'hugo'
        stage.mkdir()
        # Tooling export contains no article Markdown. All versions use the exact
        # same pinned configuration, hooks, assets and theme, irrespective of age.
        copy_regular_tree(self.tooling, stage)
        copy_regular_tree(prepared/'content', stage/'content')
        if (prepared/'static').is_dir():
            copy_regular_tree(prepared/'static', stage/'static')
        write_theme_data(self.manifest, stage/'data/versions.yaml')
        base = self.base_url+record['output_prefix']
        releases = [r for r in self.manifest['releases'] if r['publication']=='retained']
        versions = {'root':self.base_url, **{r['id']:self.base_url+r['output_prefix'] for r in releases}}
        # Group menus also come from this frozen source's inventory. Never inject
        # current Jelastic/Virtuozzo branding or navigation into an old release.
        groups = []
        def group_menus(nodes):
            for node in nodes:
                if 'children' in node:
                    groups.append(dict(name=node['title'], identifier=node['menu_id'], weight=node['weight'], **({'parent':node['menu_parent']} if node.get('menu_parent') else {})))
                    group_menus(node['children'])
        group_menus(page_map.get('navigation',[]))
        overlay = {'baseURL':base, 'menu':{'docs':groups}, 'params':{
            'version':self.manifest['default_version'] if record['id']=='root' else record['id'],
            'defaultVersion':self.manifest['default_version'],
            'versions':[r['id'] for r in releases],
            'csBuildID':record['id'], 'archived':record['id']!='root',
            'csVersionURLs':versions, 'errorPage':urlsplit(base).path+'404.html'}}
        # Hugo's config merge can retain list-valued base menu nodes; replace the
        # base configuration directly in this isolated build, then overlay params.
        config = yaml.safe_load((stage/'config.yaml').read_text())
        config['menu'] = {'docs':groups}
        (stage/'config.yaml').write_text(yaml.safe_dump(config, sort_keys=False))
        (stage/'release.yaml').write_text(yaml.safe_dump(overlay, sort_keys=False))
        public = destination/'public'
        result = subprocess.run([str(self.hugo), '--source', str(stage), '--config', 'config.yaml,release.yaml', '--destination', str(public), '--baseURL', base], capture_output=True, text=True)
        (destination/'hugo.log').write_text(result.stdout+result.stderr)
        if result.returncode:
            raise ValueError('Hugo failed for '+record['id']+': '+result.stdout+result.stderr)
        report = check_site(accepted['baseline'], map_file, public, base, accepted['exceptions'], prepared/'asset-map.json', archived=record['id']!='root')
        write_json(destination/'validation.json', report)
        if report['status'] != 'pass':
            error_type = IncompleteInputs if report['status']=='incomplete' else ValueError
            raise error_type('Site acceptance failed for '+record['id']+': '+json.dumps(report['issues']))
        return {'record':record, 'site_dir':public, 'report':report, 'validation_source_commit':validation_pin}


def _base_url(value):
    parsed = urlsplit(value)
    if parsed.scheme not in {'http','https'} or not parsed.netloc or parsed.query or parsed.fragment or not value.endswith('/') or parsed.username or parsed.password:
        raise ValueError('--base-url requires an absolute HTTP(S) URL with a final slash')
    if any(part in {'.','..'} for part in unquote(parsed.path).split('/')) or '\\' in value:
        raise ValueError('Unsafe base URL path')
    return value



def destination_inputs(repo, manifest_file, catalog_file, executables=()):
    """Collect consumed paths even when later acceptance preflight will fail."""
    repo = Path(repo).resolve()
    trees = ('.git', 'docs', 'content', 'theme', 'themes', 'scripts', 'layouts',
             'assets', 'static', 'data', 'tests', 'migration/releases', 'migration/schemas')
    paths = [repo/path for path in trees]
    paths.extend(path for path in repo.iterdir() if path.is_file())
    paths.extend(repo/path for path in ('migration/page-map.json', 'migration/asset-map.json',
                 'migration/compatibility-exceptions.json', 'migration/release-sources.yaml'))
    paths.extend((Path(manifest_file), Path(catalog_file)))
    for option in ('--absolute-git-dir', '--git-common-dir'):
        metadata = Path(_git(repo, 'rev-parse', option).decode().strip())
        paths.append(metadata if metadata.is_absolute() else repo/metadata)
    for executable in (*executables, sys.executable):
        found = shutil.which(str(executable))
        if found:
            paths.append(Path(found))
    # Catalog references may live outside the conventional migration directories.
    # Merely collect identities here; full schema/source validation remains later.
    try:
        catalog = json.loads(Path(catalog_file).read_text())
    except (OSError, ValueError):
        catalog = {}
    if isinstance(catalog, dict) and isinstance(catalog.get('builds'), list):
        for entry in catalog['builds']:
            if not isinstance(entry, dict):
                continue
            for name in ('page_map', 'baseline', 'exceptions'):
                value = entry.get(name)
                if not isinstance(value, str) or not safe_relative(value):
                    continue
                path = repo/value
                paths.append(path)
                if name != 'baseline':
                    continue
                try:
                    baseline = json.loads(path.read_text())
                except (OSError, ValueError):
                    continue
                pages = baseline.get('pages', {}) if isinstance(baseline, dict) else {}
                if not isinstance(pages, dict):
                    continue
                for page in pages.values():
                    blocks = page.get('code_blocks', []) if isinstance(page, dict) else []
                    if not isinstance(blocks, list):
                        continue
                    for block in blocks:
                        value = block.get('text_path') if isinstance(block, dict) else None
                        if isinstance(value, str) and '\x00' not in value:
                            paths.append(path.parent/value)
    return list({location for path in paths for location in (path.absolute(), path.resolve())})


def reject_destination_aliases(output, report, protected):
    """Reject path containment and hard links before writing even a failure report."""
    output, report = Path(output).resolve(), Path(report).resolve()
    if report == output or report.is_relative_to(output):
        raise ValueError('--report must be outside the artifact and source inputs')
    for source in protected:
        if output == source or output.is_relative_to(source) or source.is_relative_to(output):
            raise ValueError('--output-dir overlaps source inputs: '+str(source))
        if report == source or report.is_relative_to(source) or source.is_relative_to(report):
            raise ValueError('--report overlaps source inputs: '+str(source))
    if report.exists():
        if not report.is_file():
            raise ValueError('--report must be a regular file')
        stat = report.stat()
        if stat.st_nlink < 2:
            return
        identity = (stat.st_dev, stat.st_ino)
        # Include all prior-artifact files: the report can be an external hard
        # link to a prior served file without sharing any path prefix.
        for source in [*protected, output]:
            files = source.rglob('*') if source.is_dir() else (source,)
            for path in files:
                if path.is_file():
                    stat = path.stat()
                    if (stat.st_dev, stat.st_ino) == identity:
                        raise ValueError('--report aliases source or prior-artifact bytes: '+str(path))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('manifest','output-dir','report'):
        parser.add_argument('--'+name, required=True, type=Path)
    parser.add_argument('--base-url', required=True)
    parser.add_argument('--release', help='root or one retained ID; always a non-promotable preview')
    parser.add_argument('--jobs', type=int, default=1)
    parser.add_argument('--work-dir', type=Path, help='case-sensitive temporary export/build storage (default: beside output)')
    parser.add_argument('--acceptance-catalog', type=Path, default=REPO/'migration/releases/acceptance.json')
    parser.add_argument('--hugo', default=os.environ.get('HUGO', 'hugo'))
    parser.add_argument('--task', default=os.environ.get('TASK', 'task'))
    args = parser.parse_args(argv)
    # Reject report/output aliases before any error reporting can damage inputs.
    output, report_path = args.output_dir.absolute(), args.report.absolute()
    try:
        protected = destination_inputs(REPO, args.manifest, args.acceptance_catalog, (args.hugo, args.task))
        reject_destination_aliases(output, report_path, protected)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.error(str(error))
    report = dict(schema_version=1, status='fail', inputs={'manifest':str(args.manifest), 'base_url':args.base_url}, checks=[], issues=[])
    publication = None
    try:
        base = _base_url(args.base_url)
        manifest = yaml.safe_load(args.manifest.read_text())
        records = select_builds(manifest, args.release)
        if args.jobs < 1:
            raise ValueError('--jobs must be a positive integer')
        production = args.release is None and base == manifest['production_base_url']
        if production:
            preflight = check_production_completeness(REPO, manifest)
            if preflight['status'] != 'pass':
                error_type = IncompleteInputs if preflight['status']=='incomplete' else ValueError
                raise error_type('Production release decisions/source evidence incomplete: '+json.dumps(preflight['issues']))
        catalog = load_acceptance_catalog(REPO, args.acceptance_catalog, records)
        tools = verify_tools(args.hugo, args.task)
        tooling_commit = _git(REPO, 'rev-parse', 'HEAD').decode().strip()
        theme_pin = _git(REPO, 'rev-parse', tooling_commit+':themes').decode().strip()
        if theme_pin != THEME:
            raise ValueError('Tooling must pin the approved immutable theme revision')
        # Refuse to stamp a commit onto uncommitted builder/helper/hook bytes.
        for path in ('scripts', 'layouts', 'assets', 'static', 'config.yaml', 'redirects.htaccess', 'data', 'content/search.md', 'migration/schemas'):
            if _git(REPO, 'status', '--porcelain=v1', '--untracked-files=all', '--', path).strip():
                raise ValueError('Commit tooling inputs before building: '+path)
        work = (args.work_dir or output.parent).resolve()
        if work.is_relative_to(output.resolve()) or any(work==p or work.is_relative_to(p) for p in protected):
            raise ValueError('Work storage overlaps artifact or protected source inputs')
        require_case_sensitive(work)
        work.mkdir(parents=True, exist_ok=True)
        manifest_sha256 = digest(args.manifest)
        tooling_directory = Path(tempfile.mkdtemp(prefix='release-tooling-', dir=work))
        try:
            tooling = tooling_directory/'tooling'
            export_tree(REPO, tooling_commit, tooling, ['config.yaml','redirects.htaccess','layouts','assets','static','data','content/search.md'])
            export_tree(REPO/'themes', THEME, tooling/'themes')
            run = ReleaseBuilder(REPO, manifest, records, catalog, tooling_commit, tooling, args.hugo)
            run.base_url = base
            metadata, publication = build_and_publish(args.manifest, output, work, base, run,
                {'tooling_commit':tooling_commit, 'theme_commit':THEME, 'tools':tools}, args.release, args.jobs)
        finally:
            if publication is None:
                shutil.rmtree(tooling_directory)
            else:
                cleanup_after_publication(tooling_directory, publication['cleanup_warnings'], 'tooling-workspace')
        report['status'] = 'pass'
        report['inputs'].update(manifest_sha256=manifest_sha256, tooling_commit=tooling_commit, theme_commit=THEME, publication_committed=True)
        report['checks'] = [{'id':'artifact-assembly','status':'pass','kind':metadata['kind'], 'builds':len(metadata['builds']), 'publication_mode':publication['mode'], 'checksums_sha256':publication['checksums_sha256']}, {'id':'deployment','status':'not_run'}]
        for warning in publication['cleanup_warnings']:
            report['issues'].append({'id':'post-publication-cleanup', 'source_path':warning['retained_path'], 'severity':'warning', 'evidence':warning})
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError, yaml.YAMLError) as error:
        report['status'] = 'incomplete' if isinstance(error, IncompleteInputs) else 'fail'
        report['issues'].append({'id':'release-build', 'source_path':None, 'severity':'error', 'evidence':str(error)})
    try:
        write_json(report_path, report)
    except OSError as error:
        # After publication, a report error cannot revoke the commit or change
        # artifact layout. Before publication, preserve the original failure.
        report['issues'].append({'id':'external-report-write', 'source_path':str(report_path),
            'severity':'warning' if publication is not None else 'error',
            'evidence':{'report_path':str(report_path), 'artifact_dir':str(output), 'detail':str(error)}})
        try:
            print(json.dumps(report, indent=2, ensure_ascii=False), file=sys.stderr)
        except OSError:
            # If both reporting sinks are unavailable, exit status still reflects
            # the commit outcome; no further writes touch the artifact.
            pass
    return 0 if report['status']=='pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
