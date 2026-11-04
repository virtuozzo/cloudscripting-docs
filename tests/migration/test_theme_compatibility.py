"""Real pinned-Hugo boundary tests; HUGO_BIN may select the installed binary."""
import html5lib
import functools
import http.server
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading
import unittest
import xml.etree.ElementTree as ET
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / 'tests/fixtures/theme-compatibility'
HUGO = os.environ.get('HUGO_BIN', shutil.which('hugo') or 'hugo')


class Capture:
    """Read rendered DOM text with HTML5's textarea initial-LF rule.

    This intentionally uses the independent parser instead of correcting raw
    character data to match the hook: assertions compare actual DOM values.
    """
    def __init__(self, text):
        tree = html5lib.parse(text, namespaceHTMLElements=False)
        self.pre = [''.join(node.itertext()) for node in tree.iter('pre')]
        self.copies = [node.text or '' for node in tree.iter('textarea')
                       if 'code-block-source' in node.get('class', '').split()]
        self.links = [dict(node.attrib) for node in tree.iter('a')]
        self.panels = [node.get('data-tab-title') for node in tree.iter()
                       if node.get('role') == 'tabpanel']


class ThemeCompatibility(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        version = subprocess.check_output([HUGO, 'version'], text=True)
        assert 'v0.124.1' in version and '+extended' in version, version
        cls.temp = tempfile.TemporaryDirectory(prefix='cs-theme-')
        cls.addClassCleanup(cls.temp.cleanup)
        cls.builds = {}
        contexts = [
            ('', 'https://docs.cloudscripting.com/', 'https://docs.cloudscripting.com/', 'root'),
            ('8.15.1/', 'https://docs.cloudscripting.com/8.15.1/', 'https://docs.cloudscripting.com/', '8.15.1'),
            ('6.3.2/', 'https://docs.cloudscripting.com/6.3.2/', 'https://docs.cloudscripting.com/', '6.3.2'),
            ('staging/docs/8.15.1/', 'https://example.test/staging/docs/8.15.1/', 'https://example.test/staging/docs/', '8.15.1'),
            ('production-root', 'https://www.virtuozzo.com/cloudscripting-docs/', 'https://www.virtuozzo.com/cloudscripting-docs/', 'root'),
            ('production-latest', 'https://www.virtuozzo.com/cloudscripting-docs/8.15.1/', 'https://www.virtuozzo.com/cloudscripting-docs/', '8.15.1'),
        ]
        for prefix, base, site_root, build_id in contexts:
            work = Path(cls.temp.name) / (prefix.replace('/', '-') or 'root')
            work.mkdir()
            shutil.copytree(FIXTURE / 'content', work / 'content')
            shutil.copy(ROOT / 'content/search.md', work / 'content/search.md') if (ROOT / 'content/search.md').exists() else None
            shutil.copytree(FIXTURE / 'data', work / 'data')
            (work / 'themes').symlink_to(ROOT / 'themes')
            if (ROOT / 'layouts').exists(): shutil.copytree(ROOT / 'layouts', work / 'layouts')
            if (ROOT / 'static').exists(): shutil.copytree(ROOT / 'static', work / 'static')
            if (ROOT / 'assets').exists(): shutil.copytree(ROOT / 'assets', work / 'assets')
            if (ROOT / 'redirects.htaccess').exists(): shutil.copy(ROOT / 'redirects.htaccess', work)
            shutil.copy(ROOT / 'config.yaml', work / 'config.yaml')
            with (work / 'content/article/index.md').open('a') as stream:
                stream.write('\n[Prefixed](' + urlparse(base).path + 'article/ "prefixed fixture")\n')
            override = {'params': {'version': ('8.15.1' if build_id == 'root' else build_id), 'csBuildID': build_id,
                        'versions': ['6.3.2', '8.9.1', '8.15.1'], 'defaultVersion': '8.15.1', 'archived': build_id != 'root',
                        'csVersionURLs': {'root': site_root, '8.15.1': site_root + '8.15.1/',
                        '8.9.1': site_root + '8.9.1/', '6.3.2': site_root + '6.3.2/'}}, 'disableAliases': True}
            (work / 'fixture.json').write_text(json.dumps(override))
            run = subprocess.run([HUGO, '--source', str(work), '--config', 'config.yaml,fixture.json', '--baseURL', base], capture_output=True, text=True)
            if run.returncode: raise AssertionError(run.stdout + run.stderr)
            cls.builds[prefix] = (work / 'public', base, site_root)
            if os.environ.get('THEME_EVIDENCE_DIR'):
                evidence = Path(os.environ['THEME_EVIDENCE_DIR']) / (prefix.replace('/', '-') or 'root')
                evidence.mkdir(parents=True, exist_ok=True)
                for name in ('index.html', 'article/index.html', 'correspondence/index.html', 'index.json', 'search/index.html', 'search.html', '.htaccess', 'sitemap.xml', 'robots.txt'):
                    target = evidence / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(work / 'public' / name, target)


    def test_html5_display_and_clipboard_bytes_for_nested_tabs_and_lf_edges(self):
        # Removing the hook's fallback or LF reconstruction corrupts these literals.
        expected = ['\nkey: ${value}\ntext: "<script>& literal"\n', '{"text": "x"}\n\n',
                    '#!/bin/bash\n  echo "preserve spaces"\n', '{{< literal >}}\n',
                    'onInstall:\n  script [12345, 123456]: |\n    return { result: 0, nodeId: nodeId };\n', '', '\n', '\n\n']
        for public, base, root in self.builds.values():
            text = (public / 'article/index.html').read_text()
            parsed = Capture(text)
            self.assertEqual(parsed.pre, expected)
            self.assertEqual(parsed.copies, expected)
            self.assertEqual(parsed.panels, ['YAML', 'JSON'])
            self.assertIn('<strong>bold</strong>', text)
            self.assertIn('Inner item</li>', text)
            self.assertIn('Careful &amp; exact', text)
            self.assertIn('class="notify-block cs-admonition cs-admonition-note"', text)

    def test_no_highlight_keeps_language_identity_and_hides_label(self):
        expected = '  sudo /etc/init.d/jetty start\n<literal>& exact\n\n'
        for public, base, root in self.builds.values():
            with self.subTest(base=base):
                text = (public / 'no-highlight/index.html').read_text()
                parsed = Capture(text)
                self.assertEqual(parsed.pre, [expected])
                self.assertEqual(parsed.copies, [expected])
                tree = html5lib.parse(text, namespaceHTMLElements=False)
                code = next(next(tree.iter('pre')).iter('code'))
                self.assertIn('language-no-highlight', code.get('class', '').split())
                self.assertEqual(code.get('data-lang'), 'no-highlight')
                self.assertFalse(any('code-block-label' in node.get('class', '').split()
                                     for node in tree.iter()))

    def test_article_links_stay_in_build_prefix(self):
        for public, base, root in self.builds.values():
            links = Capture((public / 'article/index.html').read_text()).links
            hrefs = [item['href'] for item in links if 'href' in item]
            self.assertIn(base + 'article/?q=1#details', hrefs)
            self.assertIn(base + 'article/', hrefs)
            self.assertEqual(next(a['href'] for a in links if a.get('title') == 'prefixed fixture'), base + 'article/')
            self.assertIn('../article/#details', hrefs)
            self.assertIn('#details', hrefs)
            self.assertIn('?q=1', hrefs)
            self.assertIn('https://example.org/article/', hrefs)
            self.assertIn('//example.org/article/', hrefs)
            self.assertEqual(next(a['href'] for a in links if a.get('id') == 'normalized-raw'), '../article/#details')

    def test_yaml_block_scalar_keeps_highlighting_without_adding_spaces(self):
        # Pinned Chroma duplicates scalar indentation after its final text line.
        # Removing the narrow repair makes this known YAML block fall back to plain text.
        for public, _, _ in self.builds.values():
            tree = html5lib.parse((public / 'article/index.html').read_text(), namespaceHTMLElements=False)
            block = list(tree.iter('pre'))[4]
            tokens = list(block.iter('span'))
            self.assertTrue(any('nt' in token.get('class', '').split() for token in tokens),
                            'YAML keys must retain syntax highlighting')
            self.assertTrue(any('sd' in token.get('class', '').split() for token in tokens),
                            'YAML block scalar must retain syntax highlighting')
            self.assertEqual(''.join(block.itertext()),
                             'onInstall:\n  script [12345, 123456]: |\n    return { result: 0, nodeId: nodeId };\n')

    def test_search_includes_home_and_excludes_utilities_and_drafts(self):
        for public, base, root in self.builds.values():
            index = json.loads((public / 'index.json').read_text())
            self.assertEqual({p['permalink'] for p in index}, {base, base + 'article/', base + 'correspondence/', base + 'no-highlight/'})
            self.assertIn('Cloud Scripting fixture introduction', next(p['contents'] for p in index if p['permalink'] == base))
            self.assertFalse((public / 'draft').exists())
            self.assertTrue((public / 'search/index.html').exists())
            self.assertIn('data-index="' + base + 'index.json"', (public / 'search/index.html').read_text())

    def test_correspondence_table_only_numeric_descending(self):
        public, _, _ = self.builds['']
        text = (public / 'correspondence/index.html').read_text()
        self.assertEqual(text.count('<h1'), 1)
        self.assertIn('id="virtuozzo-cs-correspondence"', text)
        self.assertLess(text.index('<td>8.15.1</td>'), text.index('<td>8.9.1</td>'))
        self.assertLess(text.index('<td>8.9.1</td>'), text.index('<td>6.3.2</td>'))
        self.assertIn('<td>6.3-2</td>', text)
        self.assertTrue(all('id="' + anchor + '"' in text for anchor in ('cs', 'jel', 'table-head')), 'Legacy table fragments missing')

    def test_correspondence_sidebar_is_retired_only_for_current_docs(self):
        for public, base, root in self.builds.values():
            tree = html5lib.parse((public / 'correspondence/index.html').read_text(), namespaceHTMLElements=False)
            sidebar = next(tree.iter('aside'))
            label = 'CS vs Virtuozzo PaaS Versions'
            self.assertEqual(label in ''.join(sidebar.itertext()), base != root)
            menu_file = next((public / 'menu').glob('*.json'))
            self.assertEqual(label in menu_file.read_text(), base != root)
            self.assertTrue(list(tree.iter('table')), 'Old correspondence URL must retain its content')

    def test_home_overview_is_selected_and_its_parent_is_open(self):
        for public, base, _ in self.builds.values():
            with self.subTest(base=base):
                tree = html5lib.parse((public / 'index.html').read_text(), namespaceHTMLElements=False)
                sidebar = next(tree.iter('aside'))
                selected = [node for node in sidebar.iter('li') if 'current-page' in node.get('class', '').split()]
                self.assertEqual(len(selected), 1, 'Homepage must have exactly one selected menu entry')
                link = next(selected[0].iter('a'))
                self.assertEqual(''.join(link.itertext()), 'Overview')
                self.assertEqual(link.get('href'), base)
                parents = {child: parent for parent in sidebar.iter() for child in parent}
                group = parents[parents[selected[0]]]
                self.assertIn('expanded', group.get('class', '').split())
                article = html5lib.parse((public / 'article/index.html').read_text(), namespaceHTMLElements=False)
                current = [node for node in next(article.iter('aside')).iter('li') if 'current-page' in node.get('class', '').split()]
                self.assertEqual([next(node.iter('a')).get('href') for node in current], [base + 'article/'])

    def test_switcher_does_not_collapse_latest_to_root(self):
        for public, base, root in self.builds.values():
            links = Capture((public / 'article/index.html').read_text()).links
            versions = [a for a in links if 'data-vs-from' in a]
            self.assertEqual({a['href'] for a in versions}, {root, root + '8.15.1/', root + '8.9.1/', root + '6.3.2/'})
            self.assertEqual(len({a['href'] for a in versions if a.get('aria-current') == 'true'}), 1)

    def test_feedback_context(self):
        for public, base, root in self.builds.values():
            for route in ('article/index.html', 'index.html'):
                tree = html5lib.parse((public / route).read_text(), namespaceHTMLElements=False)
                feedback = [node for node in tree.iter() if node.get('class') == 'cs-feedback-wrap']
                self.assertEqual(len(feedback), 1, 'Render one feedback row per article')
                self.assertIs(list(next(tree.iter('main')))[-1], feedback[0],
                              'Feedback belongs after the article, inside main, before the site footer')
            links = Capture((public / 'article/index.html').read_text()).links
            issue = next(a for a in links if a.get('class') == 'cs-feedback')
            query = parse_qs(urlparse(issue['href']).query)
            self.assertIn(base + 'article/', query['body'][0])
            self.assertIn('Build: ' + ('root' if base == root else base.rstrip('/').split('/')[-1]), query['body'][0])
            self.assertTrue(urlparse(issue['href']).path.endswith('/issues/new'))

    def test_aliases_and_404_use_each_build_prefix(self):
        for public, base, root in self.builds.values():
            candidates = list(public.glob('.htaccess*'))
            self.assertEqual(len(candidates), 1)
            text = candidates[0].read_text()
            self.assertIn(base + 'article/', text)
            self.assertIn('^old-article/?$', text)
            self.assertIn('ErrorDocument 404 ' + urlparse(base).path + '404.html', text)
            self.assertNotIn('lowercase:', text)
            self.assertNotIn('virtuozzo\\.com', text)
            self.assertNotIn('Strip /', text)

    def test_sitemap_and_robots_are_scoped_to_each_build(self):
        namespace = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        for public, base, root in self.builds.values():
            urls = {node.text for node in ET.parse(public / 'sitemap.xml').findall('.//s:loc', namespace)}
            self.assertEqual(urls, {base, base + 'article/', base + 'correspondence/', base + 'no-highlight/'})
            article = (public / 'article/index.html').read_text()
            self.assertIn('content="' + ('index, follow' if base == root else 'noindex, follow') + '"', article)
            robots = (public / 'robots.txt').read_text()
            self.assertIn('Sitemap: ' + base + 'sitemap.xml', robots)
            if base != root:
                self.assertNotIn('Sitemap: ' + root + 'sitemap.xml', robots)

    def test_corporate_tracking_is_host_gated_without_legacy_ga(self):
        for public, base, root in self.builds.values():
            article = (public / 'article/index.html').read_text()
            for token in ('GTM-W9PSVPL', 'otSDKStub.js'):
                self.assertEqual(token in article, urlparse(base).hostname == 'www.virtuozzo.com')
            self.assertNotIn('UA-89532314-1', article)
            self.assertNotIn('google-analytics.com/analytics.js', article)

    def run_script(self, mode, script, **values):
        output = subprocess.check_output(['node', str(FIXTURE / 'execute-scripts.cjs'), mode, str(script), json.dumps(values)], text=True)
        return json.loads(output)

    def test_legacy_search_translates_query_with_selected_release(self):
        for public, base, root in self.builds.values():
            self.run_script('search', public / 'search.html', url=base + 'search.html?q=foo%20%26%20bar&lang=en#result',
                            expected=base + 'search/?lang=en&s=foo+%26+bar#result')
            self.run_script('search', public / 'search.html', url=base + 'search.html?q=old&s=current',
                            expected=base + 'search/?s=current')

    def test_shared_copy_button_passes_literal_text_to_clipboard(self):
        public, _, _ = self.builds['']
        values = Capture((public / 'article/index.html').read_text()).copies
        self.run_script('copy', ROOT / 'themes/compose-master/assets/js/index.js', body=values[1], expected='{"text": "x"}\n\n')

    def test_version_switcher_with_real_head_alias_and_missing_fallback(self):
        with tempfile.TemporaryDirectory(prefix='cs-version-http-') as temporary:
            directory = Path(temporary)
            for prefix, (public, _, _) in self.builds.items():
                target = directory / prefix
                target.mkdir(parents=True, exist_ok=True)
                shutil.copytree(public, target, dirs_exist_ok=True)

            shutil.copytree(self.builds[''][0], directory / 'staging/docs', dirs_exist_ok=True)
            shutil.copytree(self.builds['production-root'][0], directory / 'cloudscripting-docs', dirs_exist_ok=True)
            shutil.copytree(self.builds['production-latest'][0], directory / 'cloudscripting-docs/8.15.1', dirs_exist_ok=True)

            class Server(http.server.SimpleHTTPRequestHandler):
                def log_message(self, *args): pass
                def do_HEAD(self):
                    if self.path.endswith('/old-article/'):
                        self.send_response(301)
                        self.send_header('Location', self.path.replace('/old-article/', '/article/'))
                        self.end_headers()
                    else: super().do_HEAD()

            handler = functools.partial(Server, directory=str(directory))
            server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                origin = f'http://127.0.0.1:{server.server_port}/'
                script = ROOT / 'assets/js/version-switch.js'
                for path, expected in [('article/#details', '8.15.1/article/#details'),
                                       ('missing/#details', '8.15.1/'),
                                       ('missing/?s=foo#details', '8.15.1/'),
                                       ('old-article/#details', '8.15.1/article/#details')]:
                    self.run_script('version', script, **{'url': origin + path, 'from': origin,
                        'target': origin + '8.15.1/', 'expected': origin + expected})
                self.run_script('version', script, **{'url': origin + '8.15.1/article/#details', 'from': origin + '8.15.1/',
                    'target': origin, 'expected': origin + 'article/#details'})
                self.run_script('version', script, **{'url': origin + 'staging/docs/8.15.1/article/#details',
                    'from': origin + 'staging/docs/8.15.1/', 'target': origin + 'staging/docs/',
                    'expected': origin + 'staging/docs/article/#details'})
                self.run_script('version', script, **{'url': origin + 'cloudscripting-docs/article/#details',
                    'from': origin + 'cloudscripting-docs/', 'target': origin + 'cloudscripting-docs/8.15.1/',
                    'expected': origin + 'cloudscripting-docs/8.15.1/article/#details'})
                self.run_script('version', script, **{'url': origin + 'search/?s=hello%20world#result',
                    'from': origin, 'target': origin + '8.15.1/',
                    'expected': origin + '8.15.1/search/?s=hello%20world#result'})
                self.run_script('version', script, **{'url': origin + 'article/', 'from': origin,
                    'target': origin + '8.15.1/', 'modified': True})
            finally:
                server.shutdown()
                server.server_close()
                thread.join()


if __name__ == '__main__': unittest.main()
