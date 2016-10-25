#/usr/bin/env python
import io
# import re
from setuptools import setup, find_packages


with io.open('README.rst', encoding='utf8') as readme:
    long_description = readme.read()


setup(
    name='django-simpleuser',
    version='0.1.0',
    description='A custom Django user model for best practices email-based login.',
    long_description=long_description,
    author='Russell Keith-Magee',
    author_email='russell@keith-magee.com',
    url='http://github.com/jambonsw/simpleuser/',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'django>=1.8'
    ],
    license='New BSD',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    test_suite='tests'
)