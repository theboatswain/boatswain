from distutils.core import setup
from setuptools import find_packages

setup(name='boatswain',
      version='1.0.0',
      packages=find_packages(exclude=("venv*",)),
      install_requires=[
          'docker==4.0.2',
          'PyQt5==5.13.0',
          'peewee==3.9.6',
          'appdirs==1.4.3',
          'PyYAML==5.1.1',
          'requests'
      ],
      entry_points={
          'gui_scripts': [
              'boatswain = boatswain:main'
          ]},
      )
