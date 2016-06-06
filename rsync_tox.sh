#!/bin/sh
set -e  # Exit on errors.

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 srcdir rundir"
    exit 1
fi

srcdir="$1"
rundir="$2"

rsync -av --progress "$srcdir" "$rundir" \
    --exclude ".git" \
    --exclude "*/_build" \
    --exclude "*.egg-info"

cd "$rundir"
tox
