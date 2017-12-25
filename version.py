from sys import version_info, pypy_version_info as vi

try:
    from sys import maxint
except ImportError:
    from sys import maxsize as maxint

import platform

py = str(version_info[0]) + '.' + str(version_info[1]) if version_info[0] == 3 else ''

name = 'pypy' + py + '-' + '.'.join(map(str, vi[:3]))

if vi.releaselevel != 'final':
    name += '-' + vi.releaselevel

    if vi.serial:
        name += str(vi.serial)

if vi.releaselevel == 'alpha':
    from datetime import datetime
    name += '-' + datetime.now().strftime('%Y%m%d')

machine = 'x86_64' if maxint > 2**31 - 1 else 'i686'

name += '-linux_' + machine + '-portable'

print(name)
