export PATH=/opt/devtools/bin:/opt/prefix/bin:/opt/pypy/bin:$PATH
export CFLAGS=-I/opt/prefix/include
export CPPFLAGS=-I/opt/prefix/include
export LDFLAGS="-L/opt/prefix/lib -Wl,-rpath,/opt/prefix/lib"
export PS1=(CentOS $(uname -m))$PS1


cd /opt/prefix
