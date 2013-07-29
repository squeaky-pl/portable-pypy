====================================
Portable PyPy distribution for Linux
====================================

This repository contains efforts to build 32 and 64 bit
x86 PyPy binaries for various Linux distrubtions. The idea
is that you just download an archive, uncompress it and run
it instantly without installing any extra libraries or tweaking
your OS.
Currenly they are known to work across various DEB and RPM based
distributions including RHEL/Centos 5 and later, Ubuntu and Debian stable.

Latest release
==============

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
