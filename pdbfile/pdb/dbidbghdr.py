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


class DbiDbgHdr(object):
    def __init__(self, bits):
        self.sn_fpo = bits.read_uint16()               # 0..1
        self.sn_exception = bits.read_uint16()         # 2..3 (deprecated)
        self.sn_fixup = bits.read_uint16()             # 4..5
        self.sn_omap_to_src = bits.read_uint16()       # 6..7
        self.sn_omap_from_src = bits.read_uint16()     # 8..9
        self.sn_section_hdr = bits.read_uint16()       # 10..11
        self.sn_token_rid_map = bits.read_uint16()     # 12..13
        self.sn_xdata = bits.read_uint16()             # 14..15
        self.sn_pdata = bits.read_uint16()             # 16..17
        self.sn_new_fpo = bits.read_uint16()           # 18..19
        self.sn_section_hdr_orig = bits.read_uint16()  # 20..21
