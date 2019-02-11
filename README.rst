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

`PyPy3.6 7.0.0 alpha x86_64 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy3.6-7.0.0-alpha-20190209-linux_x86_64-portable.tar.bz2>`_::

    md5:    5f7d8e0eb2a3ef26e7cb7db263c6567c
    sha1:   096a04506238c95e1379a155c220c69a26b295d6
    sha256: ef8a5254b9a082dec23a6e029b1bb674a122a789c29d9c452452a9e97498bcbe

Latest Python 3.5 release
=========================

`PyPy3.5 7.0.0 x86_64 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy3.5-7.0.0-linux_x86_64-portable.tar.bz2>`_::

    md5:    74bf9406a79552a307b36637f039fb11
    sha1:   1c8123a43be60ccd3d3f5b3888bbc0900cc1e640
    sha256: b0fa200f25a5a0ef90b8776ab1d0665c47d47c607d2ef057cce1da1ad2568e1f

Latest Python 2.7 release
=========================

`PyPy 7.0.0 x86_64 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-7.0.0-linux_x86_64-portable.tar.bz2>`_::

    md5:    f379549e05da312da6b231d643a4bede
    sha1:   e02879902f9f8ff3666e9fe4e1b11f0f9f1cb462
    sha256: fd71f2bef69c342e492239c2de04a67676bbc08b262d31948bef9e1385a44646


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
