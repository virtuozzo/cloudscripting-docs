"""Optional heading navigation must stay local to the current page and build."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import html5lib

ROOT = Path(__file__).resolve().parents[2]
HUGO = os.environ.get('HUGO_BIN', shutil.which('hugo') or 'hugo')


def has_class(node, name):
    return name in node.get('class', '').split()


class SidebarHeadingsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='cs-sidebar-headings-')
        cls.addClassCleanup(cls.temp.cleanup)
        cls.builds = {}
        for name, setting, base in [
            ('enabled', True, 'https://example.test/'),
            ('prefixed', True, 'https://example.test/docs/8.15.1/'),
            ('disabled', False, 'https://example.test/'),
            ('omitted', None, 'https://example.test/'),
        ]:
            work = Path(cls.temp.name) / name
            (work / 'content').mkdir(parents=True)
            (work / 'themes').symlink_to(ROOT / 'themes')
            shutil.copytree(ROOT / 'layouts/partials/sidebar', work / 'layouts/partials/sidebar')
            (work / 'layouts/_default').mkdir()
            template = '{{ partial "sidebar.html" . }}<main>{{ .Content }}</main>'
            (work / 'layouts/index.html').write_text(template)
            (work / 'layouts/_default/single.html').write_text(template)
            bodies = {
                '_index.md': '# Home\n\n## Home section {#home-section}\n',
                'article.md': '# Article\n\n## Main & section {#legacy-anchor}\n\n'
                              '### `${value}` child {#special-child}\n\n#### Too deep\n\n'
                              '## Repeat\n\n## Repeat\n\n## [Linked title](https://example.org/) {#linked-title}\n',
                'empty.md': '# No sections\n\nPlain text.\n',
            }
            for index, (filename, body) in enumerate(bodies.items(), 1):
                front = {'title': filename, 'menu': {'docs': {'identifier': filename, 'parent': 'group', 'weight': index * 10}}}
                (work / 'content' / filename).write_text(json.dumps(front) + '\n' + body)
            params = {'hostName': 'example.test', 'docsMenu': {'alwaysOpen': ['group']}}
            if setting is not None:
                params['docsMenu']['showPageHeadings'] = setting
            config = {'baseURL': base, 'theme': 'compose-master', 'canonifyURLs': True, 'params': params,
                      'menu': {'docs': [{'name': 'Group', 'identifier': 'group', 'weight': 10}]}}
            (work / 'config.json').write_text(json.dumps(config))
            run = subprocess.run([HUGO, '--source', str(work), '--config', 'config.json'], capture_output=True, text=True)
            if run.returncode:
                raise AssertionError(run.stdout + run.stderr)
            cls.builds[name] = (work / 'public', base)

    def read_page(self, public, route):
        tree = html5lib.parse((public / route / 'index.html').read_text(), namespaceHTMLElements=False)
        return tree, next(tree.iter('aside'))

    def test_enabled_headings_belong_only_to_selected_page_with_original_ids(self):
        for name in ['enabled', 'prefixed']:
            public, base = self.builds[name]
            with self.subTest(name=name):
                tree, sidebar = self.read_page(public, 'article')
                lists = [node for node in sidebar.iter('ul') if has_class(node, 'cs-menu-page-headings')]
                self.assertEqual(len(lists), 1, 'Current page must have one heading list')
                links = list(lists[0].iter('a'))
                self.assertEqual([link.get('href') for link in links], [
                    '#special-child', '#repeat', '#repeat-1', '#linked-title'])
                self.assertEqual([''.join(link.itertext()) for link in links], [
                    '${value} child', 'Repeat', 'Repeat', 'Linked title'])
                parents = {child: parent for parent in sidebar.iter() for child in parent}
                self.assertTrue(has_class(parents[lists[0]], 'current-page'))
                self.assertEqual(next(parents[lists[0]].iter('a')).get('href'), base + 'article/')
                self.assertEqual(lists[0].find('li/ul/li/span/a').get('href'), '#special-child', 'h3 must nest under its own h2')
                ids = {node.get('id') for node in next(tree.iter('main')).iter()}
                self.assertTrue(all(link.get('href')[1:] in ids for link in links))
                self.assertFalse(any(list(link.iter('a'))[1:] for link in links), 'Heading labels must not create nested links')
                home, home_sidebar = self.read_page(public, '')
                home_links = [link.get('href') for ul in home_sidebar.iter('ul')
                              if has_class(ul, 'cs-menu-page-headings') for link in ul.iter('a')]
                self.assertEqual(home_links, ['#home-section'], 'Cached menu must not leak article headings')
                self.assertNotIn('#legacy-anchor', next((public / 'menu').glob('*.json')).read_text())

    def test_nested_heading_groups_use_theme_menu_and_start_collapsed(self):
        public, _ = self.builds['enabled']
        _, sidebar = self.read_page(public, 'article')
        heading_list = next(node for node in sidebar.iter('ul') if has_class(node, 'cs-menu-page-headings'))
        self.assertTrue(has_class(heading_list, 'menu-level-3'))
        parent = heading_list.find('li')
        self.assertTrue(has_class(parent, 'has-children'))
        self.assertFalse(has_class(parent, 'expanded'))
        label = parent.find('span')
        self.assertTrue(has_class(label, 'aside-menu-item'))
        self.assertEqual(label.get('data-heading-id'), 'legacy-anchor')
        self.assertEqual(''.join(label.itertext()), 'Main & section')
        self.assertIsNone(label.find('a'), 'Legacy heading groups toggle their children')
        children = parent.find('ul')
        self.assertTrue(has_class(children, 'menu-level-4'))
        self.assertIsNone(children.get('style'), 'Theme should control collapsed child visibility')

    def test_no_sections_does_not_render_an_empty_heading_list(self):
        public, _ = self.builds['enabled']
        _, sidebar = self.read_page(public, 'empty')
        self.assertFalse(any(has_class(node, 'cs-menu-page-headings') for node in sidebar.iter()))

    def test_false_or_omitted_setting_keeps_page_only_navigation(self):
        for name in ['disabled', 'omitted']:
            public, _ = self.builds[name]
            with self.subTest(name=name):
                _, sidebar = self.read_page(public, 'article')
                self.assertFalse(any(link.get('href', '').startswith('#') for link in sidebar.iter('a')))
                self.assertEqual(sum(has_class(node, 'current-page') for node in sidebar.iter('li')), 1)


if __name__ == '__main__':
    unittest.main()
