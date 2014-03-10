#!/usr/bin/env python

import errno
from os import makedirs
from os.path import isdir, join, exists, basename, dirname, samefile
from subprocess import check_call, CalledProcessError
from shutil import rmtree, copytree, copy2
from urlparse import urlparse


here = dirname(__file__)


def ensuredirs(dirs):
    try:
        makedirs(dirs)
    except OSError as e:
        if not e.errno == errno.EEXIST:
            raise

    return dirs


def urlcopy(src, dest=None):
    cache = ensuredirs(join(here, 'cache'))

    cached = join(cache, basename(src))

    if exists(cached):
        src = cached

    if not dest:
        dest = cache

    if isdir(dest):
        dest = join(dest, basename(src))

    if urlparse(src).scheme:
        check_call(['wget', '-O', dest, src])
    else:
        if samefile(src, dest):
            return dest

        if isdir(src):
            if exists(dest):
                rmtree(dest)
            copytree(src, dest)
        else:
            copy2(src, dest)

    return dest


def unpack(src, dest, strip=0, okcode=None):
    if urlparse(src).scheme:
        src = urlcopy(src)

    ensuredirs(dest)

    try:
        check_call(
            ['tar', 'xf', src, '--strip-components=' + str(strip), '-C', dest])
    except CalledProcessError as e:
        if e.returncode != okcode:
            raise


devtools = 'https://bitbucket.org/squeaky/centos-devtools/downloads/gcc-4.8.2-binutils-2.23.2-{arch}.tar.bz2'
pypy = 'https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-2.2.1-linux_{arch}-portable.tar.bz2'


def create(name):
    url = 'http://download.openvz.org/template/precreated/'
    if name == 'centos-i686':
        url += 'centos-5-x86.tar.gz'
        arch = 'i686'
    elif name == 'centos-x86_64':
        url += 'centos-5-x86_64.tar.gz'
        arch = 'x86_64'
    else:
        assert False, "Not a valid chroot image ID"

    root = join(here, name)
    unpack(url, root, okcode=2)

    for path in ['opt/pypy', 'opt/prefix', 'workspace/src']:
        ensuredirs(join(root, path))

    unpack(devtools.format(arch=arch), root)
    unpack(pypy.format(arch=arch), join(root, 'opt/pypy'), strip=1)


if __name__ == '__main__':
    from sys import argv

    if argv[1] == 'create':
        create(argv[2])
    else:
        assert False, "Invalid action"
