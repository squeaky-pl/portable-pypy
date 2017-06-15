

def _add_lazy_options():
    options = [
        ('SO_BINDTODEVICE', 25, (3, 8)),
        ('SO_DOMAIN', 39, (2, 6, 32)),
        ('SO_MARK', 36, (2, 6, 25)),
        ('SO_PROTOCOL', 38, (2, 6, 32)),
        ('SO_REUSEPORT', 15, (3, 9))
    ]

    import platform

    kern_version = platform.release().partition('-')[0]
    kern_version = kern_version.replace('.', ' ').replace('_', ' ')
    kern_version = tuple(map(int, kern_version.split()))

    for name, value, version in options:
        if name in globals():
            continue

        if kern_version >= version:
            globals()[name] = value

_add_lazy_options()
del _add_lazy_options

