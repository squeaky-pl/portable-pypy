====================================
Portable PyPy distribution for Linux
====================================

This repository contains efforts to build 32 and 64 bit
x86 `PyPy <http://pypy.org>`_ binaries for various Linux distrubtions. The idea
is that you just download an archive, uncompress it and run
it instantly without installing any extra libraries or tweaking
your OS.
Currenly they are known to work across various DEB and RPM based
distributions including RHEL/Centos 5 and later, Ubuntu and Debian stable.
It should run on any distribution that includes GLIBC 2.3 and kernel 2.6.19
or later.

Latest Python 2.7 release
=========================

`PyPy 5.1 x86_64 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-5.1-linux_x86_64-portable.tar.bz2>`_::

    md5:    eb47a9e3a9fda503b1a63c66ebd5502e
    sha1:   ec2ed33346d90923c64f8a2b6a526bbded034bac
    sha256: 893507603a58b8983b69924e60591de39b8f71f70ba36d6e3894db8f7c49c3ea

`PyPy 5.1 i686 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-5.1-linux_i686-portable.tar.bz2>`_::

    md5:    eb47a9e3a9fda503b1a63c66ebd5502e
    sha1:   ec2ed33346d90923c64f8a2b6a526bbded034bac
    sha256: 893507603a58b8983b69924e60591de39b8f71f70ba36d6e3894db8f7c49c3ea

Latest Python 3.2 release
=========================

`PyPy3 2.4 x86_64 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy3-2.4-linux_x86_64-portable.tar.bz2>`_::

    md5:    6fd83263159cc3ece4a9a186ce1ed388
    sha1:   ede1e03b1e0c4925fa0332114ed1b732d700830f
    sha256: 7b3e0f0bc924bd0d68d85c0b566979e74a2b366595db3d81502267367370a5fb

`PyPy3 2.4 i686 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy3-2.4-linux_i686-portable.tar.bz2>`_::

    md5:    deb9c7de9666d6e67939c5a97f4c0224
    sha1:   3c1cd2e201a46a32cd62d27885e749ddf6c48af0
    sha256: 7ce050b4928dc58f7e9dd01e3e48c443c85616ca83f4bcc9147f1078d0fd126c

`PyPy3 2.3.1 x86_64 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy3-2.3.1-linux_x86_64-portable.tar.bz2>`_::

    md5:    c2b876fe91396e320d3e5313fcdfc2bdx
    sha1:   f7e39cd173b6c66b057fef012a082c8c63a7be3d
    sha256: cb56b5bde8f444d44a0ea9cd475ddeed00aa895f3dcc89fd37577a51439540aa

`PyPy3 2.3.1 i686 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy3-2.3.1-linux_i686-portable.tar.bz2>`_::

    md5:    fb0d7ad6280ed41710c4f2c067bcf91c
    sha1:   5dcdad4c0724c6c84318756539be3ac4486e5866
    sha256: 32a5b3fd4299b13aedf7bc6262eee0f6be9a27744ccf787718553d973ec38abb

All downloads can be found `here <https://bitbucket.org/squeaky/portable-pypy/downloads>`_

Using virtualenv
================

For versions 2.3 and newer you can use stock virtualenv that comes from your
distribution or that you installed with PIP etc. Just pass
``-p path-to-portable-pypy/bin/pypy`` on the commandline.

For your convenience this build also includes packaged virtualenv so you
don't have to install one if you haven't done it yet::

    portable-pypy/bin/virtualenv-pypy my-environment

In this case you dont have to add ``-p`` switch as it defaults to ``pypy`` binary
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
