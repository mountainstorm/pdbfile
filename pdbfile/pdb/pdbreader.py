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


from pdbfile import PdbFile
from pdbfileheader import PdbFileHeader
from pdbstreamhelper import PdbStreamHelper
from msfdirectory import MsfDirectory
from bitaccess import BitAccess


class PdbReader(object):
    '''An object that can map offsets in an IL stream to source locations and block scopes.'''

    def __init__(self, pdb_stream=None, filename=None):
        '''Allocates an object that can map some kinds of ILocation objects to IPrimarySourceLocation objects. 
        For example, a PDB reader that maps offsets in an IL stream to source locations.'''
        self.sources = None
        '''A collection of all sources in this pdb; PdbSource'''
        self._pdb_function_map = {} # uint -> PdbFunction
        self.version = 0
        '''The version of this PDB; int'''
        self._sig = None
        self.signature = 0
        '''The Guid signature of this pdb.  Should be compared to the corresponding pdb signature in the matching PEFile; guid'''
        self.age = 0
        '''The age of this pdb.  Should be compared to the corresponding pdb age in the matching PEFile; int'''
        if pdb_stream is None:
            with open(filename, 'rb') as fs:
                self.init(fs)
        else:
            self.init(pdb_stream)

    def init(self, pdb_stream):
        (functions,
         self.version,
         self._sig,
         self.age,
         self.signature,
         self.sources) = PdbFile.load_functions(pdb_stream, True)
        for pdb_function in functions:
            self._pdb_function_map[pdb_function.token] = pdb_function

    @property
    def functions(self):
        '''A collection of all functions in this pdb; PdbFunction; list'''
        return self._pdb_function_map.values()

    @classmethod
    def get_pdb_properties(cls, pdb_file):
        '''Gets the properties of a given pdb.  Throws IOException on error'''
        bits = BitAccess(512 * 1024)
        with open(pdb_file, 'rb') as pdb_stream:
            header = PdbFileHeader(pdb_stream, bits)
            reader = PdbStreamHelper(pdb_stream, header.page_size)
            directory = MsfDirectory(reader, header, bits)

            directory.streams[1].read(reader, bits)

            bits.read_int32()          #  0..3  Version
            bits.read_int32()          #  4..7  Signature
            age = bits.read_int32()    #  8..11 Age
            guid = bits.read_guid()    # 12..27 GUID
        return guid, age

    def get_function_from_token(self, method_token):
        '''Retreives a PdbFunction by its metadata token'''
        retval = None
        if method_token in self._pdb_function_map:
            retval = self._pdb_function_map[method_token]
        return retval
