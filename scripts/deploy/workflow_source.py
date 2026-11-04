"""Bind a downloaded artifact ID to an exact successful manual release run."""
import json
import os
import re
import subprocess
import sys


def validate_records(run, artifact, repository, run_id, artifact_id, workflow):
    if (run.get('id') != run_id or run.get('conclusion') != 'success'
            or run.get('event') != 'workflow_dispatch'
            or run.get('path') != '.github/workflows/build-release.yml'
            or workflow.get('path') != '.github/workflows/build-release.yml'
            or run.get('workflow_id') != workflow.get('id')
            or not isinstance(workflow.get('id'), int)
            or not re.fullmatch('[0-9a-f]{40}', run.get('head_sha', ''))
            or run.get('head_repository', {}).get('full_name') != repository):
        raise ValueError('Selected run is not a successful manual release build in this repository')
    if (artifact.get('id') != artifact_id or artifact.get('expired') is not False
            or artifact.get('name') != 'cloudscripting-docs-release'
            or artifact.get('workflow_run', {}).get('id') != run_id
            or artifact.get('workflow_run', {}).get('head_sha') != run.get('head_sha')):
        raise ValueError('Selected release artifact does not belong to that exact run or has expired')


def main():
    if (len(sys.argv) != 4 or not all(re.fullmatch('[1-9][0-9]{0,19}', value) for value in sys.argv[1:3])
            or not re.fullmatch('[0-9a-f]{64}', sys.argv[3])):
        raise ValueError('Require literal build run ID, artifact ID and accepted archive SHA-256')
    repository = os.environ['GITHUB_REPOSITORY']
    def get(path):
        return json.loads(subprocess.run(['gh', 'api', 'repos/' + repository + '/actions/' + path],
                                         capture_output=True, text=True, check=True).stdout)
    run_id, artifact_id = map(int, sys.argv[1:3])
    run = get('runs/' + str(run_id))
    validate_records(run, get('artifacts/' + str(artifact_id)), repository, run_id, artifact_id, get('workflows/build-release.yml'))
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a') as output:
            output.write('trusted_sha=' + run['head_sha'] + '\n')
    print('Exact successful release run and artifact identity verified')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
