"""
ShiboScript - A Python-like scripting language implementation
"""

from .core import (
    Lexer, Parser, Interpreter, ShiboClass, ShiboInstance,
    run_file, repl, eval_expression, get_ast, disassemble_bytecode,
    compile_file, run_compiled_bytecode, ShiboVM, BytecodeGenerator,
    Optimizer, ShiboModule, ShiboPackageManager, ShiboCompilerBackend
)
from .compiler import ShiboCompiler, ShiboScriptCompiler

__version__ = "1.0.0"
__author__ = "Shiboscript Team"
__all__ = [
    'Lexer', 'Parser', 'Interpreter', 'ShiboClass', 'ShiboInstance',
    'run_file', 'repl', 'eval_expression', 'get_ast', 'disassemble_bytecode',
    'compile_file', 'run_compiled_bytecode', 'ShiboVM', 'BytecodeGenerator',
    'Optimizer', 'ShiboModule', 'ShiboPackageManager', 'ShiboCompilerBackend',
    'ShiboCompiler', 'ShiboScriptCompiler'
]