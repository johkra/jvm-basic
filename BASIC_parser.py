"""
Parse BASIC source to AST
"""

import re

from lib.pyPEG import parse, keyword, _and, _not

def _comment():
    return [re.compile(r"'.*"), re.compile(r"REM.*"), re.S]

def numeric_variable():
    return re.compile(r'\w+%')

def string_variable():
    return re.compile(r'\w+\$')

def numeric():
    return re.compile(r'-?\d+')

def string():
    return '"', re.compile(r'[^"]*'), '"'

def _string_value():
    return [string_variable, string]

def _numeric_value():
    return [numeric_variable, numeric]

def _value():
    return [_string_value, _numeric_value]

def numeric_assignment():
    return (numeric_variable, "=", _numeric_value)

def string_assignment():
    return (string_variable, "=" , _string_value)

def assignment():
    return [numeric_assignment, string_assignment]

def print_statement():
    return keyword("PRINT"), _value

def _statement():
    return [print_statement, assignment]

def statements():
    return -1, _statement

def BASIC():
    return statements

def parse_to_AST(code):
    """Parse BASIC file. Returns pyAST."""
    return parse(BASIC, code, skipWS=True, skipComments=_comment)
