#!/usr/bin/env python2
# Copyright 2012 Tom Vincent <http://tlvince.com/contact/>

'''Create a Kindle periodical from given URL(s).'''

import os
import sys
import logging
import argparse

from boilerpipe.extract import Extractor

def extract(urls):
    '''Extract content from a given URL.'''
    for url in urls:
        extractor = Extractor(extractor="ArticleExtractor", url=url)
        html = extractor.getHTML()
        print(html)

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
    extract(args.urls)

if __name__ == '__main__':
    main()
