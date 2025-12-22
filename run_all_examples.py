from core.interpreter import run
import sys

examples = [
    'examples/hello.ha',
    'examples/variables.ha',
    'examples/if.ha',
    'examples/else.ha',
    'examples/comparisons.ha',
    'examples/badvar.ha',
]

for ex in examples:
    print(f"\n{'='*60}")
    print(f"Running: {ex}")
    print(f"{'='*60}")
    with open(ex, 'r', encoding='utf-8') as f:
        code = f.read()
        print(f"Source:\n{code}")
        print(f"\nOutput:")
        print(f"{'-'*60}")
        run(code)
        print(f"{'-'*60}")
