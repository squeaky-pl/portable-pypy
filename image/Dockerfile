FROM centos:centos5

RUN rm /etc/yum.repos.d/*
COPY CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo 
RUN yum install -y wget make bzip2-devel zlib-devel glibc-devel libX11-devel libXt-devel patch expat.x86_64 libXft-devel

RUN wget https://github.com/squeaky-pl/centos-devtools/releases/download/6.3/gcc-6.3.0-binutils-2.27-x86_64.tar.bz2 -O - | tar -C / -xj
