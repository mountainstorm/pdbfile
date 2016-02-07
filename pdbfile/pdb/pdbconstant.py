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


class PdbConstant(object):
    '''This class represents a constant value in source code, such as: const int Foo = 3;'''

    def __init__(self, bits):
        self.name = None
        '''The variable name of the constant.'''
        self.value = 0
        '''The value of this constant'''
        self.token = bits.read_uint32()
        '''The metadata token of this constant.'''
        tag1 = bits.read_uint8()
        tag2 = bits.read_uint8()
        if tag2 == 0:
            self.value = tag1
        elif tag2 == 0x80:
            if tag1 == 0x00: # sbyte
                self.value = bits.read_uint8()
            elif tag1 == 0x01: # short
                self.value = bits.read_int16();
            elif tag1 == 0x02: # ushort
                self.value = bits.read_uint16()
            elif tag1 == 0x03: # int
                self.value = bits.read_int32()
            elif tag1 == 0x04: # uint
                self.value = bits.read_uint32()
            elif tag1 == 0x05: # float
                self.value = bits.read_float()
            elif tag1 == 0x06: # double
                self.value = bits.read_double()
            elif tag1 == 0x09: # long
                self.value = bits.read_int64()
            elif tag1 == 0x0a: # ulong
                self.value = bits.read_uint64()
            elif tag1 == 0x10: # string
                self.value = bits.read_bstring()
            elif tag1 == 0x19: # decimal
                self.value = bits.read_decimal()
            else:
                pass # TODO: error
        else:
            pass # TODO: error
        self.name = bits.read_cstring()
