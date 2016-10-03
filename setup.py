# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import sys

from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import setup, Command

import status

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] == 2:
    from codecs import open


class Gulp(Command):
    description = 'Run gulp'
    user_options = [
        ('task=', 't', 'gulp task')
    ]

    def initialize_options(self):
        self.task = 'dist'

    def finalize_options(self):
        pass

    def run(self):
        subprocess.call(['gulp', self.task])


class Dist(Command):
    description = 'Generate static files and create dist package'
    user_options = [
        ('clean', 'c', 'clean dist directories before build (default: false)')
    ]
    boolean_options = ['clean']

    def initialize_options(self):
        self.clean = False

    def finalize_options(self):
        pass

    def run(self):
        if self.clean:
            shutil.rmtree('build', ignore_errors=True)
            shutil.rmtree('dist', ignore_errors=True)
            shutil.rmtree('django_status.egg-info', ignore_errors=True)

        self.run_command('gulp')
        self.run_command('sdist')
        self.run_command('bdist_wheel')

# Read requirements
_requirements_file = os.path.join(BASE_DIR, 'requirements.txt')
_REQUIRES = [str(r.req) for r in parse_requirements(_requirements_file, session=PipSession())]

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
    'status',
    'check'
])

setup(
    name='django-status',
    version=status.__version__,
    description=status.__description__,
    long_description=_LONG_DESCRIPTION,
    author=status.__author__,
    author_email=status.__email__,
    maintainer=status.__author__,
    maintainer_email=status.__email__,
    url=status.__url__,
    download_url=status.__url__,
    packages=[
        'status',
    ],
    include_package_data=True,
    install_requires=_REQUIRES,
    extras_require={
        'dev': [
            'setuptools',
            'pip',
            'wheel',
            'prospector'
        ]
    },
    license=status.__license__,
    zip_safe=False,
    keywords=_KEYWORDS,
    classifiers=_CLASSIFIERS,
    cmdclass={
        'gulp': Gulp,
        'dist': Dist,
    },
)
