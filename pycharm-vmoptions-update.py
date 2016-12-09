#! /usr/bin/env python
from __future__ import print_function
import re

with open('/Applications/PyCharm.app/Contents/bin/pycharm.vmoptions', 'r') as f:
    s_orig = f.read()
    s = re.sub(r'-Xmx\S+', '-Xmx1250m', s_orig)
print(s)

with open('/Applications/PyCharm.app/Contents/bin/pycharm.vmoptions', 'w') as f:
    f.write(s)

with open('/Applications/PyCharm.app/Contents/bin/pycharm.vmoptions', 'r') as f:
    s2 = f.read()
    if s2 != s:
        print('Failed to update correctly')
        print('%r != %r' % (s, s2))
        print('s_orig = %r' % s_orig)