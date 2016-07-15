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


class FLOAT10(object):
    def __init__(self):
        self.data_0 = 0
        self.data_1 = 0
        self.data_2 = 0
        self.data_3 = 0
        self.data_4 = 0
        self.data_5 = 0
        self.data_6 = 0
        self.data_7 = 0
        self.data_8 = 0
        self.data_9 = 0


class CV_SIGNATURE(object):
    C6 = 0          # Actual signature is >64K
    C7 = 1          # First explicit signature
    C11 = 2         # C11 (vc5.x) 32-bit types
    C13 = 4         # C13 (vc7.x) zero terminated names
    RESERVERD = 5   # All signatures from 5 to 64K are reserved


# CodeView Symbol and Type OMF type information is broken up into two
# ranges.  Type indices less than 0x1000 describe type information
# that is frequently used.  Type indices above 0x1000 are used to
# describe more complex features such as functions, arrays and
# structures.
#
# Primitive types have predefined meaning that is encoded in the
# values of the various bit fields in the value.
#
# A CodeView primitive type is defined as:
#
# 1 1
# 1 089  7654  3  210
# r mode type  r  sub
#
# Where
#     mode is the pointer mode
#     type is a type indicator
#     sub  is a subtype enumeration
#     r    is a reserved field
#
# See Microsoft Symbol and Type OMF (Version 4.0) for more
# information.
#

# pointer mode enumeration values
class CV_prmode(object):
    CV_TM_DIRECT = 0    # mode is not a pointer
    CV_TM_NPTR32 = 4    # mode is a 32 bit near pointer
    CV_TM_NPTR64 = 6    # mode is a 64 bit near pointer
    CV_TM_NPTR128 = 7   # mode is a 128 bit near pointer


# type enumeration values
class CV_type(object):
    CV_SPECIAL = 0x00    # special type size values
    CV_SIGNED = 0x01     # signed integral size values
    CV_UNSIGNED = 0x02   # unsigned integral size values
    CV_BOOLEAN = 0x03    # Boolean size values
    CV_REAL = 0x04       # real number size values
    CV_COMPLEX = 0x05    # complex number size values
    CV_SPECIAL2 = 0x06   # second set of special types
    CV_INT = 0x07        # integral (int) values
    CV_CVRESERVED = 0x0f


# subtype enumeration values for CV_SPECIAL
class CV_special(object):
    CV_SP_NOTYPE = 0x00
    CV_SP_ABS = 0x01
    CV_SP_SEGMENT = 0x02
    CV_SP_VOID = 0x03
    CV_SP_CURRENCY = 0x04
    CV_SP_NBASICSTR = 0x05
    CV_SP_FBASICSTR = 0x06
    CV_SP_NOTTRANS = 0x07
    CV_SP_HRESULT = 0x08


# subtype enumeration values for CV_SPECIAL2
class CV_special2(object):
    CV_S2_BIT = 0x00
    CV_S2_PASCHAR = 0x01 # Pascal CHAR


# subtype enumeration values for CV_SIGNED, CV_UNSIGNED and CV_BOOLEAN
class CV_integral(object):
    CV_IN_1BYTE = 0x00
    CV_IN_2BYTE = 0x01
    CV_IN_4BYTE = 0x02
    CV_IN_8BYTE = 0x03
    CV_IN_16BYTE = 0x04


# subtype enumeration values for CV_REAL and CV_COMPLEX
class CV_real(object):
    CV_RC_REAL32 = 0x00
    CV_RC_REAL64 = 0x01
    CV_RC_REAL80 = 0x02
    CV_RC_REAL128 = 0x03


# subtype enumeration values for CV_INT (really int)
class CV_int(object):
    CV_RI_CHAR = 0x00
    CV_RI_INT1 = 0x00
    CV_RI_WCHAR = 0x01
    CV_RI_UINT1 = 0x01
    CV_RI_INT2 = 0x02
    CV_RI_UINT2 = 0x03
    CV_RI_INT4 = 0x04
    CV_RI_UINT4 = 0x05
    CV_RI_INT8 = 0x06
    CV_RI_UINT8 = 0x07
    CV_RI_INT16 = 0x08
    CV_RI_UINT16 = 0x09


class CV_PRIMITIVE_TYPE(object):
    def __init__(self):
        self.CV_MMASK = 0x700 # mode mask
        self.CV_TMASK = 0x0f0 # type mask
        self.CV_SMASK = 0x00f # subtype mask
        self.CV_MSHIFT = 8 # primitive mode right shift count
        self.CV_TSHIFT = 4 # primitive type right shift count
        self.CV_SSHIFT = 0 # primitive subtype right shift count
        # function to extract primitive mode, type and size
        self.CV_FIRST_NONPRIM = 0x1000

# selected values for type_index - for a more complete definition, see
# Microsoft Symbol and Type OMF document

# Special Types
class TYPE_ENUM(object):
    # Special Types
    T_NOTYPE = 0x0000 # uncharacterized type (no type)
    T_ABS = 0x0001 # absolute symbol
    T_SEGMENT = 0x0002 # segment type
    T_VOID = 0x0003 # void
    T_HRESULT = 0x0008 # OLE/COM HRESULT
    T_32PHRESULT = 0x0408 # OLE/COM HRESULT __ptr32//
    T_64PHRESULT = 0x0608 # OLE/COM HRESULT __ptr64//
    T_PVOID = 0x0103 # near pointer to void
    T_PFVOID = 0x0203 # far pointer to void
    T_PHVOID = 0x0303 # huge pointer to void
    T_32PVOID = 0x0403 # 32 bit pointer to void
    T_64PVOID = 0x0603 # 64 bit pointer to void
    T_CURRENCY = 0x0004 # BASIC 8 byte currency value
    T_NOTTRANS = 0x0007 # type not translated by cvpack
    T_BIT = 0x0060 # bit
    T_PASCHAR = 0x0061 # Pascal CHAR

    # Character types
    T_CHAR = 0x0010 # 8 bit signed
    T_32PCHAR = 0x0410 # 32 bit pointer to 8 bit signed
    T_64PCHAR = 0x0610 # 64 bit pointer to 8 bit signed
    T_UCHAR = 0x0020 # 8 bit unsigned
    T_32PUCHAR = 0x0420 # 32 bit pointer to 8 bit unsigned
    T_64PUCHAR = 0x0620 # 64 bit pointer to 8 bit unsigned
    
    # really a character types
    T_RCHAR = 0x0070 # really a char
    T_32PRCHAR = 0x0470 # 32 bit pointer to a real char
    T_64PRCHAR = 0x0670 # 64 bit pointer to a real char

    # really a wide character types
    T_WCHAR = 0x0071 # wide char
    T_32PWCHAR = 0x0471 # 32 bit pointer to a wide char
    T_64PWCHAR = 0x0671 # 64 bit pointer to a wide char

    # 8 bit int types
    T_INT1 = 0x0068 # 8 bit signed int
    T_32PINT1 = 0x0468 # 32 bit pointer to 8 bit signed int
    T_64PINT1 = 0x0668 # 64 bit pointer to 8 bit signed int
    T_UINT1 = 0x0069 # 8 bit unsigned int
    T_32PUINT1 = 0x0469 # 32 bit pointer to 8 bit unsigned int
    T_64PUINT1 = 0x0669 # 64 bit pointer to 8 bit unsigned int

    # 16 bit short types
    T_SHORT = 0x0011 # 16 bit signed
    T_32PSHORT = 0x0411 # 32 bit pointer to 16 bit signed
    T_64PSHORT = 0x0611 # 64 bit pointer to 16 bit signed
    T_USHORT = 0x0021 # 16 bit unsigned
    T_32PUSHORT = 0x0421 # 32 bit pointer to 16 bit unsigned
    T_64PUSHORT = 0x0621 # 64 bit pointer to 16 bit unsigned
    
    # 16 bit int types
    T_INT2 = 0x0072 # 16 bit signed int
    T_32PINT2 = 0x0472 # 32 bit pointer to 16 bit signed int
    T_64PINT2 = 0x0672 # 64 bit pointer to 16 bit signed int
    T_UINT2 = 0x0073 # 16 bit unsigned int
    T_32PUINT2 = 0x0473 # 32 bit pointer to 16 bit unsigned int
    T_64PUINT2 = 0x0673 # 64 bit pointer to 16 bit unsigned int
    
    # 32 bit long types
    T_LONG = 0x0012 # 32 bit signed
    T_ULONG = 0x0022 # 32 bit unsigned
    T_32PLONG = 0x0412 # 32 bit pointer to 32 bit signed
    T_32PULONG = 0x0422 # 32 bit pointer to 32 bit unsigned
    T_64PLONG = 0x0612 # 64 bit pointer to 32 bit signed
    T_64PULONG = 0x0622 # 64 bit pointer to 32 bit unsigned

    # 32 bit int types
    T_INT4 = 0x0074 # 32 bit signed int
    T_32PINT4 = 0x0474 # 32 bit pointer to 32 bit signed int
    T_64PINT4 = 0x0674 # 64 bit pointer to 32 bit signed int
    T_UINT4 = 0x0075 # 32 bit unsigned int
    T_32PUINT4 = 0x0475 # 32 bit pointer to 32 bit unsigned int
    T_64PUINT4 = 0x0675 # 64 bit pointer to 32 bit unsigned int

    # 64 bit quad types
    T_QUAD = 0x0013 # 64 bit signed
    T_32PQUAD = 0x0413 # 32 bit pointer to 64 bit signed
    T_64PQUAD = 0x0613 # 64 bit pointer to 64 bit signed
    T_UQUAD = 0x0023 # 64 bit unsigned
    T_32PUQUAD = 0x0423 # 32 bit pointer to 64 bit unsigned
    T_64PUQUAD = 0x0623 # 64 bit pointer to 64 bit unsigned
    
    # 64 bit int types
    T_INT8 = 0x0076 # 64 bit signed int
    T_32PINT8 = 0x0476 # 32 bit pointer to 64 bit signed int
    T_64PINT8 = 0x0676 # 64 bit pointer to 64 bit signed int
    T_UINT8 = 0x0077 # 64 bit unsigned int
    T_32PUINT8 = 0x0477 # 32 bit pointer to 64 bit unsigned int
    T_64PUINT8 = 0x0677 # 64 bit pointer to 64 bit unsigned int
    
    #  128 bit octet types
    T_OCT = 0x0014 # 128 bit signed
    T_32POCT = 0x0414 # 32 bit pointer to 128 bit signed
    T_64POCT = 0x0614 # 64 bit pointer to 128 bit signed
    T_UOCT = 0x0024 # 128 bit unsigned
    T_32PUOCT = 0x0424 # 32 bit pointer to 128 bit unsigned
    T_64PUOCT = 0x0624 # 64 bit pointer to 128 bit unsigned
    
    # 128 bit int types
    T_INT16 = 0x0078 # 128 bit signed int
    T_32PINT16 = 0x0478 # 32 bit pointer to 128 bit signed int
    T_64PINT16 = 0x0678 # 64 bit pointer to 128 bit signed int
    T_UINT16 = 0x0079 # 128 bit unsigned int
    T_32PUINT16 = 0x0479 # 32 bit pointer to 128 bit unsigned int
    T_64PUINT16 = 0x0679 # 64 bit pointer to 128 bit unsigned int
    
    # 32 bit real types
    T_REAL32 = 0x0040 # 32 bit real
    T_32PREAL32 = 0x0440 # 32 bit pointer to 32 bit real
    T_64PREAL32 = 0x0640 # 64 bit pointer to 32 bit real
    
    # 64 bit real types
    T_REAL64 = 0x0041 # 64 bit real
    T_32PREAL64 = 0x0441 # 32 bit pointer to 64 bit real
    T_64PREAL64 = 0x0641 # 64 bit pointer to 64 bit real
    
    # 80 bit real types
    T_REAL80 = 0x0042 # 80 bit real
    T_32PREAL80 = 0x0442 # 32 bit pointer to 80 bit real
    T_64PREAL80 = 0x0642 # 64 bit pointer to 80 bit real
    
    # 128 bit real types
    T_REAL128 = 0x0043 # 128 bit real
    T_32PREAL128 = 0x0443 # 32 bit pointer to 128 bit real
    T_64PREAL128 = 0x0643 # 64 bit pointer to 128 bit real
    
    # 32 bit complex types
    T_CPLX32 = 0x0050 # 32 bit complex
    T_32PCPLX32 = 0x0450 # 32 bit pointer to 32 bit complex
    T_64PCPLX32 = 0x0650 # 64 bit pointer to 32 bit complex
    
    # 64 bit complex types
    T_CPLX64 = 0x0051 # 64 bit complex
    T_32PCPLX64 = 0x0451 # 32 bit pointer to 64 bit complex
    T_64PCPLX64 = 0x0651 # 64 bit pointer to 64 bit complex
    
    # 80 bit complex types
    T_CPLX80 = 0x0052 # 80 bit complex
    T_32PCPLX80 = 0x0452 # 32 bit pointer to 80 bit complex
    T_64PCPLX80 = 0x0652 # 64 bit pointer to 80 bit complex
    
    # 128 bit complex types
    T_CPLX128 = 0x0053 # 128 bit complex
    T_32PCPLX128 = 0x0453 # 32 bit pointer to 128 bit complex
    T_64PCPLX128 = 0x0653 # 64 bit pointer to 128 bit complex
    
    # boolean types
    T_BOOL08 = 0x0030 # 8 bit boolean
    T_32PBOOL08 = 0x0430 # 32 bit pointer to 8 bit boolean
    T_64PBOOL08 = 0x0630 # 64 bit pointer to 8 bit boolean
    T_BOOL16 = 0x0031 # 16 bit boolean
    T_32PBOOL16 = 0x0431 # 32 bit pointer to 18 bit boolean
    T_64PBOOL16 = 0x0631 # 64 bit pointer to 18 bit boolean
    T_BOOL32 = 0x0032 # 32 bit boolean
    T_32PBOOL32 = 0x0432 # 32 bit pointer to 32 bit boolean
    T_64PBOOL32 = 0x0632 # 64 bit pointer to 32 bit boolean
    T_BOOL64 = 0x0033 # 64 bit boolean
    T_32PBOOL64 = 0x0433 # 32 bit pointer to 64 bit boolean
    T_64PBOOL64 = 0x0633 # 64 bit pointer to 64 bit boolean


#  No leaf index can have a value of 0x0000.  The leaf indices are
#  separated into ranges depending upon the use of the type record.
#  The second range is for the type records that are directly referenced
#  in symbols. The first range is for type records that are not
#  referenced by symbols but instead are referenced by other type
#  records.  All type records must have a starting leaf index in these
#  first two ranges.  The third range of leaf indices are used to build
#  up complex lists such as the field list of a class type record.  No
#  type record can begin with one of the leaf indices. The fourth ranges
#  of type indices are used to represent numeric data in a symbol or
#  type record. These leaf indices are greater than 0x8000.  At the
#  point that type or symbol processor is expecting a numeric field, the
#  next two bytes in the type record are examined.  If the value is less
#  than 0x8000, then the two bytes contain the numeric value.  If the
#  value is greater than 0x8000, then the data follows the leaf index in
#  a format specified by the leaf index. The final range of leaf indices
#  are used to force alignment of subfields within a complex type record..
#
class LEAF(object):
    # leaf indices starting records but referenced from symbol records
    LF_VTSHAPE = 0x000a
    LF_COBOL1 = 0x000c
    LF_LABEL = 0x000e
    LF_NULL = 0x000f
    LF_NOTTRAN = 0x0010
    LF_ENDPRECOMP = 0x0014 # not referenced from symbol
    LF_TYPESERVER_ST = 0x0016 # not referenced from symbol
    
    # leaf indices starting records but referenced only from type records
    LF_LIST = 0x0203
    LF_REFSYM = 0x020c
    LF_ENUMERATE_ST = 0x0403
    
    # 32-bit type index versions of leaves, all have the 0x1000 bit set
    LF_TI16_MAX = 0x1000

    LF_MODIFIER = 0x1001
    LF_POINTER = 0x1002
    LF_ARRAY_ST = 0x1003
    LF_CLASS_ST = 0x1004
    LF_STRUCTURE_ST = 0x1005
    LF_UNION_ST = 0x1006
    LF_ENUM_ST = 0x1007
    LF_PROCEDURE = 0x1008
    LF_MFUNCTION = 0x1009
    LF_COBOL0 = 0x100a
    LF_BARRAY = 0x100b
    LF_DIMARRAY_ST = 0x100c
    LF_VFTPATH = 0x100d
    LF_PRECOMP_ST = 0x100e # not referenced from symbol
    LF_OEM = 0x100f # oem definable type string
    LF_ALIAS_ST = 0x1010 # alias (typedef) type
    LF_OEM2 = 0x1011 # oem definable type string
    
    # leaf indices starting records but referenced only from type records
    LF_SKIP = 0x1200
    LF_ARGLIST = 0x1201
    LF_DEFARG_ST = 0x1202
    LF_FIELDLIST = 0x1203
    LF_DERIVED = 0x1204
    LF_BITFIELD = 0x1205
    LF_METHODLIST = 0x1206
    LF_DIMCONU = 0x1207
    LF_DIMCONLU = 0x1208
    LF_DIMVARU = 0x1209
    LF_DIMVARLU = 0x120a
    LF_BCLASS = 0x1400
    LF_VBCLASS = 0x1401
    LF_IVBCLASS = 0x1402
    LF_FRIENDFCN_ST = 0x1403
    LF_INDEX = 0x1404
    LF_MEMBER_ST = 0x1405
    LF_STMEMBER_ST = 0x1406
    LF_METHOD_ST = 0x1407
    LF_NESTTYPE_ST = 0x1408
    LF_VFUNCTAB = 0x1409
    LF_FRIENDCLS = 0x140a
    LF_ONEMETHOD_ST = 0x140b
    LF_VFUNCOFF = 0x140c
    LF_NESTTYPEEX_ST = 0x140d
    LF_MEMBERMODIFY_ST = 0x140e
    LF_MANAGED_ST = 0x140f
    
    # Types w/ SZ names
    LF_ST_MAX = 0x1500
    LF_TYPESERVER = 0x1501 # not referenced from symbol
    LF_ENUMERATE = 0x1502
    LF_ARRAY = 0x1503
    LF_CLASS = 0x1504
    LF_STRUCTURE = 0x1505
    LF_UNION = 0x1506
    LF_ENUM = 0x1507
    LF_DIMARRAY = 0x1508
    LF_PRECOMP = 0x1509 # not referenced from symbol
    LF_ALIAS = 0x150a # alias (typedef) type
    LF_DEFARG = 0x150b
    LF_FRIENDFCN = 0x150c
    LF_MEMBER = 0x150d
    LF_STMEMBER = 0x150e
    LF_METHOD = 0x150f
    LF_NESTTYPE = 0x1510
    LF_ONEMETHOD = 0x1511
    LF_NESTTYPEEX = 0x1512
    LF_MEMBERMODIFY = 0x1513
    LF_MANAGED = 0x1514
    LF_TYPESERVER2 = 0x1515
    LF_NUMERIC = 0x8000
    LF_CHAR = 0x8000
    LF_SHORT = 0x8001
    LF_USHORT = 0x8002
    LF_LONG = 0x8003
    LF_ULONG = 0x8004
    LF_REAL32 = 0x8005
    LF_REAL64 = 0x8006
    LF_REAL80 = 0x8007
    LF_REAL128 = 0x8008
    LF_QUADWORD = 0x8009
    LF_UQUADWORD = 0x800a
    LF_COMPLEX32 = 0x800c
    LF_COMPLEX64 = 0x800d
    LF_COMPLEX80 = 0x800e
    LF_COMPLEX128 = 0x800f
    LF_VARSTRING = 0x8010
    LF_OCTWORD = 0x8017
    LF_UOCTWORD = 0x8018
    LF_DECIMAL = 0x8019
    LF_DATE = 0x801a
    LF_UTF8STRING = 0x801b
    LF_PAD0 = 0xf0
    LF_PAD1 = 0xf1
    LF_PAD2 = 0xf2
    LF_PAD3 = 0xf3
    LF_PAD4 = 0xf4
    LF_PAD5 = 0xf5
    LF_PAD6 = 0xf6
    LF_PAD7 = 0xf7
    LF_PAD8 = 0xf8
    LF_PAD9 = 0xf9
    LF_PAD10 = 0xfa
    LF_PAD11 = 0xfb
    LF_PAD12 = 0xfc
    LF_PAD13 = 0xfd
    LF_PAD14 = 0xfe
    LF_PAD15 = 0xff
    # end of leaf indices


# Type enum for pointer records
# Pointers can be one of the following types
class CV_ptrtype(object):
    CV_PTR_BASE_SEG = 0x03 # based on segment
    CV_PTR_BASE_VAL = 0x04 # based on value of base
    CV_PTR_BASE_SEGVAL = 0x05 # based on segment value of base
    CV_PTR_BASE_ADDR = 0x06 # based on address of base
    CV_PTR_BASE_SEGADDR = 0x07 # based on segment address of base
    CV_PTR_BASE_TYPE = 0x08 # based on type
    CV_PTR_BASE_SELF = 0x09 # based on self
    CV_PTR_NEAR32 = 0x0a # 32 bit pointer
    CV_PTR_64 = 0x0c # 64 bit pointer
    CV_PTR_UNUSEDPTR = 0x0d # first unused pointer type


# Mode enum for pointers
# Pointers can have one of the following modes
class CV_ptrmode(object):
    CV_PTR_MODE_PTR = 0x00 # "normal" pointer
    CV_PTR_MODE_REF = 0x01 # reference
    CV_PTR_MODE_PMEM = 0x02 # pointer to data member
    CV_PTR_MODE_PMFUNC = 0x03 # pointer to member function
    CV_PTR_MODE_RESERVED = 0x04 # first unused pointer mode


# enumeration for pointer-to-member types
class CV_pmtype(object):
    CV_PMTYPE_Undef = 0x00 # not specified (pre VC8)
    CV_PMTYPE_D_Single = 0x01 # member data, single inheritance
    CV_PMTYPE_D_Multiple = 0x02 # member data, multiple inheritance
    CV_PMTYPE_D_Virtual = 0x03 # member data, virtual inheritance
    CV_PMTYPE_D_General = 0x04 # member data, most general
    CV_PMTYPE_F_Single = 0x05 # member function, single inheritance
    CV_PMTYPE_F_Multiple = 0x06 # member function, multiple inheritance
    CV_PMTYPE_F_Virtual = 0x07 # member function, virtual inheritance
    CV_PMTYPE_F_General = 0x08 # member function, most general


# enumeration for method properties
class CV_methodprop(object):
    CV_MTvanilla = 0x00
    CV_MTvirtual = 0x01
    CV_MTstatic = 0x02
    CV_MTfriend = 0x03
    CV_MTintro = 0x04
    CV_MTpurevirt = 0x05
    CV_MTpureintro = 0x06


# enumeration for virtual shape table entries
class CV_VTS_desc(object):
    CV_VTS_near = 0x00
    CV_VTS_far = 0x01
    CV_VTS_thin = 0x02
    CV_VTS_outer = 0x03
    CV_VTS_meta = 0x04
    CV_VTS_near32 = 0x05
    CV_VTS_far32 = 0x06
    CV_VTS_unused = 0x07


# enumeration for LF_LABEL address modes
class CV_LABEL_TYPE(object):
    CV_LABEL_NEAR = 0 # near return
    CV_LABEL_FAR = 4


# enumeration for LF_MODIFIER values
class CV_modifier(object):
    MOD_const = 0x0001
    MOD_volatile = 0x0002
    MOD_unaligned = 0x0004


# bit field structure describing class/struct/union/enum properties
class CV_prop(object):
    packed = 0x0001 # true if structure is packed
    ctor = 0x0002 # true if constructors or destructors present
    ovlops = 0x0004 # true if overloaded operators present
    isnested = 0x0008 # true if this is a nested class
    cnested = 0x0010 # true if this class contains nested types
    opassign = 0x0020 # true if overloaded assignment (=)
    opcast = 0x0040 # true if casting methods
    fwdref = 0x0080 # true if forward reference (incomplete defn)
    scoped = 0x0100


# class field attribute
class CV_fldattr(object):
    access = 0x0003 # access protection CV_access_t
    mprop = 0x001c # method properties CV_methodprop_t
    pseudo = 0x0020 # compiler generated fcn and does not exist
    noinherit = 0x0040 # true if class cannot be inherited
    noconstruct = 0x0080 # true if class cannot be constructed
    compgenx = 0x0100 # compiler generated fcn and does exist


# Structures to access to the type records
class TYPTYPE(object):
    def __init__(self):
        self.length = 0
        self.leaf = 0
        # byte data[];
        #  char *NextType (char * pType) {
        #  return (pType + ((TYPTYPE *)pType)->len + sizeof(ushort));
        #  } # general types record


# memory representation of pointer to member.  These representations are
# indexed by the enumeration above in the LF_POINTER record

# representation of a 32 bit pointer to data for a class with
# or without virtual functions and no virtual bases
class CV_PDMR32_NVVFCN(object):
    def __init__(self):
        self.mdisp = 0 # displacement to data (NULL = 0x80000000)


# representation of a 32 bit pointer to data for a class
# with virtual bases
class CV_PDMR32_VBASE(object):
    def __init__(self):
        self.mdisp = 0 # displacement to data
        self.pdisp = 0 # this pointer displacement
        self.vdisp = 0 # vbase table displacement
                       # NULL = (,,0xffffffff)


# representation of a 32 bit pointer to member function for a
# class with no virtual bases and a single address point
class CV_PMFR32_NVSA(object):
    def __init__(self):
        self.off = 0 # near address of function (NULL = 0L)


# representation of a 32 bit pointer to member function for a
# class with no virtual bases and multiple address points
class CV_PMFR32_NVMA(object):
    def __init__(self):
        self.off = 0 # near address of function (NULL = 0L,x)
        self.disp = 0


# representation of a 32 bit pointer to member function for a
# class with virtual bases
class CV_PMFR32_VBASE(object):
    def __init__(self):
        self.off = 0 # near address of function (NULL = 0L,x,x,x)
        self.mdisp = 0 # displacement to data
        self.pdisp = 0 # this pointer displacement
        self.vdisp = 0 # vbase table displacement


# The following type records are basically variant records of the
# above structure.  The "ushort leaf" of the above structure and
# the "ushort leaf" of the following type definitions are the same
# symbol.
#
# Notes on alignment
# Alignment of the fields in most of the type records is done on the
# basis of the TYPTYPE record base.  That is why in most of the lf*
# records that the type is located on what appears to
# be a offset mod 4 == 2 boundary.  The exception to this rule are those
# records that are in a list (lfFieldList, lfMethodList), which are
# aligned to their own bases since they don't have the length field
#

# Type record for LF_MODIFIER
class LeafModifier(object):
    def __init__(self):
        # leaf = LEAF.LF_MODIFIER      # LF_MODIFIER [TYPTYPE]
        self.type = 0 # (type index) modified type
        self.attr = CV_modifier() # modifier attribute modifier_t


# type record for LF_POINTER
class LeafPointerAttr(object):
    ptrtype = 0x0000001f # ordinal specifying pointer type (CV_ptrtype)
    ptrmode = 0x000000e0 # ordinal specifying pointer mode (CV_ptrmode)
    isflat32 = 0x00000100 # true if 0:32 pointer
    isvolatile = 0x00000200 # TRUE if volatile pointer
    isconst = 0x00000400 # TRUE if const pointer
    isunaligned = 0x00000800 # TRUE if unaligned pointer
    isrestrict = 0x00001000 # TRUE if restricted pointer (allow agressive opts)


# LeafPointer; wrapps this a an non used struct
class LeafPointerBody(object):
    def __init__(self):
        # self.leaf = LEAF.LF_POINTER # LF_POINTER [TYPTYPE]
        self.utype = 0 # (type index) type index of the underlying type
        self.attr = LeafPointerAttr()


# type record for LF_ARRAY
class LeafArray(object):
    def __init__(self):
        # self.leaf = LEAF.LF_ARRAY # LF_ARRAY [TYPTYPE]
        self.elemtype = 0 # (type index) type index of element type
        self.idxtype = 0 # (type index) type index of indexing type
        self.data = bytearray() # variable length data specifying size in bytes
        self.name = None # unicode


# type record for LF_CLASS, LF_STRUCTURE
class LeafClass(object):
    def __init__(self):
        # self.leaf = LEAF.LF_CLASS # LF_CLASS, LF_STRUCT [TYPTYPE]
        self.count = 0 # count of number of elements in class
        self.property = 0 # (CV_prop_t) property attribute field (prop_t)
        self.field = 0 # (type index) type index of LF_FIELD descriptor list
        self.derived = 0 # (type index) type index of derived from list if not zero
        self.vshape = 0 # (type index) type index of vshape table for this class
        self.data = bytearray() # data describing length of structure in bytes
        self.name = None # unicode


# type record for LF_UNION
class LeafUnion(object):
    def __init__(self):
        # self.leaf = LEAF.LF_UNION # LF_UNION [TYPTYPE]
        self.count = 0 # count of number of elements in class
        self.property = 0 # (CV_prop_t) property attribute field
        self.field = 0 # (type index) type index of LF_FIELD descriptor list
        self.data = bytearray() # variable length data describing length of
        self.name = None # unicode


# type record for LF_ALIAS
class LeafAlias(object):
    def __init__(self):
        # self.leaf = LEAF.LF_ALIAS # LF_ALIAS [TYPTYPE]
        self.utype = 0 # (type index) underlying type
        self.name = None # alias name - unicode


# type record for LF_MANAGED
class LeafManaged(object):
    def __init__(self):
        # self.leaf = LEAF.LF_MANAGED # LF_MANAGED [TYPTYPE]
        self.name = None # utf8, zero terminated managed type name - unicode


# type record for LF_ENUM
class LeafEnum(object):
    def __init__(self):
        # self.leaf = LEAF.LF_ENUM # LF_ENUM [TYPTYPE]
        self.count = 0 # count of number of elements in class
        self.property = 0 # (CV_propt_t) property attribute field
        self.utype = 0 # (type index) underlying type of the enum
        self.field = 0 # (type index) type index of LF_FIELD descriptor list
        self.name = None # length prefixed name of enum


# Type record for LF_PROCEDURE
class LeafProc(object):
    def __init__(self):
        # self.leaf = LEAF.LF_PROCEDURE # LF_PROCEDURE [TYPTYPE]
        self.tvtype = 0 # (type index) type index of return value
        self.callype = 0 # calling convention (CV_call_t)
        self.reserved = 0 # reserved for future use
        self.parmcount # number of parameters
        self.arglist # (type index) type index of argument list


# Type record for member function
class LeafMFunc(object):
    def __init__(self):
        # self.leaf = LEAF.LF_MFUNCTION # LF_MFUNCTION [TYPTYPE]
        self.rvtype = 0 # (type index) type index of return value
        self.classtype = 0 # (type index) type index of containing class
        self.reserved = 0 # (type index) type index of this pointer (model specific)
        self.calltype = 0 # calling convention (call_t)
        self.reserved = 0 # reserved for future use
        self.parmcount = 0 # number of parameters
        self.arglist = 0 # (type index) type index of argument list
        self.thisadjust = 0 # this adjuster (long because pad required anyway)


# Type record for virtual function table shape
class LeafVTShape(object):
    def __init__(self):
        # self.leaf = LEAF.LF_VTSHAPE # LF_VTSHAPE [TYPTYPE]
        self.count = 0 # number of entries in vfunctable
        self.desc = bytearray() # 4 bit (CV_VTS_desc) descriptors


# Type record for cobol0
class LeafCobol0(object):
    def __init__(self):
        # self.leaf = LEAF.LF_COBOL0 # LF_COBOL0 [TYPTYPE]
        self.type = 0 # (type index) parent type record index
        self.data = bytearray()


# Type record for cobol1
class LeafCobol1(object):
    def __init__(self):
        # self.leaf = LEAF.LF_COBOL1 # LF_COBOL1 [TYPTYPE]
        self.data = bytearray()


# Type record for basic array
class LeafBArray(object):
    def __init__(self):
        # self.leaf = LEAF.LF_BARRAY # LF_BARRAY [TYPTYPE]
        self.utype = 0 # (type index) type index of underlying type


# Type record for assembler labels
class LeafLabel(object):
    def __init__(self):
        # self.leaf = LEAF.LF_LABEL # LF_LABEL [TYPTYPE]
        self.mode = 0 # addressing mode of label


# Type record for dimensioned arrays
class LeafDimArray(object):
    def __init__(self):
        # self.leaf = LEAF.LF_DIMARRAY # LF_DIMARRAY [TYPTYPE]
        self.utype = 0 # (type index) underlying type of the array
        self.diminfo = 0 # (type index) dimension information
        self.name = None # length prefixed name


# Type record describing path to virtual function table
class LeafVFTPath(object):
    def __init__(self):
        # self.leaf = LEAF.LF_VFTPATH # LF_VFTPATH [TYPTYPE]
        self.count = 0 # count of number of bases in path
        self.bases = [] # (type index) bases from root to leaf


# Type record describing inclusion of precompiled types
class LeafPreComp(object):
    def __init__(self):
        # self.leaf = LEAF.LF_PRECOMP # LF_PRECOMP [TYPTYPE]
        self.start = 0 # starting type index included
        self.count = 0 # number of types in inclusion
        self.signature = 0 # signature
        self.name = None # length prefixed name of included type file


# Type record describing end of precompiled types that can be
# included by another file
class LeafEndPreComp(object):
    def __init__(self):
        # self.leaf = LEAF.LF_ENDPRECOMP # LF_ENDPRECOMP [TYPTYPE]
        self.signature = 0 # signature


# Type record for OEM definable type strings
class LeafOEM(object):
    def __init__(self):
        # self.leaf = LEAF.LF_OEM # LF_OEM [TYPTYPE]
        self.cv_oem = 0 # MS assigned OEM identified
        self.rec_oem  = 0 # OEM assigned type identifier
        self.count = 0 # count of type indices to follow
        self.index = [] # (type index) array of type indices followed


# by OEM defined data
class OEM_ID(object):
    OEM_MS_FORTRAN90 = 0xF090
    OEM_ODI = 0x0010
    OEM_THOMSON_SOFTWARE = 0x5453
    OEM_ODI_REC_BASELIST = 0x0000


class LeafOEM2(object):
    def __init__(self):
        # self.leaf = LEAF.LF_OEM2 # LF_OEM2 [TYPTYPE]
        self.id_oem = uuid.uuid() # an oem ID (Guid)
        self.count = 0 # count of type indices to follow
        self.index = [] # (type index) array of type indices followed
                        # by OEM defined data


# Type record describing using of a type server
class LeafTypeServer(object):
    def __init__(self):
        # self.leaf = LEAF.LF_TYPESERVER # LF_TYPESERVER [TYPTYPE]
        self.signature = 0 # signature
        self.age = 0 # age of database used by this module
        self.name = None # length prefixed name of PDB


# Type record describing using of a type server with v7 (GUID) signatures
class LeafTypeServer2(object):
    def __init__(self):
        # self.leaf = LEAF.LF_TYPESERVER2 # LF_TYPESERVER2 [TYPTYPE]
        self.sig70 = uuid.uuid() # guid signature
        self.age = 0 # age of database used by this module
        self.name = None # length prefixed name of PDB


# description of type records that can be referenced from
# type records referenced by symbols


# Type record for skip record
class LeafSkip(object):
    def __init__(self):
        # self.leaf = LEAF.LF_SKIP # LF_SKIP [TYPTYPE]
        self.type = 0 # (type index) next valid index
        self.data = [] # pad data


# Argument list leaf
class LeafArgList(object):
    def __init__(self):
        # self.leaf = LEAF.LF_ARGLIST # LF_ARGLIST [TYPTYPE]
        self.count = 0 # number of arguments
        self.arg = [] # (type index) number of arguments


# Derived class list leaf
class LeafDerived(object):
    def __init__(self):
        # self.leaf = LEAF.LF_DERIVED # LF_DERIVED [TYPTYPE]
        self.count = 0 # number of arguments
        self.drvdcls = [] # (type index) type indices of derived classes


# Leaf for default arguments
class LeafDefArg(object):
    def __init__(self):
        # self.leaf = LEAF.LF_DEFARG # LF_DEFARG [TYPTYPE]
        self.type = 0 # (type index) type of resulting expression
        self.expr = bytearray() # length prefixed expression string


# List leaf
#     This list should no longer be used because the utilities cannot
#     verify the contents of the list without knowing what type of list
#     it is.  New specific leaf indices should be used instead.
class LeafList(object):
    def __init__(self):
        # self.leaf = LEAF.LF_LIST # LF_LIST [TYPTYPE]
        self.data = bytearray() # data format specified by indexing type


# Field list leaf
# This is the header leaf for a complex list of class and structure
# subfields.
class LeafFieldList(object):
    def __init__(self):
        # self.leaf = LEAF.LF_FIELDLIST # LF_FIELDLIST [TYPTYPE]
        self.data = bytearray()


# Type record for non-static methods and friends in overloaded method list
class mlMethod(object):
    def __init__(self):
        self.attr = 0 # (CV_fldattr_t) method attribute
        self.pad0 = 0 # internal padding, must be 0
        self.index = 0 # (type index) index to type record for procedure
        self.vbaseoff = [] # offset in vfunctable if intro virtual


class LeafMethodList(object):
    def __init__(self):
        # self.leaf = LEAF.LF_METHODLIST # LF_METHODLIST [TYPTYPE]
        self.m_list = [] # really a mlMethod type


# Type record for LF_BITFIELD
class LeafBitfield(object):
    def __init__(self):
        # self.leaf = LEAF.LF_BITFIELD # LF_BITFIELD [TYPTYPE]
        self.type = 0 # (type index) type of bitfield
        self.length = 0
        self.position = 0


# Type record for dimensioned array with constant bounds
class LeafDimCon(object):
    def __init__(self):
        # self.leaf = LEAF.LF_DIMCONU # LF_DIMCONU or LF_DIMCONLU [TYPTYPE]
        self.typ = 0 # (type index) type of index
        self.rank = 0 # number of dimensions
        self.dim = [] # array of dimension information with
                      # either upper bounds or lower/upper bound


# Type record for dimensioned array with variable bounds
class LeafDimVar(object):
    def __init__(self):
        # self.leaf = LEAF.LF_DIMVARU # LF_DIMVARU or LF_DIMVARLU [TYPTYPE]
        self.rank = 0 # number of dimensions
        self.typ = 0 # (type index) type of index
        self.dim = [] # (type index) array of type indices for either
                      # variable upper bound or variable
                      # lower/upper bound.  The count of type
                      # indices is rank or rank*2 depending on
                      # whether it is LFDIMVARU or LF_DIMVARLU.
                      # The referenced types must be
                      # LF_REFSYM or T_VOID


# Type record for referenced symbol
class LeafRefSym(object):
    def __init__(self):
        # self.leaf = LEAF.LF_REFSYM # LF_REFSYM [TYPTYPE]
        self.sym = bytearray() # copy of referenced symbol record
                               # (including length)


# the following are numeric leaves.  They are used to indicate the
# size of the following variable length data.  When the numeric
# data is a single byte less than 0x8000, then the data is output
# directly.  If the data is more the 0x8000 or is a negative value,
# then the data is preceeded by the proper index.

# signed character leaf
class LeafChar(object):
    def __init__(self):
        # self.leaf = LEAF.LF_CHAR # LF_CHAR [TYPTYPE]
        self.val = 0 # signed 8-bit value


# signed short leaf
class LeafShort(object):
    def __init__(self):
        # self.leaf = LEAF.LF_SHORT # LF_SHORT [TYPTYPE]
        self.val = 0 # signed 16-bit value


# ushort leaf
class LeafUShort(object):
    def __init__(self):
        # self.leaf = LEAF.LF_ushort # LF_ushort [TYPTYPE]
        self.val = 0 # unsigned 16-bit value


# signed (32-bit) long leaf
class LeafLong(object):
    def __init__(self):
        # self.leaf = LEAF.LF_LONG # LF_LONG [TYPTYPE]
        self.val = 0 # signed 32-bit value


# uint leaf
class LeafULong(object):
    def __init__(self):
        # self.leaf = LEAF.LF_ULONG # LF_ULONG [TYPTYPE]
        self.val = 0 # unsigned 32-bit value


# signed quad leaf
class LeafQuad(object):
    def __init__(self):
        # self.leaf = LEAF.LF_QUAD # LF_QUAD [TYPTYPE]
        self.val = 0 # signed 64-bit value


# unsigned quad leaf
class LeafUQuad(object):
    def __init__(self):
        # self.leaf = LEAF.LF_UQUAD # LF_UQUAD [TYPTYPE]
        self.val = 0 # unsigned 64-bit value


# signed int128 leaf
class LeafOct(object):
    def __init__(self):
        # self.leaf = LEAF.LF_OCT # LF_OCT [TYPTYPE]
        self.val0 = 0 # signed 128-bit value
        self.val1 = 0 # signed 128-bit value

# unsigned int128 leaf
class LeafUOct(object):
    def __init__(self):
        # self.leaf = LEAF.LF_UOCT # LF_UOCT [TYPTYPE]
        self.val0 = 0 # unsigned 128-bit value
        self.val1 = 0 # unsigned 128-bit value


# real 32-bit leaf
class LeafReal32(object):
    def __init__(self):
        # self.leaf = LEAF.LF_REAL32 # LF_REAL32 [TYPTYPE]
        self.val = 0 # 32-bit real value


# real 64-bit leaf
class LeafReal64(object):
    def __init__(self):
        # self.leaf = LEAF.LF_REAL64 # LF_REAL64 [TYPTYPE]
        self.val = 0 # 64-bit real value


# real 80-bit leaf
class LeafReal80(object):
    def __init__(self):
        # self.leaf = LEAF.LF_REAL80 # LF_REAL80 [TYPTYPE]
        self.val = FLOAT10() # 80-bit real value


# real 128-bit leaf
class LeafReal128(object):
    def __init__(self):
        # self.leaf = LEAF.LF_REAL128 # LF_REAL128 [TYPTYPE]
        self.val0 = 0 # real 128-bit value
        self.val1 = 0 # real 128-bit value


# complex 32-bit leaf
class LeafCmplx32(object):
    def __init__(self):
        # self.leaf = LEAF.LF_COMPLEX32 # LF_COMPLEX32 [TYPTYPE]
        self.val_real = 0 # real component
        self.val_imag = 0 # imaginary component


# complex 64-bit leaf
class LeafCmplx64(object):
    def __init__(self):
        # self.leaf = LEAF.LF_COMPLEX64 # LF_COMPLEX64 [TYPTYPE]
        self.val_real = 0 # real component
        self.val_imag = 0 # imaginary component


# complex 80-bit leaf
class LeafCmplx80(object):
    def __init__(self):
        # self.leaf = LEAF.LF_COMPLEX80 # LF_COMPLEX80 [TYPTYPE]
        self.val_real = FLOAT10() # real component
        self.val_imag = FLOAT10() # imaginary component


# complex 128-bit leaf
class LeafCmplx128(object):
    def __init__(self):
        # self.leaf = LEAF.LF_COMPLEX128 # LF_COMPLEX128 [TYPTYPE]
        self.val0_real = 0
        self.val1_real = 0 # real component
        self.val0_imag = 0
        self.val1_imag = 0 # imaginary component


# variable length numeric field
class LeafVarString(object):
    def __init__(self):
        # self.leaf = LEAF.LF_VARSTRING # LF_VARSTRING [TYPTYPE]
        slf.length = 0 # length of value in bytes
        self.value = bytearray() # value


# index leaf - contains type index of another leaf
# a major use of this leaf is to allow the compilers to emit a
# long complex list (LF_FIELD) in smaller pieces.
class LeafIndex(object):
    def __init__(self):
        # self.leaf = LEAF.LF_INDEX # LF_INDEX [TYPTYPE]
        self.pad0 = 0 # internal padding, must be 0
        self.index = 0 # (type index) type index of referenced leaf


# subfield record for base class field
class LeafBClass(object):
    def __init__(self):
        # self.leaf = LEAF.LF_BCLASS # LF_BCLASS [TYPTYPE]
        self.attr = 0 # (CV_fldattr_t) attribute
        self.index = 0 # (type index) type index of base class
        self.offset = bytearray() # variable length offset of base within class


# subfield record for direct and indirect virtual base class field
class LeafVBClass(object):
    def __init__(self):
        # self.leaf = LEAF.LF_VBCLASS # LF_VBCLASS | LV_IVBCLASS [TYPTYPE]
        self.attr = 0 # (CV_fldattr_t) attribute
        self.index = 0 # (type index) type index of direct virtual base class
        self.vbptr = 0 # (type index) type index of virtual base pointer
        self.vbpoff = bytearray() # virtual base pointer offset from address point
                                  # followed by virtual base offset from vbtable


# subfield record for friend class
class LeafFriendCls(object):
    def __init__(self):
        # self.leaf = LEAF.LF_FRIENDCLS # LF_FRIENDCLS [TYPTYPE]
        self.pad0 = 0 # internal padding, must be 0
        self.index = 0 # (type index) index to type record of friend class


# subfield record for friend function
class LeafFriendFcn(object):
    def __init__(self):
        # self.leaf = LEAF.LF_FRIENDFCN # LF_FRIENDFCN [TYPTYPE]
        self.pad0 = 0 # internal padding, must be 0
        self.index = 0 # (type index) index to type record of friend function
        self.name = None # name of friend function


# subfield record for non-static data members
class LeafMember(object):
    def __init__(self):
        # self.leaf = LEAF.LF_MEMBER # LF_MEMBER [TYPTYPE]
        self.attr = 0 # (CV_fldattr_t)attribute mask
        self.index = 0 # (type index) index of type record for field
        self.offset = bytearray() # variable length offset of field
        self.name = None # length prefixed name of field


# type record for static data members
class LeafSTMember(object):
    def __init__(self):
        # self.leaf = LEAF.LF_STMEMBER # LF_STMEMBER [TYPTYPE]
        self.attr = 0 # (CV_fldattr_t) attribute mask
        self.index = 0 # (type index) index of type record for field
        self.name = None # length prefixed name of field


# subfield record for virtual function table pointer
class LeafVFuncTab(object):
    def __init__(self):
        # self.leaf = LEAF.LF_VFUNCTAB # LF_VFUNCTAB [TYPTYPE]
        self.pad0 = 0 # internal padding, must be 0
        self.type = 0 # (type index) type index of pointer


# subfield record for virtual function table pointer with offset
class LeafVFuncOff(object):
    def __init__(self):
        # self.leaf = LEAF.LF_VFUNCOFF # LF_VFUNCOFF [TYPTYPE]
        self.pad0 = 0 # internal padding, must be 0.
        self.type = 0 # (type index) type index of pointer
        self.offset = 0 # offset of virtual function table pointer


# subfield record for overloaded method list
class LeafMethod(object):
    def __init__(self):
        # self.leaf = LEAF.LF_METHOD # LF_METHOD [TYPTYPE]
        self.count = 0 # number of occurrences of function
        self.m_ist = 0 # (type index) index to LF_METHODLIST record
        self.name = None # length prefixed name of method


# subfield record for nonoverloaded method
class LeafOneMethod(object):
    def __init__(self):
       # self.leaf = LEAF.LF_ONEMETHOD # LF_ONEMETHOD [TYPTYPE]
       self.attr = 0 # (CV_fldattr_t) method attribute
       self.index = 0 # (type index) index to type record for procedure
       self.vbaseoff = [] # offset in vfunctable if intro virtual
       self.name = None


# subfield record for enumerate
class LeafEnumerate(object):
    def __init__(self):
       # self.leaf = LEAF.LF_ENUMERATE # LF_ENUMERATE [TYPTYPE]
       self.attr = 0 # (CV_fldattr_t) access
       self.value = bytearray() # variable length value field
       self.name = None


# type record for nested (scoped) type definition
class LeafNestType(object):
    def __init__(self):
        # self.leaf = LEAF.LF_NESTTYPE # LF_NESTTYPE [TYPTYPE]
        self.pad0 = 0 # internal padding, must be 0
        self.index = 0 # (type index) index of nested type definition
        self.name = None # length prefixed type name


# type record for nested (scoped) type definition, with attributes
# new records for vC v5.0, no need to have 16-bit ti versions.
class LeafNestTypeEx(object):
    def __init__(self):
       # self.leaf = LEAF.LF_NESTTYPEEX # LF_NESTTYPEEX [TYPTYPE]
       self.attr = 0 # (CV_fldattr_t) member access
       self.index = 0# (type index) index of nested type definition
       self.name = None # length prefixed type name


# type record for modifications to members
class LeafMemberModify(object):
    def __init__(self):
        # self.leaf = LEAF.LF_MEMBERMODIFY # LF_MEMBERMODIFY [TYPTYPE]
        self.attr = 0 # (CV_fldattr_t) the new attributes
        self.index = 0 # (type index) index of base class type definition
        self.name = None # length prefixed member name


# type record for pad leaf
class LeafPad(object):
    def __init__(self):
        self.leaf = 0


#  Symbol definitions
class SYM(object):
    S_END = 0x0006 # Block, procedure, "with" or thunk end
    S_OEM = 0x0404 # OEM defined symbol
    S_REGISTER_ST = 0x1001 # Register variable
    S_CONSTANT_ST = 0x1002 # constant symbol
    S_UDT_ST = 0x1003 # User defined type
    S_COBOLUDT_ST = 0x1004 # special UDT for cobol that does not symbol pack
    S_MANYREG_ST = 0x1005 # multiple register variable
    S_BPREL32_ST = 0x1006 # BP-relative
    S_LDATA32_ST = 0x1007 # Module-local symbol
    S_GDATA32_ST = 0x1008 # Global data symbol
    S_PUB32_ST = 0x1009 # a internal symbol (CV internal reserved)
    S_LPROC32_ST = 0x100a # Local procedure start
    S_GPROC32_ST = 0x100b # Global procedure start
    S_VFTABLE32 = 0x100c # address of virtual function table
    S_REGREL32_ST = 0x100d # register relative address
    S_LTHREAD32_ST = 0x100e # local thread storage
    S_GTHREAD32_ST = 0x100f # global thread storage
    S_LPROCMIPS_ST = 0x1010 # Local procedure start
    S_GPROCMIPS_ST = 0x1011 # Global procedure start
    
    # new symbol records for edit and continue information
    S_FRAMEPROC = 0x1012 # extra frame and proc information
    S_COMPILE2_ST = 0x1013 # extended compile flags and info
        
    # new symbols necessary for 16-bit enumerates of IA64 registers
    # and IA64 specific symbols
    S_MANYREG2_ST = 0x1014 # multiple register variable
    S_LPROCIA64_ST = 0x1015 # Local procedure start (IA64)
    S_GPROCIA64_ST = 0x1016 # Global procedure start (IA64)

    # Local symbols for IL
    S_LOCALSLOT_ST = 0x1017 # local IL sym with field for local slot index
    S_PARAMSLOT_ST = 0x1018 # local IL sym with field for parameter slot index
    S_ANNOTATION = 0x1019 # Annotation string literals

    # symbols to support managed code debugging
    S_GMANPROC_ST = 0x101a # Global proc
    S_LMANPROC_ST = 0x101b # Local proc
    S_RESERVED1 = 0x101c # reserved
    S_RESERVED2 = 0x101d # reserved
    S_RESERVED3 = 0x101e # reserved
    S_RESERVED4 = 0x101f # reserved
    S_LMANDATA_ST = 0x1020
    S_GMANDATA_ST = 0x1021
    S_MANFRAMEREL_ST = 0x1022
    S_MANREGISTER_ST = 0x1023
    S_MANSLOT_ST = 0x1024
    S_MANMANYREG_ST = 0x1025
    S_MANREGREL_ST = 0x1026
    S_MANMANYREG2_ST = 0x1027
    S_MANTYPREF = 0x1028 # Index for type referenced by name from metadata
    S_UNAMESPACE_ST = 0x1029 # Using namespace
    
    # Symbols w/ SZ name fields. All name fields contain utf8 encoded strings.
    S_ST_MAX = 0x1100 # starting point for SZ name symbols
    S_OBJNAME = 0x1101 # path to object file name
    S_THUNK32 = 0x1102 # Thunk Start
    S_BLOCK32 = 0x1103 # block start
    S_WITH32 = 0x1104 # with start
    S_LABEL32 = 0x1105 # code label
    S_REGISTER = 0x1106 # Register variable
    S_CONSTANT = 0x1107 # constant symbol
    S_UDT = 0x1108 # User defined type
    S_COBOLUDT = 0x1109 # special UDT for cobol that does not symbol pack
    S_MANYREG = 0x110a # multiple register variable
    S_BPREL32 = 0x110b # BP-relative
    S_LDATA32 = 0x110c # Module-local symbol
    S_GDATA32 = 0x110d # Global data symbol
    S_PUB32 = 0x110e # a internal symbol (CV internal reserved)
    S_LPROC32 = 0x110f # Local procedure start
    S_GPROC32 = 0x1110 # Global procedure start
    S_REGREL32 = 0x1111 # register relative address
    S_LTHREAD32 = 0x1112 # local thread storage
    S_GTHREAD32 = 0x1113 # global thread storage
    S_LPROCMIPS = 0x1114 # Local procedure start
    S_GPROCMIPS = 0x1115 # Global procedure start
    S_COMPILE2 = 0x1116 # extended compile flags and info
    S_MANYREG2 = 0x1117 # multiple register variable
    S_LPROCIA64 = 0x1118 # Local procedure start (IA64)
    S_GPROCIA64 = 0x1119 # Global procedure start (IA64)
    S_LOCALSLOT = 0x111a # local IL sym with field for local slot index
    S_SLOT = S_LOCALSLOT # alias for LOCALSLOT
    S_PARAMSLOT = 0x111b # local IL sym with field for parameter slot index
    
    # symbols to support managed code debugging
    S_LMANDATA = 0x111c
    S_GMANDATA = 0x111d
    S_MANFRAMEREL = 0x111e
    S_MANREGISTER = 0x111f
    S_MANSLOT = 0x1120
    S_MANMANYREG = 0x1121
    S_MANREGREL = 0x1122
    S_MANMANYREG2 = 0x1123
    S_UNAMESPACE = 0x1124 # Using namespace
    
    # ref symbols with name fields
    S_PROCREF = 0x1125 # Reference to a procedure
    S_DATAREF = 0x1126 # Reference to data
    S_LPROCREF = 0x1127 # Local Reference to a procedure
    S_ANNOTATIONREF = 0x1128 # Reference to an S_ANNOTATION symbol
    S_TOKENREF = 0x1129 # Reference to one of the many MANPROCSYM's
    
    # continuation of managed symbols
    S_GMANPROC = 0x112a # Global proc
    S_LMANPROC = 0x112b # Local proc
    
    # short, light-weight thunks
    S_TRAMPOLINE = 0x112c # trampoline thunks
    S_MANCONSTANT = 0x112d # constants with metadata type info
    
    # native attributed local/parms
    S_ATTR_FRAMEREL = 0x112e # relative to virtual frame ptr
    S_ATTR_REGISTER = 0x112f # stored in a register
    S_ATTR_REGREL = 0x1130 # relative to register (alternate frame ptr)
    S_ATTR_MANYREG = 0x1131 # stored in >1 register
    
    # Separated code (from the compiler) support
    S_SEPCODE = 0x1132
    S_LOCAL = 0x1133 # defines a local symbol in optimized code
    S_DEFRANGE = 0x1134 # defines a single range of addresses in which symbol can be evaluated
    S_DEFRANGE2 = 0x1135 # defines ranges of addresses in which symbol can be evaluated
    S_SECTION = 0x1136 # A COFF section in a PE executable
    S_COFFGROUP = 0x1137 # A COFF group
    S_EXPORT = 0x1138 # A export
    S_CALLSITEINFO = 0x1139 # Indirect call site information
    S_FRAMECOOKIE = 0x113a # Security cookie information
    S_DISCARDED = 0x113b # Discarded by LINK /OPT:REF (experimental, see richards)
    
    S_RECTYPE_MAX = 0x113c # one greater than last
    S_RECTYPE_LAST = S_RECTYPE_MAX - 1


# enum describing compile flag ambient data model
class CV_CFL_DATA(object):
    CV_CFL_DNEAR = 0x00
    CV_CFL_DFAR = 0x01
    CV_CFL_DHUGE = 0x02


# enum describing compile flag ambiant code model
class CV_CFL_CODE(object):
    CV_CFL_CNEAR = 0x00
    CV_CFL_CFAR = 0x01
    CV_CFL_CHUGE = 0x02


# enum describing compile flag target floating point package
class CV_CFL_FPKG(object):
    CV_CFL_NDP = 0x00
    CV_CFL_EMU = 0x01
    CV_CFL_ALT = 0x02


class CV_PROCFLAGS(object):
    # enum describing function return method
    CV_PFLAG_NOFPO = 0x01 # frame pointer present
    CV_PFLAG_INT = 0x02 # interrupt return
    CV_PFLAG_FAR = 0x04 # far return
    CV_PFLAG_NEVER = 0x08 # function does not return
    CV_PFLAG_NOTREACHED = 0x10 # label isn't fallen into
    CV_PFLAG_CUST_CALL = 0x20 # custom calling convention
    CV_PFLAG_NOINLINE = 0x40 # function marked as noinline
    CV_PFLAG_OPTDBGINFO = 0x80 # function has debug information for optimized code


# Extended proc flags
class CV_EXPROCFLAGS(object):
    def __init__(self):
        self.flags = 0 # (CV_PROCFLAGS)
        self.reserved = 0 # must be zero


# local variable flags
class CV_LVARFLAGS(object):
    fIsParam = 0x0001 # variable is a parameter
    fAddrTaken = 0x0002 # address is taken
    fCompGenx = 0x0004 # variable is compiler generated
    fIsAggregate = 0x0008 # the symbol is splitted in temporaries,
                          # which are treated by compiler as
                          # independent entities
    fIsAggregated = 0x0010 # Counterpart of fIsAggregate - tells
                           # that it is a part of a fIsAggregate symbol
    fIsAliased = 0x0020 # variable has multiple simultaneous lifetimes
    fIsAlias = 0x0040 # represents one of the multiple simultaneous lifetimes


# represents an address range, used for optimized code debug info
class CV_lvar_addr_range(object):
    def __init__(self):
        # defines a range of addresses
        self.off_start = 0
        self.isect_start = 0
        self.cb_range = 0


# enum describing function data return method
class CV_GENERIC_STYLE(object):
    CV_GENERIC_VOID = 0x00 # void return type
    CV_GENERIC_REG = 0x01 # return data is in registers
    CV_GENERIC_ICAN = 0x02 # indirect caller allocated near
    CV_GENERIC_ICAF = 0x03 # indirect caller allocated far
    CV_GENERIC_IRAN = 0x04 # indirect returnee allocated near
    CV_GENERIC_IRAF = 0x05 # indirect returnee allocated far
    CV_GENERIC_UNUSED = 0x06


class CV_GENERIC_FLAG(object):
    cstyle = 0x0001 # true push varargs right to left
    rsclean = 0x0002 # true if returnee stack cleanup


# flag bitfields for separated code attributes
class CV_SEPCODEFLAGS(object):
    fIsLexicalScope = 0x00000001 # S_SEPCODE doubles as lexical scope
    fReturnsToParent = 0x00000002 # code frag returns to parent


# Generic layout for symbol records
class SYMTYPE(object):
    def __init__(self):
        self.reclen = 0 # Record length
        self.rectyp = 0 # Record type
                        # byte        data[CV_ZEROLEN];
                        #  SYMTYPE *NextSym (SYMTYPE * pSym) {
                        #  return (SYMTYPE *) ((char *)pSym + pSym->reclen + sizeof(ushort));
                        #  }


# non-model specific symbol types
class RegSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_REGISTER # S_REGISTER
        self.typind = 0 # (type index) Type index or Metadata token
        self.reg = 0 # register enumerate
        self.name = None # Length-prefixed name


class AttrRegSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_MANREGISTER # S_MANREGISTER
        self.typind = 0 # (type index) Type index or Metadata token
        self.off_cod = 0 # first code address where var is live
        self.seg_cod = 0
        self.flags = 0 # (CV_LVARFLAGS)local var flags
        self.reg = 0 # register enumerate
        self.name = None # Length-prefixed name


class ManyRegSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_MANYREG # S_MANYREG
        self.typind = 0 # (type index) Type index or metadata token
        self.count = 0 # count of number of registers
        self.reg = [] # count register enumerates, most-sig first
        self.name = None # length-prefixed name.


class ManyRegSym2(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_MANYREG2 # S_MANYREG2
        self.typind = 0 # (type index) Type index or metadata token
        self.count = 0 # count of number of registers,
        self.reg = [] # count register enumerates, most-sig first
        self.name = None # length-prefixed name.


class AttrManyRegSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_MANMANYREG # S_MANMANYREG
        self.typind = 0 # (type index) Type index or metadata token
        self.off_cd = 0 # first code address where var is live
        self.seg_cod = 0
        self.flags = 0 # (CV_LVARFLAGS)local var flags
        self.count = 0 # count of number of registers
        self.reg = [] # count register enumerates, most-sig first
        self.name = None # utf-8 encoded zero terminate name


class AttrManyRegSym2(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_MANMANYREG2 # S_MANMANYREG2
        self.typind = 0 # (type index) Type index or metadata token
        self.off_cd = 0 # first code address where var is live
        self.seg_cod = 0
        self.flags = 0 # (CV_LVARFLAGS)local var flags
        self.count = 0 # count of number of registers
        self.reg = [] # count register enumerates, most-sig first
        self.name = None # utf-8 encoded zero terminate name


class ConstSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_CONSTANT # S_CONSTANT or S_MANCONSTANT
        self.typind = 0 # (type index) Type index (containing enum if enumerate) or metadata token
        self.value = 0 # numeric leaf containing value
        self.name = None # Length-prefixed name


class UdtSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_UDT # S_UDT | S_COBOLUDT
        self.typind = 0 # (type index) Type index
        self.name = None # Length-prefixed name


class ManyTypRef(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_MANTYPREF # S_MANTYPREF
        self.typind = 0 # (type index) Type index


class SearchSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_SSEARCH # S_SSEARCH
        self.startsym = 0 # offset of the procedure
        self.seg = 0 # segment of symbol


class CFLAGSYM_FLAGS(object):
    pcode = 0x0001 # true if pcode present
    floatprec = 0x0006 # floating precision
    floatpkg = 0x0018 # float package
    ambdata = 0x00e0 # ambient data model
    ambcode = 0x0700 # ambient code model
    mode32 = 0x0800  # true if compiled 32 bit mode


class CFlagSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_COMPILE # S_COMPILE
        self.machine = 0 # target processor
        self.language = 0 # language index
        self.flags = 0 # (CFLAGSYM_FLAGS)
        self.ver = None # Length-prefixed compiler version string


class COMPILESYM_FLAGS(object):
    iLanguage = 0x000000ff # language index
    fEC = 0x00000100 # compiled for E/C
    fNoDbgInfo = 0x00000200 # not compiled with debug info
    fLTCG = 0x00000400 # compiled with LTCG
    fNoDataAlign = 0x00000800 # compiled with -Bzalign
    fManagedPresent = 0x00001000 # managed code/data present
    fSecurityChecks = 0x00002000 # compiled with /GS
    fHotPatch = 0x00004000 # compiled with /hotpatch
    fCVTCIL = 0x00008000 # converted with CVTCIL
    fMSILModule = 0x00010000 # MSIL netmodule


class CompileSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_COMPILE2 # S_COMPILE2
        self.flags = 0 # (COMPILESYM_FLAGS)
        self.machine = 0 # target processor
        self.ver_fe_major = 0 # front end major version #
        self.ver_fe_minor = 0 # front end minor version #
        self.ver_fe_buld = 0 # front end build version #
        self.ver_major = 0 # back end major version #
        self.ver_minor = 0 # back end minor version #
        self.ver_build = 0 # back end build version #
        self.ver_st = None # Length-prefixed compiler version string, followed
        self.ver_args = [] # block of zero terminated strings, ended by double-zero.


class ObjNameSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_OBJNAME # S_OBJNAME
        self.signature = 0 # signature
        self.name = None # Length-prefixed name


class EndArgSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_ENDARG # S_ENDARG
        pass


class ReturnSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_RETURN # S_RETURN
        self.flags = 0 # flags
        self.style = 0 # CV_GENERIC_STYLE return style
                       # followed by return method data


class EntryThisSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_ENTRYTHIS # S_ENTRYTHIS
        self.thissym = 0 # symbol describing this pointer on entry


class BpRelSym32(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_BPREL32 # S_BPREL32
        self.off = 0 # BP-relative offset
        self.typind = 0 # (type index) Type index or Metadata token
        self.name = None # Length-prefixed name


class FrameRelSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_MANFRAMEREL # S_MANFRAMEREL | S_ATTR_FRAMEREL
        self.off = 0 # Frame relative offset
        self.typind = 0 # (type index) Type index or Metadata token
        self.off_cod = 0 # first code address where var is live
        self.seg_cod = 0
        self.flags = 0 # (CV_LVARFLAGS)local var flags
        self.name = None # Length-prefixed name


class SlotSym32(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_LOCALSLOT # S_LOCALSLOT or S_PARAMSLOT
        self.index = 0 # slot index
        self.typind = 0 # (type index) Type index or Metadata token
        self.name = None # Length-prefixed name


class AttrSlotSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_MANSLOT # S_MANSLOT
        self.index = 0 # slot index
        self.typind = 0 # (type index) Type index or Metadata token
        self.off_cod = 0 # first code address where var is live
        self.seg_cod = 0
        self.flags = 0 # (CV_LVARFLAGS)local var flags
        self.name = None # Length-prefixed name


class AnnotationSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_ANNOTATION # S_ANNOTATION
        self.off = 0
        self.seg = 0
        self.csz = 0 # Count of zero terminated annotation strings
        self.rgsz = [] # Sequence of zero terminated annotation strings


class DatasSym32(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_LDATA32 # S_LDATA32, S_GDATA32 or S_PUB32, S_LMANDATA, S_GMANDATA
        self.typind = 0 # (type index) Type index, or Metadata token if a managed symbol
        self.off = 0
        self.seg = 0
        self.name = None # Length-prefixed name


class CV_PUBSYMFLAGS(object):
    fNone = 0
    fCode = 0x00000001 # set if internal symbol refers to a code address
    fFunction = 0x00000002 # set if internal symbol is a function
    fManaged = 0x00000004 # set if managed code (native or IL)
    fMSIL = 0x00000008 # set if managed IL code


class PubSym32(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_PUB32 # S_PUB32
        self.flags = 0 # (CV_PUBSYMFLAGS)
        self.off = 0
        self.seg = 0
        self.name = None # Length-prefixed name


class ProcSym32(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_GPROC32 # S_GPROC32 or S_LPROC32
        self.parent = 0 # pointer to the parent
        self.end = 0 # pointer to this blocks end
        self.next = 0 # pointer to next symbol
        self.length = 0 # Proc length
        self.dbg_start = 0 # Debug start offset
        self.dbg_end = 0 # Debug end offset
        self.typind = 0 # (type index) Type index
        self.off = 0
        self.seg = 0
        self.flags = 0 # (CV_PROCFLAGS) Proc flags
        self.name = None # Length-prefixed name


class ManProcSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_GMANPROC # S_GMANPROC, S_LMANPROC, S_GMANPROCIA64 or S_LMANPROCIA64
        self.parent = 0 # pointer to the parent
        self.end = 0 # pointer to this blocks end
        self.next = 0 # pointer to next symbol
        self.length = 0 # Proc length
        self.dbg_start = 0 # Debug start offset
        self.dbg_end = 0 # Debug end offset
        self.token = 0 # COM+ metadata token for method
        self.off = 0 
        self.seg = 0 
        self.flags = 0 # (CV_PROCFLAGS) Proc flags
        self.ret_reg = 0 # Register return value is in (may not be used for all archs)
        self.name = None # optional name field


class ManProcSymMips(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_GMANPROCMIPS # S_GMANPROCMIPS or S_LMANPROCMIPS
        self.parent = 0 # pointer to the parent
        self.end = 0 # pointer to this blocks end
        self.next = 0 # pointer to next symbol
        self.length = 0 # Proc length
        self.dbg_start = 0 # Debug start offset
        self.dbg_end = 0 # Debug end offset
        self.reg_save = 0 # int register save mask
        self.fp_save = 0 # fp register save mask
        self.int_off = 0 # int register save offset
        self.fp_off = 0 # fp register save offset
        self.token = 0 # COM+ token type
        self.off = 0
        self.seg = 0
        self.ret_reg = 0 # Register return value is in
        self.frame_reg = 0 # Frame pointer register
        self.name = None # optional name field


class ThunkSym32(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_THUNK32 # S_THUNK32
        self.parent = 0 # pointer to the parent
        self.end = 0 # pointer to this blocks end
        self.next = 0 # pointer to next symbol
        self.off = 0
        self.seg = 0
        self.length = 0 # length of thunk
        self.ord = 0 # THUNK_ORDINAL specifying type of thunk
        self.name = None # Length-prefixed name
        self.variant = bytearray() # variant portion of thunk


class TRAMP(object):
    # Trampoline subtype
    tramp_incremental = 0 # incremental thunks
    tramp_branch_island = 1 # Branch island thunks


class TrampolineSym(object):
    def __init__(self):
        # Trampoline thunk symbol
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_TRAMPOLINE # S_TRAMPOLINE
        self.tramp_type = 0 # trampoline sym subtype
        self.cb_thunk = 0 # size of the thunk
        self.off_thunk = 0 # offset of the thunk
        self.off_target = 0 # offset of the target of the thunk
        self.sect_thunk = 0 # section index of the thunk
        self.srct_target = 0 # section index of the target of the thunk


class LabelSym32(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_LABEL32 # S_LABEL32
        self.off = 0
        self.seg = 0
        self.flags = 0 # (CV_PROCFLAGS) flags
        self.name = None # Length-prefixed name


class BlockSym32(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_BLOCK32 # S_BLOCK32
        self.parent = 0 # pointer to the parent
        self.end = 0 # pointer to this blocks end
        self.length = 0 # Block length
        self.off = 0 # Offset in code segment
        self.seg = 0 # segment of label
        self.name = None # Length-prefixed name


class WithSym32(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_WITH32 # S_WITH32
        self.parent = 0 # pointer to the parent
        self.end = 0 # pointer to this blocks end
        self.length = 0 # Block length
        self.off = 0 # Offset in code segment
        self.seg = 0 # segment of label
        self.expr = None # Length-prefixed expression string


class VpathSym32(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_VFTABLE32 # S_VFTABLE32
        self.root = 0 # (type index) type index of the root of path
        self.path = 0 # (type index) type index of the path record
        self.off = 0 # offset of virtual function table
        self.seg = 0 # segment of virtual function table


class RegRel32(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_REGREL32 # S_REGREL32
        self.off = 0 # offset of symbol
        self.typind = 0 # (type index) Type index or metadata token
        self.reg = 0 # register index for symbol
        self.name = None # Length-prefixed name


class AttrRegRel(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_MANREGREL # S_MANREGREL
        self.off = 0 # offset of symbol
        self.typind = 0 # (type index) Type index or metadata token
        self.ref = 0 # register index for symbol
        self.off_cod = 0 # first code address where var is live
        self.seg_cod = 0
        self.flags = 0 # (CV_LVARFLAGS)local var flags
        self.name = None # Length-prefixed name


class ThreadSym32(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_LTHREAD32 # S_LTHREAD32 | S_GTHREAD32
        self.typind = 0 # (type index) type index
        self.off = 0 # offset into thread storage
        self.seg = 0 # segment of thread storage
        self.name = None # length prefixed name


class Slink32(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_SLINK32 # S_SLINK32
        self.framesize = 0 # frame size of parent procedure
        self.off = 0 # signed offset where the static link was saved relative to the value of reg
        self.reg = 0


class ProcSymMips(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_GPROCMIPS # S_GPROCMIPS or S_LPROCMIPS
        self.parent = 0 # pointer to the parent
        self.end = 0 # pointer to this blocks end
        self.next = 0 # pointer to next symbol
        self.length = 0 # Proc length
        self.dbg_start = 0 # Debug start offset
        self.dbg_end = 0 # Debug end offset
        self.reg_save = 0 # int register save mask
        self.fp_save = 0 # fp register save mask
        self.int_off = 0 # int register save offset
        self.fp_off = 0 # fp register save offset
        self.typind = 0 # (type index) Type index
        self.off = 0 # Symbol offset
        self.seg = 0 # Symbol segment
        self.ret_reg = 0 # Register return value is in
        self.frame_reg = 0 # Frame pointer register
        self.name = None # Length-prefixed name


class ProcSymIa64(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_GPROCIA64 # S_GPROCIA64 or S_LPROCIA64
        self.parent = 0 # pointer to the parent
        self.end = 0 # pointer to this blocks end
        self.next = 0 # pointer to next symbol
        self.length = 0 # Proc length
        self.dbg_start = 0 # Debug start offset
        self.dbg_end = 0 # Debug end offset
        self.typind = 0 # (type index) Type index
        self.off = 0 # Symbol offset
        self.seg = 0 # Symbol segment
        self.ret_reg = 0 # Register return value is in
        self.flags = 0 # (CV_PROCFLAGS) Proc flags
        self.name = None # Length-prefixed name


class RefSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_PROCREF_ST # S_PROCREF_ST, S_DATAREF_ST, or S_LPROCREF_ST
        self.sum_num = 0 # SUC of the name
        self.ib_sym = 0 # Offset of actual symbol in $$Symbols
        self.imod = 0 # Module containing the actual symbol
        self.us_fill = 0 # align this record


class RefSym2(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_PROCREF # S_PROCREF, S_DATAREF, or S_LPROCREF
        self.sum_name = 0 # SUC of the name
        self.ib_sym = 0 # Offset of actual symbol in $$Symbols
        self.imod = 0 # Module containing the actual symbol
        self.name = None # hidden name made a first class member


class AlignSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_ALIGN # S_ALIGN
        pass


class OemSymbol(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_OEM # S_OEM
        self.id_oem = uuid.uuid() # an oem ID (GUID)
        self.typind = 0 # (type index) Type index
        self.rgl = [] # user data, force 4-byte alignment


class FRAMEPROCSYM_FLAGS(object):
    fHasAlloca = 0x00000001 # function uses _alloca()
    fHasSetJmp = 0x00000002 # function uses setjmp()
    fHasLongJmp = 0x00000004 # function uses longjmp()
    fHasInlAsm = 0x00000008 # function uses inline asm
    fHasEH = 0x00000010 # function has EH states
    fInlSpec = 0x00000020 # function was speced as inline
    fHasSEH = 0x00000040 # function has SEH
    fNaked = 0x00000080 # function is __declspec(naked)
    fSecurityChecks = 0x00000100 # function has buffer security check introduced by /GS.
    fAsyncEH = 0x00000200 # function compiled with /EHa
    fGSNoStackOrdering = 0x00000400 # function has /GS buffer checks, but stack ordering couldn't be done
    fWasInlined = 0x00000800 # function was inlined within another function


class FrameProcSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_FRAMEPROC # S_FRAMEPROC
        self.cb_frame = 0 # count of bytes of total frame of procedure
        self.cb_pad = 0 # count of bytes of padding in the frame
        self.off_pad = 0 # offset (rel to frame) to where padding starts
        self.cb_save_regs = 0 # count of bytes of callee save registers
        self.off_ex_hdlr = 0 # offset of exception handler
        self.sec_ex_hdlr = 0 # section id of exception handler
        self.flags = 0 # (FRAMEPROCSYM_FLAGS)


class UnamespaceSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_UNAMESPACE # S_UNAMESPACE
        self.name = None # name


class SepCodSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_SEPCODE # S_SEPCODE
        self.parent = 0 # pointer to the parent
        self.end = 0 # pointer to this block's end
        self.length = 0 # count of bytes of this block
        self.scf = 0 # (CV_SEPCODEFLAGS) flags
        self.off = 0 # sec:off of the separated code
        self.off_parent = 0 # secParent:offParent of the enclosing scope
        self.sec = 0 #  (proc, block, or sepcode)
        self.sec_parent = 0


class LocalSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_LOCAL # S_LOCAL
        self.id = 0 # id of the local
        self.typid = 0 # (type index) type index
        self.flags = 0 # (CV_LVARFLAGS) local var flags
        self.id_parent = 0 # This is is parent variable - fIsAggregated or fIsAlias
        self.off_parent = 0 # Offset in parent variable - fIsAggregated
        self.expr = 0 # NI of expression that this temp holds
        self.pad0 = 0 # pad, must be zero
        self.pad1 = 0 # pad, must be zero
        self.name = None # Name of this symbol.


class DefRangeSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_DEFRANGE # S_DEFRANGE
        self.id = 0 # ID of the local symbol for which this formula holds
        self.program = 0 # program to evaluate the value of the symbol
        self.range = CV_lvar_addr_range() # Range of addresses where this program is valid


class DefRangeSym2(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_DEFRANGE2 # S_DEFRANGE2
        self.id = 0 # ID of the local symbol for which this formula holds
        self.program = 0 # program to evaluate the value of the symbol
        self.count = 0 # count of CV_lvar_addr_range records following
        self.range = [] # Range of addresses where this program is valid


class SectionSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_SECTION # S_SECTION
        self.isec = 0 # Section number
        self.align = 0 # Alignment of this section (power of 2)
        self.b_reserved = 0 # Reserved.  Must be zero.
        self.rva = 0
        self.cb = 0
        self.characteristics = 0
        self.name = None # name


class CoffGroupSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_COFFGROUP # S_COFFGROUP
        self.cb = 0
        self.characteristics = 0
        self.off = 0 # Symbol offset
        self.seg = 0 # Symbol segment
        self.name = None # name


class EXPORTSYM_FLAGS(object):
    fConstant = 0x0001 # CONSTANT
    fData = 0x0002 # DATA
    fPrivate = 0x0004 # PRIVATE
    fNoName = 0x0008 # NONAME
    fOrdinal = 0x0010 # Ordinal was explicitly assigned
    fForwarder = 0x0020


 # This is a forwarder
class ExportSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_EXPORT # S_EXPORT
        self.ordinal = 0
        self.flags = 0 # (EXPORTSYM_FLAGS)
        self.name = None # name of


# Symbol for describing indirect calls when they are using
# a function pointer cast on some other type or temporary.
# Typical content will be an LF_POINTER to an LF_PROCEDURE
# type record that should mimic an actual variable with the
# function pointer type in question.
#
# Since the compiler can sometimes tail-merge a function call
# through a function pointer, there may be more than one
# S_CALLSITEINFO record at an address.  This is similar to what
# you could do in your own code by:
#
#  if (expr)
#  pfn = &function1;
#  else
#  pfn = &function2;
#
#  (*pfn)(arg list);

class CallsiteInfo(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_CALLSITEINFO # S_CALLSITEINFO
        self.off = 0 # offset of call site
        self.ect = 0 # section index of call site
        self.pad0 = 0 # alignment padding field, must be zero
        self.typind = 0 # (type index) type index describing function signature


# Frame cookie information
class CV_cookietype(object):
    CV_COOKIETYPE_COPY = 0
    CV_COOKIETYPE_XOR_SP = 1
    CV_COOKIETYPE_XOR_BP = 2
    CV_COOKIETYPE_XOR_R13 = 3


# Symbol for describing security cookie's position and type
# (raw, xor'd with esp, xor'd with ebp).
class FrameCookie(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_FRAMECOOKIE # S_FRAMECOOKIE
        self.off = 0 # Frame relative offset
        self.reg = 0 # Register index
        self.cookietype = 0 # (CV_cookietype) Type of the cookie
        self.flags = 0 # Flags describing this cookie


class CV_DISCARDED(object):
    CV_DISCARDED_UNKNOWN = 0
    CV_DISCARDED_NOT_SELECTED = 1
    CV_DISCARDED_NOT_REFERENCED = 2


class DiscardedSym(object):
    def __init__(self):
        # self.reclen = 0 # Record length [SYMTYPE]
        # self.rectyp = SYM.S_DISCARDED # S_DISCARDED
        self.iscarded = CV_DISCARDED() 
        self.fileid = 0 # First FILEID if line number info present
        self.linenum = 0 # First line number
        self.data = bytearray() # Original record(s) with invalid indices

#
# V7 line number data types
#
class DEBUG_S_SUBSECTION_TYPE(object):
    DEBUG_S_IGNORE = 0x80000000 # if this bit is set in a subsection type then ignore the subsection contents
    DEBUG_S_SYMBOLS = 0xf1
    DEBUG_S_LINES = 0xf2
    DEBUG_S_STRINGTABLE = 0xf3
    DEBUG_S_FILECHKSMS = 0xf4
    DEBUG_S_FRAMEDATA = 0xf5


#
# Line flags (data present)
#
class CV_LINE_SUBSECTION_FLAGS(object):
    CV_LINES_HAVE_COLUMNS = 0x0001


class CV_LineSection(object):
    def __init__(self):
        self.off = 0
        self.sec = 0
        self.flags = 0
        self.cod = 0


class CV_SourceFile(object):
    def __init__(self):
        self.index = 0 # Index to file in checksum section.
        self.count = 0 # Number of CV_Line records.
        self.linsiz = 0 # Size of CV_Line recods.


class CV_Line_Flags(object):
    linenum_start = 0x00ffffff # line where statement/expression starts
    delta_line_end = 0x7f000000 # delta to line where statement ends (optional)
    f_statement = 0x80000000 # true if a statement linenumber, else an expression line num


class CV_Line(object):
    def __init__(self):
        self.offset = 0 # Offset to start of code bytes for line number
        self.flags = 0 # (CV_Line_Flags)


class CV_Column(object):
    def __init__(self):
        self.off_column_start = 0
        self.off_column_end = 0


#  File information
class CV_FILE_CHECKSUM_TYPE(object):
    NONE = 0
    MD5 = 1


class CV_FileCheckSum(object):
    def __init__(self):
        self.name = 0 # Index of name in name table.
        self.length = 0 # Hash length
        self.type = 0 # Hash type


class FRAMEDATA_FLAGS(object):
    fHasSEH = 0x00000001
    fHasEH = 0x00000002
    fIsFunctionStart = 0x00000004


class FrameData(object):
    def __init__(self):
        self.ul_rva_start = 0
        self.cb_block = 0
        self.cb_locals = 0
        self.cb_params = 0
        self.cb_stk_max = 0
        self.frame_func = 0
        self.cb_prolog = 0
        self.cb_saved_regs = 0
        self.flags = 0 # (FRAMEDATA_FLAGS)


class XFixupData(object):
    def __init__(self):
        self.w_type = 0
        self.e_extra = 0
        self.rva = 0
        self.rva_target = 0


class DEBUG_S_SUBSECTION(object):
    SYMBOLS = 0xF1
    LINES = 0xF2
    STRINGTABLE = 0xF3
    FILECHKSMS = 0xF4
    FRAMEDATA = 0xF5

    INLINEELINES = 0xF6 # DEBUG_S_INLINEELINES
    CROSSSCOPEIMPORTS = 0xF7 # DEBUG_S_CROSSSCOPEIMPORTS
    CROSSSCOPEEXPORTS = 0xF8 # DEBUG_S_CROSSSCOPEEXPORTS
    IL_LINES = 0xF9 # DEBUG_S_IL_LINES





