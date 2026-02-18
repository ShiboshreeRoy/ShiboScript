"""ShiboScript - A lightweight scripting language for education and automation"""

__title__ = "shiboscript"
__description__ = "A lightweight scripting language for education and automation"
__version__ = "1.0.0"
__author__ = "ShiboShreeRoy"
__license__ = "MIT"
__copyright__ = "Copyright 2023-2026 ShiboShreeRoy"

# Import main components
from .core import Interpreter, Lexer, Parser, repl, run_file

__all__ = [
    "Interpreter",
    "Lexer", 
    "Parser",
    "repl",
    "run_file",
    "__version__"
]
