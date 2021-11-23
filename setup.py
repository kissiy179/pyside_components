import sys
from glob import glob
from os.path import basename
from os.path import splitext
from os.path import exists
from setuptools import setup
from setuptools import find_packages

# List of packages to ignore.
# Pre-installed in Maya, etc.
IGNORE_PACKAGES = ['PySide', 'PySide2']

# Is the Python running in Maya?
IS_MAYA_PYTHON = 'maya' in sys.prefix.lower()

def _requires_from_file(filename):
    if not exists(filename):
        return []

    requires = {}
    
    with open(filename, 'r') as f:
        lines = f.readlines()

        for line in lines:
            line = line.strip('\n')
            package_name = line.split(' ')[0]

            if IS_MAYA_PYTHON and package_name in IGNORE_PACKAGES:
                continue

            requires[line] = line

    return list(requires.keys())

def get_requires():
    requires = []
    
    if sys.version[0] == '2':
        requires_name = 'requirements2.txt'

    if not requires:
        requires_name = 'requirements.txt'

        requires = _requires_from_file(requires_name)

    return requires

setup(
    name='pyside_components',
    version='0.1.0',
    package_dir={"": "python"},
    packages=find_packages("python"),
    py_modules=[splitext(basename(path))[0] for path in glob('python/*.py')],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=2.7",
    install_requires=get_requires(),
)
