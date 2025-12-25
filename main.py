import sys
from core.interpreter import run


def main():
    if len(sys.argv) < 2:
        print("Kuskure: Babu fayil da aka bayar")
        return

    filename = sys.argv[1]

    if not filename.endswith(".ha"):
        print("Kuskure: Fayil dole ya kasance .ha")
        return

    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()
            run(code)
    except FileNotFoundError:
        print("Kuskure: Ba a samu fayil ba")
        return


if __name__ == "__main__":
    main()
