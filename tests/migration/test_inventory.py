"""Boundary tests for immutable source inventories and rendered legacy capture."""
import hashlib
import importlib
import json
import os
import sys
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
REVISION = '76628f8aa01571fbc348211cb7df726cf408cd17'


class InventoryTests(unittest.TestCase):
    def module(self, name):
        try:
            return importlib.import_module('scripts.migration.' + name)
        except ModuleNotFoundError as error:
            self.fail('Required migration tool is missing: ' + str(error))

    def test_inventory_covers_all_sources(self):
        # Catch implicit publication of unlisted pages or flattened nested routes.
        result = self.module('inventory').build_inventory(ROOT, REVISION)
        self.assertEqual(result['source_commit'], REVISION)
        self.assertEqual(result['source_kind'], 'git')
        self.assertEqual(len(result['pages']), 34)
        published = [p for p in result['pages'] if p['published']]
        self.assertEqual(len(published), 16)
        pending = [p for p in result['pages'] if not p['published']]
        self.assertEqual(len(pending), 18)
        self.assertTrue(all(p['disposition'] == 'pending' and p['target_path'] is None for p in pending))
        self.assertEqual([p['old_url'] for p in sorted(published, key=lambda p: p['weight'])], [
            '/', '/quick-start/', '/creating-manifest/basic-configs/',
            '/creating-manifest/selecting-containers/', '/creating-manifest/actions/',
            '/creating-manifest/events/', '/creating-manifest/placeholders/',
            '/creating-manifest/conditions-and-iterations/', '/creating-manifest/custom-scripts/',
            '/creating-manifest/mixins/', '/creating-manifest/addons/',
            '/creating-manifest/handling-custom-responses/', '/creating-manifest/visual-settings/',
            '/samples/', '/troubleshooting/', '/virtuozzo-cs-correspondence/'])
        pages = {p['source_path']: p for p in published}
        self.assertEqual(pages['docs/index.md']['target_path'], 'content/_index.md')
        self.assertEqual(pages['docs/creating-manifest/actions.md']['target_path'], 'content/creating-manifest/actions/index.md')
        self.assertEqual(pages['docs/creating-manifest/actions.md']['menu_parent'], 'creating-manifest')
        self.assertEqual(pages['docs/samples.md']['menu_parent'], 'samples')
        self.assertEqual([n['title'] for n in result['navigation']], [
            'GETTING STARTED', 'Creating Manifest', 'Samples', 'Troubleshooting',
            'CS vs Virtuozzo PaaS Versions'])
        self.assertEqual([n['title'] for n in result['navigation'][0]['children']], ['Overview', 'Quick Start'])
        source = subprocess.check_output(['git', '-C', str(ROOT), 'show', REVISION + ':docs/index.md'])
        self.assertEqual(pages['docs/index.md']['source_sha256'], hashlib.sha256(source).hexdigest())

    def test_excluded_engineering_docs(self):
        # Catch an inventory glob that turns plans into editorial/public content.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'docs/superpowers/plans').mkdir(parents=True)
            (root / 'docs/index.md').write_text('# Home\n')
            (root / 'docs/unlisted.md').write_text('# Unlisted\n')
            (root / 'docs/superpowers/plans/internal.md').write_text('# Secret plan\n')
            (root / 'mkdocs.yml').write_text('pages:\n  - Home: index.md\n')
            result = self.module('inventory').build_inventory(root)
            self.assertEqual([p['source_path'] for p in result['pages']], ['docs/index.md', 'docs/unlisted.md'])
            self.assertEqual(result['source_kind'], 'worktree')
            self.assertFalse(result['pages'][1]['published'])

    def test_schema_rejects_implicit_publication(self):
        # Catch a map/schema combination permitting public records without routes.
        import jsonschema
        schema_path = ROOT / 'migration/schemas/page-map.schema.json'
        self.assertTrue(schema_path.exists(), 'Required page-map schema is missing')
        schema = json.loads(schema_path.read_text())
        page_map = self.module('inventory').build_inventory(ROOT, REVISION)
        jsonschema.validate(page_map, schema)
        unpublished = next(p for p in page_map['pages'] if not p['published'])
        unpublished['published'] = True
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(page_map, schema)

    def test_git_inventory_ignores_worktree_edits(self):
        # Catch reading mutable docs or YAML while recording an immutable commit.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            (root / 'docs').mkdir()
            (root / 'docs/index.md').write_text('# Frozen\n')
            (root / 'mkdocs.yml').write_text('pages:\n  - Frozen: index.md\n')
            subprocess.run(['git', '-C', str(root), 'add', '.'], check=True)
            subprocess.run(['git', '-C', str(root), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'fixture'], check=True)
            revision = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD']).decode().strip()
            (root / 'docs/index.md').write_text('# New mutable bytes\n')
            (root / 'mkdocs.yml').write_text('pages:\n  - Unexpected: missing.md\n')
            result = self.module('inventory').build_inventory(root, revision)
            self.assertEqual(result['pages'][0]['title'], 'Frozen')
            self.assertEqual(result['pages'][0]['source_sha256'], hashlib.sha256(b'# Frozen\n').hexdigest())

    def test_git_inventory_ignores_replacement_refs(self):
        # Catch Git substituting different content under a recorded frozen SHA.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            (root / 'docs').mkdir()
            (root / 'docs/index.md').write_text('# Frozen\n')
            (root / 'mkdocs.yml').write_text('pages:\n  - Overview: index.md\n')
            subprocess.run(['git', '-C', str(root), 'add', '.'], check=True)
            subprocess.run(['git', '-C', str(root), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'frozen source'], check=True)
            frozen = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD']).decode().strip()
            (root / 'docs/index.md').write_text('# Replacement\n')
            subprocess.run(['git', '-C', str(root), 'add', '.'], check=True)
            subprocess.run(['git', '-C', str(root), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'replacement source'], check=True)
            replacement = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD']).decode().strip()
            subprocess.run(['git', '-C', str(root), 'replace', frozen, replacement], check=True)
            # Establish that the real replacement is effective for ordinary Git.
            self.assertEqual(subprocess.check_output(['git', '-C', str(root), 'show', frozen + ':docs/index.md']), b'# Replacement\n')
            result = self.module('inventory').build_inventory(root, frozen)
            self.assertEqual(result['source_commit'], frozen)
            self.assertEqual(result['pages'][0]['title'], 'Frozen')
            self.assertEqual(result['pages'][0]['source_sha256'], hashlib.sha256(b'# Frozen\n').hexdigest())

    def test_git_inventory_does_not_lazy_fetch_missing_blobs(self):
        # Catch immutable reads invoking a promisor remote for unavailable bytes.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = root / 'repo'
            subprocess.run(['git', 'init', '-q', str(repo)], check=True)
            (repo / 'docs').mkdir()
            (repo / 'docs/index.md').write_text('# Frozen\n')
            (repo / 'mkdocs.yml').write_text('pages:\n  - Overview: index.md\n')
            subprocess.run(['git', '-C', str(repo), 'add', '.'], check=True)
            subprocess.run(['git', '-C', str(repo), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'frozen source'], check=True)
            frozen = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD']).decode().strip()
            blob = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', frozen + ':docs/index.md']).decode().strip()
            for key, value in [('core.repositoryformatversion', '1'), ('extensions.partialClone', 'origin'),
                               ('remote.origin.promisor', 'true'), ('remote.origin.url', 'task01probe::unused'),
                               ('protocol.task01probe.allow', 'always')]:
                subprocess.run(['git', '-C', str(repo), 'config', key, value], check=True)
            # The only possible remote is an inert local probe; it cannot network.
            helper = root / 'git-remote-task01probe'
            helper.write_text('#!/bin/sh\nprintf attempted > "' + str(root / 'fetch-attempted') + '"\nexit 1\n')
            helper.chmod(0o755)
            (repo / '.git/objects' / blob[:2] / blob[2:]).unlink()
            environment = {**os.environ, 'PATH': str(root) + os.pathsep + os.environ['PATH']}
            result = subprocess.run([sys.executable, '-m', 'scripts.migration.inventory',
                '--source-root', str(repo), '--revision', frozen, '--output', str(root / 'map.json')],
                cwd=ROOT, env=environment, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((root / 'map.json').exists())
            self.assertFalse((root / 'fetch-attempted').exists(), 'Pinned inventory attempted a lazy remote fetch')

    def test_safe_config_tags(self):
        # Catch importing/calling arbitrary names from YAML instead of inert parsing.
        module = self.module('inventory')
        config = module.load_config('markdown_extensions:\n  - pymdownx.emoji:\n      emoji_generator: !!python/name:pymdownx.emoji.to_svg\npages:\n  - Home: index.md\n')
        self.assertEqual(config['markdown_extensions'][0]['pymdownx.emoji']['emoji_generator'], 'pymdownx.emoji.to_svg')
        with self.assertRaises(ValueError):
            module.load_config('unsafe: !!python/object/apply:os.system ["touch /tmp/should-not-exist"]')
        with self.assertRaises(ValueError):
            module.load_config('unsafe: !!python/name:os.system')

    def test_rendered_baseline(self):
        # Catch whitespace trimming, escaped code capture, lost IDs, or lost tab order.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'site/nested/topic').mkdir(parents=True)
            shutil.copyfile(ROOT / 'tests/migration/fixtures/baseline/rendered.html', root / 'site/nested/topic/index.html')
            (root / 'site/legacy-provenance.json').write_text(json.dumps({'mode': 'handwritten-test-fixture', 'source_commit': REVISION}))
            page_map = {'source_commit': REVISION, 'source_kind': 'git', 'pages': [
                {'source_path': 'docs/nested/topic.md', 'published': True, 'old_url': '/nested/topic/'}]}
            result = self.module('capture_legacy').capture_site(root / 'site', page_map, root / 'capture')
            self.assertEqual(result['status'], 'pass')
            self.assertEqual(result['site_id'], 'legacy-root')
            page = result['pages']['/nested/topic/']
            self.assertEqual(page['ids'], ['topic', 'repeat', 'repeat_1', 'sample', 'sample'])
            self.assertEqual(page['duplicate_ids'], ['sample'])
            self.assertEqual([h['id'] for h in page['headings']], ['topic', 'repeat', 'repeat_1'])
            self.assertEqual([c['language'] for c in page['code_blocks']], ['yaml', 'json'])
            raw = (root / 'capture' / page['code_blocks'][0]['text_path']).read_bytes()
            self.assertEqual(raw, b'root:\n  value: "${value}" & <literal>\n\n')
            self.assertEqual(page['code_blocks'][0]['sha256'], hashlib.sha256(raw).hexdigest())
            self.assertEqual(page['tab_panels'], [{'code_blocks': [0, 1], 'languages': ['yaml', 'json']}])
            self.assertEqual(page['images'][0]['resolved_url'], '/nested/img/Case.svg')
            self.assertEqual(page['links'][0]['resolved_url'], '/nested/missing/#anchor')
            self.assertEqual([n['href'] for n in page['navigation']], ['/', '/nested/topic/'])

    def test_unidentified_rendered_artifact_is_incomplete(self):
        # Catch treating unidentified HTML as verified build provenance.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copyfile(ROOT / 'tests/migration/fixtures/baseline/rendered.html', root / 'index.html')
            result = self.module('capture_legacy').capture_site(root, {'source_commit': REVISION, 'pages': [
                {'source_path': 'docs/index.md', 'old_url': '/', 'published': True}]}, root / 'capture')
            self.assertEqual(result['status'], 'incomplete')
            self.assertIn('missing-build-provenance', [i['id'] for i in result['issues']])

    def test_captured_git_root_has_code_and_legacy_anchor_evidence(self):
        # Characterize real vendored output: duplicate headings retain _1 IDs.
        baseline_dir = ROOT / 'tests/migration/fixtures/baseline'
        baseline = json.loads((baseline_dir / 'legacy-root.json').read_text())
        self.assertEqual(baseline['status'], 'pass')
        self.assertEqual(len(baseline['pages']), 16)
        self.assertEqual(sum(len(p['code_blocks']) for p in baseline['pages'].values()), 564)
        events = baseline['pages']['/creating-manifest/events/']
        self.assertIn('onbeforeinit_1', events['ids'])
        self.assertIn('onbeforeinstall_1', events['ids'])
        self.assertEqual(baseline['pages']['/samples/']['duplicate_ids'], ['bs-pr', 'first-col'])
        actions = baseline['pages']['/creating-manifest/actions/']
        self.assertEqual((baseline_dir / actions['code_blocks'][0]['text_path']).read_bytes(),
                         b'cmd [nodeId,nodeType,nodeGroup]:\n  - cmd1\n  - cmd2\nsayYes: true\n')
        for page in baseline['pages'].values():
            for block in page['code_blocks']:
                self.assertEqual(hashlib.sha256((baseline_dir / block['text_path']).read_bytes()).hexdigest(), block['sha256'])
        self.assertEqual(baseline['pages']['/quick-start/']['images'][0]['resolved_url'], '/img/import-button.png')

    def test_missing_rendered_page_is_incomplete(self):
        # Catch silently accepting a partial legacy artifact.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = self.module('capture_legacy').capture_site(root, {'source_commit': REVISION, 'pages': [
                {'source_path': 'docs/index.md', 'old_url': '/', 'published': True}]}, root / 'capture')
            self.assertEqual(result['status'], 'incomplete')
            self.assertIn('missing-rendered-page', [i['id'] for i in result['issues']])

    def test_capture_cli_reports_incomplete_with_nonzero_exit(self):
        # Catch tools that signal success despite missing rendered evidence.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'map.json').write_text(json.dumps({'source_commit': REVISION, 'pages': [
                {'source_path': 'docs/index.md', 'published': True, 'old_url': '/'}]}))
            result = subprocess.run(['python3', '-m', 'scripts.migration.capture_legacy', '--site-dir', str(root),
                '--page-map', str(root / 'map.json'), '--output', str(root / 'baseline.json')], cwd=ROOT, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue((root / 'baseline.json').exists(), result.stderr.decode())
            self.assertEqual(json.loads((root / 'baseline.json').read_text())['status'], 'incomplete')


if __name__ == '__main__':
    unittest.main()
