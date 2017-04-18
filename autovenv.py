import sys
import os
import pathlib
import venv
import subprocess
from subprocess import PIPE

def main():
    try:
       run()
       return 0
    except ParsingError as e:
        print(e.message, file=sys.stderr)
        return 1

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
        if not (path / 'autovenv.ini').exists():
            venv.create(str((path / 'venv').absolute()), clear=True, with_pip=True)
        else:
            from configparser import ConfigParser, ParsingError
            config = ConfigParser()
            try:
                config.read(str((path / 'autovenv.ini').absolute()))
            except ParsingError as e:
                raise e
            subenv = os.environ.copy()
            subenv['PY_PYTHON'] = config['defaults']['python']
            proc = subprocess.run( \
                    ('py', '-c', 'import venv,sys; venv.create(sys.argv[1], clear=True, with_pip=True)', str((path / 'venv').absolute())),\
                    stderr=subprocess.PIPE, stdout=subprocess.PIPE, env=subenv
                )
            

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
    main()
