#!/usr/bin/env python3
from hausalang.repl.session import ReplSession

s = ReplSession()
r = s.execute(
    """
n = 27
steps = 0
kadai n != 1:
    idan n % 2 == 0:
        n = n / 2
    in ba haka ba:
        n = (n * 3) + 1
    steps = steps + 1
"""
)
print("Success:", r.success)
if r.error:
    print("Error:", r.error.kind.name, "-", r.error.message)
print("Variables:", list(s.list_variables().keys()))
if s.variable_exists("steps"):
    print("steps =", s.get_variable("steps"))
