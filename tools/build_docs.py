"""Build the HTML pages in docs/ from their Markdown sources.

Run from the repository root:  python3 tools/build_docs.py
Needs the 'markdown' package (pip install markdown).
"""
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PAGES = [
    ("method-guide.md", "method-guide.html", "Method guide"),
    ("worked-example.md", "worked-example.html", "Worked example"),
]

TEMPLATE = """<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Design-led SDD</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root{{--paper:#f6f4f0;--ink:#23262b;--quiet:#4f535a;--red:#b63f25}}
*{{box-sizing:border-box}}
html,body{{margin:0;background:var(--paper);color:var(--ink);font-family:Inter,Arial,sans-serif;font-size:17px;line-height:1.65}}
a{{color:var(--red)}}
header{{border-bottom:2px solid var(--ink)}}
header div,main{{max-width:860px;margin:0 auto;padding:16px 24px}}
header a{{font-weight:700;text-decoration:none;color:var(--ink)}}
header span{{font-family:'IBM Plex Mono',monospace;font-size:14px;color:var(--quiet);margin-left:12px}}
main{{padding-top:40px;padding-bottom:80px}}
h1{{font-size:clamp(32px,5vw,46px);line-height:1.1;letter-spacing:-1px;margin:0 0 20px}}
h2{{font-size:24px;letter-spacing:-.3px;margin:44px 0 12px;padding-top:16px;border-top:1.5px solid var(--ink)}}
code{{font-family:'IBM Plex Mono',monospace;font-size:.9em;background:#ebe7df;padding:1px 4px;border-radius:3px}}
pre{{background:#fff;border:1.5px solid var(--ink);border-radius:5px;padding:16px 18px;overflow-x:auto;line-height:1.55}}
pre code{{background:none;padding:0;font-size:14px}}
table{{width:100%;border-collapse:collapse;background:#fff;border:1.5px solid var(--ink);font-size:15px;margin:12px 0 20px;display:block;overflow-x:auto}}
th,td{{text-align:left;padding:8px 12px;border-bottom:1px solid #d9d6cf;vertical-align:top}}
th{{background:#efece6;font-weight:600}}
blockquote{{margin:16px 0;padding:10px 18px;border-left:3px solid var(--red);background:#fff}}
img{{max-width:100%;height:auto;border:1.5px solid var(--ink);border-radius:5px}}
</style>
</head>
<body>
<header><div><a href="index.html">Design-led SDD</a><span>{title}</span></div></header>
<main>
{body}
</main>
</body>
</html>
"""


def build():
    for src, out, title in PAGES:
        text = (DOCS / src).read_text(encoding="utf-8")
        # Links that leave docs/ only work inside the repository, not on the site.
        text = re.sub(r"\[([^\]]+)\]\(\.\./[^)]+\)", r"\1", text)
        text = text.replace("](method-guide.md)", "](method-guide.html)")
        text = text.replace("](worked-example.md)", "](worked-example.html)")
        body = markdown.markdown(text, extensions=["tables", "fenced_code"])
        (DOCS / out).write_text(TEMPLATE.format(title=title, body=body), encoding="utf-8")
        print("built", out)


if __name__ == "__main__":
    build()
