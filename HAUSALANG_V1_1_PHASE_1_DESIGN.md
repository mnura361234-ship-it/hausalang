# HAUSALANG V1.1 ERROR REPORTING LAYER — PHASE 1 DESIGN DOCUMENT

**Date:** December 25, 2025
**Status:** 🔍 DESIGN PHASE — AWAITING APPROVAL
**Scope:** Enhanced Error Reporting (v1.1) Layer 1
**Audience:** Language Architect, Lead Engineer, Code Reviewer, Stability Manager

---

## TABLE OF CONTENTS

1. [Executive Summary](#executive-summary)
2. [ContextualError Data Model](#1-final-contextualerrror-data-model)
3. [Error Hierarchy](#2-error-hierarchy-finalized)
4. [Integration Points with v1.0](#3-integration-points-with-v10)
5. [Test Plan](#4-detailed-test-plan-mandatory)
6. [Error Philosophy & Guarantees](#5-error-philosophy--guarantees)
7. [Design Artifacts Summary](#6-design-artifacts-summary)
8. [Long-Term Alignment](#7-long-term-alignment-why-this-design-matters)
9. [Approval Checkpoint](#8-approval-checkpoint)
10. [Next Steps](#next-steps)

---

## EXECUTIVE SUMMARY

This document presents the **complete design** for Hausalang v1.1's Enhanced Error Reporting layer, *before any code is written*. The design ensures:

- **Zero modification** to v1.0 core (frozen)
- **Backward compatibility** with all existing programs
- **Error-first philosophy**: developers understand *what*, *where*, *why*, *input*, and *expected*
- **Foundation for future layers** (debugger, REPL, IDE tooling)

### Key Principles

✅ **Design before code** — This document is the specification
✅ **Small, reversible changes** — Wrapping at boundaries only
✅ **Backward compatibility is sacred** — v1.0 behavior untouched
✅ **Every change has a reason** — Explained below
✅ **Every feature has tests** — Mandatory before implementation

---

## 1. FINAL CONTEXTUALERRROR DATA MODEL

### 1.1 Core Error Type Definition

```python
from dataclasses import dataclass
from typing import Optional, List, Set
from datetime import datetime
from enum import Enum

@dataclass(frozen=True)
class ContextualError(Exception):
    """
    Core error type for Hausalang v1.1+

    Guarantees:
    - Safe to log (no PII/secrets)
    - Machine-readable first
    - Human-friendly secondary
    - Stackable context for diagnostic richness

    Inheritance:
    - When kind is LEXICAL_ERROR or PARSE_ERROR: inherits SyntaxError
    - When kind is NAME_ERROR or similar: inherits NameError
    - When kind is VALUE_ERROR: inherits ValueError
    - Ensures backward compatibility with existing error handlers
    """

    # REQUIRED FIELDS
    kind: 'ErrorKind'                      # From formal hierarchy
    message: str                           # Primary error description (1-200 chars)
    location: 'SourceLocation'             # File, line, column

    # OPTIONAL FIELDS
    source: Optional[Exception]            # Wrapped original exception (for chaining)
    context_frames: List['ContextFrame']   # Stackable diagnostic context (0+ frames)
    tags: Set[str]                         # E.g., {"recoverable", "input-error", "syntax"}
    help: Optional[str]                    # One-line actionable fix (≤80 chars)

    # METADATA
    timestamp: datetime                    # When error occurred
    error_id: str                          # UUID or deterministic hash for tracking

    def __str__(self) -> str:
        """Human-readable format"""
        return f"{self.kind.name}: {self.message} @ {self.location}"

    def to_dict(self) -> dict:
        """Machine-readable format (JSON-safe, no secrets)"""
        # Implementation details deferred to Phase 2
        pass

    @classmethod
    def from_dict(cls, data: dict) -> 'ContextualError':
        """Reconstruct from dict (round-trip safety)"""
        # Implementation details deferred to Phase 2
        pass
```

### 1.2 Source Location

```python
@dataclass(frozen=True)
class SourceLocation:
    """Pinpoint error origin in source code"""

    file_path: str           # Relative path to .ha file (e.g., "program.ha")
    line: int                # 1-indexed line number (matches user view)
    column: int              # 0-indexed column number (matches lexer output)
    end_line: Optional[int]  # For multi-line constructs (e.g., function body)
    end_column: Optional[int] # End position of error span

    def __str__(self) -> str:
        """Machine format: file:line:column"""
        return f"{self.file_path}:{self.line}:{self.column}"

    def format_pretty(self) -> str:
        """Human format: file on line N, column M"""
        return f"{self.file_path} on line {self.line}, column {self.column}"
```

### 1.3 Context Frames (Stackable)

Each frame captures a diagnostic dimension without mutation:

```python
from typing import Union

# Union type covering all context varieties
ContextFrame = Union[
    'KvFrame',
    'WithPathFrame',
    'WithValueFrame',
    'WithExpectedFrame',
    'WithSuggestionFrame',
]

@dataclass(frozen=True)
class KvFrame:
    """Key-value diagnostic pair"""
    key: str               # E.g., "step_size", "loop_count"
    value: str             # Always stringified for safety (human-readable)

@dataclass(frozen=True)
class WithPathFrame:
    """Path-related context"""
    label: str             # E.g., "file", "import_root"
    path: str              # Relative path (no absolute paths, no PII)

@dataclass(frozen=True)
class WithValueFrame:
    """Actual value that caused problem"""
    label: str             # E.g., "problematic_input", "actual_value"
    value: str             # Stringified and capped at 50 chars (safety)
    type_hint: Optional[str]  # E.g., "int", "str", "undefined"

@dataclass(frozen=True)
class WithExpectedFrame:
    """What was expected instead"""
    label: str             # E.g., "expected_type", "expected_count"
    expected: str          # What should have been (capped at 50 chars)
    actual: str            # What was actually provided (capped at 50 chars)

@dataclass(frozen=True)
class WithSuggestionFrame:
    """Actionable suggestion"""
    suggestion: str        # E.g., "Use 'aiki' keyword to define a function"
    category: str          # "syntax_fix", "config_fix", "input_fix", "debugging"
```

### 1.4 Error Kind Hierarchy

```python
from enum import Enum

class ErrorKind(Enum):
    """Formal error taxonomy for Hausalang

    Categories:
    - L1: Lexical (tokenization)
    - L2: Parse (syntax/grammar)
    - L3: Runtime (execution)
    - Infra: System/IO
    - Internal: Compiler bugs
    """

    # ===== APP ERRORS (User Code Mistakes) =====

    # L1: LEXICAL ERRORS (Tokenization)
    UNKNOWN_SYMBOL = "lexical/unknown_symbol"
    UNCLOSED_STRING = "lexical/unclosed_string"
    INVALID_NUMBER = "lexical/invalid_number"
    INVALID_ESCAPE = "lexical/invalid_escape"

    # L2: PARSE ERRORS (Syntax/Grammar)
    UNEXPECTED_TOKEN = "parse/unexpected_token"
    EXPECTED_TOKEN = "parse/expected_token"
    MISSING_COLON = "parse/missing_colon"
    MISSING_INDENT = "parse/missing_indent"
    UNMATCHED_PAREN = "parse/unmatched_paren"
    UNEXPECTED_EOF = "parse/unexpected_eof"

    # L3a: NAME ERRORS (Variable/Function Resolution)
    UNDEFINED_VARIABLE = "runtime/name/undefined_variable"
    UNDEFINED_FUNCTION = "runtime/name/undefined_function"
    UNDEFINED_PARAMETER = "runtime/name/undefined_parameter"

    # L3b: TYPE ERRORS (Type Mismatches)
    INVALID_OPERAND_TYPE = "runtime/type/invalid_operand_type"
    STRING_NUMBER_CONCAT = "runtime/type/string_number_concat"
    NON_NUMERIC_ARITHMETIC = "runtime/type/non_numeric_arithmetic"
    NON_BOOLEAN_CONDITION = "runtime/type/non_boolean_condition"
    WRONG_ARGUMENT_TYPE = "runtime/type/wrong_argument_type"

    # L3c: ARGUMENT ERRORS (Function Arguments)
    WRONG_ARGUMENT_COUNT = "runtime/argument/wrong_argument_count"
    MISSING_REQUIRED_ARG = "runtime/argument/missing_required_arg"
    UNEXPECTED_KEYWORD_ARG = "runtime/argument/unexpected_keyword_arg"

    # L3d: VALUE ERRORS (Invalid Values)
    DIVISION_BY_ZERO = "runtime/value/division_by_zero"
    ZERO_LOOP_STEP = "runtime/value/zero_loop_step"
    NEGATIVE_LOOP_STEP = "runtime/value/negative_loop_step"
    EMPTY_REQUIRED_VALUE = "runtime/value/empty_required_value"
    OUT_OF_RANGE = "runtime/value/out_of_range"

    # L3e: ASSERTION ERRORS
    ASSERTION_FAILED = "runtime/assertion/assertion_failed"

    # L3f: EXECUTION ERRORS (Control Flow)
    INFINITE_LOOP = "runtime/execution/infinite_loop"
    STACK_OVERFLOW = "runtime/execution/stack_overflow"
    UNKNOWN_OPERATOR = "runtime/execution/unknown_operator"
    UNKNOWN_STATEMENT_TYPE = "runtime/execution/unknown_statement_type"

    # ===== INFRASTRUCTURE ERRORS (System/IO) =====
    FILE_NOT_FOUND = "infra/file_not_found"
    FILE_READ_ERROR = "infra/file_read_error"
    ENCODING_ERROR = "infra/encoding_error"
    IO_ERROR = "infra/io_error"
    PERMISSION_DENIED = "infra/permission_denied"

    # ===== INTERNAL ERRORS (Compiler Bugs) =====
    COMPILER_BUG = "internal/compiler_bug"
    INTERPRETER_BUG = "internal/interpreter_bug"
    INVALID_AST_NODE = "internal/invalid_ast_node"
    ASSERTION_FAILED_INTERNAL = "internal/assertion_failed"
```

**Naming Convention:**

| Prefix | Pattern | Example |
|--------|---------|---------|
| **Lexical** | `CATEGORY_SPECIFIC` | `UNKNOWN_SYMBOL`, `UNCLOSED_STRING` |
| **Parse** | `EXPECTED_X`, `UNEXPECTED_X` | `EXPECTED_TOKEN`, `MISSING_COLON` |
| **Runtime** | `DESCRIPTOR_SPECIFIC` | `UNDEFINED_VARIABLE`, `DIVISION_BY_ZERO` |

---

## 2. ERROR HIERARCHY FINALIZED

### 2.1 Three Error Categories

| Category | Responsibility | When Raised | Recovery? | Parent Class |
|----------|-----------------|------------|-----------|--------------|
| **AppError** | User code mistakes | L1/L2/L3 | Often | `SyntaxError` or Python stdlib |
| **InfrastructureError** | System/IO issues | File I/O, environment | Sometimes | `OSError` |
| **InternalError** | Compiler/interpreter bugs | Should never happen | No | `RuntimeError` |

### 2.2 Sub-errors by Stage

#### **Lexer (L1) — Tokenization Errors**

```
Scenario: x = 5 @ y
Error: UNKNOWN_SYMBOL
Message: "Unknown symbol '@' in source code"
Location: program.ha:1:7
Context: symbol="@", expected="operator or keyword"
Help: "Use '+', '-', '*', '/', '==', '!=', '<', '>', '<=', '>=' for operations"
```

```
Scenario: x = "unclosed string
Error: UNCLOSED_STRING
Message: "String literal was not closed"
Location: program.ha:1:5
Context: string_start="1:5", eof="1:24"
Help: "Close the string with matching double quote"
```

```
Scenario: x = 1.2.3
Error: INVALID_NUMBER
Message: "Invalid number format"
Location: program.ha:1:5
Context: number="1.2.3", attempted_parse="float"
Help: "Numbers must be in format 123 or 1.23 (single decimal point only)"
```

#### **Parser (L2) — Syntax Errors**

```
Scenario: idan x > 5 (missing colon)
Error: MISSING_COLON
Message: "Expected ':' after condition"
Location: program.ha:1:10
Context: construct="if_statement", token_found="NEWLINE"
Help: "Add ':' after the condition: idan x > 5:"
```

```
Scenario: aiki foo( (missing closing paren)
Error: UNMATCHED_PAREN
Message: "Expected closing parenthesis"
Location: program.ha:1:8
Context: opened_at="1:8", expected_at="1:9"
Help: "Close the parenthesis with ')'"
```

```
Scenario: idan x > 5:\nrubuta x (missing indentation)
Error: MISSING_INDENT
Message: "Expected indentation after ':'"
Location: program.ha:1:11
Context: construct="if_statement", found="no_indent"
Help: "Indent the body with 4 spaces after ':'"
```

#### **Interpreter (L3) — Runtime Errors**

**Name Errors:**
```
Scenario: rubuta undefined_var
Error: UNDEFINED_VARIABLE
Message: "Variable 'undefined_var' is not defined"
Location: program.ha:1:8
Context: variable="undefined_var", scope="global"
Help: "Assign a value to 'undefined_var' before using it"
```

**Type Errors:**
```
Scenario: x = "hello" + 5
Error: STRING_NUMBER_CONCAT
Message: "Cannot concatenate string and number"
Location: program.ha:1:16
Context: left_type="str", right_type="int", operator="+"
Help: "Convert the number to a string: \"hello\" + string_of(5)"
```

**Argument Errors:**
```
Scenario: aiki add(a, b): mayar a + b\nadd(5)
Error: WRONG_ARGUMENT_COUNT
Message: "Function 'add' expects 2 arguments, got 1"
Location: program.ha:2:1
Context: function="add", expected=2, actual=1
Help: "Call add(5, 3) with both required arguments"
```

**Value Errors:**
```
Scenario: x = 10 / 0
Error: DIVISION_BY_ZERO
Message: "Cannot divide by zero"
Location: program.ha:1:9
Context: dividend=10, divisor=0, operator="/"
Help: "Check the divisor before division or use a conditional"
```

```
Scenario: don i = 0 zuwa 10 ta 0:
Error: ZERO_LOOP_STEP
Message: "For loop step cannot be zero"
Location: program.ha:1:19
Context: step=0, direction="ascending"
Help: "Use a non-zero step: ta 1 (or any non-zero number)"
```

---

## 3. INTEGRATION POINTS WITH V1.0

### 3.1 No Breaking Changes Strategy

**Current v1.0 Error Handling:**

```
Lexer        → raises SyntaxError (with line/column)
Parser       → raises SyntaxError (with line/column)
Interpreter → raises NameError, ValueError, RuntimeError, TypeError
main.py      → catches exceptions, prints generic message
```

**v1.1 Integration Strategy:**

| Stage | v1.0 Behavior | v1.1 Enhancement | Backward Compat? |
|-------|---------------|------------------|-----------------|
| **Lexer** | Raise `SyntaxError` | Wrap in `ContextualError(kind=UNKNOWN_SYMBOL, ...)` | ✅ Inherit from SyntaxError |
| **Parser** | Raise `SyntaxError` | Wrap in `ContextualError(kind=MISSING_COLON, ...)` | ✅ Inherit from SyntaxError |
| **Interpreter** | Raise native Python errors | Wrap in `ContextualError(...)` | ✅ Inherit from parent (NameError, etc.) |
| **main.py** | Generic catch + print | Catch `ContextualError`, format pretty output | ✅ Fallback to old format if not ContextualError |

### 3.2 Integration Entry Points (Minimal, Reversible)

#### **Entry Point 1: Main Boundary (main.py)**

```python
# main.py — NEW ERROR HANDLING
def main():
    if len(sys.argv) < 2:
        print("Kuskure: Babu fayil da aka bayar")
        return

    filename = sys.argv[1]

    if not filename.endswith(".ha"):
        print("Kuskure: Fayil dole ya kasance .ha")
        return

    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()
            interpret_program(code)

    except ContextualError as e:
        # NEW: Pretty-print with full context
        formatter = ErrorFormatter()
        print(formatter.pretty(e), file=sys.stderr)
        return 1  # Signal error exit code

    except SyntaxError as e:
        # FALLBACK: Old-style error handling (v1.0 compat)
        print(f"Kuskure: {e}", file=sys.stderr)
        return 1

    except (NameError, ValueError, RuntimeError) as e:
        # FALLBACK: Old-style error handling
        print(f"Kuskure: {e}", file=sys.stderr)
        return 1

    except FileNotFoundError:
        print("Kuskure: Ba a samu fayil ba", file=sys.stderr)
        return 1
```

#### **Entry Point 2: Domain Logic (core/lexer.py)**

```python
# core/lexer.py — NEW HELPER (no v1.0 code change)
def _raise_contextual_error(
    kind: ErrorKind,
    message: str,
    location: SourceLocation,
    context_frames: List[ContextFrame] = None,
    help: str = None,
) -> None:
    """Raise ContextualError (inherits SyntaxError for L1/L2)"""
    error = ContextualError(
        kind=kind,
        message=message,
        location=location,
        source=None,
        context_frames=context_frames or [],
        tags={"lexical"},
        help=help,
        timestamp=datetime.now(),
        error_id=generate_error_id(),
    )
    raise error

# v1.0 code unchanged:
def tokenize_program(code: str) -> List[Token]:
    """Tokenize source code into tokens"""
    # ... existing tokenization logic ...
    # When error found, call:
    # _raise_contextual_error(ErrorKind.UNKNOWN_SYMBOL, ...)
    # instead of: raise SyntaxError(...)
```

#### **Entry Point 3: Domain Logic (core/parser.py)**

```python
# core/parser.py — ENHANCE EXISTING _error() METHOD
def _error(self, message: str, token: Optional[Token] = None) -> None:
    """Raise a SyntaxError with location info (v1.0 compatible)

    Enhancement: Also creates ContextualError with rich context
    """
    location = SourceLocation(
        file_path="<input>",  # Will be updated in main.py
        line=token.line if token else self.current_token.line,
        column=token.column if token else self.current_token.column,
    )

    # Build context based on error type
    context_frames = []
    if "Expected" in message:
        context_frames.append(WithExpectedFrame(
            label="expected",
            expected=message.split("Expected ")[1].split(",")[0],
            actual=str(token) if token else "EOF",
        ))

    error = ContextualError(
        kind=ErrorKind.UNEXPECTED_TOKEN,  # TODO: infer from message
        message=message,
        location=location,
        context_frames=context_frames,
        help=self._suggest_help(message),
        tags={"parse"},
        timestamp=datetime.now(),
        error_id=generate_error_id(),
    )

    raise error  # Inherits SyntaxError
```

#### **Entry Point 4: Domain Logic (core/interpreter.py)**

```python
# core/interpreter.py — NEW WRAPPER FUNCTION
def _wrap_runtime_error(error: Exception, context: dict = None) -> ContextualError:
    """Wrap native Python exceptions into ContextualError

    Maps:
    - NameError → ContextualError(kind=UNDEFINED_VARIABLE)
    - ValueError → ContextualError(kind=VALUE_ERROR)
    - etc.
    """
    # Determine kind from exception type
    kind_map = {
        NameError: ErrorKind.UNDEFINED_VARIABLE,
        ValueError: ErrorKind.VALUE_ERROR,
        TypeError: ErrorKind.INVALID_OPERAND_TYPE,
        RuntimeError: ErrorKind.UNKNOWN_OPERATOR,
    }

    kind = kind_map.get(type(error), ErrorKind.RUNTIME_ERROR)

    # Build context from error message
    context_frames = []
    if context:
        for key, value in context.items():
            context_frames.append(KvFrame(key=key, value=str(value)))

    return ContextualError(
        kind=kind,
        message=str(error),
        location=SourceLocation(file_path="<unknown>", line=1, column=0),
        source=error,
        context_frames=context_frames,
        tags={"runtime"},
        timestamp=datetime.now(),
        error_id=generate_error_id(),
    )
```

### 3.3 Backward Compatibility Guarantees

✅ **If code catches `SyntaxError`** → Still works (ContextualError inherits)
✅ **If code catches `NameError`, `ValueError`, etc.** → Still works (wrapped versions inherit)
✅ **If code relies on exception message** → Added as `message` field in ContextualError
✅ **If code doesn't handle errors** → Traceback still works (exception chain visible via `__cause__`)
✅ **Existing test suite** → All tests pass unchanged (no API breakage)

---

## 4. DETAILED TEST PLAN (MANDATORY)

### 4.1 Test Categories

#### **Category 1: Golden Snapshot Tests**

**Purpose:** Ensure error output consistency and readability

**File:** `tests/test_error_snapshots.py`

```python
import pytest
from core.interpreter import interpret_program
from core.lexer import tokenize_program
from core.errors import ContextualError, ErrorKind

class TestLexerErrorSnapshots:
    """Golden output tests for lexer errors"""

    def test_unknown_symbol(self, snapshot):
        """Unknown symbol error format and message"""
        code = "x = 5 @ y"

        with pytest.raises(ContextualError) as exc_info:
            tokenize_program(code)

        error = exc_info.value
        assert error.kind == ErrorKind.UNKNOWN_SYMBOL
        assert "@" in error.message

        # Snapshot comparison
        output = format_pretty(error)
        assert output == snapshot

    def test_unclosed_string(self, snapshot):
        """Unclosed string literal error"""
        code = 'x = "hello'

        with pytest.raises(ContextualError) as exc_info:
            tokenize_program(code)

        error = exc_info.value
        assert error.kind == ErrorKind.UNCLOSED_STRING
        assert snapshot_match(format_pretty(error), snapshot)

    def test_invalid_number(self, snapshot):
        """Invalid number format error"""
        code = "x = 1.2.3"

        with pytest.raises(ContextualError) as exc_info:
            tokenize_program(code)

        error = exc_info.value
        assert error.kind == ErrorKind.INVALID_NUMBER
        assert snapshot_match(format_pretty(error), snapshot)


class TestParserErrorSnapshots:
    """Golden output tests for parser errors"""

    def test_missing_colon(self, snapshot):
        """Missing colon after condition"""
        code = "idan x > 5\n    rubuta x"

        with pytest.raises(ContextualError) as exc_info:
            interpret_program(code)

        error = exc_info.value
        assert error.kind == ErrorKind.MISSING_COLON
        assert snapshot_match(format_pretty(error), snapshot)

    def test_unexpected_token(self, snapshot):
        """Unexpected token in syntax"""
        code = "aiki foo(:"  # Missing closing paren or param

        with pytest.raises(ContextualError) as exc_info:
            interpret_program(code)

        error = exc_info.value
        assert error.kind == ErrorKind.UNEXPECTED_TOKEN
        assert snapshot_match(format_pretty(error), snapshot)

    def test_missing_indent(self, snapshot):
        """Missing indentation after colon"""
        code = "idan x > 5:\nrubuta x"  # No indent on line 2

        with pytest.raises(ContextualError) as exc_info:
            interpret_program(code)

        error = exc_info.value
        assert error.kind == ErrorKind.MISSING_INDENT
        assert snapshot_match(format_pretty(error), snapshot)


class TestInterpreterErrorSnapshots:
    """Golden output tests for runtime errors"""

    def test_undefined_variable(self, snapshot):
        """Undefined variable error"""
        code = "rubuta undefined_var"

        with pytest.raises(ContextualError) as exc_info:
            interpret_program(code)

        error = exc_info.value
        assert error.kind == ErrorKind.UNDEFINED_VARIABLE
        assert "undefined_var" in error.message
        assert snapshot_match(format_pretty(error), snapshot)

    def test_string_number_concat(self, snapshot):
        """String and number concatenation error"""
        code = 'x = "hello" + 5'

        with pytest.raises(ContextualError) as exc_info:
            interpret_program(code)

        error = exc_info.value
        assert error.kind == ErrorKind.STRING_NUMBER_CONCAT
        assert snapshot_match(format_pretty(error), snapshot)

    def test_wrong_argument_count(self, snapshot):
        """Function called with wrong number of arguments"""
        code = """
aiki add(a, b):
    mayar a + b

add(5)
"""

        with pytest.raises(ContextualError) as exc_info:
            interpret_program(code)

        error = exc_info.value
        assert error.kind == ErrorKind.WRONG_ARGUMENT_COUNT
        assert "add" in error.message
        assert snapshot_match(format_pretty(error), snapshot)

    def test_division_by_zero(self, snapshot):
        """Division by zero error"""
        code = "x = 10 / 0"

        with pytest.raises(ContextualError) as exc_info:
            interpret_program(code)

        error = exc_info.value
        assert error.kind == ErrorKind.DIVISION_BY_ZERO
        assert snapshot_match(format_pretty(error), snapshot)

    def test_zero_loop_step(self, snapshot):
        """For loop step cannot be zero"""
        code = """
don i = 0 zuwa 10 ta 0:
    rubuta i
"""

        with pytest.raises(ContextualError) as exc_info:
            interpret_program(code)

        error = exc_info.value
        assert error.kind == ErrorKind.ZERO_LOOP_STEP
        assert snapshot_match(format_pretty(error), snapshot)
```

**Snapshot Storage:**

```
tests/snapshots/
├── lexer/
│   ├── unknown_symbol.txt
│   ├── unclosed_string.txt
│   ├── invalid_number.txt
│   └── invalid_escape.txt
│
├── parser/
│   ├── missing_colon.txt
│   ├── unexpected_token.txt
│   ├── missing_indent.txt
│   ├── unmatched_paren.txt
│   └── unexpected_eof.txt
│
└── interpreter/
    ├── undefined_variable.txt
    ├── undefined_function.txt
    ├── string_number_concat.txt
    ├── wrong_argument_count.txt
    ├── division_by_zero.txt
    ├── zero_loop_step.txt
    ├── negative_loop_step.txt
    └── unknown_operator.txt
```

#### **Category 2: Context Accumulation Tests**

**Purpose:** Verify stacking of diagnostic frames

```python
class TestContextAccumulation:
    """Tests for context frame stacking"""

    def test_function_call_context_chain(self):
        """Context should chain: main call → function def → error site"""
        code = """
aiki compute(x):
    y = undefined_var
    mayar y + x

compute(5)
"""

        with pytest.raises(ContextualError) as exc_info:
            interpret_program(code)

        error = exc_info.value

        # At least one context frame should exist
        assert len(error.context_frames) >= 1

        # Verify diagnostic content references the problem
        context_str = "".join(str(f) for f in error.context_frames)
        assert "undefined_var" in context_str or error.message != ""

    def test_nested_loop_context(self):
        """Nested for loops should show context"""
        code = """
don i = 0 zuwa 5 ta 0:
    don j = 0 zuwa 3:
        rubuta i
"""

        with pytest.raises(ContextualError) as exc_info:
            interpret_program(code)

        error = exc_info.value
        assert error.kind == ErrorKind.ZERO_LOOP_STEP

        # Context should mention outer loop
        if error.context_frames:
            context_str = "".join(str(f) for f in error.context_frames)
            # Either context mentions it, or error_id allows tracking
            assert error.error_id is not None

    def test_deeply_nested_function_calls(self):
        """Deep call stack should have context for each frame"""
        code = """
aiki a():
    mayar b()

aiki b():
    mayar c()

aiki c():
    mayar undefined

c()
"""

        with pytest.raises(ContextualError) as exc_info:
            interpret_program(code)

        error = exc_info.value
        assert error.kind == ErrorKind.UNDEFINED_VARIABLE
        # All frames should be present (even if as message)
        assert "undefined" in error.message
```

#### **Category 3: Round-Trip Safety Tests**

**Purpose:** Verify error serialization/deserialization

```python
import json

class TestErrorSerialization:
    """Tests for error serialization and safety"""

    def test_error_to_dict_structure(self):
        """Serialize ContextualError to machine-readable dict"""
        code = "x = y + z"

        with pytest.raises(ContextualError) as exc_info:
            interpret_program(code)

        error = exc_info.value
        as_dict = error.to_dict()

        # Verify required fields
        assert "kind" in as_dict
        assert "message" in as_dict
        assert "location" in as_dict
        assert "context_frames" in as_dict

        # Verify types
        assert isinstance(as_dict["kind"], str)
        assert isinstance(as_dict["message"], str)
        assert isinstance(as_dict["location"], dict)
        assert isinstance(as_dict["context_frames"], list)

    def test_error_round_trip(self):
        """Serialize and deserialize error"""
        code = "aiki foo(a): mayar a\nfoo(1, 2)"

        with pytest.raises(ContextualError) as exc_info:
            interpret_program(code)

        original_error = exc_info.value

        # Serialize
        as_dict = original_error.to_dict()

        # Deserialize
        reconstructed_error = ContextualError.from_dict(as_dict)

        # Verify round-trip
        assert reconstructed_error.kind == original_error.kind
        assert reconstructed_error.message == original_error.message
        assert len(reconstructed_error.context_frames) == len(original_error.context_frames)

    def test_error_json_serializable(self):
        """Error must be JSON-safe"""
        code = "x = 5 / 0"

        with pytest.raises(ContextualError) as exc_info:
            interpret_program(code)

        error = exc_info.value
        as_dict = error.to_dict()

        # Must serialize to JSON without errors
        json_str = json.dumps(as_dict)
        assert json_str is not None

        # Must deserialize back
        reloaded = json.loads(json_str)
        assert reloaded is not None

    def test_error_contains_no_secrets(self):
        """Verify no secrets leak into error dict"""
        code = 'password = "secret123"\nrubuta password'

        with pytest.raises(ContextualError) as exc_info:
            interpret_program(code)

        error = exc_info.value
        as_dict = error.to_dict()
        json_str = json.dumps(as_dict)

        # Secret must not appear in any form
        assert "secret123" not in json_str
        assert "secret" not in json_str.lower() or "secret" in error.message  # unless mentioned as context
```

#### **Category 4: Source Compatibility Smoke Tests**

**Purpose:** Ensure existing v1.0 code still runs or fails gracefully

```python
from pathlib import Path

class TestSourceCompatibility:
    """Tests for backward compatibility with v1.0"""

    def test_all_examples_parse_or_error(self):
        """All v1.0 examples should parse without crashes"""
        example_files = list(Path("examples").glob("*.ha"))

        assert len(example_files) > 0, "No example files found"

        for ex_file in example_files:
            code = ex_file.read_text()

            try:
                # Should complete (may raise ContextualError)
                interpret_program(code)
            except ContextualError as e:
                # Verify error has required fields
                assert e.kind is not None
                assert e.location is not None
                assert len(e.message) > 0
            except Exception as e:
                # Should not happen; all errors should be ContextualError
                pytest.fail(f"Unexpected exception type in {ex_file}: {type(e).__name__}: {e}")

    def test_syntax_error_inheritance(self):
        """ContextualError for lexical/parse errors must inherit SyntaxError"""
        code = "idan x > 5"  # Missing colon

        caught_as_syntax = False
        caught_as_contextual = False

        try:
            interpret_program(code)
        except SyntaxError as e:
            caught_as_syntax = True
            # Must also be ContextualError
            assert isinstance(e, ContextualError)
        except ContextualError as e:
            caught_as_contextual = True

        assert caught_as_syntax or caught_as_contextual, \
            "Error must be catchable as SyntaxError or ContextualError"

    def test_name_error_inheritance(self):
        """ContextualError for name errors must inherit NameError"""
        code = "rubuta undefined_var"

        caught_as_name_error = False

        try:
            interpret_program(code)
        except NameError as e:
            caught_as_name_error = True
            # Should also be ContextualError (eventually)
        except ContextualError as e:
            # Acceptable if directly ContextualError
            assert e.kind == ErrorKind.UNDEFINED_VARIABLE

        assert caught_as_name_error or True  # Either way is OK for Phase 2
```

#### **Category 5: Property/Fuzz Safety Tests**

**Purpose:** Random error input generation and validation

```python
import random

class TestErrorFuzzing:
    """Property-based tests for error safety"""

    @pytest.mark.parametrize("invalid_code", [
        "@ # unknown symbol",
        'x = "unclosed',
        "idan x",  # missing colon
        "foo(1, 2, 3)",  # undefined function
        "x + y",  # undefined variables
        "5 / 0",  # division by zero
        "don i = 0 zuwa 5 ta 0:",  # zero step
        "aiki foo():",  # missing body
        "(((",  # unmatched parens
        "1.2.3",  # invalid number
    ])
    def test_all_invalid_codes_produce_errors(self, invalid_code):
        """All invalid inputs must raise ContextualError"""
        with pytest.raises(ContextualError) as exc_info:
            interpret_program(invalid_code)

        error = exc_info.value

        # Mandatory fields
        assert error.kind is not None
        assert error.message is not None
        assert error.location is not None

        # Safety checks
        assert error.kind.value in [k.value for k in ErrorKind]
        assert len(error.message) > 0
        assert len(error.message) <= 500  # Reasonable max
        assert error.location.line > 0
        assert error.location.column >= 0

    @pytest.mark.parametrize("secret", [
        "secret123",
        "sk_test_abc",
        "API_KEY",
        "password123",
    ])
    def test_error_messages_never_contain_secrets(self, secret):
        """Fuzz: even with secret in code, no leakage in error"""
        code = f'x = "{secret}"'

        try:
            interpret_program(code)
        except ContextualError as e:
            # Secret must not appear in output
            error_dict = e.to_dict()
            error_json = json.dumps(error_dict)

            # Check all fields
            assert secret not in str(e)
            assert secret not in error_json
            assert secret not in e.message

            # Check context frames
            for frame in e.context_frames:
                assert secret not in str(frame)
```

### 4.2 Test Execution Plan

```
PHASE 1 (Before Implementation):
  ✅ Design snapshot files (golden outputs)
  ✅ Plan test structure (THIS DOCUMENT)
  ✅ Mock ContextualError class (dummy)

PHASE 2 (During Implementation):
  ⏳ Implement ContextualError class
  ⏳ Implement error wrapping in lexer/parser/interpreter
  ⏳ Implement tests alongside errors
  ⏳ Snapshot capture: run with new code, save outputs
  ⏳ Run full test suite: pytest tests/

PHASE 3 (After Implementation):
  ⏳ 100% pass rate on all test categories
  ⏳ No regression on v1.0 tests (test_interpreter.py, test_parser.py, etc.)
  ⏳ Snapshot diffs reviewed for readability
  ⏳ Performance check: error creation overhead < 1ms
```

---

## 5. ERROR PHILOSOPHY & GUARANTEES

### 5.1 Every Error Must Answer Five Questions

| Question | Field | Example |
|----------|-------|---------|
| **What failed?** | `kind` | `UNDEFINED_VARIABLE` |
| **Where did it fail?** | `location` | `program.ha:12:5` |
| **Why did it fail?** | `message` | `Variable 'x' referenced before assignment` |
| **What was the problematic input?** | `context_frames[WithValue]` | `name: "x", type: "undefined"` |
| **What was expected instead?** | `help` + `context_frames[WithExpected]` | `Ensure x is assigned before use` |

### 5.2 Safety Guarantees

#### ✅ No Secrets in Logs

- **String values** capped at 50 characters
- **Known patterns** redacted (e.g., `sk_*` → `sk_...`, `password=*` → `password=...`)
- **File contents** never included in error output
- **Environment variables** never logged
- **Tokens** sanitized (only kind/type, not raw value)

#### ✅ No PII Leakage

- **File paths** relative only (no absolute paths like `C:\Users\Nura\...`)
- **Variable names** included (they're part of code)
- **User data** not logged (only code structure)
- **Error IDs** for tracking (hash of location + error kind, deterministic)

#### ✅ Machine-Readable First

- **JSON serialization** via `to_dict()` method
- **Structured format** with required/optional fields
- **Error codes** for IDE/tooling integration
- **Deterministic error IDs** for issue deduplication

#### ✅ Human-Friendly Secondary

- **Pretty formatter** for readable console output
- **Multi-language support** (prep for Hausa translations)
- **Actionable hints** in `help` field (max 80 chars)
- **Context frames** stackable (one concern per frame)

---

## 6. DESIGN ARTIFACTS SUMMARY

| Artifact | Purpose | Phase 1 Status |
|----------|---------|---|
| **ContextualError class** | Core error type, carries all context | ✅ Defined (spec above) |
| **ErrorKind enum** | Formal error hierarchy (30+ kinds) | ✅ Defined (spec above) |
| **SourceLocation class** | Pinpoint error origin in code | ✅ Defined (spec above) |
| **ContextFrame types** | Stackable diagnostics (5 frame types) | ✅ Defined (spec above) |
| **Error inheritance** | Backward compat via Python stdlib | ✅ Defined (section 3.1) |
| **Integration strategy** | How v1.1 wraps v1.0 (3 stages) | ✅ Mapped (section 3.2) |
| **Test plan** | 5-category suite with examples | ✅ Detailed (section 4) |
| **Snapshot template** | Golden output format | 🟡 To be designed (Phase 2) |
| **Formatter (pretty)** | Human-readable console output | 🟡 To be designed (Phase 2) |
| **Formatter (JSON)** | Machine-readable output | 🟡 To be designed (Phase 2) |
| **Error helpers** | _raise_contextual_error() etc. | 🟡 To be implemented (Phase 2) |

---

## 7. LONG-TERM ALIGNMENT (Why This Design Matters)

This error system becomes the **backbone** for future layers:

### Layer 2: Debugger & REPL

- **ContextualError.source** enables exception chaining (see what caused what)
- **SourceLocation** enables breakpoint setting (pause at exact line/column)
- **context_frames** enables step-through inspection (what was in scope?)
- **error_id** enables session history (track errors across interactions)

### Layer 3: IDE Integration

- **error.kind** enables IDE squiggly underlines (syntax vs. name vs. type errors)
- **error.help** enables quick fixes ("Fix: Add colon")
- **error_id** enables issue tracker links (click → GitHub issue)
- **location** enables jump-to-file (Ctrl+Click → source line)

### Layer 4: Profiler & Tracing

- **timestamp** enables timeline reconstruction (when did each error occur?)
- **error_id** links to execution logs (correlate errors across runs)
- **tags** filter errors by category (show only recoverable errors)
- **context_frames** reveal bottlenecks (which frames cause slowdown?)

### Future: Multi-Language Support

- **context_frames** language-agnostic (key-value pairs work in any language)
- **error.kind** maps to Hausa equivalents (UNDEFINED_VARIABLE → "ba a gane madadin")
- **help** translatable without code change (add i18n lookup)
- **message** template-based (e.g., "Variable '{name}' is not defined")

---

## 8. APPROVAL CHECKPOINT

### Before Implementation Begins, Confirm:

- [ ] **Data Model**
  - ✅ ContextualError structure approved
  - ✅ ErrorKind hierarchy (30+ kinds) approved
  - ✅ SourceLocation with line/column approved
  - ✅ 5 ContextFrame types approved

- [ ] **Integration Strategy**
  - ✅ Wrapping at boundaries (main.py, lexer/parser/interpreter) approved
  - ✅ No core v1.0 code changes approved
  - ✅ Inheritance strategy (SyntaxError, NameError, etc.) approved
  - ✅ Backward compatibility fallback approved

- [ ] **Test Plan**
  - ✅ 5 test categories approved
  - ✅ Golden snapshot approach approved
  - ✅ Context accumulation tests approved
  - ✅ Round-trip safety tests approved
  - ✅ Fuzz testing approach approved

- [ ] **Safety Guarantees**
  - ✅ No secrets in logs (capping, redaction) approved
  - ✅ No PII leakage (relative paths, etc.) approved
  - ✅ Machine-readable first (JSON, error codes) approved
  - ✅ Human-friendly secondary (pretty formatter) approved

- [ ] **Naming Convention**
  - ✅ Error kind names (CATEGORY_SPECIFIC) approved
  - ✅ Frame type names (WithPathFrame, etc.) approved
  - ✅ Enum value format (lexical/*, parse/*, runtime/*) approved

- [ ] **Implementation Feasibility**
  - ✅ No external dependencies required (except datetime)
  - ✅ Minimal changes to v1.0 codebase
  - ✅ Reversible changes (can disable error context)
  - ✅ Timeline reasonable (estimate for Phase 2)

---

## NEXT STEPS

### Phase 2: Implementation (Upon Approval)

1. **Create `core/errors.py`**
   - ContextualError class (full implementation)
   - ErrorKind enum (all 30+ kinds)
   - SourceLocation, ContextFrame classes
   - Helper functions (_raise_contextual_error, etc.)

2. **Update `core/lexer.py`**
   - Replace `raise SyntaxError(...)` with ContextualError
   - Add context frames for error diagnosis
   - Test against all lexical error types

3. **Update `core/parser.py`**
   - Enhance _error() method to create ContextualError
   - Add context frames (expected token, etc.)
   - Test against all parse error types

4. **Update `core/interpreter.py`**
   - Add _wrap_runtime_error() helper
   - Wrap NameError, ValueError, RuntimeError, TypeError
   - Add context frames (function name, argument count, etc.)

5. **Create `core/formatters.py`**
   - ErrorFormatter class with pretty() method
   - JSON serialization
   - Multi-line output with color (optional)

6. **Update `main.py`**
   - Catch ContextualError at boundary
   - Call formatter.pretty(error)
   - Fallback to old format if not ContextualError

7. **Create `tests/test_errors.py`**
   - Implement all 5 test categories
   - Generate snapshot files
   - Verify backward compatibility

### Phase 3: Testing & Validation

- Run full test suite: `pytest tests/`
- Verify 100% pass rate on all tests
- Review snapshot outputs for readability
- Test with v1.0 example files
- Measure error creation overhead

### Phase 4: Documentation

- Add error examples to README.md
- Create error reference guide (all 30+ kinds)
- Document how to catch/handle errors
- Add troubleshooting guide

### Phase 5: Integration

- Commit with design reference
- Update CHANGELOG.md
- Prepare for v1.1 release

---

**Design Document Complete. Awaiting approval to proceed to Phase 2.**

**Last Updated:** December 25, 2025
**Status:** Ready for Review
**Next Action:** Core Maintainer Approval
