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
from cvinfo import AttrSlotSym


class PdbSlot(object):
    '''The representation of a local variable slot.'''

    def __init__(self, bits, typind):
        AttrSlotSym slot

        slot.index = bits.read_uint32()
        slot.typind = bits.read_uint32()
        slot.off_cod = bits.read_uint32()
        slot.seg_cod = bits.read_uint16()
        slot.flags = bits.read_uint16()
        slot.name = bits.read_cstring()

        self.slot = slot.index
        '''The slot number; int'''
        self.name = slot.name
        '''The name of this variable slot; unicode'''
        self.flags = slot.flags
        '''The flags associated with this slot; ushort'''
        typind[0] = slot.typind
