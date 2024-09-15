#!/usr/bin/env sh

set -o errexit
set -o nounset

. /common_scripts/entrypoint.sh

readonly cmd="$*"

exec $cmd
