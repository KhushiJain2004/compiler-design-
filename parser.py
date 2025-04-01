import re
from lexer import Token, Lexer

# Abstract Syntax Tree Node Classes
class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Program(statements={self.statements})"

class Statement(ASTNode):
    pass

class VariableDeclaration(Statement):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __repr__(self):
        return f"VariableDeclaration(name='{self.name}', expression={self.expression})"

class UnitConversionStatement(Statement):
    def __init__(self, expression, target_unit):
        self.expression = expression
        self.target_unit = target_unit

    def __repr__(self):
        return f"UnitConversionStatement(expression={self.expression}, target_unit='{self.target_unit}')"

class PrintStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"PrintStatement(expression={self.expression})"

class Expression(ASTNode):
    pass

class BinaryOperation(Expression):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinaryOperation(op='{self.op}', left={self.left}, right={self.right})"

class UnitValue(Expression):
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def __repr__(self):
        return f"UnitValue(value={self.value}, unit='{self.unit}')"

class NumberLiteral(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NumberLiteral(value={self.value})"

class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Variable(name='{self.name}')"

class FunctionCall(Expression):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"FunctionCall(name='{self.name}', args={self.args})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[self.position] if self.tokens else None

    def advance(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None

    def peek(self, offset=1):
        peek_position = self.position + offset
        if peek_position < len(self.tokens):
            return self.tokens[peek_position]
        return None

    def eat(self, token_type, token_value=None):
        if self.current_token is not None and self.current_token.type == token_type and (token_value is None or self.current_token.value == token_value):
            self.advance()
        else:
            expected = f"'{token_value}'" if token_value else token_type
            found = f"'{self.current_token.value}' ({self.current_token.type})" if self.current_token else 'EOF'
            self.error(f"Expected {expected}, but found {found}")

    def error(self, message):
        if self.current_token:
            raise SyntaxError(f"Parsing error at line {self.current_token.line}, column {self.current_token.column}: {message}")
        else:
            raise SyntaxError(f"Parsing error at end of input: {message}")

    def parse(self):
        statements = []
        # raise SyntaxError("Testing if parser error is caught in UI")
        while self.current_token is not None and self.current_token.type != 'EOF':
            try:
                statement = self.statement()
                if statement:
                    statements.append(statement)
                if self.current_token is not None and self.current_token.type != 'EOF':
                    self.eat('SEMICOLON')
            except SyntaxError as e:
                print(e)
                # Attempt to recover by skipping to the next semicolon or end of file
                while self.current_token is not None and self.current_token.type != 'SEMICOLON' and self.current_token.type != 'EOF':
                    self.advance()
                if self.current_token and self.current_token.type == 'SEMICOLON':
                    self.advance()
                # raise SyntaxError(str(e))

        if statements and self.tokens and self.tokens[-1].type != 'EOF' and self.tokens[-1].type != 'SEMICOLON':
            last_token = self.tokens[-1]
            raise SyntaxError(f"Parsing error at line {last_token.line}, column {last_token.column + len(str(last_token.value))}: Expected ';'")

        return Program(statements)

    def statement(self):
        if self.current_token.type == 'KEYWORD' and self.current_token.value == 'let':
            return self.variable_declaration()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'convert':
            return self.unit_conversion_statement()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'print':
            return self.print_statement()
        else:
            return self.expression_statement()

    def variable_declaration(self):
        self.eat('KEYWORD', 'let')
        name = self.current_token.value
        self.eat('IDENTIFIER')
        self.eat('OPERATOR', '=')
        expression = self.expression()
        return VariableDeclaration(name, expression)

    def unit_conversion_statement(self):
        self.eat('KEYWORD', 'convert')
        self.eat('LPAREN')
        expression = self.expression()
        self.eat('RPAREN')
        self.eat('KEYWORD', 'to')
        target_unit = self.current_token.value
        self.eat('IDENTIFIER')
        return UnitConversionStatement(expression, target_unit)

    def print_statement(self):
        self.eat('KEYWORD', 'print')
        expression = self.expression()
        return PrintStatement(expression)

    def expression_statement(self):
        return self.expression() # For cases like function calls without 'let'

    def expression(self):
        return self.additive_expression()

    def additive_expression(self):
        left = self.multiplicative_expression()
        while self.current_token is not None and self.current_token.type == 'OPERATOR' and self.current_token.value in ['+', '-']:
            op = self.current_token.value
            self.advance()
            right = self.multiplicative_expression()
            left = BinaryOperation(op, left, right)
        return left

    def multiplicative_expression(self):
        left = self.factor()
        while self.current_token is not None and self.current_token.type == 'OPERATOR' and self.current_token.value in ['*', '/']:
            op = self.current_token.value
            self.advance()
            right = self.factor()
            left = BinaryOperation(op, left, right)
        return left

    def factor(self):
        if self.current_token is not None and self.current_token.type == 'LPAREN':
            self.eat('LPAREN')
            expression = self.expression()
            self.eat('RPAREN')
            return expression
        elif self.current_token is not None and self.current_token.type == 'NUMBER':
            token = self.current_token
            self.eat('NUMBER')
            if self.current_token is not None and self.current_token.type == 'UNIT':
                unit_token = self.current_token
                self.eat('UNIT')
                return UnitValue(token.value, unit_token.value)
            return NumberLiteral(token.value)
        elif self.current_token is not None and self.current_token.type == 'UNIT_VALUE':
            token = self.current_token
            self.eat('UNIT_VALUE')
            return UnitValue(token.value[0], token.value[1])
        elif self.current_token is not None and self.current_token.type == 'IDENTIFIER':
            if self.peek() is not None and self.peek().type == 'LPAREN':
                return self.function_call()
            else:
                token = self.current_token
                self.eat('IDENTIFIER')
                return Variable(token.value)
        elif self.current_token is not None and self.current_token.type == 'FUNCTION':
            return self.function_call()
        else:
            self.error("Unexpected token in expression.")

    def function_call(self):
        name = self.current_token.value
        self.eat('FUNCTION')
        self.eat('LPAREN')
        args =[]
        if self.current_token.type != 'RPAREN':
            args.append(self.expression())
            while self.current_token is not None and self.current_token.type == 'COMMA':
                self.eat('COMMA')
                args.append(self.expression())
        self.eat('RPAREN')
        return FunctionCall(name, args)



def print_ast(node, indent=0):
    with open("ast_output.txt",'a') as f:
        f.write("\n " * indent + repr(node).split('(',1)[0])    #fix this
    print("  " * indent + repr(node).split('(', 1)[0]) # Print node type
    if isinstance(node, Program):
        for statement in node.statements:
            print_ast(statement, indent + 1)
    elif isinstance(node, VariableDeclaration):
        print("  " * (indent + 1) + f"name: {node.name}")
        print_ast(node.expression, indent + 1)
    elif isinstance(node, UnitConversionStatement):
        print("  " * (indent + 1) + f"target_unit: {node.target_unit}")
        print_ast(node.expression, indent + 1)
    elif isinstance(node, PrintStatement):
        print_ast(node.expression, indent + 1)
    elif isinstance(node, BinaryOperation):
        print("  " * (indent + 1) + f"op: {node.op}")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)
    elif isinstance(node, UnitValue):
        print("  " * (indent + 1) + f"value: {node.value}, unit: {node.unit}")
    elif isinstance(node, NumberLiteral):
        print("  " * (indent + 1) + f"value: {node.value}")
    elif isinstance(node, Variable):
        print("  " * (indent + 1) + f"name: {node.name}")
    elif isinstance(node, FunctionCall):
        print("  " * (indent + 1) + f"name: {node.name}")
        for arg in node.args:
            print_ast(arg, indent + 2)

            
def parse(tokens):
    parser = Parser(tokens)
    return parser.parse()

# if __name__ == '__main__':
#     from lexer import scan
#     input_file = 'input.txt'
#     try:
#         with open(input_file, 'r') as f:
#             source_code = f.read()
#     except FileNotFoundError:
#         print(f"Error: Input file '{input_file}' not found.")
#         exit()
#     tokens = scan(source_code, 'token-output.txt')
#     if tokens:
#         ast = parse(tokens[:-1]) # Exclude EOF token
#         print("Parsing successful. Abstract Syntax Tree:")
#         print_ast(ast)



