#/usr/bin/env python
import io
# import re
from setuptools import setup, find_packages


with io.open('README.rst', encoding='utf8') as readme:
    long_description = readme.read()


setup(
    name='django-improved-user',
    version='0.1.1',
    description='A custom Django user model for best practices email-based login.',
    long_description=long_description,
    author=(
        'Russell Keith-Magee <russell at keith-magee dot com>, '
        'Andrew Pinkham <hello at andrewsforge dot com>',
    ),
    url='https://github.com/jambonsw/django-improved-user/',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'django>=1.8'
    ],
    license='Simplified BSD License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    test_suite='tests'
)
