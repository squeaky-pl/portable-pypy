#!/usr/bin/env python

import errno
import os
from os import makedirs
from os.path import isdir, join, exists, basename, dirname, samefile, abspath
from subprocess import check_call, check_output, CalledProcessError
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


def urlcopy(src, dest=None, use_cache=True):
    cache = ensuredirs(join(here, 'cache'))

    if use_cache:
        cached = join(cache, basename(src))

        if exists(cached):
            src = cached

    if not dest:
        dest = cache

    if isdir(dest):
        dest = join(dest, basename(src))

    if urlparse(src).scheme:
        check_call(['wget', '-O', dest, src])

        if use_cache and not exists(cached):
            copy2(dest, cache)
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


def unpack(src, dest, strip=0, excludes=None, okcode=None, use_cache=True):
    if urlparse(src).scheme:
        src = urlcopy(src, use_cache=use_cache)

    ensuredirs(dest)

    args = ['tar', 'xf', src, '--strip-components=' + str(strip), '-C', dest]
    if excludes:
        args.extend('--exclude=' + e for e in excludes)

    try:
        check_call(args)
    except CalledProcessError as e:
        if e.returncode != okcode:
            raise


devtools, pypy = """
https://bitbucket.org/squeaky/centos-devtools/downloads/gcc-4.8.2-binutils-2.23.2-{arch}.tar.bz2
https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-2.3.1-linux_{arch}-portable.tar.bz2
""".strip().split()


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
    unpack(
        url, root,
        excludes=['./dev', './etc/udev/devices', './var/named/chroot/dev'])

    for path in ['opt/pypy', 'opt/prefix', 'workspace/src', 'workspace/tmp']:
        ensuredirs(join(root, path))

    unpack(devtools.format(arch=arch), root)
    unpack(pypy.format(arch=arch), join(root, 'opt/pypy'), strip=1)

    proot = 'http://static.proot.me/proot-x86'
    if sys.maxint == 2 ** 63 - 1:
        proot += '_64'
    urlcopy(proot, join(here, 'proot'))
    check_call(['chmod', 'a+x', join(here, 'proot')])

    with open(join(root, 'etc/yum.conf'), 'a') as f:
        f.write('\nmultilib_policy=best')

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
    'PATH': '/opt/devtools/bin:/opt/prefix/bin:/opt/pypy/bin:/bin:' +
    os.environ['PATH'],
    'CFLAGS': '-I/opt/prefix/include',
    'CPPFLAGS': '-I/opt/prefix/include',
    'LDFLAGS': '-L/opt/prefix/lib -Wl,-rpath,/opt/prefix/lib',
    'PYPY_USESSION_DIR': '/workspace/tmp'
}


def runinroot(root, cmd, cwd=None, okcode=None, call=check_call):
    args = ['./proot', '-b', '/var/run/nscd/socket', '-0', '-R', root, '-b', '/run', '-b', '.:/host']
    if cwd:
        args.append('--cwd=' + cwd)
    args.extend(cmd)

    try:
        return call(args, env=prootenv)
    except CalledProcessError as e:
        if e.returncode != okcode:
            raise


deps = """
http://releases.nixos.org/patchelf/patchelf-0.8/patchelf-0.8.tar.gz
http://sqlite.org/2014/sqlite-autoconf-3080500.tar.gz
http://www.mirrorservice.org/sites/sourceware.org/pub/libffi/libffi-3.1.tar.gz
http://www.openssl.org/source/openssl-1.0.1h.tar.gz
http://downloads.sourceforge.net/project/expat/expat/2.1.0/expat-2.1.0.tar.gz
http://ftp.gnu.org/gnu/gdbm/gdbm-1.11.tar.gz
http://prdownloads.sourceforge.net/tcl/tcl8.6.1-src.tar.gz
http://prdownloads.sourceforge.net/tcl/tk8.6.1-src.tar.gz
""".strip().split()


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
            runinroot(root, ['ln', '-sf', '/opt/prefix/lib/libtcl8.6.so', '/opt/prefix/lib/libtcl.so'])

        if name.startswith('tk'):
            runinroot(root, ['ln', '-sf', '/opt/prefix/lib/libtk8.6.so', '/opt/prefix/lib/libtk.so'])

    if exists(join(root, 'opt/prefix/lib64')):
        runinroot(root, ['bash', '-c', 'cp -ra /opt/prefix/lib64/* /opt/prefix/lib'])

    # force static linking of crypto,ssl,ffi,expat
    runinroot(root, ['bash', '-c', 'rm /opt/prefix/lib/lib{crypto,ssl,ffi,expat}.so*'])


def translate(root, revision=None):
    if not revision:
        revision = 'default'

    srcdir = join(root, 'workspace/src/pypy')
    if exists(srcdir):
        rmtree(srcdir)
    ensuredirs(srcdir)
    unpack('https://bitbucket.org/pypy/pypy/get/{}.tar.bz2'.format(revision), srcdir, strip=1, use_cache=False)

    runinroot(root, ['pypy', 'rpython/bin/rpython', '-Ojit', 'pypy/goal/targetpypystandalone.py'], cwd=srcdir)


def package(root, skip_numpy=False):
    srcdir = join(root, 'workspace/src/pypy')

    runinroot(root, ['pypy', 'pypy/tool/release/package.py', '--rename_pypy_c', 'pypy', '--archive-name', 'pypy', '--targetdir', '/workspace', '--override_pypy_c', './pypy-c'], cwd=srcdir, okcode=255)

    if exists(join(root, 'workspace/pypy')):
        rmtree(join(root, 'workspace/pypy'))

    unpack(join(root, 'workspace/pypy.tar.bz2'), join(root, 'workspace'))

    ensuredirs(join(root, 'workspace/pypy/virtualenv_support'))

    baseurl = 'https://github.com/pypa/virtualenv/raw/1.11.6'
    files = ['virtualenv.py', 'virtualenv_support/pip-1.5.6-py2.py3-none-any.whl',
             'virtualenv_support/setuptools-3.6-py2.py3-none-any.whl']

    for filename in files:
        urlcopy(join(baseurl, filename), join(root, 'workspace/pypy/virtualenv_support'))

    copy2(join(here, 'virtualenv-pypy'), join(root, 'workspace/pypy/bin/virtualenv-pypy'))

    runinroot(root, ['pypy', '/host/make_portable', 'pypy'], cwd=join(root, 'workspace'))

    if exists(join(root, 'workspace/src/numpy')):
        rmtree(join(root, 'workspace/src/numpy'))

    if not skip_numpy:
        unpack('https://bitbucket.org/pypy/numpy/get/master.tar.bz2', join(root, 'workspace/src/numpy'), strip=1, use_cache=False)
        runinroot(root, ['/workspace/pypy/bin/pypy', 'setup.py', 'install'], cwd=join(root, 'workspace/src/numpy'))

        # compile cffi extensions
        runinroot(root, ['/workspace/pypy/bin/pypy', '-c', 'import numpy.fft.fft_cffi'])

    # archive name
    name = runinroot(root, ['/workspace/pypy/bin/pypy', '/host/version.py'], call=check_output).strip()

    # cleanup
    check_call(['find', join(root, 'workspace/pypy'), '-name', '*.pyc', '-delete'])
    check_call(['find', join(root, 'workspace/pypy'), '-name', '_cffi__*.[oc]', '-delete'])

    if exists(join(root, 'workspace', name)):
        rmtree(join(root, 'workspace', name))

    check_call(['mv', join(root, 'workspace/pypy'), join(root, 'workspace', name)])
    check_call(['tar', '-cjf', join(here, name + '.tar.bz2'), name], cwd=join(root, 'workspace'))


if __name__ == '__main__':
    from sys import argv

    if argv[1] == 'create':
        create(argv[2])
    elif argv[1] == 'shell':
        runinroot(argv[2], ['/bin/bash'])
    elif argv[1] == 'builddeps':
        builddeps(argv[2])
    elif argv[1] == 'translate':
        translate(argv[2], *argv[3:])
    elif argv[1] == 'package':
        package(argv[2], *argv[3:])
    else:
        assert False, "Invalid action"
