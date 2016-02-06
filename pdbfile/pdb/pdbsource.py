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


class PdbSource(object):
    '''A source file in the program.'''

    def __init__(self, name, doctype, language, vendor, algorithm_id, checksum, source):
        self.name = name
        '''The name of the source file; unicode'''
        self.doctype = doctype
        '''The DocType for this source; guid'''
        self.language = language
        '''Pdb source language; guid'''
        self.vendor = vendor
        '''Pdb source vendor; guid'''
        self.algorithm_id = algorithm_id
        '''Pdb algorithm id; guid'''
        self.checksum = checksum
        '''Checksum for this pdb; bytearray'''
        self.source = source
        '''The embeded source in this pdb; bytearray'''
