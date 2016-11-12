====================================
Portable PyPy distribution for Linux
====================================

This repository contains efforts to build 32 and 64 bit
x86 `PyPy <http://pypy.org>`_ binaries for various Linux distributions. The idea
is that you just download an archive, uncompress it and run
it instantly without installing any extra libraries or tweaking
your OS.
Currently they are known to work across various DEB and RPM based
distributions including RHEL/Centos 5 and later, Ubuntu and Debian stable.
It should run on any distribution that includes GLIBC 2.3 and kernel 2.6.19
or later.

Latest Python 2.7 release
=========================

`PyPy 5.6 x86_64 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-5.6-linux_x86_64-portable.tar.bz2>`_::

    md5:    b8cb7ecdc28f922c76bf48cc581b5ad4
    sha1:   eb52e8e3c450313f5fa678a62b5a39a2f90097be
    sha256: 9bd220bc54000e142bd4929435959305efeef8c832fbe3c907211cc5214095ce

`PyPy 5.6 i686 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-5.6-linux_i686-portable.tar.bz2>`_::

    md5:    2296f9c14d495c69712a576ce7a86001
    sha1:   8abe9ae5e2fe7162cef6640664372d43f4ff0d0b
    sha256: 1f220e05ddd4423882794f0e9d3e2dfdecee259d00f1151a52dd244607313399

Latest Python 3.3 release
=========================

`PyPy3.3 5.5 alpha x86_64 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy3.3-5.5-alpha-20161013-linux_x86_64-portable.tar.bz2>`_::

    md5:    b0f064518a5742f042b5cc067f83b9d2
    sha1:   1bd7daf24d6e090d8907b80477901aa6a68ff10b
    sha256: 1cd7a00da376b2db29b3e1f3e9bb7a77afc8ad988b3f13fd0805f37b23960a34

`PyPy3.3 5.5 alpha i686 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy3.3-5.5-alpha-20161014-linux_i686-portable.tar.bz2>`_::

    md5:    51bb9b25e86868a37b76d26a4f259511
    sha1:   271815df0491dd0d9f7d737125fee960ddc17317
    sha256: af32420f368bc3276d15a5cf4e2e8cb0bef16f711ee830a636ad117e55c3268f


All downloads can be found `here <https://bitbucket.org/squeaky/portable-pypy/downloads>`_

Using virtualenv
================

For versions 2.3 and newer you can use stock virtualenv that comes from your
distribution or that you installed with PIP etc. Just pass
``-p path-to-portable-pypy/bin/pypy`` on the commandline.

For your convenience this build also includes packaged virtualenv so you
don't have to install one if you haven't done it yet::

    portable-pypy/bin/virtualenv-pypy my-environment

In this case you don't have to add ``-p`` switch as it defaults to ``pypy`` binary
located in the build.

Stock virtualenv didn't work with portable binaries prior to version 2.3 that included RPATH
entries in ``pypy`` binary. For these versions it's obligatory to use
``virtualenv-pypy`` that fixes this problem.

Included software
=================

Besides PyPy there is OpenSSL, SQLite3, libffi, expat, TCL/TK and virtualenv packaged
in these builds.

A word about OpenSSL
====================

This software bundles OpenSSL. Each build has a version of OpenSSL that was most recent and stable at the time of packaging this software. This is done because OpenSSL versions used across distrubtions in last 10 years greately vary and they are not compatible in ABI nor API way. This also means that if there is a major security issue with OpenSSL updating your system OpenSSL will not solve it for Portable PyPy. If you are looking for tight integration with your distribution you should probably wait until your distribution vendor packages version of PyPy you want to use or you can notify me and wait for a new build.

The `ssl` module will try to locate and use your system certificate store. Namely it will look for a `/etc/pki/tls/certs/ca-bundle.crt` file (RHEL derived systems) and then look for a `/etc/ssl/certs` directory (Debian dervied systems). Finally it will fallback to bundled Mozilla trust stores extraced from `certifi` project. If you don't like this behavior or your system trust store is located somewhere else you can use `SSL_CERT_FILE` and `SSL_CERT_DIR` environment variables to point it somewhere else.

How it is done
==============

Binaries are built with a CentOS 5 base image with help of `docker <http://docker.com/>`_.
That ensures that they are built against version of GLIBC that is reasonably
old not to cause problems with symbol versioning.
All the dependencies are also built inside chroot from latest stable tarballs. They are packed together with PyPy
into one distribution and `RPATH <http://enchildfone.wordpress.com/2010/03/23/a-description-of-rpath-origin-ld_library_path-and-portable-linux-binaries/>`_
entries are inserted into them (this ensures that they can be found relatively to each other).

If you want to build it yourself checkout instructions inside `BUILD.rst`.
