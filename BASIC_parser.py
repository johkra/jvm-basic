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
    return [re.compile(r"^'.*"), re.compile(r"^REM.*")]

def string():
    return '"', re.compile(r'[^"]*'), '"'

def print_statement():
    return keyword("PRINT"), string

def statement():
    return [print_statement]

def statements():
    return -1, statement

def BASIC():
    return statements

def parse_to_AST(code):
    """Parse BASIC file. Returns pyAST."""
    return parse(BASIC, code, skipComments=comment)
