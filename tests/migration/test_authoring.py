"""Pinned-Hugo current previews mount working edits and exact frozen assets."""
import base64
import hashlib
import json
import os
from pathlib import Path
import shutil
import shlex
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

import yaml

ROOT = Path(__file__).resolve().parents[2]
HUGO = os.environ.get('HUGO_BIN', shutil.which('hugo') or 'hugo')


class AuthoringTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=os.environ.get('CS_DELIVERY_TEST_TMPDIR'))
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        probe = self.root / 'CaseProbe'
        probe.touch()
        insensitive = probe.with_name('caseprobe').exists()
        probe.unlink()
        if insensitive:
            self.skipTest('requires a case-sensitive CS_DELIVERY_TEST_TMPDIR')
        self.source = self.root / 'source'
        self.source.mkdir()
        for path in ('content/guide', 'content/draft', 'layouts/_default/_markup', 'static', 'docs', 'theme/readthedocs/img'):
            (self.source / path).mkdir(parents=True, exist_ok=True)
        self.resource = hashlib.sha256(b'theme/readthedocs/img/Icon.png').hexdigest()[:16] + '-Icon.png'
        self.original = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/l9sAAAAASUVORK5CYII=')
        (self.source / 'theme/readthedocs/img/Icon.png').write_bytes(self.original)
        (self.source / 'theme/readthedocs/img/Case.svg').write_text('<svg>upper</svg>')
        (self.source / 'theme/readthedocs/img/case.svg').write_text('<svg>lower</svg>')
        (self.source / 'content/_index.md').write_text('---\ntitle: Home\n---\nWorking home\n')
        self.guide = self.source / 'content/guide/index.md'
        self.guide.write_text('---\ntitle: Guide\n---\nWorking guide first\n\n![Bundle](' + self.resource + ')\n\n<img src="/img/Case.svg">\n')
        (self.source / 'content/draft/index.md').write_text('---\ntitle: Draft\ndraft: true\n---\nDraft authoring bytes\n')
        (self.source / 'docs/secret.md').write_text('Never newly publish legacy unapproved sources\n')
        (self.source / 'static/working.txt').write_text('static first')
        (self.source / 'config.yaml').write_text('baseURL: https://preview.test/docs/\nmarkup:\n  goldmark:\n    renderer:\n      unsafe: true\n')
        layout = '<html><head><title>{{ .Title }}</title></head><body>{{ .Content }}</body></html>'
        (self.source / 'layouts/index.html').write_text(layout)
        (self.source / 'layouts/_default/single.html').write_text(layout)
        (self.source / 'layouts/_default/_markup/render-image.html').write_text('{{ $r := .Page.Resources.GetMatch .Destination }}<img src="{{ $r.RelPermalink }}">')
        self.git('init', '-q')
        self.git('add', '.')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'immutable fixture source')
        revision = self.git('rev-parse', 'HEAD').strip()
        self.manifest = self.source / 'manifest.yaml'
        data = yaml.safe_load((ROOT / 'migration/release-sources.yaml').read_text())
        data['root'].update(source_commit=revision, source_format='hugo', decision_status='approved')
        self.manifest.write_text(yaml.safe_dump(data))
        (self.source / 'acceptance').mkdir()
        page_map = {'schema_version': 1, 'source_commit': revision, 'pages': [
            {'published': True, 'old_url': '/', 'target_path': 'content/_index.md'},
            {'published': True, 'old_url': '/guide/', 'target_path': 'content/guide/index.md'}]}
        baseline = {'schema_version': 1, 'inputs': {'source_commit': revision}, 'pages': {
            '/': {'images': []}, '/guide/': {'images': [{'resolved_url': '/img/Icon.png'}]}}}
        (self.source / 'acceptance/page-map.json').write_text(json.dumps(page_map))
        (self.source / 'acceptance/baseline.json').write_text(json.dumps(baseline))
        self.catalog = self.source / 'acceptance.json'
        self.catalog.write_text(json.dumps({'schema_version': 1, 'builds': [{'id': 'root',
            'source_commit': revision, 'validation_source_commit': revision,
            'page_map': 'acceptance/page-map.json', 'baseline': 'acceptance/baseline.json'}]}))
        self.work = self.root / 'build'
        # Deliberately dirty legacy checkout bytes must never enter the preview.
        (self.source / 'theme/readthedocs/img/Icon.png').write_bytes(b'protected dirty checkout fixture')

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.source), *args], text=True)

    def command(self, operation='build', work=None):
        return [sys.executable, '-m', 'scripts.migration.authoring', operation,
                '--source-root', str(self.source), '--work-dir', str(work or self.work),
                '--manifest', str(self.manifest), '--acceptance-catalog', str(self.catalog), '--hugo', HUGO]

    def build(self, work=None):
        return subprocess.run(self.command(work=work), cwd=ROOT, text=True, capture_output=True)

    def test_build_uses_working_content_exact_git_assets_and_excludes_drafts(self):
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        site = self.work / 'current-site'
        self.assertIn('Working guide first', (site / 'guide/index.html').read_text())
        self.assertEqual((site / 'img/Icon.png').read_bytes(), self.original)
        self.assertEqual((site / 'guide' / self.resource).read_bytes(), self.original)
        self.assertEqual((site / 'img/Case.svg').read_text(), '<svg>upper</svg>')
        self.assertEqual((site / 'img/case.svg').read_text(), '<svg>lower</svg>')
        self.assertFalse((site / 'draft/index.html').exists())
        self.assertFalse((site / 'secret/index.html').exists())
        self.assertFalse((site / 'artifact.json').exists())
        self.assertEqual(json.loads((self.work / 'current-preview.json').read_text())['kind'], 'preview')
        self.guide.write_text(self.guide.read_text().replace('Working guide first', 'Uncommitted guide edit'))
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Uncommitted guide edit', (site / 'guide/index.html').read_text())
        self.assertEqual((self.source / 'theme/readthedocs/img/Icon.png').read_bytes(), b'protected dirty checkout fixture')

    def test_build_accepts_official_hugo_extended_version(self):
        wrapper = self.root / 'official-hugo'
        version = 'hugo v0.124.1-db083b05f16c945fec04f745f0ca8640560cf1ec+extended linux/amd64 BuildDate=2024-03-20T11:40:10Z VendorInfo=gohugoio'
        wrapper.write_text('#!/bin/sh\nif [ "$1" = version ]; then\n'
                           "  printf '%s\\n' " + shlex.quote(version) + '\nelse\n'
                           '  exec ' + shlex.quote(HUGO) + ' "$@"\nfi\n')
        wrapper.chmod(0o755)
        command = self.command()
        command[-1] = str(wrapper)
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Working guide first', (self.work / 'current-site/guide/index.html').read_text())

    def test_build_rejects_wrong_hugo_versions_and_non_extended_builds(self):
        wrapper = self.root / 'unsupported-hugo'
        command = self.command()
        command[-1] = str(wrapper)
        versions = ('v0.124.1', 'v0.124.1-db083b05', 'v0.124.2+extended',
                    'v0.124.10+extended', 'v0.124.1-rc.1+extended', 'v0.124.1+extended-bogus')
        for version in versions:
            with self.subTest(version=version):
                wrapper.write_text("#!/bin/sh\nprintf '%s\\n' " + shlex.quote('hugo ' + version) + '\n')
                wrapper.chmod(0o755)
                result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Hugo Extended 0.124.1 is required', result.stderr)
                self.assertFalse((self.work / 'current-site').exists())

    def test_serve_watches_working_content_and_static_mounts(self):
        with socket.socket() as listener:
            listener.bind(('127.0.0.1', 0))
            port = listener.getsockname()[1]
        log = (self.root / 'server.log').open('w')
        self.addCleanup(log.close)
        process = subprocess.Popen(self.command('serve') + ['--port', str(port)], cwd=ROOT,
                                   stdout=log, stderr=subprocess.STDOUT)
        def stop():
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        self.addCleanup(stop)
        def body(path, expected):
            deadline = time.monotonic() + 25
            while time.monotonic() < deadline:
                if process.poll() is not None:
                    self.fail((self.root / 'server.log').read_text())
                try:
                    with urlopen(f'http://127.0.0.1:{port}/' + path, timeout=2) as response:
                        data = response.read().decode()
                        if expected in data:
                            return data
                except (URLError, OSError):
                    pass
                time.sleep(0.1)
            self.fail('server did not reflect edit: ' + path + '\n' + (self.root / 'server.log').read_text())
        body('guide/', 'Working guide first')
        body('draft/', 'Draft authoring bytes')
        self.guide.write_text(self.guide.read_text().replace('Working guide first', 'Live mounted content edit'))
        body('guide/', 'Live mounted content edit')
        (self.source / 'static/working.txt').write_text('Live mounted static edit')
        body('working.txt', 'Live mounted static edit')
        with self.assertRaises(HTTPError) as error:
            urlopen(f'http://127.0.0.1:{port}/secret/', timeout=2)
        self.assertEqual(error.exception.code, 404)

    def test_conflicting_authored_resource_fails_without_overwriting_source(self):
        resource = self.source / 'content/guide' / self.resource
        resource.write_bytes(b'conflicting user resource')
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('differs', result.stderr)
        self.assertEqual(resource.read_bytes(), b'conflicting user resource')
        self.assertFalse((self.work / 'current-site').exists())

    def test_existing_unowned_output_is_not_cleaned(self):
        output = self.work / 'current-site'
        output.mkdir(parents=True)
        (output / 'keep.txt').write_text('unrelated user output')
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('owned preview', result.stderr)
        self.assertEqual((output / 'keep.txt').read_text(), 'unrelated user output')

    def test_missing_root_acceptance_fails_clearly(self):
        self.catalog.write_text('{"schema_version":1,"builds":[]}')
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('root acceptance', result.stderr)
        self.assertFalse((self.work / 'current-site').exists())


if __name__ == '__main__':
    unittest.main()
