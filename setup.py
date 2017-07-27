#!/usr/bin/env python3
"""
====================
Django Improved User
====================

:website: https://github.com/jambonsw/django-improved-user/
:copyright: Copyright 2017 JamBon Software
:license: Simplified BSD, see LICENSE for details.
"""

from operator import attrgetter
from os.path import abspath, dirname, join

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

HERE = abspath(dirname(__file__))


def load_file_contents(file_path, as_list=True):
    """Load file as string or list"""
    abs_file_path = join(HERE, file_path)
    with open(abs_file_path, encoding='utf-8') as file_pointer:
        if as_list:
            return file_pointer.read().splitlines()
        return file_pointer.read()


LONG_DESCRIPTION = load_file_contents('README.rst', as_list=False)


class CustomTestCommand(TestCommand):
    """Customized setuptools test command"""
    # https://github.com/pypa/setuptools/blob/master/setuptools/command/test.py
    # https://github.com/python/cpython/blob/master/Lib/distutils/cmd.py
    description = 'run project tests'
    command_consumes_arguments = True
    user_options = []

    def initialize_options(self):
        """Explicitly set all instance vars"""
        self.args = []  # pylint: disable=attribute-defined-outside-init

    def finalize_options(self):
        """Needed by Superclass"""
        pass

    def run(self):
        installed_dists = self.install_dists(self.distribution)

        if self.dry_run:
            self.announce('skipping tests (dry run)')
            return

        paths = map(attrgetter('location'), installed_dists)
        with self.paths_on_pythonpath(paths):
            with self.project_on_sys_path():
                self.run_tests()

    def run_tests(self):
        from runtests import run_test_suite
        run_test_suite(*self.args)


setup(
    name='django-improved-user',
    version='0.1.1',
    description=(
        'A custom Django user model for best practices email-based login.'
    ),
    long_description=LONG_DESCRIPTION,
    url='https://github.com/jambonsw/django-improved-user/',

    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'django>=1.8',
    ],
    zip_safe=False,

    cmdclass={
        'test': CustomTestCommand,
    },

    author=(
        'Russell Keith-Magee, '
        'Andrew Pinkham',
    ),
    license='Simplified BSD License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
    ],
)
