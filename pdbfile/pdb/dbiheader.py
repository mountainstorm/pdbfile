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


class DbiHeader(object):
    def __init__(self, bits):
        self.sig = bits.read_int32()          # 0..3
        self.ver = bits.read_int32()          # 4..7
        self.age = bits.read_int32()          # 8..11
        self.gssym_stream = bits.read_int16()  # 12..13
        self.vers = bits.read_uint16()        # 14..15
        self.pssym_stream = bits.read_int16()  # 16..17
        self.pdbver = bits.read_uint16()      # 18..19
        self.symrec_stream = bits.read_int16() # 20..21
        self.pdbver2 = bits.read_uint16()     # 22..23
        self.gpmodi_size = bits.read_int32()   # 24..27
        self.seccon_size = bits.read_int32()   # 28..31
        self.secmap_size = bits.read_int32()   # 32..35
        self.filinf_size = bits.read_int32()   # 36..39
        self.tsmap_size = bits.read_int32()    # 40..43
        self.mfcIndex = bits.read_int32()     # 44..47
        self.dbghdr_size = bits.read_int32()   # 48..51
        self.ecinfo_size = bits.read_int32()   # 52..55
        self.flags = bits.read_uint16()       # 56..57
        self.machine = bits.read_uint16()     # 58..59
        self.reserved = bits.read_int32()     # 60..63
