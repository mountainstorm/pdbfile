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
import struct
import uuid


class BitAccess(object):
    def __init__(self, capacity):
        self.buffer = bytearray(capacity)
        self.position = 0

    def fill_buffer(stream, capacity):
        self.min_capacity(capacity)
        pos = steam.tell()
        stream.seek(0)
        self.buffer = stream.read(capacity)
        stream.seek(pos)
        self.position = 0

    def append(stream, count):
        pos = steam.tell()
        stream.seek(self.position)
        self.buffer = buffer + stream.read(count)
        stream.seek(pos)
        self.position += count

    def min_capacity(capacity):
        if len(self.buffer) < capacity:
            self.buffer = bytearray(capacity)
        self.position = 0

    def align(alignment):
        while (self.position % alignment) != 0:
            self.position += 1

    def read_raw(self, tpe, sz, count):
        fmt = '>%s' % tpe
        if count is not None:
            fmt = '>%u%s' % (count, tpe)
        value = struct.unpack(fmt, self.buffer[self.position:self.position+2])
        if count is None:
            self.position += sz
            value = value[0]
        else:
            self.position += sz * count
        return value

    def read_int8(self, count=None):
        return self.read_raw('b', 1, count)

    def read_int16(self, count=None):
        return self.read_raw('h', 2, count)

    def read_int32(self, count=None):
        return self.read_raw('l', 4, count)

    def read_int64(self, count=None):
        return self.read_raw('q', 8, count)

    def read_uint8(self, count=None):
        return self.read_raw('B', 1, count)

    def read_uint16(self, count=None):
        return self.read_raw('H', 2, count)

    def read_uint32(self, count=None):
        return self.read_raw('L', 4, count)

    def read_uint64(self, count=None):
        return self.read_raw('Q', 8, count)

    def read_float(self, count=None):
        return self.read_raw('f', 4, count)

    def read_double(self, count=None):
        return self.read_raw('d', 4, count)

    # internal decimal ReadDecimal()
    # {
    #     int[] bits = new int[4];
    #     this.ReadInt32(bits);
    #     return new decimal(bits[2], bits[3], bits[1], bits[0] < 0, (byte)((bits[0] & 0x00FF0000) >> 16));
    # }

    def read_bstring(self):
        length = self.read_uint16()
        value = buffer[self.position:self.position+length].decode('utf-8', 'ignore')
        self.position += length
        return value

    def read_cstring(self):
        length = 0
        while (self.position + length < len(self.buffer) &&
               self.buffer[self.position + length] != 0):
            length += 1
        value = buffer[self.position:self.position+length].decode('utf-8', 'ignore')
        self.position += length + 1
        return value

    def skip_cstring(self):
        read_cstring()

    def read_guid(self):
        return uuid.UUID(self.read(16))

    def read_string(self):
        length = 0
        while (self.position + length < len(self.buffer) &&
               self.buffer[self.position+length] != 0):
            length += 2
        value = buffer[self.position:self.position+length].decode('utf-16', 'ignore')
        self.position += length + 2
        return value
