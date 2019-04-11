#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )";
VERSION=$1

mkdocs_versioned --default-branch=$VERSION