import sys
import os
import pathlib
import venv
import subprocess
from subprocess import PIPE

def runw(*args):
    run(*args, w=True)
def run(*args, w=False):
    if not args:
        args = sys.argv

    w = 'w' if w else ''
    path = pathlib.Path.cwd()

    while not (path / 'venv').exists():
        if(path.parent == path):
            subprocess.run(('py'+w,*args[1:]))
            return
        path = path.parent

    if not (path / 'venv' / 'Scripts' / ('python'+w+'.exe')).exists():
        venv.create(str((path / 'venv').absolute()), clear=True, with_pip=True)

    if (path / 'requirements.txt').exists():
        (path / 'venv' / 'requirements.txt').touch()
        new_requirements = (path / 'requirements.txt').read_text()
        if (path / 'venv' / 'requirements.txt').read_text() != new_requirements:
            proc = subprocess.run([str(path / 'venv' / 'Scripts' / 'pip.exe'), \
                'install', '-r', str(path / 'requirements.txt')], \
                stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            if proc.returncode != 0:
                print(proc.stderr.decode(), file=sys.stderr)
                return 1
            (path / 'venv' / 'requirements.txt').write_text(new_requirements)

    subprocess.run((str(path / 'venv' / 'Scripts' / ('python'+w+'.exe')),*args[1:]))

if __name__ == '__main__':
    run()
