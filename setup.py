# -*- coding: utf-8 -*-

import sys
import os

from setuptools import setup
from setuptools.command.test import test as TestCommand
from pip.req import parse_requirements
from pip.download import PipSession

if sys.version_info[0] == 2:
    from codecs import open

import status

requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
requires = [str(r.req) for r in parse_requirements(requirements_file, session=PipSession())]

class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = ''

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        import shlex
        errno = tox.cmdline(args=shlex.split(self.tox_args))
        sys.exit(errno)


setup(
    name='django-status',
    version=status.__version__,
    description=status.__description__,
    long_description='\n'.join([open('README.rst', encoding='utf_8').read(),
                                open('CHANGELOG', encoding='utf_8').read()]),
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
    install_requires=requires,
    license=open('LICENSE', encoding='utf_8').read(),
    zip_safe=False,
    keywords='python, django, database, cache, celery, status, check',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite='tests',
    tests_require=['tox'],
    cmdclass={'test': Tox},
)

