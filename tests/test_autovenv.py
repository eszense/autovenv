import autovenv
import unittest
import tempfile
import os, sys
import shutil
from pathlib import Path
import pytest
from configparser import ParsingError
    
WHOAMI = 'executable.txt'
VERSION = 'version.txt'
def whoami():
    autovenv.run('','-c',   'import sys, pathlib;\
                             pathlib.Path("%s").write_text(sys.prefix);\
                             pathlib.Path("%s").write_text(str(sys.version_info[0])+"."+str(sys.version_info[1]))' % (WHOAMI,VERSION))
 
def test_activate(monkeypatch, tmpdir):
    monkeypatch.chdir(tmpdir)
    whoami()
    assert Path(Path(WHOAMI).read_text()).samefile(sys.base_prefix)
    assert Path(VERSION).read_text() == str(sys.version_info[0])+"."+str(sys.version_info[1])

    os.mkdir('venv')
    whoami()
    assert (Path(str(tmpdir)) / 'venv').samefile(Path(WHOAMI).read_text())
    assert Path(VERSION).read_text() == str(sys.version_info[0])+"."+str(sys.version_info[1])

    
def test_version(monkeypatch, tmpdir):
    monkeypatch.chdir(tmpdir)
    os.mkdir('venv')
    (Path(str(tmpdir)) / 'autovenv.ini' ).write_text("[defaults]\npython=3.5")
    whoami()
    assert (Path(str(tmpdir)) / 'venv').samefile(Path(WHOAMI).read_text())
    assert Path(VERSION).read_text() == '3.5'


def test_error(monkeypatch, tmpdir):
    monkeypatch.chdir(tmpdir)
    os.mkdir('venv')
    (Path(str(tmpdir)) / 'autovenv.ini' ).write_text("[defaults]\npython3.1")
    with pytest.raises(ParsingError):
        whoami()
    

if __name__ == '__main__':
    pytest.main()
