"""Assemble validated release slices, then exchange the complete local artifact."""
import ctypes
import errno
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

import jsonschema

from .assets import require_case_sensitive
from .check_artifact import check_artifact
from .check_site import digest, safe_relative, site_digest


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def copy_regular_tree(source, destination, exclude=()):
    """Copy exact-case regular files without following links or overwriting bytes."""
    source, destination = Path(source), Path(destination)
    for path in sorted(source.rglob('*')):
        relative = path.relative_to(source)
        if relative.as_posix() in exclude:
            continue
        if path.is_symlink() or not (path.is_dir() or path.is_file()):
            raise ValueError('Only regular files/directories may be copied: ' + str(path))
        target = destination / relative
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and target.read_bytes() != path.read_bytes():
                raise ValueError('Conflicting output bytes: ' + str(target))
            shutil.copyfile(path, target)


def assemble_artifact(destination, manifest_file, manifest, builds, base_url, kind, provenance):
    """No served bytes are published until every slice and final checker pass."""
    destination = Path(destination)
    if destination.exists():
        raise ValueError('Artifact assembly requires a new empty destination')
    require_case_sensitive(destination)
    wanted = {'root':manifest['root'], **{r['id']:r for r in manifest['releases'] if r['publication']=='retained'}}
    ids = [b['record']['id'] for b in builds]
    if len(ids) != len(set(ids)) or any(i not in wanted for i in ids):
        raise ValueError('Duplicate or undeclared build records')
    for build in builds:
        if build['report'].get('status') != 'pass' or build['report'].get('issues'):
            raise ValueError('Site validation must pass before assembly: ' + build['record']['id'])
    if kind == 'production' and ids != list(wanted):
        raise ValueError('Production assembly requires every retained release in manifest order')
    if kind not in {'production', 'preview'}:
        raise ValueError('Unknown artifact kind')
    prefixes = [b['record']['output_prefix'] for b in builds]
    metadata = dict(schema_version=1, kind=kind, base_url=base_url, manifest_sha256=digest(manifest_file),
                    content_commit=manifest['root']['source_commit'], prefixes=prefixes, builds=[], **provenance)
    destination.mkdir()
    (destination / 'site').mkdir()
    (destination / 'validation').mkdir()
    for build in builds:
        record = build['record']
        prefix = record['output_prefix']
        if prefix and not safe_relative(prefix):
            raise ValueError('Unsafe release prefix')
        if record['id']=='root':
            for path in Path(build['site_dir']).rglob('*'):
                relative = path.relative_to(build['site_dir']).as_posix()
                if any(relative == p.rstrip('/') or relative.startswith(p) for p in prefixes if p):
                    raise ValueError('Root output overlaps a retained release: '+relative)
        copy_regular_tree(build['site_dir'], destination/'site'/prefix)
        report = json.loads(json.dumps(build['report']))
        # The relative path is the sole normalized field. Preserve the checker’s
        # byte binding; recomputing it here could bless changes after validation.
        if report['inputs']['site_sha256'] != site_digest(build['site_dir']):
            raise ValueError('Site bytes changed after validation: '+record['id'])
        report['inputs']['site_dir'] = 'site/'+prefix
        report_path = 'validation/'+record['id']+'.json'
        write_json(destination/report_path, report)
        metadata['builds'].append(dict(id=record['id'], output_prefix=prefix, source_commit=record['source_commit'],
            source_format=record['source_format'], validation_source_commit=build['validation_source_commit'], site_report=report_path))
    schema = Path(__file__).resolve().parents[2]/'migration/schemas/artifact.schema.json'
    try:
        jsonschema.Draft202012Validator(json.loads(schema.read_text())).validate(metadata)
    except jsonschema.ValidationError as error:
        raise ValueError('Artifact schema: '+error.message) from error
    write_json(destination/'artifact.json', metadata)
    files = sorted(p for p in destination.rglob('*') if p.is_file())
    (destination/'checksums.sha256').write_text(''.join(digest(p)+'  '+p.relative_to(destination).as_posix()+'\n' for p in files))
    if kind == 'production':
        result = check_artifact(destination, manifest_file)
        if result['status'] != 'pass':
            raise ValueError('Complete artifact validation failed: '+json.dumps(result['issues']))
    return metadata


def _exchange(left, right):
    """Exchange existing directories atomically when the host supports it."""
    libc = ctypes.CDLL(None, use_errno=True)
    if sys.platform == 'darwin' and hasattr(libc, 'renamex_np'):
        function = libc.renamex_np
        result = function(os.fsencode(left), os.fsencode(right), ctypes.c_uint(2)) # RENAME_SWAP
    elif sys.platform.startswith('linux') and hasattr(libc, 'renameat2'):
        result = libc.renameat2(-100, os.fsencode(left), -100, os.fsencode(right), 2) # RENAME_EXCHANGE
    else:
        return False
    if result == 0:
        return True
    code = ctypes.get_errno()
    if code in {errno.ENOSYS, errno.ENOTSUP, errno.EINVAL, errno.EXDEV}:
        return False
    raise OSError(code, os.strerror(code))


def cleanup_after_publication(path, warnings, phase):
    """Cleanup cannot revoke a committed artifact; retain external-path evidence."""
    try:
        shutil.rmtree(path)
    except Exception as error:
        warnings.append({'phase':phase, 'retained_path':str(path),
                         'detail':str(error), 'backup_state':'cleanup_incomplete'})


def publish_artifact(staging, destination):
    """Initial rename or same-filesystem exchange; recover the portable fallback."""
    staging, destination = Path(staging).resolve(), Path(destination).absolute()
    if destination.is_symlink() or (destination.exists() and not destination.is_dir()):
        raise ValueError('Artifact destination must be a real directory')
    destination.parent.mkdir(parents=True, exist_ok=True)
    if os.stat(staging).st_dev != os.stat(destination.parent).st_dev:
        raise ValueError('Atomic artifact publication requires staging on destination filesystem')
    publication = {'mode':'rename', 'cleanup_warnings':[]}
    if not destination.exists():
        os.replace(staging, destination)
        return publication
    if _exchange(staging, destination):
        publication['mode'] = 'exchange'
        cleanup_after_publication(staging, publication['cleanup_warnings'], 'old-artifact')
        return publication
    # Hosts lacking directory exchange have a brief name gap. Restore the old
    # artifact if installation fails, and report this mode to the caller.
    backup = Path(tempfile.mkdtemp(prefix='.'+destination.name+'-prior-', dir=destination.parent))
    backup.rmdir()
    os.replace(destination, backup)
    try:
        os.replace(staging, destination)
    except BaseException:
        os.replace(backup, destination)
        raise
    publication['mode'] = 'recoverable-rename'
    cleanup_after_publication(backup, publication['cleanup_warnings'], 'old-artifact')
    return publication
