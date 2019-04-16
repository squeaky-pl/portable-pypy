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


Latest Python 3.6 release
=========================

`PyPy3.6 7.1.1 beta x86_64 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy3.6-7.1.1-beta-linux_x86_64-portable.tar.bz2>`_::

    md5:    1f44293675da46a45a3ddbd3d28d26f9
    sha1:   17de4561ec95b878757d9686a94e20d4bab3dd1a
    sha256: 82c878b61ad34fc2cf1686fa600a7a002d352e1b33a99a43007eec486ecd068e

Latest Python 2.7 release
=========================

`PyPy 7.1.1 x86_64 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-7.1.1-linux_x86_64-portable.tar.bz2>`_::

    md5:    add1d1736ee6e44288fc3390a2357b79
    sha1:   882beac41c4c672868f8eeb1f997b8ca327b37e1
    sha256: d0b226d2dd656c622cee4e3e982225e1b346653823b49f736d8b0ddc06fd0c73


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
