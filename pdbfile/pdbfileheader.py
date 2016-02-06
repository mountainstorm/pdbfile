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
import os


# 0x4D, 0x69, 0x63, 0x72, 0x6F, 0x73, 0x6F, 0x66, // "Microsof"
# 0x74, 0x20, 0x43, 0x2F, 0x43, 0x2B, 0x2B, 0x20, // "t C/C++ "
# 0x4D, 0x53, 0x46, 0x20, 0x37, 0x2E, 0x30, 0x30, // "MSF 7.00"
# 0x0D, 0x0A, 0x1A, 0x44, 0x53, 0x00, 0x00, 0x00  // "^^^DS^^^"


class PdbFileHeader(object):
    def __init__(self, reader, bits):
        bits.min_capacity(56)
        reader.seek(0)
        bits.fill_buffer(reader, 52)

        self.magic = bytearray(32)
        bits.read_bytes(self.magic)                 #   0..31
        self.page_size = bits.read_int32()          #  32..35
        self.free_pagemap = bits.read_int32()       #  36..39
        self.pages_used = bits.read_int32()         #  40..43
        self.directory_size = bits.read_int32()     #  44..47
        self.zero = bits.read_int32()               #  48..51

        directory_pages = (
            ((((self.directory_size + self.page_size - 1) / self.page_size) *
            4) + self.page_size - 1) / self.page_size
        )
        bits.fill_buffer(reader, directory_pages * 4)
        this.directory_root = bits.read_int32(directory_pages)
