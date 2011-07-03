#!/usr/bin/env python3
"""
Create a a java class file.
"""

import struct

class ClassFile:
    """Class to create a java class file."""
    constant_pool = []
    interfaces = []
    fields = []
    methods = []
    attributes = []

    ASCIZ = 0x01
    CLASS = 0x07
    STRREF = 0x08
    FIELD = 0x09
    METHOD = 0x0a
    NAME_AND_TYPE = 0x0c

    def __init__(self, class_name, source_file):
        """"Initialize class by giving the class name and the source file."""
        self.this_class_idx = self.add_class_to_const_pool(class_name)
        self.super_class_idx = self.add_class_to_const_pool("java/lang/Object")
        self.add_string_ref_attribute("SourceFile", source_file)
    
    def add_string_ref_attribute(self, name, value):
        """Add a string reference attribute to the attributes section of the
        class.
        """
        name_idx = self.add_string_to_const_pool(name)
        value_idx = self.add_string_to_const_pool(value)
        self.attributes.append((name_idx, value_idx))
    
    def _find_string_in_const_pool(self, string):
        """Private. Find the index of a string in the constant pool.
        Return the index or None. Indices start with 1.
        """
        for idx, constant in enumerate(self.constant_pool, 1):
            const_type, value = constant
            if const_type == self.ASCIZ and value == string:
                return idx
        return None

    def _add_const_to_const_pool(self, const):
        """Private. Add a constant to the constant pool. Return the index."""
        self.constant_pool.append( const )
        return len(self.constant_pool)

    def add_string_to_const_pool(self, string):
        """Add a string to the constant pool. Return the index."""
        idx = self._find_string_in_const_pool(string)
        if not idx:
            idx = self._add_const_to_const_pool((self.ASCIZ, string))
        return idx

    def _add_asciz_ref_to_const_pool(self, const_type, string):
        """Private. Add a reference to a string for a constant type to the
        constant pool. Return the index.
        """
        idx = self.add_string_to_const_pool(string)
        return self._add_const_to_const_pool((const_type, idx))

    def add_string_ref_to_const_pool(self, string):
        """Add a string reference to the constant pool. Return the index."""
        return self._add_asciz_ref_to_const_pool(self.STRREF, string)

    def add_name_and_type_to_const_pool(self, name, type_name):
        """Add Name and Type to constant pool. Return the index."""
        name_idx = self.add_string_to_const_pool(name)
        type_idx = self.add_string_to_const_pool(type_name)
        const = (self.NAME_AND_TYPE, (name_idx, type_idx))
        return self._add_const_to_const_pool(const)

    def add_class_to_const_pool(self, class_name):
        """Add class to constant pool. Return the index."""
        return self._add_asciz_ref_to_const_pool(self.CLASS, class_name)

    def add_field_to_const_pool(self, class_name, name, type_name):
        """Add field to constant pool. Return the index."""
        class_idx = self.add_class_to_const_pool(class_name)
        name_type_idx = self.add_name_and_type_to_const_pool(name, type_name)
        const = (self.FIELD, (class_idx, name_type_idx))
        return self._add_const_to_const_pool(const)

    def add_method_to_const_pool(self, class_name, name, type_name):
        """Add method to constant pool. Return the index."""
        class_idx = self.add_class_to_const_pool(class_name)
        name_type_idx = self.add_name_and_type_to_const_pool(name, type_name)
        const = (self.METHOD, (class_idx, name_type_idx))
        return self._add_const_to_const_pool(const)

    def _write_constant_pool(self):
        """Private. Write the binary representation of the constant pool."""
        const_pool = b""
        for const in self.constant_pool:
            const_type, value = const
            const_pool += struct.pack("B", const_type)
            if type(value) == str:
                value = value.encode("utf8")
                const_pool += struct.pack("!h", len(value))
                const_pool += value
            if type(value) == int:
                const_pool += struct.pack("!h", value)
            if type(value) == tuple:
                const_pool += struct.pack("!h", value[0])
                const_pool += struct.pack("!h", value[1])
        return const_pool

    def _write_attributes(self):
        """Private. Write the binary representation of the attributes."""
        attributes = b""
        for attribute in self.attributes:
            name_idx, value_idx = attribute
            attributes += struct.pack("!h", name_idx)
            attributes += struct.pack("!i", 2)
            attributes += struct.pack("!h", value_idx)
        return attributes


    def write_class(self):
        """Write the binary representation of the class. Returns a bytes string.
        """
        code = b""
        # Magic bytes
        code += struct.pack("!I", 0xcafebabe)
        # Class file format minor version
        code += struct.pack("!h", 0)
        # Class file format. 50 = java 1.6
        code += struct.pack("!h", 50)
        # Constant pool count = # of entries + 1
        code += struct.pack("!h", len(self.constant_pool) + 1)
        # Constant pool
        code += self._write_constant_pool()
        # Access flags
        code += struct.pack("!h", 0)
        # this class, index in constant pool
        code += struct.pack("!h", self.this_class_idx)
        # super class, index in constant pool
        code += struct.pack("!h", self.super_class_idx)
        # Interface count = # of entries in interface table
        code += struct.pack("!h", len(self.interfaces))
        # Interface table
        code += b""
        # Field count = # of entries in field table
        code += struct.pack("!h", len(self.fields))
        # Field table
        code += b""
        # Method count
        code += struct.pack("!h", len(self.methods))
        # Method table
        code += b""
        # Attribute count
        code += struct.pack("!h", len(self.attributes))
        # Attribute table
        code += self._write_attributes()
        return code

def main():
    """Main function. Creates a test class file."""
    code = ClassFile("Jhello", "jhello.java")
    
    open("Test.class", "wb").write(code.write_class())

if __name__ == "__main__":
    main()
