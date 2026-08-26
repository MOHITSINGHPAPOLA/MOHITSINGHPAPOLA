#!/usr/bin/env python3
"""Generate matrix-rain SVGs in dark and light variants."""
import random, html

GLYPHS = "01ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍ<>/\\$#*+-=[]{}"
W = H = 200
COLS, CS = 16, 13

# (filename, trail colour, leading-glyph colour, base opacity floor)
THEMES = [("assets/matrix.svg",       "#00ff9c", "#d8fff0", 0.25),
          ("assets/matrix-light.svg", "#0b8f5f", "#053b28", 0.35)]

for path, base, lead, floor in THEMES:
    random.seed(7)                       # same rain shape in both variants
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}" role="img" aria-label="matrix rain">',
           '<defs><linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">'
           '<stop offset="0%" stop-color="#fff" stop-opacity="0"/>'
           '<stop offset="22%" stop-color="#fff" stop-opacity="1"/>'
           '<stop offset="78%" stop-color="#fff" stop-opacity="1"/>'
           '<stop offset="100%" stop-color="#fff" stop-opacity="0"/>'
           '</linearGradient><mask id="m"><rect width="200" height="200" fill="url(#fade)"/></mask></defs>',
           '<style>'
           f'.g{{font-family:"DejaVu Sans Mono",monospace;font-size:11px;fill:{base}}}'
           f'.h{{fill:{lead};font-weight:700}}'
           + "".join(f"@keyframes r{i}{{from{{transform:translateY(-{330+i*9}px)}}"
                     f"to{{transform:translateY(200px)}}}}" for i in range(COLS))
           + "".join(f".c{i}{{animation:r{i} {4.5+random.random()*5:.1f}s linear infinite;"
                     f"animation-delay:-{random.random()*6:.1f}s}}" for i in range(COLS))
           + '</style>', '<g mask="url(#m)">']
    for i in range(COLS):
        n = random.randint(16, 26)
        out.append(f'<g class="c{i}">')
        for j in range(n):
            cls = "g h" if j == n - 1 else "g"
            op  = floor + (1 - floor) * (j / max(n - 1, 1))
            out.append(f'<text class="{cls}" x="{i*CS+4}" y="{j*12}" '
                       f'opacity="{op:.2f}">{html.escape(random.choice(GLYPHS), quote=False)}</text>')
        out.append('</g>')
    out += ['</g>', '</svg>']
    open(path, "w", encoding="utf-8").write("\n".join(out))
    print(f"wrote {path}")
