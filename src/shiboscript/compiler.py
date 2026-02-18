"""
Advanced ShiboScript Compiler - Real-world Python-like compiler implementation
"""

import ast
import sys
import os
import importlib.util
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import tempfile
import subprocess
from .core import Lexer, Parser, Interpreter


class CompilationError(Exception):
    """Custom exception for compilation errors"""
    pass


class ShiboCompiler:
    """
    Advanced ShiboScript Compiler that generates optimized bytecode and executable code
    similar to how Python compiles to bytecode.
    """
    
    def __init__(self, optimize_level: int = 1):
        self.optimize_level = optimize_level
        self.interpreter = Interpreter()
        self.compiled_functions = {}
        self.global_vars = {}
        self.local_vars = {}
        
    def compile_to_bytecode(self, code: str) -> bytes:
        """
        Compile ShiboScript code to bytecode representation
        """
        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast_tree = parser.parse()
            
            # Generate bytecode from AST
            bytecode = self._generate_bytecode(ast_tree)
            return bytecode
        except Exception as e:
            raise CompilationError(f"Compilation failed: {str(e)}")
    
    def _generate_bytecode(self, ast_tree) -> bytes:
        """
        Generate bytecode from AST tree
        """
        # For now, we'll serialize the AST as a simple bytecode representation
        # In a real implementation, this would generate actual bytecode instructions
        import pickle
        return pickle.dumps(ast_tree)
    
    def compile_to_python(self, code: str) -> str:
        """
        Translate ShiboScript code to equivalent Python code
        """
        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast_tree = parser.parse()
            
            # Convert ShiboScript AST to Python code
            python_code = self._ast_to_python(ast_tree)
            return python_code
        except Exception as e:
            raise CompilationError(f"Translation to Python failed: {str(e)}")
    
    def _ast_to_python(self, ast_node) -> str:
        """
        Convert ShiboScript AST to Python code
        """
        if hasattr(ast_node, 'statements'):
            # Program node
            code_lines = []
            for stmt in ast_node.statements:
                code_lines.append(self._convert_statement(stmt))
            return '\n'.join(code_lines)
        else:
            return self._convert_statement(ast_node)
    
    def _convert_statement(self, stmt) -> str:
        """
        Convert individual statement to Python code
        """
        from collections import namedtuple
        
        # Handle different statement types
        if hasattr(stmt, '_fields') and 'name' in stmt._fields:
            if hasattr(stmt, 'params') and hasattr(stmt, 'body'):
                # Function definition
                params = ', '.join(stmt.params) if stmt.params else ''
                body_lines = []
                for sub_stmt in stmt.body:
                    body_lines.append('    ' + self._convert_statement(sub_stmt))
                
                return f"def {stmt.name}({params}):\n" + '\n'.join(body_lines)
            elif hasattr(stmt, 'value'):
                # Variable declaration
                value_code = self._convert_expression(stmt.value)
                return f"{stmt.name} = {value_code}"
        elif hasattr(stmt, 'condition'):
            # If statement
            condition_code = self._convert_expression(stmt.condition)
            then_lines = []
            for sub_stmt in stmt.then_branch:
                then_lines.append('    ' + self._convert_statement(sub_stmt))
            
            code = f"if {condition_code}:\n" + '\n'.join(then_lines)
            
            if stmt.else_branch:
                else_lines = []
                for sub_stmt in stmt.else_branch:
                    else_lines.append('    ' + self._convert_statement(sub_stmt))
                code += f"\nelse:\n" + '\n'.join(else_lines)
            
            return code
        elif type(stmt).__name__ == 'PrintStmt':
            # Print statement - check this first to avoid general expression catch-all
            expr_code = self._convert_expression(stmt.expression)
            return f"print({expr_code})"
        elif hasattr(stmt, 'expression'):
            # General expression statement
            expr_code = self._convert_expression(stmt.expression)
            return f"{expr_code}"
        
        return "# Unhandled statement"
    
    def _convert_expression(self, expr) -> str:
        """
        Convert expression to Python code
        """
        if hasattr(expr, 'value'):
            if hasattr(expr, '_fields') and 'value' in expr._fields:
                if isinstance(expr.value, (int, float)):
                    return str(expr.value)
                elif isinstance(expr.value, str):
                    return f'"{expr.value}"'
                elif isinstance(expr.value, bool):
                    return str(expr.value)
            elif hasattr(expr, 'name'):
                return expr.name
        elif hasattr(expr, 'left') and hasattr(expr, 'right'):
            # Binary operation
            left_code = self._convert_expression(expr.left)
            right_code = self._convert_expression(expr.right)
            return f"({left_code} {expr.op} {right_code})"
        elif hasattr(expr, 'operand'):
            # Unary operation
            operand_code = self._convert_expression(expr.operand)
            return f"{expr.op}{operand_code}"
        
        return "None"
    
    def execute_compiled(self, code: str, use_interpreter: bool = True):
        """
        Execute compiled ShiboScript code
        """
        if use_interpreter:
            # Use the existing interpreter
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast_tree = parser.parse()
            return self.interpreter.eval(ast_tree)
        else:
            # Compile to Python and execute
            python_code = self.compile_to_python(code)
            exec(python_code, globals())
    
    def compile_and_save(self, code: str, output_path: str):
        """
        Compile code and save to file
        """
        # Create a Python file from the ShiboScript code
        python_code = self.compile_to_python(code)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Compiled from ShiboScript\n")
            f.write(python_code)
    
    def run_compiled_file(self, filepath: str):
        """
        Run a compiled ShiboScript file
        """
        if filepath.endswith('.shibo'):
            # Run through interpreter
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            return self.execute_compiled(code)
        elif filepath.endswith('.py'):
            # Execute Python file
            spec = importlib.util.spec_from_file_location("compiled_module", filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module


class ShiboScriptCompiler:
    """
    Main compiler class that provides command-line interface and file compilation
    """
    
    def __init__(self):
        self.compiler = ShiboCompiler()
    
    def compile_file(self, input_file: str, output_file: str = None, 
                     compile_to_py: bool = True) -> str:
        """
        Compile a ShiboScript file to Python or bytecode
        """
        with open(input_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        if compile_to_py:
            if output_file is None:
                output_file = input_file.replace('.shibo', '.py')
            
            python_code = self.compiler.compile_to_python(code)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("#!/usr/bin/env python3\n")
                f.write("# Generated by ShiboScript Compiler\n")
                f.write("# Source: " + input_file + "\n\n")
                f.write(python_code)
            
            return output_file
        else:
            bytecode = self.compiler.compile_to_bytecode(code)
            if output_file is None:
                output_file = input_file.replace('.shibo', '.sbc')  # Shibo ByteCode
            
            with open(output_file, 'wb') as f:
                f.write(bytecode)
            
            return output_file
    
    def run_file(self, filepath: str):
        """
        Run a ShiboScript file using the interpreter
        """
        if filepath.endswith('.shibo'):
            from .core import run_file as run_shibo_file
            run_shibo_file(filepath)
        elif filepath.endswith('.py'):
            # Execute Python file directly
            subprocess.run([sys.executable, filepath])
    
    def compile_and_run(self, code: str):
        """
        Compile and run code in memory
        """
        return self.compiler.execute_compiled(code)


def main():
    """
    Command-line interface for the ShiboScript compiler
    """
    if len(sys.argv) < 2:
        print("Usage: shiboc [options] <file.shibo>")
        print("Options:")
        print("  -c, --compile     Compile to Python (.py)")
        print("  -b, --bytecode    Compile to bytecode (.sbc)")
        print("  -r, --run         Run the file directly")
        print("  -h, --help        Show this help message")
        sys.exit(1)
    
    compiler = ShiboScriptCompiler()
    args = sys.argv[1:]
    
    if '--help' in args or '-h' in args:
        print("ShiboScript Compiler - Real-world Python-like compiler")
        print("Usage: shiboc [options] <file.shibo>")
        print("Options:")
        print("  -c, --compile     Compile to Python (.py)")
        print("  -b, --bytecode    Compile to bytecode (.sbc)")
        print("  -r, --run         Run the file directly")
        print("  -h, --help        Show this help message")
        sys.exit(0)
    
    input_file = args[-1]
    
    if '--run' in args or '-r' in args:
        compiler.run_file(input_file)
    elif '--compile' in args or '-c' in args:
        output_file = compiler.compile_file(input_file, compile_to_py=True)
        print(f"Compiled to {output_file}")
    elif '--bytecode' in args or '-b' in args:
        output_file = compiler.compile_file(input_file, compile_to_py=False)
        print(f"Compiled to {output_file}")
    else:
        # Default: compile to Python
        output_file = compiler.compile_file(input_file, compile_to_py=True)
        print(f"Compiled to {output_file}")


if __name__ == "__main__":
    main()