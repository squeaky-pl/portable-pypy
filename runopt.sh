#!/bin/bash

set -e

cat <<EOF

-v `pwd`/src:/src
-v `pwd`/build_deps:/src/build_deps
-v `pwd`/prefix:/opt/prefix

-e ABI=$ABI

--env-file env.list

-w /src

EOF
