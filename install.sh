#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )";

declare -a py_dependencies=(
    "${DIR}/3rdparty/markdown"
    "${DIR}/3rdparty/pymdown-extensions"
    "${DIR}/3rdparty/mkdocs"
    "${DIR}/3rdparty/GitPython"
    "${DIR}/3rdparty/mkdocs-versioned"
    "${DIR}/plugins/markdown-tabs"
)

# Install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
rm -f get-pip.py

# Install dependencies
for i in "${py_dependencies[@]}"
do
   cd "$i" && python setup.py develop;
done

