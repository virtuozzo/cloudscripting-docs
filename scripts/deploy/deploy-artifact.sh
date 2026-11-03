#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 6 ] && [ "$#" -ne 7 ]; then
  echo 'usage: deploy-artifact.sh staging|production ARCHIVE SHA256 MANIFEST REPORT HOST_CONFIG [TRUSTED_TOOLING_COMMIT]' >&2
  exit 2
fi
repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
cd -- "$repo"
if [ -n "${PYTHON:-}" ]; then
  exec "$PYTHON" -m scripts.deploy.artifact deploy "$@"
fi
exec uv run --locked python -m scripts.deploy.artifact deploy "$@"
