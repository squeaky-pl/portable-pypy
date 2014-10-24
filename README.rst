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

`PyPy 2.4 x86_64 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-2.4-linux_x86_64-portable.tar.bz2>`_

`PyPy 2.4 i686 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-2.4-linux_i686-portable.tar.bz2>`_

Latest Python 3.2 release
=========================

`PyPy3 2.4 i686 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy3-2.4-linux_i686-portable.tar.bz2>`_

`PyPy3 2.3.1 x86_64 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy3-2.3.1-linux_x86_64-portable.tar.bz2>`_

`PyPy3 2.3.1 i686 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy3-2.3.1-linux_i686-portable.tar.bz2>`_

Weekly builds
=============

These are snapshots of alpha version done at the weekends.
They include also numpy precompiled for your convenience.
`Browse here <https://bitbucket.org/squeaky/portable-pypy-weekly/downloads>`_.

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

Previous versions
=================

All downloads can be found `here <https://bitbucket.org/squeaky/portable-pypy/downloads>`_

How it is done
==============

Binaries are built in a CentOS 5 chroot with help of `proot <http://proot.me/>`_.
That ensures that they are built against version of GLIBC that is reasonably
old not to cause problems with symbol versioning.
All the dependencies are also built inside chroot from latest stable tarballs. They are packed together with PyPy
into one distribution and `RPATH <http://enchildfone.wordpress.com/2010/03/23/a-description-of-rpath-origin-ld_library_path-and-portable-linux-binaries/>`_
entries are inserted into them (this ensures that they can be found relatively to each other).
