import sys, os, pdb
from multiprocessing import *


class ForkedPdb(pdb.Pdb):
    def interaction(self, *args, **kwargs):
        _stdin = sys.stdin
        try:
            sys.stdin = open('/dev/stdin')
            pdb.Pdb.interaction(self, *args, **kwargs)
        finally:
            sys.stdin = _stdin


def run(stdin_fileno, stdout_fileno):
    sys.stdout = os.fdopen(stdin_fileno)
    sys.stdin = os.fdopen(stdout_fileno)
    breakpoint()
    # pdb.Pdb().set_trace()
    1 + 1


def run(*args):
    ForkedPdbFileNo().set_trace()

class ForkedPdbFileNo(pdb.Pdb):
    _parent_stdin_fileno = sys.stdin.fileno()
    _parent_stdin = None
    def __init__(self):
        pdb.Pdb.__init__(self, nosigint=True)

    def _cmdloop(self):
        prev_stdin = sys.stdin
        try:
            if not self._parent_stdin:
                self._parent_stdin = os.fdopen(self._parent_stdin_fileno)
            sys.stdin = self._parent_stdin
            self.cmdloop()
        finally:
            sys.stdin = prev_stdin


def test():
    from _pytest.debugging import pytestPDB
    capman = pytestPDB._pluginmanager.get_plugin('capturemanager')
    capman.suspend_global_capture(in_=True)
    stdin_fileno = sys.stdin.fileno()
    stdout_fileno = sys.stdout.fileno()
    capman.resume()
    
    
    # breakpoint()

    p = Process(target=run, args=(stdin_fileno, stdout_fileno))
    p.start()
    import time
    time.sleep(100)

if __name__ == "__main__":
    p = Process(target=run)
    p.start()
