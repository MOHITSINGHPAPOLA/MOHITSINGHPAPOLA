#!/usr/bin/env python3
"""Inject the latest blog.reapsec.com posts into README.md between markers."""
import re, html, urllib.parse, urllib.request
from datetime import datetime, timezone
from xml.etree import ElementTree as ET

FEED   = "https://blog.reapsec.com/rss.xml"
COUNT  = 5
START  = "<!-- WRITEUPS:START -->"
END    = "<!-- WRITEUPS:END -->"

req = urllib.request.Request(FEED, headers={"User-Agent": "reapsec-readme"})
root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())

def txt(item, tag):
    el = item.find(tag)
    return (el.text or "").strip() if el is not None and el.text else ""

rows = []
for item in root.findall(".//item")[:COUNT]:
    title = html.escape(txt(item, "title"))
    link  = txt(item, "link")
    tags  = [c.text.strip().lstrip("#") for c in item.findall("category")
             if c.text and c.text.strip().lower() not in ("reapsec",)][:3]
    try:
        d = datetime.strptime(txt(item, "pubDate"), "%a, %d %b %Y %H:%M:%S %Z")
        date = d.replace(tzinfo=timezone.utc).strftime("%d %b %Y")
    except ValueError:
        date = ""
    badges = " ".join(
        f"![{html.escape(t)}](https://img.shields.io/badge/{urllib.parse.quote(t.replace('-','--').replace('_','__'))}-0d1117?style=flat-square&labelColor=0d1117&color=00ff9c)"
        for t in tags)
    rows.append(f"| **[{title}]({link})** <br/> <sub>{badges}</sub> | `{date}` |")

table = ("| writeup | published |\n|:--|--:|\n" + "\n".join(rows)) if rows else "_No posts found._"
block = (f"{START}\n\n{table}\n\n"
         f"<sub>Auto-synced from [blog.reapsec.com](https://blog.reapsec.com) · "
         f"last run {datetime.now(timezone.utc).strftime('%d %b %Y %H:%M UTC')}</sub>\n\n{END}")

readme = open("README.md", encoding="utf-8").read()
new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, readme, flags=re.S)
if new == readme and START not in readme:
    raise SystemExit(f"markers {START} / {END} not found in README.md")
open("README.md", "w", encoding="utf-8").write(new)
print(f"injected {len(rows)} posts")
