line = 'rubuta "a >= 10"'
print(f"'=' in line: {'=' in line}")
if '=' in line:
    name, value = line.split('=', 1)
    print(f"name: {repr(name)}, value: {repr(value)}")
