import os

import click
import mkdocs
from git import Git
import logging


from mkdocs.commands import build
from mkdocs import config

# log = logging.getLogger('mkdocs.cli')
log = logging.getLogger(__name__)

config_file_help = "Provide a specific MkDocs config"
strict_help = ("Enable strict mode. This will cause MkDocs to abort the build "
               "on any warnings.")
site_dir_help = "The directory to output the result of the documentation build."

def _load_config(config_file, strict, site_dir):
    cfg = config.load_config(
        config_file=config_file,
        strict=strict,
        site_dir=site_dir,
        theme='mkdocs'
    )

    # TODO: We should not need to manually update settings like this.
    version_assets = os.path.join(os.path.dirname(__file__), 'assets')

    # Add the assets for the version switcher
    #print(cfg)
    #print("****")
    #print(cfg['theme_dir'])
    #cfg['theme_dir'].append(version_assets)
    #cfg['extra_javascript'].append('mkdocs_versioned/js/version_picker.js')
    return cfg


def _build(cfg, pathspec, tags, site_dir=None):

    c = {
        'extra': {
            'current_version': pathspec,
            'all_versions': tags,
        }
    }

    if site_dir is not None:
        c['site_dir'] = site_dir

    try:
        cfg.load_dict(c)
        build.build(cfg)
    except Exception:
        log.exception("Failed to build '%s'", pathspec)


@click.command()
@click.option('--config-file', type=click.File('rb'), help=config_file_help)
@click.option('--strict', is_flag=True, help=strict_help)
@click.option('--site-dir', type=click.Path(), help=site_dir_help, default='./site/')
@click.option('--tags', '-t', multiple=True)
@click.option('--default', '-d', default='master')
@click.option('--latest', '-l', default='master')


def build_command(config_file, strict, site_dir, tags, default, latest):
    """Build the MkDocs documentation"""

#    cli.configure_logging(level=logging.INFO)
    g = Git()
    tags = tags or g.tag().splitlines()
    log.info("Building %s to /", default)
    # g.checkout(default)

    print("Building %s to /", default)

    _build(_load_config(config_file, strict, site_dir), default, tags)

    # print("Building %s to /latest", latest)
    # log.info("Building %s to /latest", latest)
    # g.checkout(default)
    # _build(_load_config(config_file, strict, site_dir), latest, tags, 'latest')

    for tag in sorted(tags):

        g.checkout(tag)

        if not os.path.exists("mkdocs.yml"):
            log.warning("Unable to build %s, as no mkdocs.yml was found", tag)
            continue

        site_dir = "{0}".format(tag)
        log.info("Building %s to /%s", tag, "site/" + site_dir)
        _build(_load_config(config_file, strict, site_dir), tag, tags, "site/" + site_dir)

    g.checkout(default)
