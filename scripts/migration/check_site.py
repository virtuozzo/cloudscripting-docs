"""Offline semantic acceptance, independent of conversion and baseline extraction.

A pass describes only inspected files. Browser behavior, HTTP rewrites and hosting
are deliberately reported as not_run. Code is decoded once, never stripped.
"""
import argparse
from collections import Counter
import copy
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import unquote, urljoin, urlsplit
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

from . import placeholder_navigation


VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
CURRENT_COMMIT = '76628f8aa01571fbc348211cb7df726cf408cd17'
CUSTOM_ROUTE = '/creating-manifest/handling-custom-responses/'
# Reviewed source identities: Git c946ae18:migration/reports/task-10/source-render-deltas.json; the group at
# lines 76–100 hashes to 312f82d1b0ba94670f2ade6ccdfa06564e63ccdb9d9fc408b5b9bb257d98cf00.
# Never infer approval from a matching body at an unknown source commit.
HISTORICAL_CUSTOM_SOURCES = {
    '7e4f20f55427bb4edaf179b243de95b52e17aa94': '6ae0e3eb925b7563711516434e72f18cdd7db271db07e61e6a3d61e794016628',
    'b0a8e57823d5f618150324b143085d7b96bdb43a': '6ae0e3eb925b7563711516434e72f18cdd7db271db07e61e6a3d61e794016628',
    '6796d14270567df874729feaff5dac175c80f776': '6ae0e3eb925b7563711516434e72f18cdd7db271db07e61e6a3d61e794016628',
    'a7fff106b6f4d596ee66f6c323e12d33b754a008': '6ae0e3eb925b7563711516434e72f18cdd7db271db07e61e6a3d61e794016628',
    'e8974d16e2e3c6c929be570207de5a920984e8f3': '6ae0e3eb925b7563711516434e72f18cdd7db271db07e61e6a3d61e794016628',
    '39f8f40875b4dc8ccea281970f1ee7cf8629b582': '6ae0e3eb925b7563711516434e72f18cdd7db271db07e61e6a3d61e794016628',
    '3c756a455536ec4afa0358c8f1098dc4851a070b': '6ae0e3eb925b7563711516434e72f18cdd7db271db07e61e6a3d61e794016628',
    '2138f28f0ca0060ba9ec0de103ab1d3044d1b8ff': '6ae0e3eb925b7563711516434e72f18cdd7db271db07e61e6a3d61e794016628',
    'd883abdd7de63803706aa6918898480308d77d77': '6ae0e3eb925b7563711516434e72f18cdd7db271db07e61e6a3d61e794016628',
    '21e3d40f674a025246af114c062bf256eaee3cc9': '6ae0e3eb925b7563711516434e72f18cdd7db271db07e61e6a3d61e794016628',
    '9d35916829f4eb61f915944c39ba8968cc3ae802': '6ae0e3eb925b7563711516434e72f18cdd7db271db07e61e6a3d61e794016628',
    'b62d8010231d83eefa01a388191501672a181d60': '6ae0e3eb925b7563711516434e72f18cdd7db271db07e61e6a3d61e794016628',
    '709c2837f56c90f70f19f7d38e1042d28840314c': '4856f3a6b81acba2523e3d051802899599cbb0e9be7ae8f28c783952e7cd0cb7',
    '8c056373bffac2e2a02c3b5bc008180baf5ac4d7': '4856f3a6b81acba2523e3d051802899599cbb0e9be7ae8f28c783952e7cd0cb7',
    '57790a31e4207414f9d3ae26c0900cabfa6e4df2': '4856f3a6b81acba2523e3d051802899599cbb0e9be7ae8f28c783952e7cd0cb7',
    'ec693cc290fc24cd995c4ae5108ac3f350884e94': '4856f3a6b81acba2523e3d051802899599cbb0e9be7ae8f28c783952e7cd0cb7',
    'c9cbe7503b7055516d5772be912316f8cd2263e2': '4856f3a6b81acba2523e3d051802899599cbb0e9be7ae8f28c783952e7cd0cb7',
    '1643f00f8e5e053f43fb3dd52bde2d1f864b0c9f': '4856f3a6b81acba2523e3d051802899599cbb0e9be7ae8f28c783952e7cd0cb7',
    '6e0617cb49da66acf10335f613fcfd80820515e3': '4856f3a6b81acba2523e3d051802899599cbb0e9be7ae8f28c783952e7cd0cb7',
}
HISTORICAL_CUSTOM_BASELINE = '9a2c794c685ed892e81ecc2cbe2be4f224c73a834903d75bc34e1283d97b74d2'
RESTORED = [
    ('yaml', 'type: update\nname: response handlers\n\nonInstall:\n  return:\n    result: warning\n    message: Warning!\n    email: string\n'),
    ('json', '{\n    "type": "update",\n    "name": "response handlers",\n    "onInstall": {\n        "return": {\n          "result": "warning",\n          "message": "Warning!",\n          "email": "string"\n        }\n    }\n}\n'),
]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def site_digest(root, exclude_prefixes=()):
    root=Path(root)
    lines=[]
    for p in sorted(root.rglob('*'),key=lambda p:p.relative_to(root).as_posix()):
        relative=p.relative_to(root).as_posix()
        if p.is_file() and not p.is_symlink() and not any(relative.startswith(x) for x in exclude_prefixes):
            lines.append(digest(p)+'  '+relative+'\n')
    return hashlib.sha256(''.join(lines).encode('utf-8')).hexdigest()


def safe_relative(value):
    """Reject platform ambiguities before joining any untrusted output path."""
    value = unquote(str(value))
    return bool(value) and not value.startswith('/') and '\\' not in value and not any(c in value for c in ('\x00','\n','\r')) and all(p not in {'..', '.', ''} for p in value.rstrip('/').split('/'))


class Node:
    def __init__(self, tag='', attrs=None, parent=None):
        self.tag, self.attrs, self.parent, self.children = tag, dict(attrs or []), parent, []

    @property
    def classes(self):
        return self.attrs.get('class', '').split()

    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()

    def text(self, skip=()):
        if set(self.classes) & set(skip):
            return ''
        return ''.join(c.text(skip) if isinstance(c, Node) else c for c in self.children)

    def ancestor(self, predicate):
        n = self.parent
        while n is not None:
            if predicate(n):
                return n
            n = n.parent
        return None


class SiteHTML(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.root = self.current = Node()
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.current)
        self.current.children.append(n)
        if tag not in VOID:
            self.current = n

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        n = self.current
        while n.parent is not None:
            if n.tag == tag:
                self.current = n.parent
                return
            n = n.parent

    def handle_data(self, text):
        self.current.children.append(text)


def _visible(node):
    while node is not None:
        if 'hidden' in node.attrs or node.attrs.get('aria-hidden','').lower()=='true' or re.search(r'(?:display\s*:\s*none|visibility\s*:\s*hidden)',node.attrs.get('style',''),re.I):
            return False
        node=node.parent
    return True


def _nav_text(node):
    if not _visible(node):
        return ''
    return ''.join(_nav_text(c) if isinstance(c,Node) else c for c in node.children)


def _language(value):
    value=(value or '').lower()
    return '' if value in {'text','plaintext'} else value


def semantic(html):
    tree = SiteHTML(html).root
    main = next((n for n in tree.walk() if n.tag == 'main' or n.attrs.get('role') == 'main'), None)
    article = main
    codes, tabs = [], []
    if article:
        for n in article.walk():
            if n.tag != 'pre':
                continue
            code = next((c for c in n.walk() if c.tag == 'code'), n)
            language = next((c[9:] for c in code.classes if c.startswith('language-')), None) or code.attrs.get('data-lang')
            holder = n.ancestor(lambda p: 'code-block' in p.classes)
            source = next((p for p in holder.walk() if p.tag == 'textarea' and 'code-block-source' in p.classes), None) if holder else None
            copy_value=source.text() if source else None
            # HTML5 consumes exactly one initial LF in textarea content,
            # including an LF produced by a character reference (&#10;).
            # The remaining leading/trailing newlines are clipboard bytes.
            if copy_value is not None and copy_value.startswith('\n'):
                copy_value=copy_value[1:]
            codes.append({'node': n, 'language': language, 'text': code.text({'lnt', 'ln'}), 'copy': copy_value})
        for n in article.walk():
            if 'tabs-container' not in n.classes:
                continue
            panels = [p for p in n.walk() if p.attrs.get('role') == 'tabpanel' and p.ancestor(lambda a: 'tabs-container' in a.classes) is n]
            tabs.append({'code_blocks': [i for i, c in enumerate(codes) if c['node'].ancestor(lambda a: a is n) is n],
                         'languages': [p.attrs.get('data-tab-title', '').lower() for p in panels]})
    nav = [(n.attrs.get('href', ''), ' '.join(n.text().split())) for n in tree.walk() if n.tag == 'a' and n.ancestor(lambda a: a.tag in {'nav','aside'} or 'sidebar' in a.classes or 'sidebar-menu' in a.classes)]
    return {'tree': tree, 'article': article, 'codes': codes, 'tabs': tabs, 'nav': nav,
            'nav_labels': [' '.join(_nav_text(n).split()) for n in tree.walk() if n.tag in {'a','span','div'} and _visible(n) and n.ancestor(lambda a:a.tag in {'nav','aside'} or 'sidebar' in a.classes or 'sidebar-menu' in a.classes)],
            'ids': [n.attrs['id'] for n in article.walk() if 'id' in n.attrs] if article else [],
            'links': [n.attrs['href'] for n in article.walk() if n.tag == 'a' and 'href' in n.attrs] if article else [],
            'link_records': [{'href':n.attrs['href'],'text':n.text()} for n in article.walk() if n.tag=='a' and 'href' in n.attrs] if article else [],
            'images': [n.attrs['src'] for n in article.walk() if n.tag == 'img' and 'src' in n.attrs] if article else []}


def report_shell(inputs):
    return {'schema_version': 1, 'status': 'pass', 'scope': 'offline', 'inputs': inputs,
            'checks': {'offline': {'status': 'pass'}, **{k: {'status': 'not_run', 'evidence': 'Requires separate observed execution'} for k in ('browser','http','hosting')}}, 'issues': []}


def issue(report, check, url, evidence, status='fail', **extra):
    report['issues'].append({'id': check, 'url': url, 'severity': 'error', 'evidence': evidence, **extra})
    if status=='fail' or report['status']!='fail':
        report['status'] = report['checks']['offline']['status'] = status


def route_file(route):
    relative = unquote(route).lstrip('/')
    if not safe_relative(relative or 'index.html'):
        raise ValueError('Unsafe route: ' + route)
    return relative + 'index.html' if route.endswith('/') else relative


def _historical_code_path(base_path, baseline_name, source, block):
    """The immutable capture catalog alone uses this deduplicated code store."""
    root = Path(__file__).absolute().parents[2]
    expected_base = root/'migration/releases/baselines'/str(source)
    path = block.get('text_path', '')
    if (source not in HISTORICAL_CUSTOM_SOURCES or baseline_name != 'baseline.json' or
            base_path.absolute() != expected_base or
            not re.fullmatch(r'\.\./\.\./code/[0-9a-f]{64}\.txt', path) or
            Path(path).stem != block.get('sha256')):
        return None
    candidate = expected_base.parents[1]/'code'/Path(path).name
    # Reject symlink files and every participating directory, including the
    # baseline location; resolving first would conceal an aliased parent.
    for target in (expected_base/'baseline.json', candidate):
        if any(part.is_symlink() for part in (target, *target.parents)):
            return None
    if not (expected_base/'baseline.json').is_file():
        return None
    return candidate


def _expected_blocks(baseline, base_path, report, page_map=None, baseline_name="baseline.json"):
    pages = copy.deepcopy(baseline['pages'])
    for route, page in pages.items():
        for block in page['code_blocks']:
            path = block.get('text_path', '')
            f = base_path / path if safe_relative(path) else _historical_code_path(
                base_path, baseline_name, baseline.get('inputs', {}).get('source_commit'), block)
            if f is None:
                issue(report, 'unsafe-path', route, path)
                block['text'] = ''
                continue
            if not f.is_file() or f.is_symlink() or digest(f) != block['sha256']:
                issue(report, 'baseline-code-integrity', route, path)
                block['text'] = ''
            else:
                block['text'] = f.read_bytes().decode('utf-8')
    # This restoration is pinned to the exact accepted source AND original
    # captured shape. It grants no permission for unrelated extra examples.
    source = baseline.get('inputs', {}).get('source_commit')
    if source in {CURRENT_COMMIT, *HISTORICAL_CUSTOM_SOURCES} and CUSTOM_ROUTE in pages:
        page = pages[CUSTOM_ROUTE]
        historical_valid = True
        if source in HISTORICAL_CUSTOM_SOURCES:
            mapped = [p for p in (page_map or {}).get('pages', []) if p.get('old_url') == CUSTOM_ROUTE]
            signature = {'code_blocks': [(b.get('language'), b.get('sha256')) for b in page['code_blocks']], 'tab_panels': page['tab_panels']}
            signature_hash = hashlib.sha256(json.dumps(signature, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
            historical_valid = (len(mapped) == 1 and (page_map or {}).get('source_commit') == source and
                                page.get('source_path') == 'docs/creating-manifest/handling-custom-responses.md' and
                                mapped[0].get('source_path') == page['source_path'] and
                                mapped[0].get('source_sha256') == HISTORICAL_CUSTOM_SOURCES[source] and
                                signature_hash == HISTORICAL_CUSTOM_BASELINE)
        if not historical_valid or len(page['code_blocks']) != 20 or len(page['tab_panels']) != 10:
            issue(report, 'restoration-baseline', CUSTOM_ROUTE, 'Expected original 20 blocks/10 groups before exact restoration')
        else:
            page['code_blocks'][4:4] = [{'language': lang, 'text': text} for lang,text in RESTORED]
            for tab in page['tab_panels'][2:]:
                tab['code_blocks'] = [i+2 for i in tab['code_blocks']]
            page['tab_panels'].insert(2, {'code_blocks':[4,5], 'languages':['yaml','json']})
    if placeholder_navigation.ROUTE in pages:
        try:
            pages[placeholder_navigation.ROUTE]['links'] = placeholder_navigation.restore_links(baseline, page_map)
            pages[placeholder_navigation.ROUTE]['_restored_placeholder_navigation'] = True
        except ValueError as error:
            issue(report, 'placeholder-navigation-baseline', placeholder_navigation.ROUTE, str(error))
    return pages


def check_site(baseline_file, page_map_file, site_dir, base_url, exceptions_file, asset_map_file=None, archived=False):
    baseline_file, page_map_file, site_dir, exceptions_file = map(Path, (baseline_file,page_map_file,site_dir,exceptions_file))
    baseline = json.loads(baseline_file.read_text())
    page_map = json.loads(page_map_file.read_text())
    ex = json.loads(exceptions_file.read_text())
    if type(archived) is not bool:
        raise ValueError('archived must be an explicit boolean')
    source = page_map.get('source_commit')
    result = report_shell({'source_commit': source, 'source_kind':page_map.get('source_kind'), 'archived':archived, 'base_url': base_url, 'site_dir': str(site_dir), 'baseline_sha256':digest(baseline_file), 'page_map_sha256':digest(page_map_file), 'exceptions_sha256':digest(exceptions_file), 'site_sha256':site_digest(site_dir), 'publication_scope':page_map.get('scope','complete')})
    parsed_base = urlsplit(base_url)
    if parsed_base.scheme not in {'http','https'} or not parsed_base.netloc or parsed_base.query or parsed_base.fragment or not base_url.endswith('/'):
        issue(result,'base-url','/',base_url)
        return result
    prefix = parsed_base.path
    if page_map.get('source_kind')!='git' or not isinstance(source,str) or re.fullmatch('[0-9a-f]{40}',source) is None:
        issue(result,'source-provenance','/','Require immutable Git source identity for acceptance',status='incomplete')
    if baseline.get('inputs',{}).get('source_commit') != source or baseline.get('build_provenance',{}).get('source_commit') != source:
        issue(result,'baseline-provenance','/', 'Baseline and page map must identify the same immutable source')
    if baseline.get('status')!='pass' or not baseline.get('build_provenance',{}).get('mode'):
        issue(result,'baseline-provenance','/','Require passing baseline with identified build mode',status='incomplete')
    exceptions = ex.get('exceptions', [])
    allowed = Counter()
    for entry in exceptions:
        target = entry.get('target', '')
        parts = urlsplit(target)
        target_route = parts.path
        if not target_route.endswith('/') and target_route+'/' in baseline.get('pages', {}):
            target_route += '/'
        captured_target = baseline.get('pages', {}).get(target_route)
        defect = ('broken-link' if captured_target is None else
                  'missing-fragment' if parts.fragment and unquote(parts.fragment) not in captured_target.get('ids', []) else None)
        count = sum(x.get('resolved_url') == target for x in baseline.get('pages', {}).get(entry.get('url'), {}).get('links', []))
        key = (entry.get('check'), entry.get('url'), target)
        if (entry.get('check') not in {'broken-link', 'missing-fragment'} or entry.get('check') != defect or
                not entry.get('reason') or entry.get('source_commit') != source or
                not entry.get('url') or not target or '*' in target or parts.scheme or parts.netloc or
                entry['url'] not in baseline.get('pages', {}) or not count or key in allowed):
            issue(result,'exception-provenance', entry.get('url','/'), entry)
        else:
            allowed[key] = count
    expected = _expected_blocks(baseline, baseline_file.parent, result, page_map, baseline_file.name)
    asset_resources = _assets(Path(asset_map_file),site_dir,result,source) if asset_map_file else {}
    published = {}
    for p in page_map['pages']:
        required = ('source_path','source_sha256','published','disposition','old_url','target_path','title','nav_title','menu_id','menu_parent','weight','exceptions')
        if any(k not in p for k in required) or not re.fullmatch('[0-9a-f]{64}',p.get('source_sha256','')) or not p.get('title'):
            issue(result,'page-metadata',p.get('old_url') or '/',p,source_path=p.get('source_path'))
        if p.get('disposition') in {'pending',None,''}:
            issue(result,'pending-disposition',p.get('old_url') or '/',p,source_path=p.get('source_path'))
        if p.get('published'):
            target=p.get('target_path')
            if not p.get('nav_title') or not p.get('menu_id') or type(p.get('weight')) is not int or p['weight']<=0 or not isinstance(target,str) or not safe_relative(target) or re.fullmatch(r'content/(?:.*/)?_?index\.md',target) is None:
                issue(result,'page-metadata',p.get('old_url') or '/',p,source_path=p.get('source_path'))
            route = p.get('old_url')
            try:
                route_file(route or '')
                if not route or not route.startswith('/') or not route.endswith('/'):
                    raise ValueError('Published route must start/end in slash')
                if route in published:
                    issue(result,'duplicate-route',route,p['source_path'])
                published[route] = p
            except ValueError as err:
                issue(result,'unsafe-path',str(route),str(err))
    if set(published) != set(expected):
        issue(result,'baseline-pages','/', {'published':sorted(published),'baseline':sorted(expected)})
    for f in site_dir.rglob('*'):
        if f.is_symlink():
            issue(result,'site-symlink','/',str(f.relative_to(site_dir)))
    # User decision (2026-11-01): retire only this current sidebar entry.
    # Keep the page in every publication/content/link check and archived menu.
    sidebar_pages = {route: page for route, page in published.items()
                     if archived or route != '/virtuozzo-cs-correspondence/'}
    parsed = {}
    for route,p in published.items():
        path = site_dir/route_file(route)
        if not path.is_file():
            issue(result,'missing-page',route,str(path),source_path=p['source_path'])
            continue
        parsed[route] = semantic(path.read_text())
    def local_target(href, route):
        target = urlsplit(urljoin(base_url + route.lstrip('/'), href))
        if target.scheme not in {'http','https'} or target.netloc != parsed_base.netloc:
            return None
        if not target.path.startswith(prefix):
            return ('prefix', target)
        logical = '/' + target.path[len(prefix):]
        if not logical.endswith('/') and logical+'/' in published:
            logical+='/'  # Filesystem resolution only; HTTP redirect remains not_run.
        return (logical, target)
    for route, page in parsed.items():
        old = expected.get(route)
        if old and old.get('source_path')!=published[route].get('source_path'):
            issue(result,'page-metadata',route,{'expected_source_path':old.get('source_path'),'actual_source_path':published[route].get('source_path')})
        if not old:
            continue
        if old.get('_restored_placeholder_navigation'):
            navigation_error = placeholder_navigation.check_rendered(page, base_url)
            if navigation_error is not None:
                issue(result, 'placeholder-navigation', route, navigation_error)
        if page['article'] is None:
            issue(result,'missing-article',route,'No main/content element')
        if len(page['codes']) != len(old['code_blocks']):
            issue(result,'code-count',route,{'expected':len(old['code_blocks']),'actual':len(page['codes'])})
        for i,(actual,want) in enumerate(zip(page['codes'],old['code_blocks'])):
            if actual['copy'] is None:
                issue(result,'copy-source',route,{'block_index':i,'expected':'Exact code-block-source textarea for clipboard'})
            for field in ('text','copy'):
                if actual[field] is not None and actual[field] != want['text']:
                    a,b = actual[field].encode(),want['text'].encode()
                    offset = next((j for j,(x,y) in enumerate(zip(a,b)) if x!=y),min(len(a),len(b)))
                    issue(result,'code-bytes',route,{'block_index':i,'surface':field,'first_changed_byte':offset,'expected_sha256':hashlib.sha256(b).hexdigest(),'actual_sha256':hashlib.sha256(a).hexdigest()},source_path=published[route]['source_path'])
            if _language(actual['language']) != _language(want.get('language')):
                issue(result,'code-language',route,{'block_index':i,'expected':want.get('language'),'actual':actual['language']})
        if page['tabs'] != old['tab_panels']:
            issue(result,'tab-panels',route,{'expected':old['tab_panels'],'actual':page['tabs']})
        for anchor in set(old.get('ids',[])):
            if re.fullmatch(r'(?:tabs-\d+-\d+|tab-\d+)',anchor):
                continue
            if anchor not in page['ids']:
                issue(result,'missing-fragment',route,{'fragment':anchor})
        for heading in old.get('headings',[]):
            normal=lambda text:' '.join(text.replace('¶','').split())
            if heading.get('id') is None and normal(heading['text']) in {"What's next?",'What’s next?'}:
                continue  # Exact legacy related-links chrome, outside authored text.
            actual_headings=[n for n in page['article'].walk() if n.tag in {'h1','h2','h3','h4','h5','h6'} and ((heading.get('id') is not None and n.attrs.get('id')==heading['id']) or (heading.get('id') is None and normal(n.text())==normal(heading['text'])))] if page['article'] else []
            if not actual_headings or normal(actual_headings[0].text())!=normal(heading['text']):
                issue(result,'heading-text',route,{'fragment':heading.get('id'),'expected':heading['text'],'actual':[n.text() for n in actual_headings]})
        canonical = [n.attrs.get('href') for n in page['tree'].walk() if n.tag=='link' and n.attrs.get('rel')=='canonical']
        desired = base_url + route.lstrip('/')
        if canonical != [desired]:
            issue(result,'canonical',route,{'expected':desired,'actual':canonical})
        noindex=any(n.tag=='meta' and n.attrs.get('name','').lower()=='robots' and 'noindex' in re.split(r'[\s,]+',n.attrs.get('content','').lower()) for n in page['tree'].walk())
        if noindex != archived:
            issue(result,'robots-rule',route,{'archived':archived,'expected_noindex':archived,'actual_noindex':noindex})
        for navroute, navpage in sidebar_pages.items():
            label = navpage.get('nav_title')
            candidates = [text for href,text in page['nav'] if local_target(href,route) and local_target(href,route)[0] == navroute]
            if label and label not in candidates:
                issue(result,'menu-label',route,{'target':navroute,'expected':label,'actual':candidates})
        def groups(nodes):
            for node in nodes:
                if not node.get('source_path'):
                    yield node['title']
                yield from groups(node.get('children',[]))
        expected_groups=list(groups(page_map.get('navigation',[])))
        actual_groups=[]
        for text in page['nav_labels']:
            if text in expected_groups and text not in actual_groups:
                actual_groups.append(text)
        for label in expected_groups:
            if label not in actual_groups:
                issue(result,'menu-group',route,{'expected':label})
        if set(actual_groups)==set(expected_groups) and actual_groups!=expected_groups:
            issue(result,'menu-group-order',route,{'expected':expected_groups,'actual':actual_groups})
        nav_order=[]
        for href,text in page['nav']:
            target=local_target(href,route)
            if target and target[0] in published and text==published[target[0]].get('nav_title') and target[0] not in nav_order:
                nav_order.append(target[0])
        desired_order=sorted(sidebar_pages,key=lambda r:sidebar_pages[r].get('weight') or 0)
        if nav_order != desired_order:
            issue(result,'menu-order',route,{'expected':desired_order,'actual':nav_order})
        # Compare legacy reference identities, allowing prefixing and optional
        # asset-map resource rewrites, then independently resolve every output.
        for field,oldfield,key in [('links','links','resolved_url'),('images','images','resolved_url')]:
            actual_targets = [local_target(h,route) for h in page[field]]
            consumed=set()
            for ref in old.get(oldfield,[]):
                original=ref.get(key) or urljoin(route,ref.get('href' if field=='links' else 'src',''))
                wanted = urlsplit(original)
                authored_same_page=False
                if wanted.scheme or wanted.netloc:
                    matches=[i for i,h in enumerate(page[field]) if urljoin(base_url+route.lstrip('/'),h)==original]
                else:
                    wanted_path = wanted.path or route
                    if not wanted_path.endswith('/') and wanted_path+'/' in published:
                        wanted_path+='/'
                    matches=[i for i,t in enumerate(actual_targets) if t and t[0]!='prefix' and t[0]==wanted_path and t[1].fragment==wanted.fragment and t[1].query==wanted.query]
                    if field=='images' and not matches:
                        resources=asset_resources.get((route,wanted_path),[])
                        matches=[i for i,t in enumerate(actual_targets) if t and t[0]!='prefix' and any(_resource_matches(t[0],r) for r in resources)]
                    if field=='links' and wanted.fragment and wanted_path==route:
                        generated_glyph=(ref.get('text','').strip()=='¶' and ref.get('href')=='#'+wanted.fragment and any(h.get('id')==wanted.fragment and h.get('text','').rstrip().endswith('¶') for h in old.get('headings',[])))
                        if generated_glyph and wanted.fragment in page['ids']:
                            continue  # Captured heading permalink glyph only.
                        authored_same_page=True
                        matches=[i for i in matches if ' '.join(page['link_records'][i]['text'].split())==' '.join(ref.get('text','').split())]
                if field=='images' or authored_same_page:
                    matches=[i for i in matches if i not in consumed]
                    if matches:
                        consumed.add(matches[0])
                if not matches:
                    issue(result,'image-reference' if field=='images' else 'link-reference',route,ref)
        srcsets=[]
        if page['article']:
            for n in page['article'].walk():
                if n.tag in {'img','source'} and n.attrs.get('srcset'):
                    srcsets.extend(x.strip().split()[0] for x in n.attrs['srcset'].split(',') if x.strip())
        for kind,hrefs in [('link',page['links']),('image',page['images']+srcsets)]:
            for href in hrefs:
                target = local_target(href,route)
                if target is None:
                    continue
                logical,parts = target
                if logical=='prefix':
                    absolute=urlsplit(href)
                    docs_path=unquote(parts.path)
                    captured_external=kind=='link' and absolute.scheme in {'http','https'} and any(ref.get('resolved_url')==href and urlsplit(ref.get('href','')).scheme in {'http','https'} for ref in old.get('links',[]))
                    misplaced_docs=docs_path.startswith(('/img/','/static/','/content/','/assets/')) or docs_path.rstrip('/')+'/' in expected or docs_path.startswith(prefix.rstrip('/')+'/')
                    if captured_external and not misplaced_docs:
                        continue
                    issue(result,'release-prefix',route,{'href':href,'required_prefix':prefix})
                    continue
                try:
                    relative = route_file(logical)
                except ValueError as err:
                    issue(result,'unsafe-path',route,{'href':href,'reason':str(err)})
                    continue
                f=site_dir/relative
                exact = f.is_file() and all(part in {c.name for c in parent.iterdir()} for part,parent in _path_components(site_dir,relative))
                if not exact:
                    exception_target=logical+('?' + parts.query if parts.query else '')+('#'+parts.fragment if parts.fragment else '')
                    exception_key=('broken-link',route,exception_target)
                    if kind=='link' and allowed[exception_key]>0:
                        allowed[exception_key]-=1
                        continue
                    folded = any(x.relative_to(site_dir).as_posix().casefold()==relative.casefold() for x in site_dir.rglob('*') if x.is_file())
                    issue(result,'asset-case' if kind=='image' and folded else 'broken-link',route,{'href':href,'target':logical,'missing_file':relative})
                elif parts.fragment:
                    ids = parsed.get(logical,{}).get('ids')
                    if ids is None:
                        ids=semantic(f.read_text())['ids'] if f.suffix=='.html' else []
                    if unquote(parts.fragment) not in ids:
                        exception_target=logical+('?' + parts.query if parts.query else '')+'#'+parts.fragment
                        exception_key=('missing-fragment',route,exception_target)
                        if kind=='link' and allowed[exception_key]>0:
                            allowed[exception_key]-=1
                            continue
                        issue(result,'missing-fragment',route,{'href':href,'target':logical,'fragment':parts.fragment})
    if source == CURRENT_COMMIT and len(published)==16:
        counts={'code_blocks':sum(len(p['codes']) for p in parsed.values()),'tab_groups':sum(len(p['tabs']) for p in parsed.values())}
        if counts != {'code_blocks':566,'tab_groups':269}:
            issue(result,'active-source-counts','/',{'expected':{'code_blocks':566,'tab_groups':269},'actual':counts,'explanation':'Only Custom Responses source76–100 adds one group/two blocks; Actions149–183 stays commented'})
    _publication(site_dir,published,page_map,result)
    _search_and_seo(site_dir,published,base_url,result)
    return result


def _path_components(root,relative):
    parent=root
    for part in PurePosixPath(relative).parts:
        yield part,parent
        parent=parent/part


def _publication(site_dir,published,page_map,result):
    allowed={route_file(r) for r in published}|{'404.html','search.html','search/index.html'}
    unpublished={p['source_path'].removeprefix('docs/').removesuffix('.md').strip('/') for p in page_map['pages'] if not p.get('published')}
    for p in site_dir.rglob('*.html'):
        rel=p.relative_to(site_dir).as_posix()
        if rel in allowed:
            continue
        route=rel.removesuffix('index.html').rstrip('/') if rel.endswith('index.html') else rel.removesuffix('.html')
        issue(result,'draft-publication' if route in unpublished else 'undeclared-publication','/'+route+'/',rel)


def _search_and_seo(site_dir,published,base_url,result):
    try:
        entries=json.loads((site_dir/'index.json').read_text())
        if not isinstance(entries,list):
            raise ValueError('Expected an array')
        urls=[x.get('permalink') for x in entries]
        required={base_url+r.lstrip('/') for r in published}
        for url in required:
            matching=[x for x in entries if x.get('permalink')==url]
            route='/' + url[len(base_url):]
            if len(matching)!=1 or matching[0].get('title')!=published[route].get('title') or not matching[0].get('contents'):
                issue(result,'search-entry',url,{'expected':'One populated entry','actual':matching})
        for url in set(urls)-required:
            issue(result,'search-undeclared',str(url),'Search indexed an undeclared route')
    except (OSError,ValueError,TypeError,AttributeError) as err:
        issue(result,'search-index','index.json',str(err))
    for f in ('search/index.html','search.html'):
        if not (site_dir/f).is_file():
            issue(result,'search-route',f,'Missing search/legacy entry point')
    try:
        text=(site_dir/'robots.txt').read_text()
        robots=RobotFileParser();robots.parse(text.splitlines())
        for route in published:
            if not robots.can_fetch('*',base_url+route.lstrip('/')):
                issue(result,'robots-rule','robots.txt',{'blocked':base_url+route.lstrip('/')})
        sitemap=base_url+'sitemap.xml'
        if sitemap not in (robots.site_maps() or []):
            issue(result,'robots-sitemap','robots.txt',{'expected':sitemap})
    except OSError as err:
        issue(result,'robots-rule','robots.txt',str(err))
    try:
        root=ET.parse(site_dir/'sitemap.xml').getroot()
        urls=[n.text for n in root.iter() if n.tag.split('}')[-1]=='loc']
        required={base_url+r.lstrip('/') for r in published}
        for url in required-set(urls):
            issue(result,'sitemap-entry',url,'Missing published URL')
        for url in set(urls)-required-{base_url+'search/'}:
            issue(result,'sitemap-undeclared',str(url),'Unexpected sitemap URL')
    except (OSError,ET.ParseError) as err:
        issue(result,'sitemap-entry','sitemap.xml',str(err))


def _resource_matches(actual,resource):
    expected=urlsplit(resource).path
    if actual==expected:
        return True
    parent,_,name=expected.rpartition('/')
    stem,_,ext=name.rpartition('.')
    pattern=re.escape(parent+'/'+stem)+r'_hu[a-zA-Z0-9_]+\.(?:'+re.escape(ext)+r'|webp)'
    return re.fullmatch(pattern,actual) is not None


def _assets(path,site_dir,result,source):
    data=json.loads(path.read_text())
    result['inputs']['asset_map_sha256']=digest(path)
    resources={}
    if data.get('schema_version')!=1 or data.get('source_commit')!=source:
        issue(result,'asset-map-provenance','/',{'source_commit':data.get('source_commit'),'expected':source})
    for asset in data.get('assets',[]):
        url=asset.get('public_url','')
        if not url.startswith('/'):
            issue(result,'asset-map',url,'Expected root-relative public_url')
            continue
        urls=[url]
        for resource in asset.get('bundle_resources',[]):
            page_url,name=resource.get('page_url',''),resource.get('name','')
            if not page_url.startswith('/') or not page_url.endswith('/') or '/' in name or not safe_relative(name):
                issue(result,'asset-map',url,resource);continue
            resource_url=page_url+name
            urls.append(resource_url)
            resources.setdefault((page_url,url),[]).append(resource_url)
        for target in urls:
            rel=target.lstrip('/')
            if not safe_relative(rel):
                issue(result,'unsafe-path',target,rel);continue
            f=site_dir/rel
            exact=f.is_file() and all(part in {c.name for c in parent.iterdir()} for part,parent in _path_components(site_dir,rel))
            if not exact or digest(f)!=asset.get('sha256'):
                issue(result,'asset-integrity',target,{'expected_sha256':asset.get('sha256'),'file':rel})
    return resources


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('baseline','page-map','site-dir','base-url','exceptions','report'):
        p.add_argument('--'+name,required=True)
    p.add_argument('--asset-map')
    p.add_argument('--archived',action='store_true',help='Require noindex on all published archive articles (default: indexable root)')
    args=p.parse_args()
    try:
        result=check_site(args.baseline,args.page_map,args.site_dir,args.base_url,args.exceptions,args.asset_map,args.archived)
    except (OSError,ValueError,KeyError,TypeError,AttributeError) as err:
        result=report_shell({'site_dir':args.site_dir,'base_url':args.base_url,'archived':args.archived})
        issue(result,'invalid-input','/',str(err))
    output=Path(args.report);output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    raise SystemExit(0 if result['status']=='pass' else 1)


if __name__=='__main__':
    main()
