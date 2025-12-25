#!/usr/bin/env python3
"""Test the AST interpreter with comprehensive examples"""

from core.interpreter import interpret_program

print("=" * 70)
print("TEST 1: Simple Assignment and Print")
print("=" * 70)

code1 = """
x = 42
y = 3
rubuta x + y
"""

print("Code:")
print(code1)
print("Output: ", end="")
interpret_program(code1)
print()

print("\n" + "=" * 70)
print("TEST 2: Function Definition and Call")
print("=" * 70)

code2 = """
aiki add(a, b):
    mayar a + b

result = add(5, 3)
rubuta result
"""

print("Code:")
print(code2)
print("Output: ", end="")
interpret_program(code2)
print()

print("\n" + "=" * 70)
print("TEST 3: If/Else Conditional")
print("=" * 70)

code3 = """
x = 10
idan x > 5:
    rubuta "x is big"
in ba haka ba:
    rubuta "x is small"
"""

print("Code:")
print(code3)
print("Output: ", end="")
interpret_program(code3)
print()

print("\n" + "=" * 70)
print("TEST 4: String Operations")
print("=" * 70)

code4 = """
name = "Ali"
greeting = "Hello " + name
rubuta greeting
"""

print("Code:")
print(code4)
print("Output: ", end="")
interpret_program(code4)
print()

print("\n" + "=" * 70)
print("TEST 5: Complex Nested Program")
print("=" * 70)

code5 = """
aiki greet(n):
    rubuta "Hi " + n

aiki multiply(a, b):
    mayar a * b

suna = "World"
x = 100
idan x >= 100:
    greet(suna)
    result = multiply(7, 6)
    rubuta result
in ba haka ba:
    rubuta "value too small"
"""

print("Code:")
print(code5)
print("Output: ", end="")
interpret_program(code5)
print()

print("\n" + "=" * 70)
print("ALL TESTS COMPLETED")
print("=" * 70)
