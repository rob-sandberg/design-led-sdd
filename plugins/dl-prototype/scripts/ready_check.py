#!/usr/bin/env python3
"""The Ready check: one gate, the same from every skill.

Stages:
  approve  Before the designer is asked to approve: every prerequisite passes.
  ticket   Before tasks writes or posts tickets: the prerequisites still pass, and
           the designer's approval names the current spec revision and the latest report.
  story    (with --story S1) A story may be ticketed or built: the ticket stage passes
           and the story is marked Ready against the current spec revision.

Exit 0 when the gate passes, 1 when it does not, 2 on a usage error.

Usage (from the project root):
    python3 ready_check.py specs/features/F001-daily-gift --stage approve
    python3 ready_check.py specs/features/F001-daily-gift --stage ticket
    python3 ready_check.py specs/features/F001-daily-gift --story S1
    ... --register-rows legacy.tsv   when the register's master is not a Markdown file
    ... --json
"""
import argparse
import json
import re
import sys
from pathlib import Path

import register
import specdoc

PLACEHOLDER = re.compile(r"^\s*\[.*\]\s*\.?\s*$")


class Gate:
    def __init__(self):
        self.fails, self.warns, self.notes = [], [], []

    def fail(self, msg):
        self.fails.append(msg)

    def warn(self, msg):
        self.warns.append(msg)

    def note(self, msg):
        self.notes.append(msg)


def has_content(lines):
    real = [l for l in (lines or []) if l.strip() and not PLACEHOLDER.match(l.strip("-* "))]
    return bool(real)


def check_sections(text, g):
    for name in ("Intent", "Player experience", "Scope"):
        body = specdoc.section(text, name)
        if body is None:
            g.fail(f"the spec has no {name} section")
        elif not has_content(body):
            g.fail(f"the spec's {name} section is empty or still the template text")


def check_rules(text, g):
    blocks = specdoc.rule_blocks(text)
    if not blocks:
        g.fail("the spec has no rules with an ID (### F<NNN>.<id>: ...)")
        return
    for rid, block in blocks.items():
        lines = block.splitlines()
        if not any(re.match(r"^\s*Otherwise\b", l) for l in lines):
            g.fail(f"{rid} has no Otherwise")
        tabs = [t for t in specdoc.tables(lines) if t["rows"]]
        if not tabs:
            g.fail(f"{rid} has no examples table")
            continue
        t = tabs[0]
        if len(t["rows"]) < 2:
            g.fail(f"{rid} has fewer than two examples")
        i = specdoc.col(t, "provided")
        if i is not None:
            vals = {specdoc.cell(r, i).lower().split(" ")[0].strip(".,") for r in t["rows"]}
            if not ({"yes", "no"} <= vals):
                g.fail(f"{rid}'s examples cover only one side of the guard")


def check_terms(text, specs_root, g):
    body = specdoc.section(text, "Terms")
    terms = []
    for t in specdoc.tables(body):
        i = specdoc.col(t, "Term")
        terms += [specdoc.cell(r, i) for r in t["rows"] if specdoc.cell(r, i) and not specdoc.cell(r, i).startswith("[")]
    if not terms:
        return
    gpath = specs_root / "glossary.md" if specs_root else None
    if not gpath or not gpath.exists():
        g.fail("the spec defines terms but the project has no glossary.md")
        return
    known = set()
    for t in specdoc.tables(specdoc.read(gpath).splitlines()):
        for r in t["rows"]:
            for c in r[:2]:
                known.add(c.strip().strip("`*").lower())
    for term in terms:
        if term.strip("`*").lower() not in known:
            g.fail(f"term \"{term}\" is not in the glossary")


def check_register(root, fid, text, rows_file, g):
    rows, info, err = register.load(root, rows_file)
    if err:
        g.fail(f"cannot verify open questions: {err}")
        return
    g.note(f"register: {info['master']} ({info['mode']})")
    by_id = {r["ID"]: r for r in rows}
    for r in rows:
        if r["section"] != "open" or not register.relevant(r, fid):
            continue
        b = register.blocking_value(r["Blocking"])
        if b == "yes":
            g.fail(f"{r['ID']} is open and blocking")
        elif b == "unknown":
            g.fail(f"{r['ID']} is open with no Blocking value: triage it (Yes or No)")
        else:
            g.note(f"{r['ID']} is open, not blocking")
    for n, line in specdoc.undecided_lines(text):
        ids = specdoc.OQ_ID.findall(line)
        if not ids:
            g.warn(f"line {n} has a ? with no open-question ID: {line[:70]}")
            continue
        for qid in ids:
            r = by_id.get(qid)
            if r is None:
                g.fail(f"line {n} cites {qid}, which is not in the register")
            elif r["section"] == "open" and register.blocking_value(r["Blocking"]) != "no":
                g.fail(f"line {n} is undecided and waits on {qid}")


def report_fields(text):
    return specdoc.header_fields(text)


def carried_from(text):
    """The revision an approval was carried over from after a tuning-only change, else None."""
    ap = specdoc.bullet_fields(specdoc.section(text, "Approval"))
    m = re.search(r"(rev-[0-9a-f]{12})", ap.get("carried over", ""))
    approved = (ap.get("revision") or "").split()
    # a carry-over only counts for the revision it was recorded against
    if not m or not approved or approved[0] != specdoc.revision(text):
        return None
    return m.group(1)


def verify_carry(spec_path, text, g):
    """When the approval carries over a tuning change and names a commit, check the change
    since that commit really is parameters only."""
    ap = specdoc.bullet_fields(specdoc.section(text, "Approval"))
    commit = (ap.get("commit") or "").split()[0] if ap.get("commit") else ""
    if not re.fullmatch(r"[0-9a-f]{7,40}", commit):
        g.warn("the approval was carried over after tuning, but names no commit, so the change could not be verified")
        return
    try:
        import spec_diff
        res = spec_diff.compare(spec_diff.old_text(spec_path, commit), text)
    except Exception as e:  # git missing, commit unknown
        g.warn(f"could not verify the carried-over approval against {commit}: {e}")
        return
    if res["kind"] == "rule":
        g.fail(f"the approval was carried over as tuning, but rules or other sections changed since {commit}: "
               + ", ".join(res["sections"]))


def check_analysis(folder, text, specs_root, g, allow_from=None):
    reps = specdoc.reports(folder)
    current = specdoc.revision(text)
    if not reps:
        g.fail("no analysis report: run analyze on this revision")
        return None
    latest = reps[-1]
    rtext = specdoc.read(latest)
    f = report_fields(rtext)
    g.note(f"latest analysis: {latest.name}")
    rev = (f.get("spec revision") or "").split()[0] if f.get("spec revision") else ""
    if not rev:
        g.fail(f"{latest.name} does not record the spec revision it reviewed: rerun analyze")
    elif rev != current and not (allow_from and rev == allow_from):
        g.fail(f"{latest.name} reviewed {rev}, but the spec is now {current}: rerun analyze on the current revision")
    elif rev != current:
        g.note(f"{latest.name} reviewed {rev}; the approval was carried over to {current} after a tuning-only change")
    # context: constitution and glossary as they were when the report was written
    ctx = f.get("context", "")
    for name in ("constitution", "glossary"):
        m = re.search(rf"{name}\s+(rev-[0-9a-f]{{12}})", ctx)
        p = specs_root / f"{name}.md" if specs_root else None
        if m and p and p.exists():
            now = specdoc.revision(specdoc.read(p))
            if now != m.group(1):
                g.fail(f"{name}.md has changed since {latest.name}: recheck the findings that rely on it")
    # findings and their dispositions
    findings = {}
    for t in specdoc.tables(specdoc.section(rtext, "Findings")):
        i_n, i_sev = specdoc.col(t, "#"), specdoc.col(t, "Severity")
        if i_n is None or i_sev is None:
            continue
        for r in t["rows"]:
            findings[specdoc.cell(r, i_n)] = specdoc.cell(r, i_sev).lower()
    disp = {}
    for t in specdoc.tables(specdoc.section(rtext, "Resolutions")):
        i_n = specdoc.col(t, "#")
        i_d = specdoc.col(t, "Disposition", "Resolution")
        i_r = specdoc.col(t, "Reason")
        i_by = specdoc.col(t, "Decided by")
        for r in t["rows"]:
            disp[specdoc.cell(r, i_n)] = (specdoc.cell(r, i_d).lower(), specdoc.cell(r, i_r), specdoc.cell(r, i_by))
    open_adv = 0
    for n, sev in findings.items():
        d, reason, by = disp.get(n, ("", "", ""))
        if sev.startswith("blocking"):
            if d.startswith("dismissed"):
                if not reason or not by:
                    g.fail(f"blocking finding {n} is dismissed without a reason and a named decision-maker")
            elif d.startswith("fixed"):
                g.fail(f"blocking finding {n} is marked fixed in the report that found it: rerun analyze on the edited spec")
            else:
                g.fail(f"blocking finding {n} in {latest.name} is unresolved")
        elif not d or d.startswith("open"):
            open_adv += 1
    if open_adv:
        g.note(f"{open_adv} advisory finding(s) left open, as allowed")
    return latest.name


def check_approval(text, latest_name, g):
    current = specdoc.revision(text)
    status = specdoc.header_fields(text).get("status", "")
    ap = specdoc.bullet_fields(specdoc.section(text, "Approval"))
    if not ap:
        g.fail("the spec has no Approval section")
        return
    ready = ap.get("ready", "").lower().startswith("yes")
    if not ready:
        if status.lower().startswith("ready"):
            g.fail("the status says Ready but the Approval section does not record the designer's approval")
        else:
            g.fail("the designer has not approved this spec as Ready")
        return
    if not ap.get("approved by"):
        g.fail("the approval names no approver")
    rev = (ap.get("revision") or "").split()[0] if ap.get("revision") else ""
    if rev != current:
        g.fail(f"the approval is for {rev or 'no revision'}, but the spec is now {current}: approval has lapsed")
    analysis = (ap.get("analysis") or "").strip("` ")
    if latest_name and analysis and Path(analysis).name != latest_name:
        g.fail(f"the approval cites {analysis}, but the latest report is {latest_name}")
    if rev == current and status.lower().startswith("draft"):
        g.warn("the status line still says Draft; update it to Ready")


def check_story(folder, text, story, g):
    tpath = Path(folder) / "tasks.md"
    if not tpath.exists():
        g.fail("no tasks.md")
        return
    ttext = specdoc.read(tpath)
    current = specdoc.revision(text)
    body = None
    for title, lines in specdoc.sections(ttext, 2):
        if title and re.match(rf"Story\s+{re.escape(story)}\b", title):
            body = lines
    if body is None:
        g.fail(f"tasks.md has no story {story}")
        return
    status = next((l for l in body if l.strip().startswith("**Status:**")), "")
    if "ready" not in status.lower():
        g.fail(f"story {story} is not marked Ready")
    elif current not in status:
        g.fail(f"story {story} was approved against another spec revision; the spec is now {current}")


def run(folder, stage="ticket", story=None, root=None, rows_file=None):
    folder = Path(folder)
    spec = folder / "spec.md"
    g = Gate()
    if not spec.exists():
        g.fail(f"{spec} does not exist")
        return g, None
    text = specdoc.read(spec)
    specs_root = specdoc.find_specs_root(folder)
    root = Path(root) if root else (specs_root.parent if specs_root and specs_root.name == "specs" else Path("."))
    fid = specdoc.feature_id(folder)
    g.note(f"spec revision: {specdoc.revision(text)}")
    check_sections(text, g)
    check_rules(text, g)
    check_terms(text, specs_root, g)
    check_register(root, fid, text, rows_file, g)
    carry = carried_from(text)
    latest = check_analysis(folder, text, specs_root, g, allow_from=carry)
    if carry:
        verify_carry(spec, text, g)
    if stage in ("ticket", "story"):
        check_approval(text, latest, g)
    if stage == "story":
        check_story(folder, text, story, g)
    return g, specdoc.revision(text)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("feature", help="the feature folder, e.g. specs/features/F001-daily-gift")
    ap.add_argument("--stage", choices=["approve", "ticket", "story"], default="ticket")
    ap.add_argument("--story", help="story ID, e.g. S1 (implies --stage story)")
    ap.add_argument("--root", help="project root (default: found from the feature folder)")
    ap.add_argument("--register-rows", help="rows exported from a legacy master, tab-separated")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    stage = "story" if a.story else a.stage
    if stage == "story" and not a.story:
        print("ready_check: --stage story needs --story", file=sys.stderr)
        return 2
    g, rev = run(a.feature, stage, a.story, a.root, a.register_rows)
    passed = not g.fails
    if a.json:
        print(json.dumps({"stage": stage, "passed": passed, "revision": rev,
                          "fails": g.fails, "warnings": g.warns, "notes": g.notes}, indent=2))
    else:
        print(f"Ready check ({stage}): {'PASS' if passed else 'FAIL'}")
        for m in g.fails:
            print(f"  FAIL  {m}")
        for m in g.warns:
            print(f"  WARN  {m}")
        for m in g.notes:
            print(f"  note  {m}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
