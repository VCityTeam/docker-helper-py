#!/usr/bin/env python

import codecs
import os

from setuptools import find_packages
from setuptools import setup

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

requirements = [
    'docker >= 4.3.0',
    'requests >= 2.24.0'
]

version = None
exec(open('docker_helper/version.py').read())

long_description = ''
with codecs.open('./README.md', encoding='utf-8') as readme_md:
    long_description = readme_md.read()

setup(
    name="docker_helper",
    version=version,
    description="A tiny syntactic sugar icing on top the Docker Engine API.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/VCityTeam/docker-helper-py',
    project_urls={
        'Source': 'https://github.com/VCityTeam/docker-helper-py',
        'Tracker': 'https://github.com/VCityTeam/docker-helper-py/issues',
    },
    packages=find_packages(exclude=["tests.*", "tests"]),
    install_requires=requirements,
    python_requires='>=3.7',
    zip_safe=False,
    classifiers=[
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    maintainer='vcity_devel',
    maintainer_email='vcity@liris.cnrs.fr',
)
