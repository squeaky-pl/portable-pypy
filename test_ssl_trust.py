import ssl
import sys
print(ssl.get_default_verify_paths())

context = ssl.create_default_context()

import socket



conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname="www.python.org")
conn.connect(("www.python.org", 443))
print('OK https://www.python.org [Verified]')
conn.close()


conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname="untrusted-root.badssl.com")
try:
    conn.connect(("untrusted-root.badssl.com", 443))
except ssl.SSLError:
    print('OK https://untrusted-root.badssl.com [Unverified]')
else:
    print('FAIL https://untrusted-root.badssl.com [Verified]')
    sys.exit(1)
finally:
    conn.close()
