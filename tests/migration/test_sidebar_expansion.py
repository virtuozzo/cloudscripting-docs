"""Configured open branches must render before JS, including beyond lazy depth."""
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


class SidebarExpansionTests(unittest.TestCase):
    def render(self, configured):
        with tempfile.TemporaryDirectory(prefix='cs-sidebar-') as temporary:
            work = Path(temporary)
            (work / 'themes').symlink_to(ROOT / 'themes')
            (work / 'content').mkdir()
            (work / 'content/_index.md').write_text('---\ntitle: Home\n---\nHome\n')
            shutil.copytree(ROOT / 'layouts/partials/sidebar', work / 'layouts/partials/sidebar')
            (work / 'layouts/index.html').write_text('''{{ $menu := partial "sidebar/menu.html" . }}
{{ partial "sidebar/branch.html" (dict "menu" $menu "ids" $menu.ids "level" 1 "open" slice "current" slice "depth" 1) }}''')
            params = {'hostName': 'example.test'}
            if configured is not None:
                params['docsMenu'] = {'alwaysOpen': configured}
            config = {'baseURL': 'https://example.test/', 'theme': 'compose-master', 'params': params,
                      'menu': {'docs': [
                          {'name': 'Parent', 'identifier': 'parent', 'weight': 10},
                          {'name': 'Nested', 'identifier': 'nested', 'parent': 'parent', 'weight': 20},
                          {'name': 'Leaf', 'identifier': 'leaf', 'parent': 'nested', 'weight': 30, 'url': '/article/'},
                          {'name': 'Other', 'identifier': 'other', 'weight': 40},
                          {'name': 'Other leaf', 'identifier': 'other-leaf', 'parent': 'other', 'weight': 50, 'url': '/other/'},
                      ]}}
            (work / 'config.json').write_text(json.dumps(config))
            run = subprocess.run([HUGO, '--source', str(work), '--config', 'config.json'], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            return html5lib.parse((work / 'public/index.html').read_text(), namespaceHTMLElements=False)

    def test_configured_nested_group_and_ancestors_render_open_beyond_lazy_depth(self):
        tree = self.render(['nested'])
        groups = {node.get('data-id'): node for node in tree.iter('li') if node.get('data-id')}
        for key in ['0', '0.0']:
            self.assertIn(key, groups, 'Always-open branch must be rendered in initial HTML')
            self.assertIn('cs-menu-always-open', groups[key].get('class', '').split())
        self.assertNotIn('expanded', groups['1'].get('class', '').split())
        self.assertIn('https://example.test/article/', [node.get('href') for node in tree.iter('a')])

    def test_omitted_or_empty_setting_keeps_normal_collapsible_behavior(self):
        for configured in [None, []]:
            with self.subTest(configured=configured):
                tree = self.render(configured)
                groups = list(tree.iter('li'))
                self.assertEqual(len(groups), 2, 'Unopened deeper groups stay lazy')
                self.assertFalse(any('expanded' in node.get('class', '').split() for node in groups))
                self.assertFalse(any('cs-menu-always-open' in node.get('class', '').split() for node in groups))


if __name__ == '__main__':
    unittest.main()
