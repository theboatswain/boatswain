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
          'boatswain_updater',
          'requests'
      ],
      author='Manh Tu VU',
      author_email='glmanhtu@gmail.com',
      package_data={
          '': ['*.svg']
      },
      classifiers=[
          "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.7",
      ],
      entry_points={
          'gui_scripts': [
              'boatswain = boatswain:main'
          ]},
      )
