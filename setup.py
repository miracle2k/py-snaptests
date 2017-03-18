#!/usr/bin/env python
# coding: utf8
import os
from setuptools import setup, find_packages


setup(
    name = 'snaptest',
    version = "0.1",
    description = 'Snapshot testing w/ Python.',
    author = 'Michael Elsdörfer',
    author_email = 'michael@elsdoerfer.com',
    license = 'BSD',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
        ],
    packages=find_packages(exclude=('tests',))
)