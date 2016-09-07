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

`PyPy 5.4 x86_64 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-5.4-linux_x86_64-portable.tar.bz2>`_::

    md5:    abed31aa998562b8d52139e73c8b5014
    sha1:   9969380848e5e907f5804070f6102fc5a5580526
    sha256: 0a48c7ba7163589b1ade9cfe184f422d1bc9a0f988321b2fdcbd924d90594d9a

`PyPy 5.4 i686 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-5.4-linux_i686-portable.tar.bz2>`_::

    md5:    f4019455bd82286ad5423ab42c53eea3
    sha1:   7e6bf14420c8f20000ea10eaa066ece63fbde766
    sha256: 7d7d253f009bb2624f43db6b8caeeb73d29177c4166a643a581a231a099c8689

Latest Python 3.3 release
=========================

`PyPy3.3 5.2 alpha x86_64 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy3.3-5.2-alpha-20160602-linux_x86_64-portable.tar.bz2>`_::

    md5:    0a2332b60a40e6fd3c8625ffc4f0ef9c
    sha1:   61c8dd458e336acbb90e31d03383fb0ab08f97aa
    sha256: 4d1e7dd727448c1b2caa90c943713c0aa10b32e9d977c2c3b348835f515a3ad4

`PyPy3.3 5.2 alpha i686 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy3.3-5.2-alpha-20160602-linux_i686-portable.tar.bz2>`_::

    md5:    44bdce72b4754bebda03a12ff7cd6dfc
    sha1:   056c433a20ceadd4fc9389a77eb1203021a8d976
    sha256: 6f2412167c63d6711b41062a23794828f95a75400082a6957595867762cb170d


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

How it is done
==============

Binaries are built with a CentOS 5 base image with help of `docker <http://docker.com/>`_.
That ensures that they are built against version of GLIBC that is reasonably
old not to cause problems with symbol versioning.
All the dependencies are also built inside chroot from latest stable tarballs. They are packed together with PyPy
into one distribution and `RPATH <http://enchildfone.wordpress.com/2010/03/23/a-description-of-rpath-origin-ld_library_path-and-portable-linux-binaries/>`_
entries are inserted into them (this ensures that they can be found relatively to each other).

If you want to build it yourself checkout instructions inside `BUILD.rst`.
