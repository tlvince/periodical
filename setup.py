#!/usr/bin/env python2

from distutils.core import setup

setup(
    name = 'periodical',
    description = 'Create a Kindle periodical from given URL(s)',
    version = '0.1.0',
    author = 'Tom Vincent',
    author_email = 'http://tlvince.com/contact/',
    url = 'https://github.com/tlvince/periodical',
    license = 'MIT',
    scripts = ['src/periodical.py'],
    classifiers = [
        'Programming Language :: Python :: 2',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Topic :: Office/Business',
        'Topic :: Text Processing :: Markup :: HTML',
    ]
)
