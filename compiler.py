#!/usr/bin/env python3

# Do the simplest thing which might possibly work

import struct

code = b""
constant_pool_size = 0
interface_count = 0
field_count = 0
method_count = 0
attribute_count = 0

# Magic bytes
code += struct.pack("!I", 0xcafebabe)
# Class file format minor version
code += struct.pack("!h", 0)
# Class file format. 50 = java 1.6
code += struct.pack("!h", 50)
# Constant pool count = # of entries + 1
code += struct.pack("!h", constant_pool_size + 1)
# Constant pool
code += b""
# Access flags
code += struct.pack("!h", 0)
# this class, index in constant pool
code += struct.pack("!h", 0)
# super class, index in constant pool
code += struct.pack("!h", 0)
# Interface count = # of entries in interface table
code += struct.pack("!h", interface_count)
# Interface table
code += b""
# Field count = # of entries in field table
code += struct.pack("!h", field_count)
# Field table
code += b""
# Method count
code += struct.pack("!h", method_count)
# Method table
code += b""
# Attribute count
code += struct.pack("!h", attribute_count)
# Attribute table
code += b""


print(code)
"""
cafebabe # magic bytes
0000 # minor version
0032 # major version
001d # 29 -> 28 entries in constant pool
0a # (1) method reference
0006 # Class reference index
000f # Name and type descriptor index
09 # (2) field reference
0010 # Class reference index
0011 # Name and type descriptor index
08 # (3) String refence
0012 # Index of string 
0a # (4) method reference
0013 # class idx
0014 # name idx
07 # (5) class reference
0015 # 21 str idx
07 # (6)
0016 # 21 str idx
01 # (7) str
0006 # str length
3c 69 6e 69 74 3e # <init>
01 # (8) str
0003 # str len
28 29 56 # ()V
01 # (9) str
0004 # str len
43 6f 64 65 # Code
01 # (10)
000f # 15 str len
4c 69 6e 65 4e 75 6d 62 65 72 54 61 62 6c 65 # LineNumberTable
01 # (11)
0004 #
6d 61 69 6e # main
01 # (12)
0016 # 22
28 5b 4c 6a 61 76 61 2f 6c 61 6e 67 2f 53 74 72 69 6e 67 3b 29 56 # ([Ljava/lang/String;)V
01 # (13)
000a # 10
53 6f 75 72 63 65 46 69 6c 65 # SourceFile
01 # (14)
000b # 11
6a 68 65 6c 6c 6f 2e 6a 61 76 61 # jhello.java
0c # (15) Name and type
0007 # idx name
0008 # idx type
07 # (16) Class ref
0017 # ref to 23
0c # (17)
0018 # ref to 24
0019 # ref to 25
01 # (18)
000c # 12
48 65 6c 6c 6f 2c 20 77 6f 72 6c 64 # Hello, world
07 # (19)
001a # ref to 26
0c # (20)
001b # 27
001c # 28
01 # (21)
0006 # 
4a 68 65 6c 6c 6f # Jhello
01 # (22)
0010 # 16
6a 61 76 61 2f 6c 61 6e 67 2f 4f 62 6a 65 63 74 # java/lang/Object
01 # (23)
0010 # 16
6a 61 76 61 2f 6c 61 6e 67 2f 53 79 73 74 65 6d # java/lang/System
01 # (24)
0003 #
6f 75 74 # out
01 # (25)
0015 # 21
4c 6a 61 76 61 2f 69 6f 2f 50 72 69 6e 74 53 74 72 65 61 6d 3b # Ljava/io/PrintStream;
01 # (26)
0013 # 19
6a 61 76 61 2f 69 6f 2f 50 72 69 6e 74 53 74 72 65 61 6d # java/io/PrintStream
01 # (27)
0007 #
70 72 69 6e 74 6c 6e # println
01 # (28)
0015 # 21 
28 4c 6a 61 76 61 2f 6c 61 6e 67 2f 53 74 72 69 6e 67 3b 29 56 # (Ljava/lang/String;)V
0020 # access flag -> ACC_SUPER
0005 # this class index
0006 # super class index
0000 # interface count
0000 # field count
0002 # method count
0000 # access flags
0007 # str idx
0008 # descriptor idx
0001 # attributes count
0009 # name idx
0000001d # 29 attribute length
00 01 00 01 00 00 00 05 2a b7 00 01 b1 00 00 00 01 00 0a 00 00 00 06 00 01 00 00 00 01
0009 # access flags public static
000b # 11 str idx
000c # 12 desc idx
0001 # attr count
0009 # name idx
00000025 # 37
00 02 00 01 00 00 00 09 b2 00 02 12 03 b6 00 04 b1 00 00 00 01 00 0a 00 00 00 0a 00 02 00 00 00 03 00 08 00 04
0001 # attribute count
000d # attr name idx 13
00000002 # attribute length
000e # value
"""
