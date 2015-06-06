Guide to building Portably PyPy yourself
========================================

You are going to need Docker installed. I used docker 1.6 on Fedora to accompish
this.

All the commands are executed from the repository root.

First build a base image containging basic headers and up to date multilib GCC

.. code:: bash

    docker build -t pypy image


Then you are gonna need to build CPython to translate PyPy, you might think
I could reuse Portably PyPy to translate PyPy but there are some problems with
that, mainly because PyPy uses host Python to find out availability of some
function inside ``os`` module. So if there is a version that introduces new symbols
they might be not there yet.

From now on we are gonna use environment variable ABI set to either 32 or 64
to choose the either i686 or x86_64 builds. For the purpose of this guide
I am only gonna build 64 bit Portable PyPy.

The commands put all the source files into ``src64`` directory and all the build
artifacts into ``prefix64`` directory relative to current working directory.

.. code:: bash

    docker run --rm `ABI=64 ./runopt.sh` pypy ./build_cpython


Next we need to build all the up to date dependencies that pypy needs like
OpenSSL, libffi etc.

.. code:: bash

    docker run --rm `ABI=64 ./runopt.sh` pypy ./build_deps


Now we are ready to translate PyPy, the last parameter is the branch name or commit
hash in the PyPy Bitbucket repository. Let's build PyPy 2.6:

.. code:: bash

    docker run --rm `ABI=64 ./runopt.sh` pypy ./build release-2.6.0


This will take some time, around 90 minutes on modern hardware with enough RAM.

After obtaining the binary we need build cffi modules,
bundle needed shared objects and virtualenv,
patch it to make it relocatable and package all together.

.. code:: bash

    docker run --rm `ABI=64 ./runopt.sh` pypy ./package


You will see a line like: ``using pypy-2.6-linux_x86_64-portable`` at the end.
This leaves with a final tarball ``src64/pypy-2.6-linux_x86_64-portale.tar.bz2``
and you are done.
