#!/bin/bash

set -e

cat <<EOF

-v `pwd`/src:/src
-v `pwd`/build_deps:/src/build_deps
-v `pwd`/build:/src/build
-v `pwd`/platform_linux.patch:/src/platform_linux.patch
-v `pwd`/prefix:/opt/prefix

-e ABI=$ABI

--env-file env.list

-w /src

EOF
