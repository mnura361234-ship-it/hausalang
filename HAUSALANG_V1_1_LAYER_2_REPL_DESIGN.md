# Hausalang v1.1 Layer 2: Interactive REPL Design

**Phase**: Layer 2 (Developer Experience)
**Milestone**: Interactive REPL (Read-Eval-Print Loop)
**Status**: DESIGN PHASE (awaiting approval)
**Date**: December 2025

---

## 1. Executive Summary

This document specifies the design for **Hausalang Interactive REPL** — an interactive development environment for Hausalang that:

- **Leverages** the ContextualError system (Layer 1) for rich, actionable error diagnostics
- **Preserves** v1.0 core completely (zero modifications to lexer, parser, interpreter)
- **Maintains** backward compatibility (existing v1.0 code runs unchanged)
- **Delivers** interactive development experience with persistent state, history, and directives

**Design Principles**:
1. **No Core Changes**: REPL wraps v1.0, doesn't modify it
2. **Rich Diagnostics**: Every error includes location, context, help (via ContextualError)
3. **Persistent State**: Variables/functions survive across statements
4. **Fast Feedback**: < 100ms response time for most commands
5. **Graceful Degradation**: Errors in one command don't break session

---

## 2. Problem Statement

### Current User Experience (v1.0)
```bash
$ python main.py program.ha          # One-shot execution
# vs
$ hausa-repl                         # REPL doesn't exist
```

### Limitations
- No interactive development: Must write to file, then execute
- No state persistence: Each run is isolated
- Limited error context: Error messages lack diagnostic info
- No exploration: Can't inspect variables or function signatures
- No history: Can't recall previous commands

### Solution: Interactive REPL
Provide an interactive command loop where users can:
1. Execute statements incrementally (building state across commands)
2. Explore values and types
3. Load/test files in interactive context
4. Receive rich error diagnostics
5. Recall and edit previous commands

---

## 3. REPL Scope & Boundaries

### In Scope (Layer 2)
- Core REPL loop (read, parse, execute, print)
- Session state management (variables, functions)
- Multi-line statement handling
- Error recovery (errors don't crash REPL)
- Basic directives (:help, :clear, :exit, :reload)
- Input history (arrow keys, command recall)
- Integration with ContextualError for diagnostics

### Out of Scope (Future Layers)
- Debugger (breakpoints, step execution)
- IDE integration (LSP, hover, completion)
- Package manager (imports, modules)
- IDE-specific features (jupyter kernels, VS Code extension)

### Backward Compatibility
- ✅ v1.0 interpreter untouched
- ✅ v1.0 lexer untouched
- ✅ v1.0 parser untouched
- ✅ v1.0 main.py execution unchanged
- ✅ Existing .ha files run identically in REPL

---

## 4. Architecture & Design

### 4.1 System Components

```
┌─────────────────────────────────────────────────┐
│          Interactive REPL Main Loop             │
│  (repl.py: ReplSession, ReplCommand, etc.)     │
└────────────┬────────────────────────────────────┘
             │
    ┌────────┴────────┬────────────────┬────────────┐
    │                 │                │            │
    ▼                 ▼                ▼            ▼
┌─────────┐  ┌────────────────┐  ┌──────────┐  ┌──────────────┐
│ Session │  │ Input Handler  │  │Formatter │  │ Directive    │
│ State   │  │ (history, etc) │  │ (output) │  │ Processor    │
└─────────┘  └────────────────┘  └──────────┘  └──────────────┘
    │
    └─────────────────────────────┐
                                  │ (wraps, doesn't modify)
    ┌─────────────────────────────▼──────────────────┐
    │   v1.0 Core (Frozen)                           │
    │  ┌──────────┐ ┌────────┐ ┌──────────────┐     │
    │  │ Lexer    │ │ Parser │ │ Interpreter  │     │
    │  └──────────┘ └────────┘ └──────────────┘     │
    └─────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────┐
    │   Layer 1: ContextualError (Enhanced Errors)    │
    │  (Used by REPL for rich diagnostics)            │
    └─────────────────────────────────────────────────┘
```

### 4.2 Core Classes

#### ReplSession
Manages persistent session state across commands.

```python
class ReplSession:
    """
    Manages REPL session: variables, functions, history.

    Attributes:
        global_env: Interpreter Environment (persistent)
        history: List[str] of executed commands (for recall)
        interpreter: Interpreter instance (v1.0, wrapped)
        command_count: Number of commands executed
        metadata: Dict of session info (start_time, etc.)

    Methods:
        execute(statement: str) -> ExecutionResult
        get_variable(name: str) -> Any
        list_variables() -> List[Tuple[str, Any]]
        clear_state() -> None
        load_file(path: str) -> ExecutionResult
    """
```

#### InputHandler
Manages user input: reading, history, editing.

```python
class InputHandler:
    """
    Handles user input: reading lines, managing history, multi-line.

    Attributes:
        history: List[str] of all commands entered
        history_index: Current position in history
        readline_state: Object for readline configuration

    Methods:
        read_command(prompt: str) -> str
        read_multiline(initial_line: str) -> str
        get_history() -> List[str]
        save_history(file: str) -> None
        load_history(file: str) -> None
    """
```

#### ReplCommand
Represents a command entered in REPL (statement or directive).

```python
class ReplCommand:
    """
    Parsed REPL command (statement or directive).

    Attributes:
        raw_input: Original user input
        command_type: "statement" | "directive" | "empty" | "comment"
        content: Parsed content (statement or directive name)
        args: List of directive arguments
        line_number: Line in session history

    Methods:
        is_directive() -> bool
        is_multiline() -> bool
        get_directive_name() -> str
    """
```

#### ExecutionResult
Result of executing a command.

```python
class ExecutionResult:
    """
    Result of executing a command.

    Attributes:
        success: bool (True if no error)
        output: Any (value produced, or None)
        error: Optional[ContextualError] (if error)
        execution_time_ms: float
        statement_type: str ("assignment" | "expression" | "print" | etc)

    Methods:
        format_for_display(use_colors: bool) -> str
        is_error() -> bool
    """
```

### 4.3 REPL Directives

Special commands (not Hausalang statements) that control REPL behavior.

| Directive | Args | Purpose | Example |
|-----------|------|---------|---------|
| `:help` | `[topic]` | Show help (general or for topic) | `:help variables` |
| `:clear` | none | Clear all variables/functions | `:clear` |
| `:vars` | none | List all variables | `:vars` |
| `:funcs` | none | List all functions | `:funcs` |
| `:history` | `[N]` | Show last N commands (default 10) | `:history 20` |
| `:load` | `<file>` | Load .ha file into session | `:load program.ha` |
| `:save` | `<file>` | Save session history to file | `:save session.txt` |
| `:exit` / `:quit` | none | Exit REPL | `:exit` |
| `:reset` | none | Reset session to blank state | `:reset` |
| `:info` | `<name>` | Show variable/function details | `:info my_func` |
| `:time` | none | Toggle execution time display | `:time` |
| `:color` | none | Toggle colored output | `:color` |

### 4.4 Session State Management

#### Persistence Across Commands
```python
# User enters:
rubuta x = 5           # Creates variable x
y = x + 10             # Uses x from previous command
aiki double(n):        # Defines function
    mayar n * 2
result = double(y)     # Calls function defined earlier
```

#### Environment Isolation
- Each REPL session has its own `Interpreter.Environment`
- Variables and functions from one command available in next
- Errors don't clear state (can continue after error)

#### Session Boundaries
```python
# Same session:
Statement 1: x = 5     # ✅ x is available
Statement 2: y = x     # ✅ uses x from statement 1

# Different sessions:
repl1: x = 5
exit
repl2: y = x           # ❌ NameError (x doesn't exist in new session)
```

### 4.5 Input Handling

#### Single-Line Statements
```
hausa> x = 10
hausa> rubuta x
```

#### Multi-Line Statements
```
hausa> aiki add(a, b):
....>     mayar a + b
....>
hausa> add(3, 5)
```

**Detection Logic**:
- If line ends with `:` → expect indented block
- If blank line after indented block → statement complete
- Prompt changes to `....>` during multi-line input

#### Comments & Blank Lines
```
hausa> # This is a comment
hausa>
hausa> x = 5  # Inline comment
```

### 4.6 Error Handling & Recovery

#### Error Display (using ContextualError)
```
hausa> z = undefined_var + 5

❌ UNDEFINED_VARIABLE: Undefined variable: undefined_var @ <stdin>:1:4

   Diagnostic:
   - Line 1: z = undefined_var + 5
   - Error at column 4 (the variable name)

   Help: Assign a value before using the variable

   Session continues (x is still available):
hausa> rubuta x
5
```

#### Error Recovery
- Error in one command doesn't crash REPL
- Session state preserved (can continue)
- User can edit command history and re-execute

#### Error Context Frames (from Layer 1)
```
hausa> aiki foo():
....>     y = bar()
....>
hausa> foo()

❌ UNDEFINED_FUNCTION: Undefined function: bar @ <stdin>:2:8

   Context:
   - Called from function: foo
   - In function body (line 2)

   Help: Define the function with 'aiki' before calling it
```

---

## 5. User Experience

### 5.1 REPL Startup
```bash
$ python -m hausalang.repl
```

### 5.2 Welcome Message
```
╔════════════════════════════════════════╗
║   Hausalang Interactive REPL v1.1      ║
║   Type :help for commands              ║
╚════════════════════════════════════════╝

Session started: 2025-12-25 14:30:00
Type statements or directives (start with :)

hausa>
```

### 5.3 Example Session

```
hausa> # Define a function
hausa> aiki greet(name):
....>     msg = "Hello, " + name
....>     mayar msg
....>
hausa> # Use the function
hausa> result = greet("Ali")
hausa> rubuta result
Hello, Ali

hausa> # List variables
hausa> :vars
Variables in session:
  name (type: str) = "Ali"
  msg (type: str) = "Hello, Ali"
  result (type: str) = "Hello, Ali"

hausa> # Load a file
hausa> :load examples/arithmetic.ha
Loaded: examples/arithmetic.ha (3 statements)

hausa> # Show history
hausa> :history 5
  1: aiki greet(name):
  2:     msg = "Hello, " + name
  3:     mayar msg
  4: result = greet("Ali")
  5: rubuta result

hausa> :exit
Session saved. Goodbye!
```

### 5.4 Output Formatting

#### Values
```
hausa> x = 42
hausa> x
42

hausa> y = "hello"
hausa> y
"hello"

hausa> don i = 0 zuwa 3 ta 1:
....>     rubuta i
....>
0
1
2
```

#### Function Definitions
```
hausa> aiki add(a, b):
....>     mayar a + b
....>
Function 'add' defined (2 parameters)

hausa> add(3, 5)
8
```

#### No Output
```
hausa> x = 10        # Assignment produces no output
hausa> aiki foo():   # Function definition produces no output
....>     mayar 5
....>
```

---

## 6. Implementation Strategy

### Phase 1: Core REPL Loop
1. Create `repl.py` with ReplSession, InputHandler, ExecutionResult
2. Implement basic read-eval-print loop
3. No v1.0 modifications
4. ✅ Tests: 20+ tests for core loop

### Phase 2: Session State
1. Integrate v1.0 Interpreter's Environment
2. Variable/function persistence
3. State clearing/reset
4. ✅ Tests: 15+ tests for state management

### Phase 3: Directives & Input
1. Implement all directives (:help, :vars, :clear, etc.)
2. Multi-line statement detection
3. Command history (in-memory, file persistence)
4. ✅ Tests: 25+ tests for directives

### Phase 4: Error & Output Formatting
1. Integrate ContextualError for rich diagnostics
2. Format output (colored, with emoji)
3. Error recovery (session continues)
4. ✅ Tests: 20+ tests for error handling

### Phase 5: Polish & Optimization
1. Performance optimization (< 100ms per command)
2. Unicode support verification
3. Edge case handling
4. ✅ Tests: 10+ tests for edge cases

**Total Test Count**: ~90 tests across 5 test files

---

## 7. Technical Specifications

### 7.1 Dependencies
- **Python 3.8+** (for readline, type hints)
- **readline** module (for history, line editing) — stdlib
- **sys, os, time** — stdlib
- **core.interpreter** — v1.0 (existing, unchanged)
- **core.errors** — Layer 1 (existing, unchanged)
- **core.formatters** — Layer 1 (existing, unchanged)

### 7.2 File Structure
```
hausalang/
├── repl/                          # NEW
│   ├── __init__.py
│   ├── session.py                 # ReplSession class
│   ├── input_handler.py           # InputHandler class
│   ├── directives.py              # Directive processing
│   ├── formatter.py               # Output formatting
│   └── __main__.py                # Entry point (python -m hausalang.repl)
├── main.py                        # v1.0 entry (unchanged)
└── [rest unchanged]
```

### 7.3 Entry Point
```python
# repl/__main__.py
if __name__ == "__main__":
    from hausalang.repl.session import ReplSession
    session = ReplSession()
    session.run()  # Starts interactive loop
```

### 7.4 Command Line
```bash
python -m hausalang.repl              # Start interactive REPL
python -m hausalang.repl --no-color   # REPL without colors
python -m hausalang.repl < input.txt  # Non-interactive mode (pipe)
python main.py program.ha             # v1.0 unchanged
```

### 7.5 Session Configuration

**History File Location**: `~/.hausalang/history` (user home)

```python
history_file = os.path.expanduser("~/.hausalang/history")
max_history_size = 1000  # Keep last 1000 commands
```

---

## 8. Compatibility Matrix

### v1.0 Code in REPL
```python
# v1.0 code runs unchanged in REPL
code = """
aiki factorial(n):
    idan n <= 1:
        mayar 1
    mayar n * factorial(n - 1)

rubuta factorial(5)
"""

# In REPL, user enters statements one by one:
hausa> aiki factorial(n):
....>     idan n <= 1:
....>         mayar 1
....>     mayar n * factorial(n - 1)
....>
hausa> rubuta factorial(5)
120
```

### ContextualError Integration
```python
# REPL catches ContextualError (from Layer 1)
# and formats using ErrorFormatter.pretty()

try:
    result = interpreter.interpret(ast)
except ContextualError as e:
    output = format_pretty(e, use_colors=colors_enabled)
    print(output)
    # Session continues, no crash
```

---

## 9. Error Scenarios & Handling

### Scenario 1: Undefined Variable
```
hausa> x = undefined_var
❌ UNDEFINED_VARIABLE: Undefined variable: undefined_var @ <stdin>:1:4

Session continues:
hausa> x = 5          # User can define x
hausa> y = x          # Now x is available
5
```

### Scenario 2: Multi-line Error
```
hausa> aiki foo():
....>     return x   # Invalid keyword
....>
❌ UNKNOWN_STATEMENT_TYPE: Unknown statement: return @ <stdin>:2:4
```

### Scenario 3: Syntax Error (Missing Colon)
```
hausa> idan x = 5
❌ MISSING_COLON: Expected ":" after if condition @ <stdin>:1:7
```

### Scenario 4: Type Error
```
hausa> x = 5 + "hello"
❌ INVALID_OPERAND_TYPE: Can't add int and str @ <stdin>:1:8
```

### Scenario 5: Wrong Argument Count
```
hausa> aiki add(a, b):
....>     mayar a + b
....>
hausa> add(5)
❌ WRONG_ARGUMENT_COUNT: add() expects 2 arguments, got 1 @ <stdin>:2:0
```

---

## 10. Testing Strategy

### Test Categories

1. **Core Loop Tests** (20 tests)
   - REPL starts without error
   - Statements execute and produce output
   - Multi-line detection works
   - Empty lines handled
   - Comments ignored

2. **State Management Tests** (15 tests)
   - Variables persist across commands
   - Functions persist across commands
   - Variable reassignment works
   - Function redefinition works
   - State can be cleared

3. **Directive Tests** (25 tests)
   - `:vars` lists variables
   - `:funcs` lists functions
   - `:clear` clears state
   - `:history` shows commands
   - `:load` loads files
   - `:exit` exits cleanly
   - `:info` shows details

4. **Error Handling Tests** (20 tests)
   - Undefined variable caught
   - Syntax errors caught
   - Type errors caught
   - Wrong arg count caught
   - Errors don't crash REPL
   - Error messages include help

5. **Input Handling Tests** (10 tests)
   - Single-line input works
   - Multi-line detection
   - History recall
   - Comment handling
   - Unicode input

**Total**: ~90 tests across 5 files

### Test Example
```python
def test_variable_persistence():
    """Variables should persist across commands."""
    session = ReplSession()

    session.execute("x = 5")
    result = session.execute("y = x + 10")

    assert result.success
    assert session.get_variable("y") == 15
```

---

## 11. Success Criteria

### Code Quality
- ✅ Zero modifications to v1.0 core
- ✅ All 90+ tests pass
- ✅ No regressions on v1.0 tests
- ✅ Code coverage > 85%

### User Experience
- ✅ REPL starts in < 1 second
- ✅ Commands respond in < 100ms
- ✅ Error messages include helpful context
- ✅ History works (arrow keys, recall)

### Compatibility
- ✅ All v1.0 code runs unchanged
- ✅ ContextualError integration complete
- ✅ Backward compatibility guaranteed
- ✅ Works on Windows, Mac, Linux

### Documentation
- ✅ This design document (approved)
- ✅ Implementation checklist (per phase)
- ✅ Test completion report (90+ tests)
- ✅ User guide for REPL usage

---

## 12. Design Decisions & Rationale

### Decision 1: No v1.0 Core Modifications
**Why**: Guarantees backward compatibility, reduces risk, enables layered development

### Decision 2: Persistent Environment per Session
**Why**: Enables interactive development, allows function/variable reuse, matches user expectations (like Python REPL)

### Decision 3: Directives (`:command` syntax)
**Why**: Distinguishes from Hausalang statements, easy to parse, standard in many REPLs (Python, Ruby)

### Decision 4: Integration with ContextualError
**Why**: Provides rich diagnostics (line, column, context, help) without extra code; leverages Layer 1

### Decision 5: History File Persistence
**Why**: Users expect to recall commands across REPL sessions; improves UX

---

## 13. Constraints & Assumptions

### Constraints
- Python 3.8+ required (for type hints, datetime)
- readline not available on all platforms → graceful degradation
- Max history size = 1000 (configurable)
- REPL session limited by available memory
- No network/file system sandboxing

### Assumptions
- Users will run REPL from command line
- Session files written to ~/.hausalang/
- Colored output supported on modern terminals
- Unicode supported (Python 3 defaults)

---

## 14. Open Questions for Review

1. **Multi-file Sessions**: Should `:load` append to session or replace state?
   - Option A: Append (additive) — preferred
   - Option B: Replace (reset + load)

2. **History Limit**: Keep last 1000 commands or different value?
   - Proposed: 1000 (balances memory vs. usefulness)

3. **Output Format**: Show expression results or only explicit print?
   - Proposed: Show all expression results (like Python REPL)

4. **Color Support**: Auto-detect terminal colors or always enable?
   - Proposed: Auto-detect, with --no-color flag to override

5. **Error Recovery**: Continue session after parse error or show only?
   - Proposed: Continue (allows recovery and correction)

---

## 15. Conclusion

This design provides a **complete specification** for Hausalang Interactive REPL that:

1. ✅ Maintains **zero modifications to v1.0** (lexer, parser, interpreter)
2. ✅ Guarantees **backward compatibility** (v1.0 code runs unchanged)
3. ✅ Leverages **ContextualError system** (Layer 1) for rich diagnostics
4. ✅ Provides **interactive development experience** (state persistence, history, directives)
5. ✅ Includes **comprehensive test strategy** (90+ tests across 5 categories)

**Ready for approval before implementation begins.**

---

## Appendix A: Example Interactions

### Example 1: Function Development
```
hausa> aiki greet(name):
....>     msg = "Sannu, " + name
....>     mayar msg
....>
hausa> greet("Nura")
Sannu, Nura

hausa> :vars
name (str) = "Nura"
msg (str) = "Sannu, Nura"
```

### Example 2: Error Recovery
```
hausa> x = 5 + undefined
❌ UNDEFINED_VARIABLE: Undefined variable: undefined

hausa> undefined = 10
hausa> x = 5 + undefined
hausa> rubuta x
15
```

### Example 3: File Loading
```
hausa> :load examples/arithmetic.ha
Loaded 5 statements

hausa> result = add(3, 4)
hausa> rubuta result
7
```

---

**Design Status**: PENDING APPROVAL
**Next Step**: User review and approval before Phase 1 implementation
**Estimated Implementation Time**: 2-3 weeks (5 phases, 90+ tests)
