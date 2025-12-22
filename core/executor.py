def hus_err(ha, en):
    print(f"{ha} ({en})")


def execute(line, variables):
    # =============================
    # rubuta (print)
    # =============================
    if line.startswith("rubuta"):
        content = line.replace("rubuta", "", 1).strip()

        if content.startswith('"') and content.endswith('"'):
            print(content[1:-1])
            return

        if content in variables:
            print(variables[content])
            return

        # try to parse a number literal
        try:
            if content.isdigit() or (content.startswith('-') and content[1:].isdigit()):
                print(int(content))
                return
            # float
            float_val = float(content)
            print(float_val)
            return
        except Exception:
            hus_err("kuskure: rubuta yana bukatar rubutu ko variable", "error: 'rubuta' needs a string or a variable")
            return

    # =============================
    # Unknown command
    # =============================
    hus_err(f"kuskure: ban gane umarnin ba -> {line}", f"error: unknown command -> {line}")
