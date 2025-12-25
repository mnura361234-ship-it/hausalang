#!/usr/bin/env python3
"""Quick test to verify ExpressionStatement nodes are properly created."""

from core.lexer import tokenize_program
from core.parser import parse, ExpressionStatement

code = """
aiki greet(name):
    rubuta name

x = 5
greet(x)
"""

tokens = tokenize_program(code)
ast = parse(tokens)

print("Program statements:")
for i, stmt in enumerate(ast.statements):
    print(f"  [{i}] {stmt.__class__.__name__}")
    if isinstance(stmt, ExpressionStatement):
        print(f"       Expression: {stmt.expression.__class__.__name__}")

# Verify that statement[2] (the greet(x) call) is an ExpressionStatement
assert len(ast.statements) == 3
assert ast.statements[0].__class__.__name__ == "Function"
assert ast.statements[1].__class__.__name__ == "Assignment"
assert isinstance(
    ast.statements[2], ExpressionStatement
), f"Expected ExpressionStatement, got {ast.statements[2].__class__.__name__}"

print("\n✅ ExpressionStatement correctly created for greet(x)")
