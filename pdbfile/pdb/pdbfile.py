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
import copy

from bitset import BitSet
from bitaccess import BitAccess
from pdbdebugexception import PdbDebugException
from pdbexception import PdbException
from pdbsource import PdbSource
from pdbsequencepoint import PdbSequencePoint
from pdbsequencepointcollection import PdbSequencePointCollection
from dbidbghdr import DbiDbgHdr
from dbiheader import DbiHeader
from dbimoduleinfo import DbiModuleInfo
from pdbfileheader import PdbFileHeader
from pdbstreamhelper import PdbStreamHelper
from msfdirectory import MsfDirectory


class PdbFile(object):
    s_match = PdbFunction()

    @classmethod
    def load_guid_stream(cls, bits):
        language = bits.read_guid()
        vendor = bits.read_guid()
        doctype = bits.read_guid()
        algorithm_id = bits.read_guid()

        checksum_size = bits.read_int32()
        source_size = bits.read_int32()
        checksum = bits.read_bytes(checksum_size)
        embedded_source = bits.read_bytes(source_size)
        return (doctype, language, vendor, algorithm_id, checksum, embedded_source)

    @classmethod
    def load_name_index(cls, bits):
        result = {} # string -> int
        ver = bits.read_int32()    # 0..3   Version
        sig = bits.read_int32()    # 4..7   Signature
        age = bits.read_int32()    # 8..11  Age
        guid = bits.read_guid()    # 12..27 GUID

        #if ver != 20000404:
        #  raise PdbDebugException('Unsupported PDB Stream version {%u' % ver)

        # Read string buffer.
        buf = bits.read_int32()    # 28..31 Bytes of Strings

        beg = bits.position;
        nxt = bits.position + buf

        bits.position = nxt

        # Read map index.
        cnt = bits.read_int32() # n+0..3 hash size.
        max = bits.read_int32() # n+4..7 maximum ni.

        present = BitSet(bits)
        deleted = BitSet(bits)
        if not deleted.is_empty():
            raise PdbDebugException('Unsupported PDB deleted bitset is not empty.')

        j = 0;
        for i in range(0, max):
            if present.is_set(i):
                ns = bits.read_int32()
                ni = bits.read_int32()

                saved = bits.position
                bits.position = beg + ns
                name = bits.read_cstring()
                bits.position = saved

                result.add(name.to_upper_invariant(), ni)
                j += 1
        if j != cnt:
            raise PdbDebugException('Count mismatch. (%u != %u)' % (j, cnt))
        return (result, ver, sig, age, guid)

    @classmethod
    def load_name_stream(cls, bits):
        ht = {} # int -> string

        sig = bits.read_uint32() # 0..3  Signature
        ver = bits.read_int32()  # 4..7  Version

        # Read (or skip) string buffer.
        buf = bits.read_int32()   # 8..11 Bytes of Strings

        if sig != 0xeffeeffe or ver != 1:
            raise PdbDebugException('Unsupported Name Stream version. ' +
                                    '(sig=%08x, ver=%u)' % (sig, ver))
        beg = bits.position
        nxt = bits.position + buf
        bits.position = nxt

        # Read hash table.
        siz = bits.read_int32()   # n+0..3 Number of hash buckets.
        nxt = bits.position
        for i in range(0, siz):
            ni = bits.read_int32()
            if ni != 0:
                saved = bits.position
                bits.position = beg + ni
                name = bits.read_cstring()
                bits.position = saved
                ht[ni] = name
        bits.position = nxt
        return ht

    @classmethod
    def find_function(cls, funcs, sec, off):
        PdbFile.s_match.segment = sec
        PdbFile.s_match.address = off
        # XXX: binary search
        return Array.BinarySearch(funcs, PdbFile.s_match, PdbFunction.by_address)

    @classmethod
    def load_managed_lines(cls, funcs, names, bits, directory, name_index, reader, limit, sources):
        funcs.sort(PdbFunction.by_address_and_token)

        checks = {} # int -> PdbSource

        # Read the files first
        begin = bits.position
        while bits.position < limit:
            sig = bits.read_int32()
            siz = bits.read_int32()
            place = bits.position
            end_sym = bits.position + siz
            if DEBUG_S_SUBSECTION.sig == DEBUG_S_SUBSECTION.FILECHKSMS:
                while bits.position < end_sym:
                    chk = CV_FileCheckSum()

                    ni = bits.position - place
                    chk.name = bits.read_uint32()
                    chk.length = bits.read_uint8()
                    chk.type = bits.read_uint8()

                    name = names[chk.name]
                    src = None
                    n = name.to_upper_invariant()
                    if n in sources:
                        src = sources[n]
                        doctype_guid = None
                        language_guid = None
                        vendor_guid = None
                        algorithm_id = None
                        checksum = None
                        source = None

                        guid_stream = None
                        n = '/SRC/FILES/' + name.to_upper_invariant()
                        if n in name_index:
                            guid_stream = name_index[n]
                            guid_bits = BitAccess(0x100)
                            directory.streams[guid_stream].read(reader, guid_bits)
                            (doctype_guid, language_guid, vendor_guid,
                             algorithm_id, checksum, source) = PdbFile.load_guid_stream(guid_bits)

                        src = PdbSource(name, doctype_guid, language_guid, vendor_guid, algorithm_id, checksum, source)
                        sources[name.to_upper_invariant()] = src
                    checks[ni] = src
                    bits.position += chk.length
                    bits.align(4)
                bits.position = end_sym
            else:
                bits.position = end_sym

        # Read the lines next.
        bits.position = begin
        while bits.position < limit:
            sig = bits.read_int32()
            siz = bits.read_int32()
            end_sym = bits.position + siz

            if sig == DEBUG_S_SUBSECTION.LINES:
                sec = CV_LineSection()

                sec.off = bits.read_uint32()
                sec.sec = bits.read_uint16()
                sec.flags = bits.read_uint16()
                sec.cod = bits.read_uint32()
                func_index = PdbFile.FindFunction(funcs, sec.sec, sec.off)
                if func_index < 0:
                    break
                func = funcs[func_index]
                if func.sequence_points is None:
                    while func_index > 0:
                        f = funcs[func_index - 1]
                        if (f.sequence_points is not None or
                            f.segment != sec.sec or
                            f.Address != sec.off):
                            break
                        func = f
                        func_index -= 1
                else:
                    while func_index < funcs.length - 1 and func.sequence_points is not None:
                        f = funcs[func_index + 1]
                        if f.segment != sec.sec or f.address != sec.off:
                            break
                        func = f
                        func_index += 1
                if func.SequencePoints is not None:
                    break

                # Count the line blocks.
                beg_sym = bits.position
                blocks = 0
                while bits.position < end_sym:
                    src_file = CV_SourceFile()
                    src_file.index = bits.read_uint32()
                    src_file.count = bits.read_uint32()
                    src_file.linsiz = bits.read_uint32()  # Size of payload.
                    f = 0
                    if (sec.flags & 1) != 0:
                        f = 4
                    linsiz = src_file.count * (8 + f)
                    bits.position += linsiz
                    blocks += 1

                func.sequence_points = []

                bits.position = beg_sym
                while bits.position < end_sym:
                    src_file = CV_SourceFile()
                    src_file.index = bits.read_uint32()
                    src_file.count = bits.read_uint32()
                    src_file.linsiz = bits.read_uint32()  # Size of payload.

                    src = checks[src_file.index]
                    tmp = PdbSequencePointCollection(src, src_file.count)
                    func.sequence_points.append(tmp)
                    lines = copy.copy(tmp.lines)

                    plin = bits.position;
                    pcol = bits.position + 8 * src_file.count
                    for i in range(0, src_file.count):
                        line = CV_Line()
                        column = CV_Column()

                        bits.position = plin + 8 * i
                        line.offset = bits.read_uint32()
                        line.flags = bits.read_uint32()

                        line_begin = line.flags & CV_Line_Flags.linenum_start
                        delta = (line.flags & CV_Line_Flags.delta_line_end) >> 24
                        # statement = (line.flags & CV_Line_Flags.f_statement) == 0
                        if (sec.flags & 1) != 0:
                            bits.position = pcol + 4 * i
                            column.off_column_start = bits.read_uint16()
                            column.off_column_end = bits.read_uint16()

                        lines[i] = PdbSequencePoint(line.offset,
                                                    line_begin,
                                                    column.off_column_start,
                                                    line_begin + delta,
                                                    column.off_column_end)
            bits.position = end_sym

    @classmethod
    def load_funcs_from_dbi_module(cls,
                                   bits,
                                   info,
                                   names,
                                   func_list,
                                   read_strings,
                                   directory,
                                   name_index,
                                   reader,
                                   sources):
        bits.position = 0;
        sig = bits.read_int32()
        if sig != 4:
            raise PdbDebugException('Invalid signature. (sig=%u)' % sig)

        bits.position = 4
        # print('%s' % info.module_name)
        funcs = PdbFunction.load_managed_functions(bits, info.cb_syms, read_strings)
        if funcs is not None:
            bits.position = info.cb_syms + info.cb_old_lines
            PdbFile.load_managed_lines(funcs, names, bits, directory, name_index, reader,
                                       (info.cb_syms + info.cb_old_lines + info.cb_ines),
                                       sources)
            for i in range(0, len(funcs)):
                func_list.append(funcs[i])

    @classmethod
    def load_dbi_stream(cls, bits, read_strings):
        dh = DbiHeader(bits)
        header = DbiDbgHdr()

        #if dh.sig != -1 or dh.ver != 19990903:
        #   raise PdbException('Unsupported DBI Stream version, sig=%u, ver=%u' % (dh.sig, dh.ver))

        # Read gpmod section.
        mod_list = [] # of DbiModuleInfo
        end = bits.position + dh.gpmodi_size
        while bits.position < end:
            mod_list.append(DbiModuleInfo(bits, read_strings))
        
        if bits.position != end:
            raise PdbDebugException('Error reading DBI stream, pos=%u != %u' % (bits.position, end))

        modules = None
        if mod_list.count > 0:
            modules = mod_list

        # Skip the Section Contribution substream.
        bits.position += dh.seccon_size

        # Skip the Section Map substream.
        bits.position += dh.secmap_size

        # Skip the File Info substream.
        bits.position += dh.filinf_size

        # Skip the TSM substream.
        bits.position += dh.tsmap_size

        # Skip the EC substream.
        bits.position += dh.ecinfo_size

        # Read the optional header.
        end = bits.position + dh.dbghdr_size
        if dh.dbghdr_size > 0:
            header = DbiDbgHdr(bits)
        bits.position = end
        return modules, header

    @classmethod
    def load_functions(cls, read, read_all_strings, bits=None):
        if bits is None:
            bits = BitAccess(512 * 1024)    
        head = PdbFileHeader(read, bits)
        reader = PdbStreamHelper(read, head.PageSize)
        directory = MsfDirectory(reader, head, bits)

        directory.streams[1].read(reader, bits)
        name_index, ver, sig, age, guid = PdbFile.load_name_index(bits)
        try:
            name_stream = name_index['/NAMES']
        except KeyError:
            raise PdbException('No "name" stream')

        directory.streams[name_stream].read(reader, bits)
        names = PdbFile.load_name_stream(bits)

        directory.streams[3].read(reader, bits)
        modules, header = PdbFile.load_dbi_stream(bits, read_all_strings)

        func_list = [] # PdbFunction
        source_dictionary = {} # string -> PdbSource
        if modules is not None:
            for m in range(0, len(modules)):
                if modules[m].stream > 0:
                    directory.streams[modules[m].stream].read(reader, bits)
                    PdbFile.load_funcs_from_dbi_module(bits,
                                                       modules[m],
                                                       names,
                                                       func_list,
                                                       read_all_strings,
                                                       directory,
                                                       name_index,
                                                       reader,
                                                       source_dictionary)
        funcs = func_list
        sources = source_dictionary.values()

        # After reading the functions, apply the token remapping table if it exists.
        if header.sn_token_rid_map != 0 and header.sn_token_rid_map != 0xffff:
            directory.streams[header.sn_token_rid_map].read(reader, bits)
            rid_map = bits.read_uint32(len(directory.streams[header.sn_token_rid_map]) / 4)
            for func in funcs:
                func.token = 0x06000000 | rid_map[func.token & 0xffffff]

        funcs.sort(PdbFunction.by_address_and_token)
        #funcs.sort(PdbFunction.by_token)
        return funcs, ver, sig, age, guid, sources
