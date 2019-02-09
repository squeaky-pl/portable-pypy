FROM centos:centos6

RUN yum install -y wget make bzip2-devel zlib-devel glibc-devel libX11-devel libXt-devel patch expat libXft-devel

RUN wget https://github.com/squeaky-pl/centos-devtools/releases/download/8.2/gcc-8.2.0-binutils-2.31.1-x86_64.tar.bz2 -O - | tar -C / -xj
RUN wget https://github.com/squeaky-pl/centos-devtools/releases/download/7.2/gcc-7.2.0-binutils-2.29.1-x86_64.tar.bz2 -O - | tar -C / -xj

