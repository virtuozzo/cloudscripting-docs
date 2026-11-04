"""Verify/package complete artifacts and deliver the same archive to a confirmed host."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile

import yaml

from scripts.deploy.remote import digest, safe_path, unpack
from scripts.migration.check_artifact import check_artifact
from scripts.migration.check_site import issue, report_shell


def verify(archive, expected, manifest, report, tooling_commit=None):
    result = report_shell({'archive': str(archive), 'manifest': str(manifest)})
    try:
        if not re.fullmatch('[0-9a-f]{64}', expected) or digest(archive) != expected:
            issue(result, 'archive-digest', str(archive), 'Archive SHA-256 does not match accepted digest')
        else:
            with tempfile.TemporaryDirectory(prefix='cs-artifact-', dir=os.environ.get('CS_DELIVERY_TMPDIR')) as temp:
                unpack(archive, Path(temp))
                result = check_artifact(Path(temp), manifest)
                result['inputs'].update(archive=str(archive), archive_sha256=expected)
                if tooling_commit is not None:
                    metadata = json.loads((Path(temp) / 'artifact.json').read_text())
                    if not re.fullmatch('[0-9a-f]{40}', tooling_commit) or metadata.get('tooling_commit') != tooling_commit:
                        issue(result, 'workflow-provenance', 'artifact.json', 'Artifact tooling commit differs from trusted release run head SHA')
                    result['inputs']['trusted_workflow_head_sha'] = tooling_commit
                # Detect accidental archive replacement during local verification.
                if digest(archive) != expected:
                    issue(result, 'archive-digest', str(archive), 'Archive changed during verification')
    except (OSError, ValueError, KeyError, TypeError, AttributeError, tarfile.TarError, yaml.YAMLError) as error:
        issue(result, 'archive-member' if 'archive-member:' in str(error) else 'invalid-input', str(archive), str(error))
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, indent=2) + '\n')
    return result['status'] == 'pass'


def host_config(path, destination, expected):
    config = json.loads(path.read_text())
    target = config.get('destinations', {}).get(destination, {})
    if config.get('schema_version') != 1 or target.get('status') != 'confirmed':
        raise ValueError('destination host configuration must be confirmed by hosting owner')
    if config.get('hosting_contract', 'migration/hosting-contract.yaml') != 'migration/hosting-contract.yaml':
        raise ValueError('operational record must bind the canonical migration/hosting-contract.yaml')
    contract_path = Path(__file__).resolve().parents[2] / 'migration/hosting-contract.yaml'
    if digest(contract_path) != config.get('hosting_contract_sha256'):
        raise ValueError('hosting contract digest does not match the confirmed operational record')
    contract = yaml.safe_load(contract_path.read_text())
    strategy = contract.get('capabilities', {}).get('accepted_strategy')
    if isinstance(strategy, dict):
        strategy = strategy.get(destination)
    if (contract.get('host_acceptance') != 'confirmed'
            or contract.get('capabilities', {}).get('status') != 'observed'
            or strategy != target.get('strategy')):
        raise ValueError('hosting contract capabilities/strategy must be confirmed; current local preparation is insufficient')
    if not target.get('evidence'):
        raise ValueError('confirmed hosting evidence reference is required')
    if target.get('strategy') not in ('existing-symlink', 'initial-symlink'):
        raise ValueError('unsupported destination strategy; real-directory replacement needs host-specific provisioning')
    for key in ('case_sensitive', 'same_filesystem', 'symlink_serving', 'metadata_backup', 'writers_quiesced'):
        if target.get('capabilities', {}).get(key) is not True:
            raise ValueError('confirmed host capability required: ' + key)
    if destination == 'staging' and target.get('capabilities', {}).get('staging_isolated') is not True:
        raise ValueError('staging host isolation must be confirmed')
    if destination == 'production':
        acceptance = target.get('staging_acceptance', {})
        if acceptance.get('status') != 'pass' or acceptance.get('archive_sha256') != expected or not acceptance.get('reference'):
            raise ValueError('production requires staging acceptance of this exact archive digest')
    if not re.fullmatch('[A-Za-z0-9.-]+', target.get('host', '')) or not re.fullmatch('[A-Za-z0-9_-]+', target.get('user', '')):
        raise ValueError('invalid confirmed SSH endpoint')
    if type(target.get('port')) is not int or not 1 <= target['port'] <= 65535:
        raise ValueError('invalid confirmed SSH port')
    keys = ('public_path', 'release_root', 'upload_root', 'backup_root', 'config_snapshot_root')
    paths = []
    for key in keys:
        value = target.get(key, '')
        if not re.fullmatch('/[A-Za-z0-9_./-]+', value) or value == '/' or '..' in value.split('/'):
            raise ValueError('invalid confirmed absolute path: ' + key)
        paths.append(Path(value))
    for index, path in enumerate(paths):
        for other in paths[index + 1:]:
            if path == other or path in other.parents or other in path.parents:
                raise ValueError('confirmed operational paths must be disjoint')
    if target['strategy'] == 'existing-symlink':
        value = target.get('expected_current_target', '')
        if not re.fullmatch('/[A-Za-z0-9_./-]+', value) or '..' in value.split('/'):
            raise ValueError('existing symlink requires an exact confirmed current target')
    elif target.get('expected_current_target') is not None:
        raise ValueError('initial installation must confirm no current target')
    for key in ('managed_files', 'retired_files'):
        entries = target.get(key)
        if not isinstance(entries, list):
            raise ValueError('explicit confirmed inventory required: ' + key)
        seen = set()
        for entry in entries:
            name = entry.get('path')
            if not safe_path(name) or name in seen or not re.fullmatch('[0-9a-f]{64}', entry.get('sha256', '')):
                raise ValueError('invalid confirmed inventory: ' + key)
            seen.add(name)
    return target


def deliver(target, archive, expected):
    endpoint = target['user'] + '@' + target['host']
    remote_source = Path(__file__).with_name('remote.py').read_text()
    with tarfile.open(archive, 'r:gz') as source:
        target = dict(target, artifact_files=[m.name[5:] for m in source.getmembers()
                                            if m.isfile() and m.name.startswith('site/')],
                      archive_sha256=expected, archive_bytes=archive.stat().st_size)
    def remote(operation, session=None):
        payload = dict(target, operation=operation, session=session)
        command = 'python3 -'
        source = 'import json\nDELIVERY_CONFIG = json.loads(' + repr(json.dumps(payload, separators=(',', ':'))) + ')\n' + remote_source
        result = subprocess.run(['ssh', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=yes',
                                 '-p', str(target['port']), '--', endpoint, command],
                                input=source, text=True, capture_output=True)
        if result.returncode:
            raise ValueError('remote ' + operation + ' failed: ' + result.stderr.strip())
        return json.loads(result.stdout)
    preparation = remote('preflight')
    session = preparation['session']
    if (not isinstance(session, str) or not re.fullmatch('/[A-Za-z0-9_./-]+', session)
            or Path(session).parent != Path(target['upload_root']) or '..' in session.split('/')):
        raise ValueError('remote preflight returned an unsafe upload session')
    if digest(archive) != expected:
        raise ValueError('archive changed before transfer')
    subprocess.run(['scp', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=yes',
                    '-P', str(target['port']), '--', str(archive.resolve()), endpoint + ':' + session + '/artifact.tar.gz'], check=True)
    receipt = remote('deploy', session)
    print(json.dumps(receipt, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('verify', 'deploy'):
        command = sub.add_parser(name)
        if name == 'deploy':
            command.add_argument('destination', choices=('staging', 'production'))
        command.add_argument('archive', type=Path)
        command.add_argument('sha256')
        command.add_argument('manifest', type=Path)
        command.add_argument('report', type=Path)
        if name == 'deploy':
            command.add_argument('host_config', type=Path)
        command.add_argument('tooling_commit', nargs='?')
    package = sub.add_parser('package')
    package.add_argument('artifact_dir', type=Path)
    package.add_argument('manifest', type=Path)
    package.add_argument('archive', type=Path)
    package.add_argument('report', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'package':
            if args.report.resolve() in (args.manifest.resolve(), args.archive.resolve()):
                raise ValueError('package report must not overwrite manifest or archive')
            for output in (args.archive, args.report):
                if output.resolve().is_relative_to(args.artifact_dir.resolve()):
                    raise ValueError('package outputs must be outside the artifact')
            result = check_artifact(args.artifact_dir, args.manifest)
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(result, indent=2) + '\n')
            if result['status'] != 'pass':
                raise ValueError('Full artifact validation failed; no archive created')
            args.archive.parent.mkdir(parents=True, exist_ok=True)
            with tarfile.open(args.archive, 'x:gz') as archive:
                for path in sorted(args.artifact_dir.rglob('*')):
                    if path.is_file():
                        archive.add(path, arcname=path.relative_to(args.artifact_dir).as_posix(), recursive=False)
            expected = digest(args.archive)
            if not verify(args.archive, expected, args.manifest, args.report):
                raise ValueError('Packaged archive verification failed')
            args.archive.with_suffix(args.archive.suffix + '.sha256').write_text(expected + '  ' + args.archive.name + '\n')
            print(expected)
            return
        if args.report.resolve() in (args.archive.resolve(), args.manifest.resolve()):
            raise ValueError('verification report must not overwrite archive or manifest')
        if not verify(args.archive, args.sha256, args.manifest, args.report, args.tooling_commit):
            raise ValueError('Artifact verification failed; see ' + str(args.report))
        if args.command == 'deploy':
            target = host_config(args.host_config, args.destination, args.sha256)
            deliver(target, args.archive, args.sha256)
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
