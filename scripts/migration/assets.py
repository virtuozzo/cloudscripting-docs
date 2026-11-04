"""Exact-case, frozen Git image export; never use checkout bytes as assets."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import posixpath
import tempfile
from urllib.parse import urlsplit

from .inventory import _git

ASSET_ROOT = 'theme/readthedocs/img/'
# The pinned theme processes PNG/JPEG only; other formats keep static fallback.
PROCESSABLE = {'.png', '.jpg', '.jpeg'}


def build_asset_map(source_root, revision, page_map, baseline):
    revision = _git(source_root, 'rev-parse', '--verify', revision + '^{commit}').decode().strip()
    tree = _git(source_root, 'ls-tree', '-r', '-z', revision, '--', ASSET_ROOT)
    assets = []
    groups = {}
    for row in tree.split(b'\0'):
        if not row:
            continue
        identity, path = row.split(b'\t', 1)
        mode, kind, blob = identity.decode().split()
        path = path.decode()
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise ValueError('Only regular Git image blobs are supported: ' + path)
        raw = _git(source_root, 'cat-file', 'blob', blob)
        public_url = '/img/' + path.removeprefix(ASSET_ROOT)
        record = {'git_path': path, 'git_blob': blob, 'public_url': public_url,
                  'sha256': hashlib.sha256(raw).hexdigest(), 'byte_length': len(raw),
                  'casefold_collision_group': None, 'bundle_resources': [],
                  'overlay_decision': 'exact-git-no-intentional-overlay'}
        groups.setdefault(path.casefold(), []).append(record)
        assets.append(record)
    for number, group in enumerate(g for _, g in sorted(groups.items()) if len(g) > 1):
        for record in group:
            record['casefold_collision_group'] = 'case-' + str(number + 1).zfill(2)
    for page in page_map['pages']:
        if not page['published']:
            continue
        captured = baseline.get('pages', {}).get(page['old_url'])
        if captured is None:
            raise ValueError('Missing rendered page for asset mapping: ' + page['old_url'])
        images = {urlsplit(image['resolved_url']).path for image in captured.get('images', []) if not urlsplit(image['resolved_url']).scheme and not urlsplit(image['resolved_url']).netloc}
        for record in assets:
            if record['public_url'] not in images or PurePosixPath(record['git_path']).suffix.lower() not in PROCESSABLE:
                continue
            name = hashlib.sha256(record['git_path'].encode()).hexdigest()[:16] + '-' + PurePosixPath(record['git_path']).name
            record['bundle_resources'].append({'page_url': page['old_url'], 'target_path': str(PurePosixPath(page['target_path']).parent / name), 'name': name, 'relative_url': posixpath.relpath(record['public_url'], page['old_url'])})
    return {'schema_version': 1, 'source_commit': revision, 'source_kind': 'git',
            'overlay_policy': 'D05: preserve workspace separately; export exact-case Git blobs', 'assets': assets}


def require_case_sensitive(destination):
    destination = Path(destination)
    existing = destination
    while not existing.exists():
        existing = existing.parent
    with tempfile.TemporaryDirectory(prefix='.asset-case-probe-', dir=existing) as directory:
        probe = Path(directory) / 'case-sensitive'
        probe.write_bytes(b'probe')
        if probe.with_name('CASE-SENSITIVE').exists():
            raise ValueError('Asset export requires a case-sensitive filesystem (Linux or case-sensitive APFS); destination: ' + str(destination))


def _safe_path(value):
    path = PurePosixPath(value)
    if path.is_absolute() or '..' in path.parts or not path.parts:
        raise ValueError('Unsafe asset destination: ' + value)
    return path


def materialize(source_root: Path, asset_map: dict, destination: Path) -> None:
    destination = Path(destination).resolve()
    require_case_sensitive(destination)
    outputs = []
    resources = []
    seen = set()
    # Verify every object and destination before creating any image outputs.
    for record in asset_map['assets']:
        raw = _git(source_root, 'cat-file', 'blob', record['git_blob'])
        if hashlib.sha256(raw).hexdigest() != record['sha256']:
            raise ValueError('Git asset SHA-256 mismatch: ' + record['git_path'])
        public = record['public_url']
        if not public.startswith('/img/'):
            raise ValueError('Asset compatibility URL must be under /img/: ' + public)
        targets = ['static/' + public.lstrip('/')]
        for resource in record.get('bundle_resources', []):
            targets.append(resource['target_path'])
            resources.append({'git_path': record['git_path'], 'public_url': public, 'sha256': record['sha256'], **resource})
        for target in targets:
            safe = _safe_path(target)
            if str(safe) in seen:
                raise ValueError('Duplicate asset output: ' + str(safe))
            seen.add(str(safe))
            path = destination / safe
            if any((destination / Path(*safe.parts[:index])).is_symlink() for index in range(1, len(safe.parts) + 1)):
                raise ValueError('Symlink asset destination is not supported: ' + str(path))
            outputs.append((path, raw))
    for path, raw in outputs:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / 'bundle-resources.json').write_text(json.dumps({'schema_version': 1, 'source_commit': asset_map.get('source_commit'), 'resources': resources}, indent=2) + '\n')


def snapshot_workspace(source_root, asset_map, destination):
    """Separate checkout observations from exact-case frozen asset identities."""
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    records = []
    for record in asset_map['assets']:
        source = Path(source_root) / record['git_path']
        if not source.is_file():
            records.append({'git_path': record['git_path'], 'status': 'missing'})
            continue
        raw = source.read_bytes()
        name = hashlib.sha256(record['git_path'].encode()).hexdigest() + '.bin'
        (destination / name).write_bytes(raw)
        records.append({'git_path': record['git_path'], 'sha256': hashlib.sha256(raw).hexdigest(), 'snapshot': name})
    (destination / 'snapshot.json').write_text(json.dumps({'schema_version': 1, 'observations': records}, indent=2) + '\n')
    return records
