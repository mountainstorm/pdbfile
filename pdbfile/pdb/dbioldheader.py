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


class DbiOldHeader(object):
    def __init__(self, bits):
        self.sig = bits.read_int32()
        self.ver = bits.read_int32()
        self.age = bits.read_int32()
        self.gssym_stream = bits.read_int16()
        self.vers = None
        self.pssym_stream = bits.read_int16()
        self.pdbver = None
        self.symrec_stream = bits.read_int16()
        self.pdbver2 = None
        self.gpmodi_size = bits.read_int32()
        self.seccon_size = bits.read_int32()
        self.secmap_size = bits.read_int32()
        self.filinf_size = bits.read_int32()
        self.tsmap_size = 0
        self.mfcIndex = 0
        self.dbghdr_size = 0
        self.ecinfo_size = 0
        self.flags = 0
        self.machine = 0
        self.reserved = 0
