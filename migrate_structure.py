#!/usr/bin/env python3
"""
Restructure hausalang to proper package layout.

Current: Desktop/hausalang/
         ├── core/      (should be inside hausalang/)
         ├── hausalang/
         │   └── repl/

Target:  Desktop/hausalang/
         └── hausalang/        (Python package)
             ├── __init__.py
             ├── core/
             ├── repl/
"""
import shutil
from pathlib import Path

PROJECT_ROOT = Path("c:/Users/Nura Abdulkareem/Desktop/hausalang")
CORE_SRC = PROJECT_ROOT / "core"
CORE_DST = PROJECT_ROOT / "hausalang" / "core"
TESTS_DIR = PROJECT_ROOT / "tests"

print("=" * 60)
print("RESTRUCTURING HAUSALANG PACKAGE")
print("=" * 60)

# Step 1: Check if core exists at root
if CORE_SRC.exists():
    print(f"\n[1] Found {CORE_SRC}")

    # Step 2: Check if destination exists
    if CORE_DST.exists():
        print(f"[!] {CORE_DST} already exists, skipping copy")
    else:
        print(f"[2] Copying {CORE_SRC} → {CORE_DST}")
        shutil.copytree(CORE_SRC, CORE_DST, dirs_exist_ok=True)
        print("    ✓ Copy complete")
else:
    print(f"[!] {CORE_SRC} not found")

# Step 3: Check hausalang/__init__.py
init_file = PROJECT_ROOT / "hausalang" / "__init__.py"
if init_file.exists():
    print(f"\n[3] {init_file} exists")
else:
    print(f"[3] Creating {init_file}")
    init_file.write_text(
        '"""Hausalang - A custom educational programming language in Python."""\n\n__version__ = "1.1"\n'
    )
    print("    ✓ Created")

# Step 4: Check hausalang/core/__init__.py
core_init = PROJECT_ROOT / "hausalang" / "core" / "__init__.py"
if core_init.exists():
    print(f"\n[4] {core_init} exists")
else:
    print(f"[4] Creating {core_init}")
    core_init.parent.mkdir(parents=True, exist_ok=True)
    core_init.write_text("")
    print("    ✓ Created")

# Step 5: Check hausalang/repl/__init__.py
repl_init = PROJECT_ROOT / "hausalang" / "repl" / "__init__.py"
if repl_init.exists():
    print(f"\n[5] {repl_init} exists")
else:
    print(f"[5] Creating {repl_init}")
    repl_init.parent.mkdir(parents=True, exist_ok=True)
    repl_init.write_text('"""REPL module for Hausalang interactive environment."""\n')
    print("    ✓ Created")

print("\n" + "=" * 60)
print("RESTRUCTURING COMPLETE")
print("=" * 60)
print("\nNext steps:")
print("1. cd c:\\Users\\Nura\\ Abdulkareem\\Desktop\\hausalang")
print("2. pip install -e .")
print("3. pytest -x -vv")
