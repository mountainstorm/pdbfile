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


from pdbexception import PdbException

class DataStream(object):
    def __init__(self, content_size=None, bits=None, count=None):
        if content_size is None and bits is None and count is None:
            self.content_size = 0
            self.pages = []
            return # default constructor
        self.content_size = content_size
        if count > 0:
            self.pages = bits.read_int32(count)

    def read(self, reader, position, bytedata=None, offset=None, data=None):
        if bytedata is None and offset is None and data is None:
            # called with 2 params
            bits = position
            bits.min_capacity(self.content_size)
            return self.read(reader, 0, bits.buffer, 0, self.content_size)
        # called with all
        if position + data > self.content_size:
            raise PdbException('DataStream can\'t read off end of stream. ' +
                               '(pos=%u,siz=%u)' % (position, data))
        if position == self.content_size:
            return
        left = data
        page = position / reader.page_size
        rema = position % reader.page_size

        # First get remained of first page.
        if rema != 0:
            todo = reader.page_size - rema
            if todo > left:
                todo = left
            reader.seek(self.pages[page], rema)
            reader.read(bytedata, offset, todo)
            offset += todo
            left -= todo
            page += 1

        # Now get the remaining pages.
        while left > 0:
            todo = reader.page_size
            if todo > left:
                todo = left
            reader.seek(self.pages[page], 0)
            reader.read(bytedata, offset, todo)
            offset += todo
            left -= todo
            page += 1

    def length(self):
        return self.content_size
