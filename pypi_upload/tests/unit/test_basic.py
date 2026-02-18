"""Test basic ShiboScript functionality"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from shiboscript.core import Interpreter, Lexer, Parser

def test_basic_interpreter():
    """Test that the interpreter can be instantiated"""
    interpreter = Interpreter()
    assert interpreter is not None
    assert hasattr(interpreter, 'env')
    assert 'len' in interpreter.env

def test_lexer():
    """Test basic lexing functionality"""
    code = 'var x = 42'
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    assert len(tokens) > 0
    assert tokens[0][0] == 'VAR'

def test_parser():
    """Test basic parsing functionality"""
    code = 'var x = 42'
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    assert ast is not None
    assert hasattr(ast, 'statements')

def test_simple_execution():
    """Test executing simple code"""
    interpreter = Interpreter()
    
    # Test simple arithmetic
    code = '2 + 3'
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    result = interpreter.eval(ast)
    assert result == 5

if __name__ == "__main__":
    test_basic_interpreter()
    test_lexer()
    test_parser()
    test_simple_execution()
    print("All tests passed!")