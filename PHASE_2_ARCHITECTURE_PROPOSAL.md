```
═══════════════════════════════════════════════════════════════════════════════
                    HAUSALANG PHASE 2 ARCHITECTURE PROPOSAL
                   Senior Language Architect & Product Engineering
                              December 25, 2025
═══════════════════════════════════════════════════════════════════════════════

PHASE 2 MISSION STATEMENT
─────────────────────────

Transform Hausalang from a "proof-of-concept language engine" into a
"publicly-ready programming language with professional tooling and community
capability."

Success metrics:
  • Production-grade error messages and debugging
  • Educational value (clear learning path for users)
  • Professional tooling (CLI, REPL, package structure)
  • Clear public roadmap (v1.1 → v1.2 → v2.0)
  • Sustainable development process

═══════════════════════════════════════════════════════════════════════════════
SECTION 1: CURRENT STATE (v1.0 BASELINE)
═══════════════════════════════════════════════════════════════════════════════

v1.0 Strengths (LOCKED - DO NOT CHANGE):
  ✅ Core interpreter: 100% stable
  ✅ All basic features working: variables, arithmetic, control flow, functions
  ✅ All tests passing: 100% feature coverage
  ✅ Architecture documented: Lexer → Parser → Interpreter
  ✅ Zero breaking changes allowed

v1.0 Limitations (ADDRESS IN PHASE 2):
  ❌ No REPL (interactive mode)
  ❌ Error messages lack context (no stack traces)
  ❌ No package/module system
  ❌ Limited built-in functions
  ❌ No debugging support
  ❌ Single-file execution only
  ❌ No IDE support (syntax highlighting, linting)
  ❌ No standard library
  ❌ Limited data structures (numbers, strings only)
  ❌ No Unicode/internationalization support

═══════════════════════════════════════════════════════════════════════════════
SECTION 2: PHASE 2 ARCHITECTURE VISION
═══════════════════════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────────────────┐
│ LAYERED EXPANSION STRATEGY                                             │
└────────────────────────────────────────────────────────────────────────┘

The key to Phase 2 is "ADDITIVE EXPANSION" - each new feature is added as a
layer on top of v1.0, without modifying the core interpreter.

Architecture Layers (Bottom → Top):

  LAYER 0 (FROZEN):
  ┌─────────────────────────────────┐
  │  v1.0 Core Interpreter          │
  │  (Lexer → Parser → Interpreter) │
  │  DO NOT MODIFY                  │
  └─────────────────────────────────┘
           ▲
           │
  LAYER 1 (Phase 2.1 - USABILITY):
  ┌─────────────────────────────────┐
  │  Enhanced Error Handling         │
  │  Stack Traces                   │
  │  Better Error Messages          │
  │  Line Number Tracking           │
  └─────────────────────────────────┘
           ▲
           │
  LAYER 2 (Phase 2.2 - DEVELOPER EXPERIENCE):
  ┌─────────────────────────────────┐
  │  REPL (Interactive Mode)         │
  │  CLI Tooling (run, repl, format) │
  │  Debugging Support              │
  │  Color Output                   │
  └─────────────────────────────────┘
           ▲
           │
  LAYER 3 (Phase 2.3 - DATA & LIBS):
  ┌─────────────────────────────────┐
  │  List Data Type                 │
  │  Dictionary Data Type           │
  │  Built-in Functions (stdlib)    │
  │  String Methods                 │
  └─────────────────────────────────┘
           ▲
           │
  LAYER 4 (Phase 2.4 - ADVANCED):
  ┌─────────────────────────────────┐
  │  Module System                  │
  │  Package Management             │
  │  Documentation Generation       │
  │  Performance Profiling          │
  └─────────────────────────────────┘
           ▲
           │
  LAYER 5 (v2.0 - NEXT GENERATION):
  ┌─────────────────────────────────┐
  │  Type System (Optional)         │
  │  Exception Handling (try/catch) │
  │  Classes & Objects              │
  │  Async/Await                    │
  └─────────────────────────────────┘

Backward Compatibility Guarantee:
  Every Layer preserves all v1.0 behavior.
  v1.0 programs run identically in v1.1, v1.2, v2.0.

═══════════════════════════════════════════════════════════════════════════════
SECTION 3: FEATURE ROADMAP (v1.1 → v1.2 → v2.0)
═══════════════════════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────────────────┐
│ v1.1 ROADMAP (1-2 months) - USABILITY FOUNDATION                       │
│ Focus: Making errors understandable, improving developer experience    │
└────────────────────────────────────────────────────────────────────────┘

v1.1 Features (Release as single integrated package):

  1. ENHANCED ERROR REPORTING
     ────────────────────────
     Current: One-line error messages
     Upgrade: Full context with code snippets

     Before:
       SyntaxError: Line 5, Column 10: Unexpected token: OPERATOR(:)

     After:
       Error at line 5, column 10:
         5 │  idan x > 5:
           │          ^ expected expression here

       Unexpected token: OPERATOR(:)
       Expected: expression or statement

     Implementation:
       • Enhance lexer with better error context
       • Parser errors show code snippet + arrow
       • Interpreter errors show call stack

  2. STACK TRACES FOR DEBUGGING
     ──────────────────────────
     Current: Silent failures (variable not found, type mismatch)
     Upgrade: Full call stack showing where error occurred

     Example output:
       NameError: Undefined variable 'x'

       Traceback (most recent call last):
         File "factorial.ha", line 15
           result = result * x     <-- undefined variable
         Called from function 'calculate_factorial' (line 8)
         Called from main (line 20)

     Implementation:
       • Add call stack tracking to Interpreter
       • Store current function context
       • Print full trace on error

  3. LINE NUMBER PRESERVATION
     ───────────────────────
     Current: Line numbers lost after parsing
     Upgrade: Preserve line info through execution

     Implementation:
       • Already in AST nodes (line, column fields)
       • Use during runtime error reporting
       • No parser changes needed

  4. IMPROVED REPL (Read-Eval-Print Loop)
     ───────────────────────────────────
     New: Interactive interpreter mode

     Features:
       • hausa> (interactive prompt)
       • Line-by-line execution
       • Variable persistence
       • History support
       • Colors in output

     Implementation:
       • New module: tools/repl.py
       • Uses existing interpreter
       • Wraps interpret_program() for line input
       • No core changes needed

  5. CLI IMPROVEMENTS
     ────────────────
     Current: python main.py file.ha
     Upgrade: hausa run|repl|check|format

     Implementation:
       • New main entry point: hausa (console script)
       • Subcommands: run, repl, check, format
       • Uses existing interpreter
       • Optional arguments (colors, quiet mode, etc.)

v1.1 Estimated Effort: 3-4 weeks
v1.1 Risk Level: LOW (all additive, no core changes)
v1.1 Release Date: Mid-January 2026


┌────────────────────────────────────────────────────────────────────────┐
│ v1.2 ROADMAP (2-3 months) - DATA STRUCTURES & STDLIB                   │
│ Focus: Making programs more powerful with better data types            │
└────────────────────────────────────────────────────────────────────────┘

v1.2 Features (Staged release, each feature independent):

  1. LIST DATA TYPE (Phase 2.3.1)
     ────────────────────────────
     Syntax: [1, 2, 3, 4]
     Operations: indexing, length, append

     Grammar:
       list_literal = "[" expression ("," expression)* "]"
       index_expr = identifier "[" expression "]"

     Implementation:
       • Add List AST node
       • Add Indexing AST node
       • Extend eval_expression() for lists
       • Built-in len() function
       • List append/insert methods

     Example:
       numbers = [1, 2, 3, 4, 5]
       rubuta numbers[0]         # Prints 1
       rubuta len(numbers)        # Prints 5

  2. DICTIONARY DATA TYPE (Phase 2.3.2)
     ──────────────────────────────────
     Syntax: {"key": value, "name": "Nura"}
     Operations: access, set, iteration

     Grammar:
       dict_literal = "{" (string ":" expression ("," string ":" expression)*)? "}"
       dict_access = identifier "[" string "]"

     Implementation:
       • Add Dict AST node
       • Python dict backend
       • Key-value access
       • Optional iteration (for-each when ready)

     Example:
       person = {"name": "Nura", "age": 25}
       rubuta person["name"]     # Prints Nura

  3. BUILT-IN FUNCTIONS (Phase 2.3.3)
     ────────────────────────────────
     Functions: len(), range(), int(), str(), type(), etc.

     Signatures:
       len(list_or_string) → int
       range(end) → list
       range(start, end, step) → list
       int(string) → int
       str(number) → string
       type(value) → string
       max(list) → value
       min(list) → value
       sum(list) → number

     Implementation:
       • New module: stdlib/builtins.py
       • Extend eval_function_call() to check builtins
       • Pure Python implementations
       • No interpreter changes needed

     Example:
       don i in range(1, 5):
         rubuta i

  4. STRING METHODS (Phase 2.3.4)
     ───────────────────────────
     Methods: upper(), lower(), length(), split(), join()

     Syntax: string.method()

     Implementation:
       • Add MethodCall AST node
       • Extend parser to recognize dot notation
       • Dispatch to string method handlers

     Example:
       message = "hello world"
       rubuta message.upper()     # HELLO WORLD
       rubuta message.length()    # 11

  5. FOR-EACH LOOPS (Phase 2.3.5)
     ────────────────────────────
     Syntax: don item in list: body

     Implementation:
       • New ForEach AST node
       • Transform to while + indexing
       • Requires lists (Phase 2.3.1)

     Example:
       don x in [1, 2, 3]:
         rubuta x * 2

v1.2 Estimated Effort: 4-5 weeks (can be split into patches)
v1.2 Risk Level: MEDIUM (new AST nodes, but isolated)
v1.2 Release Strategy: v1.2.0 (lists), v1.2.1 (dicts), v1.2.2 (stdlib), etc.
v1.2 Release Date: March 2026


┌────────────────────────────────────────────────────────────────────────┐
│ v2.0 ROADMAP (3+ months) - NEXT GENERATION                             │
│ Focus: Professional features, ecosystem development                    │
└────────────────────────────────────────────────────────────────────────┘

v2.0 Vision (High-level, detailed planning in future):

  1. MODULE SYSTEM
     ────────────
     • import "other_file.ha" as other
     • other.function_name()
     • Module namespacing
     • File loading & caching

  2. EXCEPTION HANDLING
     ──────────────────
     • try { code } catch { handler }
     • Custom exceptions
     • Error propagation

  3. OPTIONAL TYPE SYSTEM
     ──────────────────────
     • Type hints (optional, no enforcement)
     • Type checking tool (optional)
     • Type hints in docs

  4. PACKAGE MANAGER
     ────────────────
     • hausa install <package>
     • Package registry
     • Dependency resolution
     • Version management

  5. STANDARD LIBRARY EXPANSION
     ──────────────────────────
     • File I/O (read, write)
     • JSON support
     • Math library
     • String utilities

v2.0 Estimated Timeline: 4-6 months of planning + 6-8 months implementation
v2.0 Release Date: Late 2026 or early 2027


Versioning Strategy:

  v1.0.0 - Initial stable release (locked)
  v1.1.0 - Error reporting & CLI improvements
  v1.2.0 - Lists data type
  v1.2.1 - Dictionaries
  v1.2.2 - Built-in functions
  v1.2.3 - String methods & for-each
  v2.0.0 - Modules, exceptions, type system

Semantic Versioning:
  MAJOR.MINOR.PATCH
  • MAJOR: Breaking changes (v1→v2)
  • MINOR: New features (v1.0→v1.1)
  • PATCH: Bug fixes, enhancements (v1.2.0→v1.2.1)

═══════════════════════════════════════════════════════════════════════════════
SECTION 4: FIRST PHASE 2 FEATURE - PRIORITY ANALYSIS
═══════════════════════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────────────────┐
│ FEATURE SELECTION CRITERIA                                             │
└────────────────────────────────────────────────────────────────────────┘

Evaluation Factors:
  1. User Impact: How much does this improve user experience?
  2. Implementation Complexity: How hard is it to build?
  3. Dependencies: What other features does it depend on?
  4. Backward Compatibility: Does it break v1.0 programs?
  5. Test Coverage: Can we write comprehensive tests?
  6. Documentation: How easy is it to document?
  7. Reusability: Will future features build on this?

┌────────────────────────────────────────────────────────────────────────┐
│ CANDIDATE FEATURES FOR FIRST v1.1 IMPLEMENTATION                       │
└────────────────────────────────────────────────────────────────────────┘

Candidate 1: IMPROVED ERROR MESSAGES & STACK TRACES
  ────────────────────────────────────────────────
  User Impact:      ⭐⭐⭐⭐⭐ (Everyone encounters errors)
  Implementation:   ⭐⭐⭐⭐   (Medium complexity)
  Dependencies:     ⭐⭐⭐⭐⭐ (None - pure enhancement)
  Compatibility:    ⭐⭐⭐⭐⭐ (100% backward compatible)
  Test Coverage:    ⭐⭐⭐⭐   (Easy to test output)
  Documentation:    ⭐⭐⭐⭐⭐ (Self-explanatory)
  Reusability:      ⭐⭐⭐⭐   (Basis for debugging)

  SCORE: 9.4/10 ✅ BEST CHOICE FOR FIRST FEATURE

Candidate 2: INTERACTIVE REPL
  ──────────────────────────
  User Impact:      ⭐⭐⭐⭐   (Nice for learning)
  Implementation:   ⭐⭐⭐⭐⭐ (Very simple)
  Dependencies:     ⭐⭐⭐⭐⭐ (None)
  Compatibility:    ⭐⭐⭐⭐⭐ (100% compatible)
  Test Coverage:    ⭐⭐⭐    (Hard to automate)
  Documentation:    ⭐⭐⭐⭐   (Easy to explain)
  Reusability:      ⭐⭐⭐    (Limited)

  SCORE: 8.7/10 (Good, but less impactful)

Candidate 3: CLI IMPROVEMENTS
  ────────────────────────────
  User Impact:      ⭐⭐⭐⭐   (Better UX)
  Implementation:   ⭐⭐⭐⭐⭐ (Very simple)
  Dependencies:     ⭐⭐⭐⭐⭐ (None)
  Compatibility:    ⭐⭐⭐⭐⭐ (100% compatible)
  Test Coverage:    ⭐⭐⭐⭐   (Easy)
  Documentation:    ⭐⭐⭐⭐⭐ (Self-explanatory)
  Reusability:      ⭐⭐⭐    (Limited)

  SCORE: 8.5/10 (Good but lower priority)

Candidate 4: LIST DATA TYPE
  ──────────────────────────
  User Impact:      ⭐⭐⭐⭐⭐ (Needed for real programs)
  Implementation:   ⭐⭐⭐    (Higher complexity)
  Dependencies:     ⭐⭐⭐    (Other features depend on this)
  Compatibility:    ⭐⭐⭐⭐⭐ (100% compatible)
  Test Coverage:    ⭐⭐⭐⭐⭐ (Very testable)
  Documentation:    ⭐⭐⭐⭐   (Straightforward)
  Reusability:      ⭐⭐⭐⭐⭐ (Blocks many features)

  SCORE: 8.9/10 (High priority, but higher complexity)

┌────────────────────────────────────────────────────────────────────────┐
│ DECISION: FIRST IMPLEMENTATION - ERROR REPORTING v1.1                  │
└────────────────────────────────────────────────────────────────────────┘

CHOSEN FEATURE: Enhanced Error Messages & Stack Traces

Rationale:
  1. ✅ Highest user impact (every developer faces errors)
  2. ✅ Medium complexity (manageable implementation)
  3. ✅ Zero dependencies (no other features needed)
  4. ✅ 100% backward compatible (purely additive)
  5. ✅ Establishes foundation for debugging tools
  6. ✅ Makes language more professional and accessible
  7. ✅ Can be released independently as v1.1.0
  8. ✅ Improves educational value significantly

Secondary Features (v1.1 as cohesive release):
  • Interactive REPL
  • CLI tooling improvements
  • Color output

These pair well with error reporting and form a complete v1.1 usability package.

═══════════════════════════════════════════════════════════════════════════════
SECTION 5: DETAILED IMPLEMENTATION PLAN - ENHANCED ERROR REPORTING v1.1
═══════════════════════════════════════════════════════════════════════════════

FEATURE SPECIFICATION: Enhanced Error Messages with Stack Traces

┌────────────────────────────────────────────────────────────────────────┐
│ GOAL                                                                    │
└────────────────────────────────────────────────────────────────────────┘

Transform error messages from:
  SyntaxError: Line 5, Column 10: Unexpected token: OPERATOR(:)

Into:
  SyntaxError: Unexpected token ':'

  File "program.ha", line 5:
     5 │  idan x > 5:
       │           ^ unexpected token ':' here

  Expected: colon after 'if' condition (but this was unexpected)

And provide full call stacks for runtime errors:
  NameError: Undefined variable: x

  Traceback (most recent call last):
    File "program.ha", line 15, in <module>
      result = result * x
    File "program.ha", line 8, in function "calculate"
      return x + y

  Variable 'x' not defined in any accessible scope

┌────────────────────────────────────────────────────────────────────────┐
│ DESIGN COMPONENTS                                                      │
└────────────────────────────────────────────────────────────────────────┘

1. ERROR REPORTER CLASS (NEW)
   ─────────────────────────
   Location: core/error_reporter.py

   Class: ErrorReporter
     • Formats error messages with code context
     • Shows line numbers and column markers
     • Provides suggestions for common errors
     • Colorizes output (optional)

   Methods:
     • report_syntax_error(message, token, source_lines)
     • report_runtime_error(error_type, message, context)
     • format_code_context(line_num, source_lines, column)
     • add_suggestion(error_type, hint)

   Example use:
     reporter = ErrorReporter(filename="program.ha")
     reporter.report_syntax_error(
       message="Unexpected token",
       token=token_obj,
       source_lines=source.split('\n')
     )

2. CALL STACK TRACKING (EXTEND INTERPRETER)
   ─────────────────────────────────────────
   Location: core/interpreter.py (extend existing)

   New feature: execution_stack
     • Track current function name
     • Track current line number
     • Track call depth

   Methods added:
     • push_frame(function_name, line_number)
     • pop_frame()
     • get_call_stack() → List[StackFrame]

   StackFrame dataclass:
     • function_name: str
     • filename: str
     • line_number: int
     • source_line: str

3. ENHANCED EXCEPTIONS (NEW)
   ──────────────────────────
   Location: core/exceptions.py (new module)

   Exception classes:
     • HausalangError (base)
     • HausalangSyntaxError (SyntaxError with context)
     • HausalangRuntimeError (RuntimeError with stack)
     • HausalangNameError (NameError with suggestions)
     • HausalangTypeError (TypeError with type info)

   Features:
     • Store line/column info
     • Store source context
     • Store execution stack
     • Format readable error messages
     • Suggest fixes

4. LINE NUMBER PROPAGATION (EXTEND PARSER)
   ──────────────────────────────────────
   Current: AST nodes have line/column (already in parser)
   Needed: Ensure all nodes preserve location

   Verification:
     • Every AST node constructor includes line, column
     • No AST node construction strips location
     • Parser always captures token location

   No code changes needed - already implemented! ✓

5. SOURCE CODE CACHING (NEW)
   ─────────────────────────
   Location: core/interpreter.py

   Feature: Store source lines with interpreter
     • Load source file at start
     • Keep source lines in memory
     • Pass to error reporter
     • Show in error messages

   Methods:
     • set_source(filename, source_code)
     • get_source_line(line_num) → str
     • get_code_context(line_num, context_lines=2) → str

┌────────────────────────────────────────────────────────────────────────┐
│ STEP-BY-STEP IMPLEMENTATION PLAN                                       │
└────────────────────────────────────────────────────────────────────────┘

PHASE 1: Foundation (Week 1)
────────────────────────────

Step 1.1: Create Error Reporting Module
  Location: core/error_reporter.py

  Tasks:
    [ ] Create ErrorReporter class
    [ ] Implement format_code_snippet(line, column, source_lines)
    [ ] Implement format_syntax_error(message, token)
    [ ] Implement format_runtime_error(message, stack)
    [ ] Add color support (optional)

  Test Requirements:
    [ ] test_error_reporter.py
    [ ] Test each error type formatting
    [ ] Test with missing source lines
    [ ] Test with very long lines
    [ ] Test color output toggle

  Estimated Time: 1.5 days
  Complexity: LOW
  Risk: VERY LOW (isolated module)

Step 1.2: Create Exception Classes
  Location: core/exceptions.py

  Tasks:
    [ ] Define HausalangError base class
    [ ] Define HausalangSyntaxError
    [ ] Define HausalangRuntimeError
    [ ] Define HausalangNameError
    [ ] Define HausalangTypeError
    [ ] Add __str__() for nice formatting

  Test Requirements:
    [ ] test_exceptions.py
    [ ] Test exception creation
    [ ] Test exception attributes
    [ ] Test exception message formatting

  Estimated Time: 1 day
  Complexity: LOW
  Risk: VERY LOW (simple data classes)

Step 1.3: Extend Interpreter with Call Stack
  Location: core/interpreter.py (extend existing)

  Tasks:
    [ ] Add StackFrame dataclass
    [ ] Add execution_stack: List[StackFrame] to Interpreter
    [ ] Add push_frame(name, line) method
    [ ] Add pop_frame() method
    [ ] Add get_call_stack() method
    [ ] Modify execute_function_call() to push/pop frames
    [ ] Modify execute_program() to track line numbers

  Test Requirements:
    [ ] test_call_stack.py
    [ ] Test frame pushing/popping
    [ ] Test nested function calls
    [ ] Test recursion stack tracking

  Estimated Time: 1.5 days
  Complexity: MEDIUM
  Risk: MEDIUM (modifies existing code, but isolated)

PHASE 2: Integration (Week 1-2)
───────────────────────────────

Step 2.1: Enhance Parser Error Handling
  Location: core/parser.py (extend existing)

  Current: Raises SyntaxError(message)
  New: Raise HausalangSyntaxError(message, token, source)

  Tasks:
    [ ] Import HausalangSyntaxError
    [ ] Modify _error() to use new exception
    [ ] Pass token and source to exception
    [ ] Update all parser._error() calls
    [ ] Ensure backward compatibility (still SyntaxError subclass)

  Test Requirements:
    [ ] Verify all existing tests still pass
    [ ] test_parser_errors.py
    [ ] Test error message formatting
    [ ] Test with various syntax errors

  Estimated Time: 1 day
  Complexity: MEDIUM
  Risk: MEDIUM (many callsites, but localized)

Step 2.2: Enhance Interpreter Error Handling
  Location: core/interpreter.py

  Tasks:
    [ ] Import HausalangRuntimeError, etc.
    [ ] Update NameError raises → HausalangNameError
    [ ] Update TypeError raises → HausalangTypeError
    [ ] Update ZeroDivisionError → HausalangRuntimeError
    [ ] Add stack trace to all errors
    [ ] Pass source code context

  Test Requirements:
    [ ] test_interpreter_errors.py
    [ ] Test undefined variable error
    [ ] Test type mismatch error
    [ ] Test division by zero error
    [ ] Test nested function errors

  Estimated Time: 1.5 days
  Complexity: MEDIUM
  Risk: MEDIUM

Step 2.3: Source Code Caching
  Location: core/interpreter.py

  Tasks:
    [ ] Add source_lines: List[str] field to Interpreter
    [ ] Add set_source(filename, code) method
    [ ] Update interpret() to call set_source()
    [ ] Update error reporting to use cached source
    [ ] Handle missing source gracefully

  Test Requirements:
    [ ] Test source caching
    [ ] Test with multi-line programs
    [ ] Test with files
    [ ] Test error display with source

  Estimated Time: 1 day
  Complexity: LOW
  Risk: LOW

PHASE 3: Testing & Refinement (Week 2)
───────────────────────────────────────

Step 3.1: Comprehensive Error Testing
  Location: tests/test_error_messages.py (new)

  Test Cases:
    [ ] Syntax errors (missing colon, wrong operator, etc.)
    [ ] Undefined variable errors
    [ ] Type mismatch errors
    [ ] Function not found errors
    [ ] Division by zero errors
    [ ] Deep recursion errors
    [ ] Nested function errors with full stack trace
    [ ] Error message formatting
    [ ] Color output toggle
    [ ] Unicode in error messages

  Estimated Time: 2 days
  Complexity: MEDIUM
  Risk: LOW (tests don't affect code)

Step 3.2: Regression Testing
  Location: Run all existing tests

  Tasks:
    [ ] Run test_interpreter.py → must pass
    [ ] Run test_parser.py → must pass
    [ ] Run test_while_loops.py → must pass
    [ ] Run test_for_loops.py → must pass
    [ ] Run examples/ tests → must pass
    [ ] Run master_test.ha → must pass
    [ ] Verify no behavior changes

  Estimated Time: 1 day
  Risk: LOW (should pass, but critical checkpoint)

Step 3.3: Documentation
  Location: docs/error_messages.md (new)

  Content:
    [ ] Guide: Understanding Error Messages
    [ ] Examples: Common errors and fixes
    [ ] Reference: All error types
    [ ] Tips: Debugging strategies

  Estimated Time: 1 day

PHASE 4: Release Preparation (Week 2-3)
────────────────────────────────────────

Step 4.1: Version Bumping
  Tasks:
    [ ] Update version in __init__.py → 1.1.0
    [ ] Update README.md with new features
    [ ] Update CHANGELOG.md
    [ ] Tag commit with v1.1.0

  Estimated Time: 0.5 day

Step 4.2: Release Notes
  Tasks:
    [ ] Write feature description
    [ ] List all improvements
    [ ] Include examples
    [ ] Explain upgrade path

  Estimated Time: 0.5 day

Step 4.3: Performance Verification
  Tasks:
    [ ] Ensure no significant slowdown
    [ ] Test with large programs
    [ ] Profile error reporting overhead

  Estimated Time: 0.5 day

┌────────────────────────────────────────────────────────────────────────┐
│ FILE STRUCTURE (NEW FILES & MODIFICATIONS)                             │
└────────────────────────────────────────────────────────────────────────┘

New Files:
  core/
    error_reporter.py      (Error formatting & display)
    exceptions.py          (Custom exception classes)

  tests/
    test_error_reporter.py (Error reporting tests)
    test_exceptions.py     (Exception tests)
    test_call_stack.py     (Stack tracking tests)
    test_error_messages.py (Integration error tests)

  docs/
    error_messages.md      (User guide)

Modified Files (MINIMAL CHANGES):
  core/interpreter.py
    • Add StackFrame class
    • Add execution_stack management (≈40 lines)
    • Enhance error reporting (≈30 lines)
    • No behavior changes

  core/parser.py
    • Update exception types (≈10 lines)
    • No behavior changes

  main.py
    • Handle new exception types (≈5 lines)
    • No behavior changes

Untouched (FROZEN):
  core/lexer.py          ✓ FROZEN
  core/parser.py         ✓ Structure FROZEN (only exception type)
  core/interpreter.py    ✓ Behavior FROZEN (only error reporting)
  examples/             ✓ FROZEN
  tests/                ✓ All existing tests FROZEN

┌────────────────────────────────────────────────────────────────────────┐
│ BACKWARD COMPATIBILITY VERIFICATION                                    │
└────────────────────────────────────────────────────────────────────────┘

Compatibility Checklist:
  ✅ All v1.0 programs execute identically
  ✅ All v1.0 tests pass without modification
  ✅ Same input → same output guarantee
  ✅ No API changes to public functions
  ✅ No changes to AST structure
  ✅ No changes to parsing rules
  ✅ No changes to execution semantics
  ✅ Errors are still exceptions (but better formatted)
  ✅ REPL mode is optional (not required)
  ✅ CLI is backward compatible (old style still works)

Risk Mitigation:
  • Create feature branch: git checkout -b feature/error-reporting
  • All changes tested before merge
  • Master test suite baseline recorded
  • Any behavior change requires investigation
  • If any test fails: rollback and debug

═══════════════════════════════════════════════════════════════════════════════
SECTION 6: SUCCESS CRITERIA & ACCEPTANCE
═══════════════════════════════════════════════════════════════════════════════

v1.1 Release Success Criteria:

Technical Criteria:
  ✅ All existing tests pass (100%)
  ✅ Master test still produces identical output
  ✅ New error tests pass (100%)
  ✅ No performance regression (< 5% slowdown)
  ✅ Stack trace displays correctly for 5+ levels
  ✅ Error messages include code snippets
  ✅ All error types covered (syntax, runtime, etc.)

Documentation Criteria:
  ✅ Error message user guide written
  ✅ Examples of common errors documented
  ✅ Migration guide for v1.0 → v1.1
  ✅ Architecture updated with error handling

Release Criteria:
  ✅ Version bumped to 1.1.0
  ✅ CHANGELOG updated
  ✅ Release notes written
  ✅ Git tagged with v1.1.0
  ✅ README updated

User Experience:
  ✅ Error messages are more helpful than before
  ✅ Users can understand and fix errors faster
  ✅ Stack traces help with debugging
  ✅ Output is clear and professional

═══════════════════════════════════════════════════════════════════════════════
SUMMARY
═══════════════════════════════════════════════════════════════════════════════

Phase 2 Strategy:
  1. Layered expansion (additive only)
  2. Clear versioning roadmap (v1.1 → v1.2 → v2.0)
  3. Staged feature releases (not monolithic)
  4. 100% backward compatibility guarantee

First Implementation Feature: Enhanced Error Reporting v1.1
  • User Impact: Very High (affects all developers)
  • Complexity: Medium (manageable scope)
  • Risk: Low (isolated changes)
  • Timeline: 2-3 weeks
  • Dependencies: None
  • Deliverables: Better errors, stack traces, REPL, CLI

Next Steps:
  1. ✅ Phase 2 Architecture Proposal (THIS DOCUMENT)
  2. ⏳ Feature Roadmap (visions for v1.1, v1.2, v2.0)
  3. ⏳ Detailed Implementation Plan for v1.1 Error Reporting
  4. ⏳ Create Feature Branch
  5. ⏳ Implement Error Reporter Module
  6. ⏳ Enhance Exception Classes
  7. ⏳ Extend Interpreter with Call Stacks
  8. ⏳ Integration Testing
  9. ⏳ Documentation
  10. ⏳ Merge & Release v1.1.0

═══════════════════════════════════════════════════════════════════════════════
```
