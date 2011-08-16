"""
Parse BASIC source to AST
"""

import re

from lib.pyPEG import parse, keyword, _and, _not

#def comment():          return [re.compile(r"//.*"), re.compile("/\*.*?\*/", re.S)]
#def literal():          return re.compile(r'\d*\.\d*|\d+|".*?"')
#def symbol():           return re.compile(r"\w+")
#def operator():         return re.compile(r"\+|\-|\*|\/|\=\=")
#def operation():        return symbol, operator, [literal, functioncall]
#def expression():       return [literal, operation, functioncall]
#def expressionlist():   return expression, -1, (",", expression)
#def returnstatement():  return keyword("return"), expression
#def ifstatement():      return keyword("if"), "(", expression, ")", block, keyword("else"), block
#def statement():        return [ifstatement, returnstatement], ";"
#def block():            return "{", -2, statement, "}"
#def parameterlist():    return "(", symbol, -1, (",", symbol), ")"
#def functioncall():     return symbol, "(", expressionlist, ")"
#def function():         return keyword("function"), symbol, parameterlist, block
#def simpleLanguage():   return function

def comment():
    return [re.compile(r"'.*"), re.compile(r"REM.*"), re.S]

def numeric_variable():
    return re.compile(r'\w+%')

def string_variable():
    return re.compile(r'\w+\$')

def numeric():
    return re.compile(r'\d+.\d+|\d+')

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

def statement():
    return [print_statement, assignment]

def statements():
    return -1, statement

def BASIC():
    return statements

def parse_to_AST(code):
    """Parse BASIC file. Returns pyAST."""
    return parse(BASIC, code, skipWS=True, skipComments=comment)
