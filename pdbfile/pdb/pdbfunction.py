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


import uuid
from pdbdebugexception import PdbDebugException
from pdbscope import PdbScope
from pdbslot import PdbSlot
from pdbconstant import PdbConstant


class PdbFunction(object):
    '''Represents a single function in a module.'''

    msilMetaData = uuid.uuid(0xc6ea3fc9, 0x59b3, 0x49d6, 0xbc, 0x25, 0x09, 0x02, 0xbb, 0xab, 0xb4, 0x60)

    @classmethod
    def by_address(cls, fx, fy):
        if fx.segment < fy.segment:
            return -1
        elif fx.segment > fy.segment:
            return 1
        elif fx.address < fy.address:
            return -1
        elif fx.address > fy.address:
            return 1
        else:
            return 0

    @classmethod
    def by_address_and_token(self, fx, fy):
        if fx.segment < fy.segment:
            return -1
        elif fx.segment > fy.segment:
            return 1
        elif fx.address < fy.address:
            return -1
        elif fx.address > fy.address:
            return 1
        else:
            if fx.token < fy.token:
                return -1
            elif fx.token > fy.token:
                return 1
            else:
                return 0

    @classmethod
    def strip_namespace(cls, module):
        li = module.rfind('.')
        if li > 0:
            return module[:li + 1]
        return module

    @classmethod
    def load_managed_functions(cls, bits, limit, read_strings):
        #mod = Pdbfunction.strip_namespace(module)
        begin = bits.position
        count = 0
        while bits.position < limit:
            siz = bits.read_uint16()
            star = bits.position
            stop = bits.position + siz
            bits.position = star
            rec = bits.read_uint16()
            if rec == SYM.S_GMANPROC or rec == SYM.S_LMANPROC:
                proc = ManProcSym()
                proc.parent = bits.read_uint32()
                proc.end = bits.read_uint32()
                bits.position = proc.end
                count += 1
            elif rec == SYM.S_END:
                bits.position = stop
            else:
                #print('%u: %u %y' %(bits.position, rec, rec))
                bits.position = stop
        if count == 0:
            return None

        bits.position = begin
        funcs = []
        while bits.position < limit:
            siz = bits.read_uint16()
            star = bits.position
            stop = bits.position + siz
            rec = bits.read_uint16()
            if rec == SYM.S_GMANPROC or rec == SYM.S_LMANPROC:
                proc = ManProcSym()
                #offset = bits.position
                proc.parent = bits.read_uint32()
                proc.end = bits.read_uint32()
                proc.next = bits.read_uint32()
                proc.length = bits.read_uint32()
                proc.dbg_start = bits.read_uint32()
                proc.dbg_end = bits.read_uint32()
                proc.token = bits.read_uint32()
                proc.off = bits.read_uint32()
                proc.seg = bits.read_uint16()
                proc.flags = bits.read_uint8()
                proc.ret_reg = bits.read_uint16()
                if read_strings:
                    proc.name = bits.read_cstring()
                else:
                    proc.name = bits.skip_cstring()
                #print('token=%08x [%s::%s]" % (proc.token, module, proc.name))
                bits.position = stop
                funcs.append(PdbFunction(proc, bits))
            else:
                #raise PdbDebugException('Unknown SYMREC %u" % rec)
                bits.position = stop
        return funcs


    @classmethod
    def count_scopes_and_slots(cls, bits, limit):
        pos = bits.position
        block = BlockSym32()
        constants = 0
        slots = 0
        scopes = 0
        used_namespaces = 0
        while bits.Position < limit:
            siz = bits.read_uint16()
            star = bits.position
            stop = bits.position + siz
            bits.position = star
            rec = bits.read_uint16()
            if rec == SYM.S_BLOCK32:
                block.parent = bits.read_uint32()
                block.end = bits.read_uint32()
                scopes += 1
                bits.position = block.end
            elif rec == SYM.S_MANSLOT:
                slots += 1
                bits.position = stop
            elif rec == SYM.S_UNAMESPACE:
                used_namespaces += 1
                bits.position = stop
            elif rec == SYM.S_MANCONSTANT:
                constants += 1
                bits.position = stop
            else:
                bits.position = stop
        bits.position = pos
        return constants, scopes, slots, used_namespaces

    def __init__(self, proc, bits):
        self.slot_token = 0
        self.slots = [] # PdbSlot
        self.constants = [] # PdbConstant
        self.namespaces = [] # unicode
        self.using_counts = [] # ushort 
        self.iterator_class = None # unicode
        self.sequence_points = []
        self.sequence_points = [] # PdbSequencePointCollection
        self.token = proc.token
        self.segment = proc.seg
        self.address = proc.off
        self.scopes = [] # PdbScope
        if proc.seg != 1:
            raise PdbDebugException('Segment is %u, not 1.' % proc.seg)
        if proc.parent != 0 or proc.next != 0:
            raise PdbDebugException('Warning parent=%u, next=%u' % (proc.parent, proc.next))
        constant_count, scope_count, slot_count, used_namespaces_count = PdbFunction.CountScopesAndSlots(bits, proc.end)

        if constant_count > 0 or slot_count > 0 or used_namespaces_count > 0:
            self.scopes.append(PdbScope(self.address, proc.len, self.slots, self.constants, self.namespaces))
        while bits.position < proc.end:
            siz = bits.read_uint16()
            star = bits.position
            stop = bits.position + siz
            bits.position = star
            rec = bits.read_uint16()
            if rec == SYM.S_OEM:
                # 0x0404
                oem = OemSymbol()
                oem.id_oem = bits.read_guid()
                oem.typind = bits.read_uint32()
                if oem.id_oem == PdbFunction.msil_meta_data:
                    name = bits.read_strng()
                    if name == 'MD2':
                        version = bits.read_uint8()
                        if version == 4:
                            count = bits.read_uint8()
                            bits.align(4)
                            while count > 0:
                                self.read_custom_metadata(bits)
                                count -= 1
                    bits.position = stop
                else:
                    raise PdbDebugException('OEM section: guid=%u ti=%u' % (oem.idOem, oem.typind))
            
            elif rec == SYM.S_BLOCK32:
                block = BlockSym32()
                block.parent = bits.read_uint32()
                block.end = bits.read_uint32()
                block.length = bits.read_uint32()
                block.off = bits.read_uint32()
                block.seg = bits.read_uint16()
                block.name = bits.skip_cstring()
                bits.Position = stop
                self.scopes.append(PdbScope(self.Address, block, bits))
                self.slot_token = self.scopes[-1].typind
                bits.position = block.end
                
            elif rec == SYM.S_MANSLOT:
                self.slots.append(PdbSlot(bits))
                bits.position = stop

            elif rec == SYM.S_MANCONSTANT:
                self.constants.append(PdbConstant(bits))
                bits.position = stop

            elif rec == SYM.S_UNAMESPACE:
                self.namespaces.append(bits.read_cstring())
                bits.position = stop

            elif rec == SYM.S_END:
                bits.position = stop

            else:
                bits.position = stop

        if bits.position != proc.end:
            raise PdbDebugException('Not at S_END')
        bits.read_uint16() # esiz
        erec = bits.read_uint16()
        if erec != SYM.S_END:
            raise PdbDebugException('Missing S_END')

    def read_custom_metadata(self, bits):
        saved_position = bits.position
        version = bits.read_uint8()
        if version != 4:
            raise PdbDebugException('Unknown custom metadata item version: %u' % version)
        kind = bits.read_uint8()
        bits.align(4)
        number_of_bytes_in_item = bits.read_uint32()
        if kind == 0:
            self.read_using_info(bits)
        elif kind == 1:
            pass # self.read_forward_info(bits)
        elif kind == 2:
            pass # self.read_forwarded_to_module_info(bits)
        elif kind == 3:
            self.read_iterator_locals(bits)
        elif kind == 4:
            self.read_forward_iterator(bits)
        else:
            raise PdbDebugException('Unknown custom metadata item kind: %u' % kind)
        bits.position = saved_position + number_of_bytes_in_item

    def read_forward_iterator(self, bits):
        self.iterator_class = bits.read_string()

    def read_iterator_locals(self, bits):
        bits.read_uint32()

    def read_using_info(self, bits):
        number_of_namespaces = bits.read_uint16()
        bits.read_uint16(number_of_namespaces)

    