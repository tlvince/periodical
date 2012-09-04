#!/usr/bin/env python2
# Copyright 2012 Tom Vincent <http://tlvince.com/contact/>

'''Create a Kindle periodical from given URL(s).'''

import os
import sys
import logging
import argparse

from urlparse import urlparse

from bs4 import BeautifulSoup
from boilerpipe.extract import Extractor

def extract(url):
    '''Extract content from a given URL.'''
    # Using python-boilerpipe
    extractor = Extractor(extractor="ArticleExtractor", url=url)
    return extractor.getHTML()

def format_boilerpipe(html, url):
    '''Return a formatted version of boilerpipe's HTML output.'''
    soup = BeautifulSoup(html)

    style = soup.style.extract()
    head = soup.new_tag('head')

    title = soup.new_tag('title')
    title.string = getattr(soup.h1, 'string', urlparse(url)[1])

    meta = soup.new_tag('meta')
    meta['http-equiv'] = 'Content-Type'
    meta['content'] = 'text/html; charset=UTF-8'

    head.append(title)
    head.append(meta)
    head.append(style)
    soup.body.insert_before(head)

    return soup

def parse_args():
    '''Parse the command-line arguments.'''
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('urls', nargs='+', help='the URL(s) to parse')
    return parser.parse_args()

def which(cmd):
    '''Check if a command is in $PATH.
    From: http://stackoverflow.com/q/377017'''

    def is_exe(fpath):
        '''Helper to check if file is executable.'''
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, _ = os.path.split(cmd)
    if fpath:
        if is_exe(cmd):
            return cmd
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, cmd)
            if is_exe(exe_file):
                return exe_file

    return None

def have_depends():
    '''Exit if required dependencies are not found.'''
    deps = ['kindlerb']

    for dep in deps:
        if which(dep) is None:
            logging.error("Dependency '{0}' not installed".format(dep))
            sys.exit(1)

def main():
    '''Start execution of periodicals.py.'''
    args = parse_args()
    logging.basicConfig(format="%(filename)s: %(levelname)s: %(message)s")
    have_depends()

    for url in args.urls:
        html = extract(url)
        formatted = format_boilerpipe(html, url)

if __name__ == '__main__':
    main()
