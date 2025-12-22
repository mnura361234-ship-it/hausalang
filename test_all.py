#!/usr/bin/env python
"""Test runner for all Hausalang examples."""
from core.interpreter import run

examples = [
    ('examples/hello.ha', 'Hello World'),
    ('examples/variables.ha', 'Variables'),
    ('examples/if.ha', 'If statement'),
    ('examples/else.ha', 'Else (in ba haka ba)'),
    ('examples/comparisons.ha', 'Numeric comparisons'),
    ('examples/badvar.ha', 'Invalid variable name error'),
    ('examples/arithmetic.ha', 'Arithmetic expressions'),
    ('examples/comments.ha', 'Comments and inline expressions'),
    ('examples/functions.ha', 'Functions and string concatenation'),
    ('examples/elif_demo.ha', 'Elif (idan ... kuma)'),
]

for filepath, desc in examples:
    print(f"\n{'='*70}")
    print(f"TEST: {desc}")
    print(f"FILE: {filepath}")
    print(f"{'='*70}")
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
        print(f"Code:\n{code}")
        print(f"\n{'-'*70}\nOutput:\n{'-'*70}")
        run(code)
        print(f"{'-'*70}")

print(f"\n{'='*70}")
print("ALL TESTS COMPLETED")
print(f"{'='*70}\n")
