"""Socials 26 Oct — "if I had to learn AI from zero, here's exactly what I'd do". New style: Route.

Route = his footage untouched; cobalt pages that wipe in on a lime line; one transit-map route
(ZERO -> ONE TOOL -> WEEK 1 -> WEEK 2 -> BUILDER) that a lime train travels as the video moves on,
mirrored by a small route HUD over his footage; real logos on white tiles; captions above his head,
the spoken word in a lime block. Red Hat Display + DIN Alternate.
Two versions (tools/TRIAL-REELS.md): TRIAL=1 main (his hook, full), TRIAL=2 contrarian-first and tight.
Run from the project root:  TRIAL=1 python3 -I edit/build.py  ->  ../2026-10-26-socials-trials/out/trial-1.html
"""
import html
import json
import math
import os
import re

N = int(os.environ.get("TRIAL", "1"))
D = f"edit/trials/{N}"
TOK = json.load(open(f"{D}/tokens.json"))
SEGS = json.load(open(f"{D}/words.json"))["segments"]
AROLL_END = SEGS[-1]["end"]
TAIL = 1.6
DURATION = round(AROLL_END + TAIL, 3)
COB, COBD, NAVY, LIME = "#1838f0", "#0f27c4", "#0a176e", "#d4ff3c"
CUTS = [g["start"] for g in SEGS[1:]]


# ---------------------------------------------------------------- words
def norm(s):
    return re.sub(r"[^a-z0-9'£]", "", s.lower().replace("’", "'"))


NT = [norm(x["text"]) for x in TOK]


def w(phrase, after=0.0):
    ws = [norm(p) for p in phrase.split()]
    for i in range(len(NT) - len(ws) + 1):
        if TOK[i]["start"] >= after - 1e-6 and NT[i:i + len(ws)] == ws:
            return i
    raise KeyError(f"trial {N}: '{phrase}' not in the cut")


def has(phrase):
    try:
        w(phrase)
        return True
    except KeyError:
        return False


def t(i):
    return TOK[i]["start"] if i < len(TOK) else AROLL_END


def seg_end_at(x):
    return next((s["end"] for s in SEGS if s["start"] - 0.01 <= x < s["end"]), AROLL_END)


def te(i):
    """End of word i: the next word's start, or the end of its take."""
    return min(t(i + 1), seg_end_at(t(i)))


def esc(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------- timeline helpers
scenes, js, sfx = [], [], []
CUR = '<svg viewBox="0 0 24 24"><path d="M5 3 L5 19 L9 15 L12 22 L15 20.5 L11.5 14 L18 14 Z" fill="#fff" stroke="#0a176e" stroke-width="1.4" stroke-linejoin="round"/></svg>'
TICK = '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7"/></svg>'
MAPBG = ('<svg class="map" viewBox="0 0 1080 1920"><g fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" stroke-linejoin="round">'
         '<path d="M-40 420 H380 L620 180 H1120"/><path d="M-40 1500 H220 L520 1800 H1120"/><path d="M960 -40 V640 L760 840 V2000"/>'
         '<path d="M120 -40 V300 L300 480 V900 L80 1120 V2000"/></g></svg>')


def scene(sid, start, end, body, whoosh=True, bg=None):
    for c in CUTS:  # never flash a new take before a page: a page that starts just after a cut starts on it
        if c <= start < c + 0.4:
            start = c - 0.02
    start = math.floor(start * 30 + 1e-6) / 30 - 0.002
    scenes.append((sid, start, end, body, bg))
    js.append(f"enter('#{sid}', {start:.3f});")
    if whoosh:
        sfx.append(("fast-whoosh", max(0, start - 0.28), 0.32))
    return start


def ft(sel, at, a, b, d=0.35, e="power3.out", ir=None):
    b = dict(b, duration=round(d, 3), ease=e)
    if ir is not None:
        b["immediateRender"] = ir
    js.append(f"tl.fromTo('{sel}', {json.dumps(a)}, {json.dumps(b)}, {at:.3f});")


def to(sel, at, b, d=0.3, e="power2.out"):
    js.append(f"tl.to('{sel}', {json.dumps(dict(b, duration=round(d, 3), ease=e, immediateRender=False))}, {at:.3f});")


def st(sel, at, b):
    js.append(f"tl.set('{sel}', {json.dumps(b)}, {at:.3f});")


def rev(sel, at, y=26):
    js.append(f"rev('{sel}', {at:.3f}, {{\"y\": {y}}});")


def pop(sel, at, s=0.5, y=20, d=0.36, ir=None):
    ft(sel, at, {"opacity": 0, "scale": s, "y": y}, {"opacity": 1, "scale": 1, "y": 0}, d, "back.out(2)", ir)


def slam(sel, at, s=1.6):
    ft(sel, at, {"opacity": 0, "scale": s, "filter": "blur(16px)"}, {"opacity": 1, "scale": 1, "filter": "blur(0px)"}, 0.38, "expo.out")


def mask_up(sel, at):
    ft(sel, at, {"opacity": 0, "y": 60, "clipPath": "inset(0% 0% 100% 0%)"}, {"opacity": 1, "y": 0, "clipPath": "inset(0% 0% -20% 0%)"}, 0.4, "expo.out")


def words_in(pfx, i0, n, cls="h3"):
    """Lead-in words that land one by one with his voice, each a different way."""
    spans = []
    for k in range(n):
        spans.append(f'<span class="ch {cls}" id="{pfx}{k}">{esc(disp(i0 + k))}</span>')
        at = t(i0 + k) - 0.05
        [rev, lambda s, a: pop(s, a, 0.6, 14, 0.3), lambda s, a: ft(s, a, {"opacity": 0, "x": -30}, {"opacity": 1, "x": 0}, 0.28)][k % 3](f"#{pfx}{k}", at)
    return " ".join(spans)


def disp(i):
    return TOK[i]["text"].strip(",.!?;:")


def click(cur, x, y, at, frm=(1150, 1500), leave=None, first=True):
    """A cursor glides in and clicks exactly at (x, y) (its tip is at 14, 8)."""
    ft(cur, at - 0.6, {"x": frm[0], "y": frm[1], "opacity": 0, "scale": 1}, {"x": x - 14, "y": y - 8, "opacity": 1}, 0.55, "power3.out", None if first else False)
    to(cur, at, {"scale": 0.8, "yoyo": True, "repeat": 1}, 0.08)
    if leave:
        to(cur, at + 0.35, {"x": leave[0], "y": leave[1], "opacity": 0}, 0.45, "power2.in")
    sfx.append(("click_002", at, 0.45))


def count(sel, at, a, b, d, fmt="{}", ease="power2.out"):
    js.append(f"(function(){{ const o = {{v:{a}}}; tl.fromTo(o, {{v:{a}}}, {{v:{b}, duration:{d:.3f}, ease:'{ease}', onUpdate(){{ const e = document.querySelector('{sel}'); if (e) e.textContent = {json.dumps(fmt)}.replace('{{}}', Math.round(o.v).toLocaleString('en-GB')); }}}}, {at:.3f}); }})();")


def typer(sel, text, a, b, clicks=True):
    js.append(f"(function(){{ const s = {json.dumps(text)}, o = {{n:0}}; tl.fromTo(o, {{n:0}}, {{n:s.length, duration:{max(b - a, 0.05):.3f}, ease:'none', onUpdate(){{ const e = document.querySelector('{sel}'); if (e) e.textContent = s.slice(0, Math.round(o.n)); }}}}, {a:.3f}); }})();")
    if clicks:
        k = max(1, len(text) // 3)
        sfx.extend([("click_004", a + (b - a) * j / k, 0.07) for j in range(k)])


ICON = {
    "dumbbell": '<path d="M6.5 6.5v11M17.5 6.5v11M3.5 9v6M20.5 9v6M6.5 12h11"/>',
    "cal": '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M8 3v4M16 3v4M3 10h18"/>',
    "wallet": '<path d="M4 7.5A2.5 2.5 0 0 1 6.5 5H18v3"/><rect x="4" y="8" width="16" height="11" rx="2.5"/><circle cx="16" cy="13.5" r="1.3"/>',
    "bulb": '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.6 10.8c.7.6 1.1 1.3 1.1 2.2h5c0-.9.4-1.6 1.1-2.2A6 6 0 0 0 12 3z"/>',
    "sun": '<circle cx="12" cy="12" r="4.5"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/>',
    "moon": '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-7 8-7s8 3 8 7"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6"/><circle cx="17" cy="9" r="2.6"/><path d="M16.2 14.2c3 .3 5.3 2.4 5.3 5.8"/>',
    "zap": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "msg": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20.5l1.4-4.7A8 8 0 1 1 21 12z"/>',
    "hammer": '<path d="M14 6l4 4M3 21l9-9M12.5 4.5l7 7-2.5 2.5-7-7z"/>',
    "music": '<path d="M9 18V5l11-2v13"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="17.5" cy="16" r="2.5"/>',
    "folder": '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    "brain": '<path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 3 3h0V4zM15 4a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-3 3V4z"/>',
    "plug": '<path d="M9 2v5M15 2v5M6 7h12v4a6 6 0 0 1-12 0zM12 17v5"/>',
    "code": '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M13.5 4l-3 16"/>',
    "doc": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
    "list": '<path d="M9 6h12M9 12h12M9 18h12"/><circle cx="4.5" cy="6" r="1.2"/><circle cx="4.5" cy="12" r="1.2"/><circle cx="4.5" cy="18" r="1.2"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "play": '<path d="M7 4.5v15l12.5-7.5z"/>',
}


def ic(name, size=58, cls="ico", sw=2.2):
    return f'<svg class="{cls}" viewBox="0 0 24 24" style="width:{size}px;height:{size}px;stroke-width:{sw}">{ICON[name]}</svg>'


def logo(name, size=64):
    return f'<img src="assets/img/logos/{name}.svg" style="width:{size}px;height:{size}px;object-fit:contain"/>'


def tick_at(sel, at, sound=True):
    pop(sel, at, 0.2, 0, 0.32)
    if sound:
        sfx.append(("tick_002", at, 0.3))


# ---------------------------------------------------------------- the route (transit map)
RPTS = [(230, 1700), (230, 1290), (420, 1100), (850, 1100), (850, 740), (660, 550), (470, 550)]
SEGL = [math.dist(RPTS[k], RPTS[k + 1]) for k in range(len(RPTS) - 1)]
RLEN = sum(SEGL)
STATIONS = [  # name, sub, point, label side
    ("ZERO", "where you start", (230, 1700), "r"),
    ("ONE TOOL", "GPT or Claude", (230, 1390), "r"),
    ("WEEK 1", "use it for real stuff", (630, 1100), "d"),
    ("WEEK 2", "build something", (850, 880), "l"),
    ("BUILDER", "", (470, 550), "u"),
]


def arclen(p):
    """Distance along the route to point p (a point on it)."""
    s = 0.0
    for k in range(len(RPTS) - 1):
        a, b = RPTS[k], RPTS[k + 1]
        if abs(math.dist(a, p) + math.dist(p, b) - SEGL[k]) < 0.5:
            return s + math.dist(a, p)
        s += SEGL[k]
    raise ValueError(p)


SARC = [arclen(s[2]) for s in STATIONS]
RPATH = "M" + " L".join(f"{x},{y}" for x, y in RPTS)


def route_body(rid, lit, sub_over=None, fill_to=None, train_at=None):
    """The route map. lit = stations already lit; fill_to = arc length already filled."""
    sub_over = sub_over or {}
    fill_to = SARC[lit - 1] if fill_to is None and lit else (fill_to or 0)
    stn = []
    for k, (name, sub, (x, y), side) in enumerate(STATIONS):
        sub = sub_over.get(k, sub)
        on = k < lit
        stn.append(f'<div class="stn" id="{rid}-s{k}" style="left:{x}px;top:{y}px"><i style="{"opacity:1;transform:scale(1)" if on else ""}"></i><b class="ring"></b></div>')
        if side == "r":
            lx, ly, al = x + 70, y - 44, "left"
        elif side == "l":
            lx, ly, al = x - 70, y - 44, "right"
        elif side == "d":
            lx, ly, al = x, y + 52, "center"
        else:
            lx, ly, al = x, y - 150, "center"
        anchor = {"left": f"left:{lx}px", "right": f"right:{1080 - lx}px", "center": f"left:{lx - 300}px;width:600px;text-align:center"}[al]
        big = "font-size:96px;" if name == "BUILDER" else ""
        stn.append(f'<div class="abs" id="{rid}-l{k}" style="{anchor};top:{ly}px;text-align:{al}"><div class="sname" style="{big}position:relative" id="{rid}-n{k}">{name}</div>'
                   f'<div class="ssub" style="position:relative;margin-top:12px" id="{rid}-u{k}">{esc(sub)}</div></div>')
    tx, ty = point_at(fill_to if train_at is None else train_at)
    return f"""
  <svg class="abs" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920">
    <path class="rline rtrack" id="{rid}-trk" d="{RPATH}" style="stroke-dasharray:{RLEN:.1f} {RLEN + 60:.1f};stroke-dashoffset:0"/>
    <path class="rline rfill" id="{rid}-fil" d="{RPATH}" style="stroke-dasharray:{RLEN:.1f} {RLEN + 60:.1f};stroke-dashoffset:{RLEN - fill_to if fill_to > 0 else RLEN + 30:.1f}"/>
  </svg>
  {''.join(stn)}
  <div class="train" id="{rid}-tr" style="left:{tx:.0f}px;top:{ty:.0f}px;opacity:{1 if lit else 0}"><span>&#9650;</span></div>"""


def point_at(s):
    for k in range(len(RPTS) - 1):
        if s <= SEGL[k] or k == len(RPTS) - 2:
            f = min(1, s / SEGL[k])
            a, b = RPTS[k], RPTS[k + 1]
            return a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
        s -= SEGL[k]


def train(rid, s0, s1, at, d, light_end=True):
    """The train runs the route from arc s0 to s1 (sine in-out); the lime fill follows it; stations it reaches light up."""
    pts = json.dumps(RPTS)
    js.append(f"(function(){{ const P = {pts}, L = {json.dumps([round(x, 2) for x in SEGL])}, o = {{s:{s0:.1f}}};"
              f" function at(s){{ for (let k = 0; k < L.length; k++) {{ if (s <= L[k] || k == L.length - 1) {{ const f = Math.min(1, s / L[k]); return [P[k][0] + (P[k+1][0]-P[k][0])*f, P[k][1] + (P[k+1][1]-P[k][1])*f]; }} s -= L[k]; }} }}"
              f" tl.fromTo(o, {{s:{s0:.1f}}}, {{s:{s1:.1f}, duration:{d:.3f}, ease:'sine.inOut', immediateRender:false, onUpdate(){{ const p = at(o.s), tr = document.getElementById('{rid}-tr'), f = document.getElementById('{rid}-fil');"
              f" if (tr) {{ tr.style.left = p[0] + 'px'; tr.style.top = p[1] + 'px'; }} if (f) f.style.strokeDashoffset = ({RLEN:.1f} - o.s); }}}}, {at:.3f}); }})();")
    for k, sa in enumerate(SARC):
        if s0 < sa <= s1 + 0.5 and (light_end or sa < s1 - 0.5):
            f = (sa - s0) / (s1 - s0)
            arrive = at + d * math.acos(1 - 2 * f) / math.pi
            light(rid, k, arrive)
    sfx.append(("arrow-whoosh", at, 0.22))


def light(rid, k, at, big=False):
    ft(f"#{rid}-s{k} i", at, {"opacity": 0, "scale": 0.4}, {"opacity": 1, "scale": 1}, 0.3, "back.out(2.4)")
    ft(f"#{rid}-s{k} .ring", at, {"opacity": 0.9, "scale": 0.6}, {"opacity": 0, "scale": 1.6 if not big else 2.4}, 0.7, "power2.out")
    ft(f"#{rid}-n{k}", at, {"color": "#ffffff"}, {"color": LIME}, 0.25, "power1.out")
    sfx.append(("confirmation_002" if big else "pluck_001", at, 0.3 if not big else 0.4))


# ---------------------------------------------------------------- HUD over his footage
HUD_ST = [70 + 760 * k / 4 for k in range(5)]
HUD_NAMES = ["ZERO", "ONE TOOL", "WEEK 1", "WEEK 2", "BUILDER"]
hud_js = []


def hud_html():
    sts = "".join(f'<div class="st" id="hs{k}" style="left:{x:.0f}px"></div><div class="lb" style="left:{x:.0f}px">{n}</div>' for k, (x, n) in enumerate(zip(HUD_ST, HUD_NAMES)))
    return f'<div id="hud"><div class="pill"></div><div class="trk"></div><div class="fil" id="hfil"></div>{sts}<div class="me" id="hme" style="left:{HUD_ST[0]:.0f}px"></div></div>'


def hud_show(at):
    hud_js.append(f"tl.fromTo('#hud', {{opacity:0, y:-30}}, {{opacity:1, y:0, duration:.45, ease:'expo.out'}}, {at:.3f});")


def hud_go(k, at):
    """Move the HUD to station k (fill + 'you are here' dot), lighting the station."""
    hud_js.append(f"tl.to('#hfil', {{scaleX:{k / 4:.3f}, duration:.6, ease:'sine.inOut', immediateRender:false}}, {at:.3f});")
    hud_js.append(f"tl.to('#hme', {{x:{HUD_ST[k] - HUD_ST[0]:.0f}, duration:.6, ease:'sine.inOut', immediateRender:false}}, {at:.3f});")
    hud_js.append(f"tl.fromTo('#hud', {{scale:1}}, {{scale:1.12, duration:.25, yoyo:true, repeat:1, ease:'power2.out', immediateRender:false}}, {at:.3f});")
    sfx.append(("pluck_001", at + 0.45, 0.22))
    for j in range(k + 1):
        hud_js.append(f"tl.to('#hs{j}', {{backgroundColor:'{LIME}', borderColor:'{LIME}', duration:.2, immediateRender:false}}, {at + 0.4:.3f});")


# ================================================================= pages
def pg_hook_route(rid="p1"):
    """'here's exactly what I would do' — the plan draws: the track runs up, each station lands as the line reaches it."""
    i = w("here's exactly what i would do")
    s, e = t(i) - 0.1, te(i + 5) + 0.55
    lead = words_in(f"{rid}w", i, 6, "h2")
    s = scene(rid, s, e, f"""
  <div class="stack" style="top:150px;padding:0 60px"><div style="display:flex;flex-wrap:wrap;justify-content:center;gap:0 22px">{lead}</div></div>
  {route_body(rid, 0)}""")
    js.append(f"tl.set('#{rid}-trk', {{strokeDashoffset:{RLEN + 30:.1f}}}, 0);")
    d = max(0.9, min(1.3, e - s - 1.05))
    ft(f"#{rid}-trk", s + 0.15, {"strokeDashoffset": RLEN + 30}, {"strokeDashoffset": 0}, d, "none")
    for k, sa in enumerate(SARC):
        at = s + 0.15 + d * sa / RLEN
        pop(f"#{rid}-s{k}", at - 0.04, 0.2, 0, 0.3)
        mask_up(f"#{rid}-n{k}", at)
        rev(f"#{rid}-u{k}", at + 0.08, 14)
        sfx.append(("pluck_002" if k < 4 else "pluck_001", at, 0.22))
    for k in range(5):
        st(f"#{rid}-s{k}", s, {"opacity": 0})
        st(f"#{rid}-n{k}", s, {"opacity": 0})
        st(f"#{rid}-u{k}", s, {"opacity": 0})
    return s, e


def pg_days():
    """'every single day' — a month of day cells, each ticks lime in a diagonal ripple."""
    i = w("every single day")
    s, e = t(i) - 0.08, te(i + 2) + 0.35
    cells = []
    for r in range(5):
        for c in range(7):
            cells.append(f'<div class="cell" id="dy{r * 7 + c}" style="left:{88 + c * 132}px;top:{720 + r * 132}px;width:112px;height:112px"><i></i></div>')
    s = scene("p2", s, e, f"""
  <div class="stack" style="top:430px"><span class="lab">i build with ai</span><span class="h1" id="dy-t" style="margin-top:22px">every single <span class="hl">day</span></span></div>
  {''.join(cells)}""")
    rev("#dy-t", s + 0.05, 30)
    span = max(0.6, e - s - 0.55)
    for k in range(35):
        r, c = divmod(k, 7)
        at = s + 0.15 + span * (r + c) / 10
        ft(f"#dy{k} i", at, {"scale": 0}, {"scale": 1}, 0.22, "back.out(2)")
        if k % 5 == 0:
            sfx.append(("click_004", at, 0.08))


def pg_tools(var):
    """'I'd skip the fifty different AI tool lists' — a '50 AI tools' list floods with real logos, then gets skipped."""
    i = w("i'd skip the 50")
    i50 = i + 3
    il = w("lists", t(i))
    s, e = t(i) - 0.05, t(il) + 0.5
    if var == "feed":  # the contrarian hook: his face first, the feed lands on '50'
        s, e = t(i50) - 0.2, te(il) + 0.25
    LG = sorted(os.listdir("assets/img/logos"))
    LG = [x[:-4] for x in LG if x.endswith(".svg")]
    tiles = []
    n = 48
    for k in range(n):
        r, c = divmod(k, 6)
        tiles.append(f'<div class="tile" id="tl{k}" style="left:{110 + c * 150}px;top:{600 + r * 128}px;width:110px;height:110px;border-radius:26px">{logo(LG[k % len(LG)], 66)}</div>')
    if var == "grid":
        s = scene("p3", s, e, f"""
  <div class="card" id="tl-card" style="left:50px;right:50px;top:330px;height:1500px;background:rgba(255,255,255,.08);box-shadow:none;border:4px solid rgba(255,255,255,.18)"></div>
  <div class="stack" style="top:380px"><span class="lab" style="color:#fff">save this ↓</span><span class="h2" style="margin-top:14px">TOP <span id="tl-n" class="lime">0</span> AI TOOLS</span><span class="h3" style="color:var(--mute);margin-top:8px;font-size:44px">you need to know in 2026</span></div>
  {''.join(tiles)}
  <div class="btn" id="tl-skip" style="left:330px;width:420px;top:1660px;height:120px">SKIP &#9654;&#9654;</div>
  <div class="cursor" id="tl-cur">{CUR}</div>""")
        a, b = t(i50) - 0.15, t(il) - 0.05
        count("#tl-n", a, 0, 50, b - a, "{}", "none")
        for k in range(n):
            at = a + (b - a) * k / n
            pop(f"#tl{k}", at, 0.3, 30, 0.3)
            if k % 4 == 0:
                sfx.append(("hard-pop-click", at, 0.1))
        pop("#tl-skip", b - 0.35, 0.6, 20)
        cl = t(il) - 0.02
        click("#tl-cur", 540, 1720, cl, frm=(1100, 1900))
        for k in range(n):  # everything is swept off the screen, left
            to(f"#tl{k}", cl + 0.08 + (k % 6) * 0.015, {"x": -1100, "rotation": -8, "opacity": 0}, 0.38, "power3.in")
        to("#tl-card", cl + 0.08, {"x": -1100, "opacity": 0}, 0.4, "power3.in")
        sfx.append(("scratch_002", cl + 0.1, 0.25))
        return
    # var feed: a phone feed of '50 AI tools' posts scrolling fast; a cursor swipes it away
    posts = []
    titles = ["TOP 50 AI TOOLS", "50 AI TOOLS YOU NEED", "AI TOOLS LIST #47", "50 MORE AI TOOLS", "BEST AI TOOLS 2026"]
    for k in range(5):
        lg = "".join(f'<div class="tile" style="position:relative;width:96px;height:96px;border-radius:24px">{logo(LG[(k * 9 + j) % len(LG)], 58)}</div>' for j in range(8))
        posts.append(f'<div class="card" style="left:40px;right:40px;top:{180 + k * 860}px;height:820px;border-radius:44px;background:#fff;padding:54px 44px">'
                     f'<div class="lab" style="color:rgba(10,23,110,.55)">@ai.tools.daily · {k + 2}h</div><div class="h2 ink" style="margin-top:20px;font-size:76px">{titles[k]}</div>'
                     f'<div style="display:flex;flex-wrap:wrap;gap:18px;margin-top:40px">{lg}</div>'
                     f'<div class="cl" style="font-size:36px;margin-top:40px">save this before it\'s gone &#128190;</div></div>')
    s = scene("p3", s, e, f"""
  <div class="phone" id="fd-ph" style="left:150px;top:300px;width:780px;height:1500px;border-radius:96px"><div class="screen" style="border-radius:76px;background:#e9ecff">
   <div id="fd-col" class="abs" style="left:0;right:0;top:0">{''.join(posts)}</div></div><div class="notch"></div></div>
  <div class="stack" style="top:130px"><span class="h2"><span class="lime" id="fd-n">0</span> AI tools</span></div>
  <div class="cursor" id="fd-cur">{CUR}</div>""")
    a, b = t(i50) - 0.15, t(il) - 0.05
    count("#fd-n", a, 0, 50, b - a, "{}", "none")
    ft("#fd-col", s + 0.1, {"y": 0}, {"y": -3440}, b - s - 0.1, "power1.inOut")
    sfx.extend([("scratch_002", s + 0.2 + k * 0.4, 0.08) for k in range(int((b - s) / 0.4))])
    cl = t(il) + 0.1
    ft("#fd-cur", cl - 0.45, {"x": 1100, "y": 1200, "opacity": 0}, {"x": 760, "y": 1100, "opacity": 1}, 0.35, "power3.out")
    to("#fd-cur", cl, {"x": 120, "y": 1080}, 0.32, "power2.in")
    to("#fd-ph", cl + 0.04, {"x": -1200, "rotation": -10}, 0.4, "power3.in")
    sfx.append(("arrow-whoosh", cl, 0.3))


def pg_course(var):
    """'(and) I definitely wouldn't start with a £5,000 course' — the price climbs on '5,000', a lime line strikes it on 'course'."""
    i = w("wouldn't start with a")
    ip = w("£5,000", t(i))
    ic_ = ip + 1
    s, e = t(i) - 0.1, te(ic_) + 0.2
    if var == "card":
        s = t(ip) - 0.2
        s = scene("p4", s, e, f"""
  <div class="stack" style="top:230px"><span class="lab">i wouldn't start with a</span><span class="h1" id="co-t" style="margin-top:18px">£5,000<br/>course</span></div>
  <div class="card" id="co-card" style="left:90px;right:90px;top:700px;height:900px;padding:60px 64px">
    <div class="lab" style="color:rgba(10,23,110,.55)">online course</div>
    <div class="h2 ink" style="font-size:78px;margin-top:16px">The Ultimate AI<br/>Masterclass</div>
    <div class="cl" style="font-size:36px;margin-top:34px;line-height:1.7">&#10003; 120+ hours of video<br/>&#10003; 50 bonus prompt packs<br/>&#10003; "lifetime" access</div>
    <div class="abs" style="left:64px;bottom:64px"><span class="h1 ink" id="co-p" style="font-size:150px">£0</span><div class="strike" id="co-x" style="left:-10px;top:84px;width:560px"></div></div>
  </div>""")
        rev("#co-t", s + 0.05)
        count("#co-p", t(ip) - 0.1, 0, 5000, 0.6, "£{}")
        sfx.append(("riser", t(ip) - 0.1, 0.18))
        ft("#co-x", t(ic_) - 0.02, {"scaleX": 0}, {"scaleX": 1}, 0.28, "power2.inOut")
        to("#co-card", t(ic_) + 0.15, {"rotation": -3, "y": 60, "opacity": 0.55}, 0.35)
        sfx.append(("scratch_002", t(ic_), 0.3))
        st("#co-x", s, {"scaleX": 0})
        return
    # var checkout: a checkout sheet totals £5,000; the cursor clicks Cancel and the sheet drops away
    s = scene("p4", s, e, f"""
  <div class="stack" style="top:250px"><span class="h1" id="co-t">£5,000<br/>course?</span></div>
  <div class="card" id="co-card" style="left:70px;right:70px;top:760px;height:860px;padding:56px 60px;border-radius:48px">
    <div class="h3 ink" style="font-size:50px">Checkout</div>
    <div class="row" style="justify-content:space-between;margin-top:40px"><span class="cl" style="font-size:38px">AI Masterclass</span><span class="cl" style="font-size:38px">£4,997</span></div>
    <div class="row" style="justify-content:space-between;margin-top:18px"><span class="cl muted" style="font-size:34px">"Bonus" community</span><span class="cl muted" style="font-size:34px">£3</span></div>
    <div style="height:4px;background:rgba(10,23,110,.1);margin:36px 0"></div>
    <div class="row" style="justify-content:space-between"><span class="h3 ink">Total</span><span class="h2 ink" id="co-p" style="font-size:96px">£0</span></div>
    <div class="abs" style="left:60px;right:60px;bottom:60px;height:120px;border-radius:30px;background:var(--navy);color:#fff;display:flex;align-items:center;justify-content:center;font-family:RHBlack;font-size:44px">Pay £5,000</div>
  </div>
  <div class="pill" id="co-cn" style="left:340px;width:400px;top:1670px;height:110px;background:#fff;color:var(--navy);font-size:42px;box-shadow:0 12px 30px rgba(4,12,80,.35)">&#10005;&nbsp; Cancel</div>
  <div class="cursor" id="co-cur">{CUR}</div>""")
    slam("#co-t", s + 0.05, 1.4)
    count("#co-p", t(ip) - 0.1, 0, 5000, 0.6, "£{}")
    sfx.append(("riser", t(ip) - 0.1, 0.18))
    pop("#co-cn", t(ip) + 0.3, 0.6, 20)
    cl = t(ic_) + 0.05
    click("#co-cur", 540, 1725, cl, frm=(1100, 1900))
    ft("#co-cn", cl, {"backgroundColor": "#ffffff"}, {"backgroundColor": LIME}, 0.15)
    to("#co-card", cl + 0.1, {"y": 1300, "rotation": 4}, 0.42, "power3.in")
    sfx.append(("minimize_006", cl + 0.1, 0.3))


def pg_pick(var):
    """'I'd pick one tool, like GPT, like Claude, and I would learn the ins and outs'."""
    i = w("i'd pick one tool")
    ig = w("gpt", t(i))
    icl = w("claude", t(i))
    ii = w("ins and outs", t(i))
    s, e = t(i) - 0.05, te(ii + 2) + 0.6
    FEAT = [("Projects", "folder"), ("Skills", "zap"), ("Memory", "brain"), ("Connectors", "plug"), ("Artifacts", "doc"), ("Claude Code", "code")]
    if var == "slot":
        cx, cy = 540, 1120
        ang = [-90 - 150 + k * 60 for k in range(6)]
        pos = [(cx + 330 * math.cos(math.radians(a)), cy + 330 * math.sin(math.radians(a)) * 1.25) for a in ang]
        feats = "".join(f'<div class="chip" id="pk-f{k}" style="left:{x - 150:.0f}px;top:{y - 44:.0f}px;width:300px;justify-content:center;font-size:34px;padding:18px 20px">{ic(n, 40)}{lab}</div>' for k, ((lab, n), (x, y)) in enumerate(zip(FEAT, pos)))
        lines = "".join(f'<path class="nline" id="pk-l{k}" d="M{cx},{cy} L{x:.0f},{y:.0f}" style="stroke-dasharray:420;stroke-dashoffset:420"/>' for k, (x, y) in enumerate(pos))
        s = scene("p5", s, e, f"""
  <div class="stack" style="top:240px"><span class="lab">i'd pick</span><span class="h1" id="pk-t" style="margin-top:16px">ONE <span class="hl">tool</span></span></div>
  <svg class="abs" style="left:0;top:0" width="1080" height="1920">{lines}</svg>
  <div class="tile" id="pk-g" style="left:{cx - 330}px;top:{cy - 130}px;width:260px;height:260px;border-radius:64px">{logo("openai", 150)}</div>
  <div class="abs h3" id="pk-or" style="left:{cx - 40}px;top:{cy - 40}px;width:80px;text-align:center">or</div>
  <div class="tile" id="pk-c" style="left:{cx + 70}px;top:{cy - 130}px;width:260px;height:260px;border-radius:64px">{logo("claude-color", 150)}</div>
  {feats}""")
        rev("#pk-t", s + 0.05)
        pop("#pk-g", t(ig) - 0.08, 0.3, 40)
        sfx.append(("drop_002", t(ig), 0.3))
        rev("#pk-or", t(ig) + 0.3, 12)
        pop("#pk-c", t(icl) - 0.08, 0.3, 40)
        sfx.append(("drop_002", t(icl), 0.3))
        a = t(ii - 3) - 0.1  # "learn the ins and outs": Claude takes the centre, the rest fades
        to("#pk-g", a, {"opacity": 0, "scale": 0.6, "x": -120}, 0.35)
        to("#pk-or", a, {"opacity": 0}, 0.2)
        to("#pk-c", a, {"x": -200}, 0.45, "power3.inOut")
        to("#pk-t", a, {"opacity": 0.6}, 0.3)
        span = 0.6
        for k in range(6):
            at = a + 0.35 + span * k / 6
            ft(f"#pk-l{k}", at, {"strokeDashoffset": 420}, {"strokeDashoffset": 0}, 0.22, "power2.in")
            pop(f"#pk-f{k}", at + 0.2, 0.4, 0, 0.3)
            sfx.append(("hard-pop-click", at + 0.2, 0.14))
        return
    # var picker: a model dropdown; the cursor picks Claude; its features expand underneath
    opts = [("openai", "ChatGPT"), ("claude-color", "Claude"), ("gemini-color", "Gemini"), ("perplexity-color", "Perplexity"), ("grok", "Grok"), ("deepseek-color", "DeepSeek")]
    rows = "".join(f'<div class="row" id="pk-o{k}" style="gap:26px;padding:22px 30px;border-radius:26px;margin-bottom:6px">{logo(lg, 60)}<span class="cl" style="font-size:44px">{nm}</span></div>' for k, (lg, nm) in enumerate(opts))
    feats = "".join(f'<div class="chip" id="pk-f{k}" style="left:{90 + (k % 2) * 460}px;top:{1290 + (k // 2) * 130}px;width:440px;font-size:36px">{ic(n, 42)}{lab}</div>' for k, (lab, n) in enumerate(FEAT))
    s = scene("p5", s, e, f"""
  <div class="stack" style="top:200px"><span class="h1" id="pk-t">pick <span class="hl">one</span></span></div>
  <div class="card" id="pk-menu" style="left:150px;right:150px;top:470px;padding:22px;border-radius:44px">{rows}</div>
  {feats}
  <div class="cursor" id="pk-cur">{CUR}</div>""")
    slam("#pk-t", s + 0.05, 1.4)
    ft("#pk-menu", s + 0.15, {"opacity": 0, "y": 40, "scale": 0.96}, {"opacity": 1, "y": 0, "scale": 1}, 0.4, "expo.out")
    st("#pk-o0", t(ig) - 0.05, {"backgroundColor": "rgba(24,56,240,.12)"})
    st("#pk-o0", t(icl) - 0.1, {"backgroundColor": "rgba(24,56,240,0)"})
    cl = t(icl) + 0.15
    click("#pk-cur", 420, 470 + 22 + 110 + 52, cl, frm=(1100, 1300))
    ft("#pk-o1", cl, {"backgroundColor": "rgba(212,255,60,0)"}, {"backgroundColor": "rgba(212,255,60,1)"}, 0.15)
    for k in (0, 2, 3, 4, 5):
        to(f"#pk-o{k}", cl + 0.2, {"opacity": 0.25}, 0.3)
    a = t(ii) - 0.2
    span = max(0.6, e - 0.4 - a)
    for k in range(6):
        pop(f"#pk-f{k}", a + span * k / 6, 0.5, 30, 0.3)
        sfx.append(("hard-pop-click", a + span * k / 6, 0.12))


def pg_route(rid, frm, to_k, phrase, end_phrase=None, sub_over=None, hold=0.3, bigger=False):
    """The route again: the train runs from station frm to station to_k as he names the step."""
    i = w(phrase)
    s = t(i) - 0.1
    e = (te(w(end_phrase, t(i))) + hold) if end_phrase else (t(i) + 2.2)
    s = scene(rid, s, e, route_body(rid, frm + 1, sub_over=sub_over, train_at=SARC[frm]))
    d = min(1.3, max(0.8, e - s - 0.9))
    train(rid, SARC[frm], SARC[to_k], s + 0.35, d)
    return s, e


def pg_week1(var):
    """'things that I'd be doing anyways, like planning my fitness, my schedule, managing my money, brainstorming new ideas'."""
    i = w("like planning my fitness")
    i_f = i + 3
    i_s = w("schedule", t(i))
    i_m = w("money", t(i))
    i_i = w("brainstorming", t(i))
    e = te(i_i + 2) + 0.35
    s = t(i) - 0.1
    if var == "grid":
        def box(k, x, y, name, icon, inner):
            return (f'<div class="card" id="wk-b{k}" style="left:{x}px;top:{y}px;width:440px;height:560px;padding:34px 34px;border-radius:40px">'
                    f'<div class="row" style="gap:18px"><div style="width:84px;height:84px;border-radius:24px;background:var(--cob);display:flex;align-items:center;justify-content:center">{ic(icon, 50, "ico w")}</div>'
                    f'<span class="h3 ink" style="font-size:46px">{name}</span></div>{inner}</div>')
        fit = "".join(f'<div class="row" style="gap:16px;margin-top:22px"><span class="cl" style="font-size:30px;width:74px">{d_}</span><div class="bar" style="position:relative;flex:1;height:44px"><i id="wk-f{k}" style="background:{COB}"></i></div><div class="tick" id="wk-ft{k}" style="position:relative;width:44px;height:44px">{TICK}</div></div>' for k, d_ in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri"]))
        cal = "".join(f'<div class="abs" id="wk-c{k}" style="left:{34 + col * 128}px;top:{150 + row_ * 0}px;width:116px;height:{h}px;margin-top:{mt}px;border-radius:18px;background:{c};"></div>' for k, (col, row_, h, mt, c) in enumerate([(0, 0, 120, 0, COB), (1, 0, 200, 60, LIME), (2, 0, 90, 20, NAVY), (0, 0, 150, 160, LIME), (2, 0, 170, 150, COB), (1, 0, 110, 290, NAVY)]))
        mon = (f'<div class="abs" style="left:34px;right:34px;top:150px"><div class="cl muted" style="font-size:28px">left this month</div><div class="h2 ink" id="wk-mn" style="font-size:88px;margin-top:6px">£0</div></div>'
               + "".join(f'<div class="bar" style="left:34px;right:34px;top:{330 + k * 64}px;height:40px"><i id="wk-m{k}" style="background:{[COB, LIME, NAVY][k]}"></i></div>' for k in range(3)))
        ideas = "".join(f'<div class="abs" id="wk-i{k}" style="left:{34 + (k % 2) * 190}px;top:{150 + (k // 2) * 170}px;width:176px;height:150px;border-radius:20px;background:{[LIME, "#eef1ff", "#eef1ff", LIME][k]};padding:18px;font-family:RHBold;font-size:26px;color:{NAVY};line-height:1.15">{x}</div>' for k, x in enumerate(["app for my gym", "faceless page", "morning bot", "client CRM"]))
        s = scene("p6", s, e, f"""
  <div class="stack" style="top:190px"><span class="lab">week 1</span><span class="h2" id="wk-t" style="margin-top:14px">use it for <span class="hl">real stuff</span></span></div>
  {box(0, 70, 440, "Fitness", "dumbbell", fit)}
  {box(1, 570, 440, "Schedule", "cal", cal)}
  {box(2, 70, 1060, "Money", "wallet", mon)}
  {box(3, 570, 1060, "Ideas", "bulb", ideas)}""")
        rev("#wk-t", s + 0.05)
        for k, at in enumerate([t(i_f), t(i_s), t(i_m), t(i_i)]):
            pop(f"#wk-b{k}", at - 0.12, 0.6, 50, 0.4)
            sfx.append(("drop_002", at - 0.05, 0.25))
        for k in range(5):
            a = t(i_f) + 0.15 + k * 0.12
            ft(f"#wk-f{k}", a, {"scaleX": 0}, {"scaleX": 1}, 0.3, "power2.out")
            tick_at(f"#wk-ft{k}", a + 0.25, k == 4)
        for k in range(6):
            ft(f"#wk-c{k}", t(i_s) + 0.15 + k * 0.1, {"opacity": 0, "y": -60}, {"opacity": 1, "y": 0}, 0.3, "back.out(1.8)")
        count("#wk-mn", t(i_m) + 0.1, 0, 1240, 0.8, "£{}")
        for k, f_ in enumerate([0.7, 0.45, 0.25]):
            ft(f"#wk-m{k}", t(i_m) + 0.15 + k * 0.1, {"scaleX": 0}, {"scaleX": f_}, 0.5, "power2.out")
        for k in range(4):
            pop(f"#wk-i{k}", t(i_i) + 0.2 + k * 0.14, 0.3, 10, 0.3)
            sfx.append(("hard-pop-click", t(i_i) + 0.2 + k * 0.14, 0.1))
        return
    # var week: a Mon–Sun planner; each thing he names drops into its day as a block
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    cols = "".join(f'<div class="abs" style="left:{70 + k * 136}px;top:470px;width:124px;height:1260px;border-radius:26px;background:rgba(255,255,255,.09)"></div><div class="abs lab" style="left:{70 + k * 136}px;width:124px;text-align:center;top:410px;color:#fff">{d_}</div>' for k, d_ in enumerate(days))
    BL = [("f", 0, 520, "Gym", LIME), ("f", 2, 520, "Gym", LIME), ("f", 4, 520, "Gym", LIME),
          ("s", 1, 760, "Deep work", "#fff"), ("s", 3, 760, "Deep work", "#fff"), ("s", 0, 1000, "Calls", "#fff"),
          ("m", 6, 640, "Budget", NAVY), ("m", 4, 1200, "Bills", NAVY),
          ("i", 5, 900, "Ideas", LIME), ("i", 2, 1380, "Ideas", LIME)]
    blocks = "".join(f'<div class="abs" id="wb{k}" style="left:{76 + d * 136}px;top:{y}px;width:112px;height:190px;border-radius:20px;background:{c};padding:14px 10px;font-family:RHBlack;font-size:24px;line-height:1.1;color:{"#fff" if c == NAVY else NAVY};box-shadow:0 10px 24px rgba(4,12,80,.35)">{lab}</div>' for k, (_, d, y, lab, c) in enumerate(BL))
    s = scene("p6", s, e, f"""
  <div class="stack" style="top:170px"><span class="h2" id="wk-t">your <span class="hl">real</span> week</span></div>
  {cols}{blocks}""")
    rev("#wk-t", s + 0.05)
    when = {"f": t(i_f), "s": t(i_s), "m": t(i_m), "i": t(i_i)}
    seen = {}
    for k, (g, *_r) in enumerate(BL):
        n_ = seen.get(g, 0)
        seen[g] = n_ + 1
        at = when[g] - 0.1 + n_ * 0.12
        ft(f"#wb{k}", at, {"opacity": 0, "y": -140, "rotation": -6}, {"opacity": 1, "y": 0, "rotation": 0}, 0.38, "back.out(1.6)")
        sfx.append(("drop_002" if n_ == 0 else "hard-pop-click", at + 0.15, 0.2 if n_ == 0 else 0.1))


def pg_build():
    """V2 'build something that actually matters' — app blocks snap together into a working app."""
    i = w("start to build something")
    ia = w("matters", t(i))
    s, e = t(i + 2) - 0.1, te(ia) + 0.3
    s = scene("p7", s, e, f"""
  <div class="stack" style="top:210px"><span class="lab">week 2</span><span class="h1" id="bd-t" style="margin-top:16px">build <span class="hl">something</span></span></div>
  <div class="card" id="bd-win" style="left:110px;right:110px;top:560px;height:1100px;border-radius:44px;background:#f3f5ff;overflow:hidden">
    <div style="height:90px;background:#fff;display:flex;align-items:center;gap:14px;padding:0 34px"><i style="width:22px;height:22px;border-radius:50%;background:#dfe3ff;display:block"></i><i style="width:22px;height:22px;border-radius:50%;background:#dfe3ff;display:block"></i><i style="width:22px;height:22px;border-radius:50%;background:#dfe3ff;display:block"></i></div>
  </div>
  <div class="abs" id="bd-b0" style="left:150px;width:780px;top:690px;height:120px;border-radius:28px;background:var(--navy);display:flex;align-items:center;padding:0 36px;gap:22px">{ic("zap", 56, "ico w")}<span class="h3" style="font-size:46px">My app</span></div>
  <div class="abs" id="bd-b1" style="left:150px;width:380px;top:850px;height:330px;border-radius:28px;background:var(--lime);padding:30px"><div class="cl" style="font-size:32px">This week</div><div class="h1 ink" style="font-size:110px;margin-top:30px">12</div></div>
  <div class="abs" id="bd-b2" style="left:550px;width:380px;top:850px;height:330px;border-radius:28px;background:#fff;padding:30px;box-shadow:0 10px 26px rgba(4,12,80,.12)"><div class="cl" style="font-size:32px">Streak</div><div class="h1 ink" style="font-size:110px;margin-top:30px">7&#128293;</div></div>
  <div class="abs" id="bd-b3" style="left:150px;width:780px;top:1220px;height:300px;border-radius:28px;background:#fff;padding:24px 30px;box-shadow:0 10px 26px rgba(4,12,80,.12)">
    {''.join(f'<div class="row" style="gap:20px;margin:14px 0"><div class="tick" style="position:relative;width:46px;height:46px">{TICK}</div><span class="cl" style="font-size:34px">{x}</span></div>' for x in ["solves my problem", "runs on its own", "I actually use it"])}</div>""")
    rev("#bd-t", s + 0.05)
    ft("#bd-win", s + 0.12, {"opacity": 0, "scale": 0.9}, {"opacity": 1, "scale": 1}, 0.4, "expo.out")
    span = e - s - 0.9
    for k, (dx, dy) in enumerate([(0, -500), (-700, 0), (700, 0), (0, 700)]):
        at = s + 0.4 + span * k / 4
        ft(f"#bd-b{k}", at, {"opacity": 0, "x": dx, "y": dy, "rotation": 8 if dx else 0}, {"opacity": 1, "x": 0, "y": 0, "rotation": 0}, 0.42, "back.out(1.4)")
        sfx.append(("drop_002", at + 0.3, 0.22))


def pg_problem():
    """'(Maybe something that) solves a problem of my own, or solves a problem for someone else' — two cards, each solved with a tick."""
    i = w("solves a problem of my own")
    io = w("own", t(i))
    i2 = w("solves a problem for someone", t(i))
    ie = w("else", t(i2))
    s, e = t(i) - 0.1, te(ie) + 0.35

    def card(k, top, icon, small, big):
        return (f'<div class="card" id="pb-c{k}" style="left:90px;right:90px;top:{top}px;height:400px;padding:50px 56px;display:flex;align-items:center;gap:44px">'
                f'<div style="width:190px;height:190px;border-radius:50px;background:var(--cob);display:flex;align-items:center;justify-content:center;flex:none">{ic(icon, 120, "ico w", 1.8)}</div>'
                f'<div><div class="lab" style="color:rgba(10,23,110,.55)">{small}</div><div class="h2 ink" style="font-size:80px;margin-top:10px">{big}</div></div>'
                f'<div class="tick" id="pb-t{k}" style="right:44px;top:44px;width:86px;height:86px">{TICK}</div></div>')
    s = scene("p7", s, e, f"""
  <div class="stack" style="top:220px"><span class="lab">build something that</span><span class="h1" id="pb-h" style="margin-top:16px"><span class="hl">solves</span> a problem</span></div>
  {card(0, 640, "user", "a problem", "of my own")}
  {card(1, 1110, "users", "a problem", "for someone else")}""")
    slam("#pb-h", s + 0.05, 1.3)
    pop("#pb-c0", t(io) - 0.35, 0.8, 60, 0.4)
    tick_at("#pb-t0", t(io) + 0.1)
    pop("#pb-c1", t(i2) + 0.2, 0.8, 60, 0.4)
    tick_at("#pb-t1", t(ie) + 0.05)
    sfx.append(("drop_002", t(io) - 0.3, 0.22))
    sfx.append(("drop_002", t(i2) + 0.25, 0.22))


def pg_auto(var):
    """'Maybe it's a certain automation that you want to run every single morning or every single night'."""
    i = w("maybe it's a certain automation")
    im = w("morning", t(i))
    i_n = w("night", t(i))
    s, e = t(i) - 0.1, te(i_n) + 0.4
    if var == "flow":
        s = scene("p8", s, e, f"""
  <div class="stack" style="top:200px"><span class="lab">an automation</span><span class="h1" id="au-t" style="margin-top:16px">that runs <span class="hl" id="au-w">every morning</span></span></div>
  <svg class="abs" style="left:0;top:0" width="1080" height="1920"><path class="nline" id="au-l1" d="M540,760 L540,1000" style="stroke-dasharray:240;stroke-dashoffset:240"/><path class="nline" id="au-l2" d="M540,1240 L540,1440" style="stroke-dasharray:200;stroke-dashoffset:200"/></svg>
  <div class="card" id="au-n0" style="left:290px;width:500px;top:560px;height:200px;border-radius:100px;display:flex;align-items:center;gap:26px;padding:0 50px">
    <div class="abs" id="au-sun" style="left:46px;top:46px">{ic("sun", 108)}</div><div class="abs" id="au-moon" style="left:46px;top:46px;opacity:0">{ic("moon", 108)}</div>
    <span class="h2 ink" id="au-clk" style="margin-left:150px;font-size:80px">7:00</span></div>
  <div class="tile" id="au-n1" style="left:420px;top:1000px;width:240px;height:240px;border-radius:60px">{logo("claude-color", 140)}</div>
  <div class="card" id="au-n2" style="left:150px;right:150px;top:1440px;height:240px;padding:40px 46px">
    <div class="lab" style="color:rgba(10,23,110,.55)" id="au-o0">sent 7:00 am</div><div class="h3 ink" id="au-o1" style="font-size:52px;margin-top:10px">Your plan for today &#9989;</div></div>
  <div class="abs" id="au-dot" style="left:518px;top:740px;width:44px;height:44px;border-radius:50%;background:var(--lime);box-shadow:0 0 0 10px rgba(212,255,60,.3);opacity:0"></div>""")
        rev("#au-t", s + 0.05)
        pop("#au-n0", s + 0.25, 0.6, 30)
        a = t(im) - 0.3
        ft("#au-l1", a, {"strokeDashoffset": 240}, {"strokeDashoffset": 0}, 0.35, "power1.in")
        ft("#au-dot", a, {"opacity": 1, "y": 0}, {"opacity": 1, "y": 260}, 0.35, "power1.in")
        pop("#au-n1", a + 0.33, 0.4, 0, 0.32)
        sfx.append(("pluck_001", a + 0.33, 0.3))
        ft("#au-l2", a + 0.55, {"strokeDashoffset": 200}, {"strokeDashoffset": 0}, 0.3, "power1.in")
        ft("#au-dot", a + 0.55, {"y": 260}, {"y": 700, "opacity": 0}, 0.32, "power1.in", False)
        pop("#au-n2", a + 0.85, 0.5, 30, 0.35)
        sfx.append(("confirmation_002", a + 0.85, 0.3))
        b = t(i_n) - 0.35  # night: the sun sets into the moon, the clock rolls to 9:00 pm, the page dims, a second run lands
        to(f"#p8 .sheet", b, {"backgroundColor": NAVY}, 0.4)
        to("#au-sun", b, {"opacity": 0, "y": 40, "rotation": 60}, 0.3)
        ft("#au-moon", b + 0.1, {"opacity": 0, "y": -40}, {"opacity": 1, "y": 0}, 0.35, "back.out(2)", False)
        st("#au-clk", b + 0.15, {"textContent": "9:00"})
        st("#au-w", b + 0.15, {"textContent": "every night"})
        st("#au-o0", b + 0.15, {"textContent": "sent 9:00 pm"})
        st("#au-o1", b + 0.15, {"textContent": "Today's recap ✅"})
        ft("#au-n2", b + 0.2, {"scale": 0.92}, {"scale": 1}, 0.3, "back.out(2)", False)
        sfx.append(("switch_003", b, 0.3))
        sfx.append(("confirmation_002", b + 0.25, 0.25))
        return
    # var lock: a phone lock screen; the clock ticks 6:59 -> 7:00, a notification lands; then night
    s = scene("p8", s, e, f"""
  <div class="phone" style="left:260px;top:360px"><div class="screen" id="lk-scr" style="background:linear-gradient(180deg,#2a47ff,#0f27c4)">
    <div class="stack" style="top:150px"><span class="lab" style="color:rgba(255,255,255,.8)" id="lk-d">Tuesday</span><span class="h1" id="lk-c" style="font-size:150px;margin-top:4px">6:59</span></div>
    <div class="card" id="lk-n0" style="left:26px;right:26px;top:520px;height:150px;border-radius:34px;padding:24px;display:flex;gap:20px;align-items:center;background:rgba(255,255,255,.94)">{logo("claude-color", 70)}<div><div class="cl" style="font-size:26px">Claude · 7:00 am</div><div class="cl" style="font-size:30px;font-family:RHBlack">Your plan for today is ready</div></div></div>
    <div class="card" id="lk-n1" style="left:26px;right:26px;top:690px;height:150px;border-radius:34px;padding:24px;display:flex;gap:20px;align-items:center;background:rgba(255,255,255,.94)">{logo("claude-color", 70)}<div><div class="cl" style="font-size:26px">Claude · 9:00 pm</div><div class="cl" style="font-size:30px;font-family:RHBlack">Today's recap: 6 tasks done</div></div></div>
  </div><div class="notch"></div></div>
  <div class="stack" style="top:150px"><span class="h2" id="lk-t">runs <span class="hl" id="lk-w">every morning</span></span></div>""")
    rev("#lk-t", s + 0.05)
    a = t(im) - 0.25
    st("#lk-c", a, {"textContent": "7:00"})
    ft("#lk-c", a, {"y": -20, "opacity": 0.3}, {"y": 0, "opacity": 1}, 0.2, "power2.out", False)
    ft("#lk-n0", a + 0.15, {"opacity": 0, "y": -60, "scale": 0.9}, {"opacity": 1, "y": 0, "scale": 1}, 0.4, "back.out(1.6)")
    sfx.append(("glass_002", a + 0.2, 0.35))
    b = t(i_n) - 0.3
    to("#lk-scr", b, {"background": "linear-gradient(180deg,#0a176e,#050b3a)"}, 0.35)
    st("#lk-c", b + 0.1, {"textContent": "9:00"})
    st("#lk-w", b + 0.1, {"textContent": "every night"})
    ft("#lk-n1", b + 0.15, {"opacity": 0, "y": -60, "scale": 0.9}, {"opacity": 1, "y": 0, "scale": 1}, 0.4, "back.out(1.6)")
    sfx.append(("glass_002", b + 0.2, 0.35))


def pg_hobby():
    """'Or maybe you just want an app for a hobby you're pursuing' — an app icon lands on a home screen and opens."""
    i = w("or maybe you just want an app")
    ia = w("app", t(i))
    ih = w("hobby", t(i))
    s, e = t(i) - 0.1, te(ih + 2) + 0.3
    apps = "".join(f'<div class="abs" style="left:{46 + (k % 4) * 118}px;top:{150 + (k // 4) * 128}px;width:92px;height:92px;border-radius:24px;background:rgba(10,23,110,{0.08 + 0.04 * (k % 3)})"></div>' for k in range(12))
    s = scene("p9", s, e, f"""
  <div class="stack" style="top:170px"><span class="h2" id="hb-t">an app for your <span class="hl">hobby</span></span></div>
  <div class="phone" style="left:260px;top:380px"><div class="screen">{apps}
    <div class="abs" id="hb-ic" style="left:46px;top:534px;width:92px;height:92px;border-radius:24px;background:var(--cob);display:flex;align-items:center;justify-content:center">{ic("music", 54, "ico w")}</div>
    <div class="abs" id="hb-app" style="inset:0;background:#fff;padding:120px 40px 0;opacity:0">
      <div class="lab" style="color:rgba(10,23,110,.55)">guitar practice</div><div class="h2 ink" style="font-size:66px;margin-top:10px">Practice log</div>
      <div class="row" style="gap:16px;margin-top:40px">{''.join(f'<div id="hb-d{k}" style="width:52px;height:120px;border-radius:14px;background:{LIME if k != 5 else "#e6e9ff"};transform-origin:bottom"></div>' for k in range(7))}</div>
      <div class="card" style="position:relative;margin-top:40px;padding:30px;border-radius:28px;background:var(--cob);color:#fff"><div class="cl" style="color:#fff;font-size:30px">next up</div><div class="h3" style="font-size:44px">F major, 10 min</div></div>
    </div></div><div class="notch"></div></div>""")
    rev("#hb-t", s + 0.05)
    pop("#hb-ic", t(ia) - 0.1, 0.2, 0, 0.35)
    sfx.append(("drop_002", t(ia), 0.3))
    a = t(ih) - 0.05
    ft("#hb-app", a, {"opacity": 0, "scale": 0.2, "transformOrigin": "92px 580px"}, {"opacity": 1, "scale": 1}, 0.4, "expo.out")
    sfx.append(("maximize_006", a, 0.3))
    for k in range(7):
        ft(f"#hb-d{k}", a + 0.3 + k * 0.06, {"scaleY": 0}, {"scaleY": [0.5, 0.8, 0.4, 1, 0.7, 0.15, 0.9][k]}, 0.3, "back.out(1.6)")


def pg_payoff(var):
    """'I went from chatting with AI like a normal user to actually building stuff'."""
    i = w("i went from chatting")
    ic_ = w("chatting", t(i))
    ib = w("building", t(i))
    istuff = ib + 1
    s, e = t(w("but that's exactly")) - 0.1, te(istuff) + 0.35
    if var == "route":
        s = scene("p10", s, e, route_body("p10", 4, train_at=SARC[3]))
        ft("#p10-n0", t(ic_) - 0.05, {"scale": 1}, {"scale": 1.12}, 0.2, "back.out(3)")
        st("#p10-n0", t(ic_) - 0.05, {"textContent": "CHATTING"})
        st("#p10-u0", t(ic_) - 0.05, {"textContent": "like a normal user"})
        ft("#p10-n0", t(ic_) - 0.05, {"color": "#ffffff"}, {"color": LIME}, 0.2, "power1.out", False)
        sfx.append(("switch_003", t(ic_), 0.25))
        train("p10", SARC[3], SARC[4], t(ib) - 0.75, 0.75, light_end=False)
        st("#p10-n4", t(ib) - 0.02, {"textContent": "BUILDING"})
        light("p10", 4, t(ib), True)
        ft("#p10-l4", t(ib), {"scale": 1}, {"scale": 1.1}, 0.3, "back.out(3)")
        return s, e
    # var split: chatting | building, a lime divider sweeps across on 'building'
    s = t(ic_) - 0.25
    CH = ["write me a caption", "Sure! Here's one…", "summarise this email", "Of course! Here…", "what should I eat?", "Great question!"]
    chat = "".join(f'<div class="abs" style="{"left:40px" if k % 2 == 0 else "right:580px"};top:{560 + k * 150}px;max-width:430px;padding:26px 30px;border-radius:30px;background:{"#fff" if k % 2 == 0 else "rgba(255,255,255,.16)"};font-family:RHBold;font-size:32px;line-height:1.1;color:{NAVY if k % 2 == 0 else "#fff"}">{CH[k]}</div>' for k in range(6))
    build = "".join(f'<div class="abs" id="sp-b{k}" style="left:{560 + (k % 2) * 230}px;top:{560 + (k // 2) * 300}px;width:210px;height:270px;border-radius:30px;background:{[LIME, "#fff", "#fff", LIME, LIME, "#fff"][k]};display:flex;align-items:center;justify-content:center">{ic(["zap", "cal", "wallet", "code", "music", "users"][k], 90)}</div>' for k in range(6))
    s = scene("p10", s, e, f"""
  <div class="abs" style="left:0;top:0;width:540px;height:1920px;background:var(--navy)"></div>
  <div class="abs lab" style="left:0;width:540px;text-align:center;top:420px;color:#fff">before</div>
  <div class="abs lab" style="left:540px;width:540px;text-align:center;top:420px;color:#fff">after</div>
  <div class="abs h2" id="sp-l" style="left:0;width:540px;text-align:center;top:250px">chatting</div>
  <div class="abs h2 lime" id="sp-r" style="left:540px;width:540px;text-align:center;top:250px">building</div>
  {chat}{build}
  <div class="abs" id="sp-cv" style="left:540px;top:0;width:540px;height:1920px;background:var(--navy)"></div>
  <div class="abs" id="sp-d" style="left:532px;top:0;width:16px;height:1920px;background:var(--lime);box-shadow:0 0 40px rgba(212,255,60,.7)"></div>""")
    rev("#sp-l", t(ic_) - 0.05)
    st("#sp-r", s, {"opacity": 0})
    a = t(ib) - 0.2
    ft("#sp-cv", a, {"scaleX": 1, "transformOrigin": "100% 50%"}, {"scaleX": 0, "transformOrigin": "100% 50%"}, 0.5, "power3.inOut")
    ft("#sp-d", a, {"x": 0}, {"x": 540}, 0.5, "power3.inOut")
    to("#sp-d", a + 0.5, {"opacity": 0}, 0.3)
    rev("#sp-r", t(ib) - 0.02)
    for k in range(6):
        pop(f"#sp-b{k}", a + 0.25 + k * 0.06, 0.6, 20, 0.3)
    sfx.append(("arrow-whoosh", a, 0.3))
    sfx.append(("confirmation_002", t(ib) + 0.1, 0.3))
    return s, e


def pg_cta():
    """'leave me a follow' — a profile card; the Follow button lights, a cursor clicks it, it flips to Following."""
    i = w("leave me a follow")
    s = t(i) - 0.15
    e = DURATION + 0.01
    s = scene("p11", s, e, f"""
  <div class="stack" style="top:300px"><span class="lab">learn all things ai</span><span class="h1" id="ct-t" style="margin-top:18px">{"follow for" if has("follow for more") else "leave a"} <span class="hl">{"more" if has("follow for more") else "follow"}</span></span></div>
  <div class="card" id="ct-card" style="left:110px;right:110px;top:700px;height:520px;border-radius:48px;padding:56px">
    <div class="row" style="gap:34px"><div style="width:150px;height:150px;border-radius:50%;background:var(--lime);display:flex;align-items:center;justify-content:center;font-family:RHBlack;font-size:80px;color:var(--navy)">J</div>
      <div><div class="h2 ink" style="font-size:72px">Jack</div><div class="cl muted" style="font-size:34px;margin-top:6px">19 · builds with AI every day</div></div></div>
    <div class="abs" id="ct-btn" style="left:56px;right:56px;bottom:56px;height:130px;border-radius:999px;background:var(--cob);color:#fff;display:flex;align-items:center;justify-content:center;font-family:RHBlack;font-size:52px"><span id="ct-bt">Follow</span></div>
  </div>
  <div class="cursor" id="ct-cur">{CUR}</div>""")
    rev("#ct-t", s + 0.05)
    pop("#ct-card", s + 0.15, 0.85, 50, 0.45)
    cl = t(w("follow", t(i))) + 0.35
    ft("#ct-btn", cl - 0.35, {"boxShadow": "0 0 0 0px rgba(24,56,240,.4)"}, {"boxShadow": "0 0 0 18px rgba(24,56,240,.25)"}, 0.3)
    click("#ct-cur", 540, 1099, cl, frm=(1100, 1700), leave=(1150, 1500))
    ft("#ct-btn", cl + 0.02, {"backgroundColor": COB, "color": "#ffffff"}, {"backgroundColor": LIME, "color": NAVY}, 0.2)
    st("#ct-bt", cl + 0.02, {"textContent": "Following ✓"})
    sfx.append(("confirmation_002", cl + 0.05, 0.35))


# ================================================================= the two versions
HUD_PLAN = []  # (station, time) the HUD moves to while he's on screen
if N == 1:  # main: his hook, everything in order
    _, hook_e = pg_hook_route()
    pg_days()
    pg_tools("grid")
    pg_course("card")
    pg_pick("slot")
    pg_week1("grid")
    pg_problem()
    pg_auto("flow")
    pg_payoff("route")
    pg_cta()
    HUD_SHOW = t(w("if i started from zero")) - 0.1
    HUD_PLAN = [(0, HUD_SHOW), (1, t(w("i'd pick one tool"))), (2, t(w("on week one"))), (3, t(w("week two"))), (4, t(w("building")))]
else:  # contrarian first, tight: the skip lines open, the plan follows; alternate pages for a third+ of the beats
    pg_tools("feed")
    pg_course("checkout")
    _, hook_e = pg_hook_route()
    pg_pick("picker")
    pg_week1("week")
    pg_auto("lock")
    pg_payoff("split")
    pg_cta()
    HUD_SHOW = hook_e - 0.42
    HUD_PLAN = [(1, t(w("i'd pick one tool"))), (2, t(w("on week one"))), (3, t(w("week two"))), (4, t(w("building")))]

def page_end_at(x):
    return next((b for _, a, b, _, _ in scenes if a - 0.05 <= x < b), None)


hud_show(page_end_at(HUD_SHOW) or HUD_SHOW)
for k, at in HUD_PLAN:
    pe = page_end_at(at)
    hud_go(k, pe + 0.05 if pe else at)

# ---------------------------------------------------------------- page windows (crossfade back to his face, dissolve page to page)
scenes.sort(key=lambda x: x[1])
handoff = set()
for k in range(len(scenes) - 1):
    sid, a, b_end, body, bg = scenes[k]
    nid, na, nb, nbody, nbg = scenes[k + 1]
    if na <= b_end + 1.0:  # never show his face for under a second between two pages
        scenes[k] = (sid, a, max(b_end, na + 0.34), body, bg)
        handoff.add(sid)
        js.append(f"tl.fromTo('#{nid}', {{opacity:0}}, {{opacity:1, duration:.32, ease:'sine.inOut', immediateRender:false}}, {na:.3f});")
for sid, a, b_end, _, _ in scenes:
    if b_end >= AROLL_END - 0.01 or sid in handoff:
        continue
    js.append(f"tl.fromTo('#{sid}', {{opacity:1}}, {{opacity:0, duration:.42, ease:'sine.inOut', immediateRender:false}}, {b_end - 0.42:.3f});")
WIN = [(a, b) for _, a, b, _, _ in scenes]


def covered(x, pad=0.0):
    return any(a - pad <= x < b + pad for a, b in WIN)


# ---------------------------------------------------------------- captions (above his head; off while a page covers him)
def groups():
    out, cur = [], []
    for i in range(len(TOK)):
        txt = TOK[i]["text"]
        if cur:
            gap = t(i) - te(cur[-1])
            chars = sum(len(disp(j)) + 1 for j in cur) + len(disp(i))
            cut_between = any(t(cur[-1]) < c <= t(i) for c in CUTS)
            if len(cur) >= 3 or chars > 15 or gap > 0.3 or cut_between or TOK[cur[-1]]["text"][-1] in ",.?!" or covered(t(i)) != covered(t(cur[-1])):
                out.append(cur)
                cur = []
        cur.append(i)
    if cur:
        out.append(cur)
    return out


cap_html, cap_js = [], []
for gi, g in enumerate(groups()):
    g_start = t(g[0]) - 0.06
    end = min(te(g[-1]) + 0.35, t(g[-1] + 1) - 0.04 if g[-1] + 1 < len(TOK) else AROLL_END)
    if covered(t(g[0]) + 0.02):
        continue
    nxt_page = min([a for a, _ in WIN if a > g_start] + [1e9])
    end = min(end, nxt_page + 0.02)
    if end - g_start < 0.1:
        continue
    spans = "".join(f'<span class="w" id="w{i}"><b></b><span class="tx">{esc(disp(i))}</span></span>' for i in g)
    cap_html.append(f'<div class="cap clip" id="cap{gi}" data-start="{g_start:.3f}" data-duration="{end - g_start:.3f}" data-track-index="2"><div class="capi">{spans}</div></div>')
    for i in g:
        a = max(g_start, t(i) - 0.05)
        cap_js.append(f"tl.fromTo('#w{i}', {{opacity:0, scale:.6, y:16}}, {{opacity:1, scale:1, y:0, duration:.18, ease:'back.out(2.2)'}}, {a:.3f});")
        cap_js.append(f"tl.fromTo('#w{i} b', {{opacity:0, scale:.7}}, {{opacity:1, scale:1, duration:.12, ease:'back.out(2)'}}, {a:.3f});")
        cap_js.append(f"tl.fromTo('#w{i} .tx', {{color:'#ffffff'}}, {{color:'{NAVY}', duration:.08}}, {a:.3f});")
        off = min(te(i), end - 0.06)
        if i != g[-1]:
            cap_js.append(f"tl.to('#w{i} b', {{opacity:0, duration:.08, immediateRender:false}}, {off:.3f});")
            cap_js.append(f"tl.to('#w{i} .tx', {{color:'#ffffff', duration:.08, immediateRender:false}}, {off:.3f});")
    cap_js.append(f"tl.to('#cap{gi} .capi', {{opacity:0, y:-12, duration:.1, ease:'power1.in', immediateRender:false}}, {end - 0.1:.3f});")

# ---------------------------------------------------------------- camera: hook slam, punch-ins at every cut, slow push between
FACES = []
for line in open(f"{D}/faces-2fps.txt"):
    p = line.split()
    if len(p) == 5:
        FACES.append((int(p[0][1:5]) / 2 - 0.5 + 0.25, *map(float, p[1:])))
cam_js = []
bounds = [0.0] + CUTS + [AROLL_END]
for k in range(len(bounds) - 1):
    a, b = bounds[k], bounds[k + 1]
    win = [f for f in FACES if a <= f[0] < b] or [min(FACES, key=lambda f: abs(f[0] - a))]
    cx = sum(f[1] + f[3] / 2 for f in win) / len(win)
    cy = sum(f[2] + f[4] / 2 for f in win) / len(win)
    z = 1.0 if k % 2 == 0 else 1.1
    if k == 0:
        cam_js.append(f"tl.fromTo('#cam', {{scale:1.35, transformOrigin:'{int(cx * 1080)}px {int(cy * 1920)}px'}}, {{scale:1, duration:.5, ease:'expo.out'}}, 0);")
        cam_js.append(f"tl.to('#cam', {{scale:1.03, duration:{b - 0.5:.3f}, ease:'none', immediateRender:false}}, .5);")
        continue
    cam_js.append(f"tl.fromTo('#cam', {{scale:{z}, transformOrigin:'{int(cx * 1080)}px {int(cy * 1920)}px'}}, {{scale:{z * 1.03:.4f}, duration:{b - a:.3f}, ease:'none', immediateRender:false}}, {a:.3f});")
    if not covered(a + 0.02):
        cam_js.append(f"focus({a:.3f});")
sfx.append(("boom", 0.0, 0.25))

# ---------------------------------------------------------------- assemble
sfx_html = "\n".join(f'<audio id="sfx{n}" src="assets/audio/sfx/{name}.wav" data-start="{max(0.0, at):.3f}" data-track-index="{20 + n}" data-volume="{vol}"></audio>'
                     for n, (name, at, vol) in enumerate(sorted(sfx, key=lambda x: x[1])))
scene_html = "\n".join(f"""<section class="scene clip" id="{sid}" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="3">
 <div class="sheet">{MAPBG}
  <div class="content">{body}
  </div>
 </div>
 <div class="edge"></div>
</section>""" for sid, a, b, body, _ in scenes)
page = open("edit/template.html").read()
page = (page.replace("{{DURATION}}", f"{DURATION:.3f}").replace("{{AROLL_END}}", f"{AROLL_END:.3f}").replace("{{AROLL}}", f"assets/video/aroll-t{N}.mp4")
        .replace("{{HUD}}", hud_html()).replace("{{SCENES}}", scene_html).replace("{{CAPTIONS}}", "\n".join(cap_html))
        .replace("{{SFX}}", sfx_html).replace("{{JS}}", "\n".join(cam_js + hud_js + js + cap_js)))
out = f"../2026-10-26-socials-trials/out/trial-{N}.html"
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, "w").write(page)
print(f"trial {N}: {len(scenes)} pages, {len(cap_html)} caption groups, {len(sfx)} sfx, {DURATION:.2f}s")
for sid, a, b, _, _ in scenes:
    print(f"  {sid:4s} {a:6.2f} – {b:6.2f}")
