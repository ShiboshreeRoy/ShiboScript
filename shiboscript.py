import re
from collections import namedtuple
from PIL import Image
import math
import sys

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

# Token Types
TOKENS = [
    ('VAR', r'\bvar\b'), ('FUNC', r'\bfunc\b'), ('IF', r'\bif\b'), ('ELSE', r'\belse\b'),
    ('WHILE', r'\bwhile\b'), ('DO', r'\bdo\b'), ('FOR', r'\bfor\b'), ('IN', r'\bin\b'),
    ('BREAK', r'\bbreak\b'), ('CONTINUE', r'\bcontinue\b'), ('PRINT', r'\bprint\b'),
    ('RETURN', r'\breturn\b'), ('TRY', r'\btry\b'), ('CATCH', r'\bcatch\b'),
    ('TRUE', r'\btrue\b'), ('FALSE', r'\bfalse\b'), ('NULL', r'\bnull\b'),
    ('NUMBER', r'\d+\.\d*|\.\d+|\d+'),  # Updated to handle integers and floats
    ('STRING', r'"[^"]*"'), ('IDENTIFIER', r'[a-zA-Z_]\w*'),
    ('OPERATOR', r'[+\-*/%=<>!&|^~]|[<>=!]=|//|&&|\|\|'),
    ('LPAREN', r'\('), ('RPAREN', r'\)'), ('LBRACE', r'\{'), ('RBRACE', r'\}'),
    ('LBRACKET', r'\['), ('RBRACKET', r'\]'), ('COMMA', r','), ('COLON', r':'),
    ('SEMI', r';'), ('DOT', r'\.'), ('NEWLINE', r'\n'),
]

# AST Nodes
Program = namedtuple('Program', ['statements'])
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
FuncCall = namedtuple('FuncCall', ['func_expr', 'args'])
ListLiteral = namedtuple('ListLiteral', ['elements'])
DictLiteral = namedtuple('DictLiteral', ['pairs'])
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

# Lexer with Line Tracking
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
        if token[0] == 'VAR':
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
            if self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] == '=':
                self.advance()
                value = self.parse_expression()
                if isinstance(expr, (Identifier, IndexExpr, AttributeExpr)):
                    self.expect('SEMI', optional=True)
                    return AssignStmt(expr, value)
                raise SyntaxError("Invalid assignment target")
            self.expect('SEMI', optional=True)
            return ExprStmt(expr)
    
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
        return self.parse_logical_or()
    
    def parse_logical_or(self):
        left = self.parse_logical_and()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] == '||':
            op = self.current_token()[1]
            self.advance()
            right = self.parse_logical_and()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_logical_and(self):
        left = self.parse_comparison()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] == '&&':
            op = self.current_token()[1]
            self.advance()
            right = self.parse_comparison()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_comparison(self):
        left = self.parse_additive()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in ('<', '>', '<=', '>=', '==', '!='):
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
        if self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in ('-', '!'):
            op = self.current_token()[1]
            self.advance()
            operand = self.parse_unary()
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
            if '.' in num_str:
                if num_str.endswith('.'):
                    num_str += '0'
                expr = Number(float(num_str))
            else:
                expr = Number(int(num_str))
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
        else:
            raise SyntaxError(f"Line {token[2]}: Unexpected token: {token}")
        
        while self.current_token() and self.current_token()[0] == 'DOT':
            self.advance()
            if self.current_token() and self.current_token()[0] == 'IDENTIFIER':
                attr = self.current_token()[1]
                self.advance()
                expr = AttributeExpr(expr, attr)
            else:
                raise SyntaxError("Expected identifier after dot")
        
        while self.current_token() and self.current_token()[0] in ('LPAREN', 'LBRACKET'):
            if self.current_token()[0] == 'LPAREN':
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
            'math': {
                'sqrt': math.sqrt,
                'sin': math.sin,
                'cos': math.cos,
                'pi': math.pi,
                'pow': math.pow,
                'exp': math.exp,
            },
            'load_image': lambda path: Image.open(path),
            'show_image': lambda img: img.show() or None,
            'read_file': lambda path: open(path, 'r').read(),
            'write_file': lambda path, content: open(path, 'w').write(content) or None,
        }
        self.loop_depth = 0
    
    def eval(self, node):
        if isinstance(node, Program):
            return self.eval_program(node)
        elif isinstance(node, VarDecl):
            return self.eval_var_decl(node)
        elif isinstance(node, FuncDef):
            return self.eval_func_def(node)
        elif isinstance(node, TryStmt):
            return self.eval_try_stmt(node)
        elif isinstance(node, AssignStmt):
            return self.eval_assign_stmt(node)
        elif isinstance(node, IfStmt):
            return self.eval_if_stmt(node)
        elif isinstance(node, WhileStmt):
            return self.eval_while_stmt(node)
        elif isinstance(node, DoWhileStmt):
            return self.eval_do_while_stmt(node)
        elif isinstance(node, ForStmt):
            return self.eval_for_stmt(node)
        elif isinstance(node, ForInStmt):
            return self.eval_for_in_stmt(node)
        elif isinstance(node, BreakStmt):
            return self.eval_break_stmt()
        elif isinstance(node, ContinueStmt):
            return self.eval_continue_stmt()
        elif isinstance(node, PrintStmt):
            return self.eval_print_stmt(node)
        elif isinstance(node, ReturnStmt):
            return self.eval_return_stmt(node)
        elif isinstance(node, ExprStmt):
            return self.eval_expr_stmt(node)
        elif isinstance(node, Identifier):
            return self.env.get(node.name, None)
        elif isinstance(node, Number):
            return node.value
        elif isinstance(node, String):
            return node.value
        elif isinstance(node, Boolean):
            return node.value
        elif isinstance(node, Null):
            return None
        elif isinstance(node, ListLiteral):
            return [self.eval(e) for e in node.elements]
        elif isinstance(node, DictLiteral):
            return {self.eval(k): self.eval(v) for k, v in node.pairs}
        elif isinstance(node, BinaryOp):
            return self.eval_binary_op(node)
        elif isinstance(node, UnaryOp):
            return self.eval_unary_op(node)
        elif isinstance(node, FuncCall):
            return self.eval_func_call(node)
        elif isinstance(node, IndexExpr):
            return self.eval_index_expr(node)
        elif isinstance(node, AttributeExpr):
            obj = self.eval(node.object)
            if isinstance(obj, dict):
                if node.attribute in obj:
                    return obj[node.attribute]
                try:
                    return getattr(obj, node.attribute)
                except AttributeError:
                    raise AttributeError(f"Dictionary has no key or attribute '{node.attribute}'")
            try:
                return getattr(obj, node.attribute)
            except AttributeError:
                raise AttributeError(f"{type(obj).__name__} has no attribute '{node.attribute}'")
    
    def eval_program(self, node):
        result = None
        for stmt in node.statements:
            result = self.eval(stmt)
        return result
    
    def eval_var_decl(self, node):
        value = self.eval(node.value)
        self.env[node.name] = value
        return None
    
    def eval_func_def(self, node):
        self.env[node.name] = node
        return None
    
    def eval_try_stmt(self, node):
        try:
            return self.eval_program(Program(node.try_block))
        except Exception as e:
            self.env[node.catch_var] = str(e)
            return self.eval_program(Program(node.catch_block))
    
    def eval_assign_stmt(self, node):
        value = self.eval(node.value)
        if isinstance(node.target, Identifier):
            self.env[node.target.name] = value
        elif isinstance(node.target, IndexExpr):
            obj = self.eval(node.target.object)
            index = self.eval(node.target.index)
            if isinstance(obj, list):
                obj[index] = value
            elif isinstance(obj, dict):
                obj[index] = value
            else:
                raise TypeError("Cannot assign to non-list or non-dict")
        elif isinstance(node.target, AttributeExpr):
            obj = self.eval(node.target.object)
            if isinstance(obj, dict):
                obj[node.target.attribute] = value
            else:
                try:
                    setattr(obj, node.target.attribute, value)
                except AttributeError:
                    raise TypeError(f"Cannot set attribute '{node.target.attribute}' on {type(obj).__name__}")
        return None
    
    def eval_if_stmt(self, node):
        condition = self.eval(node.condition)
        if condition:
            return self.eval_program(Program(node.then_branch))
        elif node.else_branch:
            return self.eval_program(Program(node.else_branch))
        return None
    
    def eval_while_stmt(self, node):
        self.loop_depth += 1
        while self.eval(node.condition):
            try:
                self.eval_program(Program(node.body))
            except ContinueException:
                continue
            except BreakException:
                break
        self.loop_depth -= 1
        return None
    
    def eval_do_while_stmt(self, node):
        self.loop_depth += 1
        while True:
            try:
                self.eval_program(Program(node.body))
            except ContinueException:
                continue
            except BreakException:
                break
            if not self.eval(node.condition):
                break
        self.loop_depth -= 1
        return None
    
    def eval_for_stmt(self, node):
        self.loop_depth += 1
        if node.init:
            self.eval(node.init)
        while node.condition is None or self.eval(node.condition):
            try:
                self.eval_program(Program(node.body))
            except ContinueException:
                pass
            except BreakException:
                break
            if node.increment:
                self.eval(node.increment)
        self.loop_depth -= 1
        return None
    
    def eval_for_in_stmt(self, node):
        self.loop_depth += 1
        iterable = self.eval(node.iterable)
        for item in iterable:
            try:
                self.env[node.var] = item
                self.eval_program(Program(node.body))
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
    
    def eval_print_stmt(self, node):
        value = self.eval(node.expression)
        print(value)
        return None
    
    def eval_return_stmt(self, node):
        value = self.eval(node.expression) if node.expression else None
        raise ReturnException(value)
    
    def eval_expr_stmt(self, node):
        return self.eval(node.expression)
    
    def eval_binary_op(self, node):
        left = self.eval(node.left)
        if node.op == '&&':
            return left and self.eval(node.right)
        elif node.op == '||':
            return left or self.eval(node.right)
        right = self.eval(node.right)
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
    
    def eval_unary_op(self, node):
        operand = self.eval(node.operand)
        if node.op == '-':
            return -operand
        elif node.op == '!':
            return not operand
    
    def eval_func_call(self, node):
        func = self.eval(node.func_expr)
        if func is None:
            raise NameError(f"Function not defined")
        args = [self.eval(arg) for arg in node.args]
        if isinstance(func, FuncDef):
            if len(args) != len(func.params):
                raise TypeError(f"Expected {len(func.params)} arguments, got {len(args)}")
            local_env = {param: arg for param, arg in zip(func.params, args)}
            interpreter = Interpreter()
            interpreter.env.update(self.env)
            interpreter.env.update(local_env)
            try:
                interpreter.eval(Program(func.body))
            except ReturnException as e:
                return e.value
            return None
        elif callable(func):
            return func(*args)
        raise TypeError("Not a function")
    
    def eval_index_expr(self, node):
        obj = self.eval(node.object)
        index = self.eval(node.index)
        if isinstance(index, Slice):
            start = index.start if index.start is not None else 0
            end = index.end if index.end is not None else len(obj)
            if isinstance(obj, list):
                return obj[start:end]
            raise TypeError("Slicing only supported on lists")
        elif isinstance(obj, list):
            return obj[index]
        elif isinstance(obj, dict):
            return obj.get(index, None)
        raise TypeError("Cannot index non-list or non-dict")

# REPL with Color and Multi-Line Support
def repl():
    interpreter = Interpreter()
    print(f"{Colors.OKCYAN}Welcome to FlexScript REPL! Type 'exit' to quit.{Colors.ENDC}")
    while True:
        try:
            code = input(f"{Colors.OKGREEN}shiboscript>>> {Colors.ENDC}")
            if code.strip() == "exit":
                break
            while True:
                try:
                    lexer = Lexer(code)
                    tokens = lexer.tokenize()
                    parser = Parser(tokens)
                    ast = parser.parse()
                    break
                except SyntaxError as e:
                    print(f"{Colors.FAIL}{e}{Colors.ENDC}")
                    next_line = input(f"{Colors.WARNING}... {Colors.ENDC}")
                    if next_line.strip() == "":
                        raise
                    code += "\n" + next_line
            result = interpreter.eval(ast)
            if result is not None:
                print(f"{Colors.OKBLUE}{result}{Colors.ENDC}")
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