from lexer import scan
from parser import parse,print_ast

# if __name__ == '__main__':
#     input_file = 'input.txt'
#     output_file = 'token-output.txt'

#     try:
#         with open(input_file, 'r') as f:
#             source_code = f.read()
#     except FileNotFoundError:
#         print(f"Error: Input file '{input_file}' not found.")
#         exit()

#     print("Starting lexical analysis...")
#     tokens = scan(source_code, output_file)

#     parser=Parser(tokens)

#     if tokens:
#         print("Starting parsing...")
#         parser.parse(tokens[:-1]) # Exclude the EOF token from parsing

if __name__ == '__main__':
    from lexer import scan
    input_file = 'input.txt'
    try:
        with open(input_file, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        exit()
    tokens = scan(source_code, 'token-output.txt')
    if tokens:
        ast = parse(tokens[:-1]) # Exclude EOF token
        print("Parsing successful. Abstract Syntax Tree:")
        print_ast(ast)


# def print_ast(node, indent=0):
#     print('  ' * indent + str(node))
#     for attr_name, attr_value in node.__dict__.items():
#         if isinstance(attr_value, ASTNode):
#             print_ast(attr_value, indent + 1)
#         elif isinstance(attr_value, list):
#             for item in attr_value:
#                 if isinstance(item, ASTNode):
#                     print_ast(item, indent + 1)