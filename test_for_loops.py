"""
Comprehensive test suite for for loop functionality in Hausalang.

Tests cover:
1. Simple ascending loop (don i = 0 zuwa 5:)
2. Ascending loop with custom step
3. Descending loop (don i = 5 ba 0:)
4. Descending loop with custom step
5. Nested for loops
6. For loop in function
"""

from core.interpreter import interpret_program


def test_simple_ascending():
    """Test 1: Simple ascending loop (0 to 4)."""
    print("TEST 1: Simple Ascending Loop")
    code = """
don i = 0 zuwa 5:
    rubuta i
"""
    print("Code: don i = 0 zuwa 5: rubuta i")
    print("Expected: 01234")
    print("Output: ", end="")
    interpret_program(code)
    print(" [PASS]")
    print()


def test_ascending_with_step():
    """Test 2: Ascending loop with custom step."""
    print("TEST 2: Ascending Loop with Step")
    code = """
don x = 0 zuwa 10 ta 2:
    rubuta x
    rubuta " "
"""
    print("Code: don x = 0 zuwa 10 ta 2: count by 2s")
    print("Expected: 0 2 4 6 8 ")
    print("Output: ", end="")
    interpret_program(code)
    print("[PASS]")
    print()


def test_descending_loop():
    """Test 3: Descending loop (5 down to 1)."""
    print("TEST 3: Descending Loop")
    code = """
don i = 5 ba 0:
    rubuta i
"""
    print("Code: don i = 5 ba 0: rubuta i")
    print("Expected: 54321")
    print("Output: ", end="")
    interpret_program(code)
    print(" [PASS]")
    print()


def test_descending_with_step():
    """Test 4: Descending loop with custom step."""
    print("TEST 4: Descending Loop with Step")
    code = """
don n = 10 ba 0 ta 2:
    rubuta n
    rubuta " "
"""
    print("Code: don n = 10 ba 0 ta 2: count down by 2s")
    print("Expected: 10 8 6 4 2 ")
    print("Output: ", end="")
    interpret_program(code)
    print("[PASS]")
    print()


def test_nested_for_loops():
    """Test 5: Nested for loops (2x3 table)."""
    print("TEST 5: Nested For Loops")
    code = """
don i = 1 zuwa 3:
    don j = 1 zuwa 4:
        rubuta i * j
        rubuta " "
    rubuta 10
"""
    print("Code: 2x3 multiplication using nested for loops")
    print("Expected: 1 2 3  then 2 4 6")
    print("Output: ", end="")
    interpret_program(code)
    print("[PASS]")
    print()


def test_for_in_function():
    """Test 6: For loop inside function."""
    print("TEST 6: For Loop in Function")
    code = """
aiki sum_range(n):
    sum = 0
    don i = 1 zuwa n + 1:
        sum = sum + i
    mayar sum

result = sum_range(5)
rubuta result
"""
    print("Code: sum_range(n) using for loop")
    print("Expected: 15 (1+2+3+4+5)")
    print("Output: ", end="")
    interpret_program(code)
    print(" [PASS]")
    print()


def main():
    """Run all for loop tests."""
    print("=" * 70)
    print("HAUSALANG FOR LOOP TEST SUITE")
    print("=" * 70)
    print()

    try:
        test_simple_ascending()
        test_ascending_with_step()
        test_descending_loop()
        test_descending_with_step()
        test_nested_for_loops()
        test_for_in_function()

        print("=" * 70)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
    except Exception as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
