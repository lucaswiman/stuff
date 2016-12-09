#! /usr/bin/env python
# https://medium.com/@joewalnes/handy-bash-feature-process-substitution-8eb6dce68133#.pryvjp8ba
# http://stackoverflow.com/questions/22777522/use-process-substitution-as-input-file-to-python-twice

# Usage `./process_subst.py <(echo foo) <(echo bar)`

import os, sys

with open(sys.argv[1], 'r') as foo:
    print(foo.name)
    print(foo.read())
    try:
        foo.seek(0)
    except IOError as e:
        print 'Cannot seek %r' % e

print('Getting file info for %s' % sys.argv[2])
_ = os.system('ls -ahl %s' % sys.argv[2]); sys.stdout.write('\n')
_ = os.system('cat %s' % sys.argv[2]); sys.stdout.write('\n')

with os.tmpfile() as tmp:
    print(tmp.name)
    print(tmp.fileno())
    tmp.write('asdf')
    tmp.seek(0)
    _ = os.system('cat /dev/fd/%s' % tmp.fileno()); sys.stdout.write('\n')
    print(tmp.tell())
    print(tmp.read())
    tmp.seek(0)
    print(tmp.tell())
    print(tmp.read())
