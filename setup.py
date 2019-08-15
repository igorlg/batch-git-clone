# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

import re
from setuptools import setup

version = re.search(
    '^__version__ *= *\'(.*)\'',
    open('gitbatch/gitbatch.py').read(),
    re.M
).group(1)

with open('README.md', 'rb') as f:
    long_descr = f.read().decode('utf-8')

install_requires = ['joblib',
                    'PyYAML',
                    'termcolor',
                    'click',
                    ]

tests_requires = ['pytest',
                  ]

setup(
    name='gitbatch',
    packages=['gitbatch'],
    entry_points={
        'console_scripts': ['gitbatch = gitbatch.gitbatch:cli']
    },
    version=version,
    install_requires=install_requires,
    tests_require=tests_requires,
    description='Perform Batch Git operations based on Config file',
    long_description=long_descr,
    long_description_content_type='text/markdown',
    author='Igor Gentil',
    author_email='igor@devops.cool',
    url='https://github.com/igorlg/gitbatch/',
)
