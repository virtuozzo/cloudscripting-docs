"""Isolation and immutable-artifact contracts; rendering is an external boundary."""
import copy
from contextlib import ExitStack, redirect_stderr
import io
import hashlib
import html5lib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from urllib.parse import urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / 'tests/migration/fixtures/validation'
try:
    from scripts.migration import release_build as builder
    from scripts.migration.assemble_artifact import assemble_artifact, publish_artifact
except ImportError:
    builder = None


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.PIPE).decode().strip()


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n')


class ReleaseBuildTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(builder, 'isolated release builder is not implemented')
        self.temp = tempfile.TemporaryDirectory(dir=os.environ.get('MIGRATION_TEST_ROOT'))
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        git(self.repo, 'init', '-b', 'feat/fixture')
        git(self.repo, 'config', 'user.name', 'Fixture')
        git(self.repo, 'config', 'user.email', 'fixture@example.test')
        (self.repo / 'docs').mkdir()
        (self.repo / 'docs/index.md').write_text('# Overview\n\nolder release\n')
        (self.repo / 'docs/guide.md').write_text('# Guide\n\n```yaml\nvalue: ${token}\n```\n')
        (self.repo / 'docs/draft.md').write_text('# Draft\n')
        (self.repo / 'mkdocs.yml').write_text('pages:\n - Overview: index.md\n - Guide: guide.md\n')
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '-m', 'historical source')
        self.old = git(self.repo, 'rev-parse', 'HEAD')
        (self.repo / 'docs/index.md').write_text('# Overview\n\nroot Ubuntu24\n')
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '-m', 'current root')
        self.current = git(self.repo, 'rev-parse', 'HEAD')
        self.manifest = yaml.safe_load((ROOT / 'migration/release-sources.yaml').read_text())
        self.manifest['production_base_url'] = 'https://docs.cloudscripting.com/'
        self.manifest['root']['source_commit'] = self.current
        self.manifest['root']['decision_status'] = 'approved'
        self.manifest['candidate_publication']['decision_status'] = 'approved'
        record = copy.deepcopy(self.manifest['releases'][0])
        self.manifest['releases'] = []
        for identity in ('8.14.3', '8.15.1'):
            entry = dict(record, id=identity, output_prefix=identity+'/', source_commit=self.old, decision_status='approved')
            self.manifest['releases'].append(entry)
        self.manifest['default_version'] = '8.15.1'
        self.manifest_path = self.root / 'manifest.yaml'
        self.write_manifest()

    def write_manifest(self):
        self.manifest_path.write_text(yaml.safe_dump(self.manifest))

    def outputs(self, record, destination, base_url=None):
        """Literal independent fixture producer, standing in for expensive Hugo."""
        from scripts.migration.check_site import check_site
        site = destination / 'public'
        shutil.copytree(FIXTURE / 'site', site)
        prefix = record['output_prefix']
        base = (base_url or self.manifest['production_base_url']) + prefix
        public_prefix = urlsplit(base).path
        marker = git(self.repo, 'show', record['source_commit']+':docs/index.md')
        for path in site.rglob('*'):
            if path.is_file() and path.suffix in {'.html', '.xml', '.json', '.txt'}:
                value = path.read_text().replace('https://docs.cloudscripting.com/', base)
                if public_prefix != '/':
                    value = value.replace('href="/', 'href="'+public_prefix).replace('src="/', 'src="'+public_prefix)
                if path.suffix == '.html' and record['id'] != 'root':
                    value = value.replace('<head>', '<head><meta name="robots" content="noindex">')
                path.write_text(value)
        for name in ('index.html', 'index.json', 'sitemap.xml'):
            with (site / name).open('a') as handle:
                handle.write('\n<!-- '+marker.replace('\n', ' ')+' '+record['id']+' -->\n' if name != 'index.json' else '')
        (site / '.htaccess').write_text('Redirect fixture '+record['id']+'\n')
        (site / 'img/Icon.svg').write_bytes(b'<svg>'+record['id'].encode()+b'</svg>')
        # The semantic validator checks exact original images; retain its fixture
        # byte expectations and use a separate emitted asset for release identity.
        shutil.copyfile(FIXTURE/'site/img/Icon.svg', site/'img/Icon.svg')
        (site / 'img/Identity.txt').write_text(record['id'])
        page_map = json.loads((FIXTURE/'page-map.json').read_text())
        baseline = json.loads((FIXTURE/'baseline.json').read_text())
        baseline['inputs']['source_commit'] = record['source_commit']
        baseline['build_provenance']['source_commit'] = record['source_commit']
        page_map['source_commit'] = record['source_commit']
        ex = json.loads((FIXTURE/'exceptions.json').read_text())
        for entry in ex['exceptions']:
            entry['source_commit'] = record['source_commit']
        dump(destination/'baseline.json', baseline)
        dump(destination/'page-map.json', page_map)
        dump(destination/'exceptions.json', ex)
        shutil.copytree(FIXTURE/'code', destination/'code')
        report = check_site(destination/'baseline.json', destination/'page-map.json', site, base, destination/'exceptions.json', archived=record['id'] != 'root')
        self.assertEqual(report['status'], 'pass', report)
        return {'record': record, 'site_dir': site, 'report': report, 'validation_source_commit': record['source_commit']}

    def assemble(self):
        records = builder.select_builds(self.manifest)
        builds = []
        for record in records:
            directory = self.root / ('build-'+record['id'])
            directory.mkdir()
            builds.append(self.outputs(record, directory))
        staging = self.root/'assembled'
        metadata = dict(tooling_commit=self.current, theme_commit='91b3863e863981905ba45566832022270a56085f', tools={'hugo':'0.124.1', 'hugo_extended':True, 'task':'3.44.1'})
        assemble_artifact(staging, self.manifest_path, self.manifest, builds, self.manifest['production_base_url'], 'production', metadata)
        return staging

    def test_root_latest_and_shared_sha_ids_remain_independent(self):
        from scripts.migration.check_artifact import check_artifact
        artifact = self.assemble()
        self.assertIn('root Ubuntu24', (artifact/'site/index.html').read_text())
        self.assertIn('older release', (artifact/'site/8.15.1/index.html').read_text())
        for identity in ('8.14.3', '8.15.1'):
            self.assertEqual((artifact/'site'/identity/'img/Identity.txt').read_text(), identity)
            self.assertIn('/'+identity+'/', (artifact/'site'/identity/'index.json').read_text())
            self.assertIn('/'+identity+'/', (artifact/'site'/identity/'sitemap.xml').read_text())
            self.assertEqual((artifact/'site'/identity/'.htaccess').read_text(), 'Redirect fixture '+identity+'\n')
        result = check_artifact(artifact, self.manifest_path)
        self.assertEqual(result['status'], 'pass', result)

    def test_preview_remains_non_promotable(self):
        from scripts.migration.check_artifact import check_artifact
        artifact = self.assemble()
        meta = json.loads((artifact/'artifact.json').read_text())
        meta['kind'] = 'preview'
        dump(artifact/'artifact.json', meta)
        result = check_artifact(artifact, self.manifest_path)
        self.assertTrue(any(i['id']=='preview-artifact' for i in result['issues']))
        self.assertEqual([r['id'] for r in builder.select_builds(self.manifest, '8.15.1')], ['8.15.1'])

    def test_rejects_invalid_overlapping_and_traversing_prefixes(self):
        for prefix in ('../escape/', '/absolute/', '8.15.1/sub/', '8.14.3/', '8.15.1\\x/', '%2e%2e/'):
            with self.subTest(prefix=prefix):
                bad = copy.deepcopy(self.manifest)
                bad['releases'][1]['output_prefix'] = prefix
                with self.assertRaises(ValueError):
                    builder.select_builds(bad)

    def test_missing_source_object_fails_without_changing_repo(self):
        before = git(self.repo, 'status', '--porcelain=v1')
        with self.assertRaises(ValueError):
            builder.export_tree(self.repo, 'f'*40, self.root/'export')
        self.assertEqual(git(self.repo, 'status', '--porcelain=v1'), before)
        self.assertEqual(git(self.repo, 'rev-parse', 'HEAD'), self.current)

    def test_export_preserves_exact_case_and_rejects_symlinks(self):
        image = self.repo/'theme/readthedocs/img'
        image.mkdir(parents=True)
        (image/'Icon.svg').write_bytes(b'UPPER')
        (image/'icon.svg').write_bytes(b'lower')
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '-m', 'case variants')
        revision = git(self.repo, 'rev-parse', 'HEAD')
        builder.export_tree(self.repo, revision, self.root/'export')
        self.assertEqual((self.root/'export/theme/readthedocs/img/Icon.svg').read_bytes(), b'UPPER')
        self.assertEqual((self.root/'export/theme/readthedocs/img/icon.svg').read_bytes(), b'lower')
        (self.repo/'outside').symlink_to('/tmp')
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '-m', 'symlink')
        with self.assertRaisesRegex(ValueError, 'regular'):
            builder.export_tree(self.repo, git(self.repo, 'rev-parse', 'HEAD'), self.root/'unsafe')

    def test_failed_build_keeps_prior_artifact_untouched(self):
        prior = self.root/'artifact'
        shutil.copytree(self.assemble(), prior)
        before = {p.relative_to(prior).as_posix():p.read_bytes() for p in prior.rglob('*') if p.is_file()}
        def fail(record, destination):
            if record['id']=='8.15.1':
                raise ValueError('forced build failure')
            destination.mkdir()
            return self.outputs(record, destination)
        with self.assertRaisesRegex(ValueError, 'forced build failure'):
            builder.build_and_publish(self.manifest_path, prior, self.root/'work', self.manifest['production_base_url'], fail, {'tooling_commit':self.current}, jobs=2)
        self.assertEqual({p.relative_to(prior).as_posix():p.read_bytes() for p in prior.rglob('*') if p.is_file()}, before)

    def test_success_replaces_complete_directory_and_preserves_old_on_collision(self):
        target = self.root/'artifact'
        target.mkdir()
        (target/'old').write_bytes(b'prior')
        stage = self.assemble()
        publish_artifact(stage, target)
        self.assertTrue((target/'site/8.15.1/index.html').is_file())
        self.assertFalse((target/'old').exists())

    def test_failed_site_report_cannot_be_assembled(self):
        rec = builder.select_builds(self.manifest)[0]
        directory = self.root/'bad-build'
        directory.mkdir()
        build = self.outputs(rec, directory)
        build['report']['status'] = 'fail'
        with self.assertRaisesRegex(ValueError, 'validation'):
            assemble_artifact(self.root/'bad', self.manifest_path, self.manifest, [build], self.manifest['production_base_url'], 'production', {})

    def test_catalog_requires_exact_pins_and_safe_regular_inputs(self):
        catalog = {'schema_version':1, 'builds':[]}
        for record in builder.select_builds(self.manifest):
            catalog['builds'].append(dict(id=record['id'], source_commit=record['source_commit'], validation_source_commit=record['source_commit'], page_map='page-map.json', baseline='baseline.json', exceptions='exceptions.json'))
        for name in ('page-map.json', 'baseline.json', 'exceptions.json'):
            dump(self.repo/name, {})
        path = self.root/'catalog.json'
        dump(path, catalog)
        result = builder.load_acceptance_catalog(self.repo, path, builder.select_builds(self.manifest))
        self.assertEqual(set(result), {'root','8.14.3','8.15.1'})
        for mutation in ('pin', 'path', 'duplicate', 'missing'):
            bad = copy.deepcopy(catalog)
            if mutation=='pin': bad['builds'][0]['source_commit'] = self.old
            if mutation=='path': bad['builds'][0]['baseline'] = '../baseline.json'
            if mutation=='duplicate': bad['builds'].append(bad['builds'][0])
            if mutation=='missing': bad['builds'].pop()
            dump(path, bad)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                builder.load_acceptance_catalog(self.repo, path, builder.select_builds(self.manifest))

    def test_publication_maps_cannot_change_source_hashes_or_routes(self):
        from scripts.migration.inventory import build_inventory
        accepted = build_inventory(self.repo, self.current)
        for page in accepted['pages']:
            if not page['published']:
                page['disposition'] = 'intentionally-unpublished'
        builder.validate_publication_map(self.repo, self.current, accepted)
        for field, value in (('source_sha256','0'*64), ('old_url','/invented/')):
            bad = copy.deepcopy(accepted)
            bad['pages'][0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                builder.validate_publication_map(self.repo, self.current, bad)
        accepted['pages'][0]['disposition'] = 'pending'
        with self.assertRaisesRegex(ValueError, 'disposition'):
            builder.validate_publication_map(self.repo, self.current, accepted)


    def test_assembly_rejects_changed_validated_bytes(self):
        record = builder.select_builds(self.manifest)[0]
        directory = self.root/'changed-build'
        directory.mkdir()
        build = self.outputs(record, directory)
        (build['site_dir']/'index.html').write_text('changed after validation')
        with self.assertRaisesRegex(ValueError, 'changed after validation'):
            assemble_artifact(self.root/'changed', self.manifest_path, self.manifest, [build], self.manifest['production_base_url'], 'preview', {})

    def test_root_cannot_hide_files_inside_release_slice(self):
        record = builder.select_builds(self.manifest)[0]
        directory = self.root/'overlap-build'
        directory.mkdir()
        build = self.outputs(record, directory)
        (build['site_dir']/'8.14.3').mkdir()
        (build['site_dir']/'8.14.3/leak.txt').write_text('root leak')
        # Other slices are declared so root output cannot occupy their prefixes.
        builds = [build]
        for release in builder.select_builds(self.manifest)[1:]:
            d = self.root/release['id']
            d.mkdir()
            builds.append(self.outputs(release, d))
        with self.assertRaisesRegex(ValueError, 'overlaps'):
            assemble_artifact(self.root/'overlap', self.manifest_path, self.manifest, builds, self.manifest['production_base_url'], 'production', {})

    def test_portable_publication_failure_restores_prior_directory(self):
        from scripts.migration import assemble_artifact as assembly
        target = self.root/'prior'
        target.mkdir()
        (target/'original').write_bytes(b'keep me')
        stage = self.root/'new'
        stage.mkdir()
        (stage/'replacement').write_bytes(b'new')
        real_replace = os.replace
        def fail_install(source, destination):
            if Path(source)==stage:
                raise OSError('forced rename failure')
            return real_replace(source, destination)
        with patch.object(assembly, '_exchange', return_value=False), patch.object(assembly.os, 'replace', side_effect=fail_install):
            with self.assertRaisesRegex(OSError, 'forced rename failure'):
                publish_artifact(stage, target)
        self.assertEqual((target/'original').read_bytes(), b'keep me')
        self.assertFalse((target/'replacement').exists())

    def test_actual_hugo_and_task_versions_are_checked(self):
        for name, output in (('hugo', 'hugo v0.124.1+extended fixture'), ('task', 'Task version: v3.44.1')):
            path = self.root/name
            path.write_text('#!/bin/sh\nprintf \'%s\\n\' \''+output+'\'\n')
            path.chmod(0o755)
        self.assertEqual(builder.verify_tools(self.root/'hugo', self.root/'task')['task'], '3.44.1')
        (self.root/'hugo').write_text('#!/bin/sh\necho "hugo v0.124.1 fixture"\n')
        with self.assertRaisesRegex(ValueError, 'Extended'):
            builder.verify_tools(self.root/'hugo', self.root/'task')

    def test_official_hugo_extended_version_is_accepted(self):
        hugo = self.root/'official-hugo'
        hugo.write_text('#!/bin/sh\necho "hugo v0.124.1-db083b05f16c945fec04f745f0ca8640560cf1ec+extended linux/amd64 BuildDate=2024-03-20T11:40:10Z VendorInfo=gohugoio"\n')
        task = self.root/'task'
        task.write_text('#!/bin/sh\necho "Task version: v3.44.1"\n')
        hugo.chmod(0o755)
        task.chmod(0o755)
        self.assertEqual(builder.verify_tools(hugo, task),
                         {'hugo':'0.124.1', 'hugo_extended':True, 'task':'3.44.1'})

    def test_wrong_hugo_versions_and_non_extended_builds_are_rejected(self):
        hugo, task = self.root/'hugo', self.root/'task'
        task.write_text('#!/bin/sh\necho "Task version: v3.44.1"\n')
        task.chmod(0o755)
        versions = ('v0.124.1', 'v0.124.1-db083b05', 'v0.124.2+extended',
                    'v0.124.10+extended', 'v0.124.1-rc.1+extended', 'v0.124.1+extended-bogus')
        for version in versions:
            with self.subTest(version=version):
                hugo.write_text('#!/bin/sh\necho "hugo '+version+'"\n')
                hugo.chmod(0o755)
                with self.assertRaisesRegex(ValueError, 'Require Hugo Extended 0.124.1'):
                    builder.verify_tools(hugo, task)



    def test_schema_rejects_unidentified_tooling_even_for_preview(self):
        record = builder.select_builds(self.manifest)[0]
        directory = self.root/'unidentified-build'
        directory.mkdir()
        build = self.outputs(record, directory)
        with self.assertRaisesRegex(ValueError, 'schema'):
            assemble_artifact(self.root/'unidentified', self.manifest_path, self.manifest, [build], self.manifest['production_base_url'], 'preview', {'tooling_commit':'moving-head'})



    def exercise_pipeline(self, authored, damage=False, build_id='root', base_url=None):
        from scripts.migration.inventory import build_inventory
        images = self.repo/'theme/readthedocs/img'
        images.mkdir(parents=True)
        shutil.copyfile(FIXTURE/'site/img/Icon.svg', images/'Icon.svg')
        (images/'icon.svg').write_bytes(b'lower-case variant')
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '-m', 'exact reference assets')
        validation_pin = git(self.repo, 'rev-parse', 'HEAD')
        if authored:
            (self.repo/'content').mkdir()
            (self.repo/'content/search.md').write_text('UNREVIEWED SOURCE SEARCH')
            (self.repo/'content/_index.md').write_text('---\ntitle: Overview\n---\nAuthored Ubuntu24\n')
            (self.repo/'content/guide').mkdir()
            (self.repo/'content/guide/index.md').write_text('---\ntitle: Guide\n---\nAuthored Guide\n')
            (self.repo/'layouts').mkdir()
            (self.repo/'layouts/index.html').write_text('UNREVIEWED SOURCE TOOLING')
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '--allow-empty', '-m', 'optional authored content')
        pin = git(self.repo, 'rev-parse', 'HEAD')
        if not authored:
            validation_pin = pin
        record = dict(self.manifest['root'], id=build_id, source_commit=pin,
                      output_prefix='' if build_id == 'root' else build_id+'/',
                      source_format='hugo' if authored else 'mkdocs')
        accepted_map = build_inventory(self.repo, validation_pin)
        for page in accepted_map['pages']:
            if not page['published']:
                page['disposition'] = 'intentionally-unpublished'
        baseline = json.loads((FIXTURE/'baseline.json').read_text())
        baseline['inputs']['source_commit'] = validation_pin
        baseline['build_provenance']['source_commit'] = validation_pin
        exceptions = json.loads((FIXTURE/'exceptions.json').read_text())
        for entry in exceptions['exceptions']:
            entry['source_commit'] = validation_pin
        dump(self.repo/'accepted/page-map.json', accepted_map)
        dump(self.repo/'accepted/baseline.json', baseline)
        dump(self.repo/'accepted/exceptions.json', exceptions)
        shutil.copytree(FIXTURE/'code', self.repo/'accepted/code')
        tooling = self.root/'tooling'
        (tooling/'content').mkdir(parents=True)
        shutil.copyfile(ROOT/'config.yaml', tooling/'config.yaml')
        (tooling/'content/search.md').write_text('---\ntitle: Search\n---\n')
        (tooling/'layouts').mkdir()
        (tooling/'layouts/index.html').write_text('REVIEWED TOOLING')
        inputs = dict(source_commit=pin, validation_source_commit=validation_pin, page_map=self.repo/'accepted/page-map.json', baseline=self.repo/'accepted/baseline.json', exceptions=self.repo/'accepted/exceptions.json')
        run = builder.ReleaseBuilder(self.repo, self.manifest, [record], {build_id:inputs}, pin, tooling, '/fixture/hugo')
        run.base_url = base_url or self.manifest['production_base_url']
        destination = self.root/'pipeline'
        real_run = subprocess.run
        def render(command, **kwargs):
            if command[0] != '/fixture/hugo':
                return real_run(command, **kwargs)
            self.assertEqual(command[0], '/fixture/hugo')
            rendered = destination/'renderer-fixture'
            rendered.mkdir()
            self.outputs(record, rendered, run.base_url)
            shutil.copytree(rendered/'public', destination/'public')
            shutil.copytree(destination/'hugo/static', destination/'public', dirs_exist_ok=True)
            if damage:
                guide = destination/'public/guide/index.html'
                guide.write_text(guide.read_text().replace('${token}', '${changed}'))
            return SimpleNamespace(returncode=0, stdout='fixture render', stderr='')
        before = git(self.repo, 'status', '--porcelain=v1')
        with patch('scripts.migration.release_build.subprocess.run', side_effect=render):
            if damage:
                with self.assertRaises(ValueError) as caught:
                    run(record, destination)
                self.assertNotIsInstance(caught.exception, builder.IncompleteInputs)
                return
            result = run(record, destination)
        self.assertEqual(result['report']['status'], 'pass', result)
        self.assertEqual(result['validation_source_commit'], validation_pin)
        if authored:
            self.assertNotEqual(pin, validation_pin)
        stage = destination/'hugo'
        self.assertIn('Authored Ubuntu24' if authored else 'root Ubuntu24', (stage/'content/_index.md').read_text())
        self.assertEqual((stage/'static/img/Icon.svg').read_bytes(), (FIXTURE/'site/img/Icon.svg').read_bytes())
        self.assertEqual((stage/'static/img/icon.svg').read_bytes(), b'lower-case variant')
        self.assertEqual((stage/'layouts/index.html').read_text(), 'REVIEWED TOOLING')
        self.assertFalse((stage/'content/draft').exists())
        self.assertEqual((stage/'content/search.md').read_text(), '---\ntitle: Search\n---\n')
        self.assertEqual(git(self.repo, 'status', '--porcelain=v1'), before)
        config = yaml.safe_load((stage/'release.yaml').read_text())
        self.assertEqual(config['params']['archived'], build_id != 'root')
        self.assertEqual(config['params']['csVersionURLs']['8.15.1'], run.base_url+'8.15.1/')
        return stage

    def assert_release_version_selector(self, build_id, base):
        stage = self.exercise_pipeline(build_id == 'root', build_id=build_id, base_url=base)
        # Render the real theme controls with the builder's generated config.
        # Do not inject version params here: their absence caused the archive bug.
        (stage/'themes').symlink_to(ROOT/'themes', target_is_directory=True)
        (stage/'layouts/partials').mkdir()
        shutil.copyfile(ROOT/'layouts/partials/versions-list.html', stage/'layouts/partials/versions-list.html')
        (stage/'layouts/index.html').write_text('{{ partial "nav.html" . }}{{ partial "sidebar.html" . }}')
        public = self.root/'selector-site'
        result = subprocess.run([os.environ.get('HUGO_BIN', 'hugo'), '--source', str(stage),
                                 '--config', 'config.yaml,release.yaml', '--destination', str(public)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        tree = html5lib.parse((public/'index.html').read_text(), namespaceHTMLElements=False)
        selectors = [node for node in tree.iter('div') if node.get('class') == 'versions']
        self.assertEqual(len(selectors), 2, 'Desktop and mobile version selectors must be rendered')
        prefix = '' if build_id == 'root' else build_id+'/'
        for selector in selectors:
            label = next(node for node in selector.iter('span') if node.get('class') == 'current')
            self.assertEqual(''.join(label.itertext()).strip(), '8.15.1' if build_id == 'root' else build_id)
            links = list(selector.iter('a'))
            self.assertEqual([link.get('href') for link in links], [base, base+'8.15.1/', base+'8.14.3/'])
            self.assertEqual([link.get('href') for link in links if link.get('aria-current') == 'true'], [base+prefix])
            self.assertTrue(all(link.get('data-vs-from') == base+prefix for link in links))

    def test_current_release_version_selector_on_test_domain(self):
        self.assert_release_version_selector('root', 'https://cs-docs-test.bilbao.jele.io/')

    def test_archived_release_version_selector_on_test_domain(self):
        self.assert_release_version_selector('8.14.3', 'https://cs-docs-test.bilbao.jele.io/')

    def test_latest_release_version_selector_on_production_prefix(self):
        self.assert_release_version_selector('8.15.1', 'https://www.virtuozzo.com/cloudscripting-docs/')

    def test_semantic_regression_is_failure_not_missing_evidence(self):
        self.exercise_pipeline(False, damage=True)

    def test_mkdocs_pipeline_converts_without_legacy_runtime(self):
        self.exercise_pipeline(False)

    def test_authored_pipeline_materializes_reference_assets_and_uses_pinned_tooling(self):
        self.exercise_pipeline(True)



    def test_correspondence_title_correction_is_exact_template_bound(self):
        from scripts.migration.inventory import build_inventory
        source = self.repo/'docs/virtuozzo-cs-correspondence.md'
        source.write_text('---\ntemplate: virtuozzo-cs-correspondence.html\n---\n')
        template = self.repo/'theme/readthedocs/virtuozzo-cs-correspondence.html'
        template.parent.mkdir(parents=True)
        shutil.copyfile(ROOT/'tests/migration/fixtures/conversion/correspondence-template.html', template)
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '-m', 'exact generated correspondence template')
        pin = git(self.repo, 'rev-parse', 'HEAD')
        accepted = build_inventory(self.repo, pin)
        for page in accepted['pages']:
            if not page['published']:
                page['disposition'] = 'intentionally-unpublished'
            if page['source_path']==source.relative_to(self.repo).as_posix():
                page['title'] = 'Virtuozzo Application Platform & CS Correspondence'
        builder.validate_publication_map(self.repo, pin, accepted)
        for page in accepted['pages']:
            if page['source_path']==source.relative_to(self.repo).as_posix():
                page['title'] = 'Invented correspondence title'
        with self.assertRaises(ValueError):
            builder.validate_publication_map(self.repo, pin, accepted)



    def redirects_cli_fixture(self):
        """Real immutable CLI pipeline; fixed pages isolate redirect rendering."""
        from scripts.migration.inventory import build_inventory
        images = self.repo/'theme/readthedocs/img'
        images.mkdir(parents=True)
        shutil.copyfile(FIXTURE/'site/img/Icon.svg', images/'Icon.svg')
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '-m', 'redirect reference source')
        source_pin = git(self.repo, 'rev-parse', 'HEAD')
        self.manifest['root'].update(source_commit=source_pin, source_format='mkdocs')
        self.write_manifest()
        accepted = build_inventory(self.repo, source_pin)
        for page in accepted['pages']:
            if not page['published']:
                page['disposition'] = 'intentionally-unpublished'
        baseline = json.loads((FIXTURE/'baseline.json').read_text())
        baseline['inputs']['source_commit'] = source_pin
        baseline['build_provenance']['source_commit'] = source_pin
        exceptions = json.loads((FIXTURE/'exceptions.json').read_text())
        for entry in exceptions['exceptions']:
            entry['source_commit'] = source_pin
        for name, value in (('page-map', accepted), ('baseline', baseline), ('exceptions', exceptions)):
            dump(self.repo/('accepted/'+name+'.json'), value)
        shutil.copytree(FIXTURE/'code', self.repo/'accepted/code')
        catalog = self.root/'acceptance.json'
        dump(catalog, {'schema_version':1, 'builds':[dict(id='root', source_commit=source_pin,
            validation_source_commit=source_pin, page_map='accepted/page-map.json',
            baseline='accepted/baseline.json', exceptions='accepted/exceptions.json')]})
        # Serve the existing acceptance pages unchanged; Hugo really renders the
        # shipped redirect template using the exported config and input file.
        shutil.copytree(FIXTURE/'site', self.repo/'static')
        config = yaml.safe_load((ROOT/'config.yaml').read_text())
        (self.repo/'config.yaml').write_text(yaml.safe_dump({
            'outputs':{'home':['HTACCESS']}, 'mediaTypes':config['mediaTypes'],
            'outputFormats':config['outputFormats'], 'params':{'readRedirects':True},
            'disableKinds':['taxonomy','term','RSS','sitemap']}))
        (self.repo/'layouts').mkdir()
        shutil.copyfile(ROOT/'layouts/index.htaccess', self.repo/'layouts/index.htaccess')
        rule = b'# committed fixture input\nRewriteRule ^fixture-old/$ fixture-new/ [R=301,L,NE]\n'
        (self.repo/'redirects.htaccess').write_bytes(rule)
        subprocess.run(['git', 'clone', '--shared', '--quiet', str(ROOT/'themes'),
                        str(self.repo/'themes')], check=True, capture_output=True)
        git(self.repo/'themes', 'checkout', '--detach', builder.THEME)
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '-m', 'immutable redirect tooling')
        tooling_pin = git(self.repo, 'rev-parse', 'HEAD')
        task = self.root/'task'
        task.write_text('#!/bin/sh\necho "Task version: v3.44.1"\n')
        task.chmod(0o755)
        output, report = self.root/'redirect-artifact', self.root/'redirect-report.json'
        output.mkdir()
        (output/'prior').write_bytes(b'prior complete artifact')
        args = self.main_args(output, report, catalog) + [
            '--work-dir', str(self.root/'redirect-work'),
            '--hugo', os.environ.get('HUGO_BIN', 'hugo'), '--task', str(task)]
        return args, output, report, tooling_pin, rule

    def test_committed_redirects_reach_isolated_hugo_render(self):
        args, output, report, tooling_pin, rule = self.redirects_cli_fixture()
        before = git(self.repo, 'status', '--porcelain=v1')
        with patch.object(builder, 'REPO', self.repo):
            result = builder.main(args)
        evidence = json.loads(report.read_text())
        self.assertEqual(result, 0, evidence)
        self.assertIn(rule, (output/'site/.htaccess').read_bytes())
        self.assertEqual(json.loads((output/'artifact.json').read_text())['tooling_commit'], tooling_pin)
        self.assertEqual(git(self.repo, 'status', '--porcelain=v1'), before)

    def test_dirty_redirects_refuse_provenance_and_preserve_prior_artifact(self):
        args, output, report, tooling_pin, rule = self.redirects_cli_fixture()
        dirty_rule = rule + b'RewriteRule ^dirty/$ uncommitted/ [R=301,L]\n'
        (self.repo/'redirects.htaccess').write_bytes(dirty_rule)
        with patch.object(builder, 'REPO', self.repo):
            result = builder.main(args)
        evidence = json.loads(report.read_text())
        self.assertEqual(result, 1, evidence)
        self.assertEqual(evidence['status'], 'fail')
        self.assertIn('Commit tooling inputs before building: redirects.htaccess',
                      evidence['issues'][0]['evidence'])
        self.assertNotIn('tooling_commit', evidence['inputs'])
        self.assertNotIn('publication_committed', evidence['inputs'])
        self.assertEqual(list(output.iterdir()), [output/'prior'])
        self.assertEqual((output/'prior').read_bytes(), b'prior complete artifact')
        self.assertEqual((self.repo/'redirects.htaccess').read_bytes(), dirty_rule)
        self.assertEqual(git(self.repo, 'rev-parse', 'HEAD'), tooling_pin)

    def test_cli_missing_acceptance_catalog_reports_incomplete_and_keeps_output(self):
        output = self.root/'prior-cli'
        output.mkdir()
        (output/'prior').write_bytes(b'prior complete artifact')
        report = self.root/'cli-report.json'
        result = subprocess.run([sys.executable, str(ROOT/'scripts/build-versions.py'), '--manifest', str(self.manifest_path), '--base-url', self.manifest['production_base_url'], '--output-dir', str(output), '--report', str(report), '--release', 'root', '--acceptance-catalog', str(self.root/'not-ready.json')], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(report.read_text())['status'], 'incomplete')
        self.assertEqual((output/'prior').read_bytes(), b'prior complete artifact')

    def test_cli_report_cannot_replace_manifest(self):
        original = self.manifest_path.read_bytes()
        result = subprocess.run([sys.executable, str(ROOT/'scripts/build-versions.py'), '--manifest', str(self.manifest_path), '--base-url', self.manifest['production_base_url'], '--output-dir', str(self.root/'output'), '--report', str(self.manifest_path), '--release', 'root'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.manifest_path.read_bytes(), original)



    def test_work_storage_cannot_be_inside_prior_artifact(self):
        output = self.root/'prior-artifact'
        output.mkdir()
        (output/'prior').write_bytes(b'untouched')
        with self.assertRaisesRegex(ValueError, 'work|storage'):
            builder.build_and_publish(self.manifest_path, output, output/'work', self.manifest['production_base_url'], lambda *args: self.fail('must reject before building'), {}, jobs=1)
        self.assertEqual(list(output.iterdir()), [output/'prior'])

    def test_cli_report_hardlink_cannot_replace_manifest_bytes(self):
        alias = self.root/'manifest-alias'
        os.link(self.manifest_path, alias)
        original = self.manifest_path.read_bytes()
        result = subprocess.run([sys.executable, str(ROOT/'scripts/build-versions.py'), '--manifest', str(self.manifest_path), '--base-url', self.manifest['production_base_url'], '--output-dir', str(self.root/'output'), '--report', str(alias), '--release', 'root', '--acceptance-catalog', str(self.root/'missing.json')], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.manifest_path.read_bytes(), original)



    def main_args(self, output, report, catalog=None):
        return ['--manifest', str(self.manifest_path), '--base-url', self.manifest['production_base_url'], '--output-dir', str(output), '--report', str(report), '--release', 'root', '--acceptance-catalog', str(catalog or self.root/'missing-catalog.json')]

    def test_report_rejects_maps_baselines_exceptions_and_tooling_before_error_write(self):
        paths = ['migration/page-map.json', 'migration/releases/baselines/source/baseline.json',
                 'layouts/index.html', 'assets/scripts/main.js', 'static/logo.svg',
                 'data/versions.yaml', 'config.yaml', 'migration/schemas/artifact.schema.json']
        for number, relative in enumerate(paths):
            with self.subTest(path=relative):
                source = self.repo/relative
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_bytes(b'preserve input bytes')
                with patch.object(builder, 'REPO', self.repo), redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        builder.main(self.main_args(self.root/'artifact', source))
                self.assertEqual(source.read_bytes(), b'preserve input bytes')
        catalog = self.root/'acceptance.json'
        refs = []
        for name in ('page_map', 'baseline', 'exceptions'):
            source = self.repo/'accepted-inputs'/name
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_bytes(b'accepted captured bytes')
            refs.append((name, source))
        dump(catalog, {'schema_version':1, 'builds':[dict(id='root', **{name:path.relative_to(self.repo).as_posix() for name,path in refs})]})
        for name, source in refs:
            with self.subTest(catalog_input=name), patch.object(builder, 'REPO', self.repo), redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    builder.main(self.main_args(self.root/'artifact', source, catalog))
                self.assertEqual(source.read_bytes(), b'accepted captured bytes')

    def test_artifact_destination_cannot_replace_tooling_or_acceptance_directories(self):
        for relative in ('layouts', 'assets', 'static', 'data', 'migration/releases/baselines'):
            source = self.repo/relative
            source.mkdir(parents=True, exist_ok=True)
            (source/'input').write_bytes(b'keep source directory')
            with self.subTest(path=relative), patch.object(builder, 'REPO', self.repo), redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    builder.main(self.main_args(source, self.root/'report.json'))
                self.assertEqual((source/'input').read_bytes(), b'keep source directory')

    def test_report_hardlinks_to_source_or_prior_artifact_are_rejected(self):
        output = self.root/'artifact'
        (output/'site').mkdir(parents=True)
        source = self.repo/'layouts/index.html'
        source.parent.mkdir(parents=True)
        source.write_bytes(b'original template')
        prior = output/'site/index.html'
        prior.write_bytes(b'prior artifact bytes')
        for number, protected in enumerate((source, prior)):
            alias = self.root/('report-alias-'+str(number))
            os.link(protected, alias)
            with self.subTest(input=str(protected)), patch.object(builder, 'REPO', self.repo), redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    builder.main(self.main_args(output, alias))
                self.assertEqual(protected.read_bytes(), b'original template' if number==0 else b'prior artifact bytes')



    def test_post_publication_old_tree_cleanup_failure_is_success_with_external_evidence(self):
        from scripts.migration import assemble_artifact as assembly
        for mode in ('exchange', 'fallback'):
            with self.subTest(mode=mode):
                target, stage = self.root/('target-'+mode), self.root/('stage-'+mode)
                target.mkdir(); stage.mkdir()
                (target/'prior').write_bytes(b'prior artifact')
                (stage/'new').write_bytes(b'new artifact')
                with ExitStack() as stack:
                    if mode=='fallback':
                        stack.enter_context(patch.object(assembly, '_exchange', return_value=False))
                    stack.enter_context(patch.object(assembly.shutil, 'rmtree', side_effect=OSError('forced old-tree cleanup error')))
                    publication = publish_artifact(stage, target)
                self.assertEqual((target/'new').read_bytes(), b'new artifact')
                self.assertFalse((target/'prior').exists())
                self.assertTrue(publication['cleanup_warnings'])
                retained = Path(publication['cleanup_warnings'][0]['retained_path'])
                self.assertFalse(retained.is_relative_to(target))
                self.assertEqual((retained/'prior').read_bytes(), b'prior artifact')

    def test_workspace_cleanup_cannot_turn_committed_artifact_into_failure(self):
        target = self.root/'workspace-artifact'
        def make(record, destination):
            destination.mkdir()
            return self.outputs(record, destination)
        original = shutil.rmtree
        def cleanup(path, *args, **kwargs):
            if Path(path).name.startswith('release-build-'):
                raise OSError('forced workspace cleanup error')
            return original(path, *args, **kwargs)
        provenance = dict(tooling_commit=self.current, theme_commit='91b3863e863981905ba45566832022270a56085f', tools={'hugo':'0.124.1','hugo_extended':True,'task':'3.44.1'})
        with patch.object(builder.shutil, 'rmtree', side_effect=cleanup):
            metadata, publication = builder.build_and_publish(self.manifest_path, target, self.root/'work', self.manifest['production_base_url'], make, provenance, release='root')
        self.assertEqual(metadata['kind'], 'preview')
        self.assertTrue((target/'site/index.html').is_file())
        self.assertTrue(any('release-build-' in warning['retained_path'] for warning in publication['cleanup_warnings']))
        self.assertEqual(set(p.name for p in target.iterdir()), {'site','validation','artifact.json','checksums.sha256'})

    def fixture_main_with_post_commit_error(self, report_error=False, tooling_error=False, stderr_error=False):
        output, report = self.root/'committed-cli', self.root/'committed-report.json'
        output.mkdir()
        (output/'prior').write_bytes(b'prior artifact')
        def make(record, destination):
            destination.mkdir()
            return self.outputs(record, destination)
        real_git, real_cleanup = builder._git, shutil.rmtree
        def read_git(repo, *args):
            if args==('rev-parse', self.current+':themes'):
                return b'91b3863e863981905ba45566832022270a56085f\n'
            if args and args[0]=='status':
                return b''
            return real_git(repo, *args)
        def cleanup(path, *args, **kwargs):
            if tooling_error and Path(path).name.startswith('release-tooling-'):
                raise OSError('forced tooling cleanup error')
            return real_cleanup(path, *args, **kwargs)
        stderr = io.StringIO()
        with ExitStack() as stack:
            stack.enter_context(patch.object(builder, 'REPO', self.repo))
            stack.enter_context(patch.object(builder, '_git', side_effect=read_git))
            stack.enter_context(patch.object(builder, 'load_acceptance_catalog', return_value={}))
            stack.enter_context(patch.object(builder, 'verify_tools', return_value={'hugo':'0.124.1','hugo_extended':True,'task':'3.44.1'}))
            stack.enter_context(patch.object(builder, 'export_tree', side_effect=lambda repo, pin, destination, *args: Path(destination).mkdir(parents=True)))
            stack.enter_context(patch.object(builder, 'ReleaseBuilder', return_value=make))
            stack.enter_context(patch.object(builder.shutil, 'rmtree', side_effect=cleanup))
            if report_error:
                stack.enter_context(patch.object(builder, 'write_json', side_effect=OSError('forced external report error')))
            if stderr_error:
                stack.enter_context(patch('builtins.print', side_effect=OSError('stderr unavailable')))
            stack.enter_context(redirect_stderr(stderr))
            result = builder.main(self.main_args(output, report)+['--work-dir', str(self.root/'cli-work')])
        self.assertEqual(result, 0)
        self.assertFalse((output/'prior').exists())
        self.assertTrue((output/'site/index.html').is_file())
        self.assertEqual(set(p.name for p in output.iterdir()), {'site','validation','artifact.json','checksums.sha256'})
        return output, report, stderr.getvalue()

    def test_tooling_cleanup_after_publication_is_reported_as_committed_success(self):
        output, report, stderr = self.fixture_main_with_post_commit_error(tooling_error=True)
        result = json.loads(report.read_text())
        self.assertEqual(result['status'], 'pass')
        self.assertTrue(result['inputs']['publication_committed'])
        self.assertTrue(any('release-tooling-' in issue['evidence']['retained_path'] for issue in result['issues']))

    def test_external_report_error_after_publication_returns_committed_success_on_stderr(self):
        output, report, stderr = self.fixture_main_with_post_commit_error(report_error=True)
        self.assertFalse(report.exists())
        result = json.loads(stderr)
        self.assertEqual(result['status'], 'pass')
        self.assertTrue(result['inputs']['publication_committed'])
        self.assertTrue(any(issue['id']=='external-report-write' for issue in result['issues']))



    def test_catalog_code_inputs_and_input_parent_directories_are_protected(self):
        baseline = self.repo/'accepted/baseline.json'
        code = self.repo/'captured-code/example.txt'
        code.parent.mkdir()
        code.write_bytes(b'canonical captured code')
        dump(baseline, {'pages':{'/':{'code_blocks':[{'text_path':'../captured-code/example.txt'}]}}})
        catalog = self.root/'catalog.json'
        dump(catalog, {'schema_version':1, 'builds':[{'id':'root', 'baseline':'accepted/baseline.json'}]})
        with patch.object(builder, 'REPO', self.repo), redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                builder.main(self.main_args(self.root/'artifact', code, catalog))
            with self.assertRaises(SystemExit):
                builder.main(self.main_args(self.repo/'accepted', self.root/'report.json', catalog))
        self.assertEqual(code.read_bytes(), b'canonical captured code')
        self.assertEqual(json.loads(baseline.read_text())['pages']['/']['code_blocks'][0]['text_path'], '../captured-code/example.txt')

    def test_external_report_error_before_publication_still_returns_failure(self):
        output = self.root/'unpublished'
        output.mkdir()
        (output/'prior').write_bytes(b'prior artifact')
        stderr = io.StringIO()
        with patch.object(builder, 'REPO', self.repo), patch.object(builder, 'write_json', side_effect=OSError('report unavailable before publication')), redirect_stderr(stderr):
            result = builder.main(self.main_args(output, self.root/'report.json'))
        self.assertEqual(result, 1)
        self.assertEqual(json.loads(stderr.getvalue())['status'], 'incomplete')
        self.assertEqual((output/'prior').read_bytes(), b'prior artifact')
        self.assertEqual(list(output.iterdir()), [output/'prior'])



    def test_unavailable_report_and_stderr_do_not_revoke_publication(self):
        output, report, stderr = self.fixture_main_with_post_commit_error(report_error=True, stderr_error=True)
        self.assertFalse(report.exists())
        self.assertEqual(stderr, '')
        self.assertTrue((output/'artifact.json').is_file())


if __name__ == '__main__':
    unittest.main()
