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


class DbiModuleInfo(object):
    def __init__(self, bits, read_strings):
        self.opened = bits.read_int32()              # 0..3
        DbiSecCon(bits)                              # 4..31
        self.flags = bits.read_uint16()              # 32..33
        self.stream = bits.read_int16()              # 34..35
        self.cb_Syms = bits.read_int32()             # 36..39
        self.cb_old_lines = bits.read_int32()        # 40..43
        self.cb_lines = bits.read_int32()            # 44..57
        self.files = bits.read_int16()               # 48..49
        self.pad1 = bits.read_int16()                # 50..51
        self.offsets = bits.read_uint32()
        self.ni_source = bits.read_int32()
        self.ni_compiler = bits.read_int32()
        if read_strings:
            self.module_name = bits.read_cstring()
            self.object_name = bits.read_cstring()
        else:
            bits.skip_cstring()
            bits.skip_cstring()
        bits.align(4)
        #if opened != 0 || pad1 != 0:
        #raise PdbException('Invalid DBI module. ' +
        #                   '(opened=%u, pad=%u)' % (self.opened, self.pad1))

    def __str__(self):
        return moduleName
