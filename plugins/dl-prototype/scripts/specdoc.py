"""Shared helpers for the dl-prototype scripts: reading the method's Markdown files.

Standard library only, so the scripts run anywhere Python 3.8+ does.
"""
import hashlib
import re
from pathlib import Path

HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
RULE_HEADING = re.compile(r"^###\s+(F\d{3}\.[A-Za-z0-9_-]+)\b")
REV_PREFIX = "rev-"

# Lines and sections that never change a spec's revision: workflow metadata, not design.
EXCLUDED_HEADER_FIELDS = ("status", "last updated")
EXCLUDED_SECTIONS = ("approval", "changelog")


def read(path):
    return Path(path).read_text(encoding="utf-8")


def sections(text, level=2):
    """Split text into (title, body_lines) by headings of exactly `level`.

    The part before the first such heading has title None.
    """
    out, title, buf = [], None, []
    in_code = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
        m = None if in_code else HEADING.match(line)
        if m and len(m.group(1)) == level:
            out.append((title, buf))
            title, buf = m.group(2).strip(), []
        else:
            buf.append(line)
    out.append((title, buf))
    return out


def section(text, name, level=2):
    """Body lines of the first section whose title starts with `name` (case-insensitive)."""
    for title, body in sections(text, level):
        if title and title.lower().startswith(name.lower()):
            return body
    return None


def header_fields(text):
    """`- Key: value` lines before the first level-2 heading, as a dict with lower-case keys."""
    head = sections(text, 2)[0][1]
    fields = {}
    for line in head:
        m = re.match(r"^\s*-\s+([^:]+):\s*(.*)$", line)
        if m:
            fields[m.group(1).strip().lower()] = m.group(2).strip()
    return fields


def bullet_fields(lines):
    fields = {}
    for line in lines or []:
        m = re.match(r"^\s*-\s+([^:]+):\s*(.*)$", line)
        if m:
            fields[m.group(1).strip().lower()] = m.group(2).strip()
    return fields


def split_row(line):
    line = line.strip()
    if not (line.startswith("|") and line.endswith("|")):
        return None
    cells = [c.strip() for c in line[1:-1].split("|")]
    return cells


def is_separator(cells):
    return all(re.fullmatch(r":?-{3,}:?", c or "") for c in cells)


def tables(lines):
    """Every Markdown table in `lines`, as a list of {'header': [...], 'rows': [[...], ...]}."""
    found, cur = [], None
    for line in lines or []:
        cells = split_row(line)
        if cells is None:
            if cur:
                found.append(cur)
                cur = None
            continue
        if cur is None:
            cur = {"header": cells, "rows": []}
        elif is_separator(cells):
            continue
        else:
            cur["rows"].append(cells)
    if cur:
        found.append(cur)
    return found


def col(table, *names):
    """Index of the first header cell matching any of `names` (case-insensitive), else None."""
    low = [h.lower() for h in table["header"]]
    for n in names:
        for i, h in enumerate(low):
            if h == n.lower():
                return i
    for n in names:
        for i, h in enumerate(low):
            if h.startswith(n.lower()):
                return i
    return None


def cell(row, i):
    if i is None or i >= len(row):
        return ""
    return row[i].strip()


def normalise_for_revision(text):
    """The spec's design content: header fields other than status and dates, and every
    section except Approval and Changelog. Whitespace at line ends and runs of blank
    lines are ignored."""
    kept = []
    for title, body in sections(text, 2):
        if title is None:
            for line in body:
                m = re.match(r"^\s*-\s+([^:]+):", line)
                if m and m.group(1).strip().lower() in EXCLUDED_HEADER_FIELDS:
                    continue
                kept.append(line)
            continue
        if title.lower().startswith(EXCLUDED_SECTIONS):
            continue
        kept.append("## " + title)
        kept.extend(body)
    lines = [l.rstrip() for l in kept]
    out, blank = [], False
    for l in lines:
        if not l:
            if not blank and out:
                out.append("")
            blank = True
        else:
            out.append(l)
            blank = False
    while out and not out[-1]:
        out.pop()
    return "\n".join(out) + "\n"


def revision(text):
    digest = hashlib.sha256(normalise_for_revision(text).encode("utf-8")).hexdigest()
    return REV_PREFIX + digest[:12]


def rule_blocks(text):
    """{rule_id: block_text} for every `### F<NNN>.<id>` rule heading in the Rules section."""
    blocks, cur, buf = {}, None, []
    body = section(text, "Rules") or []
    in_code = False
    for line in body:
        if line.strip().startswith("```"):
            in_code = not in_code
        m = None if in_code else RULE_HEADING.match(line)
        if m:
            if cur:
                blocks[cur] = "\n".join(buf).strip()
            cur, buf = m.group(1), [line]
        elif cur:
            buf.append(line)
    if cur:
        blocks[cur] = "\n".join(buf).strip()
    return blocks


def find_specs_root(start):
    """The nearest folder at or above `start` that holds constitution.md, else None."""
    p = Path(start).resolve()
    if p.is_file():
        p = p.parent
    for cand in [p, *p.parents]:
        if (cand / "constitution.md").exists():
            return cand
        if (cand / "specs" / "constitution.md").exists():
            return cand / "specs"
    return None


def feature_id(folder):
    m = re.match(r"(F\d{3})", Path(folder).name)
    return m.group(1) if m else None


def report_sort_key(path):
    """analysis-YYYY-MM-DD-NN.md, and the older -passN and undated-pass names, in run order."""
    name = Path(path).name
    m = re.match(r"analysis-(\d{4}-\d{2}-\d{2})(?:-(?:pass)?(\d+))?\.md$", name)
    if not m:
        return ("", 0)
    return (m.group(1), int(m.group(2) or 1))


def reports(folder):
    files = [p for p in Path(folder).glob("analysis-*.md") if report_sort_key(p)[0]]
    return sorted(files, key=report_sort_key)


UNDECIDED = re.compile(r"(?<![\w?`])\?(?![\w?`])")
OQ_ID = re.compile(r"\bOQ-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}\b")


def undecided_lines(text):
    """(line_no, line) for lines in design sections holding a standalone `?` placeholder."""
    out, skip, in_code = [], False, False
    for n, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            in_code = not in_code
        m = None if in_code else HEADING.match(line)
        if m and len(m.group(1)) == 2:
            skip = m.group(2).strip().lower().startswith(EXCLUDED_SECTIONS + ("open questions",))
            continue
        if skip:
            continue
        stripped = re.sub(r"`[^`]*`", "", line)
        if UNDECIDED.search(stripped):
            out.append((n, line.strip()))
    return out
