#!/usr/bin/env python
#coding:utf-8
import os
from lux2ev import *
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, 'README.md')).read()
except:
    README = 'https://github.com/EasyCam/LUX2EV/blob/main/README.md'

    


setup(name='LUX2EV',
      version= version,
      description='A very easy-to-use small software that uses the lux value measured by the illuminance meter to calculate the shutter speed under different ISO and aperture, and assist photography.',
      longdescription=README,
      author='EasyCam',
      author_email='hopephoto@outlook.com',
      url='https://github.com/EasyCam/LUX2EV/',
      packages=['lux2ev'],
      package_data={
          'lux2ev': ['*.py','*.png','*.qm','*.ttf','*.ini','*.md'],
      },
      include_package_data=True,

      install_requires=[
                        'PyQt6',
                         ],
     )