# -*- coding: utf-8 -*-

import os
import sys

from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import setup

import status

if sys.version_info[0] == 2:
    from codecs import open


_requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
_REQUIRES = [str(r.req) for r in parse_requirements(_requirements_file, session=PipSession())]

_LONG_DESCRIPTION = open('README.rst', 'r', 'utf-8').read()
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
    license=status.__license__,
    zip_safe=False,
    keywords=_KEYWORDS,
    classifiers=_CLASSIFIERS,
)
