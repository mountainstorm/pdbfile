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


from datastream import DataStream


class MsfDirectory(object):
    def __init__(self, reader, head, bits):
        self.streams = []
        pages = reader.pages_from_size(head.directory_size)

        # 0..n in page of directory pages.
        bits.min_capacity(head.directory_size)
        directory_root_pages = len(head.directory_root)
        pages_per_page = head.page_size / 4
        pages_to_go = pages
        for i in range(0, directory_root_pages):
            pages_in_this_page = pages_per_page
            if pages_to_go <= pages_per_page:
                pages_in_this_page = pages_to_go
            reader.seek(head.directory_root[i], 0);
            bits.append(reader.reader, pages_in_this_page * 4)
            pages_to_go -= pages_in_this_page
        bits.position = 0

        stream = DataStream(head.directory_size, bits, pages)
        bits.min_capacity(head.directory_size)
        stream.read(reader, bits)

        # 0..3 in directory pages
        count = bits.read_int32()

        # 4..n
        sizes = bits.read_int32(count)

        # n..m
        self.streams = []
        for i in range(0, count):
            if sizes[i] <= 0:
                self.streams.append(DataStream())
            else:
                self.streams.append(DataStream(
                    sizes[i], bits, reader.pages_from_size(sizes[i])
                ))
