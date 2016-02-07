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
from pefile import PE, PEFormatError
from pdbfile.pedebugdata import PEDebugData, PEMissingDebugDataError
import os

'''Simple script to parse pe files in a directory and extract the PDB signatures'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process the specified directory, extracting PDB signatures from any PE files')
    parser.add_argument('root', help='the root folder to search from')
    args = parser.parse_args()

    for root, dirs, files in os.walk(args.root):
        for fn in files:
            try:
                pe = PE(os.path.join(root, fn), fast_load=True)
                print(PEDebugData.symbol_id(pe))
            except PEFormatError:
                pass # not a pe file
            except PEMissingDebugDataError:
                pass
