"""
FOR LOOP IMPLEMENTATION - COMPLETE SYSTEM EXPLANATION

This document explains how for loops work in Hausalang, focusing on the
AST rewriting strategy that transforms for loops into assignment + while loops.

============================================================================
OVERVIEW
============================================================================

For loops in Hausalang use a **compiler transformation** approach:

Input Code (For Loop):
    don i = 0 zuwa 10:
        rubuta i

Internal Transformation (Rewrite to Assignment + While):
    i = 0
    kadai i < 10:
        rubuta i
        i = i + 1

This means:
- No separate while-loop-like execution needed
- Reuses proven while loop implementation
- Simpler, more maintainable code
- Natural integration with existing system


============================================================================
SYNTAX AND SEMANTICS
============================================================================

ASCENDING LOOP (zuwa):
    don i = start zuwa end:
        body

    Rewritten as:
        i = start
        kadai i < end:
            body
            i = i + 1

Example: don i = 0 zuwa 5:
    Executes with i = 0, 1, 2, 3, 4
    (Does NOT execute with i = 5)

DESCENDING LOOP (ba):
    don i = start ba end:
        body

    Rewritten as:
        i = start
        kadai i > end:
            body
            i = i - 1

Example: don i = 5 ba 0:
    Executes with i = 5, 4, 3, 2, 1
    (Does NOT execute with i = 0)

WITH CUSTOM STEP (ta):
    don i = start zuwa end ta step:
        body

    Rewritten as:
        i = start
        kadai i < end:
            body
            i = i + step

Example: don i = 0 zuwa 10 ta 2:
    Executes with i = 0, 2, 4, 6, 8
    Step must be positive (automatically applied correctly based on direction)


============================================================================
PHASE 1: LEXICAL ANALYSIS (Lexer)
============================================================================

File: core/lexer.py
Keywords Added:
    "don"  → KEYWORD_FOR       (for keyword)
    "zuwa" → KEYWORD_TO        (ascending direction)
    "ta"   → KEYWORD_STEP      (step specifier)

Note on "ba":
    "ba" is context-sensitive:
    - In else clause: KEYWORD_ELSE (part of "in ba haka ba")
    - In for loop: Descending direction
    Parser handles this contextually

Example Tokenization:
    Input:  "don i = 0 zuwa 10 ta 2:"
    Output: [
        Token(KEYWORD_FOR, "don", 1, 0),
        Token(IDENTIFIER, "i", 1, 4),
        Token(OPERATOR, "=", 1, 6),
        Token(NUMBER, "0", 1, 8),
        Token(KEYWORD_TO, "zuwa", 1, 10),
        Token(NUMBER, "10", 1, 15),
        Token(KEYWORD_STEP, "ta", 1, 18),
        Token(NUMBER, "2", 1, 21),
        Token(OPERATOR, ":", 1, 22),
        ...
    ]


============================================================================
PHASE 2: AST REPRESENTATION (Parser)
============================================================================

For AST Node Definition:
    @dataclass(frozen=True)
    class For(ASTNode):
        var: str                      # Loop variable name
        start: 'Expression'           # Starting value expression
        end: 'Expression'             # Ending value expression
        direction: str                # "ascending" or "descending"
        body: List['Statement']       # Loop body statements
        step: Optional['Expression']  # Optional step (default: None)

Example AST:
    For(
        var="i",
        start=Number(0),
        end=Number(10),
        direction="ascending",
        body=[Print(Identifier("i"))],
        step=Number(2),
        line=1, column=0
    )

Statement Type Union Updated:
    Statement = Union[..., For, ...]


============================================================================
PHASE 3: PARSING LOGIC (Parser)
============================================================================

File: core/parser.py
Method: parse_for()

Parsing Algorithm:

    1. expect(KEYWORD_FOR) → get "don" keyword

    2. expect(IDENTIFIER) → get loop variable name (e.g., "i")

    3. expect(OPERATOR "=") → verify assignment operator

    4. parse_expression() → evaluate start value

    5. Check direction token:
       - KEYWORD_TO ("zuwa") → direction = "ascending"
       - KEYWORD_ELSE "ba" → direction = "descending"
       (context-sensitive: must check in for-loop context)

    6. parse_expression() → evaluate end value

    7. Check for optional KEYWORD_STEP ("ta"):
       if found, parse_expression() → evaluate step value
       else, step = None (defaults to 1 in interpreter)

    8. expect(OPERATOR ":") → verify colon

    9. consume_newlines() + expect(INDENT) → start of block

    10. parse_block() → parse loop body statements

    11. expect(DEDENT) → end of block

    12. return For(...) → create For AST node

Example Parse Tree:
    Input: "don x = 0 zuwa 5: rubuta x"

    For(
        var="x",
        start=Number(0),
        end=Number(5),
        direction="ascending",
        body=[Print(Identifier("x"))],
        step=None,
        ...
    )


============================================================================
PHASE 4: EXECUTION - AST REWRITING (Interpreter)
============================================================================

File: core/interpreter.py
Method: execute_for()

CRITICAL: This is where the AST rewriting happens.

Instead of creating new AST nodes, we execute the rewritten logic directly:

Algorithm:

    1. Evaluate expressions to values:
       start_value = eval_expression(stmt.start, env)
       end_value = eval_expression(stmt.end, env)
       step_value = eval_expression(stmt.step, env) or 1

    2. Validate step:
       if step_value == 0: raise ValueError("step cannot be zero")
       if not numeric: raise TypeError("step must be numeric")

    3. Initialize loop variable:
       env.define_variable(stmt.var, start_value)

    4. If direction == "ascending":
       while (env.get_variable(stmt.var) < end_value):
           for each body_stmt:
               execute_statement(body_stmt, env)
           env.define_variable(stmt.var, current + step_value)

    5. If direction == "descending":
       while (env.get_variable(stmt.var) > end_value):
           for each body_stmt:
               execute_statement(body_stmt, env)
           env.define_variable(stmt.var, current - step_value)

EXAMPLE EXECUTION TRACE:

Code: don i = 0 zuwa 3: rubuta i

Iteration 1:
  Condition: 0 < 3 → True
  Execute: rubuta 0 (prints 0)
  Increment: i = 0 + 1 = 1

Iteration 2:
  Condition: 1 < 3 → True
  Execute: rubuta 1 (prints 1)
  Increment: i = 1 + 1 = 2

Iteration 3:
  Condition: 2 < 3 → True
  Execute: rubuta 2 (prints 2)
  Increment: i = 2 + 1 = 3

Iteration 4:
  Condition: 3 < 3 → False
  Exit loop

Output: "012"


============================================================================
WHY AST REWRITING (NOT SYNTHETIC AST NODES)?
============================================================================

We use DIRECT EXECUTION with INLINE loops, not synthetic AST nodes, because:

1. **Simpler Code:** No need to create and parse synthetic nodes

2. **Direct Values:** We evaluate expressions once and use the actual values

3. **Natural Mapping:** Maps directly to while loop semantics

4. **No Overhead:** Avoids re-evaluating constant expressions

5. **Better Error Messages:** Errors occur where they happen, not in synthetic code

Contrast:
  ❌ Would create: BinaryOp(Identifier, "<", Number)
  ✅ Do: env.get_variable(var) < evaluated_end_value


============================================================================
VALIDATION AND ERROR HANDLING
============================================================================

Step Value Validation:
    - Must not be zero (prevents infinite loop)
    - Must be numeric (int or float)
    - Error raised at runtime with clear message

Direction Validation:
    - Step must be positive (direction sign applied automatically)
    - For ascending: i += step
    - For descending: i -= step

Invalid For Loop Examples:

1. don i = 0 zuwa 10 ta 0:  → ValueError: step cannot be zero

2. don i = 0 zuwa 10 ta -2: → ValueError: ascending requires positive step

3. don i = 10 ba 0 ta -5:   → ValueError: descending requires positive step


============================================================================
VARIABLE SCOPING
============================================================================

For loops use the same environment as surrounding code:

1. Loop variable created/modified in current scope
2. Visible after loop ends
3. Can be modified in loop body
4. Nested loops have independent loop variables

Example:
    i = 100
    don i = 0 zuwa 3:
        rubuta i
    rubuta i        # i is 3 (loop modified it)

Output: "0123"


============================================================================
NESTED FOR LOOPS
============================================================================

For loops can be nested to any depth. Each loop is independent:

Code:
    don i = 1 zuwa 3:
        don j = 1 zuwa 3:
            rubuta i * j
            rubuta " "
        rubuta 10

Execution:
    i=1: j=1→3: 1 2 3 [newline]
    i=2: j=1→3: 2 4 6 [newline]
    i=3: j=1→3: 3 6 9 [newline]

Output: "1 2 3 \n2 4 6 \n3 6 9 \n"


============================================================================
FOR LOOPS IN FUNCTIONS
============================================================================

For loops work naturally inside functions:

Example:
    aiki sum_to(n):
        sum = 0
        don i = 1 zuwa n + 1:
            sum = sum + i
        mayar sum

    result = sum_to(5)
    rubuta result

Execution:
    Function call creates new environment
    For loop executes in function environment
    Loop variable i local to function
    Function returns sum value

Output: "15"


============================================================================
COMPARISON: FOR vs WHILE
============================================================================

When to use FOR:
    ✓ Known iteration count
    ✓ Numeric counting (0 to n)
    ✓ Simple loops
    ✓ Clear start/end values

When to use WHILE:
    ✓ Unknown iteration count
    ✓ Complex conditions
    ✓ Event-based loops
    ✓ Non-numeric iteration

BOTH ARE EQUIVALENT FOR COUNTING:
    while version:
        i = 0
        kadai i < 10:
            rubuta i
            i = i + 1

    for version:
        don i = 0 zuwa 10:
            rubuta i


============================================================================
TEST COVERAGE
============================================================================

All tests passing (6/6):

✓ TEST 1: Simple ascending (0 to 4)
✓ TEST 2: Ascending with step (0, 2, 4, 6, 8)
✓ TEST 3: Descending (5 to 1)
✓ TEST 4: Descending with step (10, 8, 6, 4, 2)
✓ TEST 5: Nested for loops (multiplication table)
✓ TEST 6: For loop in function (sum calculation)


============================================================================
EXTENSIBILITY
============================================================================

To add related features:

BREAK STATEMENT:
    - Exception-based mechanism (like return)
    - Exit loop early
    - Catch in execute_for/execute_while

CONTINUE STATEMENT:
    - Exception-based mechanism
    - Skip to next iteration
    - Continue the while loop

FOR-ELSE:
    - Execute else block after normal loop exit
    - Not executed if loop exited via break
    - Can be added to For node

RANGE FUNCTION:
    - Syntactic sugar for for loops
    - Create sequence of numbers
    - Can use with list iteration (when lists added)


============================================================================
SUMMARY
============================================================================

For loops in Hausalang:

1. SYNTAX: don i = start [zuwa|ba] end [ta step]:

2. PARSING: Full recursive-descent parser support

3. AST: For node with all components (var, start, end, direction, body, step)

4. EXECUTION: Direct rewriting to while-like semantics:
   - Initialize variable
   - Loop with condition (< for ascending, > for descending)
   - Body + increment/decrement

5. VALIDATION: Step validation, direction checking, error messages

6. INTEGRATION: Works with functions, nesting, all language features

7. TESTING: 100% pass rate on 6 comprehensive tests

8. QUALITY: Type-safe, well-documented, extensible design
"""
