import re
from collections import namedtuple
from PIL import Image
import math
import sys
import urllib.request
import urllib.parse
import base64
import hashlib
import subprocess
import os
import random
import string
import json
import time
import datetime

# ANSI Color Codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Helper Functions
def http_get(url, headers=None, params=None):
    if params:
        url += '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req) as response:
        return {'status': response.status, 'text': response.read().decode('utf-8')}

def http_post(url, data, headers=None):
    data = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers or {})
    with urllib.request.urlopen(req) as response:
        return {'status': response.status, 'text': response.read().decode('utf-8')}

def base64_encode(s): return base64.b64encode(s.encode('utf-8')).decode('utf-8')
def base64_decode(s): return base64.b64decode(s).decode('utf-8')
def md5(s): return hashlib.md5(s.encode('utf-8')).hexdigest()
def sha1(s): return hashlib.sha1(s.encode('utf-8')).hexdigest()
def sha256(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()
def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
def get_env(var): return os.environ.get(var)
def set_env(var, value): os.environ[var] = value
def get_cwd(): return os.getcwd()
def change_dir(path): os.chdir(path)
def list_dir(path): return os.listdir(path)
def exists(path): return os.path.exists(path)
def random_int(min_val, max_val): return random.randint(min_val, max_val)
def random_string(length): return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
def parse_url(url):
    parsed = urllib.parse.urlparse(url)
    return {'scheme': parsed.scheme, 'netloc': parsed.netloc, 'path': parsed.path, 'query': urllib.parse.parse_qs(parsed.query), 'fragment': parsed.fragment}
def url_encode(s): return urllib.parse.quote(s)
def url_decode(s): return urllib.parse.unquote(s)
def json_encode(obj): return json.dumps(obj)
def json_decode(s): return json.loads(s)
def time_now(): return time.time()
def time_sleep(seconds): time.sleep(seconds)

# Token Types
operator_pattern = r'>>>=|>>>|<<=|<<|>>=|>>|\+=|-=|\*=|/=|%=|&=|\|=|\^=|\+\+|--|==|!=|<=|>=|&&|\|\||//|[+\-*/%=<>!&|^~?:]'
TOKENS = [
    ('IMPORT', r'\bimport\b'), ('FROM', r'\bfrom\b'), ('CLASS', r'\bclass\b'), ('INTERFACE', r'\binterface\b'),
    ('IMPLEMENTS', r'\bimplements\b'), ('VAR', r'\bvar\b'), ('FUNC', r'\bfunc\b'), ('IF', r'\bif\b'), ('ELSE', r'\belse\b'),
    ('WHILE', r'\bwhile\b'), ('DO', r'\bdo\b'), ('FOR', r'\bfor\b'), ('IN', r'\bin\b'),
    ('BREAK', r'\bbreak\b'), ('CONTINUE', r'\bcontinue\b'), ('PRINT', r'\bprint\b'),
    ('RETURN', r'\breturn\b'), ('TRY', r'\btry\b'), ('CATCH', r'\bcatch\b'),
    ('TRUE', r'\btrue\b'), ('FALSE', r'\bfalse\b'), ('NULL', r'\bnull\b'),
    ('SET', r'\bset\b'),
    ('INSTANCEOF', r'\binstanceof\b'),
    ('NUMBER', r'\d+\.\d*|\.\d+|\d+'), ('STRING', r'"[^"]*"'), ('IDENTIFIER', r'[a-zA-Z_]\w*'),
    ('OPERATOR', operator_pattern),
    ('LPAREN', r'\('), ('RPAREN', r'\)'), ('LBRACE', r'\{'), ('RBRACE', r'\}'),
    ('LBRACKET', r'\['), ('RBRACKET', r'\]'), ('COMMA', r','), ('COLON', r':'),
    ('SEMI', r';'), ('DOT', r'\.'), ('NEWLINE', r'\n'),
]

# AST Nodes
Program = namedtuple('Program', ['statements'])
ImportStmt = namedtuple('ImportStmt', ['module'])
FromImportStmt = namedtuple('FromImportStmt', ['module', 'names'])
ClassDef = namedtuple('ClassDef', ['name', 'base', 'interfaces', 'body'])
InterfaceDef = namedtuple('InterfaceDef', ['name', 'methods'])
VarDecl = namedtuple('VarDecl', ['name', 'value'])
FuncDef = namedtuple('FuncDef', ['name', 'params', 'body'])
TryStmt = namedtuple('TryStmt', ['try_block', 'catch_var', 'catch_block'])
IfStmt = namedtuple('IfStmt', ['condition', 'then_branch', 'else_branch'])
WhileStmt = namedtuple('WhileStmt', ['condition', 'body'])
DoWhileStmt = namedtuple('DoWhileStmt', ['body', 'condition'])
ForStmt = namedtuple('ForStmt', ['init', 'condition', 'increment', 'body'])
ForInStmt = namedtuple('ForInStmt', ['var', 'iterable', 'body'])
BreakStmt = namedtuple('BreakStmt', [])
ContinueStmt = namedtuple('ContinueStmt', [])
PrintStmt = namedtuple('PrintStmt', ['expression'])
ReturnStmt = namedtuple('ReturnStmt', ['expression'])
ExprStmt = namedtuple('ExprStmt', ['expression'])
AssignStmt = namedtuple('AssignStmt', ['target', 'value'])
BinaryOp = namedtuple('BinaryOp', ['left', 'op', 'right'])
UnaryOp = namedtuple('UnaryOp', ['op', 'operand'])
PrefixOp = namedtuple('PrefixOp', ['op', 'operand'])
PostfixOp = namedtuple('PostfixOp', ['operand', 'op'])
TernaryOp = namedtuple('TernaryOp', ['condition', 'true_expr', 'false_expr'])
FuncCall = namedtuple('FuncCall', ['func_expr', 'args'])
ListLiteral = namedtuple('ListLiteral', ['elements'])
DictLiteral = namedtuple('DictLiteral', ['pairs'])
SetLiteral = namedtuple('SetLiteral', ['elements'])
Identifier = namedtuple('Identifier', ['name'])
Number = namedtuple('Number', ['value'])
String = namedtuple('String', ['value'])
Boolean = namedtuple('Boolean', ['value'])
Null = namedtuple('Null', [])
IndexExpr = namedtuple('IndexExpr', ['object', 'index'])
Slice = namedtuple('Slice', ['start', 'end'])
AttributeExpr = namedtuple('AttributeExpr', ['object', 'attribute'])

# Exceptions
class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

# Lexer
class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.tokens = []
        self.line = 1
        
    def tokenize(self):
        while self.pos < len(self.code):
            if self.code[self.pos] == '#':
                while self.pos < len(self.code) and self.code[self.pos] != '\n':
                    self.pos += 1
                continue
            match = None
            for token_type, pattern in TOKENS:
                regex = re.compile(pattern)
                match = regex.match(self.code, self.pos)
                if match:
                    value = match.group(0)
                    if token_type == 'NEWLINE':
                        self.line += 1
                        if not self.tokens or self.tokens[-1][0] != 'NEWLINE':
                            self.tokens.append((token_type, value, self.line))
                    else:
                        self.tokens.append((token_type, value, self.line))
                    self.pos = match.end()
                    break
            if not match:
                if self.code[self.pos].isspace():
                    self.pos += 1
                else:
                    raise SyntaxError(f"Line {self.line}: Unexpected character '{self.code[self.pos]}'")
        return self.tokens

# Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        
    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def advance(self):
        self.pos += 1
    
    def expect(self, token_type, value=None, optional=False):
        token = self.current_token()
        if token and token[0] == token_type and (value is None or token[1] == value):
            self.advance()
            return True
        elif optional and (token is None or token[0] == 'NEWLINE'):
            return True
        line = token[2] if token else "unknown"
        raise SyntaxError(f"Line {line}: Expected {token_type} {value or ''}, got {token}")
    
    def parse(self):
        return self.parse_program()
    
    def parse_program(self):
        statements = []
        while self.current_token():
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            if self.current_token() and self.current_token()[0] in ('NEWLINE', 'SEMI'):
                self.advance()
        return Program(statements)
    
    def parse_statement(self):
        while self.current_token() and self.current_token()[0] == 'NEWLINE':
            self.advance()
        token = self.current_token()
        if not token:
            return None
        if token[0] == 'IMPORT':
            return self.parse_import_stmt()
        elif token[0] == 'FROM':
            return self.parse_from_import_stmt()
        elif token[0] == 'CLASS':
            return self.parse_class_def()
        elif token[0] == 'INTERFACE':
            return self.parse_interface_def()
        elif token[0] == 'VAR':
            return self.parse_var_decl()
        elif token[0] == 'FUNC':
            return self.parse_func_def()
        elif token[0] == 'TRY':
            return self.parse_try_stmt()
        elif token[0] == 'IF':
            return self.parse_if_stmt()
        elif token[0] == 'WHILE':
            return self.parse_while_stmt()
        elif token[0] == 'DO':
            return self.parse_do_while_stmt()
        elif token[0] == 'FOR':
            return self.parse_for_stmt()
        elif token[0] == 'BREAK':
            self.advance()
            self.expect('SEMI', optional=True)
            return BreakStmt()
        elif token[0] == 'CONTINUE':
            self.advance()
            self.expect('SEMI', optional=True)
            return ContinueStmt()
        elif token[0] == 'PRINT':
            return self.parse_print_stmt()
        elif token[0] == 'RETURN':
            return self.parse_return_stmt()
        else:
            expr = self.parse_expression()
            if self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in ('=', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '>>>='):
                op = self.current_token()[1]
                self.advance()
                value = self.parse_expression()
                if isinstance(expr, (Identifier, IndexExpr, AttributeExpr)):
                    if op == '=':
                        return AssignStmt(expr, value)
                    else:
                        base_op = op[:-1]
                        return AssignStmt(expr, BinaryOp(expr, base_op, value))
                raise SyntaxError("Invalid assignment target")
            self.expect('SEMI', optional=True)
            return ExprStmt(expr)
    
    def parse_import_stmt(self):
        self.advance()
        module = self.current_token()[1]
        self.advance()
        self.expect('SEMI', optional=True)
        return ImportStmt(module)
    
    def parse_from_import_stmt(self):
        self.advance()
        module = self.current_token()[1]
        self.advance()
        self.expect('IMPORT', 'import')
        if self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] == '*':
            self.advance()
            names = ['*']
        else:
            names = []
            while self.current_token() and self.current_token()[0] == 'IDENTIFIER':
                names.append(self.current_token()[1])
                self.advance()
                if self.current_token() and self.current_token()[0] == 'COMMA':
                    self.advance()
        self.expect('SEMI', optional=True)
        return FromImportStmt(module, names)
    
    def parse_class_def(self):
        self.advance()
        name = self.current_token()[1]
        self.advance()
        base = None
        interfaces = []
        if self.current_token() and self.current_token()[0] == 'LPAREN':
            self.advance()
            base = self.current_token()[1]
            self.advance()
            self.expect('RPAREN', ')')
        if self.current_token() and self.current_token()[0] == 'IMPLEMENTS':
            self.advance()
            while self.current_token() and self.current_token()[0] == 'IDENTIFIER':
                interfaces.append(self.current_token()[1])
                self.advance()
                if self.current_token() and self.current_token()[0] == 'COMMA':
                    self.advance()
        self.expect('LBRACE', '{')
        body = []
        while self.current_token() and self.current_token()[0] != 'RBRACE':
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            while self.current_token() and self.current_token()[0] in ('NEWLINE', 'SEMI'):
                self.advance()
        self.expect('RBRACE', '}')
        return ClassDef(name, base, interfaces, body)
    
    def parse_interface_def(self):
        self.advance()
        name = self.current_token()[1]
        self.advance()
        self.expect('LBRACE', '{')
        methods = []
        while self.current_token() and self.current_token()[0] != 'RBRACE':
            if self.current_token()[0] == 'FUNC':
                self.advance()
                method_name = self.current_token()[1]
                self.advance()
                self.expect('LPAREN', '(')
                params = self.parse_param_list()
                self.expect('RPAREN', ')')
                self.expect('SEMI', optional=True)
                methods.append((method_name, params))
            else:
                self.advance()
        self.expect('RBRACE', '}')
        return InterfaceDef(name, methods)
    
    def parse_var_decl(self):
        self.advance()
        name = self.current_token()[1]
        self.advance()
        self.expect('OPERATOR', '=')
        value = self.parse_expression()
        self.expect('SEMI', optional=True)
        return VarDecl(name, value)
    
    def parse_func_def(self):
        self.advance()
        name = self.current_token()[1]
        self.advance()
        self.expect('LPAREN', '(')
        params = self.parse_param_list()
        self.expect('RPAREN', ')')
        self.expect('LBRACE', '{')
        body = []
        while self.current_token() and self.current_token()[0] != 'RBRACE':
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            while self.current_token() and self.current_token()[0] in ('NEWLINE', 'SEMI'):
                self.advance()
        self.expect('RBRACE', '}')
        return FuncDef(name, params, body)
    
    def parse_try_stmt(self):
        self.advance()
        self.expect('LBRACE', '{')
        try_block = []
        while self.current_token() and self.current_token()[0] != 'RBRACE':
            stmt = self.parse_statement()
            if stmt:
                try_block.append(stmt)
            while self.current_token() and self.current_token()[0] in ('NEWLINE', 'SEMI'):
                self.advance()
        self.expect('RBRACE', '}')
        self.expect('CATCH', 'catch')
        self.expect('LPAREN', '(')
        catch_var = self.current_token()[1]
        self.advance()
        self.expect('RPAREN', ')')
        self.expect('LBRACE', '{')
        catch_block = []
        while self.current_token() and self.current_token()[0] != 'RBRACE':
            stmt = self.parse_statement()
            if stmt:
                catch_block.append(stmt)
            while self.current_token() and self.current_token()[0] in ('NEWLINE', 'SEMI'):
                self.advance()
        self.expect('RBRACE', '}')
        return TryStmt(try_block, catch_var, catch_block)
    
    def parse_param_list(self):
        params = []
        while self.current_token() and self.current_token()[0] == 'IDENTIFIER':
            params.append(self.current_token()[1])
            self.advance()
            if self.current_token() and self.current_token()[0] == 'COMMA':
                self.advance()
        return params
    
    def parse_if_stmt(self):
        self.advance()
        self.expect('LPAREN', '(')
        condition = self.parse_expression()
        self.expect('RPAREN', ')')
        self.expect('LBRACE', '{')
        then_branch = []
        while self.current_token() and self.current_token()[0] != 'RBRACE':
            stmt = self.parse_statement()
            if stmt:
                then_branch.append(stmt)
            while self.current_token() and self.current_token()[0] in ('NEWLINE', 'SEMI'):
                self.advance()
        self.expect('RBRACE', '}')
        else_branch = []
        if self.current_token() and self.current_token()[0] == 'ELSE':
            self.advance()
            if self.current_token() and self.current_token()[0] == 'IF':
                else_branch = [self.parse_if_stmt()]
            else:
                self.expect('LBRACE', '{')
                while self.current_token() and self.current_token()[0] != 'RBRACE':
                    stmt = self.parse_statement()
                    if stmt:
                        else_branch.append(stmt)
                    while self.current_token() and self.current_token()[0] in ('NEWLINE', 'SEMI'):
                        self.advance()
                self.expect('RBRACE', '}')
        return IfStmt(condition, then_branch, else_branch)
    
    def parse_while_stmt(self):
        self.advance()
        self.expect('LPAREN', '(')
        condition = self.parse_expression()
        self.expect('RPAREN', ')')
        self.expect('LBRACE', '{')
        body = []
        while self.current_token() and self.current_token()[0] != 'RBRACE':
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            while self.current_token() and self.current_token()[0] in ('NEWLINE', 'SEMI'):
                self.advance()
        self.expect('RBRACE', '}')
        return WhileStmt(condition, body)
    
    def parse_do_while_stmt(self):
        self.advance()
        self.expect('LBRACE', '{')
        body = []
        while self.current_token() and self.current_token()[0] != 'RBRACE':
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            while self.current_token() and self.current_token()[0] in ('NEWLINE', 'SEMI'):
                self.advance()
        self.expect('RBRACE', '}')
        self.expect('WHILE', 'while')
        self.expect('LPAREN', '(')
        condition = self.parse_expression()
        self.expect('RPAREN', ')')
        self.expect('SEMI', optional=True)
        return DoWhileStmt(body, condition)
    
    def parse_for_stmt(self):
        self.advance()
        self.expect('LPAREN', '(')
        if self.current_token() and self.current_token()[0] == 'IDENTIFIER' and self.tokens[self.pos + 1][0] == 'IN':
            var = self.current_token()[1]
            self.advance()
            self.expect('IN', 'in')
            iterable = self.parse_expression()
            self.expect('RPAREN', ')')
            self.expect('LBRACE', '{')
            body = []
            while self.current_token() and self.current_token()[0] != 'RBRACE':
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
                while self.current_token() and self.current_token()[0] in ('NEWLINE', 'SEMI'):
                    self.advance()
            self.expect('RBRACE', '}')
            return ForInStmt(var, iterable, body)
        else:
            init = self.parse_var_decl() if self.current_token() and self.current_token()[0] == 'VAR' else (self.parse_expression() if self.current_token() and self.current_token()[0] != 'SEMI' else None)
            self.expect('SEMI', ';')
            condition = self.parse_expression() if self.current_token() and self.current_token()[0] != 'SEMI' else None
            self.expect('SEMI', ';')
            increment = self.parse_expression() if self.current_token() and self.current_token()[0] != 'RPAREN' else None
            self.expect('RPAREN', ')')
            self.expect('LBRACE', '{')
            body = []
            while self.current_token() and self.current_token()[0] != 'RBRACE':
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
                while self.current_token() and self.current_token()[0] in ('NEWLINE', 'SEMI'):
                    self.advance()
            self.expect('RBRACE', '}')
            return ForStmt(init, condition, increment, body)
    
    def parse_print_stmt(self):
        self.advance()
        self.expect('LPAREN', '(')
        expr = self.parse_expression()
        self.expect('RPAREN', ')')
        self.expect('SEMI', optional=True)
        return PrintStmt(expr)
    
    def parse_return_stmt(self):
        self.advance()
        if self.current_token() and (self.current_token()[0] == 'SEMI' or self.current_token()[0] == 'NEWLINE'):
            self.advance()
            return ReturnStmt(None)
        expr = self.parse_expression()
        self.expect('SEMI', optional=True)
        return ReturnStmt(expr)
    
    def parse_expression(self):
        expr = self.parse_logical_or()
        if self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] == '?':
            self.advance()
            true_expr = self.parse_expression()
            self.expect('OPERATOR', ':')
            false_expr = self.parse_expression()
            expr = TernaryOp(expr, true_expr, false_expr)
        return expr
    
    def parse_logical_or(self):
        left = self.parse_logical_and()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] == '||':
            op = self.current_token()[1]
            self.advance()
            right = self.parse_logical_and()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_logical_and(self):
        left = self.parse_bitwise_or()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] == '&&':
            op = self.current_token()[1]
            self.advance()
            right = self.parse_bitwise_or()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_bitwise_or(self):
        left = self.parse_bitwise_xor()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] == '|':
            op = self.current_token()[1]
            self.advance()
            right = self.parse_bitwise_xor()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_bitwise_xor(self):
        left = self.parse_bitwise_and()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] == '^':
            op = self.current_token()[1]
            self.advance()
            right = self.parse_bitwise_and()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_bitwise_and(self):
        left = self.parse_equality()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] == '&':
            op = self.current_token()[1]
            self.advance()
            right = self.parse_equality()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_equality(self):
        left = self.parse_relational()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in ('==', '!='):
            op = self.current_token()[1]
            self.advance()
            right = self.parse_relational()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_relational(self):
        left = self.parse_shift()
        while self.current_token() and ((self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in ('<', '>', '<=', '>=')) or self.current_token()[0] == 'INSTANCEOF'):
            if self.current_token()[0] == 'OPERATOR':
                op = self.current_token()[1]
            else:
                op = 'instanceof'
            self.advance()
            right = self.parse_shift()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_shift(self):
        left = self.parse_additive()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in ('<<', '>>', '>>>'):
            op = self.current_token()[1]
            self.advance()
            right = self.parse_additive()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_additive(self):
        left = self.parse_multiplicative()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in ('+', '-'):
            op = self.current_token()[1]
            self.advance()
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_multiplicative(self):
        left = self.parse_unary()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in ('*', '/', '//', '%'):
            op = self.current_token()[1]
            self.advance()
            right = self.parse_unary()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_unary(self):
        if self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in ('-', '+', '!', '~', '++', '--'):
            op = self.current_token()[1]
            self.advance()
            operand = self.parse_unary()
            if op in ('++', '--'):
                return PrefixOp(op, operand)
            else:
                return UnaryOp(op, operand)
        return self.parse_primary()
    
    def parse_primary(self):
        token = self.current_token()
        if not token:
            raise SyntaxError("Unexpected end of input")
        if token[0] == 'IDENTIFIER':
            self.advance()
            expr = Identifier(token[1])
        elif token[0] == 'NUMBER':
            self.advance()
            num_str = token[1]
            expr = Number(float(num_str) if '.' in num_str else int(num_str))
        elif token[0] == 'STRING':
            self.advance()
            expr = String(token[1][1:-1])
        elif token[0] == 'TRUE':
            self.advance()
            expr = Boolean(True)
        elif token[0] == 'FALSE':
            self.advance()
            expr = Boolean(False)
        elif token[0] == 'NULL':
            self.advance()
            expr = Null()
        elif token[0] == 'LPAREN':
            self.advance()
            expr = self.parse_expression()
            self.expect('RPAREN', ')')
        elif token[0] == 'LBRACKET':
            expr = self.parse_list_literal()
        elif token[0] == 'LBRACE':
            expr = self.parse_dict_literal()
        elif token[0] == 'SET':
            self.advance()
            self.expect('LPAREN', '(')
            elements = []
            if self.current_token() and self.current_token()[0] != 'RPAREN':
                elements.append(self.parse_expression())
                while self.current_token() and self.current_token()[0] == 'COMMA':
                    self.advance()
                    elements.append(self.parse_expression())
            self.expect('RPAREN', ')')
            expr = SetLiteral(elements)
        else:
            raise SyntaxError(f"Line {token[2]}: Unexpected token: {token}")
        
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in ('++', '--'):
            op = self.current_token()[1]
            self.advance()
            expr = PostfixOp(expr, op)
        
        while self.current_token() and self.current_token()[0] in ('DOT', 'LPAREN', 'LBRACKET'):
            if self.current_token()[0] == 'DOT':
                self.advance()
                if self.current_token() and self.current_token()[0] == 'IDENTIFIER':
                    attr = self.current_token()[1]
                    self.advance()
                    expr = AttributeExpr(expr, attr)
                else:
                    raise SyntaxError("Expected identifier after dot")
            elif self.current_token()[0] == 'LPAREN':
                self.advance()
                args = []
                while self.current_token() and self.current_token()[0] != 'RPAREN':
                    args.append(self.parse_expression())
                    if self.current_token() and self.current_token()[0] == 'COMMA':
                        self.advance()
                self.expect('RPAREN', ')')
                expr = FuncCall(expr, args)
            elif self.current_token()[0] == 'LBRACKET':
                self.advance()
                if self.current_token() and self.current_token()[0] == 'COLON':
                    self.advance()
                    end = self.parse_expression() if self.current_token() and self.current_token()[0] != 'RBRACKET' else None
                    expr = IndexExpr(expr, Slice(None, end))
                else:
                    start = self.parse_expression()
                    if self.current_token() and self.current_token()[0] == 'COLON':
                        self.advance()
                        end = self.parse_expression() if self.current_token() and self.current_token()[0] != 'RBRACKET' else None
                        expr = IndexExpr(expr, Slice(start, end))
                    else:
                        expr = IndexExpr(expr, start)
                self.expect('RBRACKET', ']')
        return expr
    
    def parse_list_literal(self):
        self.advance()
        elements = []
        while self.current_token() and self.current_token()[0] != 'RBRACKET':
            elements.append(self.parse_expression())
            if self.current_token() and self.current_token()[0] == 'COMMA':
                self.advance()
        self.expect('RBRACKET', ']')
        return ListLiteral(elements)
    
    def parse_dict_literal(self):
        self.advance()
        pairs = []
        while self.current_token() and self.current_token()[0] != 'RBRACE':
            key = self.parse_expression()
            self.expect('COLON', ':')
            value = self.parse_expression()
            pairs.append((key, value))
            if self.current_token() and self.current_token()[0] == 'COMMA':
                self.advance()
        self.expect('RBRACE', '}')
        return DictLiteral(pairs)

# Class Object
class ShiboClass:
    def __init__(self, name, base, interfaces, env, methods, attributes):
        self.name = name
        self.base = base
        self.interfaces = interfaces
        self.env = env
        self.methods = methods
        self.attributes = attributes
    
    def instantiate(self, interpreter, args):
        instance = ShiboInstance(self, interpreter)
        if 'init' in self.methods:
            method = self.methods['init']
            if len(args) != len(method.params) - 1:  # -1 for 'self'
                raise TypeError(f"Expected {len(method.params) - 1} arguments, got {len(args)}")
            local_env = {'self': instance}
            local_env.update({param: arg for param, arg in zip(method.params[1:], args)})
            try:
                interpreter.eval(Program(method.body), local_env)
            except ReturnException:
                pass  # init doesn't return anything
        return instance

class ShiboInstance:
    def __init__(self, cls, interpreter):
        self.cls = cls
        self.env = {}
        self.env.update(cls.attributes)
        if cls.base:
            base_cls = interpreter.env.get(cls.base)
            if base_cls and isinstance(base_cls, ShiboClass):
                self.env.update(base_cls.attributes)

# Interpreter
class Interpreter:
    def __init__(self):
        self.env = {
            'append': lambda lst, val: lst.append(val) or lst,
            'remove': lambda lst, val: lst.remove(val) or lst,
            'pop': lambda lst, idx=None: lst.pop(idx if idx is not None else -1),
            'sort': lambda lst: lst.sort() or lst,
            'reverse': lambda lst: lst.reverse() or lst,
            'keys': lambda d: list(d.keys()),
            'len': len,
            'range': lambda start, stop: list(range(start, stop)),
            'input': input,
            'type': lambda x: type(x).__name__,
            'str': str,
            'int': int,
            'float': float,
            'upper': lambda s: s.upper(),
            'lower': lambda s: s.lower(),
            'split': lambda s, sep=None: s.split(sep),
            'math': {'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos, 'pi': math.pi, 'pow': math.pow, 'exp': math.exp},
            'image': {'load': lambda path: Image.open(path), 'show': lambda img: img.show() or None},
            'file': {'read': lambda path: open(path, 'r').read(), 'write': lambda path, content: open(path, 'w').write(content) or None},
            'net': {'http_get': http_get, 'http_post': http_post},
            'crypto': {'md5': md5, 'sha1': sha1, 'sha256': sha256},
            'os': {'get_env': get_env, 'set_env': set_env, 'get_cwd': get_cwd, 'change_dir': change_dir, 'list_dir': list_dir, 'exists': exists, 'run_command': run_command},
            'random': {'int': random_int, 'string': random_string},
            'url': {'parse': parse_url, 'encode': url_encode, 'decode': url_decode},
            'base64': {'encode': base64_encode, 'decode': base64_decode},
            're': {'search': lambda pattern, string: re.search(pattern, string).groups() if re.search(pattern, string) else None,
                   'match': lambda pattern, string: re.match(pattern, string).groups() if re.match(pattern, string) else None,
                   'findall': lambda pattern, string: re.findall(pattern, string)},
            'json': {'encode': json_encode, 'decode': json_decode},
            'time': {'now': time_now, 'sleep': time_sleep},
            'min': min,
            'max': max,
            'sum': sum,
            'abs': abs,
            'round': round,
            'set_union': lambda s1, s2: s1.union(s2),
            'set_intersection': lambda s1, s2: s1.intersection(s2),
            'set_difference': lambda s1, s2: s1.difference(s2),
            'set_symmetric_difference': lambda s1, s2: s1.symmetric_difference(s2),
            'set_add': lambda s, elem: s.add(elem) or s,
            'set_remove': lambda s, elem: s.remove(elem) or s,
            'datetime': {
                'now': datetime.datetime.now,
                'strftime': lambda dt, fmt: dt.strftime(fmt),
                'strptime': lambda s, fmt: datetime.datetime.strptime(s, fmt),
                'date': datetime.date,
                'time': datetime.time,
                'timedelta': datetime.timedelta,
            },
        }
        self.loop_depth = 0
        self.modules = {}
    
    def eval(self, node, env=None):
        env = env if env is not None else self.env
        if isinstance(node, Program):
            return self.eval_program(node, env)
        elif isinstance(node, ImportStmt):
            return self.eval_import_stmt(node, env)
        elif isinstance(node, FromImportStmt):
            return self.eval_from_import_stmt(node, env)
        elif isinstance(node, ClassDef):
            return self.eval_class_def(node, env)
        elif isinstance(node, InterfaceDef):
            return self.eval_interface_def(node, env)
        elif isinstance(node, VarDecl):
            return self.eval_var_decl(node, env)
        elif isinstance(node, FuncDef):
            return self.eval_func_def(node, env)
        elif isinstance(node, TryStmt):
            return self.eval_try_stmt(node, env)
        elif isinstance(node, AssignStmt):
            return self.eval_assign_stmt(node, env)
        elif isinstance(node, IfStmt):
            return self.eval_if_stmt(node, env)
        elif isinstance(node, WhileStmt):
            return self.eval_while_stmt(node, env)
        elif isinstance(node, DoWhileStmt):
            return self.eval_do_while_stmt(node, env)
        elif isinstance(node, ForStmt):
            return self.eval_for_stmt(node, env)
        elif isinstance(node, ForInStmt):
            return self.eval_for_in_stmt(node, env)
        elif isinstance(node, BreakStmt):
            return self.eval_break_stmt()
        elif isinstance(node, ContinueStmt):
            return self.eval_continue_stmt()
        elif isinstance(node, PrintStmt):
            return self.eval_print_stmt(node, env)
        elif isinstance(node, ReturnStmt):
            return self.eval_return_stmt(node, env)
        elif isinstance(node, ExprStmt):
            return self.eval_expr_stmt(node, env)
        elif isinstance(node, Identifier):
            return env.get(node.name, self.env.get(node.name))
        elif isinstance(node, Number):
            return node.value
        elif isinstance(node, String):
            return node.value
        elif isinstance(node, Boolean):
            return node.value
        elif isinstance(node, Null):
            return None
        elif isinstance(node, ListLiteral):
            return [self.eval(e, env) for e in node.elements]
        elif isinstance(node, DictLiteral):
            return {self.eval(k, env): self.eval(v, env) for k, v in node.pairs}
        elif isinstance(node, SetLiteral):
            return set(self.eval(e, env) for e in node.elements)
        elif isinstance(node, BinaryOp):
            return self.eval_binary_op(node, env)
        elif isinstance(node, UnaryOp):
            return self.eval_unary_op(node, env)
        elif isinstance(node, PrefixOp):
            return self.eval_prefix_op(node, env)
        elif isinstance(node, PostfixOp):
            return self.eval_postfix_op(node, env)
        elif isinstance(node, TernaryOp):
            return self.eval_ternary_op(node, env)
        elif isinstance(node, FuncCall):
            return self.eval_func_call(node, env)
        elif isinstance(node, IndexExpr):
            return self.eval_index_expr(node, env)
        elif isinstance(node, AttributeExpr):
            return self.eval_attribute_expr(node, env)
    
    def get_lvalue(self, node, env):
        if isinstance(node, Identifier):
            return env[node.name]
        elif isinstance(node, IndexExpr):
            obj = self.eval(node.object, env)
            index = self.eval(node.index, env)
            if isinstance(obj, list) or isinstance(obj, dict):
                return obj[index]
            else:
                raise TypeError("Cannot index non-list or non-dict")
        elif isinstance(node, AttributeExpr):
            obj = self.eval(node.object, env)
            if isinstance(obj, ShiboInstance):
                return obj.env[node.attribute]
            elif isinstance(obj, dict):
                return obj[node.attribute]
            else:
                try:
                    return getattr(obj, node.attribute)
                except AttributeError:
                    raise AttributeError(f"'{type(obj).__name__}' has no attribute '{node.attribute}'")
        else:
            raise TypeError("Invalid lvalue")
    
    def set_lvalue(self, node, value, env):
        if isinstance(node, Identifier):
            env[node.name] = value
        elif isinstance(node, IndexExpr):
            obj = self.eval(node.object, env)
            index = self.eval(node.index, env)
            if isinstance(obj, list) or isinstance(obj, dict):
                obj[index] = value
            else:
                raise TypeError("Cannot assign to non-list or non-dict")
        elif isinstance(node, AttributeExpr):
            obj = self.eval(node.object, env)
            if isinstance(obj, ShiboInstance):
                obj.env[node.attribute] = value
            elif isinstance(obj, dict):
                obj[node.attribute] = value
            else:
                try:
                    setattr(obj, node.attribute, value)
                except AttributeError:
                    raise TypeError(f"Cannot set attribute '{node.attribute}' on {type(obj).__name__}")
        else:
            raise TypeError("Invalid lvalue")
    
    def eval_program(self, node, env):
        result = None
        for stmt in node.statements:
            result = self.eval(stmt, env)
        return result
    
    def eval_import_stmt(self, node, env):
        if node.module not in self.modules:
            try:
                with open(f"{node.module}.shibo", 'r') as f:
                    code = f.read()
                lexer = Lexer(code)
                tokens = lexer.tokenize()
                parser = Parser(tokens)
                ast = parser.parse()
                module_env = {}
                self.eval(ast, module_env)
                self.modules[node.module] = module_env
            except FileNotFoundError:
                raise ImportError(f"Module '{node.module}' not found")
        env.update(self.modules[node.module])
        return None
    
    def eval_from_import_stmt(self, node, env):
        if node.module not in self.modules:
            try:
                with open(f"{node.module}.shibo", 'r') as f:
                    code = f.read()
                lexer = Lexer(code)
                tokens = lexer.tokenize()
                parser = Parser(tokens)
                ast = parser.parse()
                module_env = {}
                self.eval(ast, module_env)
                self.modules[node.module] = module_env
            except FileNotFoundError:
                raise ImportError(f"Module '{node.module}' not found")
        if node.names == ['*']:
            env.update(self.modules[node.module])
        else:
            for name in node.names:
                if name in self.modules[node.module]:
                    env[name] = self.modules[node.module][name]
                else:
                    raise ImportError(f"'{name}' not found in module '{node.module}'")
        return None
    
    def eval_class_def(self, node, env):
        methods = {}
        attributes = {}
        for stmt in node.body:
            if isinstance(stmt, FuncDef):
                methods[stmt.name] = stmt
            elif isinstance(stmt, VarDecl):
                attributes[stmt.name] = self.eval(stmt.value, env)
        cls = ShiboClass(node.name, node.base, node.interfaces, env, methods, attributes)
        env[node.name] = cls
        return None
    
    def eval_interface_def(self, node, env):
        env[node.name] = {'type': 'interface', 'methods': {name: params for name, params in node.methods}}
        return None
    
    def eval_var_decl(self, node, env):
        value = self.eval(node.value, env)
        env[node.name] = value
        return None
    
    def eval_func_def(self, node, env):
        env[node.name] = node
        return None
    
    def eval_try_stmt(self, node, env):
        try:
            return self.eval_program(Program(node.try_block), env)
        except Exception as e:
            env[node.catch_var] = str(e)
            return self.eval_program(Program(node.catch_block), env)
    
    def eval_assign_stmt(self, node, env):
        value = self.eval(node.value, env)
        if isinstance(node.target, Identifier):
            env[node.target.name] = value
        elif isinstance(node.target, IndexExpr):
            obj = self.eval(node.target.object, env)
            index = self.eval(node.target.index, env)
            if isinstance(obj, list) or isinstance(obj, dict):
                obj[index] = value
            else:
                raise TypeError("Cannot assign to non-list or non-dict")
        elif isinstance(node.target, AttributeExpr):
            obj = self.eval(node.target.object, env)
            if isinstance(obj, ShiboInstance):
                obj.env[node.target.attribute] = value
            elif isinstance(obj, dict):
                obj[node.target.attribute] = value
            else:
                try:
                    setattr(obj, node.target.attribute, value)
                except AttributeError:
                    raise TypeError(f"Cannot set attribute '{node.target.attribute}' on {type(obj).__name__}")
        return None
    
    def eval_if_stmt(self, node, env):
        condition = self.eval(node.condition, env)
        if condition:
            return self.eval_program(Program(node.then_branch), env)
        elif node.else_branch:
            return self.eval_program(Program(node.else_branch), env)
        return None
    
    def eval_while_stmt(self, node, env):
        self.loop_depth += 1
        while self.eval(node.condition, env):
            try:
                self.eval_program(Program(node.body), env)
            except ContinueException:
                continue
            except BreakException:
                break
        self.loop_depth -= 1
        return None
    
    def eval_do_while_stmt(self, node, env):
        self.loop_depth += 1
        while True:
            try:
                self.eval_program(Program(node.body), env)
            except ContinueException:
                continue
            except BreakException:
                break
            if not self.eval(node.condition, env):
                break
        self.loop_depth -= 1
        return None
    
    def eval_for_stmt(self, node, env):
        self.loop_depth += 1
        if node.init:
            self.eval(node.init, env)
        while node.condition is None or self.eval(node.condition, env):
            try:
                self.eval_program(Program(node.body), env)
            except ContinueException:
                pass
            except BreakException:
                break
            if node.increment:
                self.eval(node.increment, env)
        self.loop_depth -= 1
        return None
    
    def eval_for_in_stmt(self, node, env):
        self.loop_depth += 1
        iterable = self.eval(node.iterable, env)
        for item in iterable:
            try:
                env[node.var] = item
                self.eval_program(Program(node.body), env)
            except ContinueException:
                continue
            except BreakException:
                break
        self.loop_depth -= 1
        return None
    
    def eval_break_stmt(self):
        if self.loop_depth == 0:
            raise SyntaxError("break outside loop")
        raise BreakException()
    
    def eval_continue_stmt(self):
        if self.loop_depth == 0:
            raise SyntaxError("continue outside loop")
        raise ContinueException()
    
    def eval_print_stmt(self, node, env):
        value = self.eval(node.expression, env)
        print(value)
        return None
    
    def eval_return_stmt(self, node, env):
        value = self.eval(node.expression, env) if node.expression else None
        raise ReturnException(value)
    
    def eval_expr_stmt(self, node, env):
        return self.eval(node.expression, env)
    
    def eval_prefix_op(self, node, env):
        operand = node.operand
        if not isinstance(operand, (Identifier, IndexExpr, AttributeExpr)):
            raise TypeError("Invalid operand for prefix operator")
        old_value = self.get_lvalue(operand, env)
        if not isinstance(old_value, (int, float)):
            raise TypeError("Can only increment/decrement numbers")
        if node.op == '++':
            new_value = old_value + 1
        elif node.op == '--':
            new_value = old_value - 1
        else:
            raise ValueError("Invalid prefix operator")
        self.set_lvalue(operand, new_value, env)
        return new_value
    
    def eval_postfix_op(self, node, env):
        operand = node.operand
        if not isinstance(operand, (Identifier, IndexExpr, AttributeExpr)):
            raise TypeError("Invalid operand for postfix operator")
        old_value = self.get_lvalue(operand, env)
        if not isinstance(old_value, (int, float)):
            raise TypeError("Can only increment/decrement numbers")
        if node.op == '++':
            new_value = old_value + 1
        elif node.op == '--':
            new_value = old_value - 1
        else:
            raise ValueError("Invalid postfix operator")
        self.set_lvalue(operand, new_value, env)
        return old_value
    
    def eval_ternary_op(self, node, env):
        condition = self.eval(node.condition, env)
        if condition:
            return self.eval(node.true_expr, env)
        else:
            return self.eval(node.false_expr, env)
    
    def eval_binary_op(self, node, env):
        left = self.eval(node.left, env)
        if node.op == '&&':
            return left and self.eval(node.right, env)
        elif node.op == '||':
            return left or self.eval(node.right, env)
        right = self.eval(node.right, env)
        if node.op == '+':
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            return left / right
        elif node.op == '//':
            return left // right
        elif node.op == '%':
            return left % right
        elif node.op == '==':
            return left == right
        elif node.op == '!=':
            return left != right
        elif node.op == '<':
            return left < right
        elif node.op == '>':
            return left > right
        elif node.op == '<=':
            return left <= right
        elif node.op == '>=':
            return left >= right
        elif node.op in ('&', '|', '^', '<<', '>>', '>>>'):
            if not isinstance(left, int) or not isinstance(right, int):
                raise TypeError("Bitwise operations require integers")
            if node.op == '&':
                return left & right
            elif node.op == '|':
                return left | right
            elif node.op == '^':
                return left ^ right
            elif node.op == '<<':
                return left << right
            elif node.op == '>>':
                return left >> right
            elif node.op == '>>>':
                return (left & 0xFFFFFFFF) >> right
        elif node.op == 'instanceof':
            if not isinstance(left, ShiboInstance):
                return False
            right_val = self.eval(node.right, env)
            if not isinstance(right_val, ShiboClass):
                return False
            cls = left.cls
            while cls:
                if cls == right_val:
                    return True
                cls = self.env.get(cls.base) if cls.base else None
            return False
    
    def eval_unary_op(self, node, env):
        operand = self.eval(node.operand, env)
        if node.op == '-':
            return -operand
        elif node.op == '+':
            return operand
        elif node.op == '!':
            return not operand
        elif node.op == '~':
            if not isinstance(operand, int):
                raise TypeError("Bitwise complement requires integer")
            return ~operand
    
    def eval_func_call(self, node, env, instance_env=None):
        func = self.eval(node.func_expr, env)
        args = [self.eval(arg, env) for arg in node.args]
        if isinstance(func, tuple) and len(func) == 2 and isinstance(func[0], FuncDef) and isinstance(func[1], ShiboInstance):
            method, instance = func
            if len(args) != len(method.params) - 1:  # -1 for 'self'
                raise TypeError(f"Expected {len(method.params) - 1} arguments, got {len(args)}")
            local_env = {'self': instance}
            local_env.update({param: arg for param, arg in zip(method.params[1:], args)})
            interpreter = Interpreter()
            interpreter.env.update(self.env)
            interpreter.env.update(local_env)
            try:
                interpreter.eval(Program(method.body))
            except ReturnException as e:
                return e.value
            return None
        elif isinstance(func, FuncDef):
            if len(args) != len(func.params):
                raise TypeError(f"Expected {len(func.params)} arguments, got {len(args)}")
            local_env = {param: arg for param, arg in zip(func.params, args)}
            interpreter = Interpreter()
            interpreter.env.update(self.env)
            if instance_env:
                local_env.update(instance_env)
            interpreter.env.update(local_env)
            try:
                interpreter.eval(Program(func.body))
            except ReturnException as e:
                return e.value
            return None
        elif isinstance(func, ShiboClass):
            return func.instantiate(self, args)
        elif callable(func):
            return func(*args)
        raise TypeError(f"'{type(func).__name__}' is not callable")
    
    def eval_index_expr(self, node, env):
        obj = self.eval(node.object, env)
        index = self.eval(node.index, env)
        if isinstance(index, Slice):
            start = self.eval(index.start, env) if index.start is not None else 0
            end = self.eval(index.end, env) if index.end is not None else len(obj)
            if isinstance(obj, list):
                return obj[start:end]
            raise TypeError("Slicing only supported on lists")
        elif isinstance(obj, list):
            return obj[index]
        elif isinstance(obj, dict):
            return obj.get(index, None)
        raise TypeError("Cannot index non-list or non-dict")
    
    def eval_attribute_expr(self, node, env):
        obj = self.eval(node.object, env)
        if isinstance(obj, ShiboInstance):
            if node.attribute in obj.env:
                return obj.env[node.attribute]
            elif node.attribute in obj.cls.methods:
                return (obj.cls.methods[node.attribute], obj)
            else:
                base_cls = obj.cls.base
                while base_cls:
                    base_cls_obj = self.env.get(base_cls)
                    if base_cls_obj and isinstance(base_cls_obj, ShiboClass):
                        if node.attribute in base_cls_obj.methods:
                            return (base_cls_obj.methods[node.attribute], obj)
                        base_cls = base_cls_obj.base
                    else:
                        break
                raise AttributeError(f"'{obj.cls.name}' instance has no attribute '{node.attribute}'")
        elif isinstance(obj, ShiboClass):
            if node.attribute in obj.methods:
                return obj.methods[node.attribute]
            else:
                raise AttributeError(f"Class '{obj.name}' has no method '{node.attribute}'")
        elif isinstance(obj, dict):
            if node.attribute in obj:
                return obj[node.attribute]
            try:
                return getattr(obj, node.attribute)
            except AttributeError:
                raise AttributeError(f"Dictionary has no key or attribute '{node.attribute}'")
        try:
            return getattr(obj, node.attribute)
        except AttributeError:
            raise AttributeError(f"'{type(obj).__name__}' has no attribute '{node.attribute}'")

# Enhanced REPL
def repl():
    interpreter = Interpreter()
    __version__ = "0.2.1"
    ICON = "🐕"
    print(f"{Colors.OKCYAN}{ICON} Welcome to ShiboScript v{__version__} REPL! Type 'exit' to quit, 'help' for help.{Colors.ENDC}")

    while True:
        try:
            code = input(f"{Colors.OKGREEN}shiboscript>>> {Colors.ENDC}")
            if code.strip() == "exit":
                break
            if code.strip() in ('cls', 'clear'):
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            if code.strip() == "help":
                print("Available built-ins:")
                for key in sorted(interpreter.env.keys()):
                    if not key.startswith('_'):
                        print(f" - {key}")
                continue
            while True:
                try:
                    lexer = Lexer(code)
                    tokens = lexer.tokenize()
                    parser = Parser(tokens)
                    ast = parser.parse()
                    break
                except SyntaxError as e:
                    print(f"{Colors.FAIL}Syntax Error: {e}{Colors.ENDC}")
                    next_line = input(f"{Colors.WARNING}... {Colors.ENDC}")
                    if next_line.strip() == "":
                        raise
                    code += "\n" + next_line
            result = interpreter.eval(ast)
            if result is not None:
                print(f"{Colors.OKBLUE}{result}{Colors.ENDC}")
        except SyntaxError as e:
            print(f"{Colors.FAIL}Syntax Error: {e}{Colors.ENDC}")
        except NameError as e:
            print(f"{Colors.FAIL}Name Error: {e}{Colors.ENDC}")
        except TypeError as e:
            print(f"{Colors.FAIL}Type Error: {e}{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")

# Run Script from File
def run_file(filename):
    try:
        with open(filename, 'r') as file:
            code = file.read()
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.eval(ast)
    except FileNotFoundError:
        print(f"{Colors.FAIL}File not found: {filename}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        repl()