#!/usr/bin/env python3
"""Generate the SVG assets referenced by README.md.

Edit PROFILE / STACKS below, then run:

    python3 scripts/gen_assets.py

Icons in scripts/icons/ come from Simple Icons (CC0 1.0).
Palette: Tokyo Night. No external fonts or images are referenced so the
SVGs render inside GitHub's <img> sandbox.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
ICONS = ROOT / "scripts" / "icons"

C = dict(
    bg="#1a1b26", bg2="#16161e", panel="#24283b", hi="#292e42", line="#3b4261",
    fg="#c0caf5", dim="#a9b1d6", mute="#565f89", code="#2f3549",
    purple="#bb9af7", blue="#7aa2f7", cyan="#7dcfff", green="#9ece6a",
    orange="#ff9e64", red="#f7768e", yellow="#e0af68", teal="#73daca",
)
MONO = "ui-monospace,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"

# ---------------------------------------------------------------- data ----
PROFILE = dict(
    name="DevLSJ",
    handle="@DevLSJ",
    mark=">_",
    lines=["Junior Developer", "Computer Software Engineering"],
    joined="Joined GitHub · Oct 2024",
    tz="UTC+09:00",
)

BANNER_CHIPS = [("eBPF", "purple"), ("Linux", "blue"), ("Kotlin", "teal"),
                ("Java", "orange"), ("Python", "yellow"), ("TypeScript", "cyan")]

BANNER_TERMINAL = [
    ("$", "whoami"),
    ("", "devlsj"),
    ("$", "cat now.txt"),
    (">", "building eBPF supply-chain"),
    (">", "attack detection · capstone"),
    ("$", None),  # cursor line
]

STACKS = [
    dict(id="kotlin", icon="kotlin", color="purple", name="KOTLIN",
         title="ANDROID · MOBILE", level=3, used="JansangTravel",
         specialty="Android UI · Coroutines", style="Mobile app",
         since="2026", projects=1),
    dict(id="java", icon="openjdk", color="orange", name="JAVA",
         title="BACKEND · SPRING", level=3, used="AdminWeb",
         specialty="REST API · Admin console", style="Enterprise web",
         since="2026", projects=1),
    dict(id="python", icon="python", color="yellow", name="PYTHON",
         title="BACKEND · DATA", level=3, used="eBPF-Trace",
         specialty="FastAPI · ML pipeline", style="Detection service",
         since="2026", projects=1),
    dict(id="ebpf", icon="linux", color="blue", name="eBPF / LINUX",
         title="KERNEL · SECURITY", level=2, used="eBPF-Trace",
         specialty="Kernel tracing · detection", style="Systems security",
         since="2026", projects=1),
    dict(id="typescript", icon="react", color="cyan", name="TYPESCRIPT / REACT",
         title="FRONTEND · DASHBOARD", level=3, used="AdminWeb · eBPF-Trace",
         specialty="Admin UI · live dashboard", style="Web frontend",
         since="2026", projects=2),
]

PIN_ICONS = [("python", "yellow"), ("openjdk", "orange"), ("kotlin", "purple"),
             ("linux", "blue"), ("react", "cyan"), ("typescript", "cyan"),
             ("docker", "blue"), ("postgresql", "blue"), ("terraform", "purple"),
             ("fastapi", "teal"), ("spring", "green"), ("android", "green"),
             ("c", "blue"), ("gnubash", "green"), ("github", "fg")]

# ------------------------------------------------------------- helpers ----
def icon_path(name):
    svg = (ICONS / f"{name}.svg").read_text()
    return re.search(r'd="([^"]+)"', svg).group(1)

def icon(name, cx, cy, size, fill):
    s = size / 24
    return (f'<g transform="translate({cx - size/2:.1f} {cy - size/2:.1f}) scale({s:.4f})">'
            f'<path d="{icon_path(name)}" fill="{fill}"/></g>')

def text(x, y, s, size=14, fill=C["fg"], font=MONO, weight=400, anchor="start", extra=""):
    s = (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>')

def svg(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img">\n<defs>{defs}</defs>\n{body}\n</svg>\n')

# tiny glyphs (14px box, drawn around origin 0..14)
def glyph_star(x, y, fill):
    pts = "7,0.8 8.9,5 13.4,5.4 10,8.4 11,12.9 7,10.6 3,12.9 4,8.4 0.6,5.4 5.1,5"
    return f'<polygon transform="translate({x} {y})" points="{pts}" fill="{fill}"/>'

def glyph_fork(x, y, stroke):
    return (f'<g transform="translate({x} {y})" fill="none" stroke="{stroke}" stroke-width="1.6" stroke-linecap="round">'
            f'<circle cx="3" cy="2.5" r="1.8"/><circle cx="11" cy="2.5" r="1.8"/><circle cx="7" cy="11.5" r="1.8"/>'
            f'<path d="M3 4.3v1.2c0 1.5 1 2.4 2.5 2.4h3c1.5 0 2.5-.9 2.5-2.4V4.3M7 7.9v1.8"/></g>')

def glyph_clock(x, y, stroke):
    return (f'<g transform="translate({x} {y})" fill="none" stroke="{stroke}" stroke-width="1.6" stroke-linecap="round">'
            f'<circle cx="7" cy="7" r="5.6"/><path d="M7 3.8V7l2.3 1.6"/></g>')

def glyph_calendar(x, y, stroke):
    return (f'<g transform="translate({x} {y})" fill="none" stroke="{stroke}" stroke-width="1.6" stroke-linecap="round">'
            f'<rect x="1" y="2.5" width="12" height="10.5" rx="2"/><path d="M1 6h12M4.5 1v3M9.5 1v3"/></g>')

# -------------------------------------------------------------- banner ----
def banner():
    W, H = 1200, 300
    defs = ('<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">'
            f'<circle cx="2" cy="2" r="1.2" fill="{C["hi"]}"/></pattern>'
            f'<clipPath id="round"><rect width="{W}" height="{H}" rx="18"/></clipPath>'
            f'<linearGradient id="glow" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{C["purple"]}" stop-opacity=".16"/>'
            f'<stop offset="1" stop-color="{C["cyan"]}" stop-opacity="0"/></linearGradient>')
    b = [f'<rect width="{W}" height="{H}" rx="18" fill="{C["bg"]}"/>',
         f'<rect width="{W}" height="{H}" fill="url(#dots)" clip-path="url(#round)"/>',
         f'<rect width="{W}" height="{H}" fill="url(#glow)" clip-path="url(#round)"/>']
    # faint code flourish (stands in for the illustration)
    code = ['// SEC("tracepoint/syscalls/sys_enter_execve")',
            '// bpf_probe_read_kernel(&comm, sizeof(comm), task->comm);',
            '// bpf_ringbuf_submit(evt, 0);']
    for i, s in enumerate(code):
        b.append(text(64, 40 + i * 20, s, 12.5, C["code"]))
    # big decorative braces on the far right
    b.append(text(1188, 262, "}", 190, C["line"], SANS, 700, "end", 'opacity=".5"'))
    # prompt + name
    b.append(text(64, 128, "~ $", 18, C["green"]))
    b.append(text(104, 128, "whoami", 18, C["mute"]))
    b.append(text(62, 190, PROFILE["name"], 62, C["fg"], SANS, 800, extra='letter-spacing="-1.5"'))
    b.append(text(64, 224, " · ".join(PROFILE["lines"]), 17, C["dim"], SANS))
    x = 64
    for label, col in BANNER_CHIPS:
        w = int(len(label) * 8.4 + 24)
        b.append(f'<rect x="{x}" y="246" width="{w}" height="26" rx="13" fill="{C["bg2"]}" stroke="{C[col]}" stroke-width="1.2"/>')
        b.append(text(x + w / 2, 263.5, label, 12.5, C[col], MONO, 500, "middle"))
        x += w + 10
    # terminal window
    tx, ty, tw, th = 720, 42, 416, 216
    b.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="12" fill="{C["bg2"]}" stroke="{C["line"]}"/>')
    b.append(f'<path d="M{tx} {ty+30}H{tx+tw}" stroke="{C["hi"]}"/>')
    for i, col in enumerate(("red", "yellow", "green")):
        b.append(f'<circle cx="{tx+22+i*18}" cy="{ty+15}" r="5.5" fill="{C[col]}"/>')
    b.append(text(tx + tw / 2, ty + 19, "devlsj — zsh", 12, C["mute"], MONO, 400, "middle"))
    y = ty + 56
    for prompt, line in BANNER_TERMINAL:
        px = tx + 20
        if prompt == "$":
            b.append(text(px, y, "$", 14, C["green"]))
            if line is None:
                b.append(f'<rect x="{px+18}" y="{y-13}" width="9" height="16" fill="{C["purple"]}">'
                         f'<animate attributeName="opacity" values="1;1;0;0" dur="1.1s" repeatCount="indefinite"/></rect>')
            else:
                b.append(text(px + 18, y, line, 14, C["fg"]))
        elif prompt == ">":
            b.append(text(px, y, ">", 14, C["purple"]))
            b.append(text(px + 18, y, line, 14, C["dim"]))
        else:
            b.append(text(px, y, line, 14, C["cyan"]))
        y += 24
    return svg(W, H, "\n".join(b), defs)

# ------------------------------------------------------------- profile ----
def profile():
    W, H = 320, 250
    b = [f'<rect width="{W}" height="{H}" rx="16" fill="{C["bg"]}" stroke="{C["line"]}"/>']
    b.append(f'<circle cx="60" cy="66" r="40" fill="{C["panel"]}" stroke="{C["purple"]}" stroke-width="3"/>')
    b.append(text(60, 76, PROFILE["mark"], 28, C["purple"], MONO, 700, "middle"))
    b.append(text(116, 60, PROFILE["name"], 26, C["fg"], SANS, 800))
    b.append(text(116, 84, PROFILE["handle"], 14, C["mute"]))
    b.append(f'<path d="M24 122H296" stroke="{C["line"]}"/>')
    y = 150
    for s in PROFILE["lines"]:
        b.append(text(26, y, "▸", 13, C["purple"]))
        b.append(text(44, y, s, 14, C["dim"], SANS))
        y += 24
    b.append(glyph_calendar(26, 194, C["mute"]))
    b.append(text(48, 206, PROFILE["joined"], 13, C["mute"]))
    b.append(glyph_clock(26, 218, C["mute"]))
    b.append(text(48, 230, PROFILE["tz"], 13, C["mute"]))
    return svg(W, H, "\n".join(b))

# --------------------------------------------------------- stack cards ----
def stack_card(s):
    W, H = 640, 176
    col = C[s["color"]]
    defs = f'<clipPath id="r"><rect width="{W}" height="{H}" rx="14"/></clipPath>'
    b = [f'<rect width="{W}" height="{H}" rx="14" fill="{C["bg"]}" stroke="{C["line"]}"/>',
         f'<rect width="168" height="{H}" fill="{C["panel"]}" clip-path="url(#r)"/>',
         f'<rect x="168" width="{W-168}" height="44" fill="{C["hi"]}" clip-path="url(#r)"/>',
         icon(s["icon"], 84, 88, 76, col),
         text(190, 29, s["name"], 17, col, MONO, 700),
         text(620, 29, s["title"], 11.5, C["dim"], MONO, 400, "end", 'letter-spacing="2"')]
    rows = [("Level", None), ("Used in", s["used"]), ("Specialty", s["specialty"]), ("Style", s["style"])]
    y = 76
    for label, val in rows:
        b.append(text(190, y, label, 12, C["mute"]))
        if val is None:
            for i in range(5):
                f = col if i < s["level"] else C["hi"]
                b.append(f'<rect x="{272+i*22}" y="{y-9}" width="18" height="8" rx="4" fill="{f}"/>')
        else:
            b.append(text(272, y, val, 13, C["fg"], SANS))
        y += 26
    b.append(f'<path d="M456 62V164" stroke="{C["line"]}"/>')
    b.append(glyph_star(474, 68, col)); b.append(text(496, 80, f'level {s["level"]} / 5', 12, C["dim"]))
    b.append(glyph_fork(474, 102, col)); b.append(text(496, 114, f'{s["projects"]} project' + ("s" if s["projects"] > 1 else ""), 12, C["dim"]))
    b.append(glyph_clock(474, 136, col)); b.append(text(496, 148, f'since {s["since"]}', 12, C["dim"]))
    return svg(W, H, "\n".join(b), defs)

# ----------------------------------------------------------- about art ----
def about_art():
    W, H = 200, 200
    b = [f'<rect width="{W}" height="{H}" rx="14" fill="{C["bg"]}" stroke="{C["line"]}"/>']
    layers = [("dashboard", "userspace · React", "cyan", 22),
              ("detector", "rules · ML model", "purple", 76),
              ("kernel", "eBPF probes", "green", 130)]
    for name, sub, col, y in layers:
        b.append(f'<rect x="16" y="{y}" width="168" height="44" rx="10" fill="{C["panel"]}" stroke="{C[col]}" stroke-opacity=".6"/>')
        b.append(f'<circle cx="32" cy="{y+22}" r="4" fill="{C[col]}"/>')
        b.append(text(46, y + 19, name, 13, C["fg"], MONO, 700))
        b.append(text(46, y + 35, sub, 11, C["mute"], MONO))
    # flowing events kernel -> detector -> dashboard
    for y0, y1 in ((130, 120), (76, 66)):
        b.append(f'<path d="M170 {y0}V{y1}" stroke="{C["line"]}" stroke-width="2"/>')
        b.append(f'<circle cx="170" cy="{y0}" r="3" fill="{C["purple"]}">'
                 f'<animate attributeName="cy" values="{y0};{y1}" dur="1.2s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="1;0" dur="1.2s" repeatCount="indefinite"/></circle>')
    b.append(text(100, 190, "trace → detect → respond", 11, C["mute"], MONO, 400, "middle"))
    return svg(W, H, "\n".join(b))

# --------------------------------------------------------------- icons ----
def pin_icon(name, col):
    fill = C[col]
    b = [f'<rect width="40" height="40" rx="10" fill="{C["panel"]}" stroke="{C["line"]}"/>', icon(name, 20, 20, 22, fill)]
    return svg(40, 40, "\n".join(b))

# ---------------------------------------------------------------- main ----
def main():
    OUT.mkdir(exist_ok=True)
    (OUT / "banner.svg").write_text(banner())
    (OUT / "profile.svg").write_text(profile())
    (OUT / "about.svg").write_text(about_art())
    for s in STACKS:
        (OUT / f'stack-{s["id"]}.svg').write_text(stack_card(s))
    for name, col in PIN_ICONS:
        (OUT / f"icon-{name}.svg").write_text(pin_icon(name, col))
    print("wrote", len(list(OUT.glob("*.svg"))), "svg files to", OUT)

if __name__ == "__main__":
    main()


# =====================================================================
#  Text blocks as SVG (so the two-column table can shrink at any width)
# =====================================================================
import re as _re

KO_SANS = ("-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo','Segoe UI','Malgun Gothic',"
           "'Noto Sans KR',Roboto,Helvetica,Arial,sans-serif")

TEXT = dict(
    now_title="now",
    now_sub="2026 · 캡스톤 프로젝트",
    now=[
        "**eBPF-Trace** — 리눅스 커널 레벨에서 공급망 공격을 탐지하는 시스템을 만들고 있습니다.",
        "eBPF 프로브로 커널 이벤트를 수집하고, 탐지 규칙과 ML 모델로 판별한 뒤, 대응 에이전트와 React 대시보드까지 이어지는 흐름을 직접 구현 중입니다.",
    ],
    pinned=[
        dict(id="ebpf-trace", icon="linux", color="blue", name="eBPF-Trace", desc="커널 레벨 공급망 공격 탐지 · Python / C / TS"),
        dict(id="adminweb", icon="openjdk", color="orange", name="AdminWeb", desc="Company solution 관리자 웹 · Java / TS"),
        dict(id="jansangtravel", icon="kotlin", color="purple", name="JansangTravel", desc="모바일 프로그래밍 텀프로젝트 · Kotlin"),
        dict(id="cli-crypto", icon="c", color="blue", name="CLI_Crypto", desc="Crypto Programming Project"),
    ],
    interests=[
        ("#eBPF", "kernel tracing"),
        ("#Linux", "systems programming"),
        ("#Security", "supply-chain attack detection"),
        ("#Android", "Kotlin mobile apps"),
        ("#Backend", "Java · Python · PostgreSQL"),
    ],
    tools=["docker", "terraform", "postgresql", "fastapi", "spring", "android", "gnubash", "github"],
    about=[
        "안녕하세요, 컴퓨터소프트웨어공학을 전공하는 주니어 개발자 **DevLSJ**입니다.",
        "Kotlin으로 모바일 앱을, Java와 TypeScript로 관리자 웹을, Python으로 탐지 서비스를 만들어 봤습니다. 지금은 **eBPF**로 리눅스 커널 레벨에서 공급망 공격을 잡아내는 캡스톤 프로젝트에 집중하고 있습니다.",
        "애플리케이션 위에서만 보던 문제를 커널 아래에서 다시 보는 일에 재미를 붙였고, 새 시스템 기술은 읽는 것보다 직접 만들어 보면서 배우는 편입니다.",
    ],
    about_updated="2026-09-28",
)

def _cw(ch):
    o = ord(ch)
    if o >= 0x2E80: return 0.96          # CJK: roughly square glyphs
    if ch == " ": return 0.28
    if ch in "iljtfI.,:;'|!·": return 0.32
    if ch.isupper() or ch in "mw": return 0.68
    return 0.54

def _w(s, size): return sum(_cw(c) for c in s) * size

_SEG = _re.compile(r"\*\*(.+?)\*\*|`(.+?)`|([^*`]+)")
def _segs(word):
    out = []
    for m in _SEG.finditer(word):
        if m.group(1): out.append((m.group(1), "b"))
        elif m.group(2): out.append((m.group(2), "c"))
        else: out.append((m.group(3), ""))
    return out

def wrap(par, size, max_w):
    """-> list of lines; each line = list of (text, style)."""
    lines, cur, cur_w = [], [], 0.0
    for word in par.split(" "):
        segs = _segs(word)
        ww = sum(_w(t, size) for t, _ in segs)
        sp = _w(" ", size) if cur else 0
        if cur and cur_w + sp + ww > max_w:
            lines.append(cur); cur, cur_w, sp = [], 0.0, 0
        if ww > max_w:                        # break an over-long word by characters
            for t, st in segs:
                for ch in t:
                    cw = _w(ch, size)
                    if cur and cur_w + cw > max_w:
                        lines.append(cur); cur, cur_w = [], 0.0
                    cur.append((ch, st)); cur_w += cw
            continue
        if sp: cur.append((" ", "")); cur_w += sp
        cur.extend(segs); cur_w += ww
    if cur: lines.append(cur)
    return lines

def rich_text(x, y, lines, size, lh, fill=None, accent=None, font=KO_SANS):
    fill = fill or C["fg"]; accent = accent or C["purple"]
    out = []
    for i, line in enumerate(lines):
        spans = []
        for t, st in line:
            t = t.replace("&", "&amp;").replace("<", "&lt;")
            if st == "b": spans.append(f'<tspan font-weight="700">{t}</tspan>')
            elif st == "c": spans.append(f'<tspan fill="{accent}" font-weight="700">{t}</tspan>')
            else: spans.append(t)
        out.append(f'<text x="{x}" y="{y + i*lh}" font-family="{font}" font-size="{size}" fill="{fill}" xml:space="preserve">{"".join(spans)}</text>')
    return "\n".join(out)

def heading(x, y, s, size=20):
    return text(x, y, f":: {s}", size, C["fg"], KO_SANS, 800)

def paragraphs(pars, x, y, size, lh, max_w, gap):
    """Render paragraphs; returns (svg, y_after)."""
    out = []
    for p in pars:
        ls = wrap(p, size, max_w)
        out.append(rich_text(x, y, ls, size, lh))
        y += len(ls) * lh + gap
    return "\n".join(out), y - gap

def card(W, H, body, rx=16):
    return svg(W, H, f'<rect width="{W}" height="{H}" rx="{rx}" fill="{C["bg"]}" stroke="{C["line"]}"/>\n{body}')

# ---- sidebar blocks (320 wide) ----
def now_block():
    W, pad, size, lh = 320, 22, 13, 20
    body, y = paragraphs(TEXT["now"], pad, 96, size, lh, (W - 2*pad) * 0.94, 10)
    H = y + 22
    b = [heading(pad, 42, TEXT["now_title"]), text(pad, 68, TEXT["now_sub"], 11.5, C["mute"], MONO)]
    return card(W, H, "\n".join(b) + "\n" + body)

def section_header(W, s):
    return svg(W, 46, heading(6, 34, s))

def pinned_row(p):
    W, H = 320, 64
    col = C[p["color"]]
    b = [f'<rect width="{W}" height="{H}" rx="12" fill="{C["bg"]}" stroke="{C["line"]}"/>',
         f'<rect x="12" y="12" width="40" height="40" rx="10" fill="{C["panel"]}"/>', icon(p["icon"], 32, 32, 22, col),
         text(66, 28, p["name"], 14, C["blue"], KO_SANS, 800),
         text(W - 18, 29, "↗", 13, C["mute"], KO_SANS, 400, "end"),
         text(66, 48, p["desc"], 11, C["dim"], KO_SANS)]
    return svg(W, H, "\n".join(b))

def interests_block():
    W, pad = 320, 22
    rows = TEXT["interests"]
    H = 60 + len(rows) * 30 + 14
    b = [heading(pad, 42, "interests")]
    y = 80
    for tag, sub in rows:
        b.append(text(pad, y, tag, 14, C["fg"], KO_SANS, 800))
        b.append(text(pad + 98, y, sub, 11.5, C["mute"], KO_SANS))
        y += 30
    return card(W, H, "\n".join(b))

def tools_block():
    W, pad = 320, 22
    names = TEXT["tools"]
    b = [heading(pad, 42, "tools")]
    x = pad
    for n in names:
        col = dict(PIN_ICONS).get(n, "fg")
        b.append(f'<rect x="{x}" y="60" width="32" height="32" rx="8" fill="{C["panel"]}" stroke="{C["line"]}"/>')
        b.append(icon(n, x + 16, 76, 18, C[col]))
        x += 34
    return card(W, 112, "\n".join(b))

# ---- main blocks (640 wide) ----
def about_block():
    W, pad, size, lh = 640, 24, 13.5, 21
    art_w, art_x = 200, W - pad - 200
    text_w = art_x - pad - 20
    body, y = paragraphs(TEXT["about"], pad, 90, size, lh, text_w * 0.94, 12)
    H = max(y, 60 + 200) + 52
    b = [heading(pad, 42, "about me"),
         f'<path d="M{W-38} 0h16v30l-8-6-8 6z" fill="{C["purple"]}"/>',            # bookmark
         f'<g transform="translate({art_x} 60)">{_about_art_inner()}</g>',
         f'<path d="M{pad} {H-30}H{W-pad}" stroke="{C["line"]}"/>',
         f'<rect x="{pad}" y="{H-22}" width="58" height="16" rx="3" fill="{C["purple"]}"/>',
         text(pad + 29, H - 10, "POSTED", 9, C["bg"], MONO, 800, "middle", 'letter-spacing="1.5"'),
         text(pad + 68, H - 10, TEXT["about_updated"], 11, C["dim"], MONO)]
    return card(W, H, "\n".join(b) + "\n" + body)

def _about_art_inner():
    # 200x200 version of the trace → detect → respond illustration
    b = [f'<rect width="200" height="200" rx="14" fill="{C["panel"]}" stroke="{C["line"]}"/>']
    layers = [("dashboard", "userspace · React", "cyan", 22), ("detector", "rules · ML model", "purple", 76), ("kernel", "eBPF probes", "green", 130)]
    for name, sub, col, y in layers:
        b.append(f'<rect x="16" y="{y}" width="168" height="44" rx="10" fill="{C["bg"]}" stroke="{C[col]}" stroke-opacity=".6"/>')
        b.append(f'<circle cx="32" cy="{y+22}" r="4" fill="{C[col]}"/>')
        b.append(text(46, y + 19, name, 13, C["fg"], MONO, 700))
        b.append(text(46, y + 35, sub, 11, C["mute"], MONO))
    for y0, y1 in ((130, 120), (76, 66)):
        b.append(f'<path d="M170 {y0}V{y1}" stroke="{C["line"]}" stroke-width="2"/>')
        b.append(f'<circle cx="170" cy="{y0}" r="3" fill="{C["purple"]}"><animate attributeName="cy" values="{y0};{y1}" dur="1.2s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0" dur="1.2s" repeatCount="indefinite"/></circle>')
    b.append(text(100, 190, "trace → detect → respond", 11, C["mute"], MONO, 400, "middle"))
    return "\n".join(b)

def main_blocks():
    OUT.mkdir(exist_ok=True)
    (OUT / "now.svg").write_text(now_block())
    (OUT / "h-pinned.svg").write_text(section_header(320, "pinned"))
    for p in TEXT["pinned"]:
        (OUT / f'pinned-{p["id"]}.svg').write_text(pinned_row(p))
    (OUT / "interests.svg").write_text(interests_block())
    (OUT / "tools.svg").write_text(tools_block())
    (OUT / "about.svg").write_text(about_block())
    (OUT / "h-stack.svg").write_text(section_header(640, "tech stack"))
    (OUT / "h-activity.svg").write_text(section_header(640, "activity"))
    print("wrote text blocks")

if __name__ == "__main__":
    main_blocks()
