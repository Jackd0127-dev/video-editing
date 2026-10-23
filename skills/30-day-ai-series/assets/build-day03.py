"""Day 3 — "make your own viral AI creator" (approved v5). Reference for: one long take with many retakes,
screen recordings + real generated images on pages, page videos in their own layer (VL / overlay()),
pages that snap to cuts (cover_cut / scene()), page-to-page dissolves, hook experiments (HOOK=1..5 with
hooks-day03.py, FULL=1 for a whole video with that hook), and a separate music version (scripts/mixbed.sh).
Copy it into a new project as edit/build.py and hooks-day03.py as edit/hooks.py.
Single long take (many retakes) cut to the best take of each line,
with Jack's real screen recordings, generated images and before/after results on paper pages. No music bed.
Generates index.html from edit/words.json (cut), edit/tokens.json (captions), edit/broll.json and face samples.
Run from the project root:  python3 -I edit/build.py
"""
import html
import json
import math
import os
import re

TOK = json.load(open("edit/tokens.json"))
SEGS = json.load(open("edit/words.json"))["segments"]
BROLL = json.load(open("edit/broll.json"))
AROLL_END = SEGS[-1]["end"]
HOOK = os.environ.get("HOOK", "")
FULL = bool(os.environ.get("FULL"))  # with HOOK: build the whole video with that hook instead of just the hook  # 1..5 builds a hook experiment (0 s to "Hello") instead of the full video
DURATION = round(AROLL_END + 3.0, 3)

INK, PAPER, RED, MUTED = "#17120e", "#ede7df", "#17120e", "#7a6e63"
GRADE = ""  # never grade his footage


def t(i):
    return TOK[i]["start"]


CUTS = [g["start"] for g in SEGS[1:]]


def cover_cut(e):
    """A page that ends just before a take change would flash the old take: hold it over the cut instead."""
    for c in CUTS:
        if e - 0.25 < c <= e + 0.4:
            print(f"  page end {e:.2f} -> {c + 0.3:.2f} (covers the cut at {c:.2f})")
            return c + 0.3
    return e


def esc(s):
    return html.escape(s, quote=True)


scenes, js, sfx = [], [], []
CUR = '<svg viewBox="0 0 24 24"><path d="M5 3 L5 19 L9 15 L12 22 L15 20.5 L11.5 14 L18 14 Z" fill="#fff" stroke="#141414" stroke-width="1.4" stroke-linejoin="round"/></svg>'


def scene(sid, start, end, body, whoosh=True):
    for c in CUTS:  # a page that lands just after a take change would flash the new take: start on the cut
        if c <= start < c + 0.4:
            print(f"  page {sid} start {start:.2f} -> {c - 0.02:.2f} (cut at {c:.2f})")
            start = c - 0.02
    start = math.floor(start * 30 + 1e-6) / 30 - 0.002  # land on a frame, never one frame late
    scenes.append((sid, start, end, body))
    js.append(f"enter('#{sid}', {start:.3f});")
    if whoosh:
        sfx.append(("fast-whoosh", max(0, start - 0.32), 0.34))
    return start


def rev(sel, at, **o):
    js.append(f"rev('{sel}', {at:.3f}, {json.dumps(o)});")


def words_in(sel_prefix, words, idxs):
    """Lead-in words that appear one by one with his voice."""
    spans = " ".join(f'<span class="ch" id="{sel_prefix}{k}">{w}</span>' for k, w in enumerate(words))
    for k, i in enumerate(idxs):
        js.append(f"tl.fromTo('#{sel_prefix}{k}', {{opacity:0, y:14, filter:'blur(10px)'}}, {{opacity:1, y:0, filter:'blur(0px)', duration:.25, ease:'power2.out'}}, {t(i) - 0.05:.3f});")
    return spans


def slam(sel, at, s=1.5):
    js.append(f"tl.fromTo('{sel}', {{opacity:0, scale:{s}, filter:'blur(18px)'}}, {{opacity:1, scale:1, filter:'blur(0px)', duration:.4, ease:'expo.out'}}, {at:.3f});")


def vid(vid_id, src, start, dur, style="", cls="pv"):
    return f'<video id="{vid_id}" class="clip {cls}" src="{src}" data-start="{start:.3f}" data-duration="{dur:.3f}" data-track-index="5" muted playsinline style="{style}"></video>'


VL = []  # page videos live in their own layer above the pages (a timed <video> can't be nested in a timed page)


def overlay(html_, start, end, adjacent=False, sel=None):
    """Add a positioned wrapper to the video layer; it fades in with its page and out with the page's crossfade."""
    VL.append(html_)
    if sel:
        js.append(f"tl.fromTo('{sel}', {{opacity:0}}, {{opacity:1, duration:.3, ease:'power2.out'}}, {start + 0.08:.3f});")
        if adjacent:
            js.append(f"tl.set('{sel}', {{opacity:0}}, {end:.3f});")
        else:
            js.append(f"tl.to('{sel}', {{opacity:0, duration:.42, ease:'sine.inOut', immediateRender:false}}, {end - 0.42:.3f});")


def typed_words(prefix, text):
    return " ".join(f'<span class="wd" id="{prefix}{k}">{esc(w)}</span>' for k, w in enumerate(text.split()))


def type_on(prefix, n, a, b):
    """Reveal n word spans evenly between a and b (typing rhythm)."""
    for k in range(n):
        js.append(f"tl.set('#{prefix}{k}', {{opacity:1}}, {a + (b - a) * k / max(n - 1, 1):.3f});")


SEG_W = (900 - 29 * 6) / 30
BLOCKS = "".join(f'<i class="seg" id="{{p}}-s{k}"></i>' for k in range(30))
ICON = {
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-7 8-7s8 3 8 7"/>',
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    "film": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 4v16M17 4v16M3 9h4M3 15h4M17 9h4M17 15h4"/>',
    "play": '<path d="M7 5l11 7-11 7z"/><path d="M20 2v4M18 4h4"/>',
    "send": '<path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4z"/>',
    "cal": '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M8 3v4M16 3v4M3 10h18"/>',
}
LOGOS = ["tiktok.svg", "instagram.svg", "youtube.svg", "x.svg", "facebook.svg"]
CREATORS = ["story", "lola", "ant", "lucas", "roos"]

if HOOK in ("", "0"):  # 0 = the original hook
    # ---------------------------------------------------------------- P1 hook: "five viral AI creator accounts" — his five real creators fan out
    s, e = t(3) - 0.06, cover_cut(t(7) - 0.06)
    FAN = [(215, -11, 420), (378, -5.5, 385), (540, 0, 365), (702, 5.5, 385), (865, 11, 420)]
    order = [0, 4, 1, 3, 2]
    HOOKV = [1, 0, 4, 3, 2]  # left to right: fighters, walkout, VOLT (centre), Lucas, knight
    fan = ""
    s = scene("p1", s, e, f"""
      {fan}
      <div class="stack" style="left:0;right:0;top:930px">
        <span id="p1-n" class="xb" style="font-size:210px;line-height:1">5</span>
        <span class="sm" style="font-size:64px;margin-top:8px">{words_in('p1w', ['viral', 'AI', 'creator', 'accounts'], [3, 4, 5, 6])}</span>
      </div>""")
    VL.append("".join(f'<div class="fan" id="p1-c{k}" style="left:{cx - 130}px;top:{y}px;width:260px;height:462px;z-index:{[1, 2, 3, 2, 1][k]}">{vid(f"p1-v{k}", f"assets/video/br/hook{HOOKV[k]}.mp4", s, e - s)}</div>' for k, (cx, r, y) in enumerate(FAN)))
    js.append(f"tl.to('#vlayer .fan', {{opacity:0, duration:.42, ease:'sine.inOut', immediateRender:false}}, {e - 0.42:.3f});")
    for j, k in enumerate(order):
        cx, r, y = FAN[k]
        js.append(f"tl.fromTo('#p1-c{k}', {{opacity:0, y:320, rotation:0, scale:.6}}, {{opacity:1, y:0, rotation:{r}, scale:1, duration:.5, ease:'back.out(1.4)'}}, {s + 0.02 + j * 0.07:.3f});")
    slam("#p1-n", s + 0.08)
    sfx += [("hard-pop-click", s + 0.06, 0.3), ("pluck_001", s + 0.3, 0.2)]

else:
    exec(open("edit/hooks.py").read())

# ---------------------------------------------------------------- P2 "This is day three of 30" — stat page, today's block emphasised
s, e = t(22) - 0.06, cover_cut(t(28) + 0.36)
scene("p2", s, e, f"""
  <div class="stack" style="left:0;right:0;top:600px">
    <span class="sm" style="font-size:56px">{words_in('p2w', ['this', 'is'], [22, 23])}</span>
    <div class="row" style="align-items:flex-end;justify-content:center;margin-top:10px">
      <span id="p2-day" class="xb" style="font-size:230px;line-height:1">Day</span>
      <span id="p2-n" class="xb" style="font-size:230px;line-height:1;margin-left:40px">3</span>
    </div>
    <span class="sm" style="font-size:56px;margin-top:22px">{words_in('p2o', ['of', '30'], [26, 27])}</span>
  </div>
  <div id="p2-bar" class="bar big" style="top:1250px">{BLOCKS.replace('{p}', 'p2')}</div>""")
js.append(f"tl.fromTo('#p2-day', {{opacity:0, y:60, filter:'blur(14px)'}}, {{opacity:1, y:0, filter:'blur(0px)', duration:.4, ease:'expo.out'}}, {t(24) - 0.05:.3f});")
slam("#p2-n", t(25) - 0.05)
js.append(f"tl.fromTo('#p2-bar .seg', {{scaleY:0, opacity:0}}, {{scaleY:1, opacity:1, duration:.22, stagger:.01, ease:'power2.out'}}, {t(25):.3f});")
js.append(f"tl.fromTo('#p2-s0, #p2-s1', {{backgroundColor:'rgba(23,18,14,.14)'}}, {{backgroundColor:'{INK}', duration:.15, stagger:.06}}, {t(25) + 0.25:.3f});")
js.append(f"tl.fromTo('#p2-s2', {{backgroundColor:'rgba(23,18,14,.14)', scaleY:1}}, {{backgroundColor:'{INK}', scaleY:1.9, duration:.45, ease:'back.out(2.2)'}}, {t(27):.3f});")
sfx += [("dry-pop-alert", t(25), 0.24), ("pluck_001", t(27), 0.26)]

# ---------------------------------------------------------------- P3 "making your own AI creator from start to finish" — the road map
s, e = t(44) - 0.06, cover_cut(t(55) + 0.1)
NODES = [("user", "character"), ("grid", "image sheet"), ("film", "clip"), ("play", "AI video"), ("send", "posted")]
nodes = "".join(f'<div class="node" id="p3-n{k}" style="left:{140 + 200 * k - 85}px;top:1010px"><div class="nd"><svg viewBox="0 0 24 24">{ICON[ic]}</svg></div><span>{lab}</span></div>' for k, (ic, lab) in enumerate(NODES))
scene("p3", s, e, f"""
  <div class="stack" style="left:0;right:0;top:600px">
    <span class="sm" style="font-size:56px">{words_in('p3w', ['making', 'your', 'own'], [44, 45, 46])}</span>
    <span id="p3-t" class="xb" style="font-size:120px;line-height:1.05;margin-top:6px">AI creator</span>
  </div>
  <svg class="road" viewBox="0 0 1080 1920" style="left:0;top:0;width:1080px;height:1920px">{"".join(f'<path class="p3-seg" id="p3-r{k}" d="M{140 + 200 * k + 62} 1072 L{340 + 200 * k - 62} 1072" style="stroke-dasharray:76"/>' for k in range(4))}</svg>
  {nodes}
  <span id="p3-st" class="note dim" style="position:absolute;left:92px;top:950px">start</span>
  <span id="p3-fi" class="note dim" style="position:absolute;left:885px;top:950px">finish</span>""")
rev("#p3-t", t(47) - 0.05, y=26)
NT = [t(48) + k * (t(52) - t(48)) / 4 for k in range(5)]
for k in range(4):
    js.append(f"tl.fromTo('#p3-r{k}', {{strokeDashoffset:76}}, {{strokeDashoffset:0, duration:{NT[k + 1] - NT[k] - 0.12:.3f}, ease:'power1.inOut'}}, {NT[k] + 0.12:.3f});")
for k in range(5):
    js.append(f"tl.fromTo('#p3-n{k}', {{opacity:0, y:40, scale:.7}}, {{opacity:1, y:0, scale:1, duration:.35, ease:'back.out(2)'}}, {t(48) + k * (t(52) - t(48)) / 4:.3f});")
    sfx.append(("tick_002", t(48) + k * (t(52) - t(48)) / 4, 0.16))
rev("#p3-st", t(48) - 0.1, y=10)
rev("#p3-fi", t(52) - 0.05, y=10)

# ---------------------------------------------------------------- P4 "Claude does all the heavy lifting" — animated logo
s, e = t(59) - 0.06, cover_cut(t(65) + 0.05)
rays = "".join(f'<i class="ray" style="left:537px;top:{560 - 54 - 150}px;transform:rotate({k * 30}deg);transform-origin:50% {150 + 54}px"></i>' for k in range(12))
scene("p4", s, e, f"""
  <i class="ringo" id="p4-r0" style="left:390px;top:410px;width:300px;height:300px"></i>
  <i class="ringo" id="p4-r1" style="left:390px;top:410px;width:300px;height:300px"></i>
  <div id="p4-rays">{rays}</div>
  <img id="p4-logo" src="assets/img/claude-mark.svg" style="position:absolute;left:420px;top:440px;width:240px;height:240px"/>
  <div class="stack" style="left:0;right:0;top:800px">
    <span id="p4-cl" class="xb" style="font-size:120px;line-height:1.05">Claude</span>
    <span class="sm" style="font-size:56px;margin-top:10px">{words_in('p4w', ['does', 'all', 'the'], [60, 61, 62])}</span>
    <span id="p4-h" class="xb" style="font-size:132px;line-height:1.05;margin-top:6px">heavy lifting</span>
  </div>""")
js.append(f"tl.fromTo('#p4-logo', {{opacity:0, scale:.2, rotation:-200}}, {{opacity:1, scale:1, rotation:0, duration:.7, ease:'back.out(1.6)'}}, {s + 0.02:.3f});")
js.append(f"tl.fromTo('#p4-logo', {{rotation:0}}, {{rotation:90, duration:{e - s - 0.7:.3f}, ease:'none', immediateRender:false}}, {s + 0.72:.3f});")
js.append(f"tl.fromTo('#p4-r0, #p4-r1', {{opacity:.7, scale:.6}}, {{opacity:0, scale:2.3, duration:1.0, stagger:.35, ease:'power2.out'}}, {s + 0.25:.3f});")
js.append(f"tl.fromTo('#p4-rays .ray', {{opacity:0, scaleY:0}}, {{opacity:1, scaleY:1, duration:.3, stagger:.02, ease:'power3.out'}}, {s + 0.35:.3f}); tl.to('#p4-rays .ray', {{opacity:0, duration:.3, immediateRender:false}}, {s + 0.9:.3f});")
rev("#p4-cl", t(59) - 0.04, y=26)
js.append(f"tl.fromTo('#p4-h', {{opacity:0, y:-90}}, {{opacity:1, y:0, duration:.55, ease:'bounce.out'}}, {t(63) - 0.08:.3f});")
sfx += [("hard-pop-click", s + 0.05, 0.32), ("boom", t(63) + 0.3, 0.18)]

# ---------------------------------------------------------------- P4b "...how I bang out multiple videos a day" — six real posts pop up
s, e = t(72) - 0.1, cover_cut(t(76) - 0.06)
s = scene("p4b", s, e, f"""
  <div class="stack" style="left:0;right:0;top:250px">
    <div class="row" style="align-items:baseline;gap:20px"><span id="p4b-m" class="xb" style="font-size:104px">multiple</span><span class="sm" style="font-size:56px">{words_in('p4bw', ['videos', 'a', 'day'], [73, 74, 75])}</span></div>
  </div>""")
GV = ["hook0", "hook1", "hook2", "hook3", "hook4", "ai-track"]
POS = [(80, 430, -5), (400, 400, 2), (720, 430, 6), (80, 960, 4), (400, 930, -3), (720, 960, -6)]
tiles = "".join(f'<div class="fan" id="p4b-c{k}" style="left:{x}px;top:{y}px;width:280px;height:498px;transform:rotate({r}deg)">{vid(f"p4b-v{k}", f"assets/video/br/{GV[k]}.mp4", s, e - s + 0.4)}</div>' for k, (x, y, r) in enumerate(POS))
overlay(f'<div id="o4b" style="position:absolute;inset:0">{tiles}</div>', s, e, sel="#o4b")
slam("#p4b-m", t(72) - 0.05, 1.4)
for j, k in enumerate([1, 3, 5, 0, 4, 2]):
    at = t(72) + 0.05 + j * 0.13
    js.append(f"tl.fromTo('#p4b-c{k}', {{opacity:0, scale:.3, y:80}}, {{opacity:1, scale:1, y:0, duration:.35, ease:'back.out(2.2)'}}, {at:.3f});")
    sfx.append(("pluck_001" if j % 2 else "hard-pop-click", at, 0.18))

# ---------------------------------------------------------------- P5 step 1: "tell Claude who your character is, their look, their vibe, what they post about"
PROMPT1 = "Hey, create me a new AI social media character. Funky hair. Crazy teeth. Crazy outfit. Funny vibe. Realistic. Human. Make me an image sheet with 10 different characters."
W1 = PROMPT1.split()
HIT = {"look": [9, 10, 11, 12, 13, 14], "vibe": [15, 16], "post": [6, 7, 8]}
s, e = t(85) - 0.06, (t(100) - 0.06)  # hands straight to the next page
scene("p5", s, e, f"""
  <div class="stack" style="left:0;right:0;top:310px">
    <span id="p5-st" class="note dim">step 1</span>
    <div class="row" style="align-items:center;gap:22px;margin-top:8px"><span class="sm" style="font-size:56px">tell</span><img id="p5-logo" src="assets/img/claude-mark.svg" style="width:96px;height:96px"/><span id="p5-cl" class="xb" style="font-size:110px">Claude</span></div>
  </div>
  <div id="p5-win" class="win" style="top:600px">
    <div class="bar-top"><i></i><i></i><i></i><span class="wt">Claude</span></div>
    <div class="pbody"><div class="pt">{typed_words('p5t', PROMPT1)}</div></div>
    <div class="wfoot"><span class="note dim">connected · Higgsfield</span><span id="p5-send" class="wsend">&#8593;</span></div>
  </div>
  <div class="tk-row" style="top:1290px"><span class="tk" id="p5-k0"><b>&#10003;</b>look</span><span class="tk" id="p5-k1"><b>&#10003;</b>vibe</span><span class="tk" id="p5-k2"><b>&#10003;</b>what they post</span></div>""")
rev("#p5-st", s + 0.03, y=10)
js.append(f"tl.fromTo('#p5-logo', {{opacity:0, scale:.3, rotation:-160}}, {{opacity:1, scale:1, rotation:0, duration:.55, ease:'back.out(1.8)'}}, {t(87) - 0.1:.3f});")
rev("#p5-cl", t(87) - 0.02, y=24)
js.append(f"tl.fromTo('#p5-win', {{opacity:0, y:80, scale:.96}}, {{opacity:1, y:0, scale:1, duration:.45, ease:'power3.out'}}, {s + 0.08:.3f});")
type_on("p5t", len(W1), s + 0.45, t(99) - 0.2)
for k, (key, wi) in enumerate((("look", 93), ("vibe", 95), ("post", 98))):
    sel = ", ".join(f"#p5t{i}" for i in HIT[key])
    js.append(f"tl.to('{sel}', {{backgroundColor:'rgba(23,18,14,.1)', duration:.25, immediateRender:false}}, {t(wi) - 0.05:.3f});")
    js.append(f"tl.fromTo('#p5-k{k}', {{opacity:0, y:30, scale:.8}}, {{opacity:1, y:0, scale:1, duration:.35, ease:'back.out(2)'}}, {t(wi) - 0.05:.3f});")
    js.append(f"tl.to('#p5-k{k} b', {{backgroundColor:'{INK}', duration:.2, immediateRender:false}}, {t(wi) + 0.15:.3f});")
    sfx.append(("tick_002", t(wi), 0.22))
js.append(f"tl.fromTo('#p5-send', {{backgroundColor:'rgba(23,18,14,.12)', color:'{MUTED}'}}, {{backgroundColor:'{INK}', color:'#fbf9f5', duration:.2}}, {e - 0.45:.3f});")
sfx += [("maximize_006", s + 0.08, 0.26), ("click_002", e - 0.45, 0.35)]
for k in range(0, len(W1), 3):
    sfx.append(("click_004", s + 0.45 + (t(99) - 0.65 - s) * k / len(W1), 0.08))

# ---------------------------------------------------------------- P6 "I've connected Claude to Higgsfield, so it makes my images right there" — real screen recording
s, e = t(100) - 0.06, cover_cut(t(113) - 0.06)
s = scene("p6", s, e, f"""
  <img id="p6-cl" src="assets/img/claude-mark.svg" style="position:absolute;left:300px;top:250px;width:110px;height:110px"/>
  <svg class="road" viewBox="0 0 1080 1920" style="left:0;top:0;width:1080px;height:1920px"><path id="p6-line" d="M425 305 L655 305" style="stroke-dasharray:230"/></svg>
  <i class="pk" id="p6-pk" style="left:440px;top:305px"></i>
  <img id="p6-hf" src="assets/img/logos/higgsfield.png" style="position:absolute;left:670px;top:250px;width:110px;height:110px;border-radius:26px"/>
  <i class="ringo" id="p6-g0" style="left:645px;top:225px;width:160px;height:160px;opacity:0"></i>
  <i class="ringo" id="p6-g1" style="left:645px;top:225px;width:160px;height:160px;opacity:0"></i>
  <span id="p6-ok" class="tk" style="position:absolute;left:400px;top:150px;font-size:30px;padding:10px 22px 10px 12px"><b style="background:#2fae5b;color:#fff">&#10003;</b>connected</span>
  <span id="p6-l1" class="note dim" style="position:absolute;left:300px;top:378px;width:110px;text-align:center">Claude</span>
  <span id="p6-l2" class="note dim" style="position:absolute;left:640px;top:378px;width:170px;text-align:center">Higgsfield</span>
  <div id="p6-win" class="win" style="top:470px">
    <div class="bar-top"><i></i><i></i><i></i><span class="wt">Claude · Higgsfield generate_image</span></div>
    <div class="gv" style="height:705px;background:#fbf9f5"></div>
  </div>""")
overlay(f'<div id="o6" style="position:absolute;left:70px;top:554px;width:940px;height:705px;border-radius:0 0 30px 30px;overflow:hidden">{vid("p6-v", "assets/video/br/gridland.mp4", s, e - s, style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover", cls="")}</div>', s, e, sel="#o6")
js.append(f"tl.fromTo('#p6-cl, #p6-hf', {{opacity:0, scale:.4}}, {{opacity:1, scale:1, duration:.45, stagger:.12, ease:'back.out(2)'}}, {s + 0.02:.3f});")
js.append(f"tl.fromTo('#p6-l1, #p6-l2', {{opacity:0}}, {{opacity:1, duration:.3}}, {s + 0.3:.3f});")
c0, c1 = t(102) - 0.05, t(105) + 0.05
js.append(f"tl.fromTo('#p6-line', {{strokeDashoffset:230}}, {{strokeDashoffset:0, duration:{c1 - c0:.3f}, ease:'sine.inOut'}}, {c0:.3f});")
js.append(f"tl.fromTo('#p6-pk', {{x:-15, opacity:0}}, {{x:215, opacity:1, duration:{c1 - c0:.3f}, ease:'sine.inOut'}}, {c0:.3f}); tl.to('#p6-pk', {{opacity:0, scale:2, duration:.2, immediateRender:false}}, {c1:.3f});")
js.append(f"tl.to('#p6-hf', {{scale:1.25, duration:.14, yoyo:true, repeat:1, ease:'power2.out', immediateRender:false}}, {c1:.3f});")
js.append(f"tl.fromTo('#p6-g0, #p6-g1', {{opacity:.8, scale:.6}}, {{opacity:0, scale:2.4, duration:.8, stagger:.18, ease:'power2.out'}}, {c1:.3f});")
js.append(f"tl.fromTo('#p6-ok', {{opacity:0, y:20, scale:.6}}, {{opacity:1, y:0, scale:1, duration:.35, ease:'back.out(2.4)'}}, {c1 + 0.1:.3f});")
sfx += [("confirmation_002", c1, 0.3)]
js.append(f"tl.fromTo('#p6-win, #o6', {{y:80}}, {{y:0, duration:.45, ease:'power3.out'}}, {s + 0.1:.3f});")
sfx += [("pluck_001", t(102), 0.24), ("explainer-light-pop-whoosh", s + 1.6, 0.24)]

# ---------------------------------------------------------------- P7 "follow this prompt, and then you've got your image sheet" — grid → prompt → Bev's sheet
SHEET_PROMPT = [
    "Create a 16:9 character reference sheet of the 2nd character on the top row. Clean, grey, neutral background with five panels:",
    "• Three full-body shots (front, back and side profile), each cropped at the shoulders so no neck or face is visible.",
    "• Two face close-ups, one with a happy expression and one with a neutral expression. These are the only panels that show the face.",
    "Keep the outfit, body proportions, scale and lighting the same in every panel. Use even studio lighting.",
]
s, e = t(123) - 0.06, cover_cut(t(140) + 0.1)
lines7 = "".join(f'<div class="pl" id="p7-l{k}" style="font-size:26px;line-height:1.3">{esc(ln)}</div>' for k, ln in enumerate(SHEET_PROMPT))
scene("p7", s, e, f"""
  <div id="p7-card" class="c16" style="top:150px">
    <img src="assets/img/grid10.jpg"/>
    <div class="ov"><i class="hl" id="p7-ring" style="left:182px;top:-6px;width:200px;height:276px"></i></div>
  </div>
  <span id="p7-tag" class="mtag" style="left:180px;top:86px;font-size:36px">your character</span>
  <div id="p7-win" class="win" style="top:720px">
    <div class="bar-top"><i></i><i></i><i></i><span class="wt">the image-sheet prompt</span></div>
    <div class="pbody" style="gap:10px;padding:26px 42px 30px">{lines7}</div>
  </div>
  <div id="p7-out" class="c16" style="left:150px;right:150px;top:1290px"><img src="assets/img/bev-sheet.jpg"/></div>
  <span id="p7-tag2" class="mtag" style="left:150px;top:1236px;font-size:32px;background:#fbf9f5;color:{INK}">image sheet</span>""")
js.append(f"tl.fromTo('#p7-card', {{opacity:0, y:-40, scale:.95}}, {{opacity:1, y:0, scale:1, duration:.4, ease:'power3.out'}}, {s + 0.03:.3f});")
js.append(f"tl.fromTo('#p7-ring', {{opacity:0, scale:1.3}}, {{opacity:1, scale:1, duration:.35, ease:'power3.out'}}, {s + 0.3:.3f});")
js.append(f"tl.fromTo('#p7-tag', {{opacity:0, scale:.6}}, {{opacity:1, scale:1, duration:.35, ease:'back.out(2.4)'}}, {s + 0.45:.3f});")
js.append(f"tl.fromTo('#p7-win', {{opacity:0, y:120}}, {{opacity:1, y:0, duration:.45, ease:'power3.out'}}, {t(128) - 0.1:.3f});")
js.append(f"tl.fromTo('#p7-win .pl', {{opacity:0, y:14, filter:'blur(8px)'}}, {{opacity:1, y:0, filter:'blur(0px)', duration:.3, stagger:.12, ease:'power2.out'}}, {t(128) + 0.1:.3f});")
swap = t(133) - 0.1
js.append(f"tl.fromTo('#p7-out', {{opacity:0, y:60, clipPath:'inset(0% 100% 0% 0%)'}}, {{opacity:1, y:0, clipPath:'inset(0% 0% 0% 0%)', duration:.6, ease:'power2.inOut'}}, {swap:.3f});")
js.append(f"tl.fromTo('#p7-tag2', {{opacity:0, scale:.6}}, {{opacity:1, scale:1, duration:.3, ease:'back.out(2.4)'}}, {swap + 0.4:.3f});")
sfx += [("pluck_001", s + 0.3, 0.22), ("maximize_006", t(128) - 0.1, 0.24), ("arrow-whoosh", swap, 0.28)]

# ---------------------------------------------------------------- P8 "the sheet is what keeps your character looking the same in every single video"
s, e = t(159) - 0.06, (t(169) - 0.06)  # hands straight to the next page
VOLT = ["volt-1-rooftop-antennas", "volt-2-elevator-mirror", "volt-3-record-store"]
cards8 = "".join(f'<div class="tile" id="p8-v{k}" style="left:{70 + k * 326}px;top:960px;width:288px;height:512px"><img src="assets/img/creators/{n}.jpg"/></div>' for k, n in enumerate(VOLT))
checks8 = "".join(f'<span class="tk" id="p8-c{k}" style="position:absolute;left:{70 + k * 326 + 54}px;top:1500px;font-size:30px;padding:10px 22px 10px 12px"><b>&#10003;</b>same</span>' for k in range(3))
web8 = "".join(f'<path id="p8-w{k}" d="M540 800 C 540 880, {214 + k * 326} 880, {214 + k * 326} 960"/>' for k in range(3))
scene("p8", s, e, f"""
  <div class="stack" style="left:0;right:0;top:210px">
    <div class="row" style="align-items:baseline;gap:18px"><span class="sm" style="font-size:56px">{words_in('p8w', ['looking', 'the'], [162, 163])}</span><span id="p8-same" class="xb" style="font-size:110px">same</span></div>
  </div>
  <div class="tile" id="p8-sheet" style="left:380px;top:420px;width:320px;height:320px"><img src="assets/img/volt-sheet.jpg"/></div>
  <span id="p8-tag" class="mtag" style="left:330px;top:390px;font-size:32px">one sheet</span>
  <svg class="web">{web8}</svg>
  {cards8}{checks8}""")
js.append(f"tl.fromTo('#p8-sheet', {{opacity:0, scale:.7}}, {{opacity:1, scale:1, duration:.4, ease:'back.out(1.8)'}}, {s + 0.04:.3f});")
js.append(f"tl.fromTo('#p8-tag', {{opacity:0, scale:.6}}, {{opacity:1, scale:1, duration:.3, ease:'back.out(2.4)'}}, {s + 0.25:.3f});")
slam("#p8-same", t(164) - 0.05, 1.4)
js.append(f"tl.fromTo('#p8 .web path', {{strokeDashoffset:1400}}, {{strokeDashoffset:0, duration:.45, stagger:.08, ease:'power2.out'}}, {t(162) - 0.1:.3f});")
for k in range(3):
    js.append(f"tl.fromTo('#p8-v{k}', {{opacity:0, y:60, scale:.85}}, {{opacity:1, y:0, scale:1, duration:.4, ease:'back.out(1.6)'}}, {t(162) + k * 0.16:.3f});")
    js.append(f"tl.fromTo('#p8-c{k}', {{opacity:0, scale:.6}}, {{opacity:1, scale:1, duration:.3, ease:'back.out(2.4)'}}, {t(166 + k) - 0.05:.3f});")
    js.append(f"tl.to('#p8-c{k} b', {{backgroundColor:'{INK}', duration:.15, immediateRender:false}}, {t(166 + k) + 0.1:.3f});")
    sfx.append(("tick_002", t(166 + k), 0.2))
sfx += [("pluck_001", s + 0.05, 0.22), ("dry-pop-alert", t(164), 0.22)]

# ---------------------------------------------------------------- P9 "the reason we cut the face off in the body shots"
s, e = t(169) - 0.06, cover_cut(t(184) - 0.06)
CW, CH = 940, 529
scene("p9", s, e, f"""
  <div class="stack" style="left:0;right:0;top:300px">
    <span class="sm" style="font-size:52px">{words_in('p9w', ['the', 'reason', 'we'], [169, 170, 171])}</span>
    <span id="p9-t" class="xb" style="font-size:100px;line-height:1.05;margin-top:6px">cut the face off</span>
  </div>
  <div id="p9-card" class="c16" style="top:600px">
    <img src="assets/img/bev-sheet.jpg"/>
    <div class="ov">
      <i class="hl" id="p9-body" style="left:-6px;top:-6px;width:{int(CW * 0.705) + 12}px;height:{CH + 12}px;border-radius:30px"></i>
      <i class="cropl" id="p9-crop" style="left:0;top:6px;width:{int(CW * 0.705)}px"></i>
    </div>
  </div>
  <span id="p9-a" class="mtag" style="left:190px;top:1150px;font-size:34px">body shots · no face</span>
  <span id="p9-b" class="mtag" style="left:690px;top:1150px;font-size:34px;background:#fbf9f5;color:{INK}">face · close-ups</span>""")
rev("#p9-t", t(172) - 0.05, y=26)
js.append(f"tl.fromTo('#p9-card', {{opacity:0, y:60, scale:.95}}, {{opacity:1, y:0, scale:1, duration:.45, ease:'power3.out'}}, {s + 0.05:.3f});")
js.append(f"tl.fromTo('#p9-crop', {{scaleX:0, transformOrigin:'0% 50%'}}, {{scaleX:1, duration:.5, ease:'power2.inOut'}}, {t(172):.3f});")
js.append(f"tl.fromTo('#p9-body', {{opacity:0}}, {{opacity:1, duration:.3}}, {t(178) - 0.1:.3f});")
js.append(f"tl.fromTo('#p9-a', {{opacity:0, y:20}}, {{opacity:1, y:0, duration:.3, ease:'back.out(2)'}}, {t(178) - 0.05:.3f});")
js.append(f"tl.fromTo('#p9-b', {{opacity:0, y:20}}, {{opacity:1, y:0, duration:.3, ease:'back.out(2)'}}, {t(179) + 0.15:.3f});")
sfx += [("scribble", t(172), 0.26), ("tick_002", t(178), 0.22), ("tick_002", t(180), 0.2)]

# ---------------------------------------------------------------- P9b "it's not gonna hallucinate between different faces" — the face won't hold still
s, e = t(190) - 0.06, cover_cut(t(197) - 0.06)
FACES = [f"f{k}" for k in range(10)] + ["bev"]
faces = "".join(f'<img id="p9b-f{n}" src="assets/img/faces/{n}.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:{1 if n == "bev" else 0}"/>' for n in FACES)
s = scene("p9b", s, e, f"""
  <div class="stack" style="left:0;right:0;top:250px">
    <span class="sm" style="font-size:56px">{words_in('p9bw', ["it's", 'not', 'gonna'], [190, 191, 192])}</span>
    <div style="position:relative;margin-top:6px">
      <span id="p9b-g1" class="xb" style="position:absolute;left:0;top:0;font-size:112px;line-height:1.05;opacity:0;color:rgba(23,18,14,.28)">hallucinate</span>
      <span id="p9b-g2" class="xb" style="position:absolute;left:0;top:0;font-size:112px;line-height:1.05;opacity:0;color:rgba(23,18,14,.18)">hallucinate</span>
      <span id="p9b-t" class="xb" style="position:relative;font-size:112px;line-height:1.05">hallucinate</span>
    </div>
  </div>
  <div id="p9b-card" class="tile" style="left:270px;top:560px;width:540px;height:540px;border-radius:40px">{faces}</div>
  <span id="p9b-q" class="mtag" style="left:620px;top:520px;font-size:40px">which face?</span>
  <div class="stack" style="left:0;right:0;top:1170px"><span class="sm" style="font-size:56px">{words_in('p9bw2', ['between', 'different', 'faces'], [194, 195, 196])}</span></div>""")
js.append(f"tl.fromTo('#p9b-card', {{opacity:0, scale:.85}}, {{opacity:1, scale:1, duration:.4, ease:'back.out(1.6)'}}, {s + 0.05:.3f});")
slam("#p9b-t", t(193) - 0.06, 1.3)
g0, g1 = t(193) - 0.02, t(196) + 0.35
order9 = [0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 6, 3, 9, 5, 2, 8, 4, 1, 7]
step = (g1 - g0) / len(order9)
prev = "bev"
for k, n in enumerate(order9):
    at = g0 + k * step
    jx, jr = [(-14, -3), (12, 2.5), (-8, 1.5), (16, -2), (-12, 3), (9, -1.5)][k % 6]
    js.append(f"tl.set('#p9b-f{prev}', {{opacity:.35, x:{-jx}}}, {at:.3f}); tl.set('#p9b-ff{k}', {{}}, {at:.3f});" if False else f"tl.set('#p9b-f{prev}', {{opacity:.3, x:{-jx}}}, {at:.3f});")
    js.append(f"tl.set('#p9b-ff', {{}}, {at:.3f});" if False else f"tl.set('#p9b-f{FACES[n]}', {{opacity:1, x:0}}, {at:.3f});")
    js.append(f"tl.set('#p9b-card', {{x:{jx}, rotation:{jr}}}, {at:.3f});")
    js.append(f"tl.set('#p9b-g1', {{opacity:1, x:{jx * 0.8:.0f}}}, {at:.3f}); tl.set('#p9b-g2', {{opacity:1, x:{-jx * 0.6:.0f}}}, {at:.3f});")
    if k >= 1:
        old = FACES[order9[k - 2]] if k >= 2 else "bev"
        js.append(f"tl.set('#p9b-f{old}', {{opacity:0, x:0}}, {at:.3f});")
    prev = FACES[n]
js.append(f"tl.set('#p9b-card', {{x:0, rotation:0}}, {g1:.3f}); tl.set('#p9b-g1, #p9b-g2', {{opacity:0, x:0}}, {g1:.3f});")
js.append(f"tl.fromTo('#p9b-q', {{opacity:0, scale:.6, rotation:-10}}, {{opacity:1, scale:1, rotation:4, duration:.35, ease:'back.out(2.4)'}}, {t(194) - 0.05:.3f});")
sfx += [("glitch_002", g0, 0.26), ("glitch_004", t(195), 0.22)]

# ---------------------------------------------------------------- P10 step 3: "find your clip — a dance, a walk, a reaction video"
def step_head(pid, n, title_html, top=200):
    """Approved step header: small 'step', big number, title — all centred, the title row complete from the start."""
    return f"""  <div class="stack" style="left:0;right:0;top:{top}px">
    <span id="{pid}-st" class="sm" style="font-size:56px">step</span>
    <span id="{pid}-n" class="xb" style="font-size:210px;line-height:.95">{n}</span>
    <div id="{pid}-t" class="row" style="align-items:center;justify-content:center;gap:20px;margin-top:6px">{title_html}</div>
  </div>"""


s, e = t(205) - 0.06, cover_cut(t(229) - 0.06)
s = scene("p10", s, e, step_head("p10", 3, '<span class="xb" style="font-size:88px;line-height:1.05">find your clip</span>') + f"""
  <div class="phn" id="p10-ph" style="left:355px;top:640px;width:370px;height:658px"></div>
  <div class="tk-row" style="top:1360px"><span class="tk" id="p10-k0"><b>&#10003;</b>dance</span><span class="tk" id="p10-k1"><b>&#10003;</b>walk</span><span class="tk" id="p10-k2"><b>&#10003;</b>reaction</span></div>""")
overlay(f'<div id="o10" style="position:absolute;left:355px;top:640px;width:370px;height:658px;border-radius:48px;overflow:hidden">{vid("p10-v", "assets/video/br/src-track.mp4", s, e - s)}</div>', s, e, sel=None)
js.append(f"tl.fromTo('#o10', {{opacity:0}}, {{opacity:1, duration:.2}}, {s + 0.1:.3f}); tl.to('#o10', {{opacity:0, duration:.42, ease:'sine.inOut', immediateRender:false}}, {e - 0.42:.3f});")
rev("#p10-st", s + 0.03, y=10)
slam("#p10-n", t(205) - 0.05)
rev("#p10-t", t(208) - 0.05, y=24)
js.append(f"tl.fromTo('#p10-ph, #o10', {{y:120, rotation:6}}, {{y:0, rotation:0, duration:.5, ease:'power3.out'}}, {s + 0.1:.3f});")
js.append(f"tl.fromTo('#p10-ph', {{opacity:0}}, {{opacity:1, duration:.3}}, {s + 0.1:.3f});")
for k, wi in enumerate((217, 222, 227)):
    js.append(f"tl.fromTo('#p10-k{k}', {{opacity:0, y:30, scale:.8}}, {{opacity:1, y:0, scale:1, duration:.32, ease:'back.out(2)'}}, {t(wi) - 0.08:.3f});")
    js.append(f"tl.to('#p10-k{k} b', {{backgroundColor:'{INK}', duration:.15, immediateRender:false}}, {t(wi) + 0.08:.3f});")
    sfx.append(("tick_002", t(wi), 0.22))
sfx += [("dry-pop-alert", t(205), 0.24)]

# ---------------------------------------------------------------- P11 step 4: a cursor drags the clip, then the character sheet, onto Claude's prompt box
PROMPT3 = "Use Higgsfield Genjutsu Lite and replace the main character in the source video with my character."
W3 = PROMPT3.split()
s, e = t(234) - 0.06, cover_cut(t(259) + 0.25)
FILES = [("dance.mp4", "assets/img/src-thumb.jpg", 300), ("character-sheet.png", "assets/img/volt-sheet.jpg", 780)]
files = "".join(f'<div class="fcard" id="p11-f{k}" style="left:{cx - 105}px;top:640px"><img src="{img}"/><span>{name}</span></div>' for k, (name, img, cx) in enumerate(FILES))
scene("p11", s, e, step_head("p11", 4, '<span class="sm" style="font-size:52px">drop it into</span><img src="assets/img/claude-mark.svg" style="width:84px;height:84px"/><span class="xb" style="font-size:96px">Claude</span>') + f"""
  {files}
  <div id="p11-win" class="win" style="top:1000px">
    <i id="p11-drop" class="dropz"></i>
    <div class="bar-top"><i></i><i></i><i></i><span class="wt">Claude</span></div>
    <div class="atts"><div class="att2 sel2" id="p11-a0"><img src="assets/img/src-thumb.jpg"/>dance.mp4<b>&#10003;</b></div><div class="att2 sel2" id="p11-a1"><img src="assets/img/volt-sheet.jpg"/>character-sheet.png<b>&#10003;</b></div></div>
    <div class="pbody" style="padding-top:22px"><div class="pt">{typed_words('p11t', PROMPT3)}</div></div>
    <div class="wfoot"><span class="hfc" id="p11-hf"><img src="assets/img/logos/higgsfield.png"/>Higgsfield MCP</span><span id="p11-send" class="wsend">&#8593;</span></div>
  </div>
  <div id="p11-cur" class="cursor">{CUR}</div>""")
rev("#p11-st", s + 0.03, y=10)
slam("#p11-n", s + 0.06)
rev("#p11-t", s + 0.2, y=24)
js.append(f"tl.fromTo('#p11-win', {{opacity:0, y:80}}, {{opacity:1, y:0, duration:.45, ease:'power3.out'}}, {s + 0.1:.3f});")
js.append(f"tl.fromTo('#p11-f0, #p11-f1', {{opacity:0, y:40, scale:.85}}, {{opacity:1, y:0, scale:1, duration:.4, stagger:.1, ease:'back.out(1.8)'}}, {s + 0.2:.3f});")
js.append(f"tl.set('#p11-a0, #p11-a1, #p11-hf', {{opacity:0}}, {s:.3f});")
# cursor: grab the clip, drag it over the box (overshoot), drop; then the sheet. Tip offset is (14, 8).
TIP = (14, 8)
drags = [(0, t(239) - 0.15, (300, 735), (430, 1150), (400, 1120)), (1, t(244) - 0.1, (780, 735), (650, 1150), (680, 1120))]
js.append(f"tl.fromTo('#p11-cur', {{x:1100, y:1500, opacity:0}}, {{x:{300 - TIP[0]}, y:{735 - TIP[1]}, opacity:1, duration:.5, ease:'power3.out'}}, {drags[0][1] - 0.55:.3f});")
for k, at, (gx, gy), (ox, oy), (dx, dy) in drags:
    if k == 1:
        js.append(f"tl.to('#p11-cur', {{x:{gx - TIP[0]}, y:{gy - TIP[1]}, duration:.4, ease:'power2.inOut', immediateRender:false}}, {at - 0.45:.3f});")
    js.append(f"tl.to('#p11-cur', {{scale:.86, duration:.08, immediateRender:false}}, {at:.3f});")
    js.append(f"tl.to('#p11-f{k}', {{scale:1.06, boxShadow:'0 40px 70px rgba(40,26,14,.35)', duration:.12, immediateRender:false}}, {at:.3f});")
    js.append(f"tl.to('#p11-cur', {{x:{ox - TIP[0]}, y:{oy - TIP[1]}, duration:.45, ease:'power2.inOut', immediateRender:false}}, {at + 0.1:.3f});")
    js.append(f"tl.to('#p11-f{k}', {{x:{ox - gx}, y:{oy - gy}, rotation:{-6 if k == 0 else 6}, duration:.45, ease:'power2.inOut', immediateRender:false}}, {at + 0.1:.3f});")
    js.append(f"tl.fromTo('#p11-drop', {{opacity:0}}, {{opacity:1, duration:.15, immediateRender:false}}, {at + 0.35:.3f});")
    js.append(f"tl.to('#p11-cur', {{x:{dx - TIP[0]}, y:{dy - TIP[1]}, duration:.2, ease:'back.out(2)', immediateRender:false}}, {at + 0.55:.3f});")
    js.append(f"tl.to('#p11-f{k}', {{x:{dx - gx}, y:{dy - gy}, duration:.2, ease:'back.out(2)', immediateRender:false}}, {at + 0.55:.3f});")
    js.append(f"tl.to('#p11-cur', {{scale:1, duration:.08, immediateRender:false}}, {at + 0.78:.3f});")
    js.append(f"tl.to('#p11-f{k}', {{opacity:0, scale:.4, duration:.18, ease:'power2.in', immediateRender:false}}, {at + 0.78:.3f});")
    js.append(f"tl.to('#p11-drop', {{opacity:0, duration:.2, immediateRender:false}}, {at + 0.85:.3f});")
    js.append(f"tl.fromTo('#p11-a{k}', {{opacity:0, scale:.7}}, {{opacity:1, scale:1, duration:.3, ease:'back.out(2.2)', immediateRender:false}}, {at + 0.85:.3f});")
    js.append(f"tl.fromTo('#p11-a{k}', {{boxShadow:'0 0 0 0px rgba(23,18,14,0)'}}, {{boxShadow:'0 0 0 5px rgba(23,18,14,1)', duration:.25, immediateRender:false}}, {at + 1.0:.3f});")
    js.append(f"tl.fromTo('#p11-a{k} b', {{scale:0}}, {{scale:1, duration:.25, ease:'back.out(2.6)', immediateRender:false}}, {at + 1.05:.3f});")
    sfx += [("click_002", at, 0.25), ("drop_002", at + 0.8, 0.3), ("tick_002", at + 1.05, 0.2)]
js.append(f"tl.to('#p11-cur', {{x:1150, y:1700, opacity:0, duration:.4, ease:'power2.in', immediateRender:false}}, {drags[1][1] + 1.2:.3f});")
type_on("p11t", len(W3), t(249), t(257) + 0.2)
js.append(f"tl.fromTo('#p11-hf', {{opacity:0, scale:.6}}, {{opacity:1, scale:1, duration:.35, ease:'back.out(2.4)', immediateRender:false}}, {t(257) - 0.05:.3f});")
hi, ck = t(257) + 0.35, t(258) + 0.5
js.append(f"tl.fromTo('#p11-send', {{backgroundColor:'rgba(23,18,14,.12)', color:'{MUTED}', boxShadow:'0 0 0 0px rgba(23,18,14,.25)'}}, {{backgroundColor:'{INK}', color:'#fbf9f5', boxShadow:'0 0 0 14px rgba(23,18,14,.18)', duration:.3, ease:'power2.out'}}, {hi:.3f});")
js.append(f"tl.to('#p11-send', {{boxShadow:'0 0 0 4px rgba(23,18,14,.1)', duration:.35, yoyo:true, repeat:1, immediateRender:false}}, {hi + 0.3:.3f});")
js.append(f"tl.fromTo('#p11-cur', {{x:1120, y:1800, opacity:0, scale:1}}, {{x:{955 - 14}, y:{1512 - 8}, opacity:1, duration:.55, ease:'power3.out', immediateRender:false}}, {ck - 0.6:.3f});")
js.append(f"tl.to('#p11-cur', {{scale:.82, duration:.08, yoyo:true, repeat:1, immediateRender:false}}, {ck:.3f}); tl.to('#p11-send', {{scale:.88, duration:.08, yoyo:true, repeat:1, immediateRender:false}}, {ck:.3f});")
sfx += [("pluck_001", t(257), 0.26), ("tick_002", hi, 0.2), ("click_002", ck, 0.4)]
for k in range(0, len(W3), 2):
    sfx.append(("click_004", t(249) + (t(257) + 0.2 - t(249)) * k / len(W3), 0.08))

# ---------------------------------------------------------------- P12 "Genjutsu keeps the moves, the timing and the camera angle, and swaps in your character"
s, e = t(269) - 0.1, cover_cut(t(289) - 0.06)
s = scene("p12", s, e, f"""
  <div class="stack" style="left:0;right:0;top:200px">
    <div class="row" style="align-items:center;gap:26px"><img id="p12-hf" src="assets/img/logos/higgsfield.png" style="width:104px;height:104px;border-radius:26px"/><span id="p12-t" class="xb" style="font-size:112px;line-height:1.05">Genjutsu</span></div>
  </div>
  <div class="phn" id="p12-ph" style="left:310px;top:390px;width:460px;height:818px"></div>
  <div class="tk-row" style="top:1270px"><span class="tk" id="p12-k0"><b>&#10003;</b>moves</span><span class="tk" id="p12-k1"><b>&#10003;</b>timing</span><span class="tk" id="p12-k2"><b>&#10003;</b>camera angle</span></div>""")
overlay(f'''<div id="o12" style="position:absolute;left:310px;top:390px;width:460px;height:818px">
    <div style="position:absolute;inset:0;border-radius:48px;overflow:hidden">
      {vid('p12-v0', 'assets/video/br/src-track.mp4', s, e - s)}
      <div id="p12-ai" style="position:absolute;inset:0;clip-path:inset(0% 0% 100% 0%)">{vid('p12-v1', 'assets/video/br/ai-track.mp4', s, e - s)}</div>
      <i id="p12-scan" style="position:absolute;left:0;right:0;top:0;height:6px;background:#fbf9f5;box-shadow:0 0 24px #fff;opacity:0"></i>
    </div>
    <span id="p12-g0" class="mtag" style="left:-40px;top:-40px;font-size:34px">your clip</span>
    <span id="p12-g1" class="mtag" style="left:-40px;top:-40px;font-size:34px">your character</span>
  </div>''', s, e, sel=None)
js.append(f"tl.fromTo('#o12', {{opacity:0}}, {{opacity:1, duration:.25}}, {s + 0.1:.3f}); tl.to('#o12', {{opacity:0, duration:.42, ease:'sine.inOut', immediateRender:false}}, {e - 0.42:.3f});")
js.append(f"tl.fromTo('#p12-hf', {{opacity:0, scale:.3, rotation:-120}}, {{opacity:1, scale:1, rotation:0, duration:.5, ease:'back.out(1.8)'}}, {s + 0.02:.3f});")
rev("#p12-t", s + 0.08, y=24)
js.append(f"tl.fromTo('#p12-ph', {{opacity:0, y:120, scale:.94}}, {{opacity:1, y:0, scale:1, duration:.5, ease:'power3.out'}}, {s + 0.1:.3f});")
js.append(f"tl.fromTo('#o12', {{y:120, scale:.94}}, {{y:0, scale:1, duration:.5, ease:'power3.out'}}, {s + 0.1:.3f});")
js.append(f"tl.fromTo('#p12-g0', {{opacity:0, scale:.6}}, {{opacity:1, scale:1, duration:.3, ease:'back.out(2.4)'}}, {s + 0.35:.3f});")
js.append(f"tl.set('#p12-g1', {{opacity:0}}, {s:.3f});")
for k, wi in enumerate((274, 276, 279)):
    js.append(f"tl.fromTo('#p12-k{k}', {{opacity:0, y:30, scale:.8}}, {{opacity:1, y:0, scale:1, duration:.32, ease:'back.out(2)'}}, {t(wi) - 0.08:.3f});")
    js.append(f"tl.to('#p12-k{k} b', {{backgroundColor:'{INK}', duration:.15, immediateRender:false}}, {t(wi) + 0.08:.3f});")
    sfx.append(("tick_002", t(wi), 0.22))
w = t(282) - 0.1
js.append(f"tl.fromTo('#p12-ai', {{clipPath:'inset(0% 0% 100% 0%)'}}, {{clipPath:'inset(0% 0% 0% 0%)', duration:.7, ease:'power2.inOut'}}, {w:.3f});")
js.append(f"tl.fromTo('#p12-scan', {{y:0, opacity:1}}, {{y:812, opacity:1, duration:.7, ease:'power2.inOut'}}, {w:.3f}); tl.to('#p12-scan', {{opacity:0, duration:.1, immediateRender:false}}, {w + 0.7:.3f});")
js.append(f"tl.to('#p12-g0', {{opacity:0, duration:.15, immediateRender:false}}, {w:.3f}); tl.fromTo('#p12-g1', {{opacity:0, scale:.6}}, {{opacity:1, scale:1, duration:.3, ease:'back.out(2.4)', immediateRender:false}}, {w + 0.45:.3f});")
sfx += [("hard-pop-click", s + 0.04, 0.3), ("arrow-whoosh", w, 0.3), ("dry-pop-alert", w + 0.5, 0.22)]

# ---------------------------------------------------------------- P13 "It can take hours to post five videos on five accounts on five platforms"
s, e = t(312) - 0.06, t(337) - 0.06  # holds until the planner page takes over
XS = [160, 350, 540, 730, 920]
vt = "".join(f'<div class="tile" id="p13-v{k}" style="left:{x - 60}px;top:430px;width:120px;height:213px;border-radius:18px"><img src="assets/img/creators/{CREATORS[k]}.jpg"/></div>' for k, x in enumerate(XS))
av = "".join(f'<div class="av" id="p13-a{k}" style="left:{x - 60}px;top:880px"><img src="assets/img/creators/{CREATORS[(k + 2) % 5]}.jpg"/></div>' for k, x in enumerate(XS))
lg = "".join(f'<div class="lgt" id="p13-l{k}" style="left:{x - 62}px;top:1250px"><img src="assets/img/logos/{LOGOS[k]}"/></div>' for k, x in enumerate(XS))
w1 = "".join(f'<path class="p13-w1" d="M{a} 650 C {a} 770, {b} 760, {b} 880"/>' for a in XS for b in XS)
w2 = "".join(f'<path class="p13-w2" d="M{a} 1008 C {a} 1130, {b} 1120, {b} 1250"/>' for a in XS for b in XS)
overlay("".join(f'<div class="tile" id="o13-v{k}" style="left:{x - 60}px;top:430px;width:120px;height:213px;border-radius:18px;opacity:0">{vid(f"p13-vv{k}", f"assets/video/br/hook{k}.mp4", s, e - s + 0.3)}</div>' for k, x in enumerate(XS)), s, e, adjacent=False, sel=None)
js.append(f"tl.fromTo('[id^=o13-v]', {{opacity:0, y:40, scale:.7}}, {{opacity:1, y:0, scale:1, duration:.32, stagger:.06, ease:'back.out(2)'}}, {t(318) - 0.05:.3f}); tl.to('[id^=o13-v]', {{opacity:0, duration:.42, ease:'sine.inOut', immediateRender:false}}, {e - 0.42:.3f});")
scene("p13", s, e, f"""
  <div class="stack" style="left:0;right:0;top:200px">
    <div class="row" style="align-items:center;gap:22px"><svg id="p13-clk" viewBox="0 0 24 24" style="width:96px;height:96px;fill:none;stroke:{INK};stroke-width:2.2;stroke-linecap:round;overflow:visible"><circle cx="12" cy="12" r="10"/><path id="p13-hand" d="M12 12 L12 5"/><path id="p13-hand2" d="M12 12 L16 12"/></svg><span id="p13-h" class="xb" style="font-size:110px">hours</span></div>
  </div>
  <svg class="web">{w1}{w2}</svg>
  <span class="note dim" id="p13-n0" style="position:absolute;left:100px;top:385px">5 videos</span>
  <span class="note dim" id="p13-n1" style="position:absolute;left:100px;top:835px">5 accounts</span>
  <span class="note dim" id="p13-n2" style="position:absolute;left:100px;top:1205px">5 platforms</span>
  {vt}{av}{lg}""")
js.append(f"tl.fromTo('#p13-clk', {{opacity:0, scale:.5}}, {{opacity:1, scale:1, duration:.35, ease:'back.out(2)'}}, {s + 0.03:.3f});")
js.append(f"tl.fromTo('#p13-hand', {{rotation:0, svgOrigin:'12 12'}}, {{rotation:1440, svgOrigin:'12 12', duration:{e - s:.3f}, ease:'none'}}, {s:.3f});")
js.append(f"tl.fromTo('#p13-hand2', {{rotation:0, svgOrigin:'12 12'}}, {{rotation:120, svgOrigin:'12 12', duration:{e - s:.3f}, ease:'none'}}, {s:.3f});")
slam("#p13-h", t(315) - 0.05, 1.4)
for row, wi in (("v", 320), ("a", 324), ("l", 327)):
    js.append(f"tl.fromTo('#p13 [id^=p13-{row}]', {{opacity:0, y:40, scale:.7}}, {{opacity:1, y:0, scale:1, duration:.32, stagger:.06, ease:'back.out(2)'}}, {t(wi - 2) - 0.05:.3f});")
    sfx.append(("tick_002", t(wi - 2), 0.2))
js.append(f"tl.fromTo('#p13-n0', {{opacity:0}}, {{opacity:1, duration:.2}}, {t(318):.3f}); tl.fromTo('#p13-n1', {{opacity:0}}, {{opacity:1, duration:.2}}, {t(322):.3f}); tl.fromTo('#p13-n2', {{opacity:0}}, {{opacity:1, duration:.2}}, {t(326):.3f});")
js.append(f"tl.fromTo('#p13 .p13-w1', {{strokeDashoffset:1400}}, {{strokeDashoffset:0, duration:.5, stagger:.012, ease:'power2.out'}}, {t(322) + 0.05:.3f});")
js.append(f"tl.fromTo('#p13 .p13-w2', {{strokeDashoffset:1400}}, {{strokeDashoffset:0, duration:.5, stagger:.012, ease:'power2.out'}}, {t(325) + 0.05:.3f});")
sfx += [("riser", t(318), 0.18), ("dry-pop-alert", t(315), 0.22)]

# ---------------------------------------------------------------- P14 "use my content planner ... you go to content.novasagency.com" — keyboard + return
URL = "content.novasagency.com"
s, e = t(337) - 0.06, (t(347) - 0.06)  # hands straight to the next page
ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm."]
kid = lambda c: "dot" if c == "." else c
kb = (f'<div class="kr">{"".join(f"<b class=k id=k-{kid(c)}>{c}</b>" for c in ROWS[0])}</div>'
      f'<div class="kr">{"".join(f"<b class=k id=k-{kid(c)}>{c}</b>" for c in ROWS[1])}<b class="k ret" id="k-ret">return&nbsp;&#8629;</b></div>'
      f'<div class="kr"><b class="k w">&#8679;</b>{"".join(f"<b class=k id=k-{kid(c)}>{c}</b>" for c in ROWS[2])}<b class="k w">&#8679;</b></div>'
      f'<div class="kr"><b class="k cmd">&#8984;</b><b class="k w" id="k-space"></b><b class="k cmd">&#8984;</b></div>')
scene("p14", s, e, f"""
  <div class="stack" style="left:0;right:0;top:220px"><div class="row" style="align-items:baseline;gap:20px"><span class="sm" style="font-size:56px">{words_in('p14w', ['my'], [337])}</span><span id="p14-t" class="xb" style="font-size:100px">content planner</span></div></div>
  <div id="p14-win" class="bwin" style="top:400px;height:560px">
    <div class="bbar"><i></i><i></i><i></i><div class="urlpill"><i class="ldot"></i><span id="p14-url"></span><span id="p14-caret" class="ucaret"></span><i id="p14-load" class="uload"></i></div></div>
    <div class="newtab" id="p14-nt"><b></b><b></b><b></b><b></b></div>
    <div class="bview" id="p14-view"><img src="assets/img/planner.jpg"/></div>
  </div>
  <div id="p14-kb" class="kb" style="top:1020px">{kb}</div>""")
rev("#p14-t", t(338) - 0.05, y=24)
js.append(f"tl.fromTo('#p14-win', {{opacity:0, y:70, scale:.96}}, {{opacity:1, y:0, scale:1, duration:.45, ease:'power3.out'}}, {s + 0.1:.3f});")
u0, u1 = t(345) - 0.02, t(346) - 0.05
js.append(f"tl.fromTo('#p14-kb', {{opacity:0, y:260}}, {{opacity:1, y:0, duration:.5, ease:'expo.out'}}, {u0 - 0.65:.3f});")
js.append(f"(function(){{ const s = {json.dumps(URL)}, o = {{n:0}}; tl.fromTo(o, {{n:0}}, {{n:s.length, duration:{u1 - u0:.3f}, ease:'none', onUpdate(){{ (document.getElementById('p14-url') || {{}}).textContent = s.slice(0, Math.round(o.n)); }}}}, {u0:.3f}); }})();")
for i, c in enumerate(URL):
    at = u0 + (u1 - u0) * (i + 0.5) / len(URL)
    js.append(f"tl.fromTo('#k-{kid(c)}', {{y:0, backgroundColor:'#fbf9f5', boxShadow:'0 4px 0 rgba(40,26,14,.2)'}}, {{y:4, backgroundColor:'#e6e0d6', boxShadow:'0 0px 0 rgba(40,26,14,.2)', duration:.04, yoyo:true, repeat:1, immediateRender:false}}, {at:.3f});")
    if i % 2 == 0:
        sfx.append(("click_004", at, 0.12))
ent = u1 + 0.18
js.append(f"tl.fromTo('#k-ret', {{y:0, scale:1, backgroundColor:'#fbf9f5', color:'{INK}'}}, {{y:6, scale:.95, backgroundColor:'{INK}', color:'#fbf9f5', duration:.09, ease:'power2.out', immediateRender:false}}, {ent:.3f});")
js.append(f"tl.to('#k-ret', {{y:0, scale:1, backgroundColor:'#fbf9f5', color:'{INK}', duration:.3, ease:'power2.out', immediateRender:false}}, {ent + 0.16:.3f});")
js.append(f"tl.set('#p14-caret', {{opacity:0}}, {ent:.3f});")
js.append(f"tl.fromTo('#p14-load', {{scaleX:0, opacity:1}}, {{scaleX:1, duration:.35, ease:'power2.inOut'}}, {ent + 0.04:.3f}); tl.to('#p14-load', {{opacity:0, duration:.12, immediateRender:false}}, {ent + 0.39:.3f});")
js.append(f"tl.to('#p14-nt', {{opacity:0, duration:.15, immediateRender:false}}, {ent + 0.2:.3f});")
js.append(f"tl.fromTo('#p14-view', {{opacity:0, y:30}}, {{opacity:1, y:0, duration:.3, ease:'power3.out'}}, {ent + 0.25:.3f});")
sfx += [("hard-pop-click", ent, 0.42), ("explainer-light-pop-whoosh", ent + 0.25, 0.2)]

# ---------------------------------------------------------------- P15 "you connect your accounts and you schedule your content" — real planner recording
s, e = t(347) - 0.06, cover_cut(t(356) - 0.06)
s = scene("p15", s, e, f"""
  <div class="stack" style="left:0;right:0;top:220px"><span class="sm" style="font-size:56px">{words_in('p15w', ['connect', 'your', 'accounts'], [348, 349, 350])}</span></div>
  <div id="p15-win" class="bwin" style="left:150px;right:150px;top:330px;height:{96 + 897}px">
    <div class="bbar"><i></i><i></i><i></i><div class="urlpill"><i class="ldot"></i><span>content.novasagency.com</span></div></div>
  </div>""", whoosh=False)
overlay(f'<div id="o15" style="position:absolute;left:150px;top:426px;width:780px;height:897px;border-radius:0 0 30px 30px;overflow:hidden">{vid("p15-v", "assets/video/br/planner.mp4", s, e - s, style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover", cls="")}</div>', s, e, sel="#o15")
js.append(f"tl.fromTo('#p15-win', {{opacity:0}}, {{opacity:1, duration:.3, ease:'power2.out'}}, {s:.3f});")
sfx += [("click_002", s + 1.0, 0.2), ("click_002", s + 2.4, 0.2)]

# ---------------------------------------------------------------- P16 "it posts through the APIs, so you never have to open the app"
s, e = t(360) - 0.06, cover_cut(t(376) - 0.06)  # holds a beat on "posted"
lg16 = "".join(f'<div class="lgt" id="p16-l{k}" style="left:{x - 62}px;top:900px"><img src="assets/img/logos/{LOGOS[k]}"/><b class="pok" id="p16-ok{k}">&#10003;</b></div>' for k, x in enumerate(XS))
w16 = "".join(f'<path class="p16-w" id="p16-p{k}" pathLength="100" style="stroke-dasharray:100" d="M540 560 C 540 720, {x} 740, {x} 900"/>' for k, x in enumerate(XS))
pk16 = "".join(f'<i class="pk" id="p16-k{k}" style="left:0;top:0"></i>' for k in range(5))
scene("p16", s, e, f"""
  <div id="p16-pl" class="win" style="left:250px;right:250px;top:330px;height:230px;display:flex;align-items:center;justify-content:center;gap:26px">
    <svg viewBox="0 0 24 24" style="width:84px;height:84px;fill:none;stroke:{INK};stroke-width:2;stroke-linecap:round;stroke-linejoin:round">{ICON['cal']}</svg>
    <div style="display:flex;flex-direction:column"><span class="xb" style="font-size:56px;line-height:1">content</span><span class="xb" style="font-size:56px;line-height:1">planner</span></div>
  </div>
  <span id="p16-api" class="mtag" style="left:470px;top:690px;font-size:34px;z-index:4">API</span>
  <svg class="web">{w16}</svg>{pk16}
  <span id="p16-posted" class="tk" style="position:absolute;left:50%;top:1345px;transform:translateX(-50%);font-size:38px"><b style="background:#2fae5b;color:#fff">&#10003;</b>posted</span>
  {lg16}
  <div class="stack" style="left:0;right:0;top:1130px">
    <span class="sm" style="font-size:56px">{words_in('p16w', ['you', 'never', 'have', 'to'], [366, 367, 368, 369])}</span>
    <span id="p16-t" class="xb" style="font-size:110px;line-height:1.05">open the app</span>
  </div>""")
js.append(f"tl.fromTo('#p16-pl', {{opacity:0, y:-40, scale:.95}}, {{opacity:1, y:0, scale:1, duration:.4, ease:'power3.out'}}, {s + 0.03:.3f});")
# each line draws with its dot riding it; the moment it reaches a platform, that icon pops in, then ticks
js.append(f"tl.fromTo('#p16-api', {{opacity:0, scale:.6}}, {{opacity:1, scale:1, duration:.3, ease:'back.out(2.4)'}}, {t(361) - 0.05:.3f});")
js.append(f"tl.set('#p16 [id^=p16-l]', {{opacity:0}}, {s:.3f});")
for k, x in enumerate(XS):
    a = t(361) + 0.1 + k * 0.32
    js.append(f"tl.fromTo('#p16-p{k}', {{strokeDashoffset:100}}, {{strokeDashoffset:0, duration:.75, ease:'sine.inOut'}}, {a:.3f});")
    js.append(f"tl.fromTo('#p16-k{k}', {{x:540, y:560, opacity:0, scale:1}}, {{keyframes:[{{opacity:1, duration:.06}}, {{x:{(540 + x) / 2:.0f}, y:740, duration:.37, ease:'sine.in'}}, {{x:{x}, y:900, duration:.37, ease:'sine.out'}}, {{opacity:0, scale:2.2, duration:.12}}]}}, {a:.3f});")
    js.append(f"tl.fromTo('#p16-l{k}', {{opacity:0, scale:.5, y:20}}, {{opacity:1, scale:1, y:0, duration:.32, ease:'back.out(2.4)', immediateRender:false}}, {a + 0.76:.3f});")
    js.append(f"tl.fromTo('#p16-ok{k}', {{opacity:0, scale:0}}, {{opacity:1, scale:1, duration:.28, ease:'back.out(2.6)'}}, {a + 1.0:.3f});")
    sfx += [("pluck_001", a + 0.76, 0.16), ("tick_002", a + 1.0, 0.12)]
js.append(f"tl.to('#p16 [id^=p16-l]', {{opacity:.4, duration:.3, immediateRender:false}}, {t(370) - 0.05:.3f});")
rev("#p16-t", t(370) - 0.05, y=26)
pz = t(361) + 0.1 + 4 * 0.32 + 1.35
js.append(f"tl.fromTo('#p16-posted', {{opacity:0, y:20, scale:.6}}, {{opacity:1, y:0, scale:1, duration:.35, ease:'back.out(2.4)'}}, {pz:.3f});")
sfx.append(("confirmation_002", pz, 0.3))
sfx += [("pluck_001", t(361), 0.22), ("dry-pop-alert", t(370), 0.22)]

# ---------------------------------------------------------------- P17 "I'm releasing the full beginners course very very soon"
s, e = t(411) - 0.06, (t(420) - 0.06)  # hands straight to the next page
scene("p17", s, e, f"""
  <div class="stack" style="left:0;right:0;top:330px"><span class="sm" style="font-size:56px">{words_in('p17w', ["I'm", 'releasing', 'the'], [411, 412, 413])}</span></div>
  <div id="p17-card" class="win" style="left:110px;right:110px;top:470px;height:640px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px">
    <span class="note dim">AI creator</span>
    <span id="p17-a" class="xb" style="font-size:110px;line-height:1">full</span>
    <span id="p17-b" class="xb" style="font-size:110px;line-height:1">beginners</span>
    <span id="p17-c" class="xb" style="font-size:110px;line-height:1">course</span>
    <span class="note dim" style="margin-top:10px">start to finish</span>
  </div>
  <span id="p17-soon" class="mtag" style="left:360px;top:1080px;font-size:42px">very very soon</span>""")
js.append(f"tl.fromTo('#p17-card', {{opacity:0, y:80, rotation:-3}}, {{opacity:1, y:0, rotation:0, duration:.5, ease:'back.out(1.4)'}}, {t(412) - 0.05:.3f});")
for k, (sel, wi) in enumerate((("#p17-a", 414), ("#p17-b", 415), ("#p17-c", 416))):
    rev(sel, t(wi) - 0.05, y=26)
js.append(f"tl.fromTo('#p17-soon', {{opacity:0, scale:1.6, rotation:-12}}, {{opacity:1, scale:1, rotation:-4, duration:.35, ease:'back.out(2)'}}, {t(417) - 0.05:.3f});")
sfx += [("maximize_006", t(412), 0.24), ("hard-pop-click", t(417), 0.36)]

# ---------------------------------------------------------------- P18 "Comment creator in the comments, and I'll send you all three prompts"
s, e = t(420) - 0.06, (t(432) - 0.06)  # hands straight to the next page
WORD = "CREATOR"
PC = [("1", "your character"), ("2", "image sheet"), ("3", "Genjutsu")]
pcs = "".join(f'<div class="pcd" id="p18-p{k}" style="left:{70 + k * 330}px;top:1080px"><span class="xb" style="font-size:64px;line-height:1">{n}</span><span class="sm" style="font-size:34px">{lab}</span><i style="width:90%"></i><i style="width:75%"></i><i style="width:84%"></i><i style="width:60%"></i></div>' for k, (n, lab) in enumerate(PC))
scene("p18", s, e, f"""
  <div class="stack" style="left:0;right:0;top:470px"><span id="p18-c" class="sm" style="font-size:56px">comment</span></div>
  <div id="p18-box" class="cbox" style="top:590px"><span id="p18-tx" class="xb" style="font-size:96px"></span><span class="ucaret big"></span><span id="p18-send" class="wsend">&#8593;</span></div>
  <div class="stack" style="left:0;right:0;top:880px"><span class="sm" style="font-size:52px">{words_in('p18w', ["and", "I'll", "send", "you", "all", "three", "prompts"], [425, 426, 427, 428, 429, 430, 431])}</span></div>
  {pcs}
  <div id="p18-cur" class="cursor">{CUR}</div>""")
rev("#p18-c", s + 0.04, y=12)
js.append(f"tl.fromTo('#p18-box', {{opacity:0, y:40}}, {{opacity:1, y:0, duration:.35, ease:'power3.out'}}, {s + 0.08:.3f});")
c0, c1 = t(421) - 0.05, t(421) + 0.5
js.append(f"(function(){{ const s = {json.dumps(WORD)}, o = {{n:0}}; tl.fromTo(o, {{n:0}}, {{n:s.length, duration:{c1 - c0:.3f}, ease:'none', onUpdate(){{ (document.getElementById('p18-tx') || {{}}).textContent = s.slice(0, Math.round(o.n)); }}}}, {c0:.3f}); }})();")
js.append(f"tl.fromTo('#p18-send', {{backgroundColor:'rgba(23,18,14,.12)', color:'{MUTED}'}}, {{backgroundColor:'{INK}', color:'#fbf9f5', duration:.18}}, {c1 + 0.05:.3f});")
ck18 = c1 + 0.6
js.append(f"tl.fromTo('#p18-cur', {{x:1120, y:1300, opacity:0}}, {{x:{890 - 14}, y:{679 - 8}, opacity:1, duration:.5, ease:'power3.out'}}, {ck18 - 0.55:.3f});")
js.append(f"tl.to('#p18-cur', {{scale:.82, duration:.08, yoyo:true, repeat:1, immediateRender:false}}, {ck18:.3f}); tl.to('#p18-send', {{scale:.86, duration:.08, yoyo:true, repeat:1, immediateRender:false}}, {ck18:.3f});")
js.append(f"tl.to('#p18-cur', {{x:1150, y:1100, opacity:0, duration:.45, ease:'power2.in', immediateRender:false}}, {ck18 + 0.35:.3f});")
sfx.append(("click_002", ck18, 0.4))
for k in range(len(WORD)):
    sfx.append(("click_002", c0 + (c1 - c0) * k / len(WORD), 0.14))
for k in range(3):
    js.append(f"tl.fromTo('#p18-p{k}', {{opacity:0, y:120, rotation:{(k - 1) * 8}}}, {{opacity:1, y:0, rotation:{(k - 1) * 4}, duration:.45, ease:'back.out(1.6)'}}, {t(430) - 0.15 + k * 0.1:.3f});")
sfx += [("pluck_001", t(430), 0.24)]

# ---------------------------------------------------------------- P19 end card "stay tuned for day four" — 30 blocks, today's three lit, zoom into day 3
s = t(432) - 0.06
ZX, ZY = 90 + 2 * (SEG_W + 6) + SEG_W / 2, 1340 - 40 * 1.9 / 2
scene("p19", s, DURATION, f"""
  <div id="p19-zoom" style="position:absolute;inset:0;transform-origin:{ZX:.1f}px {ZY:.1f}px">
    <div class="stack" style="left:0;right:0;top:560px">
      <span id="p19-lead" class="sm" style="font-size:56px">{words_in('p19w', ['stay', 'tuned', 'for'], [432, 433, 434])}</span>
      <div class="row" style="align-items:flex-end;justify-content:center;margin-top:6px">
        <span id="p19-day" class="xb" style="font-size:230px;line-height:1">Day</span>
        <span id="p19-n" class="xb" style="font-size:230px;line-height:1;margin-left:40px">4</span>
      </div>
    </div>
    <span id="p19-lbl" class="note" style="position:absolute;left:{90 + 2 * (SEG_W + 6):.0f}px;top:1186px">day 03 / 30</span>
    <div id="p19-bar" class="bar big" style="top:1300px">{BLOCKS.replace('{p}', 'p19')}</div>
  </div>""")
rev("#p19-day", t(435) - 0.05, y=30)
slam("#p19-n", t(436) - 0.05)
js.append(f"tl.fromTo('#p19-bar .seg', {{scaleY:0, opacity:0}}, {{scaleY:1, opacity:1, duration:.3, stagger:.014, ease:'power2.out'}}, {s + 0.1:.3f});")
lit = t(436) + 0.45
js.append(f"tl.fromTo('#p19-s0, #p19-s1', {{backgroundColor:'rgba(23,18,14,.14)'}}, {{backgroundColor:'{INK}', duration:.2, stagger:.08}}, {lit - 0.3:.3f});")
js.append(f"tl.fromTo('#p19-s2', {{backgroundColor:'rgba(23,18,14,.14)', scaleY:1}}, {{backgroundColor:'{INK}', scaleY:1.9, duration:.5, ease:'back.out(2.2)'}}, {lit:.3f});")
js.append(f"tl.fromTo('#p19-lbl', {{opacity:0, y:12}}, {{opacity:1, y:0, duration:.35, ease:'power2.out'}}, {lit + 0.15:.3f});")
js.append(f"tl.fromTo('#p19-s2', {{scaleY:1.9}}, {{scaleY:2.2, duration:.6, yoyo:true, repeat:1, ease:'sine.inOut', immediateRender:false}}, {lit + 0.6:.3f});")
zoom_at = DURATION - 1.4
js.append(f"tl.to('#p19-lbl', {{opacity:0, duration:.3, immediateRender:false}}, {zoom_at:.3f});")
js.append(f"tl.fromTo('#p19-zoom', {{scale:1, x:0, y:0}}, {{scale:60, x:{540 - ZX:.1f}, y:{960 - ZY:.1f}, duration:1.3, ease:'power3.inOut'}}, {zoom_at:.3f});")
sfx += [("dry-pop-alert", t(436), 0.24), ("pluck_001", lit, 0.3), ("riser", zoom_at + 0.25, 0.35), ("boom", DURATION - 0.12, 0.3)]

# ---------------------------------------------------------------- "Claude comes back with this": the result, a strobe back to the original, then side by side
P0 = BROLL[0]["start"]
SW_T = [1.2, 1.3333, 1.4666, 1.5999, 1.7332, 1.8665]
VL.append(f'''<div id="pay" style="position:absolute;inset:0">
  <span id="pay-o" class="mtag" style="left:50%;top:250px;transform:translateX(-50%);font-size:40px;opacity:0">original</span>
  <span id="pay-a" class="mtag" style="left:50%;top:250px;transform:translateX(-50%);font-size:40px;opacity:0;background:#fbf9f5;color:{INK}">AI</span>
  <span id="pay-l" class="mtag" style="left:150px;top:250px;font-size:40px;opacity:0">original</span>
  <span id="pay-r" class="mtag" style="left:720px;top:250px;font-size:40px;opacity:0;background:#fbf9f5;color:{INK}">AI</span>
</div>''')
js.append(f"tl.set('#pay-a', {{opacity:1}}, {P0 + 0.25:.3f});")
for k, at in enumerate(SW_T):
    show, hide = ("#pay-o", "#pay-a") if k % 2 == 0 else ("#pay-a", "#pay-o")
    js.append(f"tl.set('{show}', {{opacity:1}}, {P0 + at:.3f}); tl.set('{hide}', {{opacity:0}}, {P0 + at:.3f});")
    js.append(f"tl.fromTo('#br0', {{scale:1.06}}, {{scale:1, duration:.12, ease:'power2.out', immediateRender:false}}, {P0 + at:.3f});")
    sfx.append(("tick_002", P0 + at, 0.3))
js.append(f"tl.set('#pay-o, #pay-a', {{opacity:0}}, {P0 + 2.0:.3f});")
js.append(f"tl.fromTo('#pay-l, #pay-r', {{opacity:0, y:-20}}, {{opacity:1, y:0, duration:.25, stagger:.08, ease:'back.out(2)'}}, {P0 + 2.0:.3f});")
js.append(f"tl.to('#pay-l, #pay-r', {{opacity:0, duration:.2, immediateRender:false}}, {BROLL[0]['end'] - 0.2:.3f});")
if HOOK in ("", "0"):  # 0 = the original hook
    # ---------------------------------------------------------------- hook "exactly how you can too": original | AI slider, the line glides left then right
    W0, W1 = t(13) - 0.08, t(19) - 0.12
    VL.append(f'''<div id="wp" style="position:absolute;inset:0;opacity:0">
      <div id="wp-or" style="position:absolute;inset:0;clip-path:inset(0 0% 0 0)">{vid("wp-o", "assets/video/br/wipe-src.mp4", W0, W1 - W0 + 0.5)}</div>
      <div id="wp-ai" style="position:absolute;inset:0;clip-path:inset(0 0 0 50%)">{vid("wp-a", "assets/video/br/wipe-ai.mp4", W0, W1 - W0 + 0.5)}</div>
      <i id="wp-line" style="position:absolute;top:0;bottom:0;left:537px;width:6px;background:#fbf9f5;box-shadow:0 0 18px rgba(0,0,0,.35)"></i>
      <i id="wp-line2" style="position:absolute;top:0;bottom:0;left:537px;width:6px;background:#fbf9f5;box-shadow:0 0 18px rgba(0,0,0,.35);opacity:0"></i>
      <span id="wp-l" class="mtag" style="left:60px;top:1470px;font-size:40px">original</span>
      <span id="wp-r" class="mtag" style="left:auto;right:60px;top:1470px;font-size:40px;background:#fbf9f5;color:{INK}">AI</span>
    </div>''')
    js.append(f"tl.fromTo('#wp', {{opacity:0, scale:1.06}}, {{opacity:1, scale:1, duration:.2, ease:'power2.out'}}, {W0:.3f}); tl.set('#wp', {{opacity:0}}, {W1 + 0.5:.3f});")
    # the middle line splits in two and both glide outwards, opening onto his face
    js.append(f"tl.set('#wp-line2', {{opacity:1}}, {W1 - 0.05:.3f});")
    js.append(f"tl.to('#wp-line', {{x:-560, duration:.5, ease:'power2.inOut', immediateRender:false}}, {W1 - 0.05:.3f});")
    js.append(f"tl.to('#wp-line2', {{x:560, duration:.5, ease:'power2.inOut', immediateRender:false}}, {W1 - 0.05:.3f});")
    js.append(f"tl.fromTo('#wp-or', {{clipPath:'inset(0 50% 0 0%)'}}, {{clipPath:'inset(0 50% 0 0%)', duration:.01, immediateRender:false}}, {W1 - 0.07:.3f});")
    js.append(f"tl.to('#wp-or', {{clipPath:'inset(0 100% 0 0%)', duration:.5, ease:'power2.inOut', immediateRender:false}}, {W1 - 0.05:.3f});")
    js.append(f"tl.to('#wp-ai', {{clipPath:'inset(0 0 0 100%)', duration:.5, ease:'power2.inOut', immediateRender:false}}, {W1 - 0.05:.3f});")
    js.append(f"tl.to('#wp-l', {{x:-300, opacity:0, duration:.4, ease:'power2.in', immediateRender:false}}, {W1 - 0.05:.3f}); tl.to('#wp-r', {{x:300, opacity:0, duration:.4, ease:'power2.in', immediateRender:false}}, {W1 - 0.05:.3f});")
    sfx.append(("arrow-whoosh", W1 - 0.08, 0.26))
    js.append(f"tl.fromTo('#wp-line', {{scaleY:0}}, {{scaleY:1, duration:.25, ease:'power3.out'}}, {W0:.3f});")
    D = W1 - W0
    for sel, prop, fmt in (("#wp-ai", "clipPath", "inset(0 0 0 {}%)"), ("#wp-line", "x", "{}")):
        pts = [(0.25, 50), (0.25 + D * 0.3, 22), (0.25 + D * 0.7, 78), (D - 0.05, 50)]
        for (ta, va), (tb, vb) in zip(pts, pts[1:]):
            fv = (lambda v: f"'{fmt.format(v)}'") if prop == "clipPath" else (lambda v: f"{(v - 50) * 10.8:.0f}")
            js.append(f"tl.fromTo('{sel}', {{{prop}:{fv(va)}}}, {{{prop}:{fv(vb)}, duration:{tb - ta:.3f}, ease:'sine.inOut', immediateRender:false}}, {W0 + ta:.3f});")
    js.append(f"tl.fromTo('#wp-l, #wp-r', {{opacity:0, y:20}}, {{opacity:1, y:0, duration:.25, stagger:.06, ease:'back.out(2)'}}, {W0 + 0.15:.3f});")
    sfx += [("arrow-whoosh", W0 - 0.05, 0.3), ("fast-whoosh", W0 + 0.25 + D * 0.3, 0.2)]
    SCRIM_WIN = [(W0, W1)]
EXTRA_AUDIO = f'<audio id="song" src="assets/audio/song.wav" data-start="{P0:.3f}" data-duration="3.400" data-track-index="18" data-volume="0.42"></audio>'
sfx += [("arrow-whoosh", 0.0, 0.3), ("explainer-light-pop-whoosh", P0, 0.24), ("hard-pop-click", P0 + 2.0, 0.3)]

# ---------------------------------------------------------------- captions (small lead-in, bold phrase, italic accent)
CAPS = [
    [["s:0", "s:1"], ["b:2"]],
    [["s:7", "s:8", "s:9", "s:10"], ["b:11", "b:12"]],
    [["s:13", "s:14", "s:15"], ["b:16", "b:17", "b:18"]],
    [["s:19", "s:20"], ["b:21"]],
    [["s:28", "s:29", "s:30", "s:31"], ["b:32", "b:33"]],
    [["s:34", "s:35", "s:36", "s:37", "s:38"], ["i:39"]],
    [["s:40", "s:41", "s:42", "s:43"]],
    [["s:53", "s:54", "s:55"], ["b:56", "b:57"]],
    [["s:65", "s:66", "s:67", "s:68", "s:69"], ["b:70", "b:71"]],
    [["s:72", "s:73"], ["b:74", "b:75"]],
    [["s:76", "s:77", "s:78", "s:79"], ["s:80", "s:81", "s:82"], ["b:83", "b:84"]],
    [["s:113", "s:114", "s:115", "s:116", "s:117", "s:118"], ["s:119", "s:120"], ["b:121", "b:122"]],
    [["s:138", "s:139", "s:140", "s:141", "s:142", "s:143"], ["b:144", "b:145"], ["i:146"]],
    [["s:147", "s:148", "s:149", "s:150"], ["b:151", "b:152", "b:153"]],
    [["s:154", "s:155", "s:156", "s:157", "s:158"]],
    [["s:182", "s:183", "s:184", "s:185", "s:186"], ["b:187"], ["s:188", "s:189"]],
    [["s:190", "s:191", "s:192"], ["b:193"], ["s:194", "s:195", "i:196"]],
    [["s:197", "s:198", "s:199", "s:200"], ["b:201", "b:202", "b:203"]],
    [["s:229", "s:230", "s:231"], ["b:232", "b:233"]],
    [["s:259", "s:260", "s:261", "s:262", "s:263"], ["s:264", "s:265", "s:266", "s:267", "b:268"]],
    [["s:288", "s:289"], ["b:290", "b:291", "b:292"]],
    [["s:293", "s:294", "s:295", "s:296"], ["b:297"]],
    [["s:298", "s:299", "s:300", "s:301", "s:302"], ["s:303", "s:304", "s:305", "s:306", "s:307"], ["b:308", "b:309", "s:310", "s:311"]],
    [["s:329", "s:330", "s:331", "s:332", "s:333", "s:334"], ["s:335", "s:336"]],
    [["s:356", "s:357", "s:358"], ["b:359"]],
    [["s:373", "s:374", "s:375", "s:376", "s:377", "s:378", "s:379"], ["b:380"]],
    [["s:381", "s:382", "s:383", "s:384", "s:385"], ["b:386"], ["s:387", "s:388", "s:389"]],
    [["s:390", "s:391", "s:392", "s:393", "s:394"], ["s:395", "s:396"], ["b:397", "b:398"]],
    [["s:399", "s:400", "s:401", "s:402", "s:403"], ["b:404", "b:405"]],
    [["s:406", "s:407", "s:408"], ["b:409", "b:410"]],
]
KEEP_CASE = ("I", "I'm", "I've", "I'll", "AI", "AI.", "Claude", "Claude,", "Claude.", "Jack.", "Higgsfield", "Higgsfield,")
cap_cover = [(a, b) for _, a, b, _ in scenes] + [(b_['start'], b_['end']) for b_ in BROLL]  # captions wait for the full-frame result


def next_cover(at):
    starts = [a for a, b in cap_cover if a > at + 0.01]
    return min(starts) if starts else AROLL_END


samples = []
for line in open("edit/faces-cut-2fps.txt"):
    p = line.split()
    if p[1] != "none":
        samples.append(((int(p[0][1:5]) - 1) / 2, *map(float, p[1:5])))
cap_html, cap_js, lifted = [], [], []
for g, lines in enumerate(CAPS):
    idx = [int(tok.split(":")[1]) for ln in lines for tok in ln]
    g_start = max(0.0, t(min(idx)) - 0.08)
    for pa, pb in cap_cover:
        if pa - 0.01 <= g_start < pb:
            g_start = pb + 0.01
    nxt = CAPS[g + 1] if g + 1 < len(CAPS) else None
    next_start = t(min(int(x.split(":")[1]) for ln in nxt for x in ln)) - 0.08 if nxt else AROLL_END
    end = min(next_start, next_cover(g_start), t(max(idx)) + 0.75)
    if end - g_start < 0.25:
        continue
    rows = []
    for ln in lines:
        spans = []
        for tok in ln:
            style, i = tok.split(":")
            cls = {"s": "cs", "b": "cb", "i": "ci"}[style[0]]
            text = TOK[int(i)]["text"]
            if not text:
                continue
            if style[0] == "s" and text not in KEEP_CASE:
                text = text.lower()
            spans.append(f'<span class="w {cls}" id="w{i}">{esc(text)}</span>')
        rows.append(f'<div class="cl">{" ".join(spans)}</div>')
    scrim = " scrim" if any(g_start < bb["end"] and end > bb["start"] for bb in BROLL) or any(g_start < wb and end > wa for wa, wb in SCRIM_WIN) else ""
    high = [f for f in samples if g_start - 0.3 <= f[0] <= end + 0.3 and f[2] < 0.36]
    lift = ' style="bottom:1430px"' if high else ""
    if high:
        lifted.append((g_start, end))
    cap_html.append(f'<div class="cap clip{scrim}" id="cap{g}"{lift} data-start="{g_start:.3f}" data-duration="{end - g_start:.3f}" data-track-index="2"><div class="capi">{"".join(rows)}</div></div>')
    for i in idx:
        if TOK[i]["text"]:
            cap_js.append(f"word('#w{i}', {max(0.0, t(i) - 0.05):.3f});")
    cap_js.append(f"tl.fromTo('#cap{g} .capi', {{opacity:1, filter:'blur(0px)', y:0}}, {{opacity:0, filter:'blur(10px)', y:-10, duration:.12, ease:'power1.in', immediateRender:false}}, {end - 0.12:.3f});")

# ---------------------------------------------------------------- b-roll layer (inside the camera, muted)
br_html = "".join(f'<video id="br{n}" class="clip brl" src="{b["file"]}" data-start="{b["start"]:.3f}" data-duration="{b["end"] - b["start"]:.3f}" data-track-index="1" muted playsinline></video>'
                  for n, b in enumerate(BROLL))
br_windows = [(b["start"], b["end"]) for b in BROLL]

# ---------------------------------------------------------------- camera: hook slam, face-aware punch-ins, slow push on b-roll
extra = [t(19), t(13), t(65), t(72), t(147), t(154), t(190), t(197), t(381), t(390), t(399), t(406)]
edges = sorted(set([0.0] + [s["start"] for s in SEGS] + [x for w in cap_cover + br_windows for x in w] + [round(x - 0.08, 3) for x in extra]))
edges = [e for e in edges if e < AROLL_END - 0.05] + [AROLL_END]
merged = []
for x in edges:
    if not merged or x - merged[-1] >= 0.1:
        merged.append(x)
edges = merged if merged[-1] == AROLL_END else merged[:-1] + [AROLL_END]
CAP_CLEAR, ZOOMS = 0.40, [1.0, 1.06, 1.12, 1.18, 1.24]
cam_js, soft_cuts = [], []
prev_size, tight = None, False
for a, b in zip(edges, edges[1:]):
    covered = any(pa - 0.01 <= a and b <= pb + 0.01 for pa, pb in cap_cover)
    on_broll = any(pa - 0.01 <= a and b <= pb + 0.01 for pa, pb in br_windows)
    win = [f for f in samples if a - 0.3 <= f[0] <= b + 0.3]
    if a == 0:
        cam_js.append("tl.fromTo('#cam', {scale:1.35, transformOrigin:'540px 960px'}, {scale:1, duration:.5, ease:'expo.out'}, 0);")
        cam_js.append(f"tl.fromTo('#cam', {{scale:1}}, {{scale:1.04, duration:{b - 0.5:.3f}, ease:'none', immediateRender:false}}, .5);")
        continue
    if covered or on_broll or not win:
        cam_js.append(f"tl.fromTo('#cam', {{scale:1, transformOrigin:'540px 960px'}}, {{scale:1.04, duration:{b - a:.3f}, ease:'none', immediateRender:false}}, {a:.3f});")
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
    clear = 0.28 if any(la < b and a < lb for la, lb in lifted) else CAP_CLEAR  # lifted captions leave room to punch in
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

# Pages crossfade into the footage; same-size cuts get a soft focus pull.
# pages that hand to another page: the old page stays until the new one has dissolved in (no face flash, no glitch)
scenes.sort(key=lambda x: x[1])
handoff = set()
for k in range(len(scenes) - 1):
    sid, a, b_end, body = scenes[k]
    nid, na, nb, nbody = scenes[k + 1]
    if na <= b_end + 0.1:
        scenes[k] = (sid, a, max(b_end, na + 0.34), body)
        handoff.add(sid)
        js.append(f"tl.fromTo('#{nid}', {{opacity:0}}, {{opacity:1, duration:.32, ease:'sine.inOut'}}, {na:.3f});")
back_js = []
for sid, a, b_end, _ in scenes:
    if b_end >= AROLL_END - 0.01 or sid in handoff or any(abs(b_end - w[0]) < 0.02 for w in br_windows):
        continue
    back_js.append(f"tl.fromTo('#{sid}', {{opacity:1}}, {{opacity:0, duration:.42, ease:'sine.inOut', immediateRender:false}}, {b_end - 0.42:.3f});")
    back_js.append(f"tl.fromTo('#{sid} .sheet', {{scale:1, filter:'blur(0px)'}}, {{scale:1.03, filter:'blur(10px)', duration:.42, ease:'sine.inOut', immediateRender:false}}, {b_end - 0.42:.3f});")
cut_starts = [s["start"] for s in SEGS[1:]]
if os.path.exists("edit/qa-latest.json"):
    soft_cuts += [j for j in json.load(open("edit/qa-latest.json"))["jumps"] if not any(abs(j - x) < 0.05 for x in soft_cuts)]
for a in soft_cuts:
    if any(abs(a - c) < 0.02 for c in cut_starts) and not any(abs(a - x[1]) < 0.05 for x in scenes):
        back_js.append(f"focus({a:.3f});")

# ---------------------------------------------------------------- assemble
if HOOK and not FULL:
    END = round(t(19) + 0.5, 3)
    st = lambda h: float(re.search(r'data-start="([\d.]+)"', h).group(1)) if re.search(r'data-start="([\d.]+)"', h) else 0
    scenes = [(sid, a, min(b, END), body) for sid, a, b, body in scenes if a < END]
    sfx = [x for x in sfx if x[1] < END]
    cap_html = [h for h in cap_html if st(h) < END]
    VL = [v for v in VL if st(v) < END]
    br_html, EXTRA_AUDIO = "", ""
    DURATION = AROLL_END = END
sfx_html = EXTRA_AUDIO + "\n" + "\n".join(f'<audio id="sfx{n}" src="assets/audio/sfx/{name}.wav" data-start="{at:.3f}" data-track-index="{20 + n}" data-volume="{vol}"></audio>'
                     for n, (name, at, vol) in enumerate(sorted(sfx, key=lambda x: x[1])))
scene_html = "\n".join(f"""<section class="scene clip" id="{sid}" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="3">
 <div class="sheet"><img class="paper" src="assets/img/paper-clean.jpg"/>
  <div class="content">{body}
  </div>
 </div>
</section>""" for sid, a, b, body in scenes) + f'\n<div id="vlayer" style="position:absolute;inset:0;pointer-events:none;z-index:40">{"".join(VL)}</div>' 
page = open("edit/template.html").read()
page = re.sub(r'\s*<audio id="bgm"[^>]*></audio>', "", page)  # no music bed
page = (page.replace("{{DURATION}}", f"{DURATION:.3f}").replace("{{AROLL_END}}", f"{AROLL_END:.3f}")
        .replace("{{SCENES}}", scene_html).replace("{{CAPTIONS}}", "\n".join(cap_html)).replace("{{GRADE_LAYER}}", br_html)
        .replace("{{SFX}}", sfx_html).replace("{{JS}}", "\n".join(cam_js + back_js + js + cap_js))
        .replace("{{GRADE}}", GRADE).replace("{{INK}}", INK).replace("{{PAPER}}", PAPER).replace("{{RED}}", RED).replace("{{MUTED}}", MUTED))
open((f"../2026-10-23-day3-hooks/out/full-hook-{HOOK}.html" if FULL else f"../2026-10-23-day3-hooks/out/hook-{HOOK}.html") if HOOK else "index.html", "w").write(page)
print(f"index.html: {len(scenes)} pages, {len(cap_html)} caption groups, {len(BROLL)} b-roll, {len(sfx)} sfx, {DURATION:.2f}s")
