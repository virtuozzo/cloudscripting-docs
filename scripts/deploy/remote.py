"""Sent over SSH stdin; stdlib transaction for confirmed symlink deployments.

This executes only after host evidence, local full validation and remote preflight.
It preserves backups and the previous tree; it never changes server configuration.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import uuid


def digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b''):
            value.update(chunk)
    return value.hexdigest()


def safe_path(value):
    return (isinstance(value, str) and value and not value.startswith('/')
            and not any(ord(c) < 32 or c == '\\' for c in value)
            and all(part not in ('', '.', '..') for part in value.split('/')))


def unpack(archive, destination):
    """Inspect every entry before writing any; never delegate path handling to tar."""
    with tarfile.open(archive, 'r:gz') as source:
        members = source.getmembers()
        seen = set()
        for member in members:
            name = member.name.rstrip('/') if member.isdir() else member.name
            allowed = name in ('site', 'validation') or name.startswith(('site/', 'validation/'))
            allowed = allowed or name in ('artifact.json', 'checksums.sha256')
            if (not safe_path(name) or not allowed or name in seen
                    or not (member.isfile() or member.isdir())):
                raise ValueError('archive-member: unsafe, duplicate or unexpected member ' + repr(member.name))
            seen.add(name)
        # Distinct case-only directory names also need distinct storage, even
        # when their leaf filenames differ and exclusive file creation succeeds.
        names = set(seen)
        for name in tuple(names):
            parts = name.split('/')
            names.update('/'.join(parts[:i]) for i in range(1, len(parts)))
        if len({name.casefold() for name in names}) != len(names):
            probe = destination / '.cs-CaseProbe'
            probe.write_bytes(b'probe')
            insensitive = probe.with_name('.cs-caseprobe').exists()
            probe.unlink()
            if insensitive:
                raise ValueError('archive-member: case-sensitive extraction storage required')
        files = {m.name for m in members if m.isfile()}
        for name in seen:
            parts = name.split('/')
            if any('/'.join(parts[:i]) in files for i in range(1, len(parts))):
                raise ValueError('archive-member: file used as an ancestor ' + repr(name))
        for member in members:
            path = destination / member.name
            if member.isdir():
                path.mkdir(parents=True, exist_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                try:
                    with path.open('xb') as output, source.extractfile(member) as content:
                        shutil.copyfileobj(content, output)
                except FileExistsError as error:
                    raise ValueError('archive-member: case-sensitive extraction storage required') from error


def regular_inventory(root):
    result = {}
    for path in root.rglob('*'):
        if path.is_symlink() or not (path.is_dir() or path.is_file()):
            raise ValueError('unsupported symlink/special node in served/config tree')
        if path.is_file():
            result[path.relative_to(root).as_posix()] = digest(path)
    return result


def preflight(config):
    public = Path(config['public_path'])
    roots = [Path(config[key]) for key in ('release_root', 'upload_root', 'backup_root', 'config_snapshot_root')]
    # Reject symlinked roots and ancestors; private roots must already be provisioned.
    for path in roots + [public.parent]:
        if not path.is_dir() or any(part.is_symlink() for part in [path, *path.parents]):
            raise ValueError('host operational roots must be existing real directories without symlink ancestors')
    for tool in ('tar', 'cp'):
        version = subprocess.run([tool, '--version'], text=True, capture_output=True, check=True).stdout
        if 'GNU' not in version:
            raise ValueError('GNU ' + tool + ' required for reviewed metadata-preserving operations')
    if roots[0].stat().st_dev != public.parent.stat().st_dev:
        raise ValueError('public pointer and release root must share one filesystem')
    # Probe instead of trusting a platform name or a configured declaration.
    with tempfile.TemporaryDirectory(prefix='cs-case-', dir=roots[0]) as temporary:
        probe = Path(temporary) / 'CaseProbe'
        probe.write_bytes(b'case-sensitive')
        if probe.with_name('caseprobe').exists():
            raise ValueError('case-sensitive host storage required')
    previous = None
    if config['strategy'] == 'initial-symlink':
        if public.exists() or public.is_symlink():
            raise ValueError('initial install requires a confirmed absent public path')
    else:
        if not public.is_symlink() or public.resolve() != Path(config['expected_current_target']):
            raise ValueError('public pointer changed or is not the confirmed existing symlink')
        previous = public.resolve()
        if not previous.is_dir() or any(p.is_symlink() for p in [previous, *previous.parents]):
            raise ValueError('previous target must be a real directory with no symlink ancestors')
        if previous == public.parent or previous in public.parent.parents:
            raise ValueError('previous target must not include public pointer')
        for root in roots[1:]:
            if previous == root or previous in root.parents or root in previous.parents:
                raise ValueError('previous target overlaps private upload, backup or config roots')
    current = regular_inventory(previous) if previous else {}
    files = set(config['artifact_files'])
    managed = {entry['path']: entry['sha256'] for entry in config['managed_files']}
    retired = {entry['path']: entry['sha256'] for entry in config['retired_files']}
    if set(managed) & set(retired):
        raise ValueError('managed and retired inventories overlap')
    for name in managed:
        if any(name == f or name.startswith(f + '/') or f.startswith(name + '/') for f in files):
            raise ValueError('managed file collides with accepted artifact')
    for name, expected in {**managed, **retired}.items():
        if current.get(name) != expected:
            raise ValueError('managed/retired inventory does not match current served bytes: ' + name)
    if set(current) - files - set(managed) - set(retired):
        raise ValueError('unaccounted non-artifact served files require a managed/retired disposition')
    regular_inventory(roots[3])
    total = config['archive_bytes'] * 5 + sum((previous / name).stat().st_size for name in current) * 2 if previous else config['archive_bytes'] * 5
    if any(shutil.disk_usage(root).free < total for root in roots[:3]):
        raise ValueError('insufficient free space for archive, release and verified backup')
    return previous, current


def check_received(root):
    lines = (root / 'checksums.sha256').read_text().splitlines()
    listed = {}
    for line in lines:
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        if not match or not safe_path(match[2]) or match[2] in listed or match[2] == 'checksums.sha256':
            raise ValueError('invalid received checksum inventory')
        listed[match[2]] = match[1]
    actual = regular_inventory(root)
    actual.pop('checksums.sha256', None)
    if actual != listed:
        raise ValueError('received artifact inventory or checksums differ')
    return actual


def backup_tree(source, output):
    subprocess.run(['tar', '--acls', '--xattrs', '--numeric-owner', '-cpf', str(output), '-C', str(source), '.'], check=True)
    subprocess.run(['tar', '--acls', '--xattrs', '--compare', '-f', str(output), '-C', str(source)], check=True)


def deploy(config):
    previous, current = preflight(config)
    public = Path(config['public_path'])
    upload = Path(config['session'])
    if upload.parent != Path(config['upload_root']) or not upload.is_dir() or upload.is_symlink():
        raise ValueError('invalid private upload session')
    archive = upload / 'artifact.tar.gz'
    if archive.is_symlink() or digest(archive) != config['archive_sha256']:
        raise ValueError('received archive digest mismatch before extraction')
    unpacked = upload / 'unpacked'
    unpacked.mkdir()
    unpack(archive, unpacked)
    inventory = check_received(unpacked)
    # Local check_artifact already bound semantic reports, manifest and provenance
    # to this exact archive. No second build or local override is allowed here.
    site_files = {name[5:]: value for name, value in inventory.items() if name.startswith('site/')}
    if set(site_files) != set(config['artifact_files']):
        raise ValueError('received site inventory differs from local verified archive')
    release = Path(config['release_root']) / config['archive_sha256']
    if release.exists() or release.is_symlink():
        raise ValueError('immutable release directory already exists; inspect before retrying')
    backup = Path(tempfile.mkdtemp(prefix=config['archive_sha256'][:12] + '-', dir=config['backup_root']))
    if previous:
        backup_tree(previous, backup / 'served.tar')
    backup_tree(Path(config['config_snapshot_root']), backup / 'config.tar')
    backups = {p.name: digest(p) for p in backup.glob('*.tar')}
    (backup / 'SHA256SUMS').write_text(''.join(value + '  ' + name + '\n' for name, value in sorted(backups.items())))
    (backup / 'served-files.json').write_text(json.dumps(current, indent=2) + '\n')
    shutil.copytree(unpacked / 'site', release)
    for entry in config['managed_files']:
        subprocess.run(['cp', '-a', '--parents', '--', entry['path'], str(release)], cwd=previous, check=True)
    combined = regular_inventory(release)
    wanted = dict(site_files, **{e['path']: e['sha256'] for e in config['managed_files']})
    if combined != wanted:
        raise ValueError('prepared release differs from artifact plus confirmed managed overlay')
    # Recheck the live tree/pointer immediately before switching. Owner must keep
    # configured writers quiesced for the entire transaction.
    again, latest = preflight(config)
    if again != previous or latest != current:
        raise ValueError('served tree changed during preparation')
    receipt = {'schema_version': 1, 'status': 'prepared', 'archive_sha256': config['archive_sha256'],
               'previous_target': str(previous) if previous else None, 'release': str(release),
               'backup': str(backup), 'backup_sha256': backups,
               'combined_files': combined, 'hosting_acceptance': 'pending-operator-http-browser-checks'}
    record = backup / 'deployment.json'
    record.write_text(json.dumps(receipt, indent=2) + '\n')
    next_pointer = public.with_name('.' + public.name + '-' + uuid.uuid4().hex)
    switched = False
    try:
        if previous:
            next_pointer.symlink_to(release, target_is_directory=True)
            os.replace(next_pointer, public)
        else:
            # symlink creation refuses an unexpected existing path; no overwrite.
            public.symlink_to(release, target_is_directory=True)
        switched = True
        if public.resolve() != release:
            raise ValueError('public pointer verification failed')
        receipt['status'] = 'switched'
        record.write_text(json.dumps(receipt, indent=2) + '\n')
    except Exception:
        if switched and public.is_symlink() and public.resolve() == release:
            if previous:
                next_pointer.unlink(missing_ok=True)
                next_pointer.symlink_to(previous, target_is_directory=True)
                os.replace(next_pointer, public)
            else:
                public.unlink()
        raise
    finally:
        next_pointer.unlink(missing_ok=True)
    return {key: value for key, value in receipt.items() if key != 'combined_files'}


def main():
    config = globals().get('DELIVERY_CONFIG') or json.loads(sys.argv[1])
    # One host-side lock covers preflight and commit operations separately. A
    # changed expected target is rejected again before the public pointer moves.
    lock = Path(config['release_root']) / '.cloudscripting-delivery.lock'
    descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        os.close(descriptor)
        if config['operation'] == 'preflight':
            preflight(config)
            session = tempfile.mkdtemp(prefix='cs-' + config['archive_sha256'][:12] + '-', dir=config['upload_root'])
            print(json.dumps({'session': session}))
        elif config['operation'] == 'deploy':
            print(json.dumps(deploy(config)))
        else:
            raise ValueError('unknown remote operation')
    finally:
        lock.unlink()


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
