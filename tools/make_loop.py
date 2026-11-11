"""The dl-prototype loop as SVG, in the same blueprint style as the method flow."""
import sys

INK, RED, BG, QUIET = "#23262b", "#d6512b", "#f6f4f0", "#5b5f66"
SANS = "Inter, 'Helvetica Neue', Arial, sans-serif"
MONO = "'IBM Plex Mono', 'JetBrains Mono', 'DejaVu Sans Mono', monospace"
W, H = 160, 64
out = []


def t(x, y, s, size=14, font=MONO, fill=INK, weight=400, anchor="middle"):
    out.append(f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
               f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{s}</text>')


def box(cx, cy, name, sub, dark=False):
    fill = INK if dark else "#ffffff"
    col = "#ffffff" if dark else INK
    subcol = "#e6e6e6" if dark else QUIET
    out.append(f'<rect x="{cx - W / 2}" y="{cy - H / 2}" width="{W}" height="{H}" rx="5" '
               f'fill="{fill}" stroke="{INK}" stroke-width="{2.6 if dark else 1.5}"/>')
    t(cx, cy - 4, name, size=17, font=SANS, weight=600, fill=col)
    t(cx, cy + 18, sub, size=12.5, fill=subcol)


def path(d, colour=INK, dashed=False, width=1.6):
    m = "arr" if colour == RED else "ar"
    dash = ' stroke-dasharray="5 5"' if dashed else ""
    out.append(f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{width}"{dash} marker-end="url(#{m})"/>')


VW, VH = 900, 400
out.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" width="{VW}" height="{VH}" '
           f'role="img" aria-label="The dl-prototype loop: every playtest feeds back into the spec">')
out.append(f'''<defs>
<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>
<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{RED}"/></marker>
</defs>''')
out.append(f'<rect width="{VW}" height="{VH}" fill="{BG}"/>')
t(40, 46, "Every playtest feeds back into the spec", size=22, font=SANS, weight=700, anchor="start")
t(40, 72, "dl-prototype loop · design-led SDD", size=13, fill=QUIET, anchor="start")

c1, c2, c3, c4 = 120, 330, 540, 750
ra, rb, low = 150, 290, 360
t(40, ra - H / 2 - 12, "start: constitution · adopt", size=12, fill=QUIET, anchor="start")
box(c1, ra, "Request", "spec or brief")
box(c2, ra, "Clarify", "no blocking ?")
box(c3, ra, "Analyse", "separate agent")
box(c4, ra, "Tasks", "stories, tickets")
box(c4, rb, "Build", "lead and helpers")
box(c3, rb, "Prove", "on the target")
box(c2, rb, "Playtest", "log and revise", dark=True)

for a, b in ((c1, c2), (c2, c3), (c3, c4)):
    path(f"M{a + W / 2},{ra} L{b - W / 2 - 4},{ra}")
path(f"M{c4},{ra + H / 2} L{c4},{rb - H / 2 - 4}")
path(f"M{c4 - W / 2},{rb} L{c3 + W / 2 + 4},{rb}")
path(f"M{c3 - W / 2},{rb} L{c2 + W / 2 + 4},{rb}")
path(f"M{c2},{rb - H / 2} L{c2},{ra + H / 2 + 4}", colour=RED, width=2)
t(c2 + 12, (ra + rb) / 2 + 5, "rule or scope change", size=13, fill=RED, anchor="start")
path(f"M{c1},{ra + H / 2} L{c1},{low} L{c4},{low} L{c4},{rb + H / 2 + 4}", dashed=True)
t(c1 + 14, low - 10, "short path: a brief goes straight to build", size=13, fill=QUIET, anchor="start")

out.append("</svg>")
open(sys.argv[1], "w").write("\n".join(out))
