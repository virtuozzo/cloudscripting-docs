import os
import sys
import click
import logging
import mkdocs

from git import Git
from git import Repo
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


def _build(cfg, pathspec, branches, site_dir=None):

    c = {
        'extra': {
            'current_version': pathspec,
            'all_versions': branches,
        }
    }

    if site_dir is not None:
        c['site_dir'] = site_dir

    try:
        cfg.load_dict(c)
        build.build(cfg)
    except Exception:
        log.exception("Failed to build '%s'", pathspec)


def get_logging_level(level):
    if level == 'notset':
        return logging.NOTSET
    elif level == 'debug':
        return logging.DEBUG
    elif level == 'info':
        return logging.INFO
    elif level == 'warning':
        return logging.WARNING
    elif level == 'error':
        return logging.ERROR
    elif level == 'critical':
        return logging.CRITICAL


@click.command()
@click.option('--config-file', type=click.File('rb'), help=config_file_help)
@click.option('--strict', is_flag=True, help=strict_help)
@click.option('--site-dir', type=click.Path(), help=site_dir_help, default='./site/')
@click.option('--branches', '-b', multiple=True)
@click.option('--default', '-d', default='master')
@click.option('--latest', '-l', default='master')
@click.option('--logging-level', default='info')
def build_command(config_file, strict, site_dir, branches, default, latest, logging_level):
    """Build the MkDocs documentation"""

#    cli.configure_logging(level=logging.INFO)
    global release_branches

    logging.basicConfig(
        stream=sys.stdout,
        level=get_logging_level(logging_level),
        format='%(asctime)s %(levelname)s [%(threadName)s] [%(filename)s:%(lineno)d] %(message)s'
    )

    g = Git()
    repo = Repo()

    branches = branches or g.branch('-r').splitlines()
    all_branch_names = list(map(lambda branch: branch.split("origin/")[1], branches))

    print("Branches %s", branches)

    active_branch = repo.active_branch.name
    print("Active branch %s", active_branch)

    if active_branch != default:
        print("Checkout %s", active_branch)
        g.checkout(default)

    default_config = _load_config(config_file, strict, site_dir)

    versions = default_config.get("versions")

    if versions is not None:
        release_branches = versions.keys()

    if release_branches is not None:
        release_branches = sorted(release_branches)
        default_version = release_branches[-1]
        print("Default version %s", default_version)

        print("Building %s to /", default_version)
        _build(default_config, default_version, release_branches)

        for branch in release_branches:
            if branch != default_version and branch in all_branch_names:
                g.checkout(branch)
                g.pull()

                if not os.path.exists("mkdocs.yml"):
                    log.warning("Unable to build %s, as no mkdocs.yml was found", branch)
                    print("Unable to build %s, as no mkdocs.yml was found", branch)
                    continue

                site_dir = "{0}".format(branch)
                log.info("Building %s to /%s", branch, "site/" + site_dir)
                print("Building %s to /%s", branch, "site/" + site_dir)
                _build(_load_config(config_file, strict, site_dir), branch, release_branches, "site/" + site_dir)

        # print("Selected Branches %s", default_config.get("versions").get("releases"))

    print("Checkout branch %s", active_branch)

    g.checkout(active_branch)