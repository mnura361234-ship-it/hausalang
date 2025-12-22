condition = 'a >= 10'
ops = ['==', '!=', '>=', '<=', '>', '<']

print(f"condition: {repr(condition)}")
for o in ops:
    print(f"  '{o}' in condition: {o in condition}")

two_char_ops = ['==', '!=', '>=', '<=']
found = None
for o in two_char_ops:
    if o in condition:
        found = o
        print(f"Found: {found}")
        break

if found:
    left_s, right_s = condition.split(found, 1)
    print(f"left_s: {repr(left_s)}, right_s: {repr(right_s)}")
