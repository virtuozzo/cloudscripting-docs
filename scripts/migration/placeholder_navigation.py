"""Independent, finite acceptance rule for the reviewed broken navigation list.

No converter imports. The identity catalog binds each accepted Git file to its
proven seven-line list and the complete immutable captured link sequence. Only
four exact parser-corrupt references are replaced; code expectations are untouched.
"""
import hashlib
import json
from pathlib import Path

ROUTE = '/creating-manifest/placeholders/'
SOURCE = 'docs/creating-manifest/placeholders.md'
LINKS = [
    ('${*.toBase64()}', '#42tobase64'),
    ('${*.fromBase64()}', '#42frombase64'),
    ('${*.md5()}', '#42md5'),
    ('${*.join()}', '#42join'),
    ('${*.toJSON()}', '#42tojson'),
    ('${*.contains()}', '#42contains'),
    ('${*.print()}', '#42print'),
]
IDENTITIES = json.loads(Path(__file__).with_name('placeholder_navigation_identities.json').read_text())['snapshots']


def signature(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def restore_links(baseline, page_map):
    """Return new link expectations only for a completely proven original shape."""
    source = baseline.get('inputs', {}).get('source_commit')
    identity = IDENTITIES.get(source)
    captured = baseline['pages'][ROUTE]
    mapped = [p for p in (page_map or {}).get('pages', []) if p.get('old_url') == ROUTE]
    if (identity is None or (page_map or {}).get('source_commit') != source
            or len(mapped) != 1 or mapped[0].get('source_path') != SOURCE
            or captured.get('source_path') != SOURCE
            or mapped[0].get('source_sha256') != identity['source_sha256']
            or signature(captured.get('links')) != identity['baseline_links_sha256']
            or not {href[1:] for _, href in LINKS} <= set(captured.get('ids', []))):
        raise ValueError('Unreviewed Placeholders source/file/list or baseline reference identity')
    start = identity['corrupt_reference_start']
    original = captured['links']
    if signature(original[start:start+4]) != identity['corrupt_reference_sha256']:
        raise ValueError('Unexpected four captured corrupt navigation references')
    replacement = [dict(href=href, text=label, resolved_url=ROUTE+href) for label, href in LINKS]
    return original[:start] + replacement + original[start+4:]

DESCRIPTIONS = [
    'does data encoding into Base64 format',
    'decodes data from Base64 format',
    'md5 hash generator',
    'concatenates data provided as array of words or objects',
    'converts array of of words or objects into JSON format',
    'allows to find a word or object in the array of words or objects respectively',
    'outputs an array of words or objects to the console',
]


def check_rendered(page, base_url):
    """Independently require one ordered seven-item source-intended navigation list.

    Text normalization is confined to prose layout. Code-block bytes continue
    through the existing strict oracle without any normalization or waiver.
    """
    from urllib.parse import urljoin, urlsplit
    article = page['article']
    headings = [n for n in article.walk() if n.attrs.get('id') == 'data-processing-placeholders'] if article else []
    if len(headings) != 1 or headings[0].tag != 'h2':
        return 'Expected one Data Processing Placeholders section heading'
    heading = headings[0]
    siblings = heading.parent.children
    region = []
    for sibling in siblings[siblings.index(heading)+1:]:
        if not hasattr(sibling, 'tag'):
            continue
        if sibling.tag in {'h1','h2','h3','h4','h5','h6'}:
            break
        region.append(sibling)
    lists = [n for n in region if n.tag == 'ul']
    if len(lists) != 1:
        return 'Expected one seven-function navigation list before the first function heading'
    items = [n for n in lists[0].children if hasattr(n, 'tag')]
    if len(items) != 7 or any(n.tag != 'li' for n in items):
        return 'Expected exactly seven list items'
    canonical_page = urlsplit(base_url + ROUTE.lstrip('/'))
    for index, (item, (label, href), description) in enumerate(zip(items, LINKS, DESCRIPTIONS)):
        anchors = [n for n in item.walk() if n.tag == 'a']
        if not anchors:
            return {'index': index, 'expected_label': label, 'reason': 'Missing function link'}
        anchor = anchors[0]
        codes = [n for n in anchor.walk() if n.tag == 'code']
        target = urlsplit(urljoin(base_url + ROUTE.lstrip('/'), anchor.attrs.get('href', '')))
        if (anchor.text() != label or len(codes) != 1 or codes[0].text() != label
                or target.scheme != canonical_page.scheme or target.netloc != canonical_page.netloc
                or target.path != canonical_page.path or target.query or target.fragment != href[1:]
                or href[1:] not in page['ids']
                or ' '.join(item.text().split()) != label + ' - ' + description):
            return {'index': index, 'expected_label': label, 'expected_target': href,
                    'actual_label': anchor.text(), 'actual_target': anchor.attrs.get('href'),
                    'expected_description': description, 'actual_item_text': item.text()}
    return None
