import autovenv
import unittest
import tempfile
import os, sys
from pathlib import Path
import pytest

WHOAMI = 'executable.txt'

def whoami():
    autovenv.run('','-c','import sys, pathlib; pathlib.Path("%s").write_text(sys.prefix)' % WHOAMI)


def test_activate(monkeypatch, tmpdir):
    monkeypatch.chdir(tmpdir)
    whoami()
    assert Path(Path(WHOAMI).read_text()).samefile(sys.base_prefix)

    os.mkdir('venv')
    whoami()
    assert (Path(str(tmpdir)) / 'venv').samefile(Path(WHOAMI).read_text())


if __name__ == '__main__':
    pytest.main()
