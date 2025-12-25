from core.executor import execute
from core.lexer import tokenize_expr, strip_comments
import re
from copy import deepcopy


def hus_err(ha, en):
    print(f"{ha} ({en})")


def is_valid_name(name):
    return re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name) is not None


def parse_literal(token, variables):
    s = token.strip()

    # string literal
    if s.startswith('"') and s.endswith('"') and len(s) >= 2:
        return s[1:-1]

    # tokenizer for arithmetic expressions and quoted strings
    def tokenize(expr):
        tokens = []
        i = 0
        while i < len(expr):
            c = expr[i]
            if c.isspace():
                i += 1
                continue
            if c in "+-*/()":
                tokens.append(c)
                i += 1
                continue
            # quoted string
            if c == '"':
                j = i + 1
                while j < len(expr):
                    if expr[j] == '"' and expr[j - 1] != "\\":
                        break
                    j += 1
                if j >= len(expr):
                    return None
                tokens.append(expr[i : j + 1])
                i = j + 1
                continue
            # number
            if c.isdigit() or (
                c == "." and i + 1 < len(expr) and expr[i + 1].isdigit()
            ):
                j = i
                dot = False
                while j < len(expr) and (
                    expr[j].isdigit() or (expr[j] == "." and not dot)
                ):
                    if expr[j] == ".":
                        dot = True
                    j += 1
                tokens.append(expr[i:j])
                i = j
                continue
            # identifier
            if c.isalpha() or c == "_":
                j = i
                while j < len(expr) and (expr[j].isalnum() or expr[j] == "_"):
                    j += 1
                tokens.append(expr[i:j])
                i = j
                continue
            # unknown
            return None
        return tokens

    def to_postfix(tokens):
        prec = {"+": 1, "-": 1, "*": 2, "/": 2}
        output = []
        ops = []
        for t in tokens:
            if re.match(r"^-?\d+(?:\.\d+)?$", t):
                output.append(t)
            elif re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", t):
                output.append(t)
            elif t.startswith('"') and t.endswith('"'):
                output.append(t)
            elif t in prec:
                while ops and ops[-1] in prec and prec[ops[-1]] >= prec[t]:
                    output.append(ops.pop())
                ops.append(t)
            elif t == "(":
                ops.append(t)
            elif t == ")":
                while ops and ops[-1] != "(":
                    output.append(ops.pop())
                if not ops or ops[-1] != "(":
                    return None
                ops.pop()
            else:
                return None
        while ops:
            if ops[-1] in "()":
                return None
            output.append(ops.pop())
        return output

    def eval_postfix(postfix):
        stack = []
        for t in postfix:
            if re.match(r"^-?\d+$", t):
                stack.append(int(t))
            elif re.match(r"^-?\d+\.\d+$", t):
                stack.append(float(t))
            elif t.startswith('"') and t.endswith('"'):
                stack.append(t[1:-1])
            elif re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", t):
                if t in variables:
                    stack.append(variables[t])
                else:
                    return None
            elif t in ("+", "-", "*", "/"):
                if len(stack) < 2:
                    return None
                b = stack.pop()
                a = stack.pop()
                try:
                    if t == "+":
                        # allow string concatenation with non-strings
                        if isinstance(a, str) or isinstance(b, str):
                            stack.append(str(a) + str(b))
                        else:
                            stack.append(a + b)
                    elif t == "-":
                        stack.append(a - b)
                    elif t == "*":
                        # allow string repetition when multiplied by int
                        if isinstance(a, str) and isinstance(b, int):
                            stack.append(a * b)
                        elif isinstance(b, str) and isinstance(a, int):
                            stack.append(b * a)
                        else:
                            stack.append(a * b)
                    elif t == "/":
                        stack.append(a / b)
                except Exception:
                    return None
            else:
                return None
        if len(stack) != 1:
            return None
        return stack[0]

    tokens = tokenize(s)
    if tokens is None:
        return None

    if len(tokens) == 1:
        t = tokens[0]
        if re.match(r"^-?\d+$", t):
            return int(t)
        if re.match(r"^-?\d+\.\d+$", t):
            return float(t)
        if t in variables:
            return variables[t]
        return None

    postfix = to_postfix(tokens)
    if postfix is None:
        return None
    return eval_postfix(postfix)


def compare_values(left, op, right):
    try:
        if op == "==":
            return left == right
        if op == "!=":
            return left != right
        if op == ">":
            return left > right
        if op == "<":
            return left < right
        if op == ">=":
            return left >= right
        if op == "<=":
            return left <= right
    except TypeError:
        return False
    return False


def run(code):
    lines = code.splitlines()
    variables = {}
    functions = {}

    # support nested blocks using a stack of dicts: {base_indent, condition, else_mode}
    blocks = []

    def run_block(block_lines, local_vars):
        # execute a list of lines in isolated local_vars; supports 'mayar' for return
        i = 0
        while i < len(block_lines):
            raw = block_lines[i].rstrip("\n\r")
            i += 1
            if raw.strip() == "":
                continue
            indent = len(raw) - len(raw.lstrip(" "))
            line = strip_comments(raw.lstrip(" "))

            # mayar (return)
            if line.startswith("mayar"):
                expr = line.replace("mayar", "", 1).strip()
                val = parse_literal(expr, local_vars)
                return val, True

            # assignment inside function
            if "=" in line and not line.startswith(("rubuta", "idan", "in ba haka ba")):
                name, value = line.split("=", 1)
                name = name.strip()
                value_s = value.strip()
                if not is_valid_name(name):
                    hus_err(
                        f"kuskure: sunan variable mara kyau -> {name}",
                        f"error: invalid variable name -> {name}",
                    )
                    continue
                # function calls in RHS
                m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\((.*)\)$", value_s)
                if m and m.group(1) in functions:
                    fname = m.group(1)
                    args_s = m.group(2).strip()
                    args = []
                    if args_s:
                        args = [a.strip() for a in args_s.split(",")]
                    # evaluate args
                    eval_args = []
                    for a in args:
                        av = parse_literal(a, local_vars)
                        eval_args.append(av)
                    # call
                    fdef = functions[fname]
                    params = fdef["params"]
                    if len(params) != len(eval_args):
                        hus_err(
                            f"kuskure: adadin hujjoji bai dace ba -> {fname}",
                            f"error: wrong arg count -> {fname}",
                        )
                        continue
                    new_loc = deepcopy(local_vars)
                    for p, v in zip(params, eval_args):
                        new_loc[p] = v
                    ret, did = run_block(fdef["body"], new_loc)
                    if did:
                        local_vars[name] = ret
                    else:
                        local_vars[name] = None
                    continue

                val = parse_literal(value_s, local_vars)
                if val is None:
                    hus_err(
                        f"kuskure: darajar ba ta da inganci -> {value_s}",
                        f"error: invalid value -> {value_s}",
                    )
                    continue
                local_vars[name] = val
                continue

            # simple execution lines
            # function call as statement
            m2 = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\((.*)\)$", line)
            if m2 and m2.group(1) in functions:
                fname = m2.group(1)
                args_s = m2.group(2).strip()
                args = []
                if args_s:
                    args = [a.strip() for a in args_s.split(",")]
                eval_args = []
                for a in args:
                    av = parse_literal(a, local_vars)
                    eval_args.append(av)
                fdef = functions[fname]
                params = fdef["params"]
                if len(params) != len(eval_args):
                    hus_err(
                        f"kuskure: adadin hujjoji bai dace ba -> {fname}",
                        f"error: wrong arg count -> {fname}",
                    )
                    continue
                new_loc = deepcopy(local_vars)
                for p, v in zip(params, eval_args):
                    new_loc[p] = v
                run_block(fdef["body"], new_loc)
                continue

            # determine if this line should run considering enclosing blocks
            should_run = True
            for b in blocks:
                if indent > b["base_indent"]:
                    cond = (not b["condition"]) if b["else_mode"] else b["condition"]
                    should_run = should_run and bool(cond)

            if should_run and line:
                execute(line, local_vars)

        return None, False

    i = 0
    while i < len(lines):
        raw = lines[i].rstrip("\n\r")
        i += 1
        if raw.strip() == "":
            continue

        indent = len(raw) - len(raw.lstrip(" "))
        line = strip_comments(raw.lstrip(" "))

        # pop blocks when leaving their indentation (unless it's an else-line which we'll handle)
        while (
            blocks
            and indent <= blocks[-1]["base_indent"]
            and not line.startswith("in ba haka ba")
        ):
            blocks.pop()

        # function definition: aiki name(param, ...):
        if line.startswith("aiki"):
            sig = line.replace("aiki", "", 1).strip()
            if not sig.endswith(":"):
                hus_err(
                    "kuskure: aiki dole ya kare da ':'",
                    "error: 'aiki' must end with ':'",
                )
                continue
            sig = sig[:-1].strip()
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\((.*)\)$", sig)
            if not m:
                hus_err(
                    "kuskure: sunan aiki mara kyau", "error: invalid function signature"
                )
                continue
            fname = m.group(1)
            params_s = m.group(2).strip()
            params = []
            if params_s:
                params = [p.strip() for p in params_s.split(",")]
            # capture body lines with greater indent
            body = []
            while i < len(lines):
                nxt = lines[i]
                nxt_indent = len(nxt) - len(nxt.lstrip(" "))
                if nxt.strip() == "":
                    i += 1
                    continue
                if nxt_indent <= indent:
                    break
                body.append(nxt[indent + 1 :] if len(nxt) > indent else nxt.lstrip(" "))
                i += 1
            functions[fname] = {"params": params, "body": body}
            continue

        # idan (if) and support explicit 'kuma' as elif
        if line.startswith("idan"):
            condition = line.replace("idan", "", 1).strip()
            if not condition.endswith(":"):
                hus_err(
                    "kuskure: idan dole ya kare da ':'",
                    "error: 'idan' must end with ':'",
                )
                continue
            condition = condition[:-1].strip()

            # detect explicit 'kuma' (elif)
            is_elif = False
            if re.search(r"\bkuma\b\s*$", condition):
                is_elif = True
                condition = re.sub(r"\bkuma\b\s*$", "", condition).strip()

            # find operator
            found = None
            two_char_ops = ["==", "!=", ">=", "<="]
            for o in two_char_ops:
                if o in condition:
                    found = o
                    break
            if not found:
                single_char_ops = [">", "<"]
                for o in single_char_ops:
                    if o in condition:
                        found = o
                        break

            if not found:
                hus_err(
                    "kuskure: idan yana bukatar ma'aunin kwatanci (==, !=, >, <, >=, <=)",
                    "error: 'idan' requires a comparison operator",
                )
                continue

            left_s, right_s = condition.split(found, 1)
            left_s = left_s.strip()
            right_s = right_s.strip()

            left = parse_literal(left_s, variables)
            right = parse_literal(right_s, variables)

            if left is None:
                hus_err(
                    f"kuskure: ba a san {left_s} ba", f"error: unknown value {left_s}"
                )
                continue

            if right is None:
                hus_err(
                    f"kuskure: ba a san {right_s} ba", f"error: unknown value {right_s}"
                )
                continue

            cond = compare_values(left, found, right)

            if is_elif and blocks and indent == blocks[-1]["base_indent"]:
                # explicit elif replaces previous block
                blocks.pop()

            blocks.append(
                {"base_indent": indent, "condition": cond, "else_mode": False}
            )
            continue

        if line.startswith("in ba haka ba"):
            if not line.endswith(":"):
                hus_err(
                    "kuskure: 'in ba haka ba' dole ya kare da ':'",
                    "error: 'in ba haka ba' must end with ':'",
                )
                continue
            if not blocks:
                hus_err(
                    "kuskure: 'in ba haka ba' bai da idan kafin sa",
                    "error: 'else' without matching 'if'",
                )
                continue
            blocks[-1]["else_mode"] = True
            continue

        # assignment
        if "=" in line and not line.startswith(("rubuta", "idan", "in ba haka ba")):
            name, value = line.split("=", 1)
            name = name.strip()
            value_s = value.strip()

            if not is_valid_name(name):
                hus_err(
                    f"kuskure: sunan variable mara kyau -> {name}",
                    f"error: invalid variable name -> {name}",
                )
                continue

            # function call in RHS
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\((.*)\)$", value_s)
            if m and m.group(1) in functions:
                fname = m.group(1)
                args_s = m.group(2).strip()
                args = []
                if args_s:
                    args = [a.strip() for a in args_s.split(",")]
                eval_args = []
                for a in args:
                    av = parse_literal(a, variables)
                    eval_args.append(av)
                fdef = functions[fname]
                params = fdef["params"]
                if len(params) != len(eval_args):
                    hus_err(
                        f"kuskure: adadin hujjoji bai dace ba -> {fname}",
                        f"error: wrong arg count -> {fname}",
                    )
                    continue
                new_loc = deepcopy(variables)
                for p, v in zip(params, eval_args):
                    new_loc[p] = v
                ret, did = run_block(fdef["body"], new_loc)
                if did:
                    variables[name] = ret
                else:
                    variables[name] = None
                continue

            val = parse_literal(value_s, variables)
            if val is None:
                hus_err(
                    f"kuskure: darajar ba ta da inganci -> {value_s}",
                    f"error: invalid value -> {value_s}",
                )
                continue

            variables[name] = val
            continue

        # execution: determine if all enclosing blocks allow execution
        should_run = True
        for b in blocks:
            # a block affects lines with greater indent than its base
            if indent > b["base_indent"]:
                cond = (not b["condition"]) if b["else_mode"] else b["condition"]
                should_run = should_run and bool(cond)

        if should_run and line:
            # function call as statement
            m2 = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\((.*)\)$", line)
            if m2 and m2.group(1) in functions:
                fname = m2.group(1)
                args_s = m2.group(2).strip()
                args = []
                if args_s:
                    args = [a.strip() for a in args_s.split(",")]
                eval_args = []
                for a in args:
                    av = parse_literal(a, variables)
                    eval_args.append(av)
                fdef = functions[fname]
                params = fdef["params"]
                if len(params) != len(eval_args):
                    hus_err(
                        f"kuskure: adadin hujjoji bai dace ba -> {fname}",
                        f"error: wrong arg count -> {fname}",
                    )
                else:
                    new_loc = deepcopy(variables)
                    for p, v in zip(params, eval_args):
                        new_loc[p] = v
                    run_block(fdef["body"], new_loc)
                continue
            execute(line, variables)
