"""Generate the dl-prototype method flow chart as SVG."""
import sys

INK = "#23262b"
RED = "#d6512b"
BG = "#f6f4f0"
SANS = "Inter, 'Helvetica Neue', Arial, sans-serif"
MONO = "'IBM Plex Mono', 'JetBrains Mono', 'DejaVu Sans Mono', monospace"

out = []


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=15, font=MONO, fill=INK, weight=400, anchor="start", spacing=None):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    out.append(f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
               f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{ls}>{s}</text>')


def rich(x, y, parts, size=15):
    """parts: list of (text, colour)."""
    spans = "".join(f'<tspan fill="{c}">{esc(t)}</tspan>' for t, c in parts)
    out.append(f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" xml:space="preserve">{spans}</text>')


def box(x, y, w, h, dark=False, stroke=1.5, dashed=False):
    fill = INK if dark else "#ffffff"
    dash = ' stroke-dasharray="6 5"' if dashed else ""
    if dashed:
        fill = "none"
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fill}" '
               f'stroke="{INK}" stroke-width="{stroke}"{dash}/>')


def card(x, y, w, h, title, lines=(), label=None, dark=False, stroke=1.5, title_size=22):
    box(x, y, w, h, dark=dark, stroke=stroke)
    col = "#ffffff" if dark else INK
    ty = y + 34
    if label:
        text(x + 22, y + 30, label, size=12, fill=col, spacing=1.2)
        ty = y + 60
    text(x + 22, ty, esc(title), size=title_size, font=SANS, weight=600, fill=col)
    ly = ty + 30
    for ln in lines:
        if isinstance(ln, list):
            rich(x + 22, ly, ln)
        else:
            text(x + 22, ly, esc(ln), fill=col)
        ly += 23


def chip(x, y, w, h, label):
    box(x, y, w, h)
    text(x + w / 2, y + h / 2 + 6, esc(label), size=16, font=SANS, weight=600, anchor="middle")


def line(pts, colour=INK, head=True, width=1.6, dashed=False):
    d = " ".join(f"{'M' if i == 0 else 'L'}{x},{y}" for i, (x, y) in enumerate(pts))
    m = f' marker-end="url(#{"ar" if colour == INK else "arr"})"' if head else ""
    dash = ' stroke-dasharray="4 5"' if dashed else ""
    out.append(f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{width}"{m}{dash}/>')


def both(x, y1, y2):
    out.append(f'<path d="M{x},{y1} L{x},{y2}" stroke="{INK}" stroke-width="1.6" '
               f'marker-start="url(#ars)" marker-end="url(#ar)"/>')


W, H = 2048, 1121
out.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
out.append(f'''<defs>
<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>
<marker id="ars" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="9" markerHeight="9" orient="auto"><path d="M10,0 L0,5 L10,10 z" fill="{INK}"/></marker>
<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{RED}"/></marker>
</defs>''')
out.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

# Column headers
cols = [
    (73, "1", "Request", "spec · brief"),
    (468, "2", "Specification", "clarify"),
    (863, "3", "Analyse", "analyze"),
    (1258, "4", "Build", "tasks · brief"),
    (1653, "5", "Playtest", "playtest"),
]
CW = 346
for x, n, t, skill in cols:
    text(x, 80, f'{n}<tspan dx="12">{t}</tspan>', size=19, font=SANS, weight=600)
    text(x + CW, 80, skill, size=15, anchor="end")
    out.append(f'<line x1="{x}" y1="97" x2="{x + CW}" y2="97" stroke="{INK}" stroke-width="2"/>')

# ---------- Column 1: Request ----------
x1 = 73
card(x1, 146, CW, 121, "Client or product owner",
     ["never reads the specs;", "gets a plain summary"], dark=True)
both(x1 + 173, 272, 360)
text(x1 + 186, 322, "questions / answers")
card(x1, 365, CW, 122, "Spec skill", ["asks one at a time,", "never decides"], label="AGENT")
line([(x1 + 173, 487), (x1 + 173, 555)])
card(x1, 560, CW, 122, "Request",
     ["intent · scope · job stories", [("short path: ", INK), ("brief", RED), (" · full: ", INK), ("spec", RED)]])
# request -> clarify
line([(x1 + CW, 621), (443, 621), (443, 718), (463, 718)])

# ---------- Column 2: Specification ----------
x2 = 468
box(x2, 146, CW, 462, dashed=True)
text(x2 + 20, 176, "specs/, beside the code")
text(x2 + 20, 200, "constitution → feature → rule", size=14)
box(x2 + 20, 218, 306, 128)
text(x2 + 42, 256, "Rules", size=22, font=SANS, weight=600)
rich(x2 + 42, 290, [("When · ", INK), ("Provided", RED), (" ·", INK)])
rich(x2 + 42, 317, [("Then · ", INK), ("Otherwise", RED), (" + examples", INK)])
box(x2 + 20, 365, 306, 102)
text(x2 + 42, 403, "Open questions", size=22, font=SANS, weight=600)
rich(x2 + 42, 437, [("?", RED), (" blocks building · owner", INK)])
chip(x2 + 20, 487, 148, 47, "Constitution")
chip(x2 + 178, 487, 148, 47, "Glossary")
chip(x2 + 20, 543, 148, 47, "States")
chip(x2 + 178, 543, 148, 47, "Parameters")
# clarify
card(x2, 677, CW, 110, "Clarify", ["sorts who answers what"], label="AGENT")
line([(x2 + 173, 677), (x2 + 173, 613)])
text(x2 + 186, 636, "decisions written in,")
text(x2 + 186, 656, "? removed")
both(x2 + 173, 792, 848)
text(x2 + 186, 826, "questions / answers")
card(x2, 853, CW, 97, "Designer", ["decides gaps · marks Ready"], dark=True)
# red: clarify -> request (business questions)
line([(x2, 768), (x1 + 173, 768), (x1 + 173, 687)], colour=RED)
text(x1 + 14, 795, "business questions ·", fill=RED)
text(x1 + 14, 816, "plain summary to the owner", fill=RED)

# spec tree -> analysis pack
line([(x2 + CW, 243), (858, 243)])

# ---------- Column 3: Analyse ----------
x3 = 863
card(x3, 195, CW, 97, "Analysis pack", ["spec · constitution · glossary"])
line([(x3 + 173, 292), (x3 + 173, 360)])
card(x3, 365, CW, 127, "Checking agent",
     ["fresh each run, sees no code,", "tickets or playtests"], label="AGENT")
line([(x3 + 173, 492), (x3 + 173, 580)])
text(x3 + 186, 541, "judge")
card(x3, 585, CW, 98, "Analysis report", ["findings · blocking · advisory"])
line([(x3 + 173, 683), (x3 + 173, 738)])
card(x3, 743, CW, 98, "Ready gate", ["no blocking ? · no open finding"], stroke=2.6)
# red: report -> designer
line([(x3, 650), (838, 650), (838, 928), (819, 928)], colour=RED)

# ready gate -> tasks
line([(x3 + CW, 792), (1233, 792), (1233, 243), (1253, 243)])

# ---------- Column 4: Build ----------
x4 = 1258
card(x4, 195, CW, 97, "Tasks", ["job stories · Gherkin · tickets"])
line([(x4 + 173, 292), (x4 + 173, 324), (x4 + 78, 324), (x4 + 78, 360)])
line([(x4 + 173, 324), (x4 + 268, 324), (x4 + 268, 360)], head=True)
card(x4, 365, 157, 127, "Lead", ["plans, briefs,", "reviews"], label="AGENT")
card(x4 + 189, 365, 157, 127, "Helpers", ["one task each,", "max two"], label="AGENT")
out.append(f'<line x1="{x4 + 173}" y1="355" x2="{x4 + 173}" y2="512" stroke="{INK}" '
           f'stroke-width="1.6" stroke-dasharray="5 5"/>')
text(x4 + 173, 535, "never on the", anchor="middle")
text(x4 + 173, 555, "same files", anchor="middle")
line([(x4 + 78, 492), (x4 + 78, 604)])
line([(x4 + 268, 492), (x4 + 268, 604)])
card(x4, 609, CW, 74, "Prove it on the target", [], title_size=21)
text(x4 + 22, 669, "a playable build, not “it compiled”", size=14)
# red: prove -> designer (gaps)
line([(x4 + 173, 683), (x4 + 173, 884), (819, 884)], colour=RED)
text(845, 906, "gaps the spec doesn't decide", fill=RED)
text(845, 952, "findings: resolve by edit, or dismiss with a reason", fill=RED)
# prove -> playtest log
line([(x4 + CW, 646), (1648, 646)])

# ---------- Column 5: Playtest ----------
x5 = 1653
box(x5, 146, CW, 102)
text(x5 + 22, 174, "NOTE", size=12, spacing=1.2)
text(x5 + 22, 203, "Agents report; people decide.", size=18, font=SANS)
text(x5 + 22, 229, "The spec keeps the reasons.", size=18, font=SANS)
card(x5, 330, CW, 110, "Players and team", ["play the build; record what", "they did, not what they think"], dark=True)
line([(x5 + 173, 440), (x5 + 173, 567)])
card(x5, 572, CW, 135, "Playtest log",
     ["hypotheses: held · failed ·", "unclear, with evidence"], label="EACH SESSION")
line([(x5 + 173, 707), (x5 + 173, 738)])
card(x5, 743, CW, 74, "Spec changes", [], title_size=21)
text(x5 + 22, 803, "tuning · rule · scope · pillar")
line([(x5 + 173, 817), (x5 + 173, 845)])
card(x5, 850, CW, 104, "Graduation check", ["settled economy or rewards →", "production tier (planned)"], stroke=2.6, title_size=21)

# big red loop: spec changes -> spec tree
line([(x5 + CW, 780), (2024, 780), (2024, 985), (443, 985), (443, 575), (463, 575)], colour=RED, width=2)
text(1024, 1013, "what the build teaches goes back into the spec", size=17, fill=RED, anchor="middle")
text(1024, 1037, "Rule and scope changes rerun analyze; tuning changes go straight in.", size=14, anchor="middle")

# footer
out.append(f'<line x1="73" y1="1055" x2="1999" y2="1055" stroke="{INK}" stroke-width="1.5"/>')
text(73, 1090, "One spec carries the design and its reasons: designers decide, agents build and report, "
     "every playtest feeds back in.", size=18, font=SANS)

out.append("</svg>")
open(sys.argv[1], "w").write("\n".join(out))
