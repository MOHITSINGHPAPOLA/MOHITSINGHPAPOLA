#!/usr/bin/env python3
"""Generate a looping fake-recon terminal SVG, in dark and light variants."""
import html

W, H, CYCLE = 268, 214, 9.0
PAD = 17          # transparent top padding: nudges the box down half a line
LH, X0, Y0  = 17, 14, 56

# (text, class)  -- p=prompt line, o=output, ok=success
LINES = [("$ nmap -sV 10.10.11.42",        "p"),
         ("22/tcp   open  ssh",            "o"),
         ("80/tcp   open  http",           "o"),
         ("445/tcp  open  microsoft-ds",   "o"),
         ("$ ./foothold.py --rev 443",     "p"),
         ("[+] shell obtained",            "ok"),
         ("$ whoami",                      "p"),
         ("root",                          "ok")]

THEMES = [("assets/terminal.svg",       "#0d1117", "#161b22", "#00ff9c", "#8b949e", "#c9d1d9", ".30"),
          ("assets/terminal-light.svg", "#ffffff", "#f0f3f6", "#0b8f5f", "#57606a", "#1f2328", ".45")]

for path, bg, chrome, accent, dim, fg, stroke in THEMES:
    step = CYCLE / (len(LINES) + 2)
    css = [f'.m{{font-family:"DejaVu Sans Mono","Courier New",monospace;font-size:10.5px}}',
           f'.p{{fill:{accent}}}.o{{fill:{dim}}}.ok{{fill:{accent};font-weight:700}}.t{{fill:{dim};font-size:9.5px}}',
           '@keyframes rv{0%{opacity:0}4%{opacity:1}92%{opacity:1}100%{opacity:0}}',
           '@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:0}}',
           f'.cur{{fill:{accent};animation:bl 1s steps(1) infinite}}']
    for i in range(len(LINES)):
        css.append(f'.l{i}{{opacity:0;animation:rv {CYCLE}s linear infinite;'
                   f'animation-delay:{i*step:.2f}s}}')

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H+PAD}" '
           f'viewBox="0 0 {W} {H+PAD}" role="img" aria-label="recon terminal">',
           '<style>' + "".join(css) + '</style>',
           f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="9" fill="{bg}" '
           f'stroke="{accent}" stroke-opacity="{stroke}" stroke-width="1.5"/>',
           f'<path d="M1 10a9 9 0 0 1 9-9h{W-20}a9 9 0 0 1 9 9v22H1z" fill="{chrome}"/>',
           '<circle cx="17" cy="17" r="4.5" fill="#ff5f57"/>',
           '<circle cx="32" cy="17" r="4.5" fill="#febc2e"/>',
           '<circle cx="47" cy="17" r="4.5" fill="#28c840"/>',
           f'<text class="m t" x="{W//2+14}" y="20.5" text-anchor="middle">root@reapsec</text>']
    out.insert(2, f'<g transform="translate(0,{PAD})">')
    for i, (txt, cls) in enumerate(LINES):
        out.append(f'<text class="m {cls} l{i}" x="{X0}" y="{Y0 + i*LH}">{html.escape(txt)}</text>')
    out.append(f'<rect class="cur" x="{X0}" y="{Y0 + len(LINES)*LH - 8}" width="6" height="11"/>')
    out.append('</g>')
    out.append('</svg>')
    open(path, "w", encoding="utf-8").write("\n".join(out))
    print(f"wrote {path}")
