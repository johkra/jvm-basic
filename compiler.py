#!/usr/bin/env python3
"""
Compile a basic file to a class file.
"""

import fileinput
import re
import struct
import sys

from class_file import ClassFile
from BASIC_parser import parse_to_AST
from lib.pyPEG import Symbol

ALOAD = b"\x19"
ASTORE = b"\x3a"
GETSTATIC = b"\xb2"
GOTO = b"\xa7"
IADD = b"\x60"
IDIV = b"\x6c"
IF_ICMPEQ = b"\x9f"
IF_ICMPNE = b"\xa0"
IF_ICMPGE = b"\xa2"
IF_ICMPGT = b"\xa3"
IF_ICMPLE = b"\xa4"
IF_ICMPLT = b"\xa1"
IFEQ = b"\x99"
IINC = b"\x84"
ILOAD = b"\x15"
IMUL = b"\x68"
INVOKESTATIC = b"\xb8"
INVOKEVIRTUAL = b"\xb6"
ISTORE = b"\x36"
ISUB = b"\x64"
LDC = b"\x12"
SIPUSH = b"\x11"

def create_code(file_name, message):
    """Write the compile code to a class file"""

class Compiler:
    def __init__(self, file_name, functions):
        self.file_name = file_name.replace(".bas","")
        self.class_name = self.file_name.capitalize()
        self.functions = functions
        self.code = ClassFile(self.class_name, self.file_name)
        self.method_bytecode = b""
        self.vars = {"args": 0};

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
                    function(self, tree.what)
            self._tree_walker(tree.what)

    def _add_var(self, var_name):
        if var_name in self.vars:
            return self.vars[var_name]
        idx = len(self.vars)
        self.vars[var_name] = idx
        return idx

    def save(self):
        method_bytecode = b"\x2a\xb7" + struct.pack("!h",
            self.code.add_method_to_const_pool("java/lang/Object", "<init>", "()V")
        ) + b"\xb1"
        self.code.add_method(0x0000, "<init>", "()V", 1, 1, method_bytecode)
        self.method_bytecode += b"\xb1"
        # TODO: Keep track of stack size
        self.code.add_method(0x0009, "main", "([Ljava/lang/String;)V", 100, len(self.vars), self.method_bytecode)

        open(self.class_name + ".class", "wb").write(self.code.write_class())

def get_var_idx(self, node):
    try:
        var_idx = self.vars[node.what]
    except KeyError:
        print("Unknown variable '%s' in %s" % (node.what, node.__name__.line))
        sys.exit(-1)
    return var_idx

def load_string_value(self, node):
    if re.match(r"^numeric", node.__name__):
        bytecode = load_int_value(self, node)
        method_int_to_string = self.code.add_method_to_const_pool("java/lang/Integer", "toString", "(I)Ljava/lang/String;")
        bytecode += INVOKESTATIC + struct.pack("!h", method_int_to_string)
        return bytecode
    if re.match(r"^boolean", node.__name__):
        bytecode = load_boolean_value(self, node)
        method_int_to_string = self.code.add_method_to_const_pool("java/lang/Integer", "toString", "(I)Ljava/lang/String;")
        bytecode += INVOKESTATIC + struct.pack("!h", method_int_to_string)
        return bytecode
    if node.__name__ == "string":
        print_value = self.code.add_string_ref_to_const_pool(node.what[0])
        return LDC + struct.pack("B", print_value)
    return ALOAD + struct.pack("B", get_var_idx(self, node))

def load_boolean_value(self, node):
    if node.__name__ == "boolean":
        return SIPUSH + struct.pack("!h", int(node.what == "TRUE"))
    comparator = node.what[1].what
    comparators = {
        "==": IF_ICMPEQ,
        "<>": IF_ICMPNE,
        "<=": IF_ICMPLE,
        ">=": IF_ICMPGE,
        "<": IF_ICMPLT,
        ">": IF_ICMPGT,
    }
    bytecode  = load_int_value(self, node.what[0])
    bytecode += load_int_value(self, node.what[2])
    bytecode += comparators[comparator] + struct.pack("!h", 9)
    bytecode += SIPUSH + struct.pack("!h", 0)
    bytecode += GOTO + struct.pack("!h", 6)
    bytecode += SIPUSH + struct.pack("!h", 1)
    return bytecode

def load_int_value(self, node, fix_left_precedence=False):
    if node.__name__ == "numeric":
        value = int(node.what)
        try:
            bytecode = SIPUSH + struct.pack("!h", value)
        except struct.error:
            print("Numeric constant %d is outside allowed range (-32768..32767) in %s" % (value, node.__name__.line))
            sys.exit(-1)
        return bytecode
    if node.__name__ == "numeric_variable":
        return ILOAD + struct.pack("B", get_var_idx(self, node))
    operator = node.what[1].what

    if operator == "^":
        var_name = "tmp"
        self._add_var(var_name)
        bytecode_load_base  = load_int_value(self, node.what[0])

        bytecode  = SIPUSH + struct.pack("!h", 1)
        term = load_int_value(self, node.what[2], fix_left_precedence=True)
        if type(term) == tuple:
            bytecode += term[0]
        else:
            bytecode += term
        bytecode += ISTORE + struct.pack("B", self.vars[var_name])
        bytecode += ILOAD + struct.pack("B", self.vars[var_name])
        bytecode += IFEQ + struct.pack("!h", 10 + len(bytecode_load_base))
        bytecode += bytecode_load_base
        bytecode += IMUL
        bytecode += IINC + struct.pack("Bb", self.vars[var_name], -1)
        bytecode += GOTO + struct.pack("!h", - (9 + len(bytecode_load_base)))
        if type(term) == tuple:
            bytecode += term[1]
        return bytecode

    operators = {
        "+": IADD,
        "-": ISUB,
        "*": IMUL,
        "/": IDIV
    }

    bytecode  = load_int_value(self, node.what[0])
    term = load_int_value(self, node.what[2], fix_left_precedence=True)
    bytecode2 = term
    if type(term) == tuple:
        bytecode2 = term[0]
    bytecode2 += operators[operator]
    if type(term) == tuple:
        bytecode2 += term[1]
    if fix_left_precedence and operator not in ["*", "/"]:
        return (bytecode, bytecode2)
    return bytecode+bytecode2

def print_statement(self, args):
    field_print_stream = self.code.add_field_to_const_pool("java/lang/System", "out", "Ljava/io/PrintStream;")

    method_print_stream = self.code.add_method_to_const_pool("java/io/PrintStream", "println", "(Ljava/lang/String;)V")
    self.method_bytecode += GETSTATIC + struct.pack("!h", field_print_stream)
    self.method_bytecode += load_string_value(self, args[0])
    self.method_bytecode += INVOKEVIRTUAL + struct.pack("!h", method_print_stream)

def string_assignment(self, args):
    var_name = args[0].what
    var = self._add_var(var_name)
    self.method_bytecode += load_string_value(self, args[1])
    self.method_bytecode += ASTORE + struct.pack("B", self.vars[var_name])

def numeric_assignment(self, args):
    var_name = args[0].what
    var = self._add_var(var_name)
    self.method_bytecode += load_int_value(self, args[1])
    self.method_bytecode += ISTORE + struct.pack("B", self.vars[var_name])

def main():
    """Main function. Compiles a basic file to a class file."""
    if len(sys.argv) != 2:
        print("Usage: %s file.bas" % (sys.argv[0]))
        sys.exit(1)
    messages = []

    file_name = sys.argv[1]
    compiler = Compiler(file_name, [print_statement, string_assignment, numeric_assignment])
    compiler.parse(fileinput.input())
    compiler.save()

if __name__ == "__main__":
    main()
