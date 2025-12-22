# Hausalang — A Beginner-Friendly Programming Language in Hausa

Hausalang is a simple, educational programming language designed for absolute beginners, especially Hausa speakers. It prioritizes readability and clarity over advanced features.

## Quick Start

Run a `.ha` file:

```bash
python main.py examples/hello.ha
```

## Language Features

### Variables & Strings

Assign string values to variables:

```
suna = "nura"
rubuta suna
```

### Numbers

Integers and floats are supported:

```
a = 10
b = 3.14
rubuta a
```

### Print (rubuta)

Print strings, variables, or numbers:

```
rubuta "Sannu Duniya"
rubuta suna
rubuta 42
```

### Conditionals (idan / in ba haka ba)

Use `idan` for if-statements and indent the body with 4 spaces:

```
suna = "nura"

idan suna == "nura":
    rubuta "Sannu nura"

idan suna == "ali":
    rubuta "Wani jiya"
```

Use `in ba haka ba` (else) for alternate paths:

```
a = 5

idan a > 10:
    rubuta "A big"

in ba haka ba:
    rubuta "A small"
```

### Comparison Operators

- `==` — equal
- `!=` — not equal
- `>` — greater than
- `<` — less than
- `>=` — greater than or equal
- `<=` — less than or equal

Examples:

```
idan a > b:
    rubuta "a is bigger"

idan x != 0:
    rubuta "x is nonzero"
```

### Variable Names

Variable names must:
- Start with a letter (a–z, A–Z) or underscore (_)
- Contain only letters, digits (0–9), and underscores

Valid: `suna`, `_name`, `age2`, `NAME`

Invalid: `1suna`, `suna-name`, `name!`

## Examples

The `examples/` folder contains sample programs:

- `examples/hello.ha` — prints a greeting
- `examples/variables.ha` — variable assignment and printing
- `examples/if.ha` — simple `idan` (if) usage
- `examples/else.ha` — demonstrates `in ba haka ba` (else)
- `examples/comparisons.ha` — numbers and various comparison operators
- `examples/badvar.ha` — shows invalid variable name error handling

## Error Messages

Errors are displayed in Hausa with English hints to help learners:

```
kuskure: sunan variable mara kyau -> 1suna (error: invalid variable name -> 1suna)
```

This dual format supports learning while building vocabulary in both languages.

## Implementation Notes

- **Interpreter**: A single-pass line-based interpreter written in Python.
- **Parsing**: Simple regex and string-based parsing; no external dependencies.
- **Indentation**: Blocks (if/else bodies) use 4-space indentation, Python-style.
- **Bilingual Errors**: All error messages include Hausa and English for accessibility.

## Project Structure

```
.
├── main.py                    # Entry point
├── core/
│   ├── __init__.py
│   ├── interpreter.py         # Main interpreter loop
│   ├── executor.py            # Command execution (rubuta, etc.)
│   ├── lexer.py               # (Placeholder for future tokenizer)
│   └── perser.py              # (Placeholder for future parser)
├── examples/
│   ├── hello.ha
│   ├── variables.ha
│   ├── if.ha
│   ├── else.ha
│   ├── comparisons.ha
│   └── badvar.ha
└── README.md
```

## Future Enhancements

- Arithmetic operations (+, -, *, /)
- String concatenation
- Loops (while, for)
- Functions and procedures
- Comments
- Nested blocks
- More built-in commands
- A proper lexer and parser (currently in `core/lexer.py` and `core/perser.py`)

## Contributing

Hausalang is an educational project. When contributing:

1. Keep the language simple and readable for beginners.
2. Prioritize clear error messages in both Hausa and English.
3. Maintain backward compatibility unless explicitly changing the design.
4. Test all new features with example `.ha` files.

## License

MIT (modify and use freely for educational purposes).
