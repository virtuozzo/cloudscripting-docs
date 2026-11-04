"""Inventory editorial sources without trusting YAML constructors or checkout case.

Run ``uv run --locked python -m scripts.migration.inventory --source-root . --revision SHA
--output migration/page-map.json``. A revision always reads Git objects, never
working-tree bytes. Omitting it explicitly inventories the working tree.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess

import yaml


class InventoryLoader(yaml.SafeLoader):
    """Only the one existing PyMdown name is allowed, as an inert string."""


def _emoji_name(loader, node):
    if loader.construct_scalar(node):
        raise ValueError('The legacy emoji name tag must have an empty value')
    return 'pymdownx.emoji.to_svg'


InventoryLoader.add_constructor('tag:yaml.org,2002:python/name:pymdownx.emoji.to_svg', _emoji_name)


def load_config(text):
    try:
        config = yaml.load(text, Loader=InventoryLoader)
    except yaml.YAMLError as error:
        raise ValueError('Unsupported or invalid YAML: ' + str(error)) from error
    if not isinstance(config, dict):
        raise ValueError('Expected a configuration mapping')
    return config


def _git(root, *args):
    """Read local frozen objects without replacement refs, fetching, or optional locks."""
    environment = {**os.environ, 'GIT_NO_LAZY_FETCH': '1', 'GIT_OPTIONAL_LOCKS': '0'}
    return subprocess.check_output(
        ['git', '--no-replace-objects', '-C', str(root), *args], env=environment
    )


def _slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def build_inventory(source_root, revision=None):
    root = Path(source_root)
    if revision:
        revision = _git(root, 'rev-parse', '--verify', revision + '^{commit}').decode().strip()
        paths = _git(root, 'ls-tree', '-r', '--name-only', '-z', revision, '--', 'docs/').decode().split('\0')
        read = lambda path: _git(root, 'show', revision + ':' + path)
    else:
        paths = [p.relative_to(root).as_posix() for p in (root / 'docs').rglob('*.md')]
        read = lambda path: (root / path).read_bytes()
    paths = sorted(p for p in paths if p.endswith('.md') and not p.startswith('docs/superpowers/'))
    config = load_config(read('mkdocs.yml').decode('utf-8-sig'))
    configured = {}
    weight = 0

    def navigation(items, parent=None):
        nonlocal weight
        nodes = []
        for item in items:
            if isinstance(item, str):
                label, value = PurePosixPath(item).stem.replace('-', ' ').title(), item
            elif isinstance(item, dict) and len(item) == 1:
                label, value = next(iter(item.items()))
            else:
                raise ValueError('Navigation entries must be paths or single-key mappings')
            node_id = _slug(label) if isinstance(value, list) else 'page-' + _slug(str(PurePosixPath(value).with_suffix('')))
            weight += 10
            node = {'title': label, 'menu_id': node_id, 'menu_parent': parent, 'weight': weight}
            if isinstance(value, list):
                node['children'] = navigation(value, node_id)
            elif isinstance(value, str):
                path = 'docs/' + value
                if path not in paths:
                    raise ValueError('Configured page is missing or excluded: ' + path)
                if path in configured:
                    raise ValueError('Configured page appears twice: ' + path)
                node['source_path'] = path
                configured[path] = node
            else:
                raise ValueError('Navigation value must be a list or a path')
            nodes.append(node)
        return nodes

    nav = navigation(config.get('pages', []))
    records = []
    for path in paths:
        raw = read(path)
        source = raw.decode('utf-8-sig')
        entry = configured.get(path)
        title = re.search(r'^(?:#{1,6}\s+(.+?)\s*#*\s*$|<h1[^>]*>(.*?)</h1>)', source, re.M | re.I)
        title = (title.group(1) or title.group(2)).strip() if title else PurePosixPath(path).stem.replace('-', ' ').title()
        relative = PurePosixPath(path).relative_to('docs').with_suffix('')
        route = '/' + str(relative) + '/'
        target = 'content/' + str(relative) + '/index.md'
        if relative.name == 'index':
            route = '/' if str(relative) == 'index' else '/' + str(relative.parent) + '/'
            target = 'content/_index.md' if str(relative) == 'index' else 'content/' + str(relative.parent) + '/_index.md'
        exceptions = []
        if re.search(r'^!!!Note\b', source, re.M):
            exceptions.append('legacy-malformed-note')
        if path == 'docs/samples.md':
            exceptions.append('legacy-duplicate-sample-ids')
        if path == 'docs/creating-manifest/visual-settings.md':
            exceptions.append('legacy-unresolved-source-links')
        records.append({
            'source_path': path, 'source_sha256': hashlib.sha256(raw).hexdigest(),
            'published': bool(entry), 'disposition': 'retain' if entry else 'pending',
            'old_url': route if entry else None, 'target_path': target if entry else None,
            'title': title, 'nav_title': entry['title'] if entry else None,
            'menu_id': entry['menu_id'] if entry else None,
            'menu_parent': entry['menu_parent'] if entry else None,
            'weight': entry['weight'] if entry else None, 'exceptions': exceptions,
        })
    return {'schema_version': 1, 'source_commit': revision, 'source_kind': 'git' if revision else 'worktree',
            'production_base_url': config.get('site_url'), 'navigation': nav, 'pages': records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', required=True, type=Path)
    parser.add_argument('--revision')
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    result = build_inventory(args.source_root, args.revision)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
