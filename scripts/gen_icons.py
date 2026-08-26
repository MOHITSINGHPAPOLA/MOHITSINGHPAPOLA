#!/usr/bin/env python3
"""Build solid brand-coloured circular profile icons. Self-hosted, no CDN."""
import re

SRC, SIZE = "assets/icons", 48

def path_of(f):
    m = re.search(r'd="([^"]+)"', open(f"{SRC}/{f}", encoding="utf-8").read())
    if not m: raise SystemExit(f"no path in {f}")
    return m.group(1)

def shell(bg, inner):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" '
            f'viewBox="0 0 {SIZE} {SIZE}"><circle cx="24" cy="24" r="24" fill="{bg}"/>'
            f'{inner}</svg>')

def brand(src, out, bg, fg):
    g = (f'<g transform="translate(12,12) scale(1)" fill="{fg}">'
         f'<path d="{path_of(src)}"/></g>')
    open(f"{SRC}/{out}.svg", "w", encoding="utf-8").write(shell(bg, g))
    print(f"{out:14} bg={bg} glyph")

def text(label, out, bg, fg, size, dy):
    g = (f'<text x="24" y="{24+dy}" text-anchor="middle" fill="{fg}" '
         f'font-family="DejaVu Sans,Helvetica,Arial,sans-serif" font-size="{size}" '
         f'font-weight="700">{label}</text>')
    open(f"{SRC}/{out}.svg", "w", encoding="utf-8").write(shell(bg, g))
    print(f"{out:14} bg={bg} text")

brand("_htb.svg", "htb", "#9FEF00", "#111811")   # HTB lime, dark glyph for contrast
brand("_thm.svg", "thm", "#212C42", "#FFFFFF")   # THM navy, white glyph
text("CTF", "ctftime-icon",  "#E3000B", "#FFFFFF", 14, 5)
text("in",  "linkedin-icon", "#0A66C2", "#FFFFFF", 20, 7)
