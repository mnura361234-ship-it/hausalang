#!/usr/bin/env python3
"""
Parser Examples and Testing

This script demonstrates the recursive-descent parser by showing:
1. Example Hausalang programs
2. The tokens they produce (via the lexer)
3. The resulting Abstract Syntax Tree (AST)

Run with: python test_parser.py
"""

from core.lexer import tokenize_program
from core.parser import parse


def print_tokens(code: str) -> None:
    """Tokenize and display tokens."""
    try:
        tokens = tokenize_program(code)
        print("Tokens:")
        for i, tok in enumerate(tokens):
            if tok.type not in ("NEWLINE", "INDENT", "DEDENT"):
                print(
                    f"  [{i}] {tok.type:15s} '{tok.value}' @ L{tok.line}:C{tok.column}"
                )
        print()
    except SyntaxError as e:
        print(f"Tokenization Error: {e}\n")


def print_ast(code: str, depth: int = 0) -> None:
    """Parse and display the AST in a readable format."""
    indent = "  " * depth

    # Handle Program node
    if hasattr(code, "statements"):
        print(f"{indent}Program")
        for stmt in code.statements:
            print_ast(stmt, depth + 1)
        return

    # Handle Statement nodes
    class_name = type(code).__name__

    if class_name == "Assignment":
        print(f"{indent}Assignment: {code.name} =")
        print_ast(code.value, depth + 1)

    elif class_name == "Print":
        print(f"{indent}Print:")
        print_ast(code.expression, depth + 1)

    elif class_name == "Return":
        print(f"{indent}Return:")
        print_ast(code.expression, depth + 1)

    elif class_name == "If":
        print(f"{indent}If:")
        print(f"{indent}  Condition:")
        print_ast(code.condition, depth + 2)
        print(f"{indent}  Then:")
        for stmt in code.then_body:
            print_ast(stmt, depth + 2)
        if code.else_body:
            print(f"{indent}  Else:")
            for stmt in code.else_body:
                print_ast(stmt, depth + 2)

    elif class_name == "Function":
        print(f"{indent}Function: {code.name}({', '.join(code.parameters)})")
        for stmt in code.body:
            print_ast(stmt, depth + 1)

    # Handle Expression nodes
    elif class_name == "BinaryOp":
        print(f"{indent}BinaryOp: '{code.operator}'")
        print(f"{indent}  Left:")
        print_ast(code.left, depth + 2)
        print(f"{indent}  Right:")
        print_ast(code.right, depth + 2)

    elif class_name == "Number":
        print(f"{indent}Number: {code.value}")

    elif class_name == "String":
        print(f'{indent}String: "{code.value}"')

    elif class_name == "Identifier":
        print(f"{indent}Identifier: {code.name}")

    elif class_name == "FunctionCall":
        print(f"{indent}FunctionCall: {code.name}()")
        for arg in code.arguments:
            print_ast(arg, depth + 1)


def example_1():
    """Example 1: Simple variable assignment and print"""
    code = """
x = 42
y = 3.14
rubuta x + y
"""

    print("=" * 70)
    print("EXAMPLE 1: Simple Assignment and Print")
    print("=" * 70)
    print("\nCode:")
    print(code)

    print_tokens(code)

    try:
        tokens = tokenize_program(code)
        ast = parse(tokens)
        print("AST:")
        print_ast(ast)
    except SyntaxError as e:
        print(f"Parse Error: {e}")

    print()


def example_2():
    """Example 2: Function definition and calls"""
    code = """
aiki add(a, b):
    mayar a + b

result = add(5, 3)
rubuta result
"""

    print("=" * 70)
    print("EXAMPLE 2: Function Definition and Call")
    print("=" * 70)
    print("\nCode:")
    print(code)

    print_tokens(code)

    try:
        tokens = tokenize_program(code)
        ast = parse(tokens)
        print("AST:")
        print_ast(ast)
    except SyntaxError as e:
        print(f"Parse Error: {e}")

    print()


def example_3():
    """Example 3: If/else with comparisons"""
    code = """
x = 10
idan x > 5:
    rubuta "x is big"
in ba haka ba:
    rubuta "x is small"
"""

    print("=" * 70)
    print("EXAMPLE 3: If/Else Conditional")
    print("=" * 70)
    print("\nCode:")
    print(code)

    print_tokens(code)

    try:
        tokens = tokenize_program(code)
        ast = parse(tokens)
        print("AST:")
        print_ast(ast)
    except SyntaxError as e:
        print(f"Parse Error: {e}")

    print()


def example_4():
    """Example 4: Complex nested program"""
    code = """
aiki greet(name):
    rubuta "Sannu " + name
    mayar 1

suna = "Ali"
x = 100
idan x >= 100:
    greet(suna)
    rubuta x * 2
in ba haka ba:
    rubuta "small"
"""

    print("=" * 70)
    print("EXAMPLE 4: Complex Nested Program")
    print("=" * 70)
    print("\nCode:")
    print(code)

    print_tokens(code)

    try:
        tokens = tokenize_program(code)
        ast = parse(tokens)
        print("AST:")
        print_ast(ast)
    except SyntaxError as e:
        print(f"Parse Error: {e}")

    print()


if __name__ == "__main__":
    example_1()
    example_2()
    example_3()
    example_4()

    print("=" * 70)
    print("All examples parsed successfully!")
    print("=" * 70)
