#!/bin/bash

set -e

if [ -n "${BUILD_HOME}" ] ; then
    PREFIX_DIR="${BUILD_HOME}/prefix"
    SRC_DIR="${BUILD_HOME}/src"
    TARGET_DIR="${BUILD_HOME}"
else
    BUILD_HOME="$( pwd )"
fi

if [ -z "${PREFIX_DIR}" ] ; then
    SRC_DIR="${BUILD_HOME}/prefix${ABI}"
    mkdir -p "${PREFIX_DIR}"
fi

if [ -z "${SRC_DIR}" ] ; then
    SRC_DIR="${BUILD_HOME}/src${ABI}"
    mkdir -p "${SRC_DIR}"
fi

if [ -z "${TARGET_DIR}" ] ; then
    TARGET_DIR="${BUILD_HOME}"
    mkdir -p "${TARGET_DIR}"
fi

ABI="${ABI:-64}"
MAKE_PROCS="${MAKE_PROCS:-4}"
REVISION="${REVISION:-default}"

cat <<EOF

-v ${PREFIX_DIR}:/opt/prefix

-v ${SRC_DIR}:/opt/src

-v ${TARGET_DIR}:/opt/target

--env-file env.list

-e ABI=${ABI}

-e MAKE_PROCS=${MAKE_PROCS}

-e REVISION=${REVISION}

-w /opt/src

EOF
