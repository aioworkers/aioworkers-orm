#!/usr/bin/env python

import pathlib

from setuptools import find_packages, setup

version = __import__('aioworkers_orm').__version__

requirements = [
    # 'aioworkers>=0.12.0',
    'orm',
]

test_requirements = [
    'pyyaml',
    'pytest',
    'pytest-runner',
    'pytest-aioworkers',
    'pytest-flake8',
    'flake8-isort',
]

readme = pathlib.Path('README.rst').read_text()


setup(
    name='aioworkers-orm',
    version=version,
    description='ORM for aioworkers',
    long_description=readme,
    author='Alexander Bogushov',
    author_email='abogushov@gmail.com',
    url='https://github.com/aioworkers/aioworkers-orm',
    packages=[
        i for i in find_packages()
        if i.startswith('aioworkers_orm')
    ],
    include_package_data=True,
    install_requires=requirements,
    license='Apache Software License 2.0',
    keywords='aioworkers',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
