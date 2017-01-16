import sys
import os
import pathlib
import venv
import subprocess
from subprocess import PIPE

def runw(*args):
    run(*args, w=True)
def run(*args, w=False):
    w = 'w' if w else ''
    path = pathlib.Path.cwd()

    while not (path / 'venv').exists():
        if(path.parent == path):
            subprocess.run(('py'+w,)+args[1:])
            return
        path = path.parent

    if not (path / 'venv' / 'Scripts' / ('python'+w+'.exe')).exists():
        venv.create(str((path / 'venv').absolute()), clear=True, with_pip=True)
        (path / 'venv' / 'requirements.txt').touch()

    if (path / 'requirements.txt').exists():
        new_requirements = (path / 'requirements.txt').read_text()
        if (path / 'venv' / 'requirements.txt').read_text() != new_requirements:
            subprocess.run([str(path / 'venv' / 'Scripts' / 'pip.exe'), 'install', '-r', str(path / 'requirements.txt')], creationflags=subprocess.CREATE_NEW_CONSOLE)
            (path / 'venv' / 'requirements.txt').write_text(new_requirements)

    subprocess.run((str(path / 'venv' / 'Scripts' / ('python'+w+'.exe')),)+args[1:])

def test_activate():
    run('','-c','import sys;print(sys.executable)')

if __name__ == '__main__':
    run(*sys.argv)
