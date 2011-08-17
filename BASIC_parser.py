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

def boolean():
    return re.compile(r"TRUE|FALSE")

def numeric():
    return re.compile(r'-?\d+')

def string():
    return '"', re.compile(r'[^"]*'), '"'

def _numeric_simple_value():
    return [numeric, numeric_variable]

def operator():
    return re.compile(r"\+|-|\*|/|\^")

def numeric_expression():
    return _numeric_simple_value, -2, (operator, _numeric_value)

def _string_value():
    return [string, string_variable]

def _numeric_value():
    return [numeric_expression, _numeric_simple_value]

def _boolean_value():
    return [boolean, boolean_conditional]

def _value():
    return [_boolean_value, _string_value, _numeric_value]

def numeric_assignment():
    return (numeric_variable, "=", _numeric_value)

def string_assignment():
    return (string_variable, "=" , _string_value)

def assignment():
    return [numeric_assignment, string_assignment]

def comparator():
    return re.compile(r"==|<>|>=|<=|>|<")

def boolean_conditional():
    return _numeric_value, comparator, _numeric_value

def if_statement():
    return keyword("IF"), boolean_conditional, keyword("THEN"), statements, keyword("ENDIF")

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
