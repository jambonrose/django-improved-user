#!/usr/bin/env python3
"""
====================
Django Improved User
====================

:website: https://github.com/jambonsw/django-improved-user/
:copyright: Copyright 2018 JamBon Software
:license: Simplified BSD, see LICENSE for details.
"""

from distutils.command.check import check as CheckCommand
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


LONG_DESCRIPTION = (
    load_file_contents('README.rst', as_list=False)
    .split('.. end-badges')[1]  # remove badge icons at top
    .lstrip()  # remove any extraneous spaces before title
)


class CustomCheckCommand(CheckCommand):
    """Customized distutils check command"""
    # https://github.com/python/cpython/blob/master/Lib/distutils/command/check.py
    user_options = CheckCommand.user_options + [
        ('disable-metadata', None, "don't check meta-data"),
        ('enforce-email', 'e', 'Ensure that all author/maintainer use email'),
    ]
    negative_opt = {'disable-metadata': 'metadata'}

    def initialize_options(self):
        """Setup superclass and new options"""
        super().initialize_options()
        self.enforce_email = 0  # pylint:disable=attribute-defined-outside-init

    def check_metadata(self):
        """
        Ensures that all required elements of meta-data are supplied.

        Specifically: name, version, URL, author or maintainer
        Warns if any are missing.

        If enforce-email option is true, author and/or maintainer must
        specify an email.

        """
        metadata = self.distribution.metadata

        missing = []
        for attr in ('name', 'version', 'url'):
            if not (hasattr(metadata, attr) and getattr(metadata, attr)):
                missing.append(attr)

        # https://www.python.org/dev/peps/pep-0345/
        # author or maintainer must be specified
        # author is preferred; if identifcal, specify only author
        if not metadata.author and not metadata.maintainer:
            missing.append('author')
            if self.enforce_email:
                missing.append('author_email')
        else:
            # one or both of author or maintainer specified
            if (metadata.author and self.enforce_email
                    and not metadata.author_email):
                missing.append('author_email')
            if (metadata.maintainer and self.enforce_email
                    and not metadata.maintainer_email):
                missing.append('maintainer_email')
            if (metadata.author and metadata.maintainer
                    and metadata.author == metadata.maintainer):
                self.warn(
                    'Maintainer should be omitted if identical to Author.\n'
                    'See https://www.python.org/dev/peps/pep-0345/'
                    '#maintainer-email-optional')
            if (metadata.author_email and metadata.maintainer_email
                    and metadata.author_email == metadata.maintainer_email):
                self.warn(
                    'Maintainer Email should be omitted if'
                    "identical to Author's.\n"
                    'See https://www.python.org/dev/peps/pep-0345/'
                    '#maintainer-email-optional')

        if missing:
            self.warn('missing required meta-data: %s' % ', '.join(missing))


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
        from runtests import (
            check_missing_migrations, configure_django, run_test_suite,
        )
        configure_django()
        check_missing_migrations()
        run_test_suite(*self.args)


setup(
    name='django-improved-user',
    version='1.0.0',
    description=(
        'A custom Django user model for best practices email-based login.'
    ),
    long_description=LONG_DESCRIPTION,
    url='https://github.com/jambonsw/django-improved-user/',

    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'django>=1.8,!=1.9.*,!=1.10.*',
    ],
    extras_require={
        'factory': [
            'factory_boy>=2.9',
            'Faker>=0.8',
            'python-dateutil>=2.6',
        ],
    },
    zip_safe=False,

    cmdclass={
        'check': CustomCheckCommand,
        'test': CustomTestCommand,
    },

    author=(
        'Russell Keith-Magee, '
        'Andrew Pinkham'
    ),
    license='BSD License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
    ],
)
