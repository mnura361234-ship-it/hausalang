import re


def strip_comments(s: str) -> str:
    i = 0
    while True:
        idx = s.find('#', i)
        if idx == -1:
            return s
        before = s[:idx]
        if before.count('"') % 2 == 0:
            return s[:idx].rstrip()
        i = idx + 1


def tokenize_expr(expr: str):
    tokens = []
    i = 0
    while i < len(expr):
        c = expr[i]
        if c.isspace():
            i += 1
            continue
        if c in '+-*/()':
            tokens.append(c)
            i += 1
            continue
        if c == '"':
            j = i + 1
            while j < len(expr):
                if expr[j] == '"' and expr[j-1] != '\\':
                    break
                j += 1
            if j >= len(expr):
                return None
            tokens.append(expr[i:j+1])
            i = j+1
            continue
        if c.isdigit() or (c == '.' and i + 1 < len(expr) and expr[i + 1].isdigit()):
            j = i
            dot = False
            while j < len(expr) and (expr[j].isdigit() or (expr[j] == '.' and not dot)):
                if expr[j] == '.':
                    dot = True
                j += 1
            tokens.append(expr[i:j])
            i = j
            continue
        if c.isalpha() or c == '_':
            j = i
            while j < len(expr) and (expr[j].isalnum() or expr[j] == '_'):
                j += 1
            tokens.append(expr[i:j])
            i = j
            continue
        return None
    return tokens
