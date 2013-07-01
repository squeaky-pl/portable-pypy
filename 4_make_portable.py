#!/usr/bin/python

bundle = ['sqlite3', 'ncurses', 'ssl', 'crypto', 'ffi', 'expat']
ffi_libs = ['sqlite3', 'curses']

from os import system, chdir, unlink, mkdir
from os.path import dirname, relpath, join
from shutil import rmtree, copy, copy2
from sys import argv, exit
from glob import glob
from subprocess import check_output, call


def get_deps(binary):
    deps = {}
    output = check_output(['ldd', binary])
    for line in output.splitlines():
        if not '=>' in line:
            continue
        line = line.strip()
        needed, path = line.split(' => ')
        path = path.split(' ')[0]
        if not path:
            continue
        deps[needed] = path
        deps.update(get_deps(path))

    return deps


def strip_deps(deps):
    stripped = {}
    for k, v in deps.items():
        name = k[3:].split('.', 1)[0]
        if not name in bundle:
            continue
        stripped[k] = v

    return stripped


def gather_deps(binaries):
    deps = {}
    for binary in binaries:
        deps.update(get_deps(binary))

    return strip_deps(deps)


def copy_deps(deps):
    for needed, path in deps.items():
        copy2(path, 'lib/' + needed)

    return ['lib/' + k for k in deps.keys()]


def rpath_binaries(binaries):
    rpaths = {}

    for binary in binaries:
        rpath = join('$ORIGIN', relpath('lib', dirname(binary)))
        call(['patchelf', '--set-rpath', rpath, binary])

        rpaths[binary] = rpath

    return rpaths


def main():
    binaries = ['bin/pypy']
    binaries.extend(glob('lib_pypy/__pycache__/*.so'))

    deps = gather_deps(binaries)
    copied = copy_deps(deps)

    for item in copied:
        print('Copied ' + item)

    binaries.extend(copied)

    rpaths = rpath_binaries(binaries)
    for binary, rpath in rpaths.items():
        print('Set RPATH of {0} to {1}'.format(binary, rpath))

    return deps


if __name__ == '__main__':
    chdir(argv[1])
    try:
        rmtree('lib')
    except OSError:
        pass

    try:
        mkdir('lib')
    except OSError:
        pass

    main()

