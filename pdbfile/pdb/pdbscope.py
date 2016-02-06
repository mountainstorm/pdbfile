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


from pdbslot import PdbSlot
from pdbconstant import PdbConstant


class PdbScope(object):
    '''Represents a scope within a function or class.'''

    def __init__(self, address, length, slots, constants, used_namespaces):
        self.constants = constants
        '''A list of constants defined in this scope; PdbConstant[]'''
        self.slots = slots
        '''A list of variable slots in this function; PdbSlot[]'''
        self.scopes = [PdbScope()]
        '''A list of sub-scopes within this scope; PdbScope[]'''
        self.used_namespaces = used_namespaces
        '''A list of namespaces used in this scope; unicode[]'''
        self.address = address
        '''The address of this scope; uint'''
        self.offset = 0
        '''The IL offset of this scope; uint'''
        self.length = length
        '''The length of this scope; uint'''
        self.typind = 0

    @classmethod
    def PdbScope(cls, func_offset, block, bits):
        '''Creates a PdbScope object
           * func_offset; uint
           * block; BlockSym32
           * bits; BitAccess
           * typind; [uint]'''
        self = PdbScope(block.off, block.length, None, None, None)
        self.offset = block.off - func_offset

        constants = []
        scopes = []
        slots = []
        used_namespaces = []

        while bits.position < block.end:
            siz = bits.read_uint16()
            star = bits.position
            stop = bits.position + siz
            bits.position = star
            rec = bits.read_uint16()

            if rec == SYM.S_BLOCK32:
                sub = BlockSym32()

                sub.parent = bits.read_uint32()
                sub.end = bits.read_uint32()
                sub.length = bits.read_uint32()
                sub.off = bits.read_uint32()
                sub.seg = bits.read_uint16()
                sub.name = bits.skip_cstring()

                bits.position = stop
                scopes.append(PdbScope(func_offset, sub, bits))
                self.typind = scopes[-1].typind
            elif rec == SYM.S_MANSLOT:
                slots.append(PdbSlot(bits))
                self.typind = slots[-1].typind
                bits.position = stop
            elif rec == SYM.S_UNAMESPACE:
                used_namespaces.append(bits.read_cstring())
                bits.position = stop
            elif rec == SYM.S_END:
                bits.position = stop
            elif rec == SYM.S_MANCONSTANT:
                constants.append(PdbConstant(bits))
                bits.position = stop
            else:
                #raise PdbException('Unknown SYM in scope %u", rec)
                bits.position = stop

        if bits.position != block.end:
            raise Exception('Not at S_END')

        bits.read_uint16() # esiz
        erec = bits.read_uint16()
        if erec != SYM.S_END:
            raise Exception('Missing S_END')
