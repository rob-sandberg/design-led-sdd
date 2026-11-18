#!/usr/bin/env python3
"""What changed in a spec since a commit, and which stories it touches.

Compares the spec on disk with the same file at a git commit (the one the
approval recorded) and sorts the change into one of three kinds:

  none     no design change (status, dates, approval or changelog only)
  tuning   only rows of the Parameters table changed
  rule     anything else: rules, examples, scope, states, job stories, terms...

A tuning change keeps approval only when no acceptance criterion depends on the
old value and no other feature relies on it; this script lists the stories that
name a changed parameter so that can be checked. A rule change ends approval.

Usage (from the project root):
    python3 spec_diff.py specs/features/F001-daily-gift/spec.md --since abc1234
    python3 spec_diff.py ... --since abc1234 --tasks specs/features/F001-daily-gift/tasks.md
    python3 spec_diff.py ... --since abc1234 --test-plan specs/features/F001-daily-gift/test-plan.md
    python3 spec_diff.py ... --old old-spec.md        (compare two files, no git)
    ... --json
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import specdoc


def old_text(spec, since):
    spec = Path(spec).resolve()
    top = subprocess.run(["git", "-C", str(spec.parent), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, check=True).stdout.strip()
    rel = spec.relative_to(top).as_posix()
    return subprocess.run(["git", "-C", top, "show", f"{since}:{rel}"],
                          capture_output=True, text=True, check=True).stdout


def section_map(text):
    out = {}
    for title, body in specdoc.sections(text, 2):
        key = (title or "(header)")
        if key.lower().startswith(specdoc.EXCLUDED_SECTIONS):
            continue
        # the header keeps its own exclusions (status and dates); sections are compared whole
        prefix = "" if title is None else "## x\n"
        out[key] = specdoc.normalise_for_revision(prefix + "\n".join(body))
    return out


def param_rows(text):
    rows = {}
    for t in specdoc.tables(specdoc.section(text, "Parameters")):
        i = specdoc.col(t, "Name")
        for r in t["rows"]:
            rows[specdoc.cell(r, i).strip("`")] = " | ".join(r)
    return rows


def compare(old, new):
    so, sn = section_map(old), section_map(new)
    changed_sections = sorted(k for k in set(so) | set(sn) if so.get(k) != sn.get(k))
    ro, rn = specdoc.rule_blocks(old), specdoc.rule_blocks(new)
    rules = {
        "added": sorted(set(rn) - set(ro)),
        "removed": sorted(set(ro) - set(rn)),
        "changed": sorted(k for k in set(ro) & set(rn) if ro[k] != rn[k]),
    }
    po, pn = param_rows(old), param_rows(new)
    params = sorted(k for k in set(po) | set(pn) if po.get(k) != pn.get(k))
    header_only = [s for s in changed_sections if s == "(header)"]
    design = [s for s in changed_sections if s != "(header)"]
    if specdoc.revision(old) == specdoc.revision(new):
        kind = "none"
    elif design == ["Parameters"] and not header_only:
        kind = "tuning"
    else:
        kind = "rule"
    return {"kind": kind, "sections": design + header_only, "rules": rules, "parameters": params,
            "old_revision": specdoc.revision(old), "new_revision": specdoc.revision(new)}


def affected_stories(tasks_text, result):
    names = set(result["rules"]["added"] + result["rules"]["removed"] + result["rules"]["changed"])
    params = set(result["parameters"])
    hits = []
    for title, body in specdoc.sections(tasks_text, 2):
        if not title or not title.lower().startswith("story"):
            continue
        sid = title.split(":")[0].replace("Story", "").strip()
        text = "\n".join(body)
        why = sorted(n for n in names if re.search(rf"\b{re.escape(n)}\b", text))
        why += sorted(f"parameter {p}" for p in params if p and re.search(rf"\b{re.escape(p)}\b", text))
        status = next((l.split("**Status:**")[1].strip() for l in body if "**Status:**" in l), "")
        if why:
            hits.append({"story": sid, "because": why, "status": status})
    return hits


def affected_cases(plan_text, result):
    """Test-plan cases whose Rule is a changed rule, or whose row names a changed parameter."""
    names = set(result["rules"]["added"] + result["rules"]["removed"] + result["rules"]["changed"])
    params = set(result["parameters"])
    hits = []
    for t in specdoc.tables(specdoc.section(plan_text, "Cases")):
        i_case, i_rule = specdoc.col(t, "Case"), specdoc.col(t, "Rule")
        if i_case is None:
            continue
        for r in t["rows"]:
            rule = specdoc.cell(r, i_rule)
            row = " ".join(r)
            why = [rule] if rule in names else []
            why += [f"parameter {p}" for p in params if p and re.search(rf"\b{re.escape(p)}\b", row)]
            if why:
                hits.append({"case": specdoc.cell(r, i_case), "because": why})
    return hits


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--since", help="git commit the approval recorded")
    src.add_argument("--old", help="an older copy of the spec")
    ap.add_argument("--tasks", help="tasks.md to check for affected stories")
    ap.add_argument("--test-plan", help="test-plan.md to check for affected cases")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        new = specdoc.read(a.spec)
        old = specdoc.read(a.old) if a.old else old_text(a.spec, a.since)
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"spec_diff: could not read the older spec: {e}", file=sys.stderr)
        return 2
    res = compare(old, new)
    if a.tasks and Path(a.tasks).exists():
        res["stories"] = affected_stories(specdoc.read(a.tasks), res)
    if a.test_plan and Path(a.test_plan).exists():
        res["cases"] = affected_cases(specdoc.read(a.test_plan), res)
    if a.json:
        print(json.dumps(res, indent=2))
        return 0
    print(f"Change: {res['kind']} ({res['old_revision']} to {res['new_revision']})")
    if res["sections"]:
        print("Sections changed: " + ", ".join(res["sections"]))
    for k in ("added", "removed", "changed"):
        if res["rules"][k]:
            print(f"Rules {k}: " + ", ".join(res["rules"][k]))
    if res["parameters"]:
        print("Parameters changed: " + ", ".join(res["parameters"]))
    for s in res.get("stories", []):
        print(f"Story {s['story']} ({s['status'] or 'no status'}): " + ", ".join(s["because"]))
    for c in res.get("cases", []):
        print(f"Case {c['case']}: " + ", ".join(c["because"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
