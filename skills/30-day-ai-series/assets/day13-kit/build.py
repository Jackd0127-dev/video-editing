"""Day 13 — "an AI receptionist for wedding venues" (Jack's own pre-cut take, 1102.mov). Earlier header: Day 10 — "speak any language with AI" (Higgsfield audio -> ElevenLabs dubbing). One take, IMG_5555 (edit/trials/<n>/).
Built on the approved Day 7/8 machinery (helpers, captions, camera, assembly); Day 9 pages are in edit/pages9.py.
Run from the project root:  TRIAL=1 python3 -I edit/build.py  ->  ../2026-10-28-day9-trials/out/trial-1.html
(Day 8 header kept below for reference.)
Built on the approved Day 7 machinery (helpers, captions, camera, assembly); Day 8 pages and the Genjutsu layer are new.
OLD DAY 7 NOTES:
Two versions (tools/TRIAL-REELS.md): TRIAL=1 close-up hook (IMG_5508) and the full walk-through; TRIAL=2 the angle-2 hook
(IMG_5509, his last take) and a tighter, evergreen cut (posted on another day: no day lines, day page or end card). No screen recordings were filmed: Claude's screens are real frames from Anthropic's
Skills tutorial (assets/img/ui), the rest are code-built props that move on his words.
Run from the project root:  TRIAL=1 python3 -I edit/build.py  ->  ../2026-10-27-day8-trials/out/trial-1.html
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
DURATION = round(AROLL_END + {1: 5.2, 2: 2.7, 3: 2.1}[N], 3)  # Day 14: "what next?" card + end card after his last word
INK, PAPER, RED, MUTED = "#17120e", "#ede7df", "#17120e", "#7a6e63"
GRADE = ""  # never grade his footage
CALM = False

# ---------------------------------------------------------------- words and phrases
def norm(s):
    return re.sub(r"[^a-z0-9']", "", s.lower().replace("’", "'"))


NT = [norm(x["text"]) for x in TOK]


def w(phrase, after=0.0):
    """Index of the first word of `phrase` in this trial's cut (at or after `after` seconds)."""
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
    return TOK[i]["start"]


def te(i):
    """End of word i: the next word's start, or the end of its take."""
    seg_end = next((s["end"] for s in SEGS if s["start"] - 0.01 <= t(i) < s["end"]), AROLL_END)
    nxt = t(i + 1) if i + 1 < len(TOK) else AROLL_END
    return min(nxt, seg_end)


CUTS = [g["start"] for g in SEGS[1:]]
CUTS_ALL = [g["start"] for g in SEGS]
KEEP = {"I", "I'm", "I've", "I'll", "I'd", "AI", "Jack", "Claude", "Google", "Maps", "Karizma", "Turkish", "Barber", "Club", "Tools", "Advanced", "Search", "Fresha", "CRM", "Review", "Website", "Builder", "admin.novasagency.com"}


def disp(i):
    x = TOK[i]["text"].strip(",.!?;:")
    return x if x in KEEP else x.lower()


def cover_cut(e):
    """A page that ends just before a take change would flash the old take: hold it over the cut instead."""
    for c in CUTS:
        if e - 0.25 < c <= e + 0.4:
            return c + 0.3
    return e


def esc(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------- timeline helpers
scenes, js, sfx, VL, BROLL = [], [], [], [], []
CUR = '<svg viewBox="0 0 24 24"><path d="M5 3 L5 19 L9 15 L12 22 L15 20.5 L11.5 14 L18 14 Z" fill="#fff" stroke="#141414" stroke-width="1.4" stroke-linejoin="round"/></svg>'


def scene(sid, start, end, body, whoosh=True):
    for c in CUTS:  # a page that lands just after a take change would flash the new take: start on the cut
        if c <= start < c + 0.4:
            start = c - 0.02
    start = math.floor(start * 30 + 1e-6) / 30 - 0.002  # land on a frame, never one frame late
    scenes.append((sid, start, end, body))
    js.append(f"enter('#{sid}', {start:.3f});")
    if whoosh:
        sfx.append(("fast-whoosh", max(0, start - 0.32), 0.34))
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


def rev(sel, at, y=24):
    js.append(f"rev('{sel}', {at:.3f}, {{\"y\": {y}}});")


def pop(sel, at, s=0.6, y=20, d=0.35, ir=None):
    ft(sel, at, {"opacity": 0, "scale": s, "y": y}, {"opacity": 1, "scale": 1, "y": 0}, d, "back.out(2)", ir)


def slam(sel, at, s=1.5):
    ft(sel, at, {"opacity": 0, "scale": s, "filter": "blur(18px)"}, {"opacity": 1, "scale": 1, "filter": "blur(0px)"}, 0.4, "expo.out")


def words_in(pfx, i0, n):
    """Lead-in words that appear one by one with his voice (tokens i0 .. i0+n-1)."""
    spans = []
    for k in range(n):
        spans.append(f'<span class="ch" id="{pfx}{k}">{esc(disp(i0 + k))}</span>')
        ft(f"#{pfx}{k}", t(i0 + k) - 0.05, {"opacity": 0, "y": 14, "filter": "blur(10px)"}, {"opacity": 1, "y": 0, "filter": "blur(0px)"}, 0.25, "power2.out")
    return " ".join(spans)


def vid(vid_id, src, start, dur, style="", cls="pv"):
    return f'<video id="{vid_id}" class="clip {cls}" src="{src}" data-start="{start:.3f}" data-duration="{dur:.3f}" data-track-index="5" muted playsinline style="{style}"></video>'


def overlay(html_, start, end, sel):
    """Page videos live in their own layer above the pages (a timed <video> can't be nested in a timed page)."""
    VL.append(html_)
    ft(sel, start + 0.08, {"opacity": 0}, {"opacity": 1}, 0.3, "power2.out")
    js.append(f"tl.to('{sel}', {{opacity:0, duration:.42, ease:'sine.inOut', immediateRender:false}}, {end - 0.42:.3f});")


def typed_words(pfx, text):
    return " ".join(f'<span class="wd" id="{pfx}{k}">{esc(x)}</span>' for k, x in enumerate(text.split()))


def type_on(pfx, n, a, b, step=1):
    """Reveal n word spans evenly between a and b (typing rhythm) with key clicks."""
    for k in range(n):
        at = a + (b - a) * k / max(n - 1, 1)
        st(f"#{pfx}{k}", at, {"opacity": 1})
        if k % step == 0:
            sfx.append(("click_004", at, 0.08))


def click(cur, x, y, at, frm=(1120, 1500), leave=None, first=True):
    """A cursor glides in and clicks exactly at (x, y) (tip offset 14, 8)."""
    ft(cur, at - 0.6, {"x": frm[0], "y": frm[1], "opacity": 0, "scale": 1}, {"x": x - 14, "y": y - 8, "opacity": 1}, 0.55, "power3.out", None if first else False)
    to(cur, at, {"scale": 0.82, "yoyo": True, "repeat": 1}, 0.08)
    if leave:
        to(cur, at + 0.35, {"x": leave[0], "y": leave[1], "opacity": 0}, 0.45, "power2.in")
    sfx.append(("click_002", at, 0.4))


def send_lit(sel, at):
    ft(sel, at, {"backgroundColor": "rgba(23,18,14,.12)", "color": MUTED, "boxShadow": "0 0 0 0px rgba(23,18,14,.25)"},
       {"backgroundColor": INK, "color": "#fbf9f5", "boxShadow": "0 0 0 14px rgba(23,18,14,.18)"}, 0.3, "power2.out")
    to(sel, at + 0.3, {"boxShadow": "0 0 0 4px rgba(23,18,14,.1)", "yoyo": True, "repeat": 1}, 0.3)
    sfx.append(("tick_002", at, 0.2))


ICON = {
    "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4.2-4.2"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M3.5 7l8.5 6 8.5-6"/>',
    "cal": '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M8 3v4M16 3v4M3 10h18"/>',
    "phone": '<path d="M5 4h4l2 5-2.6 1.6a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    "people": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6"/><circle cx="17" cy="9" r="2.6"/><path d="M16.2 14.2c3 .3 5.3 2.4 5.3 5.8"/>',
    "list": '<path d="M9 6h12M9 12h12M9 18h12"/><circle cx="4.5" cy="6" r="1.2"/><circle cx="4.5" cy="12" r="1.2"/><circle cx="4.5" cy="18" r="1.2"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/>',
    "tool": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/>',
    "coin": '<circle cx="12" cy="12" r="9"/><path d="M15 9.2A3 3 0 0 0 9.5 10v2.5c0 1.5-.5 2.6-1.5 3.5H15.5M8 12.5h5"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-7 8-7s8 3 8 7"/>',
}


def ic(name, size=58, stroke=INK):
    return f'<svg viewBox="0 0 24 24" style="width:{size}px;height:{size}px;fill:none;stroke:{stroke};stroke-width:2.1;stroke-linecap:round;stroke-linejoin:round">{ICON[name]}</svg>'


CLAUDE = '<img src="assets/img/claude-mark.svg" style="width:{0}px;height:{0}px"/>'
LOGO = lambda n, s: f'<img src="assets/img/logos/{n}.svg" style="width:{s}px;height:{s}px;object-fit:contain"/>'
SEG_W = (900 - 29 * 6) / 30
BLOCKS = "".join(f'<i class="seg" id="{{p}}-s{k}"></i>' for k in range(30))


def step_head(pid, n, title_html, top=150, style="num"):
    """Step header. num: approved centred layout (small 'step', big number, title). big: numeral on the left (tight
    trial). agent: the 'AI sales team' member doing this step (wildcard trial)."""
    if style == "big":
        return f"""  <div id="{pid}-hd" class="row" style="position:absolute;left:90px;right:90px;top:{top}px;align-items:center;gap:34px">
    <span id="{pid}-n" class="xb" style="font-size:250px;line-height:.9">{n}</span>
    <div style="display:flex;flex-direction:column;gap:6px"><span id="{pid}-st" class="sm" style="font-size:46px">step {n} of 3</span><div id="{pid}-t" class="row" style="align-items:center;gap:16px">{title_html}</div></div>
  </div>"""
    if style == "agent":
        return f"""  <div class="stack" style="left:0;right:0;top:{top}px">
    <div id="{pid}-n" class="nd" style="width:150px;height:150px;border-radius:44px;position:relative">{CLAUDE.format(84)}<span class="agb">{ic(n, 30, '#fbf9f5')}</span></div>
    <span id="{pid}-st" class="sm" style="font-size:44px;margin-top:18px">the</span>
    <div id="{pid}-t" class="row" style="align-items:center;justify-content:center;gap:16px">{title_html}</div>
  </div>"""
    return f"""  <div class="stack" style="left:0;right:0;top:{top}px">
    <span id="{pid}-st" class="sm" style="font-size:56px">step</span>
    <span id="{pid}-n" class="xb" style="font-size:210px;line-height:.95">{n}</span>
    <div id="{pid}-t" class="row" style="align-items:center;justify-content:center;gap:20px;margin-top:6px">{title_html}</div>
  </div>"""


def head_in(pid, at, style="num"):
    rev(f"#{pid}-st", at + 0.03, 10)
    if style == "agent":
        ft(f"#{pid}-n", at + 0.04, {"opacity": 0, "scale": 0.4, "rotation": -90}, {"opacity": 1, "scale": 1, "rotation": 0}, 0.5, "back.out(1.8)")
    else:
        slam(f"#{pid}-n", at + 0.06)
    rev(f"#{pid}-t", at + 0.2, 24)
    sfx.append(("dry-pop-alert", at + 0.06, 0.24))




def pg_day():
    """'This is day eight of 30' — the series stat page, today's block lifts."""
    i = w("this is day eight")
    s, e = t(i) - 0.06, cover_cut(t(i + 5) + 0.6)
    scene("pday", s, e, f"""
  <div class="stack" style="left:0;right:0;top:600px">
    <span class="sm" style="font-size:56px">{words_in('pdw', i, 2)}</span>
    <div class="row" style="align-items:flex-end;justify-content:center;margin-top:10px">
      <span id="pday-d" class="xb" style="font-size:230px;line-height:1">Day</span>
      <span id="pday-n" class="xb" style="font-size:230px;line-height:1;margin-left:40px">8</span>
    </div>
    <span class="sm" style="font-size:56px;margin-top:22px">{words_in('pdo', i + 4, 2)}</span>
  </div>
  <div id="pday-bar" class="bar big" style="top:1250px">{BLOCKS.replace('{p}', 'pday')}</div>""")
    ft("#pday-d", t(i + 2) - 0.05, {"opacity": 0, "y": 60, "filter": "blur(14px)"}, {"opacity": 1, "y": 0, "filter": "blur(0px)"}, 0.4, "expo.out")
    slam("#pday-n", t(i + 3) - 0.05)
    ft("#pday-bar .seg", t(i + 3), {"scaleY": 0, "opacity": 0}, {"scaleY": 1, "opacity": 1, "stagger": 0.01}, 0.22, "power2.out")
    ft("#pday-s0, #pday-s1, #pday-s2, #pday-s3, #pday-s4, #pday-s5, #pday-s6", t(i + 3) + 0.25, {"backgroundColor": "rgba(23,18,14,.14)"}, {"backgroundColor": INK, "stagger": 0.06}, 0.15)
    ft("#pday-s7", t(i + 5), {"backgroundColor": "rgba(23,18,14,.14)", "scaleY": 1}, {"backgroundColor": INK, "scaleY": 1.9}, 0.45, "back.out(2.2)")
    sfx.extend([("dry-pop-alert", t(i + 3), 0.24), ("pluck_001", t(i + 5), 0.26)])




def pg_end():
    """'(I will) see you on day nine' — 30 blocks, today's eight lit, zoom into day 8."""
    i = w("see you on")
    s = t(i) - 0.06
    ZX, ZY = 90 + 7 * (SEG_W + 6) + SEG_W / 2, 1340 - 40 * 1.9 / 2
    scene("ed", s, DURATION, f"""
  <div id="ed-zoom" style="position:absolute;inset:0;transform-origin:{ZX:.1f}px {ZY:.1f}px">
    <div class="stack" style="left:0;right:0;top:560px">
      <span class="sm" style="font-size:56px">{words_in('edw', i, 3)}</span>
      <div class="row" style="align-items:flex-end;justify-content:center;margin-top:6px">
        <span id="ed-day" class="xb" style="font-size:230px;line-height:1">Day</span>
        <span id="ed-n" class="xb" style="font-size:230px;line-height:1;margin-left:40px">9</span>
      </div>
    </div>
    <span id="ed-lbl" class="note" style="position:absolute;left:{90 + 7 * (SEG_W + 6):.0f}px;top:1186px">day 08 / 30</span>
    <div id="ed-bar" class="bar big" style="top:1300px">{BLOCKS.replace('{p}', 'ed')}</div>
  </div>""")
    rev("#ed-day", t(i + 3) - 0.05, 30)
    slam("#ed-n", t(i + 4) - 0.05)
    ft("#ed-bar .seg", s + 0.1, {"scaleY": 0, "opacity": 0}, {"scaleY": 1, "opacity": 1, "stagger": 0.014}, 0.3, "power2.out")
    lit = t(i + 4) + 0.45
    ft("#ed-s0, #ed-s1, #ed-s2, #ed-s3, #ed-s4, #ed-s5, #ed-s6", lit - 0.3, {"backgroundColor": "rgba(23,18,14,.14)"}, {"backgroundColor": INK, "stagger": 0.08}, 0.2)
    ft("#ed-s7", lit, {"backgroundColor": "rgba(23,18,14,.14)", "scaleY": 1}, {"backgroundColor": INK, "scaleY": 1.9}, 0.5, "back.out(2.2)")
    ft("#ed-lbl", lit + 0.15, {"opacity": 0, "y": 12}, {"opacity": 1, "y": 0}, 0.35, "power2.out")
    ft("#ed-s7", lit + 0.6, {"scaleY": 1.9}, {"scaleY": 2.2, "yoyo": True, "repeat": 1}, 0.6, "sine.inOut", False)
    zoom_at = DURATION - 1.4
    to("#ed-lbl", zoom_at, {"opacity": 0}, 0.3)
    ft("#ed-zoom", zoom_at, {"scale": 1, "x": 0, "y": 0}, {"scale": 60, "x": round(540 - ZX, 1), "y": round(960 - ZY, 1)}, 1.3, "power3.inOut")
    sfx.extend([("dry-pop-alert", t(i + 4), 0.24), ("pluck_001", lit, 0.3), ("riser", zoom_at + 0.25, 0.35), ("boom", DURATION - 0.12, 0.3)])




# ================================================================= Day 7 pages: series look (face, then paper pages) with a prop per
# phrase that moves on its words (references/reference-motion-reel.md); real Claude screens from Anthropic's own Skills tutorial
# (assets/img/ui, references/claude-ui/skills-tutorial) wherever the app is on screen; no drawn app UIs.
ENV = json.load(open(f"{D}/env30.json"))
OV = []
TICK = "&#10003;"


def nxt_start(phrase, after=0.0):
    e = t(w(phrase, after)) - 0.06
    for c in CUTS:
        if c <= e < c + 0.4:
            e = c - 0.02
    return e


def head(pid, small, big, top=200, size=120):
    return f"""  <div class="stack" style="left:0;right:0;top:{top}px"><div class="row" style="align-items:baseline;gap:20px"><span id="{pid}-a" class="sm" style="font-size:56px">{small}</span><span id="{pid}-h" class="xb" style="font-size:{size}px">{big}</span></div></div>"""


def doc(pid, name, lines=6, logo=True, style=""):
    ls = "".join(f'<i class="dl{" k" if k == 0 else ""}" style="width:{(92, 70, 84, 60, 78, 50, 66)[k % 7]}%"></i>' for k in range(lines))
    lg = f'<img src="assets/img/claude-mark.svg" style="width:62px;height:62px"/><span class="dt">Skill</span>' if logo else ""
    return f'<div class="doc shd" id="{pid}" style="{style}"><span class="dn">{name}</span>{ls}{lg}</div>'


def count_js(el, a, b, at, d, fmt="Math.round(o.n)"):
    js.append(f"(function(){{ const o = {{n:{a}}}; tl.fromTo(o, {{n:{a}}}, {{n:{b}, duration:{d:.3f}, ease:'power1.inOut', onUpdate(){{ (document.getElementById('{el}') || {{}}).textContent = {fmt}; }}}}, {at:.3f}); }})();")


def text_at(el, at, val, prev):
    """Switch an element's text at a time (seek-safe: a tiny tween on a counter, so scrubbing back restores it)."""
    js.append(f"(function(){{ const o = {{n:0}}; tl.fromTo(o, {{n:0}}, {{n:1, duration:.01, ease:'none', immediateRender:false, onUpdate(){{ (document.getElementById('{el}') || {{}}).textContent = o.n >= 1 ? {json.dumps(val)} : {json.dumps(prev)}; }}}}, {at:.3f}); }})();")


def stamp(sel, at, rot=-10):
    ft(sel, at, {"opacity": 0, "scale": 2.6, "rotation": rot * 2.4}, {"opacity": 1, "scale": 1, "rotation": rot}, 0.3, "back.out(1.6)")
    sfx.extend([("boom", at + 0.05, 0.16), ("hard-pop-click", at + 0.05, 0.28)])



# ================================================================= Day 8: the Genjutsu shot (his Higgsfield output) lives in the camera, lined up
# with the real take (edit/gen/: audio-synced section by section, face/body boxes -> scale + offset, gaps filled with the
# generated studio's own edge colours). Real screens and images only (his ChatGPT screenshot, his Riven board and sheet);
# props are code-built and move on his words.
GENL, CIN, CAMFIX, CAMJS = [], [], [], []
ICON.update({
    "box": '<path d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5z"/><path d="M3 7.5 12 12l9-4.5M12 12v9"/>',
    "bulb": '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.6 10.8c.8.6 1.1 1.4 1.1 2.2h5c0-.8.3-1.6 1.1-2.2A6 6 0 0 0 12 3z"/>',
    "cart": '<circle cx="9" cy="20" r="1.6"/><circle cx="18" cy="20" r="1.6"/><path d="M2.5 3.5h3l2.4 11.5h11l2-8H6.7"/>',
    "play": '<circle cx="12" cy="12" r="9.5"/><path d="M10 8.3v7.4l6-3.7z" fill="currentColor"/>',
    "img": '<rect x="3" y="4" width="18" height="16" rx="3"/><circle cx="9" cy="10" r="2"/><path d="m3.5 18 5.5-5.5 4 4 3-3 4.5 4.5"/>',
    "spark": '<path d="M12 2.5 14 10l7.5 2-7.5 2-2 7.5-2-7.5-7.5-2 7.5-2z"/>',
    "q": '<circle cx="12" cy="12" r="9.5"/><path d="M9.3 9.3a2.8 2.8 0 1 1 3.7 2.6c-.6.3-1 .9-1 1.6v.6"/><circle cx="12" cy="17.2" r=".6" fill="currentColor"/>',
    "tagi": '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.6"/>',
    "film": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M7 5v14M17 5v14M3 9.5h4M3 14.5h4M17 9.5h4M17 14.5h4"/>',
    "heart": '<path d="M12 20s-8-5-8-10.5A4.5 4.5 0 0 1 12 7a4.5 4.5 0 0 1 8 2.5C20 15 12 20 12 20z"/>',
})
OPENAI = LOGO("openai", 1).replace('style="width:1px;height:1px', 'style="width:{0}px;height:{0}px')
HF = '<img src="assets/img/logos/higgsfield.png" style="width:{0}px;height:{0}px;border-radius:{1}px"/>'
GTR = "assets/img/guitar/"


def seg_of(src, n=0):
    """The n-th segment of this cut that comes from source key `src`."""
    return [s for s in SEGS if s["src"] == src][n]


CAMMAP = []  # (a, b, z0, z1, ox, oy) scripted camera windows, for caption placement


def cam_hold(a, b, z, ox=530, oy=800, slam=None):
    """Hand-scripted camera between a and b (the auto punch-ins skip this window)."""
    CAMFIX.append((a, b))
    CAMMAP.append((a, b, slam or z, z, ox, oy))
    if slam:
        CAMJS.append(f"tl.fromTo('#cam', {{scale:{slam}, transformOrigin:'{ox}px {oy}px'}}, {{scale:{z}, duration:.5, ease:'expo.out'}}, {a:.3f});")
        CAMJS.append(f"tl.fromTo('#cam', {{scale:{z}}}, {{scale:{z}, duration:{b - a - 0.5:.3f}, ease:'none', immediateRender:false}}, {a + 0.5:.3f});")
    else:
        CAMJS.append(f"tl.fromTo('#cam', {{scale:{z}, transformOrigin:'{ox}px {oy}px'}}, {{scale:{z}, duration:{b - a:.3f}, ease:'none', immediateRender:false}}, {a:.3f});")


def cam_out(a, d, z0, z1, ox=530, oy=800):
    CAMFIX.append((a, a + d))
    CAMMAP.append((a, a + d, z0, z1, ox, oy))
    CAMJS.append(f"tl.fromTo('#cam', {{scale:{z0}, transformOrigin:'{ox}px {oy}px'}}, {{scale:{z1}, duration:{d:.3f}, ease:'power2.inOut', immediateRender:false}}, {a:.3f});")


def clip_tw(sel, at, a, b, d, e="power2.inOut", ir=None):
    ft(sel, at, {"clipPath": a}, {"clipPath": b}, d, e, ir)


def divider(did, left="REAL", right="AI"):
    CIN.append(f'<div class="dvw" id="{did}"><i class="dl8"></i><span class="kn8"><i class="l"></i><i class="r"></i></span>'
               f'<span class="lb8 lft">{left}</span><span class="lb8 rgt">{right}</span></div>')


def dv_to(did, gid, at, pct, d=0.4, e="power2.inOut", first=False):
    """Move divider `did` to pct% of the frame and clip Genjutsu layer `gid` to the right of it."""
    to(f"#{did}", at, {"x": round(pct * 10.8, 1)}, d, e)
    js.append(f"tl.to('#{gid}', {{clipPath:'inset(0% 0% 0% {pct}%)', duration:{d:.3f}, ease:'{e}', immediateRender:false}}, {at:.3f});")


def ring_cam(rid, cx, cy, rx, ry, rot, at, out, tag=None, tx=0, ty=0, dark=False):
    """A white ring drawn round something in the footage (inside the camera, so it stays on it)."""
    CIN.append(f'<svg class="rg8" id="{rid}" viewBox="0 0 1080 1920"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx} {cy})" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"/></svg>')
    ft(f"#{rid}", at, {"opacity": 0}, {"opacity": 1}, 0.05, "none")  # round caps would leave a dot before the stroke draws
    ft(f"#{rid} ellipse", at, {"strokeDashoffset": 100}, {"strokeDashoffset": 0}, 0.45, "power2.out")
    to(f"#{rid}", out, {"opacity": 0}, 0.25)
    sfx.append(("scribble", at, 0.18))
    if tag:
        CIN.append(f'<span class="rtag8{" dk" if dark else ""}" id="{rid}-t" style="left:{tx}px;top:{ty}px">{tag}</span>')
        ft(f"#{rid}-t", at + 0.25, {"opacity": 0, "scale": 0.4, "rotation": -12}, {"opacity": 1, "scale": 1, "rotation": -4}, 0.32, "back.out(2.2)")
        to(f"#{rid}-t", out, {"opacity": 0, "scale": 0.7}, 0.22)


def sticker(sid, inner, x, y, rot, at, out, cls="", s0=0.2):
    """Buzzword sticker over his footage: white border, tilt, bounce in, one wiggle, quick out."""
    OV.append(f'<div class="sk8 {cls}" id="{sid}" style="left:{x}px;top:{y}px">{inner}</div>')
    ft(f"#{sid}", at, {"opacity": 0, "scale": s0, "rotation": rot * 2.5}, {"opacity": 1, "scale": 1, "rotation": rot}, 0.38, "back.out(2)")
    ft(f"#{sid}", at + 0.42, {"rotation": rot}, {"rotation": rot - 5, "yoyo": True, "repeat": 1}, 0.12, "sine.inOut", False)
    to(f"#{sid}", out, {"opacity": 0, "scale": 0.6}, 0.2, "power2.in")
    sfx.append(("dry-pop-alert", at, 0.22))


def sk_ic(icon, word, size=62):
    return f'<span class="ic8">{ic(icon, size)}</span>{word}'


def xstamp(sid, text, x, y, at, out, rot=-10, wt=False):
    OV.append(f'<div class="xst8{" wt" if wt else ""}" id="{sid}" style="left:{x}px;top:{y}px">{text}</div>')
    stamp(f"#{sid}", at, rot)
    to(f"#{sid}", out, {"opacity": 0}, 0.2)



CAPFORCE = []  # (a, b, top_px) forced caption bands
exec(open("edit/pages10.py").read())
exec(open("edit/pages10b.py").read())
exec(open("edit/pages12.py").read())
exec(open("edit/pages13.py").read())
exec(open("edit/pages14.py").read())

# ================================================================= the two versions
def page_end(sid):
    return next(b for s_, a, b, _ in scenes if s_ == sid)


def page_start(sid):
    return next(a for s_, a, b, _ in scenes if s_ == sid)


# Day 14 (four takes cut together). V1: his sales hook, the Day 14 card, each step on his face with his real screen in a card under
# his chin, paper notes on the key moments, Claude's finished site, the CRM, then "what next?" + the Day 15 end card. V2 (evergreen,
# posted another day): cold open on Karizma (75 reviews, 4.7 stars, no website), a tighter walk-through, ends on the "what next?" card.
# V3 (evergreen, ~60 s): opens on his promise line, one beat per step, ends on the "what next?" card.
if N == 1:
    hook14()
    pg_day14()
elif N == 2:
    open14()
    hook14()
today14()
pitch14()
google14()
adv14()
active14()
maps14()
validate14()
nosite14()
qualified14()
claude14()
smart14()
models14()
easy14()
wait14()
site14()
crmsite14()
if N == 1:
    pg_next(AROLL_END - 0.1, AROLL_END + 2.5)
    pg_end14(AROLL_END + 2.3)
else:
    pg_next(AROLL_END - 0.1, DURATION)
finalize14()

# ---------------------------------------------------------------- captions: auto groups (small lead-in, bold phrase, italic accent)
STOPW = set("a an the to of and or but so that is i you it in on for with my your be we're i'm i'll it's they them their if as do does can will just what this these at by from up me we gonna wanna been are was there some sort not now when which who how where why get got have don't didn't could would might need want".split())
ITAL = {"today", "streamlined", "fine", "perfect", "free", "money", "next"}


def groups():
    out, cur = [], []
    BREAKS = set()
    for i, x in enumerate(TOK):
        if cur and i in BREAKS:
            out.append(cur)
            cur = []
        if cur and TOK[i].get("spk") != TOK[i - 1].get("spk"):  # a new speaker starts a new line
            out.append(cur)
            cur = []
        if cur:
            gap = t(i) - te(i - 1)
            prev = TOK[i - 1]["text"]
            if prev.endswith((".", "?", "!")) or (prev.endswith(",") and len(cur) >= 2) or gap > 0.35 or len(cur) >= 5:
                out.append(cur)
                cur = []
        cur.append(i)
    if cur:
        out.append(cur)
    for k in range(len(out) - 1):  # never end a group on a dangling "to"/"a": move it to the next line
        while len(out[k]) > 2 and NT[out[k][-1]] in STOPW and not TOK[out[k][-1]]["text"].endswith((",", ".")) and t(out[k + 1][0]) - te(out[k][-1]) < 0.35:
            out[k + 1].insert(0, out[k].pop())
    return out


CAPS = []
for g in groups():
    g = [i for i in g if TOK[i]["text"]]
    if not g:
        continue
    styles = ["s"] * len(g)
    if NT[g[-1]] not in STOPW:
        styles[-1] = "b"
        if len(g) >= 3 and NT[g[-2]] not in STOPW and len(disp(g[-2]) + disp(g[-1])) <= 15:
            styles[-2] = "b"
        if styles.count("b") == 1 and NT[g[-1]] in ITAL:
            styles[-1] = "i"
    bold = [disp(i) for i, sx in zip(g, styles) if sx in "bi"]
    if sum(len(x) for x in bold) * 58 > 960:
        styles = ["s"] * len(g)
    CAPS.append(list(zip(g, styles)))

cap_cover = [(a, b) for _, a, b, _ in scenes] + [(b_["start"], b_["end"]) for b_ in BROLL]
_m = []
for a_, b_ in sorted(cap_cover):  # pages under a second apart dissolve into each other: no caption in between
    if _m and a_ <= _m[-1][1] + 1.0:
        _m[-1] = (_m[-1][0], max(_m[-1][1], b_))
    else:
        _m.append((a_, b_))
cap_cover = _m


def next_cover(at):
    starts = [a for a, b in cap_cover if a > at + 0.01]
    return min(starts) if starts else AROLL_END


samples = []
for line in open(f"{D}/faces-2fps.txt"):
    p = line.split()
    if p[1] != "none":
        samples.append(((int(p[0][1:5]) - 1) / 2, *map(float, p[1:5])))
lifted = []  # (old caption lift windows; captions are now placed per face after the camera)
# ---------------------------------------------------------------- b-roll layer (inside the camera, muted)
br_html = "".join(f'<video id="br{n}" class="clip brl" src="{b["file"]}" data-start="{b["start"]:.3f}" data-media-start="{b.get("media", 0):.3f}" data-duration="{b["end"] - b["start"]:.3f}" data-track-index="1" muted playsinline></video>' for n, b in enumerate(BROLL))
br_html += "".join(f'<video id="{g["id"]}" class="clip gv" src="{g["file"]}" data-start="{g["start"]:.3f}" data-media-start="{g["media"]:.3f}" data-duration="{g["end"] - g["start"]:.3f}" data-track-index="{6 + k}" muted playsinline style="z-index:{2 + k};{g.get("style", "")}"></video>' for k, g in enumerate(GENL))
br_html += "".join(CIN)
br_windows = [(b["start"], b["end"]) for b in BROLL]
sfx += [("arrow-whoosh", b["start"] - 0.25, 0.22) for b in BROLL if b["start"] > 0.5]

# ---------------------------------------------------------------- camera: hook slam, face-aware punch-ins, slow push on b-roll
edges = sorted(set([0.0] + call_edges() + [s_["start"] for s_ in SEGS] + [x for w_ in cap_cover + br_windows + CAMFIX for x in w_]))
edges = [x for x in edges if x < AROLL_END - 0.05] + [AROLL_END]
merged = []
for x in edges:
    if not merged or x - merged[-1] >= 0.1:
        merged.append(x)
edges = merged if merged[-1] == AROLL_END else merged[:-1] + [AROLL_END]
CAP_CLEAR = 0.345
ZOOMS = [1.0, 1.05, 1.1, 1.15] if CALM else [1.0, 1.06, 1.12, 1.18, 1.24]
cam_js, soft_cuts = [], []
prev_size, tight = None, False
def fixed(a, b):
    return any(fa - 0.01 <= a and b <= fb + 0.01 for fa, fb in CAMFIX)


cam_js.extend(CAMJS)
for a, b in zip(edges, edges[1:]):
    if fixed(a, b):
        prev_size = None
        continue
    covered = any(pa - 0.01 <= a and b <= pb + 0.01 for pa, pb in cap_cover)
    on_broll = any(pa - 0.01 <= a and b <= pb + 0.01 for pa, pb in br_windows)
    win = [f for f in samples if a - 0.3 <= f[0] <= b + 0.3]
    if a == 0:
        cam_js.append("tl.fromTo('#cam', {scale:1.35, transformOrigin:'540px 960px'}, {scale:1, duration:.5, ease:'expo.out'}, 0);")
        cam_js.append(f"tl.fromTo('#cam', {{scale:1}}, {{scale:1.04, duration:{b - 0.5:.3f}, ease:'none', immediateRender:false}}, .5);")
        continue
    if covered or on_broll or not win:
        cam_js.append(f"tl.fromTo('#cam', {{scale:1, transformOrigin:'540px 960px'}}, {{scale:1.04, duration:{b - a:.3f}, ease:'none', immediateRender:false}}, {a:.3f});")
        CAMMAP.append((a, b, 1.0, 1.04, 540, 960))
        if not covered:
            prev_size = None
        continue
    head = [f for f in win if f[0] <= a + 0.6] or win
    tail = [f for f in win if f[0] >= b - 0.6] or win
    cx = sum(f[1] + f[3] / 2 for f in win) / len(win)
    cy = sum(f[2] + f[4] / 2 for f in win) / len(win)
    top = min(f[2] for f in win)
    w_head = sum(f[3] for f in head) / len(head)
    w_tail = sum(f[3] for f in tail) / len(tail)
    clear = 0.28 if any(la < b and a < lb for la, lb in lifted) else CAP_CLEAR
    zmax = max(1.0, (cy - clear) / max(cy - top, 1e-3) / 1.025)
    options = [z for z in ZOOMS if z <= zmax + 1e-6] or [1.0]
    if prev_size is None:
        z = options[0]
    else:
        def score(z):
            r = w_head * z / prev_size
            return (abs(r - 1) >= 0.14, (r > 1) == (not tight), -abs(abs(r - 1) - 0.2))
        z = max(options, key=score)
        if abs(w_head * z / prev_size - 1) < 0.14:
            soft_cuts.append(a)
    prev_size, tight = w_tail * z * 1.025, z >= 1.12
    cam_js.append(f"tl.fromTo('#cam', {{scale:{z}, transformOrigin:'{int(cx * 1080)}px {int(cy * 1920)}px'}}, {{scale:{z * 1.025:.4f}, duration:{b - a:.3f}, ease:'none', immediateRender:false}}, {a:.3f});")
    CAMMAP.append((a, b, z, z * 1.025, int(cx * 1080), int(cy * 1920)))

# ---------------------------------------------------------------- captions (placed after the camera so they know its zoom)
CAP_TOP_MIN = 0.22 * 1920


def cap_height(grp):
    small = [disp(i) for i, sx in grp if sx == "s"]
    big = [disp(i) for i, sx in grp if sx != "s"]
    h = 0
    if small:
        h += 54 * max(1, math.ceil(sum(len(x) + 1 for x in small) * 24 / 980))
    if big:
        h += 126 * max(1, math.ceil(sum(len(x) + 1 for x in big) * 60 / 980))
    return h + 18


HOOK_FACE = (700, 990)  # the real hook take (b-roll / before-after) face band in screen px, even at the 1.6x hold


def face_band(g0, g1):
    """Screen-space vertical extent of his face during a caption group (px), through scripted camera windows; auto punch-ins
    are taken at their largest (1.27x about the face centre)."""
    if any(g0 < b_["end"] and g1 > b_["start"] for b_ in BROLL) or any(g0 < g_["end"] and g1 > g_["start"] for g_ in GENL if g_["id"] in ("pR", "pG")):
        return HOOK_FACE
    fs = [f for f in samples if g0 - 0.3 <= f[0] <= g1 + 0.3]
    if not fs:
        return None
    tops, bots = [], []
    for (tt, x, y, wf, hf) in fs:
        win = [m for m in CAMMAP if m[0] - 0.01 <= tt <= m[1] + 0.01]
        if win:
            a, b, z0, z1, ox, oy = win[-1]  # the latest camera window wins (a card's push over a note's hold)
            for z in (z0, z1):
                tops.append(oy + z * ((y - HAIR * hf) * 1920 - oy))
                bots.append(oy + z * ((y + hf) * 1920 - oy))
        else:
            cy = (y + hf / 2) * 1920
            for z in (1.0, 1.27):
                tops.append(cy + z * ((y - HAIR * hf) * 1920 - cy))
                bots.append(cy + z * ((y + hf) * 1920 - cy))
    return min(tops) - 30, max(bots) + 45


cap_html, cap_js, lifted = [], [], []
for gi, grp in enumerate(CAPS):
    idx = [i for i, _ in grp]
    if t(idx[0]) < TEASER_END:
        continue
    g_start = max(0.0, t(idx[0]) - 0.08)
    for pa, pb in sorted(cap_cover):
        if pa - 0.01 <= g_start < pb:
            g_start = pb + 0.01
    next_start = t(CAPS[gi + 1][0][0]) - 0.08 if gi + 1 < len(CAPS) else AROLL_END
    end = min(next_start, next_cover(g_start), te(idx[-1]) + 0.6)
    for fa, fb, _ in CAPFORCE + [(x, y, 0) for x, y in CAPBELOW] + CAPAT:  # a forced band never runs past its window, and a group never runs into one
        if fa - 0.05 <= g_start < fb:
            end = min(end, fb)
        elif g_start < fa < end:
            end = fa
    if end - g_start < 0.3 or g_start > te(idx[-1]) - 0.05:
        continue
    if any(fa - 0.05 <= g_start < fb for fa, fb, _ in CAPFORCE):  # over an overlay: if it can't fit above his head, go small
        _bd = face_band(g_start, end)
        if _bd is not None and _bd[0] - 16 - cap_height(grp) < 330:
            grp = [(i, "s") for i, _ in grp]
    small = [f'<span class="w cs" id="w{i}">{esc(disp(i))}</span>' for i, sx in grp if sx == "s"]
    big = [f'<span class="w {"cb" if sx == "b" else "ci"}" id="w{i}">{esc(disp(i))}</span>' for i, sx in grp if sx != "s"]
    rows = (f'<div class="cl">{" ".join(small)}</div>' if small else "") + (f'<div class="cl">{" ".join(big)}</div>' if big else "")
    scrim = " scrim" if any(g_start < bb["end"] and end > bb["start"] for bb in BROLL + GENL) else ""
    # Captions sit below TikTok's top tabs (top 22 %) and never on the face: right above the head when there is room,
    # otherwise under the chin (with a soft scrim behind the words). Face boxes are mapped through the camera.
    h_cap = cap_height(grp) + (36 if TOK[idx[0]].get("spk") == "jess" else 0)
    forced = next((ft_ for fa, fb, ft_ in CAPFORCE if fa - 0.05 <= g_start < fb), None)
    band = face_band(g_start, end)
    below = any(fa - 0.05 <= g_start < fb for fa, fb in CAPBELOW)
    at_band = next((tp for fa, fb, tp in CAPAT if fa - 0.05 <= g_start < fb), None)
    if at_band is not None:  # Day 14: under the big site window
        top = at_band
        scrim = " scrim"
    elif below and band is not None:  # Day 14: a card sits above his head -> captions under his chin
        top = min(band[1] + 95, 1760 - h_cap)
        scrim = " scrim"
    elif forced is not None:
        top = forced
        scrim = " scrim sx2"
        if band is not None:  # over an overlay: sit right above his head (clear of TikTok's tabs, which end ~300 px)
            top = max(330, min(forced, band[0] - 16 - h_cap))
    elif band is None:
        top = CAP_TOP_MIN + 20
    elif band[0] - 16 - h_cap >= 330:  # above his head, at most into the bottom edge of TikTok's tabs (they end ~300 px)
        top = band[0] - 16 - h_cap
    elif UNDER_CHIN:
        top = min(band[1] + 110, 1600 - h_cap)
        scrim = " scrim"
        if band[1] + 110 + h_cap > 1600:  # no room under the chin either: above the head, a little into the top band
            top = max(CAP_TOP_MIN - 90, band[0] - 16 - h_cap)
            scrim = ""
    else:  # Day 13: the notes live on his chest, so captions stay above his head, as high as TikTok's tabs allow
        top = 330
    lift = f' style="top:{top:.0f}px;bottom:auto" data-band="{top:.0f},{top + h_cap:.0f}"'
    scrim += " jess" if TOK[idx[0]].get("spk") == "jess" else ""
    cap_html.append(f'<div class="cap clip{scrim}" id="cap{gi}"{lift} data-start="{g_start:.3f}" data-duration="{end - g_start:.3f}" data-track-index="2"><div class="capi">{rows}</div></div>')
    for i in idx:
        cap_js.append(f"word('#w{i}', {max(0.0, t(i) - 0.05):.3f});")
    cap_js.append(f"tl.fromTo('#cap{gi} .capi', {{opacity:1, filter:'blur(0px)', y:0}}, {{opacity:0, filter:'blur(10px)', y:-10, duration:.12, ease:'power1.in', immediateRender:false}}, {end - 0.12:.3f});")


# Pages crossfade into the footage; a page that hands to another page (or leaves under a second of face) dissolves into it.
scenes.sort(key=lambda x: x[1])
handoff = set()
for k in range(len(scenes) - 1):
    sid, a, b_end, body = scenes[k]
    nid, na, nb, nbody = scenes[k + 1]
    if na <= b_end + 1.0:
        scenes[k] = (sid, a, max(b_end, na + 0.34), body)
        handoff.add(sid)
        js.append(f"tl.fromTo('#{nid}', {{opacity:0}}, {{opacity:1, duration:.32, ease:'sine.inOut'}}, {na:.3f});")
back_js = []
for sid, a, b_end, _ in scenes:
    if b_end >= AROLL_END - 0.01 or sid in handoff:
        continue
    if any(abs(b_end - w_[0]) < 0.05 for w_ in br_windows):
        continue
    back_js.append(f"tl.fromTo('#{sid}', {{opacity:1}}, {{opacity:0, duration:.42, ease:'sine.inOut', immediateRender:false}}, {b_end - 0.42:.3f});")
    back_js.append(f"tl.fromTo('#{sid} .sheet', {{scale:1, filter:'blur(0px)'}}, {{scale:1.03, filter:'blur(10px)', duration:.42, ease:'sine.inOut', immediateRender:false}}, {b_end - 0.42:.3f});")
cut_starts = [s_["start"] for s_ in SEGS[1:]]
if os.path.exists(f"{D}/qa-latest.json"):
    soft_cuts += [j for j in json.load(open(f"{D}/qa-latest.json"))["jumps"] if not any(abs(j - x) < 0.05 for x in soft_cuts)]
soft_cuts += [c for c in CUTS if not any(abs(c - x) < 0.05 for x in soft_cuts)]  # Day 9: one take with many joins -> a soft focus pull on every visible cut
for a in soft_cuts:
    if any(abs(a - c) < 0.02 for c in cut_starts) and not any(abs(a - x[1]) < 0.05 for x in scenes):
        back_js.append(f"focus({a:.3f});")

# ---------------------------------------------------------------- assemble
D5CSS = open("edit/day6.css").read() + open("edit/day7.css").read() + open("edit/day8.css").read() + open("edit/day9.css").read() + open("edit/day10.css").read() + open("edit/day10b.css").read() + open("edit/day12.css").read() + open("edit/day13.css").read() + open("edit/day14.css").read()
sfx_html = "\n".join(f'<audio id="sfx{n}" src="assets/audio/sfx/{name}.wav" data-start="{max(0.0, at):.3f}" data-track-index="{20 + n}" data-volume="{vol}"></audio>'
                     for n, (name, at, vol) in enumerate(sorted(sfx, key=lambda x: x[1])))
scene_html = f'<div id="ovl" style="position:absolute;inset:0;pointer-events:none">{"".join(OV)}</div>\n' + "\n".join(f"""<section class="scene clip" id="{sid}" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="3">
 <div class="sheet"><img class="paper" src="assets/img/paper-clean.jpg"/>
  <div class="content">{body}
  </div>
 </div>
</section>""" for sid, a, b, body in scenes) + f'\n<div id="vlayer" style="position:absolute;inset:0;pointer-events:none;z-index:40">{"".join(VL)}</div>'
page = open("edit/template.html").read()
page = re.sub(r'\s*<audio id="bgm"[^>]*></audio>', "", page)  # no music bed (the -music version is mixed after the render)
page = page.replace('src="assets/video/aroll.mp4"', f'src="assets/video/aroll-t{N}.mp4"').replace("</style>", D5CSS + "    </style>")
page = (page.replace("{{DURATION}}", f"{DURATION:.3f}").replace("{{AROLL_END}}", f"{AROLL_END:.3f}")
        .replace("{{SCENES}}", scene_html).replace("{{CAPTIONS}}", "\n".join(cap_html)).replace("{{GRADE_LAYER}}", br_html)
        .replace("{{SFX}}", sfx_html).replace("{{JS}}", "\n".join(cam_js + back_js + js + cap_js))
        .replace("{{GRADE}}", GRADE).replace("{{INK}}", INK).replace("{{PAPER}}", PAPER).replace("{{RED}}", RED).replace("{{MUTED}}", MUTED))
out = f"../{os.path.basename(os.getcwd())}-trials/out/trial-{N}.html"  # sibling <project>-trials folder
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, "w").write(page)
print(f"trial {N}: {len(scenes)} pages, {len(cap_html)} caption groups, {len(BROLL)} b-roll, {len(sfx)} sfx, {DURATION:.2f}s")
for sid, a, b, _ in scenes:
    print(f"  {sid:4s} {a:6.2f} – {b:6.2f}")


