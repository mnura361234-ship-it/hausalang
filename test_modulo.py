#!/usr/bin/env python3
from hausalang.repl.session import ReplSession

s = ReplSession()
r = s.execute("n = 5")
print("n =", s.get_variable("n"))

r = s.execute("n % 2")
print("Modulo result:", r.output)

r = s.execute(
    """
idan n % 2 == 0:
    m = "even"
in ba haka ba:
    m = "odd"
"""
)
print("Success:", r.success)
if r.error:
    print("Error:", r.error.message)
else:
    print("m =", s.get_variable("m"))
