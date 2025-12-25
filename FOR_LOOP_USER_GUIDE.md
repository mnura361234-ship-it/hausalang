"""
FOR LOOP USER GUIDE - Hausalang

Quick reference and examples for using for loops.
"""

============================================================================
FOR LOOP SYNTAX REFERENCE
============================================================================

BASIC SYNTAX:

    don variable = start zuwa end:
        statements

Example:
    don i = 0 zuwa 5:
        rubuta i


WITH STEP:

    don variable = start zuwa end ta step:
        statements

Example:
    don i = 0 zuwa 10 ta 2:
        rubuta i


DESCENDING:

    don variable = start ba end:
        statements

Example:
    don i = 5 ba 0:
        rubuta i


WITH STEP (DESCENDING):

    don variable = start ba end ta step:
        statements

Example:
    don i = 10 ba 0 ta 2:
        rubuta i


============================================================================
SEMANTICS
============================================================================

ASCENDING (zuwa):
    Loop while: var < end
    Increment: var = var + step (default step = 1)

DESCENDING (ba):
    Loop while: var > end
    Decrement: var = var - step (default step = 1)

BOUNDS:
    Ascending: includes start, excludes end
    Descending: includes start, excludes end

Examples:
    don i = 0 zuwa 5:    # i = 0, 1, 2, 3, 4 (NOT 5)
    don i = 5 ba 0:      # i = 5, 4, 3, 2, 1 (NOT 0)


============================================================================
EXAMPLE 1: SIMPLE COUNTING
============================================================================

Code:
    don i = 0 zuwa 5:
        rubuta i

Output: 01234

Explanation:
    - i starts at 0
    - Loop while i < 5
    - Print i each iteration
    - Auto-increment i by 1


============================================================================
EXAMPLE 2: COUNTING WITH STEP
============================================================================

Code:
    don x = 0 zuwa 10 ta 2:
        rubuta x
        rubuta " "

Output: 0 2 4 6 8

Explanation:
    - x starts at 0
    - Loop while x < 10
    - Increment x by 2 each iteration
    - Print x with space separator


============================================================================
EXAMPLE 3: COUNTDOWN
============================================================================

Code:
    don n = 5 ba 0:
        rubuta n

Output: 54321

Explanation:
    - n starts at 5
    - Loop while n > 0
    - Auto-decrement n by 1
    - Print n each iteration


============================================================================
EXAMPLE 4: COUNTDOWN WITH STEP
============================================================================

Code:
    don i = 20 ba 0 ta 5:
        rubuta i
        rubuta " "

Output: 20 15 10 5

Explanation:
    - i starts at 20
    - Loop while i > 0
    - Decrement i by 5
    - Print i with space


============================================================================
EXAMPLE 5: SUM CALCULATION
============================================================================

Code:
    sum = 0
    don i = 1 zuwa 11:
        sum = sum + i
    rubuta sum

Output: 55

Explanation:
    - sum_range(1..10)
    - Use for loop to add 1+2+3+...+10
    - Result is 55


============================================================================
EXAMPLE 6: NESTED LOOPS - MULTIPLICATION TABLE
============================================================================

Code:
    don i = 1 zuwa 4:
        don j = 1 zuwa 4:
            rubuta i * j
            rubuta " "
        rubuta 10

Output:
    1 2 3
    2 4 6
    3 6 9

Explanation:
    - Outer loop: i from 1 to 3
    - Inner loop: j from 1 to 3
    - For each pair, print i*j
    - Newline after each row


============================================================================
EXAMPLE 7: FOR LOOP IN FUNCTION
============================================================================

Code:
    aiki factorial(n):
        result = 1
        don i = 1 zuwa n + 1:
            result = result * i
        mayar result

    f = factorial(5)
    rubuta f

Output: 120

Explanation:
    - Function calculates n! using for loop
    - factorial(5) = 1*2*3*4*5 = 120
    - For loop executes in function scope


============================================================================
EXAMPLE 8: STRING REPETITION
============================================================================

Code:
    don i = 0 zuwa 5:
        rubuta "Ha"
    rubuta 10

Output: HaHaHaHaHa

Explanation:
    - Loop 5 times
    - Print "Ha" each iteration
    - Newline at end


============================================================================
EXAMPLE 9: PATTERN GENERATION
============================================================================

Code:
    don row = 1 zuwa 4:
        don col = 1 zuwa row + 1:
            rubuta col
        rubuta 10

Output:
    1
    1 2
    1 2 3

Explanation:
    - Outer loop: row from 1 to 3
    - Inner loop: col from 1 to row
    - Print col each iteration
    - Creates triangle pattern


============================================================================
EXAMPLE 10: FILTERING WITH MODULO
============================================================================

Code:
    don i = 0 zuwa 10:
        idan i * 2 == 10:
            rubuta i

Output: 5

Explanation:
    - Loop through i = 0 to 9
    - Print only if i*2 == 10
    - Only i=5 satisfies condition


============================================================================
COMMON PATTERNS
============================================================================

Pattern 1: Count and Print
    don i = 0 zuwa n:
        rubuta i

Pattern 2: Sum Range
    sum = 0
    don i = 1 zuwa n + 1:
        sum = sum + i

Pattern 3: Multiplication Table
    don i = 1 zuwa n + 1:
        don j = 1 zuwa m + 1:
            rubuta i * j

Pattern 4: Countdown
    don i = n ba 0:
        rubuta i

Pattern 5: Even Numbers
    don i = 0 zuwa n ta 2:
        rubuta i

Pattern 6: Fibonacci Sequence
    a = 0
    b = 1
    don i = 0 zuwa n:
        rubuta a
        temp = a + b
        a = b
        b = temp


============================================================================
TRUTHINESS IN FOR LOOPS
============================================================================

For loops use numeric comparison, so truthiness doesn't apply directly.

Condition evaluation:
    Ascending: i < end (numeric comparison)
    Descending: i > end (numeric comparison)

Both must evaluate to true/false based on numeric values.


============================================================================
STEP VALUE RULES
============================================================================

ASCENDING (zuwa):
    - Step must be positive (enforced)
    - default: 1
    - Example: ta 2 (increment by 2)

DESCENDING (ba):
    - Step must be positive (automatically negated)
    - default: 1
    - Example: ta 3 (decrement by 3)

INVALID:
    ✗ ta 0  (zero step - causes error)
    ✗ don i = 0 zuwa 10 ta -1  (negative step with zuwa - causes error)


============================================================================
VARIABLE SCOPE
============================================================================

Loop Variable Scope:
    - Created in current scope
    - Visible after loop ends
    - Can modify in loop body
    - Persists with final value after loop

Example:
    i = 100
    don i = 0 zuwa 3:
        rubuta i
    rubuta " "
    rubuta i

Output: 0123

Explanation:
    - Loop reuses/overwrites i
    - After loop, i = 3
    - Both loop and final i are printed


============================================================================
LOOP BEHAVIOR
============================================================================

LOOP BOUNDS:

Ascending: for (start, end)
    Includes: start
    Excludes: end
    Range: [start, end)

Descending: for (start, end)
    Includes: start
    Excludes: end
    Range: (end, start]

LOOP DOES NOT EXECUTE IF:
    Ascending: start >= end
    Descending: start <= end

Example:
    don i = 5 zuwa 5:
        rubuta i
    (loop doesn't execute, i stays 5)


============================================================================
FREQUENTLY ASKED QUESTIONS
============================================================================

Q: How do I iterate from N down to 1 (including 1)?
A: Use "ba 0" (down to 0, excluding 0, so goes 1, not reaching 0)
   don i = n ba 0:
       rubuta i

Q: How do I skip numbers in a loop?
A: Use step with "ta" keyword
   don i = 0 zuwa 10 ta 2:
       rubuta i

Q: Can I modify the loop variable in the loop body?
A: Yes, but the increment/decrement still happens after body execution
   don i = 0 zuwa 10:
       i = i + 5  # manual change
       # increment still happens: i += 1

Q: Can for loops be nested?
A: Yes, to any depth
   don i = 0 zuwa 3:
       don j = 0 zuwa 3:
           rubuta i * j

Q: What's the difference between for and while loops?
A: For loops are better for counting, while for complex conditions
   For: known iteration count, numeric ranges
   While: unknown count, complex conditions

Q: Can for loops be used with lists/arrays?
A: Not yet - lists not implemented. Use traditional for loops for now.
   Future: don item in list: ...

Q: What if start == end?
A: Loop doesn't execute (0 iterations)

Q: What if step is larger than range?
A: Loop might execute once or zero times depending on bounds
   don i = 0 zuwa 5 ta 10:
       rubuta i
   Prints: 0 (i < 5, then i += 10 makes i = 10, now i not < 5)


============================================================================
ERROR MESSAGES
============================================================================

"For loop step cannot be zero"
    Cause: Tried to use ta 0
    Fix: Use positive step value

"For loop: ascending (zuwa) direction requires positive step, got -2"
    Cause: Used negative step with zuwa
    Fix: Use positive step, or use ba direction

"For loop: descending (ba) direction requires positive step, got -1"
    Cause: Used negative step with ba
    Fix: Use positive step (automatically negated)

"TypeError: For loop step must be numeric, got <type>"
    Cause: Step evaluated to non-numeric value
    Fix: Ensure step is a number


============================================================================
BEST PRACTICES
============================================================================

1. Use for loops when you know the iteration count
2. Use descriptive variable names (don row, don i)
3. Keep loop bodies simple (complex logic → separate function)
4. Use step correctly (positive for both zuwa and ba)
5. Remember bounds exclude end value
6. Use nested loops sparingly (indentation gets complex)
7. Test boundary conditions (i=0, i=end-1)


============================================================================
"""
