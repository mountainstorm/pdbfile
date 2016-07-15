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


class PdbSequencePoint(object):
    '''Represents a sequence point (multiple lines) in a source file.'''

    def __init__(self, offset, line_begin, col_begin, line_end, col_end):
        self.offset = offset
        '''The IL offset of this line; uint'''
        self.line_begin = line_begin
        '''The first line of this sequence point; uint'''
        self.col_begin = col_begin
        '''The first column of the first line of this sequence point; ushort'''
        self.line_end = line_end
        '''The last line of this sequence point; uint'''
        self.col_end = col_end
        '''The last column of the last line of this sequence point; ushort'''

    def __str__(self):
        if self.line_begin == self.line_end:
            return 'iloffs: %u line: %u' % (self.offset, self.line_begin)
        return 'iloffs: %u lines: %u-%u' % (self.offset, self.line_begin, self.line_end)
