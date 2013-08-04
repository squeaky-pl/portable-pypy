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
It should run on any distribution that includes GLIBC 2.3 or later.

Latest Python 2.7 release
=========================

`PyPy 2.1 x86_64 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-2.1-linux_x86_64-portable.tar.bz2>`_

`PyPy 2.1 i686 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-2.1-linux_i686-portable.tar.bz2>`_

Latest Python 3.2 release
=========================

`PyPy3 2.1-beta x86_64 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy3-2.1-beta-linux_x86_64-portable.tar.bz2>`_

`PyPy3 2.1-beta i686 <https://bitbucket.org/squeaky/portable-pypy/downloads/pypy3-2.1-beta-linux_i686-portable.tar.bz2>`_

Using virtualenv
================
Stock virtualenv is not working with portable binaries including RPATH
entries. For this reason build includes specially patched ``virtualenv-pypy``
script that takes care of the details for you::

    portable-pypy/bin/virtualenv-pypy my-environment

You dont have to add -p switch as it defaults to pypy binary located in
the build.

Included software
=================

Besides PyPy there is OpenSSL, SQLite3, libffi, TCL/TK and virtualenv packaged
in these builds.
