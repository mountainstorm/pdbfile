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
from pdb.bitaccess import BitAccess
from pdb.pdbfileheader import PdbFileHeader
from pdb.pdbstreamhelper import PdbStreamHelper
from pdb.msfdirectory import MsfDirectory
from pdb.pdbfile import PdbFile
from pdb.pdbexception import PdbException
from pdb.pdbdebugexception import PdbDebugException
import os


class PDBInvalidError(Exception):
    pass


class PdbUnsupportedError(Exception):
    pass


class NameStream(object):
    def __init__(self, reader, bits, directory):
        directory.streams[1].read(reader, bits)
        (self.name_index,
         self.ver,
         self.sig,
         self.age,
         self.guid) = PdbFile.load_name_index(bits)


class DbiStream(object):
    def __init__(self, reader, bits, directory, ext=PdbFile.EXT_MODULE_FILES):
        directory.streams[3].read(reader, bits)
        self.module_files = None
        (self.modules,
         self.header,
         self.dbghdr,
         self.module_files) = PdbFile.load_dbi_stream(
            bits, True, ext
        )


class PDB(object):
    '''Helper for retrieving information from PDB file'''

    def __init__(self, path):
        self.bits = BitAccess(512 * 1024)
        self.path = path
        self.filename = os.path.basename(path)
        self.pdb_stream = open(path, 'rb')
        self.check_format()
        self.header = PdbFileHeader(self.pdb_stream, self.bits)
        self.reader = PdbStreamHelper(self.pdb_stream, self.header.page_size)
        self.directory = MsfDirectory(self.reader, self.header, self.bits)
        # streams
        self.name_stream = NameStream(self.reader, self.bits, self.directory)
        self.dbi_stream = None
        try:
            self.dbi_stream = DbiStream(self.reader, self.bits, self.directory)
        except PdbDebugException:
            # try without files
            self.dbi_stream = DbiStream(
                self.reader, self.bits, self.directory, PdbFile.EXT_DBIHEADER
            )        
        except PdbException, e:
            raise PdbUnsupportedError(e)
        # generate the symbol id which will match the one from the PE file
        age = self.name_stream.age
        if self.dbi_stream is not None:
            age = self.dbi_stream.dbghdr.age
        self.symbol_id = '%s\\%s%X' % (
            self.filename,
            str(self.name_stream.guid).replace('-', '').upper(),
            age
        )

    def __del__(self):
        self.close()

    def close(self):
        if self.pdb_stream is not None:
            self.pdb_stream.close()
            self.pdb_stream = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

    def check_format(self):
        pdb7 = b'Microsoft C/C++ MSF 7.00\r\n\x1ADS\0\0\0'
        magic = self.pdb_stream.read(len(pdb7))
        self.pdb_stream.seek(0)
        if magic != pdb7:
            pdb2 = b'Microsoft C/C++ program database 2.00\r\n\032JG\0\0'
            magic = self.pdb_stream.read(len(pdb2))
            self.pdb_stream.seek(0)
            if magic != pdb2:
                raise PDBInvalidError('File not a PDB or contains an invalid header')
            else:
                raise PdbUnsupportedError('File is an unsupported PDB2 symbol file')



    

