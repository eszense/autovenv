import autovenv
import unittest
import tempfile
import os, sys
from contextlib import redirect_stdout
from io import StringIO


class AutovenvTest(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self._lastcd = os.getcwd()
        os.chdir(self._tmpdir.name)
    def tearDown(self):
        os.chdir(self._lastcd)
        self._tmpdir.cleanup()

    def test_activate(self):
        out = StringIO()
        with redirect_stdout(out):
            autovenv.run('','-c','import sys;print(sys.executable)')
        autovenv.run('','-c','import sys;print(sys.executable)')

if __name__ == '__main__':
    unittest.main()
