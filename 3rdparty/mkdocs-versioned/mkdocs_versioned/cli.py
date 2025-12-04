import functools
import os
import sys
import click
import re
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


def _build(cfg, pathspec, branches, versions, site_dir=None):

    c = {
        'extra': {
            'current_version': pathspec,
            'all_versions': branches,
            'all_virt_versions': versions,
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


def version_compare(version1, version2):
    version_parts1 = str(version1).split('.')
    version_parts2 = str(version2).split('.')
    max_len = max(len(version_parts1), len(version_parts2))

    for i in range(0, max_len):
        part1 = next(iter(version_parts1[i:]), 0)
        part2 = next(iter(version_parts2[i:]), 0)

        if part1 != part2:
            return -1 if part1 > part2 else 1

    return 0


def version_key(version):
    """
    Convert version string like '8.10.1' to a tuple of ints (8, 10, 1)
    so that normal ascending sort gives oldest -> newest.
    """
    return tuple(map(int, str(version).split('.')))

@click.command()
@click.option('--config-file', type=click.File('rb'), help=config_file_help)
@click.option('--strict', is_flag=True, help=strict_help)
@click.option('--site-dir', type=click.Path(), help=site_dir_help, default='./site/')
@click.option('--branches', '-b', multiple=True)
@click.option('--default-branch', '-d', default='master')
@click.option('--latest', '-l', default='master')
@click.option('--logging-level', default='info')
def build_command(config_file, strict, site_dir, branches, default_branch, latest, logging_level):
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

    active_branch = repo.active_branch.name
    print("Active branch %s", active_branch)
    print("Default branch %s", default_branch)
    print("Latest branch %s", latest)

    start_stashes_count = len(re.findall("stash@{[0-9]{1,3}}:", repo.git.stash("list")))
    repo.git.stash("save")

    if active_branch != latest:
        print("Checkout Default %s", active_branch)
        g.checkout(default_branch)

    default_config = _load_config(config_file, strict, site_dir)

    versions = default_config.get("extra").get("versions")

    formatedCSVersions = {}
    virtuozzoVersions = []

    try:
        # Python 2.x
        unicode  # Attempt to access undefined name 'unicode' in Python 3.x will raise a NameError
    except NameError:
        # Python 3.x
        unicode = str  # Define 'unicode' as an alias for 'str' in Python 3.x

    for version in versions:
        formatedCSVersions[unicode(version)] = versions[version]

    if formatedCSVersions is not None:
        release_branches = formatedCSVersions.keys()
        virtuozzoVersions = formatedCSVersions.values()

    if release_branches is not None:
        # Sort branch keys numerically (X.Y.Z): oldest -> newest,
        # then reverse to get newest -> oldest for UI version list.
        sorted_branches = sorted(release_branches, key=version_key)
        release_branches = list(reversed(sorted_branches))
        # Rebuild virtuozzoVersions list in the same order as release_branches
        virtuozzoVersions = [formatedCSVersions[rb] for rb in release_branches]

        # Take the first (newest) version as default
        default_version = release_branches[0] if release_branches else None

        print("Default version %s", default_version)
        print("Building %s to /", default_version)

        _build(default_config, default_version, release_branches, virtuozzoVersions)

        for branch in release_branches:
            if branch in all_branch_names: #branch != default_version and
                g.checkout(branch)
                g.pull()

                if not os.path.exists("mkdocs.yml"):
                    log.warning("Unable to build %s, as no mkdocs.yml was found", branch)
                    print("Unable to build %s, as no mkdocs.yml was found", branch)
                    continue

                site_dir = "{0}".format(branch)
                log.info("Building %s to /%s", branch, "site/" + site_dir)
                print("Building %s to /%s", branch, "site/" + site_dir)
                _build(_load_config(config_file, strict, site_dir), branch, release_branches, virtuozzoVersions, "site/" + site_dir)

        # print("Selected Branches %s", default_config.get("versions").get("releases"))

    print("Checkout branch %s", active_branch)
    g.checkout("master")

    end_stashes_count = len(re.findall("stash@{[0-9]{1,3}}:", repo.git.stash("list")))

    if end_stashes_count > start_stashes_count:
        repo.git.stash("pop")
        print("pop latest stash")
