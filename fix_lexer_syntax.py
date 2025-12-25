#!/usr/bin/env python3
"""Quick fix script for lexer.py"""

path = "core/lexer.py"
with open(path, "r") as f:
    content = f.read()

# Fix line 242: add colon
content = content.replace('if c in "=+-*/:()<>,"', 'if c in "=+-*/:()<>,":')

with open(path, "w") as f:
    f.write(content)

print("✓ Fixed lexer.py syntax")
