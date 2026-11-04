"""Extract a semantic comparison baseline from identified legacy HTML.

Code text is HTML-decoded once and written as UTF-8 without trimming or newline
normalization. Paths in text_path are relative to the output JSON's directory.
The optional legacy-provenance.json sidecar in site-dir records how HTML was
obtained. Missing page/article evidence gives an incomplete, nonzero result.
"""
import argparse
from collections import Counter
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import urljoin


class LegacyParser(HTMLParser):
    """Read legacy role=main content plus sidebar navigation, in source order."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.article = False
        self.article_seen = False
        self.ids = []
        self.headings = []
        self.code_blocks = []
        self.tab_panels = []
        self.links = []
        self.images = []
        self.navigation = []
        self.code = None
        self.heading = None
        self.anchor = None
        self.tab = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get('class', '').split()
        is_article = attrs.get('role') == 'main'
        if tag not in {'img', 'br', 'hr', 'meta', 'link', 'input', 'source', 'wbr', 'area', 'base', 'embed', 'param', 'track', 'col'}:
            self.stack.append((tag, is_article))
        if is_article:
            self.article = self.article_seen = True
        if tag == 'a':
            record = {'href': attrs.get('href', ''), 'text': ''}
            if self.article:
                self.links.append(record)
            elif any(t in {'nav', 'aside'} for t, _ in self.stack):
                self.navigation.append(record)
            self.anchor = record
        if not self.article:
            return
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}:
            self.heading = {'level': int(tag[1]), 'id': attrs.get('id'), 'text': ''}
            self.headings.append(self.heading)
        if tag == 'img':
            self.images.append({'src': attrs.get('src', ''), 'alt': attrs.get('alt', '')})
        if 'c-tabs' in classes:
            self.tab = {'code_blocks': [], 'languages': []}
            self.tab_panels.append(self.tab)
        if tag == 'pre':
            self.code = {'language': None, 'text': ''}
            self.code_blocks.append(self.code)
            if self.tab is not None:
                self.tab['code_blocks'].append(len(self.code_blocks) - 1)
        if tag == 'code' and self.code is not None:
            self.code['language'] = next((c.removeprefix('language-') for c in classes if c.startswith('language-')), None)
            if not self.code['language'] and classes:
                self.code['language'] = classes[0]

    def handle_endtag(self, tag):
        if tag == 'pre':
            self.code = None
        if tag in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}:
            self.heading = None
        if tag == 'a':
            self.anchor = None
        # Match a real ancestor, tolerating malformed legacy table markup.
        indices = [i for i, (name, _) in enumerate(self.stack) if name == tag]
        if indices:
            index = indices[-1]
            removed = self.stack[index:]
            del self.stack[index:]
            if any(is_article for _, is_article in removed):
                self.article = False
        if self.tab is not None and tag == 'ul':
            self.tab['languages'] = [self.code_blocks[i]['language'] for i in self.tab['code_blocks']]
            self.tab = None

    def handle_data(self, data):
        if self.code is not None:
            self.code['text'] += data
        if self.heading is not None:
            self.heading['text'] += data
        if self.anchor is not None:
            self.anchor['text'] += data


def capture_site(site_dir, page_map, output_dir):
    site_dir, output_dir = Path(site_dir), Path(output_dir)
    result = {'schema_version': 1, 'status': 'pass', 'site_id': 'legacy-root',
              'inputs': {'source_commit': page_map.get('source_commit'), 'source_kind': page_map.get('source_kind'),
                         'page_map_sha256': hashlib.sha256(json.dumps(page_map, sort_keys=True).encode()).hexdigest()},
              'build_provenance': {}, 'checks': [], 'issues': [], 'pages': {}}
    provenance = site_dir / 'legacy-provenance.json'
    if provenance.exists():
        result['build_provenance'] = json.loads(provenance.read_text())
    if not result['build_provenance'].get('mode') or result['build_provenance'].get('source_commit') != page_map.get('source_commit'):
        result['status'] = 'incomplete'
        result['issues'].append({'id': 'missing-build-provenance', 'url': '/', 'severity': 'error',
                                 'evidence': 'Require legacy-provenance.json with mode and matching source_commit'})
    for page in page_map['pages']:
        if not page['published']:
            continue
        route = page['old_url']
        relative = route.lstrip('/') + 'index.html'
        path = site_dir / relative
        if not path.is_file():
            result['status'] = 'incomplete'
            result['issues'].append({'id': 'missing-rendered-page', 'url': route, 'source_path': page['source_path'],
                                     'severity': 'error', 'evidence': relative})
            continue
        raw = path.read_bytes()
        parser = LegacyParser()
        parser.feed(raw.decode('utf-8'))
        parser.close()
        if not parser.article_seen:
            result['status'] = 'incomplete'
            result['issues'].append({'id': 'missing-article', 'url': route, 'source_path': page['source_path'],
                                     'severity': 'error', 'evidence': 'No role=main article in ' + relative})
        blocks = []
        for index, block in enumerate(parser.code_blocks):
            text_path = 'code/' + (route.strip('/').replace('/', '__') or 'root') + '/%04d.txt' % index
            text_bytes = block['text'].encode('utf-8')
            destination = output_dir / text_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(text_bytes)
            blocks.append({'language': block['language'], 'sha256': hashlib.sha256(text_bytes).hexdigest(),
                           'text_path': text_path, 'byte_length': len(text_bytes), 'index': index})
        for link in parser.links:
            link['resolved_url'] = urljoin(route, link['href'])
        for image in parser.images:
            image['resolved_url'] = urljoin(route, image['src'])
        duplicate_ids = sorted(key for key, count in Counter(parser.ids).items() if count > 1)
        result['pages'][route] = {'source_path': page['source_path'], 'html_path': relative,
            'html_sha256': hashlib.sha256(raw).hexdigest(), 'code_blocks': blocks, 'tab_panels': parser.tab_panels,
            'ids': parser.ids, 'duplicate_ids': duplicate_ids, 'headings': parser.headings,
            'links': parser.links, 'images': parser.images, 'navigation': parser.navigation,
            'known_defects': page.get('exceptions', [])}
    result['checks'].append({'id': 'published-pages-captured', 'expected': sum(bool(p['published']) for p in page_map['pages']),
                             'actual': len(result['pages']), 'status': result['status']})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site-dir', required=True, type=Path)
    parser.add_argument('--page-map', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    result = capture_site(args.site_dir, json.loads(args.page_map.read_text()), args.output.parent)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    raise SystemExit(0 if result['status'] == 'pass' else 1)


if __name__ == '__main__':
    main()
