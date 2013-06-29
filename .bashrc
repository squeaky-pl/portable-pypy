source /opt/centos/devtoolset-1.1/enable

export PATH=/opt/prefix/bin:$PATH
export CFLAGS=-I/opt/prefix/include
export CPPFLAGS=-I/opt/prefix/include
export LDFLAGS="-L/opt/prefix/lib -Wl,-rpath,/opt/prefix/lib"
export PS1=(CentOS $(uname -m))$PS1


cd /opt/prefix
