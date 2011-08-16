#!/usr/bin/env python3
"""
Compile a basic file to a class file.
"""

import fileinput
import pprint
import struct
import sys

from class_file import ClassFile
from BASIC_parser import parse_to_AST
from lib.pyPEG import Symbol

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

class Compiler:
    def __init__(self, functions):
        self.functions = functions

    def parse(self, _fileinput):
        self.AST = parse_to_AST(_fileinput)
        self._tree_walker(self.AST)

    def _tree_walker(self, tree):
        if type(tree) == list:
            for node in tree:
                self._tree_walker(node)
        if type(tree) == Symbol:
            for function in self.functions:
                if function.__name__ == tree.__name__:
                    function(tree.what)
            self._tree_walker(tree.what)

def main():
    """Main function. Compiles a basic file to a class file."""
    if len(sys.argv) != 2:
        print("Usage: %s file.bas" % (sys.argv[0]))
        sys.exit(1)
    messages = []
    def print_statement(args):
        string_value = args[0].what[0]
        if string_value.__name__ == "string":
            messages.append(string_value.what[0])
    compiler = Compiler([print_statement])
    compiler.parse(fileinput.input())
    message = "\n".join(messages)
    create_code(sys.argv[1].replace(".bas",""), message)

if __name__ == "__main__":
    main()
