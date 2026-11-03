#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 4 ] && [ "$#" -ne 5 ]; then
  echo 'usage: verify-artifact.sh ARCHIVE SHA256 MANIFEST REPORT [TRUSTED_TOOLING_COMMIT]' >&2
  exit 2
fi
repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
cd -- "$repo"
if [ -n "${PYTHON:-}" ]; then
  exec "$PYTHON" -m scripts.deploy.artifact verify "$@"
fi
exec uv run --locked python -m scripts.deploy.artifact verify "$@"
