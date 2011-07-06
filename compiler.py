#!/usr/bin/env python3
"""
Compile a basic file to a class file.
"""

import re
import struct
import sys

from class_file import ClassFile

def create_code(file_name, message):
    """Write the compile code to a class file"""
    code = ClassFile(file_name.capitalize(), file_name)
    method_bytecode = b"\x2a\xb7" + struct.pack("!h", 
        code.add_method_to_const_pool("java/lang/Object", "<init>", "()V")
    ) + b"\xb1"
    code.add_method(0x0000, "<init>", "()V", 1, 1, method_bytecode)
    
    method_bytecode = b"\xb2" + struct.pack("!h", code.add_field_to_const_pool("java/lang/System", "out", "Ljava/io/PrintStream;")) + b"\x12" + struct.pack("B", code.add_string_ref_to_const_pool(message)) + b"\xb6" + struct.pack("!h", code.add_method_to_const_pool("java/io/PrintStream", "println", "(Ljava/lang/String;)V")) + b"\xb1"
    code.add_method(0x0009, "main", "([Ljava/lang/String;)V", 2, 1, method_bytecode)
    
    open(file_name.capitalize() + ".class", "wb").write(code.write_class())

def parse(code):
    """Parse basic file. Supports comments, empty lines and static print statements"""
    messages = []
    for line in code.split("\n"):
        line = re.sub(r"'(.*)$", "", line).strip()
        match = re.match(r'^PRINT[\s]+"(.*)"$',line, re.I)
        if match:
            messages.append(match.groups()[0])
    return "\n".join(messages)

def main():
    """Main function. Compiles a basic file to a class file."""
    if len(sys.argv) != 2:
        print("Usage: %s file.bas" % (sys.argv[0]))
        sys.exit(1)
    message = parse(open(sys.argv[1]).read())
    create_code(sys.argv[1].replace(".bas",""), message)

if __name__ == "__main__":
    main()
