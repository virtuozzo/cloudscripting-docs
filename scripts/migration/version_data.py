"""Derive theme version data solely from the authoritative pinned manifest."""
from pathlib import Path

from .inventory_releases import validate_manifest, write_yaml


def write_theme_data(manifest: dict, destination: Path) -> None:
    validate_manifest(manifest)
    write_yaml({
        'default_version': manifest['default_version'],
        'releases': [{key: release[key] for key in ('id', 'platform_version', 'output_prefix')}
                     for release in manifest['releases'] if release['publication'] == 'retained'],
    }, destination)
