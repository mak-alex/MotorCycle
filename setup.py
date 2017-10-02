#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name     = 'MotorCycle',
    version  = '0.1.0',
    packages = find_packages(),
    requires = ['python (>= 2.5)'],
    description  = 'Script for downloading PDF files from website carlsalter',
    long_description = open('Readme.md').read(),
    author       = 'Alexandr Mikhailenko a.k.a Alex M.A.K.',
    author_email = 'alex-m.a.k@yandex.kz',
    url          = 'https://github.com/mak-alex/MotorCycle',
    download_url = 'https://github.com/mak-alex/MotorCycle/archive/master.zip',
    license      = 'GPL3 License',
    keywords     = [
        'MotorCycle', 'carlsalter', 'pdf', 'MotorCycle PDF'
    ],
    install_requires=[
        'paramiko',
        'dropbox',
        'requests==2.17.1',
        'lxml'
    ],
    test_suite='tests.test_motorcycle',
)

