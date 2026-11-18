#!/usr/bin/env python3
"""Print a feature spec's revision ID.

The ID is a hash of the spec's design content. It ignores the Status and Last
updated header lines, the Approval section and the Changelog, so recording an
approval or changing the status line keeps the same ID, while any edit to intent,
scope, job stories, rules, examples, states, parameters, terms or the other
sections gives a new one. Whitespace at line ends and extra blank lines are ignored.

Usage:
    python3 spec_rev.py specs/features/F001-daily-gift/spec.md
    python3 spec_rev.py spec.md --rules        # one ID per rule, as JSON
"""
import argparse
import hashlib
import json
import sys

import specdoc


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("--rules", action="store_true", help="print one ID per rule as JSON")
    args = ap.parse_args(argv)
    try:
        text = specdoc.read(args.spec)
    except OSError as e:
        print(f"spec_rev: {e}", file=sys.stderr)
        return 2
    if args.rules:
        out = {rid: hashlib.sha256(block.encode()).hexdigest()[:12]
               for rid, block in specdoc.rule_blocks(text).items()}
        print(json.dumps(out, indent=2))
    else:
        print(specdoc.revision(text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
