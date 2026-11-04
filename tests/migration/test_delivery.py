"""Exercise literal delivery scripts; remote calls use disposable local stubs."""
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]
VERIFY = ROOT / 'scripts/deploy/verify-artifact.sh'
DEPLOY = ROOT / 'scripts/deploy/deploy-artifact.sh'


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=os.environ.get("CS_DELIVERY_TEST_TMPDIR"))
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.tree = self.root / 'artifact'
        self.tree.mkdir()
        self.manifest = self.root / 'manifest.yaml'
        records = [('root', '', '1' * 40), ('8.15.1', '8.15.1/', '2' * 40)]
        data = {'schema_version': 1, 'production_base_url': 'https://www.virtuozzo.com/cloudscripting-docs/',
                'root': {'source_commit': '1' * 40, 'source_format': 'hugo', 'output_prefix': ''},
                'releases': [{'id': '8.15.1', 'source_commit': '2' * 40, 'source_format': 'hugo',
                              'publication': 'retained', 'output_prefix': '8.15.1/'}]}
        self.manifest.write_text(yaml.safe_dump(data))
        self.metadata = {'schema_version': 1, 'kind': 'production', 'base_url': data['production_base_url'],
                         'manifest_sha256': self.hash(self.manifest), 'content_commit': '1' * 40,
                         'tooling_commit': '3' * 40, 'theme_commit': '91b3863e863981905ba45566832022270a56085f',
                         'tools': {'hugo': '0.124.1', 'hugo_extended': True, 'task': '3.44.1'},
                         'prefixes': ['', '8.15.1/'], 'builds': []}
        for name, prefix, commit in records:
            for path in ('index.html', 'index.json', 'sitemap.xml', 'robots.txt', 'search/index.html', 'search.html'):
                p = self.tree / 'site' / prefix / path
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(name + '\n')
            report = {'schema_version': 1, 'status': 'pass', 'scope': 'offline', 'issues': [],
                      'checks': {key: {'status': 'pass' if key == 'offline' else 'not_run'}
                                 for key in ('offline', 'browser', 'http', 'hosting')},
                      'inputs': {'source_commit': commit, 'base_url': data['production_base_url'] + prefix,
                                 'site_dir': 'site/' + prefix, 'archived': name != 'root',
                                 'baseline_sha256': 'a' * 64, 'page_map_sha256': 'b' * 64,
                                 'publication_scope': 'complete'}}
            site = self.tree / 'site' / prefix
            files = sorted((p for p in site.rglob('*') if p.is_file() and
                            (prefix or not p.relative_to(site).as_posix().startswith('8.15.1/'))),
                           key=lambda p: p.relative_to(site).as_posix())
            report['inputs']['site_sha256'] = hashlib.sha256(''.join(
                self.hash(p) + '  ' + p.relative_to(site).as_posix() + '\n' for p in files).encode()).hexdigest()
            rp = self.tree / f'validation/{name}.json'
            rp.parent.mkdir(exist_ok=True)
            rp.write_text(json.dumps(report))
            self.metadata['builds'].append({'id': name, 'output_prefix': prefix, 'source_commit': commit,
                                           'source_format': 'hugo', 'validation_source_commit': commit,
                                           'site_report': f'validation/{name}.json'})
        self.archive = self.root / 'release.tar.gz'
        self.report = self.root / 'verify.json'
        self.seal()
        self.env = dict(os.environ, PYTHON=sys.executable)
        self.calls = self.root / 'calls'
        bindir = self.root / 'bin'
        bindir.mkdir()
        for command in ('scp', 'ssh'):
            p = bindir / command
            p.write_text('#!/bin/sh\nprintf "%s\\n" "' + command + '" >> "$DELIVERY_CALLS"\nexit 91\n')
            p.chmod(0o755)
        self.env.update(PATH=str(bindir) + os.pathsep + self.env['PATH'], DELIVERY_CALLS=str(self.calls))

    @staticmethod
    def hash(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def seal(self):
        (self.tree / 'artifact.json').write_text(json.dumps(self.metadata))
        paths = sorted(p for p in self.tree.rglob('*') if p.is_file() and p.name != 'checksums.sha256')
        (self.tree / 'checksums.sha256').write_text(''.join(
            self.hash(p) + '  ' + p.relative_to(self.tree).as_posix() + '\n' for p in paths))
        with tarfile.open(self.archive, 'w:gz') as archive:
            for p in sorted(self.tree.rglob('*')):
                if p.is_file():
                    archive.add(p, arcname=p.relative_to(self.tree).as_posix(), recursive=False)

    def verify(self, digest=None):
        return subprocess.run(['bash', str(VERIFY), str(self.archive), digest or self.hash(self.archive),
                               str(self.manifest), str(self.report)], cwd=ROOT, env=self.env,
                              text=True, capture_output=True)

    def deploy(self, destination='staging', config=None, digest=None):
        deploy_script = getattr(self, 'tooling_root', ROOT) / 'scripts/deploy/deploy-artifact.sh'
        return subprocess.run(['bash', str(deploy_script), destination, str(self.archive), digest or self.hash(self.archive),
                               str(self.manifest), str(self.report), str(config or self.root / 'missing-host.json')],
                              cwd=ROOT, env=self.env, text=True, capture_output=True)

    def test_complete_archive_verifies_without_hosting_claim(self):
        result = self.verify()
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(self.report.read_text())
        self.assertEqual(report['status'], 'pass')
        self.assertEqual(report['inputs']['archive_sha256'], self.hash(self.archive))
        self.assertEqual(report['checks']['hosting']['status'], 'not_run')

    def test_bad_digest_is_rejected_before_archive_is_opened(self):
        self.archive.write_bytes(b'not a tar archive')
        result = self.verify('0' * 64)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('archive-digest', self.report.read_text())
        self.assertFalse(self.calls.exists())

    def test_default_interpreter_ignores_unprepared_ambient_python(self):
        self.env.pop('PYTHON')
        self.env.pop('VIRTUAL_ENV', None)
        self.env.pop('UV_PROJECT_ENVIRONMENT', None)
        for name in ('python', 'python3'):
            ambient = self.root / 'bin' / name
            ambient.write_text('#!/bin/sh\necho "unprepared ambient Python" >&2\nexit 97\n')
            ambient.chmod(0o755)
        result = self.verify()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(self.report.read_text())['status'], 'pass')
        self.assertFalse(self.calls.exists())

    def test_preview_and_incomplete_archives_are_rejected_before_transfer(self):
        self.metadata['kind'] = 'preview'
        self.seal()
        result = self.deploy()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('preview-artifact', self.report.read_text())
        self.assertFalse(self.calls.exists())
        self.metadata['kind'] = 'production'
        shutil.rmtree(self.tree / 'site/8.15.1')
        self.seal()
        result = self.deploy()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('missing-release-output', self.report.read_text())
        self.assertFalse(self.calls.exists())

    def test_unknown_destination_and_unconfirmed_host_stop_before_transfer(self):
        result = self.deploy('typo')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('destination', result.stderr)
        self.assertFalse(self.calls.exists())
        config = self.root / 'host.json'
        config.write_text('{"schema_version":1,"destinations":{"staging":{"status":"unverified"}}}')
        result = self.deploy(config=config)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('confirmed', result.stderr)
        self.assertFalse(self.calls.exists())

    def confirmed_config(self, strategy='existing-symlink'):
        host = self.root / 'host'
        host.mkdir(exist_ok=True)
        for name in ('uploads', 'releases', 'backups', 'config'):
            (host / name).mkdir(exist_ok=True)
        (host / 'config/vhost.conf').write_text('verified fixture config')
        old = host / 'old'
        old.mkdir(exist_ok=True)
        (old / 'index.html').write_text('old served tree')
        public = host / 'public'
        if strategy == 'existing-symlink' and not public.is_symlink():
            public.symlink_to(old, target_is_directory=True)
        self.tooling_root = self.root / 'tooling'
        shutil.copytree(ROOT / 'scripts', self.tooling_root / 'scripts', ignore=shutil.ignore_patterns('__pycache__'))
        (self.tooling_root / 'migration').mkdir()
        contract = self.tooling_root / 'migration/hosting-contract.yaml'
        contract.write_text(yaml.safe_dump({'schema_version': 1, 'host_acceptance': 'confirmed',
            'capabilities': {'status': 'observed', 'accepted_strategy': strategy}}))
        self.target = {'status': 'confirmed', 'evidence': 'disposable fixture, not hosting acceptance',
            'host': 'fixture.invalid', 'user': 'operator', 'port': 22, 'strategy': strategy,
            'public_path': str(public), 'expected_current_target': str(old) if strategy == 'existing-symlink' else None,
            'upload_root': str(host / 'uploads'), 'release_root': str(host / 'releases'),
            'backup_root': str(host / 'backups'), 'config_snapshot_root': str(host / 'config'),
            'managed_files': [], 'retired_files': [],
            'capabilities': {key: True for key in ('case_sensitive', 'same_filesystem', 'symlink_serving',
                'metadata_backup', 'writers_quiesced', 'staging_isolated')},
            'staging_acceptance': {'status': 'pass', 'archive_sha256': self.hash(self.archive),
                                   'reference': 'fixture-only-staging-record'}}
        config = self.root / 'host.json'
        self.config_data = {'schema_version': 1, 'hosting_contract': 'migration/hosting-contract.yaml',
            'hosting_contract_sha256': self.hash(contract), 'destinations': {'staging': self.target,
                                                                          'production': self.target}}
        config.write_text(json.dumps(self.config_data))
        return config

    def test_private_record_cannot_substitute_the_canonical_hosting_contract(self):
        config = self.confirmed_config()
        self.config_data['hosting_contract'] = str(self.tooling_root / 'migration/hosting-contract.yaml')
        config.write_text(json.dumps(self.config_data))
        result = self.deploy(config=config)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('canonical', result.stderr)
        self.assertFalse(self.calls.exists())

    def test_contract_capabilities_and_production_digest_gate_before_network(self):
        config = self.confirmed_config()
        self.target['capabilities']['metadata_backup'] = False
        config.write_text(json.dumps(self.config_data))
        result = self.deploy(config=config)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('metadata_backup', result.stderr)
        self.assertFalse(self.calls.exists())
        self.target['capabilities']['metadata_backup'] = True
        self.target['staging_acceptance']['archive_sha256'] = '0' * 64
        config.write_text(json.dumps(self.config_data))
        result = self.deploy('production', config=config)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('staging', result.stderr)
        self.assertFalse(self.calls.exists())

    def test_failed_remote_preflight_stops_before_scp(self):
        config = self.confirmed_config()
        result = self.deploy(config=config)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.calls.read_text().splitlines(), ['ssh'])
        self.assertEqual((self.root / 'host/public/index.html').read_text(), 'old served tree')

    def local_transport(self):
        # Only transport and GNU metadata tools are doubled. The delivered Python
        # transaction runs unchanged against real disposable trees. These regular-
        # file doubles cannot establish ACL/xattr or host acceptance.
        probe = self.root / 'CaseProbe'
        probe.write_text('probe')
        insensitive = probe.with_name('caseprobe').exists()
        probe.unlink()
        if insensitive:
            self.skipTest('remote transaction requires case-sensitive CS_DELIVERY_TEST_TMPDIR')
        bindir = self.root / 'bin'
        scripts = {
            'ssh': "import shlex,subprocess,sys; args=shlex.split(sys.argv[-1]); raise SystemExit(subprocess.run([sys.executable]+args[1:],input=sys.stdin.read(),text=True).returncode)",
            'scp': "import shutil,sys; shutil.copyfile(sys.argv[-2],sys.argv[-1].split(':',1)[1])",
            'tar': """import pathlib,sys,tarfile
if '--version' in sys.argv:
 print('tar (GNU tar) fixture'); raise SystemExit(0)
args=sys.argv[1:]; root=pathlib.Path(args[args.index('-C')+1]); path=pathlib.Path(args[args.index('-f')+1] if '-f' in args else args[args.index('-cpf')+1])
if '--compare' in args:
 with tarfile.open(path) as archive:
  for item in archive.getmembers():
   if item.isfile() and archive.extractfile(item).read() != (root/item.name).read_bytes(): raise SystemExit(1)
else:
 with tarfile.open(path,'w') as archive: archive.add(root,arcname='.')
""",
            'cp': """import pathlib,shutil,sys
if '--version' in sys.argv:
 print('cp (GNU coreutils) fixture'); raise SystemExit(0)
relative=pathlib.Path(sys.argv[-2]); target=pathlib.Path(sys.argv[-1])/relative
target.parent.mkdir(parents=True,exist_ok=True)
shutil.copy2(relative,target)
"""}
        if sys.platform.startswith('linux'):
            # CI exercises real GNU backups/copies on disposable regular files.
            scripts.pop('tar')
            scripts.pop('cp')
        for name, body in scripts.items():
            p = bindir / name
            p.write_text('#!' + sys.executable + '\nimport os\nwith open(os.environ["DELIVERY_CALLS"],"a") as log: log.write("' + name + '\\n")\n' + body + '\n')
            p.chmod(0o755)

    def test_existing_symlink_transaction_keeps_backup_and_full_release(self):
        config = self.confirmed_config()
        self.local_transport()
        result = self.deploy(config=config)
        self.assertEqual(result.returncode, 0, result.stderr)
        public = self.root / 'host/public'
        self.assertEqual((public / 'index.html').read_text(), 'root\n')
        self.assertEqual((public / '8.15.1/index.html').read_text(), '8.15.1\n')
        self.assertEqual((self.root / 'host/old/index.html').read_text(), 'old served tree')
        backups = list((self.root / 'host/backups').glob('*/served.tar'))
        self.assertEqual(len(backups), 1)
        with tarfile.open(backups[0]) as archive:
            self.assertEqual(archive.extractfile('./index.html').read(), b'old served tree')
        self.assertFalse((public / 'artifact.json').exists())
        calls = self.calls.read_text().splitlines()
        self.assertLess(calls.index('scp'), len(calls) - 1)
        self.assertEqual([c for c in calls if c in ('ssh', 'scp')], ['ssh', 'scp', 'ssh'])

    def test_initial_install_requires_absent_public_path(self):
        config = self.confirmed_config('initial-symlink')
        self.local_transport()
        public = self.root / 'host/public'
        public.mkdir()
        result = self.deploy(config=config)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('scp', self.calls.read_text().splitlines())
        public.rmdir()
        result = self.deploy(config=config)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(public.is_symlink())
        self.assertEqual((public / '8.15.1/index.html').read_text(), '8.15.1\n')

    def test_managed_file_accounting_and_collision_are_fail_closed(self):
        config = self.confirmed_config()
        self.local_transport()
        managed = self.root / 'host/old/issue_report.php'
        managed.write_text('server-owned legacy bytes')
        result = self.deploy(config=config)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('scp', self.calls.read_text().splitlines())
        self.target['managed_files'] = [{'path': 'issue_report.php', 'sha256': self.hash(managed)}]
        config.write_text(json.dumps(self.config_data))
        result = self.deploy(config=config)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.root / 'host/public/issue_report.php').read_bytes(), managed.read_bytes())

    def test_failed_backup_does_not_switch_public_pointer(self):
        config = self.confirmed_config()
        self.local_transport()
        tar = self.root / 'bin/tar'
        tar.write_text('#!/bin/sh\nif [ "$1" = --version ]; then echo "GNU tar fixture"; exit 0; fi\nexit 93\n')
        tar.chmod(0o755)
        result = self.deploy(config=config)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.root / 'host/public/index.html').read_text(), 'old served tree')

    def test_post_switch_receipt_failure_restores_previous_pointer(self):
        config = self.confirmed_config()
        self.local_transport()
        ssh = self.root / 'bin/ssh'
        failure = """import pathlib
original_write_text = pathlib.Path.write_text
def fail_receipt(path, *args, **kwargs):
 if path.name == 'deployment.json' and path.exists():
  raise OSError('fixture receipt storage failure after switch')
 return original_write_text(path, *args, **kwargs)
pathlib.Path.write_text = fail_receipt
"""
        body = ('import shlex,subprocess,sys\nsource=sys.stdin.read()\n'
                'args=shlex.split(sys.argv[-1])\n'
                'raise SystemExit(subprocess.run([sys.executable]+args[1:],input=' + repr(failure) + '+source,text=True).returncode)\n')
        ssh.write_text('#!' + sys.executable + '\n' + body)
        ssh.chmod(0o755)
        result = self.deploy(config=config)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('receipt storage failure after switch', result.stderr)
        self.assertEqual((self.root / 'host/public').resolve(), self.root / 'host/old')
        self.assertEqual((self.root / 'host/public/index.html').read_text(), 'old served tree')
        self.assertTrue(list((self.root / 'host/backups').glob('*/served.tar')))
        self.assertTrue(list((self.root / 'host/releases').glob('*/8.15.1/index.html')))

    def test_remote_digest_mismatch_stops_before_extraction_or_backup(self):
        config = self.confirmed_config()
        self.local_transport()
        scp = self.root / 'bin/scp'
        scp.write_text('#!' + sys.executable + '\nimport pathlib,sys\npathlib.Path(sys.argv[-1].split(":",1)[1]).write_bytes(b"tampered")\n')
        scp.chmod(0o755)
        result = self.deploy(config=config)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('digest mismatch before extraction', result.stderr)
        self.assertFalse(list((self.root / 'host/uploads').glob('*/unpacked')))
        self.assertFalse(list((self.root / 'host/backups').iterdir()))
        self.assertEqual((self.root / 'host/public/index.html').read_text(), 'old served tree')

    def test_managed_file_collision_stops_before_transfer(self):
        config = self.confirmed_config()
        self.local_transport()
        self.target['managed_files'] = [{'path': 'index.html', 'sha256': self.hash(self.root / 'host/old/index.html')}]
        config.write_text(json.dumps(self.config_data))
        result = self.deploy(config=config)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('collides', result.stderr)
        self.assertNotIn('scp', self.calls.read_text().splitlines())

    def test_package_preserves_exact_archive_identity(self):
        self.archive.unlink()
        result = subprocess.run([sys.executable, '-m', 'scripts.deploy.artifact', 'package',
            str(self.tree), str(self.manifest), str(self.archive), str(self.report)],
            cwd=ROOT, env=self.env, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.verify().returncode, 0)
        self.assertEqual(self.archive.with_suffix(self.archive.suffix + '.sha256').read_text().split()[0], self.hash(self.archive))

    def test_case_only_directories_never_merge_during_extraction(self):
        from scripts.deploy.remote import unpack
        with tarfile.open(self.archive, 'w:gz') as target:
            for name, data in [('site/Case/a', b'A'), ('site/case/b', b'B')]:
                member = tarfile.TarInfo(name)
                member.size = len(data)
                target.addfile(member, io.BytesIO(data))
        destination = self.root / 'extraction'
        destination.mkdir()
        probe = destination / 'Probe'
        probe.touch()
        insensitive = (destination / 'probe').exists()
        probe.unlink()
        if insensitive:
            with self.assertRaisesRegex(ValueError, 'case-sensitive'):
                unpack(self.archive, destination)
            self.assertEqual(list(destination.iterdir()), [])
        else:
            unpack(self.archive, destination)
            self.assertEqual((destination / 'site/Case/a').read_bytes(), b'A')
            self.assertEqual((destination / 'site/case/b').read_bytes(), b'B')

    def test_archive_tooling_commit_must_match_trusted_build_run(self):
        result = subprocess.run(['bash', str(VERIFY), str(self.archive), self.hash(self.archive),
            str(self.manifest), str(self.report), '4' * 40], cwd=ROOT, env=self.env,
            text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('workflow-provenance', self.report.read_text())
        self.assertFalse(self.calls.exists())

    def test_verification_report_cannot_overwrite_archive(self):
        before = self.archive.read_bytes()
        self.report = self.archive
        result = self.verify()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.archive.read_bytes(), before)

    def test_workflow_source_rejects_untrusted_or_mismatched_artifact(self):
        from scripts.deploy.workflow_source import validate_records
        run = {'id': 42, 'conclusion': 'success', 'event': 'workflow_dispatch',
               'path': '.github/workflows/build-release.yml', 'workflow_id': 12, 'head_sha': '3' * 40,
               'head_repository': {'full_name': 'example/docs'}}
        artifact = {'id': 99, 'name': 'cloudscripting-docs-release', 'expired': False, 'workflow_run': {'id': 42, 'head_sha': '3' * 40}}
        workflow = {'id': 12, 'path': '.github/workflows/build-release.yml'}
        validate_records(run, artifact, 'example/docs', 42, 99, workflow)
        for key, value in [('event', 'pull_request'), ('conclusion', 'failure'),
                           ('path', '.github/workflows/main.yml'), ('id', 41), ('workflow_id', 13), ('head_sha', 'HEAD')]:
            changed = dict(run, **{key: value})
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_records(changed, artifact, 'example/docs', 42, 99, workflow)
        with self.assertRaises(ValueError):
            validate_records(run, dict(artifact, workflow_run={'id': 43, 'head_sha': '3' * 40}), 'example/docs', 42, 99, workflow)
        with self.assertRaises(ValueError):
            validate_records(run, dict(artifact, expired=True), 'example/docs', 42, 99, workflow)
        with self.assertRaises(ValueError):
            validate_records(run, dict(artifact, workflow_run={'id': 42, 'head_sha': '4' * 40}), 'example/docs', 42, 99, workflow)

    def test_traversal_links_duplicates_and_unexpected_members_are_rejected(self):
        for name, kind in [('../escape', 'file'), ('site/link', 'symlink'),
                           ('artifact.json', 'file'), ('extra-secret', 'file')]:
            with self.subTest(name=name, kind=kind):
                self.seal()
                with tarfile.open(self.archive, 'r:gz') as source:
                    members = [(member, source.extractfile(member).read()) for member in source.getmembers()]
                with tarfile.open(self.archive, 'w:gz') as target:
                    for member, payload in members:
                        target.addfile(member, io.BytesIO(payload))
                    member = tarfile.TarInfo(name)
                    if kind == 'symlink':
                        member.type = tarfile.SYMTYPE
                        member.linkname = '/tmp'
                        target.addfile(member)
                    else:
                        member.size = 1
                        target.addfile(member, io.BytesIO(b'x'))
                result = self.verify()
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn('archive-member', self.report.read_text())
                self.assertFalse((self.root / 'escape').exists())


if __name__ == '__main__':
    unittest.main()
