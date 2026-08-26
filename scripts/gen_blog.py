#!/usr/bin/env python3
"""Inject the latest blog.reapsec.com post into README.md as a bordered card."""
import html, re, urllib.request
from datetime import datetime, timezone
from xml.etree import ElementTree as ET

FEED  = "https://blog.reapsec.com/rss.xml"
START = "<!-- WRITEUPS:START -->"
END   = "<!-- WRITEUPS:END -->"

req  = urllib.request.Request(FEED, headers={"User-Agent": "reapsec-readme"})
item = ET.fromstring(urllib.request.urlopen(req, timeout=30).read()).find(".//item")
if item is None:
    raise SystemExit("no items in feed")

def txt(tag):
    el = item.find(tag)
    return (el.text or "").strip() if el is not None and el.text else ""

title = html.escape(txt("title"))
link  = txt("link")
enc   = item.find("enclosure")
cover = enc.get("url") if enc is not None else ""

try:
    date = datetime.strptime(txt("pubDate"), "%a, %d %b %Y %H:%M:%S %Z") \
             .replace(tzinfo=timezone.utc).strftime("%d %B %Y")
except ValueError:
    date = ""

cover_row = (f'<a href="{link}"><img src="{cover}" alt="{title}" /></a>\n\n'
             if cover else "")

card = f"""<table width="100%">
<tr><td width="100%" align="center">

{cover_row}### [{title}]({link})

<sub>{date}</sub>

<a href="{link}"><b>Read the writeup &rarr;</b></a>

</td></tr>
</table>

<sub>Latest post, synced automatically from <a href="https://blog.reapsec.com">blog.reapsec.com</a></sub>"""

block  = f"{START}\n\n{card}\n\n{END}"
readme = open("README.md", encoding="utf-8").read()
if START not in readme or END not in readme:
    raise SystemExit(f"markers {START} / {END} not found in README.md")
open("README.md", "w", encoding="utf-8").write(
    re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, readme, flags=re.S))
print(f"injected: {title} ({date}) cover={'yes' if cover else 'no'}")
