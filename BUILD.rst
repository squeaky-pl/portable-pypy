Guide to building Portable PyPy yourself
========================================

You are going to need Docker installed.

Quick Start
-----------

Assuming Docker is already installed and running, the quick way to build one version on one architecture (e.g., release 2.6.0, 64-bit) is:

.. code:: bash

    git clone https://github.com/squeaky-pl/portable-pypy.git
    ./portable-pypy/mkall -a 64 -r release-2.6.0


Run ``./mkall -h`` for additional options and information.


Building Using a VM
-------------------

I use Docker 1.6 on Fedora.
However, not all users run Linux natively.
You can build Portable PyPy using a VM (e.g., via |boot2docker|_ and `Vagrant`_).

.. |boot2docker| replace:: ``boot2docker``
.. _`boot2docker`: http://boot2docker.io/
.. _`Vagrant`: https://www.vagrantup.com/

``mkall`` supports using a native ``docker`` client and file system for maintaining build state, even when using a VM for running the Docker service.
First, from within your native OS clone this repository and create a build state directory:

.. code:: bash

    git clone git clone https://github.com/squeaky-pl/portable-pypy.git
    cd portable-pypy
    mkdir -p build-home/{prefix,src}
    # edit Vagrantfile (see below)


Then expose your newly-created native build state directory inside your VM.
Running ``boot2docker`` via Vagrant is beyond the scope of this documentation, but the following sample ``Vagrantfile`` extends this example:

.. code:: ruby
    # Vagrantfile
    VAGRANTFILE_API_VERSION = '2'
    Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
        config.vm.box = '.../boot2docker' # pick an appropriate image for your provider
        config.vm.synced_folder('./build-home', '/mnt/build-home', create: true, disabled: false, id: 'pypy-build-home')
        config.vm.network(:private_network, ip: '192.168.123.123')
        config.vm.provider(:...) do |v, override| # provider-specific parameters
            v.memory = 5120 # need >=4GB free to build PyPy
        end
        # ...
    end


Now, bring up the VM and do the build:

.. code:: bash

    vagrant up
    export DOCKER_HOST=tcp://192.168.123.123:2375 # IP address of VM
    ./mkall -a 64 -r release-2.6.0 -d /mnt/build-home


Note that the path given to the ``-d`` option is as perceived from within the VM (not the native OS).
This will create a tarball in the root level of the native ``build-home`` directory.


Advanced
--------

If you want more granular control, you can execute each step manually.
All commands should be executed from the repository root.

First build a base image containging basic headers and up to date multilib GCC

.. code:: bash

    docker build -t pypy .


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

    docker run --rm `ABI=64 ./runopt.sh` pypy /opt/portable-pypy/build_cpython


This is roughly equivalent to:

.. code:: base

    ./mkall -a 64 -b build_cpython


Next we need to build all the up to date dependencies that pypy needs like
OpenSSL, libffi etc.

.. code:: bash

    docker run --rm `ABI=64 ./runopt.sh` pypy /opt/portable-pypy/build_deps


This is roughly equivalent to:

.. code:: base

    ./mkall -a 64 -b build_deps


Now we are ready to translate PyPy, the last parameter is the branch name or commit
hash in the PyPy Bitbucket repository. Let's build PyPy 2.6:

.. code:: bash

    docker run --rm `ABI=64 REVISION=release-2.6.0 ./runopt.sh` pypy /opt/portable-pypy/build


This is roughly equivalent to:

.. code:: base

    ./mkall -a 64 -b build -r release-2.6.0


This will take some time, around 90 minutes on modern hardware with enough RAM.

After obtaining the binary we need build cffi modules, bundle needed shared objects and ``virtualenv``, patch it to make it relocatable and package all together.

.. code:: bash

    docker run --rm `ABI=64 REVISION=release-2.6.0 ./runopt.sh` pypy /opt/portable-pypy/package


This is roughly equivalent to:

.. code:: base

    ./mkall -a 64 -b package -r release-2.6.0


You will see a line like: ``using pypy-2.6-linux_x86_64-portable`` at the end.
This leaves with a final tarball ``pypy-2.6-linux_x86_64-portable.tar.bz2`` in the current working directory and you are done.
