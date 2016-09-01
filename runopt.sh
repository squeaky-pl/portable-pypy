#!/bin/bash

set -e

cat <<EOF

-v `pwd`/src$ABI:/src
-v `pwd`/build_deps:/src/build_deps
-v `pwd`/build:/src/build
-v `pwd`/build_cpython:/src/build_cpython
-v `pwd`/package:/src/package
-v `pwd`/make_portable:/src/make_portable
-v `pwd`/version.py:/src/version.py
-v `pwd`/platform_linux.patch:/src/platform_linux.patch
-v `pwd`/_tkinter_app.py.patch:/src/_tkinter_app.py.patch
-v `pwd`/subprocess.py.patch:/src/subprocess.py.patch
-v `pwd`/subprocess3.py.patch:/src/subprocess3.py.patch
-v `pwd`/sysconfig_pypy.py.patch:/src/sysconfig_pypy.py.patch
-v `pwd`/recursion.patch:/src/recursion.patch
-v `pwd`/virtualenv-pypy:/src/virtualenv-pypy
-v `pwd`/prefix$ABI:/opt/prefix

-e ABI=$ABI

--env-file env.list

-w /src

EOF
