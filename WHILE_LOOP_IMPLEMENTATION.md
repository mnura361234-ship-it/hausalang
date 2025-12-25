"""
WHILE LOOP IMPLEMENTATION - COMPLETE SYSTEM EXPLANATION

This document explains how while loops work in Hausalang, detailing how
the Lexer, Parser, and Interpreter collaborate to execute loops.

============================================================================
OVERVIEW
============================================================================

A while loop in Hausalang follows this syntax:

    kadai condition:
        statement1
        statement2
        ...

The keyword "kadai" (Hausa for "while") introduces a loop that executes
its body repeatedly as long as the condition remains truthy.

Example:
    x = 0
    kadai x < 5:
        rubuta x
        x = x + 1

This prints: 01234


============================================================================
PHASE 1: LEXICAL ANALYSIS (Lexer)
============================================================================

File: core/lexer.py
Key Addition: Added "kadai" to KEYWORDS dictionary

    KEYWORDS = {
        "idan": "KEYWORD_IF",
        ...
        "kadai": "KEYWORD_WHILE",  # NEW
    }

EXECUTION FLOW:
1. When lexer encounters "kadai" in source code
2. Looks up "kadai" in KEYWORDS dictionary
3. Matches the string "kadai"
4. Returns Token(type="KEYWORD_WHILE", value="kadai", line=..., column=...)

EXAMPLE TOKEN STREAM:
    Input:  "kadai x < 5:"
    Tokens: [
        Token("KEYWORD_WHILE", "kadai", 1, 0),
        Token("IDENTIFIER", "x", 1, 6),
        Token("OPERATOR", "<", 1, 8),
        Token("NUMBER", "5", 1, 10),
        Token("OPERATOR", ":", 1, 11),
        Token("NEWLINE", "\\n", 1, 12),
        ...
    ]

PURPOSE: Classify "kadai" as a language keyword, distinguishing it from
variables and other identifiers.


============================================================================
PHASE 2: PARSING (Parser)
============================================================================

File: core/parser.py
Key Additions:
1. While AST node (dataclass)
2. parse_while() method (44 lines)
3. Updated parse_statement() dispatcher
4. Updated Statement type union

--
2A. WHILE AST NODE DEFINITION
--

@dataclass(frozen=True)
class While(ASTNode):
    """While loop.

    kadai x < 10:
        rubuta x
        x = x + 1
    """
    condition: 'Expression'   # Expression to evaluate before each iteration
    body: List['Statement']   # Statements to execute in each iteration

This immutable dataclass represents a while loop in the AST.

--
2B. PARSE_WHILE() METHOD
--

def parse_while(self) -> While:
    # 1. Consume KEYWORD_WHILE token
    while_token = self.expect("KEYWORD_WHILE", 'Expected "kadai"')

    # 2. Parse the condition (any valid expression)
    condition = self.parse_expression()

    # 3. Expect ":" separator
    colon_token = self.peek()
    if not colon_token or colon_token.type != "OPERATOR" or colon_token.value != ":":
        self._error('Expected ":" after while condition', colon_token)
    self.advance()

    # 4. Expect indentation (NEWLINE followed by INDENT)
    self.consume_newlines()
    self.expect("INDENT", "Expected INDENT after while block")

    # 5. Parse body statements (until DEDENT)
    body = self.parse_block()

    # 6. Expect dedent (end of block)
    self.expect("DEDENT", "Expected DEDENT after while block")

    # 7. Return While AST node
    return While(
        condition=condition,
        body=body,
        line=while_token.line,
        column=while_token.column
    )

DESIGN NOTE: This method exactly mirrors parse_if(), ensuring consistency.
The only difference is that While has no else_body (no "in ba haka ba").

--
2C. PARSE_STATEMENT() DISPATCHER UPDATE
--

def parse_statement(self) -> Optional[Statement]:
    token = self.peek()

    if token.type == "KEYWORD_FUNCTION":
        return self.parse_function()

    if token.type == "KEYWORD_IF":
        return self.parse_if()

    if token.type == "KEYWORD_WHILE":      # NEW
        return self.parse_while()           # NEW

    if token.type == "KEYWORD_RETURN":
        return self.parse_return()

    ...

EXECUTION FLOW:
1. parse_statement() is called to parse the next statement
2. peek() returns KEYWORD_WHILE token
3. isinstance check matches token.type == "KEYWORD_WHILE"
4. Dispatches to parse_while()
5. parse_while() builds and returns While AST node

--
2D. STATEMENT TYPE UNION UPDATE
--

Statement = Union[Assignment, Print, Return, If, While, Function, ExpressionStatement]
                                           ^^^^^ NEW

This enables the type system to recognize While as a valid statement.

--
2E. EXAMPLE: PARSING A WHILE LOOP
--

Input Source:
    x = 0
    kadai x < 5:
        rubuta x
        x = x + 1

Token Stream:
    IDENTIFIER("x"), OPERATOR("="), NUMBER("0"), NEWLINE,
    KEYWORD_WHILE("kadai"), IDENTIFIER("x"), OPERATOR("<"), NUMBER("5"), OPERATOR(":"), NEWLINE,
    INDENT,
        KEYWORD_PRINT("rubuta"), IDENTIFIER("x"), NEWLINE,
        IDENTIFIER("x"), OPERATOR("="), IDENTIFIER("x"), OPERATOR("+"), NUMBER("1"), NEWLINE,
    DEDENT,
    EOF

Parsing:
1. parse() calls parse_statement() for first statement
2. Parses: Assignment(name="x", value=Number(0))
3. parse() calls parse_statement() for second statement
4. Token is KEYWORD_WHILE → dispatches to parse_while()
5. parse_while() parses:
   - condition = BinaryOp(Identifier("x"), "<", Number(5))
   - body = [
       Print(Identifier("x")),
       Assignment(name="x", value=BinaryOp(Identifier("x"), "+", Number(1)))
     ]
6. Returns: While(condition=..., body=[...])

Resulting AST:
Program(statements=[
    Assignment(name="x", value=Number(0, line=1, column=4), line=1, column=0),
    While(
        condition=BinaryOp(
            left=Identifier("x", line=2, column=6),
            operator="<",
            right=Number(5, line=2, column=10),
            line=2, column=6
        ),
        body=[
            Print(Identifier("x", line=3, column=17), line=3, column=12),
            Assignment(name="x", value=BinaryOp(...), line=4, column=8)
        ],
        line=2, column=0
    )
])

PURPOSE: Convert textual "kadai x < 5: ..." into structured While AST node
that the interpreter can execute.


============================================================================
PHASE 3: INTERPRETATION (Interpreter)
============================================================================

File: core/interpreter.py
Key Additions:
1. execute_while() method (20 lines)
2. Updated execute_statement() dispatcher

--
3A. EXECUTE_WHILE() METHOD
--

def execute_while(self, stmt: parser.While, env: Environment) -> None:
    """Execute a while loop."""
    while self.is_truthy(self.eval_expression(stmt.condition, env)):
        # Execute loop body
        for body_stmt in stmt.body:
            self.execute_statement(body_stmt, env)

ALGORITHM:
1. Loop while condition is truthy:
   a. Evaluate condition expression with current environment
   b. Check if result is truthy using is_truthy()
   c. If falsy, exit loop
   d. If truthy, execute each statement in body
   e. Return to step 1

EXAMPLE EXECUTION:
Loop iteration 1:
  Evaluate: x < 5 → 0 < 5 → True
  Execute: rubuta x (prints 0)
  Execute: x = x + 1 (x becomes 1)

Loop iteration 2:
  Evaluate: x < 5 → 1 < 5 → True
  Execute: rubuta x (prints 1)
  Execute: x = x + 1 (x becomes 2)

... (iterations 3-4 similar) ...

Loop iteration 5:
  Evaluate: x < 5 → 4 < 5 → True
  Execute: rubuta x (prints 4)
  Execute: x = x + 1 (x becomes 5)

Loop iteration 6:
  Evaluate: x < 5 → 5 < 5 → False
  Exit loop

Output: 01234

--
3B. EXECUTE_STATEMENT() DISPATCHER UPDATE
--

def execute_statement(self, stmt: parser.Statement, env: Environment) -> None:
    if isinstance(stmt, parser.Assignment):
        self.execute_assignment(stmt, env)
    elif isinstance(stmt, parser.Print):
        self.execute_print(stmt, env)
    elif isinstance(stmt, parser.Return):
        self.execute_return(stmt, env)
    elif isinstance(stmt, parser.If):
        self.execute_if(stmt, env)
    elif isinstance(stmt, parser.While):      # NEW
        self.execute_while(stmt, env)         # NEW
    elif isinstance(stmt, parser.Function):
        self.execute_function_def(stmt, env)
    elif isinstance(stmt, parser.ExpressionStatement):
        self.eval_expression(stmt.expression, env)
    else:
        raise RuntimeError(f"Unknown statement type: {type(stmt)}")

EXECUTION FLOW:
1. execute_statement() receives a While AST node
2. isinstance(stmt, parser.While) is True
3. Dispatches to execute_while()
4. execute_while() iterates while condition is true

--
3C. SUPPORTING METHODS
--

is_truthy(value):
    """Determine truthiness in Hausalang."""
    if value is False or value is None:
        return False
    if value == 0 or value == "":
        return False
    return True

This method determines whether a condition is true or false:
    is_truthy(5) → True
    is_truthy(0) → False
    is_truthy("hello") → True
    is_truthy("") → False
    is_truthy(None) → False

eval_expression(expr, env):
    """Evaluate any expression in an environment."""
    Used to evaluate the loop condition before each iteration.


============================================================================
COMPLETE END-TO-END EXECUTION TRACE
============================================================================

Source Code:
    x = 0
    kadai x < 5:
        rubuta x
        x = x + 1

Step 1: LEXICAL ANALYSIS
    Lexer converts source to token stream:
    [Assignment tokens, While tokens with INDENT/DEDENT, ...]

Step 2: PARSING
    Parser converts tokens to AST:
    Program([
        Assignment(name="x", value=Number(0)),
        While(condition=BinaryOp(...), body=[...])
    ])

Step 3: INTERPRETATION
    Interpreter walks the AST:

    3.1. Execute Program node
         For each statement in program.statements:

    3.2. Execute Assignment(name="x", value=Number(0))
         env.define_variable("x", 0)
         Global env: {x: 0}

    3.3. Execute While(condition=x<5, body=[...])
         Call execute_while()

    3.4. Loop iteration 1:
         - Eval condition: x < 5 → 0 < 5 → True
         - Execute body statements:
           - Execute Print(x): eval_expression(x) → 0; print(0)
           - Execute Assignment(x = x+1):
             eval_expression(x+1) → 1
             env.define_variable("x", 1)
         - Go to next iteration

    3.5. Loop iteration 2:
         - Eval condition: x < 5 → 1 < 5 → True
         - Execute body statements:
           - Print 1
           - x = 2

    ... (iterations 3-4 similar) ...

    3.6. Loop iteration 5:
         - Eval condition: x < 5 → 4 < 5 → True
         - Execute body statements:
           - Print 4
           - x = 5

    3.7. Loop iteration 6:
         - Eval condition: x < 5 → 5 < 5 → False
         - Exit loop (while condition is false)

Step 4: OUTPUT
    Output on stdout: "01234"

The entire program execution is complete.


============================================================================
VARIABLE SCOPING IN WHILE LOOPS
============================================================================

The while loop executes in the same environment as the code that declares it.
This means:
- Variables created before the loop remain accessible inside the loop
- Variables modified in the loop persist after the loop ends
- Variables created inside the loop (if supported) are local to that block

Example:
    x = 0                # x defined in global env
    kadai x < 3:
        y = x * 2        # y defined in loop body
        x = x + 1        # x modified in loop body
    rubuta x             # x is 3 (modified by loop)
    rubuta y             # y is 4 (last value from loop)

In current Hausalang: y would be undefined after the loop since we don't
track block-local scopes. Each variable assignment updates the current env.


============================================================================
NESTED WHILE LOOPS
============================================================================

While loops can be nested arbitrarily deep. Each nested loop has its own
condition that is evaluated independently.

Example: Multiplication table
    i = 1
    kadai i <= 3:
        j = 1
        kadai j <= 3:
            rubuta i * j
            rubuta " "
            j = j + 1
        rubuta 10         # Newline
        i = i + 1

Execution:
    i=1: j=1→3: print 1,2,3; newline
    i=2: j=1→3: print 2,4,6; newline
    i=3: j=1→3: print 3,6,9; newline

Output: "1 2 3 \n2 4 6 \n3 6 9 \n"

Parser creates nested While nodes. Interpreter executes them correctly
due to environment continuity and proper condition re-evaluation.


============================================================================
WHILE LOOPS IN FUNCTIONS
============================================================================

While loops inside functions work correctly because:
1. Function body is executed in a new environment with parent = calling env
2. Loop condition is evaluated in that function environment
3. Loop body statements are executed in the same environment
4. Variables modified in loop persist within the function
5. When function returns, the function environment is discarded

Example:
    aiki sum_to(n):
        sum = 0
        i = 1
        kadai i <= n:
            sum = sum + i
            i = i + 1
        mayar sum

    result = sum_to(5)
    rubuta result        # Prints 15

Function environment:
    Parent: global env
    Variables: {sum: 15, i: 6, n: 5}

After function return, sum and i are not accessible globally.


============================================================================
DESIGN DECISIONS AND RATIONALE
============================================================================

1. USE "kadai" AS KEYWORD
   Rationale: Natural Hausa word meaning "while" or "so long as"
   Alternative: "har da", "saai"
   Chosen: "kadai" for clarity and cultural authenticity

2. SAME BLOCK SYNTAX AS IF STATEMENTS
   Rationale: Consistency, users already understand INDENT/DEDENT
   Alternative: Braces {...}, different syntax
   Chosen: Indentation for simplicity and Python-like feel

3. NO ELSE CLAUSE FOR WHILE
   Rationale: While-else (execute block after normal loop exit) is uncommon
   Alternative: Support "in ba haka ba" after while
   Chosen: Simpler design for now, can be added later

4. LOOP CONDITION RE-EVALUATED EACH ITERATION
   Rationale: Standard while loop semantics
   Alternative: Evaluate once at start
   Chosen: Re-evaluation allows for proper loop termination

5. NO BREAK/CONTINUE STATEMENTS YET
   Rationale: Complexity increase, can be addressed separately
   Alternative: Add keyword_break and keyword_continue
   Chosen: Keep loops simple initially, add later

6. REUSE is_truthy() FOR LOOP CONDITIONS
   Rationale: Consistent with if statement conditions
   Alternative: Require explicit boolean expressions
   Chosen: is_truthy() provides intuitive behavior


============================================================================
TESTING STRATEGY
============================================================================

Test Coverage:
1. Simple counting loop (basic iteration)
2. Sum accumulation (modifying variables)
3. Fibonacci generation (complex expressions)
4. Nested while loops (loop within loop)
5. While inside function (function scoping)

All 5 tests pass, confirming:
✓ Lexer recognizes "kadai" keyword
✓ Parser builds correct While AST nodes
✓ Interpreter executes loops correctly
✓ Condition evaluation works properly
✓ Loop body executes repeatedly
✓ Variables persist across iterations
✓ Nested loops work correctly
✓ Loops work inside functions


============================================================================
EXTENSIBILITY
============================================================================

To add for loops next:
1. Add "don" (or similar) keyword to lexer
2. Create For AST node with var, start, end, body
3. Implement parse_for() method
4. Add execute_for() method
5. Update dispatchers

To add break/continue:
1. Create Break and Continue AST nodes
2. Use exception-based mechanism like ReturnValue
3. Catch BreakException in execute_while()
4. Handle in interpreter dispatch

To add while-else:
1. Add else_body field to While AST node
2. Update parse_while() to check for else
3. Update execute_while() to run else_body if loop exits normally
4. (Not run else_body if break is used)


============================================================================
SUMMARY
============================================================================

The while loop implementation demonstrates clean separation of concerns:

LEXER: Recognizes "kadai" as a keyword and produces KEYWORD_WHILE token

PARSER: Understands while syntax and creates While AST nodes
  - Parses condition expression
  - Handles INDENT/DEDENT for blocks
  - Returns immutable While dataclass

INTERPRETER: Executes While nodes by repeatedly evaluating condition
  - Leverages is_truthy() for truthiness
  - Executes body statements in loop
  - Maintains proper environment/scoping
  - Integrates naturally with rest of language

This architecture enables:
✓ Simple addition of new control flow structures
✓ Clear execution semantics
✓ Proper variable scoping
✓ Nested loop support
✓ Integration with functions
✓ Type safety via dataclasses


TEST RESULTS:
✓ All 5 comprehensive tests passing
✓ Covers basic, arithmetic, complex, nested, and function scenarios
✓ Ready for for loop implementation next
✓ Foundation solid for further language expansion
"""
