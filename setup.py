#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
      name='app_store',
      version=0.5,
      description="App Store for Vertica",
      author="Adam Seering",
      author_email="aseering@vertica.com",
      packages=find_packages(),
      install_requires=['django>=1.4',
                        'django-userena'],
)
