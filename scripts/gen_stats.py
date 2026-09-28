#!/usr/bin/env python3
"""Render assets/activity.svg from live GitHub data (needs the `gh` CLI, authenticated).

    python3 scripts/gen_stats.py

Run daily by .github/workflows/refresh-stats.yml so the card stays current
without depending on a third-party stats service.
"""
import json, subprocess, datetime
from pathlib import Path

LOGIN = "DevLSJ"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "activity.svg"

C = dict(bg="#1a1b26", panel="#24283b", hi="#292e42", line="#3b4261",
         fg="#c0caf5", dim="#a9b1d6", mute="#565f89",
         purple="#bb9af7", blue="#7aa2f7", cyan="#7dcfff", green="#9ece6a",
         orange="#ff9e64", yellow="#e0af68", teal="#73daca", red="#f7768e")
MONO = "ui-monospace,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
LANG_COLORS = ["purple", "blue", "cyan", "green", "orange", "yellow", "teal", "red"]

QUERY = """
query($login:String!, $from:DateTime!, $to:DateTime!) {
  user(login:$login) {
    followers { totalCount }
    contributionsCollection(from:$from, to:$to) {
      totalCommitContributions totalPullRequestContributions
      totalIssueContributions totalPullRequestReviewContributions
      contributionCalendar { totalContributions weeks { contributionDays { contributionCount } } }
    }
    repositories(first:100, ownerAffiliations:OWNER, isFork:false) {
      totalCount
      nodes { stargazerCount
        languages(first:10, orderBy:{field:SIZE, direction:DESC}) { edges { size node { name } } } }
    }
  }
}"""

def fetch(year):
    args = ["gh", "api", "graphql", "-f", f"query={QUERY}", "-F", f"login={LOGIN}",
            "-F", f"from={year}-01-01T00:00:00Z", "-F", f"to={year}-12-31T23:59:59Z"]
    return json.loads(subprocess.check_output(args))["data"]["user"]

def text(x, y, s, size=13, fill=C["fg"], font=MONO, weight=400, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}">{s}</text>')

def render(u, year):
    W, H = 520, 190
    cc = u["contributionsCollection"]
    repos = u["repositories"]
    stars = sum(n["stargazerCount"] for n in repos["nodes"])
    langs = {}
    for n in repos["nodes"]:
        for e in n["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:5]
    other = total - sum(v for _, v in top)
    if other > 0:
        top.append(("Other", other))

    b = [f'<rect width="{W}" height="{H}" rx="14" fill="{C["bg"]}" stroke="{C["line"]}"/>',
         f'<path d="M250 24V166" stroke="{C["line"]}"/>']
    b.append(text(24, 36, f"activity · {year}", 12, C["purple"], MONO, 700))
    days = [d for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    active = sum(1 for d in days if d["contributionCount"] > 0)
    stats = [("contributions", cc["contributionCalendar"]["totalContributions"], "purple"),
             ("commits", cc["totalCommitContributions"], "cyan"),
             ("pull requests", cc["totalPullRequestContributions"], "green"),
             ("public repos", repos["totalCount"], "yellow"),
             ("active days", active, "orange")]
    y = 66
    for label, val, col in stats:
        b.append(f'<circle cx="28" cy="{y-4}" r="3" fill="{C[col]}"/>')
        b.append(text(40, y, label, 12, C["dim"], SANS))
        b.append(text(226, y, str(val), 13, C["fg"], MONO, 700, "end"))
        y += 26
    # languages
    b.append(text(274, 36, "languages", 12, C["purple"], MONO, 700))
    x, bx, bw = 274, 274, 222
    b.append(f'<rect x="{bx}" y="48" width="{bw}" height="10" rx="5" fill="{C["hi"]}"/>')
    b.append(f'<clipPath id="bar"><rect x="{bx}" y="48" width="{bw}" height="10" rx="5"/></clipPath>')
    for i, (name, size) in enumerate(top):
        w = bw * size / total
        col = C[LANG_COLORS[i % len(LANG_COLORS)]] if name != "Other" else C["mute"]
        b.append(f'<rect x="{x:.1f}" y="48" width="{w:.1f}" height="10" fill="{col}" clip-path="url(#bar)"/>')
        x += w
    y = 84
    for i, (name, size) in enumerate(top):
        col = C[LANG_COLORS[i % len(LANG_COLORS)]] if name != "Other" else C["mute"]
        cx = 274 if i % 2 == 0 else 392
        if i % 2 == 0 and i: y += 24
        b.append(f'<rect x="{cx}" y="{y-9}" width="9" height="9" rx="2" fill="{col}"/>')
        b.append(text(cx + 16, y, f"{name} {100*size/total:.0f}%", 11.5, C["dim"]))
    b.append(text(496, 172, f"updated {datetime.date.today():%Y-%m-%d}", 10, C["mute"], MONO, 400, "end"))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">\n'
            + "\n".join(b) + "\n</svg>\n")

if __name__ == "__main__":
    year = datetime.date.today().year
    OUT.write_text(render(fetch(year), year))
    print("wrote", OUT)
