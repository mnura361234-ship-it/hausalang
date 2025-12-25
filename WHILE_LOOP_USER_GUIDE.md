"""
WHILE LOOP QUICK REFERENCE - Hausalang User Guide
"""

============================================================================
WHILE LOOP SYNTAX
============================================================================

Basic Syntax:
    kadai condition:
        statement1
        statement2
        ...

The keyword "kadai" (Hausa: "while") introduces a loop.
The condition is evaluated before each iteration.
The body is executed repeatedly while the condition is truthy.


============================================================================
TRUTHINESS IN HAUSALANG
============================================================================

Truthy Values:
  - Any non-zero number: 1, -5, 3.14
  - Any non-empty string: "hello", "0"
  - True values from comparisons: 5 > 3, x == y

Falsy Values:
  - Zero: 0
  - Empty string: ""
  - False/None/null


============================================================================
EXAMPLE 1: Simple Counting Loop
============================================================================

Code:
    x = 0
    kadai x < 5:
        rubuta x
        x = x + 1

Output: 01234

Explanation:
  - x starts at 0
  - While x < 5 is true, print x and increment x
  - Loop executes 5 times (x = 0, 1, 2, 3, 4)
  - When x becomes 5, condition is false, loop exits


============================================================================
EXAMPLE 2: Sum Accumulation
============================================================================

Code:
    sum = 0
    i = 1
    kadai i <= 10:
        sum = sum + i
        i = i + 1
    rubuta sum

Output: 55

Explanation:
  - Calculate sum of 1 + 2 + 3 + ... + 10
  - i increments from 1 to 10
  - sum accumulates each value
  - Loop exits when i > 10
  - Result: 1+2+3+...+10 = 55


============================================================================
EXAMPLE 3: Print with Separator
============================================================================

Code:
    i = 1
    kadai i <= 5:
        rubuta i
        rubuta ","
        i = i + 1

Output: 1,2,3,4,5,

Explanation:
  - Print number, then comma
  - Repeat 5 times
  - Notice trailing comma (no special handling)


============================================================================
EXAMPLE 4: Nested While Loops
============================================================================

Code:
    i = 1
    kadai i <= 3:
        j = 1
        kadai j <= 3:
            rubuta i * j
            rubuta " "
            j = j + 1
        rubuta 10
        i = i + 1

Output:
    1 2 3
    2 4 6
    3 6 9

Explanation:
  - Outer loop: i from 1 to 3
  - Inner loop: j from 1 to 3
  - Print i*j for each (i,j) pair
  - Newline after each row


============================================================================
EXAMPLE 5: While Loop in Function
============================================================================

Code:
    aiki factorial(n):
        result = 1
        i = 1
        kadai i <= n:
            result = result * i
            i = i + 1
        mayar result

    f = factorial(5)
    rubuta f

Output: 120

Explanation:
  - Function computes n! using while loop
  - factorial(5) = 1*1*2*3*4*5 = 120
  - Loop variable i local to function
  - Return statement exits function


============================================================================
COMMON PATTERNS
============================================================================

Pattern 1: Count Up
    x = 0
    kadai x < n:
        # Do something with x
        x = x + 1

Pattern 2: Count Down
    x = n
    kadai x > 0:
        # Do something with x
        x = x - 1

Pattern 3: Accumulate
    sum = 0
    i = 0
    kadai i < n:
        sum = sum + values[i]  # (after lists are implemented)
        i = i + 1

Pattern 4: Condition-Based Exit
    x = 1
    kadai x < 1000000:
        x = x * 2
    # x is now >= 1000000


============================================================================
LIMITATIONS (Current Version)
============================================================================

Not Supported Yet:
  ✗ break statement (exit loop early)
  ✗ continue statement (skip to next iteration)
  ✗ else clause (execute after normal exit)
  ✗ for loops (use while instead for now)
  ✗ Lists and iteration
  ✗ Generator expressions


============================================================================
GOOD PRACTICES
============================================================================

1. Always ensure loop terminates
   ✓ GOOD: kadai x < 10: (condition becomes false)
   ✗ BAD:  kadai 1: (infinite loop - no way to exit)

2. Initialize loop variables before loop
   ✓ GOOD: x = 0; kadai x < 5: ...
   ✗ BAD:  kadai x < 5: x = x + 1 (x undefined)

3. Update loop variable in body
   ✓ GOOD: kadai x < 5: ... x = x + 1
   ✗ BAD:  kadai x < 5: rubuta x (infinite loop)

4. Use meaningful variable names
   ✓ GOOD: count = 0; kadai count < 5: ...
   ✗ BAD:  a = 0; kadai a < 5: ...

5. Keep loop bodies simple and focused
   ✓ GOOD: Single operation per iteration
   ✗ BAD:  Complex logic within loop


============================================================================
TROUBLESHOOTING
============================================================================

Problem: Infinite Loop
  Symptom: Program never finishes
  Cause: Loop condition never becomes false
  Solution: Check loop variable is properly updated

  Example:
    ✗ kadai x < 10: rubuta x  (x never changes)
    ✓ kadai x < 10: rubuta x; x = x + 1  (x incremented)

Problem: Loop Never Executes
  Symptom: Loop body not executed at all
  Cause: Condition is false from the start
  Solution: Check initial variable value

  Example:
    ✗ x = 10; kadai x < 5: ...  (x already >= 5)
    ✓ x = 0; kadai x < 5: ...   (x < 5 initially)

Problem: Variable Not Found
  Symptom: NameError: Undefined variable
  Cause: Loop variable not initialized before loop
  Solution: Define variable before loop starts

  Example:
    ✗ kadai x < 5: x = x + 1  (x not defined)
    ✓ x = 0; kadai x < 5: x = x + 1  (x defined)


============================================================================
COMPARISON WITH OTHER CONTROL FLOW
============================================================================

If Statement:
  idan condition:
      # Executes once if condition is true
  in ba haka ba:
      # Executes once if condition is false

While Loop:
  kadai condition:
      # Executes repeatedly while condition is true

For Loop:
  # Not yet implemented - use while for now


============================================================================
PERFORMANCE NOTES
============================================================================

While loops in Hausalang execute interpreted, so:
- Simple loops: Very fast (simple operations)
- Complex loops: Slower (interpreter overhead)
- Deep nesting: Linear slowdown per level

Example performance:
  sum_to_100: ~milliseconds
  sum_to_1000: ~milliseconds
  sum_to_million: ~seconds (depends on machine)


============================================================================
NEXT FEATURES
============================================================================

Planned for Future:
  1. For loops (similar to while)
  2. Break statement (exit loop early)
  3. Continue statement (skip iteration)
  4. List data type with iteration
  5. Range function for easy counting


============================================================================
"""
