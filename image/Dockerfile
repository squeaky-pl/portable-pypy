FROM centos:centos6

RUN yum install -y wget make bzip2-devel zlib-devel glibc-devel libX11-devel libXt-devel patch expat libXft-devel perl

RUN wget https://github.com/squeaky-pl/centos-devtools/releases/download/8.2-s1/gcc-8.2.0-binutils-2.32-x86_64.tar.bz2 -O - | tar -C / -xj
RUN wget https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-7.0.0-linux_x86_64-portable.tar.bz2 -O - | tar -C /opt -xj
RUN mkdir -p /opt/pypy/bin
RUN ln -s /opt/pypy-7.0.0-linux_x86_64-portable/bin/pypy /opt/pypy/bin/python

