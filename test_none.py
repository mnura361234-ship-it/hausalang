from hausalang.repl.session import ReplSession

s = ReplSession()
r1 = s.execute("result = None")
print(f"success: {r1.success}")
print(f'result: {s.get_variable("result")}')
