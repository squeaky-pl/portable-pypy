FROM centos:centos5

RUN yum install -y make bzip2-devel bzip2-devel.i386 zlib-devel zlib-devel.i386 perl glibc-devel glibc-devel.i386 libX11-devel libX11-devel.i386 libXt-devel libXt-devel.i386 patch expat.i386 expat.x86_64

RUN yum install -y wget
RUN wget https://github.com/squeaky-pl/centos-devtools/releases/download/6.2/gcc-6.2.0-binutils-2.27-x86_64.tar.bz2 -O - | tar -C / -xj
RUN ln -s /opt/devtools-6.2/bin/gcc /opt/devtools-6.2/bin/cc
RUN yum install -y setarch
