# Copyright (c) 2026 NyxeraLabs
# Author: José María Micoli
# Licensed under BSL 1.1
# Change Date: 2033-02-17 → Apache-2.0
#
# You may:
# ✔ Study
# ✔ Modify
# ✔ Use for internal security testing
#
# You may NOT:
# ✘ Offer as a commercial service
# ✘ Sell derived competing products

from __future__ import annotations

from pathlib import Path
import py_compile
import sys


ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIRS = ("src", "internal", "web", "frontend", "tests", "scripts", ".github")
TEXT_SUFFIXES = {".py", ".sh", ".md", ".yml", ".yaml", ".ts", ".tsx", ".js", ".mjs", ".d.ts"}
IGNORED_PARTS = {"__pycache__", "node_modules", ".next", "dist", "build"}


def iter_files() -> list[Path]:
    files: list[Path] = []
    for relative in SOURCE_DIRS:
        base = ROOT / relative
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and not any(part in IGNORED_PARTS for part in path.parts):
                files.append(path)
    return sorted(files)


def check_text_hygiene(path: Path) -> list[str]:
    if path.suffix not in TEXT_SUFFIXES:
        return []
    errors: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.rstrip(" ") != line:
            errors.append(f"{path}: line {line_number} has trailing spaces")
        if "\t" in line:
            errors.append(f"{path}: line {line_number} contains tab indentation")
    return errors


def check_python_syntax(path: Path) -> list[str]:
    if path.suffix != ".py":
        return []
    try:
        py_compile.compile(str(path), doraise=True)
    except py_compile.PyCompileError as exc:
        return [f"{path}: python syntax check failed: {exc.msg}"]
    return []


def main() -> int:
    failures: list[str] = []
    for path in iter_files():
        failures.extend(check_text_hygiene(path))
        failures.extend(check_python_syntax(path))

    if failures:
        for failure in failures:
            print(failure)
        return 1

    print("Repository lint checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
