# coding: utf-8
"""
Discover mkdocs entry points without pkg_resources (stdlib importlib.metadata).

Used when setuptools is not installed and ``import pkg_resources`` fails.
"""
from __future__ import unicode_literals

import sys

from importlib.metadata import distribution, entry_points, distributions


def _dist_key_from_dist(dist):
    name = dist.metadata.get('Name', '') or getattr(dist, 'name', '') or ''
    part = name.split(';')[0].split(',')[0].strip()
    first = part.split()[0] if part else ''
    if first:
        return first.lower().replace('-', '_')
    return getattr(dist, 'name', 'unknown').lower().replace('-', '_')


def _dist_key_for_ep(ep):
    for dist in distributions():
        try:
            des = dist.entry_points
        except Exception:
            continue
        for cand in des:
            if cand.name == ep.name and cand.group == ep.group and cand.value == ep.value:
                return _dist_key_from_dist(dist)
    return 'unknown'


class _CompatDist(object):
    __slots__ = ('key',)

    def __init__(self, key):
        self.key = key


class _CompatEP(object):
    __slots__ = ('_ep', 'name', 'dist')

    def __init__(self, ep, dist_key):
        self._ep = ep
        self.name = ep.name
        self.dist = _CompatDist(dist_key)

    def load(self):
        return self._ep.load()


def get_entry_map(dist=None, group=None):
    """Subset of pkg_resources.get_entry_map(dist=..., group=...)."""
    if dist is None or group is None:
        raise TypeError('dist and group are required')
    d = distribution(dist)
    dk = _dist_key_from_dist(d)
    out = {}
    for ep in d.entry_points:
        if ep.group == group:
            out[ep.name] = _CompatEP(ep, dk)
    return out


def _entry_points_in_group(group):
    if sys.version_info >= (3, 10):
        return entry_points(group=group)
    eps = entry_points()
    if hasattr(eps, 'select'):
        return eps.select(group=group)
    try:
        return eps[group]
    except (KeyError, TypeError):
        return []


def iter_entry_points(group=None):
    """Subset of pkg_resources.iter_entry_points(group=...)."""
    if group is None:
        raise TypeError('group is required')
    for ep in _entry_points_in_group(group):
        yield _CompatEP(ep, _dist_key_for_ep(ep))
