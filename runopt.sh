#!/bin/bash

set -e

cat <<EOF

-v `pwd`/src:/src
-v `pwd`/build_deps:/src/build_deps
-v `pwd`/build:/src/build
-v `pwd`/package:/src/package
-v `pwd`/make_portable:/src/make_portable
-v `pwd`/version.py:/src/version.py
-v `pwd`/platform_linux.patch:/src/platform_linux.patch
-v `pwd`/_tkinter_app.py.patch:/src/_tkinter_app.py.patch
-v `pwd`/prefix:/opt/prefix

-e ABI=$ABI

--env-file env.list

-w /src

EOF
