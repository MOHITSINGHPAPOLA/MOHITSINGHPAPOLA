#!/usr/bin/env python3
"""Build circular social icons for the Profiles row. Self-hosted, no CDN."""
import re, os

SRC   = "assets/icons"
SIZE  = 48
BG    = "#0d1117"
RING  = "#00ff9c"
GLYPH = "#00ff9c"

def brand_path(name):
    m = re.search(r'd="([^"]+)"', open(f"{SRC}/{name}.svg", encoding="utf-8").read())
    return m.group(1) if m else None

def shell(inner):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" '
            f'viewBox="0 0 {SIZE} {SIZE}">'
            f'<circle cx="24" cy="24" r="23" fill="{BG}" stroke="{RING}" '
            f'stroke-opacity=".55" stroke-width="1.6"/>{inner}</svg>')

def from_brand(name, out):
    d = brand_path(name)
    if not d:
        raise SystemExit(f"no path in {name}.svg")
    g = (f'<g transform="translate(11,11) scale(1.0833)" fill="{GLYPH}">'
         f'<path d="{d}"/></g>')
    open(f"{SRC}/{out}.svg", "w", encoding="utf-8").write(shell(g))
    print(f"wrote {SRC}/{out}.svg  (brand glyph)")

def from_text(text, out, size=15, dy=5.5, spacing=0.5):
    g = (f'<text x="24" y="{24+dy}" text-anchor="middle" fill="{GLYPH}" '
         f'font-family="DejaVu Sans Mono,Courier New,monospace" font-size="{size}" '
         f'font-weight="700" letter-spacing="{spacing}">{text}</text>')
    open(f"{SRC}/{out}.svg", "w", encoding="utf-8").write(shell(g))
    print(f"wrote {SRC}/{out}.svg  (text mark)")

from_brand("tryhackme",  "thm")
from_brand("hackthebox", "htb")
from_text("in",  "linkedin-icon", size=19, dy=6.5)
from_text("CTF", "ctftime-icon",  size=13, dy=4.5)
