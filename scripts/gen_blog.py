#!/usr/bin/env python3
"""Inject the two most recent blog.reapsec.com posts into README.md as side-by-side cards."""
import html, re, urllib.request
from datetime import datetime, timezone
from xml.etree import ElementTree as ET

FEED  = "https://blog.reapsec.com/rss.xml"
COUNT = 2
START = "<!-- WRITEUPS:START -->"
END   = "<!-- WRITEUPS:END -->"

req   = urllib.request.Request(FEED, headers={"User-Agent": "reapsec-readme"})
items = ET.fromstring(urllib.request.urlopen(req, timeout=30).read()).findall(".//item")[:COUNT]
if not items:
    raise SystemExit("no items in feed")

def cell(item):
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
    img = (f'<a href="{link}"><img src="{cover}" alt="{title}" width="100%" /></a>\n\n'
           if cover else "")
    return (f'<td width="50%" valign="top" align="center">\n\n'
            f'{img}### [{title}]({link})\n\n'
            f'<sub>{date}</sub>\n\n'
            f'<a href="{link}"><b>Read the writeup &rarr;</b></a>\n\n'
            f'</td>')

cells = [cell(i) for i in items]
while len(cells) < COUNT:                      # keep the grid even if the feed is short
    cells.append('<td width="50%"></td>')

card  = "<table width=\"100%\">\n<tr>\n" + "\n".join(cells) + "\n</tr>\n</table>"
block = f"{START}\n\n{card}\n\n{END}"

readme = open("README.md", encoding="utf-8").read()
if START not in readme or END not in readme:
    raise SystemExit(f"markers {START} / {END} not found in README.md")
open("README.md", "w", encoding="utf-8").write(
    re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, readme, flags=re.S))
print("injected: " + ", ".join(
    (i.findtext("title") or "?") for i in items))
