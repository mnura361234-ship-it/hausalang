from core.interpreter import run

with open('examples/comparisons.ha','r',encoding='utf-8') as f:
    s=f.read()
    print('---FILE START---')
    print(s)
    print('---FILE END---')
    run(s)
