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
from pdbfile.pdbfile import PDB
import traceback
import hashlib
import json
import os

'''Script to extract data from PDB and validate it against stored version'''


def pdb_info(path):
    print(path.lower()[path.find('/')+1:])
    try:
        pdb = PDB(path)
        # XXX: create json from pdb
    except:
        print(traceback.format_exc())
    return {}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extracts info from pdbs and checks it against the last run')
    parser.add_argument('root', help='the root folder of your symbol store')
    parser.add_argument(
        '--generate',
        default=False,
        action='store_true',
        help='generate the exemplar'
    )
    args = parser.parse_args()

    for root, dirs, files in os.walk(args.root):
        for fn in files:
            path = os.path.join(root, fn)
            ext = os.path.splitext(path)[1]
            if ext == '.pdb':
                exemplar = os.path.splitext(path)[0] + '.json'
                info = pdb_info(path)
                if args.generate is True:
                    if os.path.exists(exemplar):
                        os.unlink(exemplar)
                    # generate new exemplar
                    with open(exemplar, 'wt') as f:
                        json.dump(info, f, indent=4, sort_keys=True)
                        print('generating exemplar: %s' % path)
                elif os.path.exists(exemplar):
                    # read exemplar and compare them
                    h = hashlib.sha256()
                    h.update(json.dumps(info, indent=4, sort_keys=True))
                    infohash = h.hexdigest()

                    h = hashlib.sha256()
                    with open(exemplar, 'rt') as f:
                        h.update(f.read())
                        exemplarhash = h.hexdigest()
                    print('checking: [%s] %s' % (
                        'pass' if infohash == exemplarhash else 'fail',
                        path
                    ))
                else:
                    print('exemplar missing: %s' % path)
