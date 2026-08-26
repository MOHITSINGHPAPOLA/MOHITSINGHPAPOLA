#!/usr/bin/env python3
"""Generate a self-hosted GitHub stats card. No third-party service to go down."""
import json, os, urllib.request

USER  = os.environ.get("GH_USER", "MOHITSINGHPAPOLA")
TOKEN = os.environ["GH_TOKEN"]
API   = "https://api.github.com/graphql"

Q = """
query($login:String!){
  user(login:$login){
    followers{totalCount}
    repositories(first:100, ownerAffiliations:OWNER, isFork:false){
      totalCount
      nodes{ stargazerCount languages(first:10, orderBy:{field:SIZE,direction:DESC}){
        edges{ size node{ name color } } } }
    }
    contributionsCollection{
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      contributionCalendar{ totalContributions }
    }
  }
}"""

def gql(q, v):
    r = urllib.request.Request(API, json.dumps({"query": q, "variables": v}).encode(),
        {"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json",
         "User-Agent": "reapsec-stats"})
    return json.load(urllib.request.urlopen(r))["data"]

u = gql(Q, {"login": USER})["user"]
c = u["contributionsCollection"]
stars = sum(n["stargazerCount"] for n in u["repositories"]["nodes"])

langs = {}
for n in u["repositories"]["nodes"]:
    for e in n["languages"]["edges"]:
        k = (e["node"]["name"], e["node"]["color"] or "#00ff9c")
        langs[k] = langs.get(k, 0) + e["size"]
top = sorted(langs.items(), key=lambda x: -x[1])[:6]
total = sum(v for _, v in top) or 1

rows = [("commits", c["totalCommitContributions"]),
        ("pull requests", c["totalPullRequestContributions"]),
        ("issues", c["totalIssueContributions"]),
        ("contributions (yr)", c["contributionCalendar"]["totalContributions"]),
        ("public repos", u["repositories"]["totalCount"]),
        ("stars earned", stars),
        ("followers", u["followers"]["totalCount"])]

W, H = 480, 300
p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
     '<style>.m{font-family:"JetBrains Mono","DejaVu Sans Mono",monospace}'
     '.k{fill:#7d8590;font-size:12.5px}.v{fill:#00ff9c;font-size:12.5px;font-weight:700}'
     '.t{fill:#00ff9c;font-size:13.5px;font-weight:700}'
     '.b{animation:f .9s ease-out both}@keyframes f{from{opacity:0;transform:translateX(-8px)}to{opacity:1}}</style>',
     f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#00ff9c" stroke-opacity=".3"/>',
     '<text class="m t" x="20" y="30">root@reapsec:~# git log --stat</text>']

y = 60
for i, (k, v) in enumerate(rows):
    p.append(f'<g class="b" style="animation-delay:{i*.09:.2f}s">'
             f'<text class="m k" x="22" y="{y}">{k}</text>'
             f'<text class="m v" x="{W-22}" y="{y}" text-anchor="end">{v:,}</text>'
             f'<rect x="22" y="{y+5}" width="{W-44}" height="1" fill="#00ff9c" opacity=".08"/></g>')
    y += 23

p.append(f'<text class="m t" x="20" y="{y+18}">languages</text>')
x, bw, by = 22, W - 44, y + 30
for i, ((name, color), size) in enumerate(top):
    w = bw * size / total
    p.append(f'<rect x="{x:.1f}" y="{by}" width="{max(w,2):.1f}" height="9" fill="{color}">'
             f'<animate attributeName="width" from="0" to="{max(w,2):.1f}" dur=".8s" fill="freeze"/></rect>')
    x += w
lx, ly = 22, by + 30
for (name, color), size in top:
    p.append(f'<circle cx="{lx+4}" cy="{ly-4}" r="4" fill="{color}"/>'
             f'<text class="m k" x="{lx+14}" y="{ly}">{name} {100*size/total:.0f}%</text>')
    lx += 16 + len(name) * 7.2 + 34
    if lx > W - 90: lx, ly = 22, ly + 18
p.append("</svg>")

os.makedirs("assets", exist_ok=True)
open("assets/stats.svg", "w").write("\n".join(p))
print(f"wrote assets/stats.svg  ({len(top)} langs, {sum(v for _,v in rows)} total events)")
