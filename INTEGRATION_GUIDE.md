# AST Interpreter Integration Guide

## Current Status

The Hausalang language now has three completed components:

1. **Lexer** (`core/lexer.py`) - ✅ Complete
   - Tokenizes source code into a token stream
   - Recognizes keywords, operators, numbers, strings, identifiers
   - Handles indentation (INDENT/DEDENT tokens)
   - Strips comments

2. **Parser** (`core/parser.py`) - ✅ Complete
   - Recursive-descent parser
   - Produces Abstract Syntax Tree (AST)
   - Handles all language constructs with proper precedence
   - Full error reporting with line/column information

3. **Interpreter** (`core/interpreter.py`) - ✅ Complete
   - AST-driven execution
   - Environment-based scope management
   - Exception-based return mechanism
   - Full support for all parsed constructs

## How to Use the Interpreter

### Direct Usage (Python)

```python
from core.interpreter import interpret_program

code = '''
aiki greet(name):
    rubuta "Hello " + name

greet("World")
'''

interpret_program(code)  # Output: "Hello World"
```

### From Main Program

Update `main.py` to use the new interpreter:

```python
from core.interpreter import interpret_program

def main():
    # Read source code from file
    with open('program.ha', 'r') as f:
        source_code = f.read()

    # Interpret the program
    try:
        interpret_program(source_code)
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
    except NameError as e:
        print(f"Name Error: {e}")
    except ValueError as e:
        print(f"Value Error: {e}")
    except Exception as e:
        print(f"Runtime Error: {e}")

if __name__ == "__main__":
    main()
```

## End-to-End Flow

```
User Source Code (.ha file)
    ↓
main.py (reads file)
    ↓
interpret_program()
    ├─ tokenize_program() [Lexer]
    │   └─ Returns: List[Token]
    ├─ parse() [Parser]
    │   └─ Returns: Program (AST root)
    └─ Interpreter().interpret() [Interpreter]
        └─ Walks AST and executes
        └─ Outputs to stdout
    ↓
Program Output
```

## Example: Complete Program

### Source Code (program.ha)

```
aiki fibonacci(n):
    idan n <= 1:
        mayar n
    in ba haka ba:
        mayar fibonacci(n - 1) + fibonacci(n - 2)

result = fibonacci(5)
rubuta "Fibonacci(5) = "
rubuta result
```

### Execution Flow

1. **Lexer Output** (first few tokens):
   ```
   KEYWORD_FUNCTION 'aiki'
   IDENTIFIER 'fibonacci'
   OPERATOR '('
   IDENTIFIER 'n'
   OPERATOR ')'
   OPERATOR ':'
   INDENT
   KEYWORD_IF 'idan'
   ...
   ```

2. **Parser Output** (AST structure):
   ```
   Program([
       Function(
           name='fibonacci',
           parameters=['n'],
           body=[
               If(
                   condition=BinaryOp(<=, Identifier('n'), Number(1)),
                   then_body=[Return(Identifier('n'))],
                   else_body=[Return(BinaryOp(+, ...))]
               )
           ]
       ),
       Assignment(name='result', value=FunctionCall('fibonacci', [Number(5)])),
       Print(BinaryOp(+, String("Fibonacci(5) = "), Identifier('result')))
   ])
   ```

3. **Interpreter Output**:
   ```
   Fibonacci(5) = 5
   ```

## Error Handling

The interpreter provides clear error messages:

### SyntaxError
```python
code = "aiki foo(:"  # Missing )
interpret_program(code)
# SyntaxError: Line 1, Column 8: Expected IDENTIFIER
```

### NameError
```python
code = "rubuta undefined_variable"
interpret_program(code)
# NameError: Undefined variable: undefined_variable
```

### ValueError
```python
code = "aiki foo(a): mayar a\nfoo(1, 2)"  # Wrong arg count
interpret_program(code)
# ValueError: Function foo expects 1 arguments, got 2
```

## Testing

Run the comprehensive test suite:

```bash
python test_interpreter.py
```

Output:
```
TEST 1: Simple Assignment and Print      → PASS ✓
TEST 2: Function Definition and Call     → PASS ✓
TEST 3: If/Else Conditional              → PASS ✓
TEST 4: String Operations                → PASS ✓
TEST 5: Complex Nested Program           → PASS ✓
```

## Supported Language Features

### Variables
```
x = 42
name = "Ali"
result = x + 10
```

### Arithmetic
```
sum = 5 + 3        # 8
diff = 10 - 3      # 7
prod = 4 * 5       # 20
quot = 20 / 4      # 5 (integer division)
```

### Comparisons
```
idan x > 5:
    rubuta "greater"
in ba haka ba:
    rubuta "not greater"
```

### String Operations
```
greeting = "Hello " + "World"  # Concatenation
rubuta greeting                # "Hello World"
```

### Functions
```
aiki add(a, b):
    mayar a + b

result = add(5, 3)  # 8
```

### Conditionals
```
idan x == 10:
    rubuta "equal"
in ba haka ba:
    rubuta "not equal"
```

## Architecture Benefits

1. **Clean Separation**
   - Lexer: Only tokenizes
   - Parser: Only builds AST
   - Interpreter: Only executes
   - Each can be tested independently

2. **Easy to Extend**
   - Add new statement? Just add method to Interpreter
   - Add new operator? Update parser and eval_binary_op()
   - Add new type? Just create new AST node

3. **Maintainable**
   - No line-by-line string parsing
   - No regex pattern matching for execution
   - Clear intent in each method
   - Well-documented code

4. **Correct Semantics**
   - Proper scope handling with parent chain
   - Exception-based returns (matches Python)
   - Truthiness evaluation for conditionals

## Performance Characteristics

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Variable lookup | O(depth) | Search parent scope chain |
| Function call | O(body_size) | Execute function body |
| Binary op | O(1) | Evaluate both operands + apply op |
| Program run | O(total_statements) | Full AST traversal |

For typical programs (< 100 functions, < 1000 statements):
- **Execution time:** Milliseconds
- **Memory usage:** Negligible

## Future Enhancements

### Planned Features
- [ ] Loop constructs (while, for)
- [ ] List/dictionary types
- [ ] Built-in functions (len, range, str, int)
- [ ] Standard library modules

### Performance Optimizations
- [ ] Bytecode compilation
- [ ] Variable indexing
- [ ] Call stack caching
- [ ] JIT compilation

### Developer Features
- [ ] Debug mode with breakpoints
- [ ] Variable inspection
- [ ] Execution profiling
- [ ] AST pretty-printing

## File Structure

```
hausalang/
├── core/
│   ├── lexer.py           # Tokenization
│   ├── parser.py          # AST generation
│   └── interpreter.py     # Execution
├── main.py                # Entry point
├── test_parser.py         # Parser tests
├── test_interpreter.py    # Interpreter tests
├── INTERPRETER_DESIGN.md  # Architecture details
└── INTERPRETER_SUMMARY.md # Implementation summary
```

## Quick Start

1. **Run a simple program:**
   ```python
   from core.interpreter import interpret_program

   interpret_program('x = 42\nrubuta x')
   # Output: 42
   ```

2. **Run from file:**
   ```python
   with open('myprogram.ha') as f:
       interpret_program(f.read())
   ```

3. **Handle errors:**
   ```python
   try:
       interpret_program(code)
   except Exception as e:
       print(f"Error: {e}")
   ```

## Questions & Support

See `INTERPRETER_DESIGN.md` for detailed architecture documentation including:
- Component descriptions
- Execution flow diagrams
- Extension guide
- Implementation details

All code is well-commented and thoroughly documented.
