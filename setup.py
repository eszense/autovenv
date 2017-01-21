import sys
import bdist_msi
sys.modules['distutils.command.bdist_msi'] = bdist_msi

from distutils.core import setup

setup(
    name='autovenv',
    py_modules=['autovenv'],
    entry_points = {
        'console_scripts': ['pyv=autovenv:run'],
        'gui_scripts':['pywv=autovenv:runw']
    }
)
