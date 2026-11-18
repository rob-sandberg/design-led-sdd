#!/usr/bin/env python3
"""Make sure CLAUDE.md points to AGENTS.md exactly once.

Adds `@AGENTS.md` as the first line if no line is exactly that, removes any extra
copies, and keeps every other line as it was. Creates CLAUDE.md if it is missing.
Running it twice changes nothing the second time.

Usage (from the project root):
    python3 pointer.py            # fix CLAUDE.md
    python3 pointer.py --check    # report only; exit 1 if a fix is needed
"""
import argparse
import sys
from pathlib import Path

POINTER = "@AGENTS.md"


def fixed(text):
    lines = text.splitlines()
    out, seen = [], False
    for l in lines:
        if l.strip() == POINTER:
            if seen:
                continue
            seen = True
            out.append(POINTER)
        else:
            out.append(l)
    if not seen:
        out = [POINTER, ""] + out if out else [POINTER]
    return "\n".join(out).rstrip("\n") + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    path = Path(a.root) / "CLAUDE.md"
    before = path.read_text(encoding="utf-8") if path.exists() else ""
    after = fixed(before)
    if before == after:
        print("CLAUDE.md already points to AGENTS.md once")
        return 0
    if a.check:
        print("CLAUDE.md needs the pointer fixed")
        return 1
    path.write_text(after, encoding="utf-8")
    print("CLAUDE.md now points to AGENTS.md once" + (" (created)" if not before else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
