#!/usr/bin/env python2
# Copyright 2012 Tom Vincent <http://tlvince.com/contact/>

'''Create a Kindle periodical from given URL(s).'''

import os
import sys
import shutil
import logging
import argparse
import tempfile
import datetime
import subprocess

import yaml

from urlparse import urlparse

from bs4 import BeautifulSoup
from boilerpipe.extract import Extractor

def extract(url):
    '''Extract content from a given URL.'''
    # Using python-boilerpipe
    extractor = Extractor(extractor='ArticleExtractor', url=url)
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

def write_yaml(title, author, subject, out_path):
    '''Write document YAML for kindlerb.'''
    date = datetime.datetime.now()
    mobi = '{0}-{1}.mobi'.format(title.lower(),
                                 date.strftime('%Y%m%d%H%M%S'))
    doc = {
        'doc_uuid':     '{0}-{1}'.format(title.lower(),
                                         date.strftime('%Y%m%d%H%M%S')),
        'title':        '{0} {1}'.format(title, date.strftime('%Y-%m-%d')),
        'author':       author,
        'publisher':    author,
        'subject':      subject,
        'date':         date.strftime('%Y-%m-%d'),
        'mobi_outfile': mobi,
    }

    with open(os.path.join(out_path, '_document.yml'), 'w') as out:
        yaml.dump(doc, out)

    return mobi

def write_html(out_path, html, subject, count):
    '''Generate stripped HTML file for the given URL.'''
    section = os.path.join(out_path, 'sections', str(count))
    os.makedirs(section)
    html_path = os.path.join(section, '{0}.html'.format(count))
    with open(os.path.join(section, '_section.txt'), 'w') as section_file:
        section_file.write(subject)
    with open(html_path, 'w') as html_file:
        html_file.write(html.encode('utf8'))

def parse_args():
    '''Parse the command-line arguments.'''
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('urls', nargs='+', help='the URL(s) to parse')
    parser.add_argument('--outdir', default='~',
        help='directory to write mobi file')

    meta = parser.add_argument_group('meta', description='Periodical meta data')
    meta.add_argument('--title', default='Periodical',
        help='the periodical title')
    meta.add_argument('--author', default='Tom Vincent',
        help='the periodical author')
    meta.add_argument('--subject', default='News',
        help='the periodical subject')

    return parser.parse_args()

def which(cmd):
    '''Check if a command is in $PATH
    From: http://stackoverflow.com/q/377017
    '''

    def is_exe(fpath):
        '''Helper to check if file is executable.'''
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, _ = os.path.split(cmd)
    if fpath:
        if is_exe(cmd):
            return cmd
    else:
        for path in os.environ['PATH'].split(os.pathsep):
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

def extract_urls(urls, out_path, subject):
    '''Extract html from the given list of urls.'''
    for index, url in enumerate(urls):
        html = extract(url)
        formatted = format_boilerpipe(html, url)
        write_html(out_path, formatted, subject, index)

def generate(out_path):
    '''Generate the periodical.'''
    if os.path.exists(os.path.join(out_path, 'sections', '0', '0.html')):
        subprocess.call(['kindlerb', out_path])

def clean_up(tmp, mobi_file, outdir):
    '''Clean temporary directory and move resulting mobi file.'''
    mobi_path = os.path.join(tmp, mobi_file)
    if os.path.exists(mobi_path):
        outdir = os.path.expanduser(os.path.expandvars(outdir))
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        shutil.move(mobi_path, outdir)
    else:
        logging.error('periodical creation failed')
    shutil.rmtree(tmp)

def main():
    '''Start execution of periodicals.py.'''
    args = parse_args()
    logging.basicConfig(format='%(filename)s: %(levelname)s: %(message)s',
                        level=logging.INFO)
    have_depends()

    tmp = tempfile.mkdtemp()
    mobi = write_yaml(args.title, args.author, args.subject, tmp)

    extract_urls(args.urls, tmp, args.subject)
    generate(tmp)
    clean_up(tmp, mobi, args.outdir)

if __name__ == '__main__':
    main()
