#!/usr/bin/python
# coding: utf-8

# Copyright (c) 2016 Mountainstorm
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import unicode_literals, print_function
import argparse
from urllib2 import build_opener, URLError, HTTPError
import posixpath
import subprocess
import os

'''Simple script to download symbols from symbol server'''


def download_file(url, output):
    retval = None
    try:
        opener = build_opener()
        opener.addheaders = [('User-Agent', 'Microsoft-Symbol-Server/6.12.0002.633')]
        req = opener.open(url)
        try:
            uidname = posixpath.basename(posixpath.dirname(url))
            pdbname = posixpath.basename(posixpath.dirname(posixpath.dirname(url)))
            fn = os.path.join(
                output,
                pdbname,
                uidname,
                posixpath.basename(url)
            )
            os.makedirs(os.path.dirname(fn))
        except os.error:
            pass # dir exists
        with open(fn, 'wb') as symbol:
            symbol.write(req.read())
            retval = fn
    except (HTTPError, URLError) as e:
        pass
    return retval


def decompress_symbol(local):
    retval = None
    cmd = '7z'
    if os.path.exists('/Applications/Keka.app/Contents/Resources/keka7z'):
        cmd = '/Applications/Keka.app/Contents/Resources/keka7z'
    orig = os.getcwd()
    os.chdir(os.path.dirname(local))
    subprocess.call([cmd, 'e', os.path.basename(local)])
    os.chdir(orig)
    if os.path.exists(local[:-1] + 'b'):
        retval = local[:-1] + 'b'
        os.unlink(local)
    return retval


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrieves all avaliable symbol files [specified in he signature file]')
    parser.add_argument('signatures', help='the file of signatures to process')
    parser.add_argument('output', help='the folder to store downloaded symbols in')
    parser.add_argument(
        'symsvr',
        nargs='?',
        default='http://msdl.microsoft.com/download/symbols',
        help='the symbol server url; default Microsofts server'
    )
    args = parser.parse_args()

    symbols = set()
    # prevent downloading duplicates
    with open(args.signatures, 'rt') as f:
        for line in f:
            symbols.add(line.strip())
    # now process all the unique symbols
    for symbol_id in list(symbols):
        filename = symbol_id[:symbol_id.find('/')]
        # first try to get the uncompressed version
        url = posixpath.join(
            args.symsvr,
            symbol_id,
            filename
        )
        print('downloading: %s' % url)
        local = download_file(url, args.output)
        if local is None:
            # try to get the compressed version
            url = posixpath.join(
                args.symsvr,
                symbol_id,
                filename[:-1] + '_'
            )
            print('downloading: %s' % url)
            local = download_file(url, args.output)
            if local is not None:
                local = decompress_symbol(local)
        if local is None:
            print('failed to download')

