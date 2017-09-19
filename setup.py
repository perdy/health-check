# -*- coding: utf-8 -*-

import os
import sys

from pip.download import PipSession
from pip.req import parse_requirements as requirements
from setuptools import setup

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] == 2:
    from codecs import open


def parse_requirements(req_file):
    return [str(req.req) for req in requirements(req_file, session=PipSession())]


# Read requirements
_requirements_file = os.path.join(BASE_DIR, 'requirements.txt')
_tests_requirements_file = os.path.join(BASE_DIR, 'requirements-tests.txt')
_REQUIRES = parse_requirements(_requirements_file)
_TESTS_REQUIRES = parse_requirements(_tests_requirements_file)

# Read description
with open(os.path.join(BASE_DIR, 'README.rst'), encoding='utf-8') as f:
    _LONG_DESCRIPTION = f.read()

_CLASSIFIERS = (
    'Development Status :: 5 - Production/Stable',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Natural Language :: English',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules',
)
_KEYWORDS = ' '.join([
    'python',
    'django',
    'database',
    'cache',
    'celery',
    'health',
    'check'
])

setup(
    name='health-check',
    version='3.1.2',
    description='Health Check is an application that provides an API to check the health health_check of some parts '
                'and some utilities like ping requests. This application can works as standalone or included in a '
                'Django project.',
    long_description=_LONG_DESCRIPTION,
    author='José Antonio Perdiguero López',
    author_email='perdy.hh@gmail.com',
    maintainer='José Antonio Perdiguero López',
    maintainer_email='perdy.hh@gmail.com',
    url='https://github.com/PeRDy/health-check',
    download_url='https://github.com/PeRDy/health-check',
    packages=[
        'health_check',
    ],
    include_package_data=True,
    install_requires=_REQUIRES,
    tests_require=_TESTS_REQUIRES,
    extras_require={
        'dev': [
            'setuptools',
            'pip',
            'wheel',
            'twine',
            'bumpversion',
            'pre-commit',
        ] + _TESTS_REQUIRES
    },
    license='GPLv3',
    zip_safe=False,
    keywords=_KEYWORDS,
    classifiers=_CLASSIFIERS,
    entry_points={
        'console_scripts': [
            'health_check = health_check.__main__:main',
        ],
    }
)
