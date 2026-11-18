#!/usr/bin/env python3
"""The project's open-questions register: where it is, what is open, safe imports.

The constitution names the register in its "Open questions register" section:

    ## Open questions register

    - Master: `specs/open-questions.md`
    - Mode: local
    - Legacy source: none

Mode `local` means the Master file is the register. Mode `legacy` means another
document is the master and the Master line names it (a path or a URL); if it is
not a Markdown file in the method's format, skills read it themselves and pass its
rows to ready_check.py with --register-rows. With no such section, the register is
`specs/open-questions.md` in local mode.

Usage (run from the project root):
    python3 register.py where
    python3 register.py list --feature F003 [--open]
    python3 register.py next-id --feature F003
    python3 register.py merge --rows rows.tsv --source "mechanics doc §9"
    python3 register.py check

Rows files are tab-separated with a header line naming at least ID and Question;
the other columns used are Proposal, Owner, Blocking, Raised, Spec and Was.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

import specdoc

DEFAULT = "specs/open-questions.md"
COLUMNS = ["ID", "Question", "Proposal", "Owner", "Blocking", "Raised", "Spec", "Was"]


def project_root(start="."):
    p = Path(start).resolve()
    for cand in [p, *p.parents]:
        if (cand / "specs" / "constitution.md").exists() or (cand / "specs").is_dir():
            return cand
    return p


def where(root):
    """{'master', 'mode', 'legacy', 'source'} from the constitution, else the default."""
    con = Path(root) / "specs" / "constitution.md"
    info = {"master": DEFAULT, "mode": "local", "legacy": "none", "source": "default"}
    if not con.exists():
        return info
    body = specdoc.section(specdoc.read(con), "Open questions register")
    if body is None:
        return info
    f = specdoc.bullet_fields(body)
    master = f.get("master", "").strip().strip("`")
    if master:
        info["master"] = master
    info["mode"] = (f.get("mode", "local").split()[0].strip("`").lower() or "local")
    info["legacy"] = f.get("legacy source", "none") or "none"
    info["source"] = "constitution"
    return info


def blocking_value(text):
    t = (text or "").strip().lower()
    if t.startswith("yes"):
        return "yes"
    if t.startswith("no"):
        return "no"
    return "unknown"


def rows_from_markdown(text):
    """Every register row, with the level-2 section it sits in (Open, Resolved, Deferred)."""
    out = []
    for title, body in specdoc.sections(text, 2):
        status = (title or "").strip().split()[0].lower() if title else ""
        for t in specdoc.tables(body):
            i_id = specdoc.col(t, "ID")
            if i_id is None:
                continue
            idx = {c: specdoc.col(t, c) for c in COLUMNS}
            for r in t["rows"]:
                rid = specdoc.cell(r, i_id)
                if not re.match(r"^OQ-", rid):
                    continue
                row = {c: specdoc.cell(r, idx[c]) for c in COLUMNS}
                row["ID"] = rid
                row["section"] = status
                out.append(row)
    return out


def rows_from_tsv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        rows = []
        for r in reader:
            norm = {k.strip().title() if k.strip().lower() != "id" else "ID": (v or "").strip() for k, v in r.items() if k}
            row = {c: norm.get(c, "") for c in COLUMNS}
            row["section"] = (norm.get("Status", "") or "open").lower()
            rows.append(row)
        return rows


def relevant(row, fid):
    return bool(fid) and (f"-{fid}-" in row["ID"] or re.search(rf"\b{fid}\b", row.get("Spec", "")))


def load(root, rows_file=None):
    """(rows, info, error). error is a sentence when the authoritative register cannot be read."""
    info = where(root)
    if rows_file:
        return rows_from_tsv(rows_file), info, None
    master = info["master"]
    if re.match(r"^[a-z]+://", master):
        return [], info, f"the register's master is {master}; read it and pass its rows with --register-rows"
    path = Path(root) / master
    if not path.exists():
        return [], info, f"the register's master {master} does not exist"
    if path.suffix.lower() != ".md":
        return [], info, f"the register's master {master} is not a Markdown register; read it and pass its rows with --register-rows"
    return rows_from_markdown(specdoc.read(path)), info, None


def next_id(rows, fid):
    nums = [int(m.group(1)) for r in rows for m in [re.match(rf"OQ-{fid}-(\d{{3}})$", r["ID"])] if m]
    return f"OQ-{fid}-{(max(nums) if nums else 0) + 1:03d}"


def merge(path, new_rows, source, dry=False):
    """Add rows whose ID is not already in the register, under '### Imported from <source>'
    in the Open section. Never changes or removes an existing row. Returns (added, skipped)."""
    text = specdoc.read(path) if Path(path).exists() else "# Open questions\n\n## Open\n\n## Resolved\n\n## Deferred\n"
    have = {r["ID"] for r in rows_from_markdown(text)}
    add, seen = [], set()
    for r in new_rows:
        if not r["ID"] or r["ID"] in have or r["ID"] in seen:
            continue
        seen.add(r["ID"])
        add.append(r)
    skipped = len(new_rows) - len(add)
    if not add or dry:
        return len(add), skipped
    heading = f"### Imported from {source}"
    head = "| " + " | ".join(COLUMNS) + " |"
    sep = "| " + " | ".join("---" for _ in COLUMNS) + " |"

    def fmt(r):
        vals = [(r.get(c) or "").replace("|", "/") for c in COLUMNS]
        if not vals[COLUMNS.index("Blocking")]:
            vals[COLUMNS.index("Blocking")] = "?"
        return "| " + " | ".join(vals) + " |"

    lines = text.splitlines()
    if heading in lines:
        # append after the last table row of the existing import block
        i = lines.index(heading) + 1
        last = i
        while i < len(lines) and not lines[i].startswith("#"):
            if lines[i].startswith("|"):
                last = i
            i += 1
        lines[last + 1:last + 1] = [fmt(r) for r in add]
    else:
        try:
            j = next(k for k, l in enumerate(lines) if re.match(r"^##\s+(Resolved|Deferred)\b", l))
        except StopIteration:
            j = len(lines)
        block = [heading, "", head, sep, *[fmt(r) for r in add], ""]
        lines[j:j] = block
    # read first, then write: never open the file for writing while reading it
    new_text = "\n".join(lines) + "\n"
    Path(path).write_text(new_text, encoding="utf-8")
    return len(add), skipped


def check(rows):
    problems = []
    ids = [r["ID"] for r in rows]
    for rid in sorted({i for i in ids if ids.count(i) > 1}):
        problems.append(f"{rid} appears {ids.count(rid)} times")
    for r in rows:
        if r["section"] == "open" and blocking_value(r["Blocking"]) == "unknown":
            problems.append(f"{r['ID']} is open with no Blocking value (Yes or No): triage it")
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["where", "list", "next-id", "merge", "check"])
    ap.add_argument("--root", default=".")
    ap.add_argument("--feature")
    ap.add_argument("--open", action="store_true")
    ap.add_argument("--rows", help="tab-separated rows to merge")
    ap.add_argument("--source", default="an earlier register")
    ap.add_argument("--register-rows", help="rows exported from a legacy master, tab-separated")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    root = project_root(a.root)

    if a.command == "where":
        info = where(root)
        print(json.dumps(info, indent=2) if a.json else f"{info['master']} ({info['mode']}, from {info['source']})")
        return 0

    rows, info, err = load(root, a.register_rows)
    if a.command == "merge":
        if info["mode"] != "local" and not a.register_rows:
            print(f"register: the master is {info['master']} (legacy). Add the rows there, or switch the "
                  "constitution to local mode first.", file=sys.stderr)
            return 1
        if not a.rows:
            print("register: merge needs --rows", file=sys.stderr)
            return 2
        added, skipped = merge(Path(root) / info["master"], rows_from_tsv(a.rows), a.source, a.dry_run)
        print(f"added {added}, already present {skipped}" + (" (dry run)" if a.dry_run else ""))
        return 0
    if err:
        print(f"register: {err}", file=sys.stderr)
        return 1
    if a.command == "list":
        sel = [r for r in rows if (not a.feature or relevant(r, a.feature)) and (not a.open or r["section"] == "open")]
        if a.json:
            print(json.dumps(sel, indent=2))
        else:
            for r in sel:
                print(f"{r['ID']}\t{r['section']}\tblocking={blocking_value(r['Blocking'])}\t{r['Question'][:80]}")
        return 0
    if a.command == "next-id":
        if not a.feature:
            print("register: next-id needs --feature", file=sys.stderr)
            return 2
        print(next_id(rows, a.feature))
        return 0
    if a.command == "check":
        probs = check(rows)
        for p in probs:
            print(p)
        print(f"{len(rows)} rows, {len(probs)} problems")
        return 1 if probs else 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
