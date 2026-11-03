"""Case-sensitive asset export and route-based prose reference boundaries."""
import hashlib
from html.parser import HTMLParser
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / 'tests/migration/fixtures/assets-urls'
REVISION = '76628f8aa01571fbc348211cb7df726cf408cd17'
CS_ROOT = Path(os.environ.get('MIGRATION_CASE_SENSITIVE_TMP', '/tmp/cloudscripting-task01-volume'))


class AssetsUrlsTests(unittest.TestCase):
    def module(self, name):
        try:
            return importlib.import_module('scripts.migration.' + name)
        except ModuleNotFoundError as error:
            self.fail('Required asset/URL implementation missing: ' + str(error))

    def baseline(self):
        return json.loads((ROOT / 'tests/migration/fixtures/baseline/legacy-root.json').read_text())

    def page_map(self):
        return json.loads((ROOT / 'migration/page-map.json').read_text())

    def test_markdown_legacy_media_raw_html_and_literal_bytes(self):
        # Catch treating Quick Start Markdown media as browser-relative raw HTML.
        result = self.module('content_urls').normalize_document(
            (FIXTURES / 'prose.md').read_bytes(), {'old_url': '/quick-start/', 'source_path': 'docs/quick-start.md'}, self.baseline())
        self.assertEqual(result, (FIXTURES / 'expected.md').read_bytes())

    def test_nested_destinations_resolve_in_each_build_prefix(self):
        # Catch root-absolute output escaping release or staging isolation.
        module = self.module('content_urls')
        result = module.normalize_document(b'[A](/creating-manifest/actions/?x=1#cmd) <img src="/img/x.svg">',
             {'old_url': '/creating-manifest/visual-settings/'}, self.baseline()).decode()
        self.assertEqual(result, '[A](../actions/?x=1#cmd) <img src="../../img/x.svg">')
        for prefix in ['', '8.15.1/', 'staging/docs/8.14.3/']:
            base = 'https://example.test/' + prefix
            self.assertEqual(urljoin(base + 'creating-manifest/visual-settings/', '../actions/?x=1#cmd'), base + 'creating-manifest/actions/?x=1#cmd')
            self.assertEqual(urljoin(base + 'creating-manifest/visual-settings/', '../../img/x.svg'), base + 'img/x.svg')

    def test_reference_links_nested_parentheses_and_multiline_literals(self):
        # Catch breaking Markdown titles, parenthesized paths or code/comment spans.
        source = b'''[ref][target]\n[target]: /samples/?x=(a)#part "Title"\n![x](/img/a(b).png "label")\n<!--\n<a href="/samples/">comment</a>\n-->\n~~~html\n<img src="/img/literal.png">\n~~~\n    <a href="/samples/">indented code</a>\n<pre><img src="/img/pre.png"></pre>\n'''
        expected = source.replace(b'[target]: /samples/', b'[target]: ../samples/').replace(b'](/img/a(b).png', b'](../img/a(b).png')
        self.assertEqual(self.module('content_urls').normalize_document(source, {'old_url': '/quick-start/'}, self.baseline()), expected)

    def test_html_after_multiline_code_and_comments_keeps_location(self):
        # Catch parser offsets drifting when protected newlines are masked.
        source = b'<!--\ncomment\n-->\n```html\n<a href="/literal/">code</a>\n```\n<a href="/samples/">real</a>\n'
        expected = source.replace(b'href="/samples/"', b'href="../samples/"')
        self.assertEqual(self.module('content_urls').normalize_document(source, {'old_url': '/quick-start/'}, self.baseline()), expected)

    def test_nested_list_prose_is_normalized_without_touching_indented_code(self):
        # Catch classifying every indented list continuation as literal code.
        source = b'- Item\n    [Samples](/samples/)\n\n        <a href="/literal/">list code</a>\n\n<a href="/samples/">real</a>\n'
        expected = source.replace(b'[Samples](/samples/)', b'[Samples](../samples/)').replace(b'href="/samples/"', b'href="../samples/"')
        self.assertEqual(self.module('content_urls').normalize_document(source, {'old_url': '/quick-start/'}, self.baseline()), expected)

    def test_comment_openers_inside_code_do_not_hide_following_prose(self):
        # Catch interpreting a literal comment opener as a prose comment to EOF.
        for literal in (b'```html\n<!-- literal\n```\n', b'`<!-- literal`\n', b'    <!-- literal\n\n'):
            source = literal + b'<a href="/samples/">real</a>\n'
            expected = literal + b'<a href="../samples/">real</a>\n'
            self.assertEqual(self.module('content_urls').normalize_document(source, {'old_url': '/quick-start/'}, self.baseline()), expected)

    def test_blockquote_fences_protect_normalization_and_bundling_until_valid_close(self):
        # Catch changing examples, or closing them on short/wrong/trailing fences.
        module = self.module('content_urls')
        resources = [{'relative_url': '../img/literal.png', 'name': 'bundled-literal.png'}]
        for marker in ('~', '`'):
            for prefix in ('> ', '> > '):
                with self.subTest(marker=marker, prefix=prefix):
                    other = '`' if marker == '~' else '~'
                    literal = (prefix + marker * 4 + 'html {cs_trailing_newlines=2}\n'
                        + prefix + '<img src="/img/literal.png">\n'
                        + prefix + '![literal](../img/literal.png)\n'
                        + prefix + marker * 3 + '\n'
                        + prefix + other * 4 + '\n'
                        + prefix + marker * 4 + ' trailing\n'
                        + prefix + '<a href="/samples/">literal</a>\n'
                        + prefix + marker * 5 + '\n').encode()
                    source = literal + b'<a href="/samples/">prose</a>\n![prose](/img/literal.png)\n'
                    normalized = module.normalize_document(source, {'old_url': '/quick-start/'}, self.baseline())
                    expected = literal + b'<a href="../samples/">prose</a>\n![prose](../img/literal.png)\n'
                    self.assertEqual(normalized, expected)
                    self.assertEqual(module.bundle_markdown_images(normalized, resources),
                        literal + b'<a href="../samples/">prose</a>\n![prose](bundled-literal.png)\n')

    def test_blockquote_end_does_not_hide_following_unquoted_prose(self):
        # Catch a quoted unclosed fence masking text after the quote container ends.
        for marker in ('~~~', '```'):
            with self.subTest(marker=marker):
                literal = ('> ' + marker + 'html\n> <img src="/img/literal.png">\n').encode()
                source = literal + b'<a href="/samples/">prose</a>\n'
                self.assertEqual(self.module('content_urls').normalize_document(source,
                    {'old_url': '/quick-start/'}, self.baseline()),
                    literal + b'<a href="../samples/">prose</a>\n')

    def test_rewritten_html_attribute_entities_keep_complete_url_meaning(self):
        # Catch decoded quotes terminating rewritten quoted href/src values.
        class Attributes(HTMLParser):
            def __init__(self, text):
                super().__init__()
                self.tags = []
                self.feed(text)

            def handle_starttag(self, tag, attrs):
                self.tags.append((tag, dict(attrs)))

        cases = [
            ('<a href="/samples/?q=&quot;hello&quot;&amp;x=1#&#x27;part&#39;">link</a>',
             'a', 'href', '../samples/?q="hello"&x=1#\'part\''),
            ("<a href='/samples/?q=&apos;hello&apos;&amp;x=1#&#34;part&#x22;'>link</a>",
             'a', 'href', "../samples/?q='hello'&x=1#\"part\""),
            ('<img src="/img/example.png?q=&#34;hello&#x22;#&apos;part&apos;">',
             'img', 'src', '../img/example.png?q="hello"#\'part\''),
            ("<img src='/img/example.png?q=&#39;hello&#x27;#&quot;part&quot;'>",
             'img', 'src', "../img/example.png?q='hello'#\"part\""),
        ]
        for source, tag, attr, expected in cases:
            with self.subTest(source=source):
                result = self.module('content_urls').normalize_document(source.encode(),
                    {'old_url': '/quick-start/'}, self.baseline()).decode()
                self.assertEqual(Attributes(result).tags, [(tag, {attr: expected})])

    def test_above_root_references_stay_rooted_independent_of_working_directory(self):
        # Catch POSIX relpath using the process cwd when URL joining climbs above /.
        module = self.module('content_urls')
        baseline = self.baseline()
        cases = [
            (b'![x](../img/import-button.png)', '/quick-start/', b'![x](../img/import-button.png)'),
            (b'![x](../../../img/import-button.png)', '/creating-manifest/actions/', b'![x](../../img/import-button.png)'),
            (b'<img src="../../img/import-button.png">', '/quick-start/', b'<img src="../img/import-button.png">'),
        ]
        previous = Path.cwd()
        try:
            with tempfile.TemporaryDirectory() as directory:
                for working_directory in (ROOT, Path(directory)):
                    os.chdir(working_directory)
                    for source, route, expected in cases:
                        with self.subTest(cwd=str(working_directory), source=source):
                            self.assertEqual(module.normalize_document(source, {'old_url': route}, baseline), expected)
        finally:
            os.chdir(previous)

    def test_all_exact_git_cases_and_svg_bytes_materialize(self):
        # Catch filesystem alias overwrite, checkout-byte reads or missing SVG fallback.
        module = self.module('assets')
        asset_map = module.build_asset_map(ROOT, REVISION, self.page_map(), self.baseline())
        self.assertEqual(len(asset_map['assets']), 142)
        groups = {a['casefold_collision_group'] for a in asset_map['assets'] if a['casefold_collision_group']}
        self.assertEqual(len(groups), 9)
        parent = CS_ROOT if CS_ROOT.exists() else None
        with tempfile.TemporaryDirectory(prefix='task05-', dir=parent) as directory:
            destination = Path(directory) / 'prepared'
            module.materialize(ROOT, asset_map, destination)
            for record in asset_map['assets']:
                output = destination / 'static' / record['public_url'].lstrip('/')
                self.assertEqual(hashlib.sha256(output.read_bytes()).hexdigest(), record['sha256'])
            self.assertEqual(len(list((destination / 'static/img').iterdir())), 142)
            data = json.loads((destination / 'bundle-resources.json').read_text())
            self.assertTrue(data['resources'])
            self.assertTrue(all(not r['public_url'].endswith('.svg') for r in data['resources']))

    def test_refuses_case_insensitive_destination_without_partial_assets(self):
        # Catch silently overwriting case variants on the user's default macOS volume.
        module = self.module('assets')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'case').write_text('x')
            if not (root / 'CASE').exists():
                self.skipTest('Default temporary storage is case-sensitive')
            with self.assertRaisesRegex(ValueError, 'case-sensitive'):
                module.materialize(ROOT, {'assets': []}, root / 'output')
            self.assertFalse((root / 'output/static').exists())

    def test_duplicate_basename_bundles_use_distinct_names(self):
        # Catch basename-only resource resolution selecting the wrong image.
        module = self.module('assets')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            for path, data in [('theme/readthedocs/img/a/pic.png', b'A'), ('theme/readthedocs/img/b/pic.png', b'B')]:
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            subprocess.run(['git', '-C', str(root), 'add', '.'], check=True)
            subprocess.run(['git', '-C', str(root), '-c', 'user.name=Test', '-c', 'user.email=test@example.test', 'commit', '-qm', 'assets'], check=True)
            revision = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD']).decode().strip()
            pages = {'pages': [{'published': True, 'old_url': '/quick-start/', 'target_path': 'content/quick-start/index.md'}]}
            baseline = {'pages': {'/quick-start/': {'images': [{'src': '/img/a/pic.png', 'resolved_url': '/img/a/pic.png'}, {'src': '/img/b/pic.png', 'resolved_url': '/img/b/pic.png'}]}}}
            asset_map = module.build_asset_map(root, revision, pages, baseline)
            resources = [r for a in asset_map['assets'] for r in a['bundle_resources']]
            self.assertEqual(len(resources), 2)
            self.assertEqual(len({r['name'].casefold() for r in resources}), 2)

    def test_prepare_reports_missing_git_object_and_rejects_stale_output(self):
        # Catch a failed frozen-source read escaping without an actionable report,
        # or stale excluded pages surviving in a reused production destination.
        module = self.module('prepare_content')
        parent = CS_ROOT if CS_ROOT.exists() else None
        with tempfile.TemporaryDirectory(prefix='task05-failure-', dir=parent) as directory:
            root = Path(directory)
            page_map = self.page_map()
            baseline = self.baseline()
            page_map['source_commit'] = '0' * 40
            baseline['inputs']['source_commit'] = '0' * 40
            (root / 'map.json').write_text(json.dumps(page_map))
            (root / 'baseline.json').write_text(json.dumps(baseline))
            run = subprocess.run([sys.executable, '-m', 'scripts.migration.prepare_content',
                '--source-root', str(ROOT), '--converted-dir', str(root),
                '--page-map', str(root / 'map.json'), '--baseline', str(root / 'baseline.json'),
                '--destination', str(root / 'missing'), '--report', str(root / 'missing.json')],
                cwd=ROOT, capture_output=True, text=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn('fatal: Needed a single revision', run.stderr)
            report = json.loads((root / 'missing.json').read_text())
            self.assertEqual(report['status'], 'fail')
            output = root / 'existing'
            (output / 'content/excluded').mkdir(parents=True)
            (output / 'content/excluded/index.md').write_text('must never publish')
            report = module.prepare(ROOT, root, self.page_map(), self.baseline(), output, root / 'stale.json')
            self.assertEqual(report['status'], 'fail')
            self.assertIn('empty', report['issues'][0]['evidence'])

    def test_git_replacement_refs_cannot_change_asset_bytes(self):
        # Catch replacement refs substituting asset bytes under a frozen identity.
        module = self.module('assets')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            target = root / 'theme/readthedocs/img/pic.svg'
            target.parent.mkdir(parents=True)
            target.write_bytes(b'<svg>Frozen</svg>')
            subprocess.run(['git', '-C', str(root), 'add', '.'], check=True)
            subprocess.run(['git', '-C', str(root), '-c', 'user.name=Test', '-c', 'user.email=test@example.test', 'commit', '-qm', 'asset'], check=True)
            revision = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD']).decode().strip()
            blob = subprocess.check_output(['git', '-C', str(root), 'rev-parse', revision + ':theme/readthedocs/img/pic.svg']).decode().strip()
            replacement = subprocess.check_output(['git', '-C', str(root), 'hash-object', '-w', '--stdin'], input=b'<svg>Replacement</svg>').decode().strip()
            subprocess.run(['git', '-C', str(root), 'replace', blob, replacement], check=True)
            asset_map = module.build_asset_map(root, revision, {'pages': []}, {'pages': {}})
            self.assertEqual(asset_map['assets'][0]['sha256'], hashlib.sha256(b'<svg>Frozen</svg>').hexdigest())

    def test_prepare_cli_requires_baseline_identity_and_keeps_publication_boundary(self):
        # Catch admitting excluded Markdown or using a baseline from a different source pin.
        self.module('prepare_content')
        parent = CS_ROOT if CS_ROOT.exists() else None
        with tempfile.TemporaryDirectory(prefix='task05-cli-', dir=parent) as directory:
            root = Path(directory)
            converted = root / 'converted'
            article = converted / 'content/quick-start/index.md'
            article.parent.mkdir(parents=True)
            article.write_text('---\ntitle: Quick Start\n---\n![import](img/import-button.png)\n')
            (converted / 'content/excluded').mkdir()
            (converted / 'content/excluded/index.md').write_text('Secret')
            page_map = self.page_map()
            page_map['pages'] = [p for p in page_map['pages'] if p['source_path'] == 'docs/quick-start.md']
            (root / 'map.json').write_text(json.dumps(page_map))
            (root / 'baseline.json').write_text(json.dumps(self.baseline()))
            command = [sys.executable, '-m', 'scripts.migration.prepare_content', '--source-root', str(ROOT), '--converted-dir', str(converted), '--page-map', str(root / 'map.json'), '--baseline', str(root / 'baseline.json'), '--destination', str(root / 'output'), '--report', str(root / 'report.json')]
            run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            result = (root / 'output/content/quick-start/index.md').read_text()
            self.assertIn('title: Quick Start', result)
            self.assertNotIn('](img/import-button.png)', result)
            self.assertFalse((root / 'output/content/excluded').exists())
            self.assertEqual(json.loads((root / 'report.json').read_text())['status'], 'pass')
            baseline = self.baseline()
            baseline['inputs']['source_commit'] = '0' * 40
            (root / 'baseline.json').write_text(json.dumps(baseline))
            run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertEqual(json.loads((root / 'report.json').read_text())['status'], 'fail')


if __name__ == '__main__':
    unittest.main()
