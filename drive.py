#!/usr/bin/env python

import errno
import os
from os import makedirs
from os.path import isdir, join, exists, basename, dirname, samefile, abspath
from subprocess import check_call, CalledProcessError
from shutil import rmtree, copytree, copy2
import sys
from urlparse import urlparse


here = dirname(abspath(__file__))


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
        if exists(dest) and samefile(src, dest):
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

    proot = 'http://static.proot.me/proot-x86'
    if sys.maxint == 2 ** 63 - 1:
        proot += '_64'
    urlcopy(proot, join(here, 'proot'))
    check_call(['chmod', 'a+x', join(here, 'proot')])

    # XXX hack
    rmtree(join(root, 'etc/yum.repos.d'))
    ensuredirs(join(root, 'etc/yum.repos.d'))
    copy2(join(here, 'CentOS-Base.repo'), join(root, 'etc/yum.repos.d'))
    # XXX end hack

    copy2(join(here, 'yum.conf'), join(root, 'etc/yum.conf'))

    runinroot(root, ['yum', 'install', '-y', 'yum-downloadonly'])

    def install(packages):
        runinroot(root, ['mkdir', '-p', '/tmp/rpms'])
        runinroot(
            root,
            ['yum', 'install', '-y', '--downloadonly',
             '--downloaddir=/tmp/rpms'] + packages, okcode=1)
        runinroot(
            root,
            ['/bin/bash', '-c', 'rpm -i --noscripts --force /tmp/rpms/*'])
        runinroot(root, ['rm', '-r', '/tmp/rpms'])

    install(
        ['bzip2-devel', 'zlib-devel', 'ncurses-devel', 'perl',
         'glibc-devel', 'libX11-devel', 'libXt-devel', 'patch'])

prootenv = {
    'PATH': '/opt/devtools/bin:/opt/prefix/bin:/opt/pypy/bin:' +
    os.environ['PATH'],
    'CFLAGS': '-I/opt/prefix/include',
    'CPPFLAGS': '-I/opt/prefix/include',
    'LDFLAGS': '-L/opt/prefix/lib -Wl,-rpath,/opt/prefix/lib'
}


def runinroot(root, cmd, cwd=None, okcode=None):
    args = ['./proot', '-b', '/run:/run', '-0', '-R', root]
    if cwd:
        args.append('--cwd=' + cwd)
    args.extend(cmd)

    try:
        check_call(args, env=prootenv)
    except CalledProcessError as e:
        if e.returncode != okcode:
            raise


deps = [
    'http://hydra.nixos.org/build/1524660/download/2/patchelf-0.6.tar.bz2',
    'http://sqlite.org/2013/sqlite-autoconf-3080200.tar.gz',
    'http://www.mirrorservice.org/sites/sourceware.org/pub/libffi/libffi-3.0.13.tar.gz',
    'http://www.openssl.org/source/openssl-1.0.1f.tar.gz',
    'http://downloads.sourceforge.net/project/expat/expat/2.1.0/expat-2.1.0.tar.gz',
    'http://prdownloads.sourceforge.net/tcl/tcl8.6.1-src.tar.gz',
    'http://prdownloads.sourceforge.net/tcl/tk8.6.1-src.tar.gz'
]


def builddeps(root):
    srcdir = join(root, 'workspace/src')
    for url in deps:
        name = basename(url).split('.tar.')[0]
        if name.startswith(('tcl', 'tk')):
            name = name[:-4] + '/unix' # get rid of src and add subdir
        directory = join(srcdir, name)

        if exists(directory):
            rmtree(directory)

        unpack(url, srcdir)

        configure = ['./config', 'shared'] if name.startswith('openssl') else \
            ['./configure']
        runinroot(root, configure + ['--prefix=/opt/prefix'], cwd=directory)

        if name.startswith('openssl'):
            runinroot(
                root,
                ['sed', '-i',
                 's#^SHARED_LDFLAGS=\\(.*\\)#SHARED_LDFLAGS={} \\1#'.format(prootenv['LDFLAGS']),
                 'Makefile'],
                cwd=directory)
        runinroot(
            root, ['make', '-j4'], cwd=directory,
            okcode=(2 if name.startswith('openssl') else None))
        runinroot(root, ['make', 'install'], cwd=directory)

        if name.startswith('libffi'):
            libdir = join(root, 'opt/prefix/lib')
            if exists(libdir):
                runinroot(
                    root,
                    ['bash', '-c',
                     'find . -name ffi.h | xargs -i ln -sf ../lib/{} ../include/'],
                    cwd=libdir)
                runinroot(
                    root,
                    ['bash', '-c',
                     'find . -name ffitarget.h | xargs -i ln -sf ../lib/{} ../include/'],
                    cwd=libdir)

        if name.startswith('tcl'):
            runinroot(root, ['ln', '-s', '/opt/prefix/lib/libtcl8.6.so', '/opt/prefix/lib/libtcl.so'])

        if name.startswith('tk'):
            runinroot(root, ['ln', '-s', '/opt/prefix/lib/libtk8.6.so', '/opt/prefix/lib/libtk.so'])

    runinroot(root, ['bash', '-c', 'cp -ra /opt/prefix/lib64/* /opt/prefix/lib'])


def translate(root):
    srcdir = join(root, 'workspace/src/pypy')
    if exists(srcdir):
        rmtree(srcdir)
    ensuredirs(srcdir)
    unpack('https://bitbucket.org/pypy/pypy/get/default.tar.bz2', srcdir, strip=1)

    runinroot(root, ['pypy', 'rpython/bin/rpython', '-Ojit', 'pypy/goal/targetpypystandalone.py'], cwd=srcdir)


def package(root):
    srcdir = join(root, 'workspace/src/pypy')

    runinroot(root, ['pypy', 'pypy/tool/release/package.py', '.', 'pypy', 'pypy', '/workspace', './pypy-c'], cwd=srcdir)

    if exists(join(root, 'workspace/pypy')):
        rmtree(join(root, 'workspace/pypy'))

    unpack(join(root, 'workspace/pypy.tar.bz2'), join(root, 'workspace'))

    ensuredirs(join(root, 'workspace/pypy/virtualenv_support'))

    baseurl = 'https://github.com/pypa/virtualenv/raw/1.11.4'
    files = ['virtualenv.py', 'virtualenv_support/pip-1.5.4-py2.py3-none-any.whl',
             'virtualenv_support/setuptools-2.2-py2.py3-none-any.whl']

    for filename in files:
        urlcopy(join(baseurl, filename), join(root, 'workspace/pypy/virtualenv_support'))

    copy2(join(here, 'virtualenv-pypy'), join(root, 'workspace/pypy/bin/virtualenv-pypy'))

    for filename in ['virtualenv.py.patch', '_tkinter_app.py.patch', 'make_portable']:
        copy2(join(here, filename), join(root, 'workspace'))

    runinroot(root, ['pypy', 'make_portable', 'pypy'], cwd=join(root, 'workspace'))

    if exists(join(root, 'workspace/portable-pypy')):
        rmtree(join(root, 'workspace/portable-pypy'))

    check_call(['mv', join(root, 'workspace/pypy'), join(root, 'workspace/portable-pypy')])
    check_call(['tar', '-cjf', join(here, 'portable-pypy.tar.bz2'), 'portable-pypy'], cwd=join(root, 'workspace'))


if __name__ == '__main__':
    from sys import argv

    if argv[1] == 'create':
        create(argv[2])
    elif argv[1] == 'shell':
        runinroot(argv[2], ['/bin/bash'])
    elif argv[1] == 'builddeps':
        builddeps(argv[2])
    elif argv[1] == 'translate':
        translate(argv[2])
    elif argv[1] == 'package':
        package(argv[2])
    else:
        assert False, "Invalid action"
