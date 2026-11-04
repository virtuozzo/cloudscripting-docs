"""Release provenance tests; use real Git objects rather than mocked commands."""
import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml

REPO = Path(__file__).resolve().parents[2]
ROOT_SHA = '76628f8aa01571fbc348211cb7df726cf408cd17'
LATEST_SHA = '6e0617cb49da66acf10335f613fcfd80820515e3'
try:
    inventory = importlib.import_module('scripts.migration.inventory_releases')
    version_data = importlib.import_module('scripts.migration.version_data')
except ModuleNotFoundError:
    inventory = version_data = None


class ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # The retired checkout config must not be an input to provenance tests.
        cls.config_dir = tempfile.TemporaryDirectory(prefix='cs-release-import-')
        cls.addClassCleanup(cls.config_dir.cleanup)
        cls.config = Path(cls.config_dir.name) / 'mkdocs.yml'
        cls.config.write_bytes(inventory.git(REPO, 'show', ROOT_SHA + ':mkdocs.yml'))

    def setUp(self):
        self.assertIsNotNone(inventory, 'release inventory implementation is missing')
        self.assertIsNotNone(version_data, 'theme data implementation is missing')

    def manifest(self):
        return inventory.build_manifest(REPO, self.config)

    # Wrong ref pinning or dropping mappings must fail this test.
    def test_all_configured_refs_pinned(self):
        manifest = self.manifest()
        self.assertEqual(len(manifest['releases']), 24)
        self.assertEqual(len({r['source_commit'] for r in manifest['releases']}), 19)
        for release in manifest['releases']:
            self.assertRegex(release['source_commit'], r'^[0-9a-f]{40}$')
            actual = subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', release['source_ref']], text=True).strip()
            self.assertEqual(release['source_commit'], actual)
        self.assertEqual(manifest['releases'][0]['platform_version'], '6.3-2')
        inventory.validate_manifest(manifest)

    # Lexicographic sorting and YAML numeric coercion break downstream version menus.
    def test_numeric_order_and_string_platforms(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'versions.yaml'
            version_data.write_theme_data(self.manifest(), destination)
            data = yaml.safe_load(destination.read_text())
        ids = [r['id'] for r in data['releases']]
        self.assertLess(ids.index('8.8.1'), ids.index('8.10.1'))
        self.assertEqual(data['default_version'], '8.15.1')
        self.assertTrue(all(isinstance(r['platform_version'], str) for r in data['releases']))
        self.assertEqual(data['releases'][0], {'id': '6.3.2', 'platform_version': '6.3-2', 'output_prefix': '6.3.2/'})

    # Using executing HEAD or latest for root loses authored root-only examples.
    def test_distinct_root_and_latest(self):
        manifest = self.manifest()
        self.assertEqual(manifest['root']['source_commit'], ROOT_SHA)
        self.assertEqual(manifest['root']['output_prefix'], '')
        self.assertEqual(manifest['root']['decision_status'], 'approved')
        latest = next(r for r in manifest['releases'] if r['id'] == '8.15.1')
        self.assertEqual(latest['source_commit'], LATEST_SHA)
        self.assertEqual(latest['output_prefix'], '8.15.1/')
        report = inventory.inventory_sources(REPO, manifest)
        root = report['inventories'][ROOT_SHA]
        self.assertEqual(len(root['editorial']), 34)
        self.assertEqual(len(root['navigation']), 16)
        self.assertEqual(len(root['assets']), 142)
        self.assertNotEqual(root['editorial'], report['inventories'][LATEST_SHA]['editorial'])

    # Deduplication by source SHA must never collapse release identities or prefixes.
    def test_shared_sha_retains_release_identity(self):
        manifest = self.manifest()
        releases = {r['id']: r for r in manifest['releases']}
        self.assertEqual(releases['8.10.2']['source_commit'], releases['8.14.3']['source_commit'])
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'versions.yaml'
            version_data.write_theme_data(manifest, destination)
            output = yaml.safe_load(destination.read_text())
        ids = [r['id'] for r in output['releases']]
        self.assertIn('8.10.2', ids)
        self.assertIn('8.14.3', ids)
        self.assertEqual(len(ids), 24)

    # Reports retain each release identity while storing a shared immutable inventory once.
    def test_shared_commit_inventory_stored_once(self):
        report = inventory.inventory_sources(REPO, self.manifest())
        self.assertTrue('inventories' in report, 'source inventories must be keyed by commit')
        self.assertEqual(len(report['inventories']), 20)
        shared = '1643f00f8e5e053f43fb3dd52bde2d1f864b0c9f'
        self.assertEqual(report['sources']['8.10.2']['inventory_key'], shared)
        self.assertEqual(report['sources']['8.14.3']['inventory_key'], shared)
        self.assertEqual(len(report['sources']), 25)

    # Normalizing punctuation would hide a separate legacy source identity.
    def test_candidates_keep_hyphenated_identity(self):
        candidates = inventory.discover_candidates(REPO)
        self.assertEqual(len(candidates), 48)
        sources = {r['id']: r['source_commit'] for r in candidates}
        self.assertEqual(sources['6.0-2'], '14a0f7ea2cce1d38e1de1d93750f9ef9dfe75c01')
        self.assertEqual(sources['6.0.2'], 'a5de631f362433f63ddfbeacd38d52e2a2164d30')

    # A manifest rerun must retain pins even when remote-tracking refs have moved.
    def test_existing_manifest_pins_are_authoritative(self):
        manifest = self.manifest()
        manifest['releases'][0]['source_commit'] = LATEST_SHA
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'manifest.yaml'
            path.write_text(yaml.safe_dump(manifest))
            actual = inventory.build_manifest(REPO, path)
        self.assertEqual(actual['releases'][0]['source_commit'], LATEST_SHA)

    # Schema failures must reject unquoted numeric mappings and traversal prefixes.
    def test_schema_rejects_unsafe_manifest(self):
        for field, value in [('platform_version', 6.3), ('source_commit', 'HEAD'), ('output_prefix', '../escape/')]:
            with self.subTest(field=field):
                manifest = self.manifest()
                manifest['releases'][0][field] = value
                with self.assertRaises(ValueError):
                    inventory.validate_manifest(manifest)
        manifest = self.manifest()
        manifest['default_version'] = '9.9.9'
        with self.assertRaises(ValueError):
            inventory.validate_manifest(manifest)

    # Missing commits and unknown publication evidence must never report production pass.
    def test_production_completeness_fails_closed(self):
        manifest = self.manifest()
        report = inventory.check_production_completeness(REPO, manifest)
        self.assertEqual(report['status'], 'incomplete')
        self.assertNotIn('root-policy-unresolved', [i['id'] for i in report['issues']])
        self.assertIn('extra-publication-unresolved', [i['id'] for i in report['issues']])
        manifest['root']['decision_status'] = 'provisional'
        provisional = inventory.check_production_completeness(REPO, manifest)
        self.assertIn('root-policy-unresolved', [i['id'] for i in provisional['issues']])
        manifest['root']['decision_status'] = 'approved'
        manifest['releases'][0]['source_commit'] = '0' * 40
        report = inventory.check_production_completeness(REPO, manifest)
        self.assertEqual(report['status'], 'fail')
        self.assertIn('missing-source-object', [i['id'] for i in report['issues']])

    # Generated repository data must actually describe the committed authoritative pins.
    def test_authoritative_manifest_and_generated_theme_data(self):
        path = REPO / 'migration/release-sources.yaml'
        self.assertTrue(path.exists(), 'authoritative manifest has not been generated')
        manifest = inventory.build_manifest(REPO, path)
        self.assertEqual(manifest['root']['source_commit'],
                         'c779dbee16190019695af0201c822a0307004842')
        self.assertEqual(manifest['root']['source_format'], 'hugo')
        self.assertEqual(len(manifest['releases']), 24)
        with tempfile.TemporaryDirectory() as directory:
            generated = Path(directory) / 'versions.yaml'
            version_data.write_theme_data(manifest, generated)
            self.assertEqual(yaml.safe_load(generated.read_text()),
                             yaml.safe_load((REPO / 'data/versions.yaml').read_text()))

    # Filesystem case folding or dirty overlays must not change recorded Git bytes.
    def test_source_inventory_preserves_exact_case_and_git_bytes(self):
        report = inventory.inventory_sources(REPO, self.manifest())
        assets = {r['path']: r for r in report['inventories'][ROOT_SHA]['assets']}
        upper = 'theme/readthedocs/img/SettingsCustom.jpg'
        lower = 'theme/readthedocs/img/settingsCustom.jpg'
        self.assertIn(upper, assets)
        self.assertIn(lower, assets)
        expected = subprocess.check_output(['git', '-C', str(REPO), 'show', ROOT_SHA + ':' + upper])
        self.assertEqual(assets[upper]['sha256'], hashlib.sha256(expected).hexdigest())
        self.assertNotEqual(assets[upper]['git_blob'], assets[lower]['git_blob'])
        self.assertFalse(any(r['path'].startswith('docs/superpowers/')
                             for r in report['inventories'][ROOT_SHA]['editorial']))

    # Replacement refs must not change bytes attributed to an immutable commit identity.
    def test_git_replacement_refs_cannot_substitute_source_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            def git(*args):
                return subprocess.check_output(['git', '-C', str(repo), *args], stderr=subprocess.DEVNULL).decode().strip()
            git('init', '-q')
            git('config', 'user.email', 'fixture@example.invalid')
            git('config', 'user.name', 'Fixture')
            (repo / 'value.txt').write_text('original bytes')
            git('add', 'value.txt')
            git('commit', '-qm', 'Original')
            original = git('rev-parse', 'HEAD')
            (repo / 'value.txt').write_text('substituted bytes')
            git('add', 'value.txt')
            git('commit', '-qm', 'Replacement')
            replacement = git('rev-parse', 'HEAD')
            git('replace', original, replacement)
            self.assertEqual(inventory.git(repo, 'show', original + ':value.txt'), b'original bytes')

    # CLI reports uncertainty nonzero in production mode; ordinary source audit remains usable.
    def test_cli_production_gate_and_immutable_reads(self):
        before = subprocess.check_output(['git', '-C', str(REPO), 'status', '--porcelain=v1', '-z'])
        refs_before = subprocess.check_output(['git', '-C', str(REPO), 'for-each-ref', 'refs/remotes/origin/'])
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory) / 'manifest.yaml'
            report = Path(directory) / 'report.json'
            command = [sys.executable, '-m', 'scripts.migration.inventory_releases', '--repo', str(REPO), '--config', str(self.config), '--output', str(out), '--report', str(report)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            evidence = json.loads(report.read_text())
            self.assertEqual(evidence['status'], 'incomplete')
            self.assertEqual(evidence['checks']['configured_source_commits'], 19)
            self.assertEqual(evidence['checks']['candidate_count'], 48)
            result = subprocess.run(command + ['--production'], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
        self.assertEqual(before, subprocess.check_output(['git', '-C', str(REPO), 'status', '--porcelain=v1', '-z']))
        self.assertEqual(refs_before, subprocess.check_output(['git', '-C', str(REPO), 'for-each-ref', 'refs/remotes/origin/']))


if __name__ == '__main__':
    unittest.main()
