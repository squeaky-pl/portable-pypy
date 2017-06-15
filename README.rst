====================================
Portable PyPy distribution for Linux
====================================

This repository contains efforts to build 64 bit
x86 `PyPy <http://pypy.org>`_ binaries for various Linux distributions. The idea
is that you just download an archive, uncompress it and run
it instantly without installing any extra libraries or tweaking
your OS.
Currently they are known to work across various DEB and RPM based
distributions including RHEL/Centos 6 and later, Fedora, SuSE Linux, Ubuntu and Debian stable.
PyPy binaries should run on any distribution that includes glibc 2.17.

Latest Python 3.5 release
=========================

`PyPy3.5 5.8 beta x86_64 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy3.5-5.8-1-beta-linux_x86_64-portable.tar.bz2>`_::

    md5:    67408e5d8db6f97dbb574ad75cb1476c
    sha1:   f93eb33c6a9a7095afeeee3aedc52d943a1f5057
    sha256: cab20a6d315a1bb05aa953ebc37d8deaa34dcbe298cb5938e373c42c05542b99

Latest Python 2.7 release
=========================

`PyPy 5.8 x86_64 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-5.8-1-linux_x86_64-portable.tar.bz2>`_::

    md5:    b846cb3737db59ff604d11cc74c157ce
    sha1:   989039a27104b1890766e75c97b631d5b42dd67a
    sha256: 52556230af5769c656173ae8a1bdcb2e16aef46e3993ed89f3aec3d220aec862


All downloads can be found `here <https://bitbucket.org/squeaky/portable-pypy/downloads>`_

Using virtualenv
================

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

Binaries are built with a CentOS 6 base image with help of `docker <http://docker.com/>`_.
That ensures that they are built against version of GLIBC that is reasonably
old not to cause problems with symbol versioning.
All the dependencies are also built inside chroot from latest stable tarballs. They are packed together with PyPy
into one distribution and `RPATH <http://enchildfone.wordpress.com/2010/03/23/a-description-of-rpath-origin-ld_library_path-and-portable-linux-binaries/>`_
entries are inserted into them (this ensures that they can be found relatively to each other).

If you want to build it yourself checkout instructions inside `BUILD.rst`.
