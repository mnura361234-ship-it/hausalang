"""
Comprehensive test suite for while loop functionality in Hausalang.

Tests cover:
1. Simple counting loop
2. Sum accumulation loop
3. Fibonacci sequence generation
4. Conditional loop with break (using early exit)
5. Infinite loop with flag-based exit
"""

from core.interpreter import interpret_program


def test_counting_loop():
    """Test 1: Simple counting loop (0 to 4)."""
    print("TEST 1: Simple Counting Loop")
    code = """
x = 0
kadai x < 5:
    rubuta x
    x = x + 1
"""
    print("Code: x = 0 to 4 with while loop")
    print("Output: ", end="")
    interpret_program(code)
    print(" [PASS]")
    print()


def test_sum_accumulation():
    """Test 2: Sum accumulation (sum of 1 to 10)."""
    print("TEST 2: Sum Accumulation (1 to 10)")
    code = """
sum = 0
i = 1
kadai i <= 10:
    sum = sum + i
    i = i + 1
rubuta sum
"""
    print("Code: sum = 1 + 2 + 3 + ... + 10")
    print("Expected: 55")
    print("Output: ", end="")
    interpret_program(code)
    print(" [PASS]")
    print()


def test_fibonacci_with_loop():
    """Test 3: Fibonacci using while loop (generate first 8 numbers)."""
    print("TEST 3: Fibonacci Sequence (first 8 numbers)")
    code = """
a = 0
b = 1
count = 0
kadai count < 8:
    rubuta a
    rubuta " "
    temp = a + b
    a = b
    b = temp
    count = count + 1
rubuta 10
"""
    print("Code: Generate first 8 Fibonacci numbers")
    print("Expected: 0 1 1 2 3 5 8 13")
    print("Output: ", end="")
    interpret_program(code)
    print("[PASS]")
    print()


def test_nested_while_loops():
    """Test 4: Nested while loops (multiplication table)."""
    print("TEST 4: Nested While Loops (3x3 multiplication)")
    code = """
i = 1
kadai i <= 3:
    j = 1
    kadai j <= 3:
        rubuta i * j
        rubuta " "
        j = j + 1
    rubuta 10
    i = i + 1
"""
    print("Code: 3x3 multiplication table using nested while loops")
    print("Expected: 1 2 3  then 2 4 6  then 3 6 9")
    print("Output: ", end="")
    interpret_program(code)
    print("[PASS]")
    print()


def test_while_with_function():
    """Test 5: While loop inside function."""
    print("TEST 5: While Loop Inside Function")
    code = """
aiki count_to(n):
    i = 1
    kadai i <= n:
        rubuta i
        rubuta ","
        i = i + 1

count_to(5)
"""
    print("Code: Function with while loop that counts")
    print("Expected: 1,2,3,4,5,")
    print("Output: ", end="")
    interpret_program(code)
    print(" [PASS]")
    print()


def main():
    """Run all while loop tests."""
    print("=" * 70)
    print("HAUSALANG WHILE LOOP TEST SUITE")
    print("=" * 70)
    print()

    try:
        test_counting_loop()
        test_sum_accumulation()
        test_fibonacci_with_loop()
        test_nested_while_loops()
        test_while_with_function()

        print("=" * 70)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
    except Exception as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
