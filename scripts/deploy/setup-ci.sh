#!/usr/bin/env bash
# Linux runner setup; versions and release bytes are deliberately pinned.
set -euo pipefail
: "${RUNNER_TEMP:?GitHub runner temporary directory is required}"
: "${GITHUB_PATH:?GitHub path export file is required}"
test "$(uname -s)" = Linux
test "$(uname -m)" = x86_64
stage=$(mktemp -d "$RUNNER_TEMP/cs-tools.XXXXXXXX")
trap 'rm -rf -- "$stage"' EXIT
curl --fail --location --silent --show-error https://github.com/gohugoio/hugo/releases/download/v0.124.1/hugo_extended_0.124.1_linux-amd64.tar.gz -o "$stage/hugo.tar.gz"
curl --fail --location --silent --show-error https://github.com/go-task/task/releases/download/v3.44.1/task_linux_amd64.tar.gz -o "$stage/task.tar.gz"
printf '%s  %s\n' 55f5a5f6a4c923457b2ed4e2b00c251eabfe43d8d4afbe2ada92d9759c5e0410 "$stage/hugo.tar.gz" 62969d22bee5ea8950cc64a30cc7eb278f89ad67683132e728841457aae523c1 "$stage/task.tar.gz" | sha256sum --check -
mkdir -p "$RUNNER_TEMP/cs-bin"
tar -xzf "$stage/hugo.tar.gz" -C "$RUNNER_TEMP/cs-bin" hugo
tar -xzf "$stage/task.tar.gz" -C "$RUNNER_TEMP/cs-bin" task
"$RUNNER_TEMP/cs-bin/hugo" version
"$RUNNER_TEMP/cs-bin/task" --version
printf '%s\n' "$RUNNER_TEMP/cs-bin" >> "$GITHUB_PATH"
