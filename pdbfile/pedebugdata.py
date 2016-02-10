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

from pefile import PE, DEBUG_TYPE, DIRECTORY_ENTRY
import struct
import ntpath
import uuid


class PEUnknownDebugDataError(Exception):
    pass


class PEMissingDebugDataError(Exception):
    pass


class CodeViewRSDS(object):
    def __init__(self, data):
        fmt = '<4s16sI'
        sz = struct.calcsize(fmt)
        self.magic, guid, self.age = struct.unpack(fmt, data[:sz])
        self.guid = uuid.UUID(bytes_le=guid)
        i = data[sz:].find('\x00')
        self.filename = data[sz:sz+i].decode('utf-8', 'ignore')
        # generate symbol_id
        guid = str(self.guid).replace('-', '').upper()
        fn = ntpath.basename(self.filename).lower()
        self.symbol_id = '%s/%s%X' % (fn, guid, self.age)


class CodeViewNB10(object):
    def __init__(self, data):
        fmt = '<4sIII'
        sz = struct.calcsize(fmt)
        (self.magic,
         self.offset,
         self.timestamp,
         self.age) = struct.unpack(fmt, data[:sz])
        i = data[sz:].find('\x00')
        self.filename = data[sz:sz+i].decode('utf-8', 'ignore')
        # generate symbol_id
        fn = ntpath.basename(self.filename).lower()
        self.symbol_id = '%s/%X%X' % (
            fn, self.timestamp, self.age
        )


class PEDebugData(object):
    def __init__(self, path, filename=None):
        self.pe = PE(path, fast_load=True)
        self.path = path
        self.filename = filename
        if filename is None:
            self.filename = os.path.basename(path)

    @property
    def symbol_id(self):
        return self.codeview_info().symbol_id

    @property
    def executable_id(self):
        retval = None
        if self.filename is not None:
            retval = '%s/%X%X' % (self.filename.lower(),
                                  self.pe.FILE_HEADER.TimeDateStamp,
                                  self.pe.OPTIONAL_HEADER.SizeOfImage)
        return retval

    def codeview_info(self):
        info = None
        data = self.debug_data()
        if data is not None:
            if data[:4] == 'RSDS':
                info = CodeViewRSDS(data)
            elif data[:4] == 'NB10':
                info = CodeViewNB10(data)
            else:
                raise PEUnknownDebugDataError('Unknown CodeView type: %s' % data[:4])
        else:
            raise PEMissingDebugDataError()
        return info

    def debug_data(self):
        data = None
        if not hasattr(self.pe, 'DIRECTORY_ENTRY_DEBUG'):
            self.pe.parse_data_directories(
                DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_DEBUG']
            )
        if hasattr(self.pe, 'DIRECTORY_ENTRY_DEBUG'):
            for entry in self.pe.DIRECTORY_ENTRY_DEBUG:
                off = entry.struct.PointerToRawData
                if (entry.struct.Type == DEBUG_TYPE['IMAGE_DEBUG_TYPE_CODEVIEW'] or
                    entry.struct.Type == DEBUG_TYPE['IMAGE_DEBUG_TYPE_MISC']):
                    data = self.pe.__data__[off:off+entry.struct.SizeOfData]
                    if data is not None:
                        break
        return data
