#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements_install = [
    'click>=6.0'
    ]

requirements_test = [
    'click>=6.0',
    'Sphinx>=1.4.1',
    'sphinx_rtd_theme>=0.1.0',
    'jinja2>=2.8',
    'pip>=8.0',
    'wheel>=0.27',
    'flake8>=2.0',
    'tox>=2.3.0',
    'coverage>=4.0',
    'pytest>=3.0',
    'pytest_cov>=2.0',
    'pytest-runner>=2.5'
    ]

extras = {
    'test': requirements_test
}

setup(
    name='clatter',
    version='0.0.3',
    description="A Doctest-stype Command Line Application Tester",
    long_description=readme,
    author="Michael Delgado",
    url='https://github.com/delgadom/clatter',
    packages=find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests', 'docs', 'examples']),
    package_dir={'clatter':
                 'clatter'},
    include_package_data=True,
    install_requires=requirements_install,
    license="MIT license",
    zip_safe=False,
    keywords='clatter',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    test_suite='tests',
    setup_requires=['pytest-runner'],
    tests_require=requirements_test,
    extras_require=extras
)
