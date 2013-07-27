#!/usr/bin/env python

bundle = ['sqlite3', 'ncurses', 'panel', 'ssl',
          'crypto', 'ffi', 'expat', 'tcl', 'tk']

from os import chdir, mkdir
from os.path import dirname, relpath, join, samefile, exists, basename
from shutil import copy2, copytree
from sys import argv
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
        if path == 'not found':
            print 'Broken dependency in ' + binary
        path = path.split(' ')[0]
        if not path:
            continue

        if needed[3:].split('.', 1)[0] not in bundle:
            continue

        deps[needed] = path
        deps.update(get_deps(path))

    return deps


def gather_deps(binaries):
    deps = {}
    for binary in binaries:
        deps.update(get_deps(binary))

    return deps


def copy_deps(deps):
    copied = {}

    for needed, path in deps.items():
        if exists('lib/' + needed) and samefile(path, 'lib/' + needed):
            continue

        copy2(path, 'lib/' + needed)
        copied[path] = 'lib/' + needed

    return copied


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
    binaries.extend(glob('lib_pypy/_tkinter/__pycache__/*.so'))

    deps = gather_deps(binaries)

    copied = copy_deps(deps)

    for path, item in copied.items():
        print('Copied {0} to {1}'.format(path, item))

    binaries.extend(copied.values())

    rpaths = rpath_binaries(binaries)
    for binary, rpath in rpaths.items():
        print('Set RPATH of {0} to {1}'.format(binary, rpath))

    return deps


if __name__ == '__main__':
    chdir(argv[1])

    try:
        mkdir('lib')
    except OSError:
        pass

    main()

    # tcl/tk library
    copytree('/opt/prefix/lib/tcl8.6', 'lib/tcl')
    copytree('/opt/prefix/lib/tk8.6', 'lib/tk')
    call(['patch', 'lib_pypy/_tkinter/app.py', '../_tkinter_app.py.patch'])

    # virtualenv
    if not exists('virtualenv_support'):
        mkdir('virtualenv_support')

    root = 'https://raw.github.com/pypa/virtualenv/1.10.X'
    files = ['virtualenv.py', 'virtualenv_support/pip-1.4.tar.gz',
             'virtualenv_support/setuptools-0.9.7.tar.gz']
    for file in files:
        call(['wget', '-O', join('virtualenv_support', basename(file)),
              join(root, file)])

    call(['patch', 'virtualenv_support/virtualenv.py',
          '../virtualenv.py.patch'])
    copy2('../virtualenv-pypy', 'bin/virtualenv-pypy')
    call(['chmod', 'a+x', 'bin/virtualenv-pypy'])
