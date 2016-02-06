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


class DbiSecCon(object):
    def __init__(self, bits):
        self.section = bits.read_int16()      # 0..1
        self.pad1 = bits.read_int16()         # 2..3
        self.offset = bits.read_int32()       # 4..7
        self.size = bits.read_int32()         # 8..11
        self.flags = bits.read_uint32()       # 12..15
        self.module = bits.read_int16()       # 16..17
        self.pad2 = bits.read_int16()         # 18..19
        self.data_crc = bits.read_uint32()    # 20..23
        self.reloc_crc = bits.read_uint32()   # 24..27
        #if pad1 != 0 || pad2 != 0:
        #  raise PdbException('Invalid DBI section. ' +
        #                     '(pad1=%u, pad2=%u)' % (self.pad1, self.pad2))
