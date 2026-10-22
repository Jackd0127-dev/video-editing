"""Generate index.html for the Day 1 edit from the cut (edit/words.json), caption tokens
(edit/tokens.json) and face positions (edit/faces.json). Run from the project root:

    python3 -I edit/build.py
"""
import html
import json

TOK = json.load(open("edit/tokens.json"))
SEGS = json.load(open("edit/words.json"))["segments"]
FACES = {f["i"]: f for f in json.load(open("edit/faces.json"))}
AROLL_END = SEGS[-1]["end"]
DURATION = round(AROLL_END + 3.6, 3)

INK, PAPER, RED, MUTED = "#17120e", "#ede7df", "#17120e", "#7a6e63"
GRADE = ""  # never grade his footage (Day 2 note); Day 1 shipped with a light grade that read as "washed"


def t(i):
    return TOK[i]["start"]


def esc(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------- paper scenes
# Each scene: id, start, end, inner html, and a list of JS timeline lines.
scenes = []
js = []  # timeline code, appended in order
sfx = []  # (file, start, volume)


def scene(sid, start, end, body, whoosh=True):
    scenes.append((sid, start, end, body))
    js.append(f"enter('#{sid}', {start:.3f});")
    if whoosh:
        sfx.append(("fast-whoosh", max(0, start - 0.32), 0.42))


def rev(sel, at, **o):
    js.append(f"rev('{sel}', {at:.3f}, {json.dumps(o)});")


# P1 — hook page after the face: "I wish I / discovered / sooner." stacked tight, three different entrances
s1 = t(3) - 0.06
scene("p1", s1, t(10) - 0.12, f"""
  <div class="stack" style="left:0;right:0;top:700px">
    <span id="p1-wish" class="sm" style="font-size:56px"><span class="ch" id="p1-w0">i</span> <span class="ch" id="p1-w1">wish</span> <span class="ch" id="p1-w2">i</span></span>
    <div class="mask" style="margin-top:8px"><span id="p1-disc" class="xb" style="font-size:150px;line-height:.95">discovered</span></div>
    <span id="p1-soon" class="ital" style="font-size:170px;line-height:.8;margin-top:-34px">sooner.</span>
  </div>""")
for k, wi in enumerate([3, 4, 5]):
    js.append(f"tl.fromTo('#p1-w{k}', {{opacity:0, y:14, filter:'blur(10px)'}}, {{opacity:1, y:0, filter:'blur(0px)', duration:.25, ease:'power2.out'}}, {t(wi) - 0.05:.3f});")
js.append(f"tl.fromTo('#p1-disc', {{yPercent:150, opacity:0}}, {{yPercent:0, opacity:1, duration:.45, ease:'expo.out'}}, {t(6) - 0.06:.3f});")
js.append(f"tl.fromTo('#p1-soon', {{opacity:0, scale:1.4, filter:'blur(16px)'}}, {{opacity:1, scale:1, filter:'blur(0px)', duration:.42, ease:'expo.out'}}, {t(7) - 0.05:.3f});")
sfx += [("dry-pop-alert", t(7), 0.22)]

# P3 — "This is day one of my" as a short centred stat page; "30 day series" goes back to the face
s3, e3 = t(11) - 0.06, t(17) - 0.06
bars = "".join(f'<i class="seg" id="p3-s{k}"></i>' for k in range(30))
scene("p3", s3, e3, f"""
  <div class="stack" style="left:0;right:0;top:560px">
    <span id="p3-this" class="sm" style="font-size:56px">this is</span>
    <div class="row" style="align-items:flex-end;justify-content:center;margin-top:10px">
      <span id="p3-day" class="xb" style="font-size:230px;line-height:1">Day</span>
      <span id="p3-one" class="xb" style="font-size:230px;line-height:1;margin-left:40px">1</span>
    </div>
    <span id="p3-ofmy" class="sm" style="font-size:56px;margin-top:22px">of my</span>
  </div>
  <div id="p3-bar" class="bar" style="top:1250px">{bars}</div>""")
js.append(f"tl.fromTo('#p3-this', {{opacity:0, filter:'blur(14px)'}}, {{opacity:1, filter:'blur(0px)', duration:.3}}, {t(11) - 0.02:.3f});")
js.append(f"tl.fromTo('#p3-day', {{opacity:0, y:60, filter:'blur(14px)'}}, {{opacity:1, y:0, filter:'blur(0px)', duration:.45, ease:'expo.out'}}, {t(13) - 0.06:.3f});")
js.append(f"tl.fromTo('#p3-one', {{opacity:0, scale:1.5, filter:'blur(20px)'}}, {{opacity:1, scale:1, filter:'blur(0px)', duration:.45, ease:'expo.out'}}, {t(14) - 0.05:.3f});")
rev("#p3-ofmy", t(15) - 0.04, y=12)
js.append(f"tl.fromTo('#p3-bar .seg', {{scaleY:0, opacity:0}}, {{scaleY:1, opacity:1, duration:.22, stagger:.012, ease:'power2.out'}}, {t(14):.3f});")
js.append(f"tl.fromTo('#p3-s0', {{backgroundColor:'rgba(23,18,14,.14)'}}, {{backgroundColor:'{INK}', duration:.2}}, {t(14) + 0.35:.3f});")
sfx += [("dry-pop-alert", t(14), 0.24)]

# P4 — "Day one is Claude Motion Graphics." as an animated Claude logo
s4, e4 = SEGS[2]["start"], SEGS[3]["start"]
import math as _m4
rays = "".join(f'<line class="ray" x1="{450 + 250 * _m4.cos(k * _m4.pi / 12):.1f}" y1="{450 + 250 * _m4.sin(k * _m4.pi / 12):.1f}" x2="{450 + 430 * _m4.cos(k * _m4.pi / 12):.1f}" y2="{450 + 430 * _m4.sin(k * _m4.pi / 12):.1f}"/>' for k in range(24))
scene("p4", s4, e4, f"""
  <svg class="burst" width="900" height="900" style="left:90px;top:400px"><g id="p4-rays">{rays}</g><circle id="p4-orbit" cx="450" cy="450" r="330" class="orbit"/></svg>
  <div id="p4-spin" class="logo-stage" style="left:340px;top:650px;width:400px;height:400px">
    <img class="echo-m" id="p4-e0" src="assets/img/claude-mark.svg"/><img class="echo-m" id="p4-e1" src="assets/img/claude-mark.svg"/><img class="echo-m" id="p4-e2" src="assets/img/claude-mark.svg"/>
    <img id="p4-mark" class="echo-m solid" src="assets/img/claude-mark.svg"/>
  </div>
  <div class="stack" style="left:0;right:0;top:1180px">
    <span id="p4-mg" class="ital" style="font-size:104px">{"".join(f'<span class="ch">{c if c != " " else "&nbsp;"}</span>' for c in "motion graphics")}</span>
  </div>""")
js.append(f"tl.fromTo('#p4-mark', {{opacity:0, scale:.2, rotation:-200, filter:'blur(18px)'}}, {{opacity:1, scale:1, rotation:0, filter:'blur(0px)', duration:.9, ease:'expo.out'}}, {s4 + 0.05:.3f});")
js.append(f"tl.fromTo('#p4-spin', {{rotation:0}}, {{rotation:24, duration:{e4 - s4:.3f}, ease:'none'}}, {s4:.3f});")
js.append(f"tl.fromTo('#p4-spin .echo-m:not(.solid)', {{opacity:.35, scale:1}}, {{opacity:0, scale:2.3, duration:.9, stagger:.14, ease:'power2.out'}}, {t(40) - 0.05:.3f});")
js.append(f"tl.fromTo('#p4-rays .ray', {{strokeDashoffset:180}}, {{strokeDashoffset:-180, duration:.8, stagger:.012, ease:'power2.out'}}, {t(40) - 0.08:.3f});")
js.append(f"tl.fromTo('#p4-orbit', {{strokeDashoffset:2075, rotation:-90, svgOrigin:'450 450'}}, {{strokeDashoffset:0, rotation:30, svgOrigin:'450 450', duration:1.1, ease:'power2.inOut'}}, {s4 + 0.3:.3f});")
js.append(f"tl.fromTo('#p4-mg .ch', {{opacity:0, y:30, filter:'blur(10px)'}}, {{opacity:1, y:0, filter:'blur(0px)', duration:.35, stagger:.025, ease:'power3.out'}}, {t(41) - 0.08:.3f});")
sfx += [("arrow-whoosh", s4, 0.35), ("boom", t(40) - 0.05, 0.22), ("pluck_001", t(41), 0.22)]

# P5 — "I bought the Claude Pro Plan." as a membership card
s5, e5 = SEGS[5]["start"], t(66) - 0.05
scene("p5", s5, e5, f"""
  <div class="stack" style="left:0;right:0;top:300px">
    <img id="p5-logo" src="assets/img/claude-mark.svg" style="width:150px;height:150px"/>
    <span id="p5-lead" class="sm" style="margin-top:36px;font-size:56px">i bought the</span>
  </div>
  <div id="p5-card" class="pro-card" style="top:700px">
    <div class="row" style="justify-content:space-between;align-items:center;width:100%">
      <div class="row" style="align-items:center;gap:16px"><img src="assets/img/claude-mark-white.svg" style="width:60px;height:60px"/><span class="xb" style="font-size:56px;color:#fff;text-shadow:none">Claude</span></div>
      <span id="p5-pill" class="pro-pill">PRO</span>
    </div>
    <div class="chip-gold"></div>
    <div class="row" style="justify-content:space-between;align-items:flex-end;width:100%">
      <div class="col"><span class="caps" style="color:rgba(255,255,255,.78)">member</span><span class="xb" style="font-size:46px;color:#fff;text-shadow:none;margin-top:6px">Jack</span></div>
      <span id="p5-plan" class="ital" style="font-size:118px;color:#fff;text-shadow:none;line-height:.9">Pro plan</span>
    </div>
    <div class="sheen-rot"><div id="p5-sheen" class="sheen"></div></div>
  </div>
  <span class="note" style="position:absolute;left:110px;top:1290px;display:flex;flex-direction:column"><span>order confirmed.</span><span>bought yesterday.</span></span>""")
js.append(f"tl.fromTo('#p5-logo', {{opacity:0, scale:.3, rotation:-140}}, {{opacity:1, scale:1, rotation:0, duration:.6, ease:'back.out(1.6)'}}, {s5 + 0.04:.3f});")
rev("#p5-lead", t(57) - 0.04, y=12)
js.append(f"tl.fromTo('#p5-card', {{opacity:0, y:220, rotationX:32, rotationY:-26, transformPerspective:1400}}, {{opacity:1, y:0, rotationX:0, rotationY:0, transformPerspective:1400, duration:.7, ease:'power3.out'}}, {s5 + 0.12:.3f});")
js.append(f"tl.to('#p5-card', {{rotationY:8, rotationX:-5, transformPerspective:1400, duration:{e5 - s5 - 0.85:.3f}, ease:'sine.inOut', immediateRender:false}}, {s5 + 0.82:.3f});")
js.append(f"tl.fromTo('#p5-pill', {{opacity:0, scale:1.8}}, {{opacity:1, scale:1, duration:.3, ease:'back.out(2)'}}, {t(61) - 0.03:.3f});")
rev("#p5-plan", t(62) - 0.04, y=20)
rev("#p5 .note", t(62) + 0.3, y=8)
js.append(f"tl.fromTo('#p5-sheen', {{x:-500}}, {{x:1700, duration:.65, ease:'power2.inOut'}}, {t(62) + 0.05:.3f});")
sfx += [("maximize_006", s5 + 0.12, 0.32), ("glass_002", t(62) + 0.1, 0.32), ("dry-pop-alert", t(61), 0.18)]



# P7 — "insane motion graphics like this." four kinetic cards, then a riser + hit back to the face
s7 = t(118) - 0.05
cuts = [s7, t(119) - 0.04, t(120) - 0.04, t(121) - 0.04, SEGS[11]["start"]]
CLIFF = cuts[-1]
rows = "".join(f'<div class="irow {"solid" if k % 2 else "line"}" id="p7a-r{k}" style="top:{380 + k * 170}px">INSANE INSANE INSANE INSANE</div>' for k in range(7))
echoes = "".join(f'<span class="xb mecho" style="opacity:{0.08 + k * 0.1:.2f};transform:translateX({-(6 - k) * 48}px)">motion</span>' for k in range(6))
scene("p7", cuts[0], cuts[-1], f"""
  <div id="p7a" class="sub">{rows}</div>
  <div id="p7b" class="sub">
    <div class="speed">{"".join(f'<i style="top:{560 + k * 90}px;width:{300 + (k * 137) % 500}px"></i>' for k in range(10))}</div>
    <div id="p7b-word" class="center-abs" data-layout-allow-overlap style="top:820px;height:280px">{echoes}<span id="p7b-main" class="xb mecho main">motion</span></div>
  </div>
  <div id="p7c" class="sub grid-bg">
    <svg class="burst" width="1080" height="1920"><circle id="p7c-c" cx="250" cy="760" r="120" class="shape"/><rect id="p7c-s" x="720" y="1080" width="200" height="200" class="shape"/><path id="p7c-t" d="M820 560 L940 760 L700 760 Z" class="shape"/><circle cx="540" cy="930" r="360" class="shape thin"/></svg>
    <span id="p7c-word" class="xb center-abs" style="font-size:220px;top:820px">graphics</span>
  </div>
  <div id="p7d" class="sub">
    <div id="p7d-stack" class="stack" style="left:0;right:0;top:700px">
      <span class="sm" style="font-size:60px">like</span>
      <span id="p7d-this" class="xb" style="font-size:300px;line-height:.95">this.</span>
    </div>
  </div>""")
for k, sub_id in enumerate(["p7a", "p7b", "p7c", "p7d"]):
    js.append(f"tl.fromTo('#{sub_id}', {{opacity:1, xPercent:100}}, {{xPercent:0, duration:.18, ease:'power3.out'}}, {cuts[k] - (0.08 if k else 0):.3f});")
    if k < 3:
        js.append(f"tl.fromTo('#{sub_id}', {{xPercent:0}}, {{xPercent:-40, opacity:0, duration:.18, ease:'power3.in', immediateRender:false}}, {cuts[k + 1] - 0.08:.3f});")
    sfx.append(("tick_002", cuts[k], 0.32))
for k in range(7):
    d = 1 if k % 2 else -1
    js.append(f"tl.fromTo('#p7a-r{k}', {{x:{-300 * d - 200}}}, {{x:{300 * d - 200}, duration:{cuts[1] - cuts[0] + 0.2:.3f}, ease:'none'}}, {cuts[0]:.3f});")
js.append(f"tl.fromTo('#p7a', {{scale:1.25}}, {{scale:1, duration:.4, ease:'expo.out'}}, {cuts[0]:.3f});")
js.append(f"tl.fromTo('#p7b-word', {{x:-520}}, {{x:0, duration:.32, ease:'expo.out'}}, {cuts[1]:.3f});")
js.append(f"tl.fromTo('#p7b .speed i', {{x:900}}, {{x:-1400, duration:.45, stagger:.02, ease:'none'}}, {cuts[1]:.3f});")
js.append(f"tl.fromTo('#p7c .shape', {{scale:0, rotation:-90, transformOrigin:'50% 50%'}}, {{scale:1, rotation:0, duration:.3, stagger:.04, ease:'back.out(2)'}}, {cuts[2]:.3f});")
js.append(f"tl.fromTo('#p7c-word', {{scale:1.3, filter:'blur(10px)'}}, {{scale:1, filter:'blur(0px)', duration:.25, ease:'expo.out'}}, {cuts[2]:.3f});")
js.append(f"tl.fromTo('#p7d-this', {{scale:3.2, opacity:0, filter:'blur(24px)'}}, {{scale:1, opacity:1, filter:'blur(0px)', duration:.32, ease:'expo.out'}}, {t(122) - 0.08:.3f});")
js.append(f"tl.fromTo('#p7d-stack', {{scale:1}}, {{scale:1.12, duration:{CLIFF - t(122):.3f}, ease:'power2.in'}}, {t(122):.3f});")
sfx += [("riser", CLIFF - 0.88, 0.55), ("boom", CLIFF - 0.02, 0.6)]

# P_info — "it can only do as much information as you give it." inputs stream into Claude and fill the output ring
si, ei = t(137) - 0.06, t(149) - 0.05
import math as _mi
inputs = ["prompt", "footage", "style", "goal", "length", "captions", "music", "fonts", "pacing", "hook", "b-roll", "format"]
CX, CY = 540, 1090
chips, lines, packets, PL = "", "", "", []
for k, name in enumerate(inputs):
    a = -_mi.pi / 2 + k * 2 * _mi.pi / len(inputs)
    x, y = CX + 390 * _mi.cos(a), CY + 330 * _mi.sin(a)
    chips += f'<span class="nchip" id="pn-c{k}" style="left:{x:.0f}px;top:{y:.0f}px">{name}</span>'
    x0, y0 = CX + 120 * _mi.cos(a), CY + 120 * _mi.sin(a)
    L = _mi.hypot(x - x0, y - y0)
    PL.append(L)
    lines += f'<path class="nline" id="pn-l{k}" d="M{x:.0f} {y:.0f} L{x0:.0f} {y0:.0f}" style="stroke-dasharray:{L:.0f};stroke-dashoffset:{L:.0f}"/>'
    packets += f'<path class="npkt" id="pn-p{k}" d="M{x:.0f} {y:.0f} L{x0:.0f} {y0:.0f}" style="stroke-dasharray:10 {L + 40:.0f};stroke-dashoffset:{L + 10:.0f}"/>'
scene("pi", si, ei, f"""
  <div class="dotgrid"></div>
  <i class="xmark" style="left:60px;top:640px"></i><i class="xmark" style="right:60px;top:640px"></i>
  <i class="xmark" style="left:60px;top:1500px"></i><i class="xmark" style="right:60px;top:1500px"></i>
  <div class="stack" style="left:0;right:0;top:250px">
    <span id="pi-lead" class="sm" style="font-size:52px">it can only do as much</span>
    <div class="mask"><span id="pi-info" class="xb" style="font-size:136px;line-height:1.02">information</span></div>
    <span id="pi-give" class="ital" style="font-size:88px;margin-top:-4px">as you give it.</span>
  </div>
  <div class="ncount" style="left:84px;top:668px"><span class="note">inputs</span><span id="pi-n" class="xb" style="font-size:64px;line-height:1">0</span></div>
  <div class="ncount" style="right:84px;top:668px;align-items:flex-end"><span class="note">output</span><span id="pi-q" class="xb" style="font-size:64px;line-height:1">0%</span></div>
  <svg class="burst" width="1080" height="1920">{lines}{packets}
    <circle cx="{CX}" cy="{CY}" r="150" class="nring-t"/><circle id="pi-ring" cx="{CX}" cy="{CY}" r="150" class="nring"/></svg>
  {chips}
  <div id="pi-node" class="inode" style="left:{CX - 90}px;top:{CY - 90}px;width:180px;height:180px"><img src="assets/img/claude-mark.svg" style="width:100px;height:100px"/></div>""")
js.append(f"tl.fromTo('#pi .dotgrid, #pi .xmark, #pi .ncount', {{opacity:0}}, {{opacity:1, duration:.4, stagger:.04}}, {si + 0.05:.3f});")
js.append(f"tl.fromTo('#pi-lead', {{opacity:0, filter:'blur(12px)'}}, {{opacity:1, filter:'blur(0px)', duration:.3}}, {si + 0.05:.3f});")
js.append(f"tl.fromTo('#pi-node', {{opacity:0, scale:.3}}, {{opacity:1, scale:1, duration:.5, ease:'back.out(1.8)'}}, {si + 0.15:.3f});")
span = t(146) - si - 0.35
step = span / len(inputs)
for k in range(len(inputs)):
    at = si + 0.3 + k * step
    js.append(f"tl.fromTo('#pn-c{k}', {{opacity:0, scale:.5, xPercent:-50, yPercent:-50}}, {{opacity:1, scale:1, xPercent:-50, yPercent:-50, duration:.3, ease:'back.out(2)'}}, {at:.3f});")
    js.append(f"tl.to('#pn-l{k}', {{strokeDashoffset:0, duration:.3, ease:'power2.out', immediateRender:false}}, {at + 0.05:.3f});")
    js.append(f"tl.fromTo('#pn-p{k}', {{strokeDashoffset:{PL[k] + 10:.0f}}}, {{strokeDashoffset:-10, duration:.5, repeat:{max(1, int((ei - at - 0.4) / 0.5))}, ease:'none'}}, {at + 0.3:.3f});")
js.append(f"(function(){{ const o = {{v:0}}; tl.fromTo(o, {{v:0}}, {{v:{len(inputs)}, duration:{span:.3f}, ease:'none', onUpdate(){{ document.getElementById('pi-n').textContent = String(Math.round(o.v)); }}}}, {si + 0.3:.3f}); }})();")
js.append(f"(function(){{ const o = {{v:0}}; tl.fromTo(o, {{v:0}}, {{v:100, duration:{span + 0.3:.3f}, ease:'power1.inOut', onUpdate(){{ document.getElementById('pi-q').textContent = Math.round(o.v) + '%'; }}}}, {si + 0.35:.3f}); }})();")
js.append(f"tl.fromTo('#pi-ring', {{strokeDashoffset:943}}, {{strokeDashoffset:0, duration:{span + 0.3:.3f}, ease:'power1.inOut'}}, {si + 0.35:.3f});")
js.append(f"tl.fromTo('#pi-info', {{yPercent:150, opacity:0}}, {{yPercent:0, opacity:1, duration:.45, ease:'expo.out'}}, {t(143) - 0.08:.3f});")
rev("#pi-give", t(144) - 0.05, y=20)
js.append(f"tl.fromTo('#pi-node', {{scale:1}}, {{scale:1.12, duration:.18, yoyo:true, repeat:1, ease:'power2.out', immediateRender:false}}, {t(146):.3f});")
sfx += [("tick_002", si + 0.3 + k * step, 0.18) for k in range(0, len(inputs), 3)] + [("pluck_001", si + 0.15, 0.25), ("maximize_006", t(146) - 0.1, 0.28)]

# P8 — PROMPT 1 (install)
P1_LINES = [
    "Install the video editing skills from",
    '<span class="url">https://github.com/Jackd0127-dev/video-editing</span>',
    "Clone the repo, copy every folder in skills/ into ~/.claude/skills/,",
    "install HyperFrames and ffmpeg if they're missing,",
    "then list the editing styles you installed.",
]
s8 = t(155) - 0.06
lines8 = "".join(f'<div class="pl" id="p8-l{k}">{ln}</div>' for k, ln in enumerate(P1_LINES))
scene("p8", s8, t(172) - 0.06, f"""
  <div class="stack" style="left:80px;top:250px;align-items:flex-start">
    <div class="row" style="align-items:baseline;gap:22px">
      <span id="p8-paste" class="xb" style="font-size:100px">paste</span>
      <span id="p8-this" class="ital" style="font-size:108px;white-space:nowrap">this prompt.</span>
    </div>
  </div>
  <div id="p8-win" class="win" style="top:560px">
    <div class="bar-top"><i></i><i></i><i></i><span class="wt">Claude Code</span><span id="p8-copy" class="copy">Copy</span><span id="p8-copied" class="copy done">Copied &#10003;</span></div>
    <div class="pbody">{lines8}</div>
  </div>
  <div class="stack" style="left:80px;right:80px;top:1270px;align-items:flex-start">
    <div class="row" style="align-items:baseline;gap:16px">
      <span id="p8-the" class="sm">the</span>
      <span id="p8-src" class="xb" style="font-size:96px">source code</span>
    </div>
    <div class="row" style="align-items:baseline;gap:16px;margin-top:2px">
      <span id="p8-for" class="sm">for all the</span>
      <span id="p8-styles" class="ital" style="font-size:104px;color:{RED}">editing styles</span>
    </div>
  </div>""")
rev("#p8-paste", s8 + 0.04, y=20)
rev("#p8-this", t(155) - 0.02, y=24)
js.append(f"tl.fromTo('#p8-win', {{opacity:0, y:90, scale:.96}}, {{opacity:1, y:0, scale:1, duration:.45, ease:'power3.out'}}, {s8 + 0.08:.3f});")
js.append(f"tl.fromTo('#p8-win .pl', {{opacity:0, y:14, filter:'blur(8px)'}}, {{opacity:1, y:0, filter:'blur(0px)', duration:.32, stagger:.09, ease:'power2.out'}}, {s8 + 0.3:.3f});")
js.append(f"tl.set('#p8-copy', {{opacity:0}}, {t(160):.3f}); tl.fromTo('#p8-copied', {{opacity:0, scale:.8}}, {{opacity:1, scale:1, duration:.2, ease:'back.out(2)'}}, {t(160):.3f});")
rev("#p8-the", t(159) - 0.04, y=10)
rev("#p8-src", t(160) - 0.04, y=20)
rev("#p8-for", t(162) - 0.04, y=10)
rev("#p8-styles", t(165) - 0.04, y=20)
sfx += [("maximize_006", s8 + 0.08, 0.3), ("select_002", t(160), 0.45)]

# P9 — "a nice cinematic style video, to a dramatic, eye-catching, bold video" on the live footage
s9a, s9b, e9 = t(172) - 0.06, t(181) - 0.06, SEGS[18]["start"]
style_windows = [(s9a, e9)]
GRADE_CINE = "contrast(1.3) saturate(0.62) brightness(0.84) sepia(0.32) hue-rotate(-12deg)"
GRADE_HTML = ''
STYLE_HTML = f"""
<div id="st-cine" class="clip" data-start="{s9a:.3f}" data-duration="{s9b - s9a + 0.5:.3f}" data-track-index="6" style="position:absolute;inset:0">
  <div class="stack" style="left:0;right:0;top:300px">
    <span class="cl" style="font-size:46px">{" ".join(f'<span class="w cs" id="st-w{k}">{w}</span>' for k, w in enumerate(["all", "the", "way", "from", "a", "nice"]))}</span>
    <span id="st-c-title" class="ital" style="font-size:130px;line-height:1;color:#f6f1ea;text-shadow:0 8px 34px rgba(0,0,0,.55)">cinematic</span>
    <span id="st-c-sub" class="w cs" style="margin-top:6px">style video</span>
  </div>
</div>
<div id="st-bold" class="clip" data-start="{s9b:.3f}" data-duration="{e9 - s9b:.3f}" data-track-index="6" style="position:absolute;inset:0">
  <div id="st-b1" class="bblock light" style="left:70px;top:250px">DRAMATIC</div>
  <div id="st-b2" class="bblock dark" style="right:70px;top:360px">EYE-CATCHING</div>
  <span id="st-b-bold" class="xb" style="position:absolute;left:0;right:0;top:450px;text-align:center;font-size:240px;line-height:1;color:#fff;text-shadow:0 16px 50px rgba(0,0,0,.5)">BOLD</span>
  <div class="bchart" style="right:70px;top:1180px">{"".join(f'<i id="st-bar{k}" style="height:{h}px"></i>' for k, h in enumerate([90, 150, 230, 320]))}</div>
</div>"""
for k, wi in enumerate([172, 173, 174, 175, 176, 177]):
    js.append(f"word('#st-w{k}', {t(wi) - 0.05:.3f});")
rev("#st-c-sub", t(179) - 0.05, y=8)
js.append(f"tl.fromTo('#st-c-title', {{opacity:0, filter:'blur(14px)'}}, {{opacity:1, filter:'blur(0px)', duration:.6, ease:'power2.out'}}, {t(178) - 0.1:.3f});")
js.append(f"tl.to('#st-cine .stack', {{opacity:0, duration:.25, immediateRender:false}}, {s9b:.3f});")
js.append(f"tl.fromTo('#st-b1', {{xPercent:-130, rotation:-8}}, {{xPercent:0, rotation:-3, duration:.4, ease:'expo.out'}}, {t(183) - 0.08:.3f});")
js.append(f"tl.fromTo('#st-b2', {{xPercent:130, rotation:8}}, {{xPercent:0, rotation:2, duration:.4, ease:'expo.out'}}, {t(184) - 0.08:.3f});")
js.append(f"tl.fromTo('#st-b-bold', {{opacity:0, scale:1.8, filter:'blur(16px)'}}, {{opacity:1, scale:1, filter:'blur(0px)', duration:.35, ease:'expo.out'}}, {t(185) - 0.05:.3f});")
js.append(f"tl.fromTo('.bchart i', {{scaleY:0}}, {{scaleY:1, duration:.45, stagger:.07, ease:'back.out(1.6)'}}, {t(184) - 0.05:.3f});")
sfx += [("fast-whoosh", s9a - 0.3, 0.3), ("arrow-whoosh", s9b - 0.1, 0.3), ("drop_002", t(183), 0.3), ("drop_002", t(184), 0.3), ("dry-pop-alert", t(185), 0.26)]

# P10 — "Next, I want you to drag in all your raw footage.": file icons carried into the chat, then upload
s10, e10 = SEGS[19]["start"], SEGS[20]["start"]
files = ["clip_01.mov", "clip_02.mov", "clip_03.mov"]
file_html = "".join(f'<div class="ficon" id="p10-f{k}" style="left:{380 + k * 210}px;top:{660 + (k % 2) * 30}px"><div class="fbody"><i class="fstrip"></i><i class="fplay"></i><i class="fstrip b"></i></div><span class="fname">{n}</span></div>' for k, n in enumerate(files))
chip_html = "".join(f'<div class="achip" id="p10-a{k}"><i class="fmini"></i><span>{n}</span><i class="aprog"><i id="p10-ap{k}"></i></i></div>' for k, n in enumerate(files))
scene("p10", s10, e10, f"""
  <div class="stack" style="left:90px;top:250px;align-items:flex-start">
    <span id="p10-next" class="sm" style="font-size:56px">{" ".join(f'<span class="ch" id="p10-w{k}">{w}</span>' for k, w in enumerate(["next,", "i", "want", "you", "to"]))}</span>
    <div class="mask"><span id="p10-drag" class="xb" style="font-size:136px;line-height:1">drag in</span></div>
    <span id="p10-raw" class="ital" style="font-size:120px;margin-top:-10px">raw footage.</span>
  </div>
  <div id="p10-box" class="composer" style="top:1150px">
    <span id="p10-ph" class="ph">Message Claude…</span>
    <div class="achips">{chip_html}</div>
    <i id="p10-send" class="send">&#8593;</i>
  </div>
  <div id="p10-files">{file_html}</div>
  <div id="p10-cursor" class="cursor"><svg viewBox="0 0 24 24"><path d="M5 3 L5 19 L9 15 L12 22 L15 20.5 L11.5 14 L18 14 Z" fill="#fff" stroke="#141414" stroke-width="1.4" stroke-linejoin="round"/></svg></div>""")
for k, wi in enumerate([201, 202, 203, 204, 205]):
    js.append(f"tl.fromTo('#p10-w{k}', {{opacity:0, y:14, filter:'blur(10px)'}}, {{opacity:1, y:0, filter:'blur(0px)', duration:.25, ease:'power2.out'}}, {t(wi) - 0.05:.3f});")
js.append(f"tl.fromTo('#p10-drag', {{yPercent:150, opacity:0}}, {{yPercent:0, opacity:1, duration:.45, ease:'expo.out'}}, {t(206) - 0.08:.3f});")
rev("#p10-raw", t(210) - 0.05, y=24)
js.append(f"tl.fromTo('#p10-files .ficon', {{opacity:0, y:50, rotation:0}}, {{opacity:1, y:0, rotation:(i) => [-7, 0, 7][i], duration:.4, stagger:.07, ease:'back.out(1.6)'}}, {s10 + 0.1:.3f});")
js.append(f"tl.fromTo('#p10-box', {{opacity:0, y:50}}, {{opacity:1, y:0, duration:.4, ease:'power3.out'}}, {s10 + 0.15:.3f});")
grab, drop = t(206) - 0.05, t(210) + 0.05
js.append(f"tl.fromTo('#p10-cursor', {{x:1000, y:1500, opacity:0}}, {{x:680, y:800, opacity:1, duration:{grab - s10 - 0.3:.3f}, ease:'power2.inOut'}}, {s10 + 0.3:.3f});")
js.append(f"tl.to('#p10-cursor', {{scale:.86, duration:.1, immediateRender:false}}, {grab:.3f});")
js.append(f"tl.to('#p10-files', {{scale:1.06, duration:.15, immediateRender:false}}, {grab + 0.04:.3f});")
js.append(f"tl.to('#p10-cursor', {{x:430, y:1235, duration:{drop - grab - 0.25:.3f}, ease:'power2.inOut', immediateRender:false}}, {grab + 0.22:.3f});")
js.append(f"tl.to('#p10-files', {{x:-300, y:430, scale:.55, duration:{drop - grab - 0.25:.3f}, ease:'power2.inOut', immediateRender:false}}, {grab + 0.22:.3f});")
js.append(f"tl.to('#p10-files', {{opacity:0, scale:.3, duration:.18, ease:'power2.in', immediateRender:false}}, {drop - 0.02:.3f});")
js.append(f"tl.to('#p10-cursor', {{scale:1, duration:.1, immediateRender:false}}, {drop:.3f}); tl.to('#p10-cursor', {{x:1000, y:1600, opacity:0, duration:.45, ease:'power2.in', immediateRender:false}}, {drop + 0.2:.3f});")
js.append(f"tl.set('#p10-ph', {{opacity:0}}, {drop:.3f}); tl.fromTo('#p10-box .achip', {{opacity:0, y:20, scale:.9}}, {{opacity:1, y:0, scale:1, duration:.3, stagger:.07, ease:'back.out(1.8)'}}, {drop + 0.05:.3f});")
up_end = e10 - 0.35
js.append(f"tl.fromTo('#p10-box .aprog i', {{scaleX:0}}, {{scaleX:1, duration:{up_end - drop - 0.25:.3f}, stagger:.12, ease:'power1.inOut'}}, {drop + 0.2:.3f});")
js.append(f"tl.fromTo('#p10-send', {{backgroundColor:'rgba(23,18,14,.12)', color:'{MUTED}'}}, {{backgroundColor:'{INK}', color:'#fbf9f5', duration:.25}}, {up_end:.3f});")
sfx += [("click_002", grab, 0.4), ("drop_002", drop, 0.38), ("confirmation_002", up_end, 0.28)]

# P11 — PROMPT 2 (template) + model choice
P2_LINES = [
    'Edit my video using the <b class="fill">clean / cinematic</b> skill.',
    'Footage: <b class="fill">drag your clips in</b>',
    'About: <b class="fill">one line on what the video is</b>',
    'Length: <b class="fill">e.g. 60s</b> · Format: 9:16',
    'Must-haves: <b class="fill">captions / logo / CTA / anything else</b>',
    "Cut retakes and dead air, add captions and motion graphics, and show me a draft before the final render.",
]
s11 = t(227) - 0.06
lines11 = "".join(f'<div class="pl" id="p11-l{k}">{ln}</div>' for k, ln in enumerate(P2_LINES))
scene("p11", s11, SEGS[23]["start"], f"""
  <div class="stack" style="left:80px;top:240px;align-items:flex-start">
    <div class="row" style="align-items:baseline;gap:22px">
      <span id="p11-prompt" class="xb" style="font-size:120px">prompt</span>
      <span id="p11-tpl" class="ital" style="font-size:132px">template</span>
    </div>
  </div>
  <div id="p11-win" class="win" style="top:500px">
    <div class="bar-top"><i></i><i></i><i></i><span class="wt">Claude Code</span></div>
    <div class="pbody">{lines11}</div>
  </div>
  <span id="p11-mlabel" class="caps" style="position:absolute;left:84px;top:1236px">choose a model</span>
  <div id="p11-wheel" class="wheel" style="top:1276px">
    <div class="band"></div>
    <div id="p11-list" class="wlist"><div class="wi" id="p11-w0">Haiku 5.5</div><div class="wi" id="p11-w1">Sonnet 5.5</div><div class="wi" id="p11-w2">Opus 5.5</div></div>
    <span id="p11-pro" class="pro-badge"><img src="assets/img/claude-mark.svg"/>needs Pro plan</span>
  </div>""")
rev("#p11-prompt", t(228) - 0.04, y=20)
rev("#p11-tpl", t(229) - 0.04, y=24)
js.append(f"tl.fromTo('#p11-win', {{opacity:0, y:90, scale:.96}}, {{opacity:1, y:0, scale:1, duration:.45, ease:'power3.out'}}, {s11 + 0.08:.3f});")
js.append(f"tl.fromTo('#p11-win .pl', {{opacity:0, y:14, filter:'blur(8px)'}}, {{opacity:1, y:0, filter:'blur(0px)', duration:.32, stagger:.1, ease:'power2.out'}}, {s11 + 0.3:.3f});")
js.append(f"tl.fromTo('#p11-win .fill', {{backgroundColor:'rgba(23,18,14,0)'}}, {{backgroundColor:'rgba(23,18,14,.08)', duration:.3, stagger:.08}}, {s11 + 1.2:.3f});")
js.append(f"tl.fromTo('#p11-mlabel, #p11-wheel', {{opacity:0, y:40}}, {{opacity:1, y:0, duration:.4, stagger:.06, ease:'power3.out'}}, {t(233) - 0.25:.3f});")
js.append(f"tl.fromTo('#p11-list', {{y:0}}, {{y:-160, duration:.6, ease:'back.out(1.25)'}}, {t(234) - 0.08:.3f});")
js.append(f"tl.fromTo('#p11-w0', {{opacity:1}}, {{opacity:.28, duration:.3, immediateRender:false}}, {t(234) - 0.08:.3f});")
js.append(f"tl.fromTo('#p11-w1', {{opacity:.28}}, {{opacity:.28, duration:.3}}, {t(234) - 0.08:.3f});")
js.append(f"tl.fromTo('#p11-w2', {{opacity:.28}}, {{opacity:1, duration:.3}}, {t(234) + 0.3:.3f});")
js.append(f"tl.fromTo('#p11-pro', {{opacity:0, x:40}}, {{opacity:1, x:0, duration:.35, ease:'power3.out'}}, {t(242) - 0.06:.3f});")
sfx += [("maximize_006", s11 + 0.08, 0.3), ("tick_002", t(234) + 0.05, 0.3), ("tick_002", t(234) + 0.22, 0.3), ("select_002", t(234) + 0.45, 0.4), ("pluck_001", t(242), 0.22)]

# P12 — "Give it 15 to 20 minutes" as a time-lapse clock
import math as _m
ticks = ""
for k in range(60):
    a = _m.radians(k * 6)
    r0 = 236 if k % 5 == 0 else 258
    ticks += f'<line class="{"tk big" if k % 5 == 0 else "tk"}" x1="{350 + r0 * _m.sin(a):.1f}" y1="{350 - r0 * _m.cos(a):.1f}" x2="{350 + 282 * _m.sin(a):.1f}" y2="{350 - 282 * _m.cos(a):.1f}"/>'
wedge = f"M350 350 L{350 + 226 * _m.sin(_m.radians(90)):.1f} {350 - 226 * _m.cos(_m.radians(90)):.1f} A226 226 0 0 1 {350 + 226 * _m.sin(_m.radians(120)):.1f} {350 - 226 * _m.cos(_m.radians(120)):.1f} Z"
s12, e12 = SEGS[23]["start"], t(260) - 0.05
scene("p12", s12, e12, f"""
  <div class="stack" style="left:0;right:0;top:380px"><span id="p12-give" class="sm">give it</span></div>
  <svg id="p12-clock" width="700" height="700" style="position:absolute;left:190px;top:470px;overflow:visible">
    <circle cx="350" cy="350" r="300" class="face"/>
    {ticks}
    <path id="p12-wedge" d="{wedge}" fill="#8f857b" opacity=".9"/>
    <line id="p12-hour" class="hand" x1="350" y1="350" x2="350" y2="200"/>
    <line id="p12-min" class="hand" x1="350" y1="350" x2="350" y2="110"/>
    <line id="p12-sec" class="hand sec" x1="350" y1="380" x2="350" y2="96"/>
    <circle cx="350" cy="350" r="14" fill="{INK}"/>
  </svg>
  <div class="row" style="position:absolute;left:0;right:0;top:1210px;justify-content:center;align-items:baseline;gap:22px">
    <span id="p12-15" class="xb" style="font-size:170px">15</span><span id="p12-20" class="xb" style="font-size:170px">&#8211;20</span>
    <span id="p12-min-w" class="ital" style="font-size:120px;color:{RED}">min</span>
  </div>""")
rev("#p12-give", s12 + 0.04, y=12)
js.append(f"tl.fromTo('#p12-clock', {{opacity:0, scale:.85}}, {{opacity:1, scale:1, duration:.4, ease:'power3.out'}}, {s12:.3f});")
js.append(f"tl.fromTo('#p12-min', {{rotation:0, svgOrigin:'350 350'}}, {{rotation:90, svgOrigin:'350 350', duration:{t(253) + 0.1 - s12:.3f}, ease:'power2.inOut'}}, {s12:.3f});")
js.append(f"tl.to('#p12-min', {{rotation:120, svgOrigin:'350 350', duration:{t(255) + 0.15 - t(253) - 0.1:.3f}, ease:'power2.inOut', immediateRender:false}}, {t(253) + 0.1:.3f});")
js.append(f"tl.fromTo('#p12-hour', {{rotation:0, svgOrigin:'350 350'}}, {{rotation:10, svgOrigin:'350 350', duration:{e12 - s12:.3f}, ease:'none'}}, {s12:.3f});")
js.append(f"tl.fromTo('#p12-sec', {{rotation:0, svgOrigin:'350 350'}}, {{rotation:1440, svgOrigin:'350 350', duration:{e12 - s12:.3f}, ease:'none'}}, {s12:.3f});")
js.append(f"tl.fromTo('#p12-wedge', {{opacity:0, scale:.6, svgOrigin:'350 350'}}, {{opacity:.9, scale:1, svgOrigin:'350 350', duration:.3, ease:'back.out(1.7)'}}, {t(255) - 0.05:.3f});")
js.append(f"tl.fromTo('#p12-15', {{opacity:0, y:30, filter:'blur(12px)'}}, {{opacity:1, y:0, filter:'blur(0px)', duration:.3, ease:'expo.out'}}, {t(253) - 0.05:.3f});")
js.append(f"tl.fromTo('#p12-20', {{opacity:0, x:-30, filter:'blur(12px)'}}, {{opacity:1, x:0, filter:'blur(0px)', duration:.3, ease:'expo.out'}}, {t(255) - 0.05:.3f});")
rev("#p12-min-w", t(256) - 0.05, y=20)
sfx += [("tick_002", t(253), 0.3), ("tick_002", t(255), 0.3), ("dry-pop-alert", t(255), 0.2)]

# P13 — "without needing a whole designer, a video editor or some marketing specialist."
s13 = t(274) - 0.06
e13 = t(289) - 0.05
ICONS = {'designer': '<path d="M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83z"/><path d="M2 12a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 12"/><path d="M2 17a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 17"/>', 'editor': '<path d="m12.296 3.464 3.02 3.956"/><path d="M20.2 6 3 11l-.9-2.4c-.3-1.1.3-2.2 1.3-2.5l13.5-4c1.1-.3 2.2.3 2.5 1.3z"/><path d="M3 11h18v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="m6.18 5.276 3.1 3.899"/>', 'marketing': '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>'}
roles = [("designer", 278, "designer", "layouts · type · colour"), ("editor", 280, "video editor", "cuts · pacing · sound"), ("marketing", 284, "marketing specialist", "hooks · captions · posting")]
rows_html = ""
for k, (ic, wi, title, subtitle) in enumerate(roles):
    rows_html += f'<div class="rrow" id="p13-r{k}" style="top:{560 + k * 230}px"><div class="ribox"><svg viewBox="0 0 24 24" class="rico">{ICONS[ic]}</svg></div><div class="col"><span class="xb" style="font-size:60px;line-height:1">{title}</span><span class="note dim" style="margin-top:12px">{subtitle}</span></div><span class="rnum">0{k + 1}</span></div>'
scene("p13", s13, e13, f"""
  <div class="stack" style="left:0;right:0;top:360px"><span id="p13-lead" class="sm" style="font-size:56px">without needing a whole</span></div>
  {rows_html}
  <div id="p13-claude" class="rrow dark" style="top:790px"><div class="ribox light"><img src="assets/img/claude-mark.svg" style="width:84px;height:84px"/></div><div class="col"><span class="xb" style="font-size:64px;line-height:1;color:#fbf9f5;text-shadow:none">Claude</span><span class="note light" style="margin-top:12px">design · edit · market</span></div></div>""")
rev("#p13-lead", t(274) - 0.03, y=12)
for k, (ic, wi, title, subtitle) in enumerate(roles):
    d = -1 if k % 2 == 0 else 1
    js.append(f"tl.fromTo('#p13-r{k}', {{opacity:0, xPercent:{40 * d}, rotationY:{-35 * d}, transformPerspective:1400}}, {{opacity:1, xPercent:0, rotationY:0, transformPerspective:1400, duration:.55, ease:'expo.out'}}, {t(wi) - 0.1:.3f});")
    js.append(f"tl.fromTo('#p13-r{k} .rico path', {{strokeDashoffset:60}}, {{strokeDashoffset:0, duration:.5, stagger:.06, ease:'power2.out'}}, {t(wi) + 0.1:.3f});")
    sfx.append(("drop_002", t(wi), 0.28))
fold = t(285) + 0.35
for k in range(3):
    js.append(f"tl.to('#p13-r{k}', {{y:{790 - (560 + k * 230)}, scale:.92, opacity:0, duration:.45, ease:'power3.inOut', immediateRender:false}}, {fold + k * 0.05:.3f});")
js.append(f"tl.fromTo('#p13-claude', {{opacity:0, scaleY:.2, scaleX:.9}}, {{opacity:1, scaleY:1, scaleX:1, duration:.5, ease:'back.out(1.5)'}}, {fold + 0.32:.3f});")
sfx += [("fast-whoosh", fold - 0.25, 0.3), ("pluck_001", fold + 0.35, 0.3)]

# P14 — end card "stay tuned for day two.": 30 blocks, only the first lit, held, then a smooth zoom into it
bars14 = "".join(f'<i class="seg" id="p14-s{k}"></i>' for k in range(30))
SEG_W = (900 - 29 * 6) / 30
ZX, ZY = 90 + SEG_W / 2, 1340 - 40 * 1.9 / 2
scene("p14", SEGS[26]["start"], DURATION, f"""
  <div id="p14-zoom" style="position:absolute;inset:0;transform-origin:{ZX:.1f}px {ZY}px">
    <div class="stack" style="left:0;right:0;top:560px">
      <span id="p14-lead" class="sm" style="font-size:56px">stay tuned for</span>
      <div class="row" style="align-items:flex-end;justify-content:center;margin-top:6px">
        <span id="p14-day" class="xb" style="font-size:230px;line-height:1">Day</span>
        <span id="p14-two" class="xb" style="font-size:230px;line-height:1;margin-left:40px">2</span>
      </div>
    </div>
    <span id="p14-lbl" class="note" style="position:absolute;left:90px;top:1186px">day 01 / 30</span>
    <div id="p14-bar" class="bar big" style="top:1300px">{bars14}</div>
  </div>""")
rev("#p14-lead", t(305) - 0.04, y=12)
rev("#p14-day", t(308) - 0.04, y=30)
js.append(f"tl.fromTo('#p14-two', {{opacity:0, scale:1.5, filter:'blur(18px)'}}, {{opacity:1, scale:1, filter:'blur(0px)', duration:.45, ease:'expo.out'}}, {t(309) - 0.04:.3f});")
js.append(f"tl.fromTo('#p14-bar .seg', {{scaleY:0, opacity:0}}, {{scaleY:1, opacity:1, duration:.3, stagger:.014, ease:'power2.out'}}, {t(305):.3f});")
lit = t(309) + 0.45
js.append(f"tl.fromTo('#p14-s0', {{backgroundColor:'rgba(23,18,14,.14)', scaleY:1}}, {{backgroundColor:'{INK}', scaleY:1.9, duration:.5, ease:'back.out(2.2)'}}, {lit:.3f});")
js.append(f"tl.fromTo('#p14-lbl', {{opacity:0, y:12}}, {{opacity:1, y:0, duration:.35, ease:'power2.out'}}, {lit + 0.15:.3f});")
js.append(f"tl.fromTo('#p14-s0', {{scaleY:1.9}}, {{scaleY:2.2, duration:.6, yoyo:true, repeat:1, ease:'sine.inOut', immediateRender:false}}, {lit + 0.6:.3f});")
zoom_at = DURATION - 1.4
js.append(f"tl.to('#p14-lbl', {{opacity:0, duration:.3, immediateRender:false}}, {zoom_at:.3f});")
js.append(f"tl.fromTo('#p14-zoom', {{scale:1, x:0, y:0}}, {{scale:60, x:{540 - ZX:.1f}, y:{960 - ZY:.1f}, duration:1.3, ease:'power3.inOut'}}, {zoom_at:.3f});")
sfx += [("dry-pop-alert", t(309), 0.24), ("pluck_001", lit, 0.3), ("riser", zoom_at + 0.25, 0.35), ("boom", DURATION - 0.12, 0.3)]

# ---------------------------------------------------------------- captions on A-roll
# Each group: (first token, last token, layout) — layout is lines of "style:index" tokens.
# Styles: s small, b bold, i serif italic, r = red accent on top of b/i.
CAPS = [
    [["s:0"], ["br:1", "b:2"]],
    [["s:8", "s:9"], ["n:10"]],
    [["b:17", "b:18"], ["i:19"]],
    [["s:20", "s:21", "s:22"], ["b:23", "b:24"], ["i:25"]],
    [["s:26", "s:27", "s:28"], ["b:29", "b:30"]],
    [["s:31", "s:32", "s:33", "s:34"], ["s:35", "br:36"]],
    [["s:43"], ["s:44", "s:45", "s:46"], ["i:47"]],
    [["s:48"], ["b:49"]],
    [["s:50"], ["i:51", "b:52"]],
    [["s:53", "s:54"], ["b:55"], ["ir:56"]],
    [["s:63", "s:64", "s:65", "s:66", "s:67"], ["b:68", "b:69", "b:70"], ["s:71", "b:72"]],
    [["s:73", "s:74", "s:75"], ["i:76", "i:77", "i:78"]],
    [["s:79", "s:80"], ["br:81", "br:82"]],
    [["s:83", "s:84", "s:85"], ["b:86", "b:87", "b:88"], ["b:89", "i:90", "s:91"]],
    [["s:92"], ["b:93"]],
    [["s:94", "s:95", "s:96"], ["s:97", "s:98", "s:99"], ["b:100"]],
    [["s:101"], ["b:102", "b:103"], ["i:104", "i:105"]],
    [["s:106", "s:107", "s:108"], ["b:109", "b:110"], ["i:111"]],
    [["s:112", "s:113", "s:114"], ["b:115", "b:116"], ["s:117"]],
    [["s:123"], ["b:124"], ["s:125", "s:126", "i:127"]],
    [["s:128", "s:129", "s:130", "s:131"], ["s:132", "s:133"], ["ir:134"]],
    [["s:135", "s:136"], ["s:137", "s:138", "s:139", "s:140"]],
    [["s:148", "s:149", "s:150", "s:151", "s:152", "s:153"], ["b:154"]],
    [["s:187", "s:188", "s:189", "s:190"], ["b:191", "b:192"], ["i:193"]],
    [["s:194", "s:195", "s:196", "s:197", "s:198"], ["b:199", "b:200"]],
    [["s:212", "s:213", "s:214", "s:215", "s:216", "s:217"], ["b:218", "b:219"], ["i:220", "s:221", "s:222", "s:223"]],
    [["s:224", "s:225", "s:226"]],
    [["s:257", "s:258", "s:259", "s:260", "s:261"], ["b:262", "b:263"], ["i:264", "i:265"], ["b:266"]],
    [["s:267", "s:268", "s:269"], ["b:270", "b:271", "b:272"], ["ir:273"]],
    [["s:286", "s:287", "s:288"], ["b:289", "b:290"], ["i:291", "i:292", "i:293"]],
    [["s:294", "s:295"], ["b:296"], ["i:297"]],
    [["s:298", "s:299", "s:300"], ["i:301", "i:302", "ir:303"]],
]

# The A-roll windows (not covered by paper) bound each caption group's end.
paper_windows = [(s[1], s[2]) for s in scenes]


cap_cover = paper_windows + style_windows


def next_cover(at):
    starts = [a for a, b in cap_cover if a > at + 0.01]
    return min(starts) if starts else AROLL_END


cap_html, cap_js = [], []
for g, lines in enumerate(CAPS):
    idx = [int(tok.split(":")[1]) for ln in lines for tok in ln]
    g_start = max(0.0, t(min(idx)) - 0.08)
    for pa, pb in cap_cover:
        if pa - 0.01 <= g_start < pb:
            g_start = pb + 0.01
    nxt = CAPS[g + 1] if g + 1 < len(CAPS) else None
    next_start = t(min(int(x.split(":")[1]) for ln in nxt for x in ln)) - 0.08 if nxt else AROLL_END
    end = min(next_start, next_cover(g_start), t(max(idx)) + 0.75)
    rows = []
    for ln in lines:
        spans = []
        for tok in ln:
            style, i = tok.split(":")
            cls = {"s": "cs", "b": "cb", "i": "ci", "n": "cn"}[style[0]] + (" red" if "r" in style[1:] else "")
            text = TOK[int(i)]["text"]
            if style[0] == "s":
                text = text.lower() if text not in ("I", "I'm", "AI.", "Claude", "Codex,", "Codex.") else text
            logo = '<img class="logo-in" src="assets/img/openai-white.svg"/>' if text.startswith("Codex") else ""
            spans.append(f'<span class="w {cls}" id="w{i}">{logo}{esc(text)}</span>')
        rows.append(f'<div class="cl">{" ".join(spans)}</div>')
    cap_html.append(f'<div class="cap clip" id="cap{g}" data-start="{g_start:.3f}" data-duration="{end - g_start:.3f}" data-track-index="2"><div class="capi">{"".join(rows)}</div></div>')
    for i in idx:
        cap_js.append(f"word('#w{i}', {max(0.0, t(i) - 0.05):.3f});")
    cap_js.append(f"tl.fromTo('#cap{g} .capi', {{opacity:1, filter:'blur(0px)', y:0}}, {{opacity:0, filter:'blur(10px)', y:-10, duration:.12, ease:'power1.in', immediateRender:false}}, {end - 0.12:.3f});")

# ---------------------------------------------------------------- camera: punch-ins per A-roll window
# Split A-roll into windows between paper scenes and at cuts; alternate zoom so jump cuts read as punches.
extra_punch = [t(93), t(29), t(50), t(68), t(73), t(79), t(97), t(101), t(112), t(128), t(135), t(144), t(194), t(218), t(262), t(267), t(289), t(298)]
edges = sorted(set([0.0] + [s["start"] for s in SEGS] + [b for a, b in paper_windows] + [round(x - 0.08, 3) for x in extra_punch]))
edges = [e for e in edges if e < AROLL_END - 0.05] + [AROLL_END]
# Merge edges closer than 0.1s so no window is too short to tween.
merged = []
for e in edges:
    if not merged or e - merged[-1] >= 0.1:
        merged.append(e)
edges = merged[:-1] + [AROLL_END] if merged[-1] != AROLL_END else merged

# Face samples (source time, 2fps) give each window its face box, so the zoom can keep the face
# clear of the caption band and always change size enough at a cut to read as a punch, not a jump.
samples = []
for line in open("edit/faces-source-2fps.txt"):
    p = line.split()
    if p[1] != "none":
        samples.append(((int(p[0][1:5]) - 1) / 2, *map(float, p[1:5])))
CAP_CLEAR = 0.40  # face-box top must stay below this (caption band ends at 0.307; hair sits above the box)
ZOOMS = [1.0, 1.06, 1.12, 1.18, 1.24]
cam_js = []
soft_cuts = []  # visible cuts where the zoom alone can't change enough: hide with a focus pull
prev_size, tight = None, False


def box_near(t0, t1):
    win = [f for f in samples if t0 <= f[0] <= t1]
    return win


for a, b in zip(edges, edges[1:]):
    covered = any(pa - 0.01 <= a and b <= pb + 0.01 for pa, pb in paper_windows)
    seg = max((s for s in SEGS if s["start"] <= a + 0.001), key=lambda s: s["start"])
    src_a, src_b = seg["src_in"] + a - seg["start"], seg["src_in"] + b - seg["start"]
    win = box_near(src_a - 0.3, src_b + 0.3) or [(0, 0.4, 0.45, 0.3, 0.2)]
    head = box_near(src_a - 0.3, src_a + 0.6) or win
    tail = box_near(src_b - 0.6, src_b + 0.3) or win
    cx = sum(f[1] + f[3] / 2 for f in win) / len(win)
    cy = sum(f[2] + f[4] / 2 for f in win) / len(win)
    top = min(f[2] for f in win)
    w_head = sum(f[3] for f in head) / len(head)
    w_tail = sum(f[3] for f in tail) / len(tail)
    zmax = max(1.0, (cy - CAP_CLEAR) / max(cy - top, 1e-3) / 1.025)
    options = [z for z in ZOOMS if z <= zmax + 1e-6] or [1.0]
    if covered or prev_size is None:
        z = options[0] if not tight else options[-1]
    else:
        def score(z):
            r = w_head * z / prev_size
            change = abs(r - 1)
            return (change >= 0.14, (r > 1) == (not tight), -abs(change - 0.2))
        z = max(options, key=score)
    if not covered and prev_size is not None and abs(w_head * z / prev_size - 1) < 0.14:
        soft_cuts.append(a)
    if not covered:
        prev_size, tight = w_tail * z * 1.025, z >= 1.12
    ox, oy = int(cx * 1080), int(cy * 1920)
    if a == 0:
        cam_js.append(f"tl.fromTo('#cam', {{scale:1.3, transformOrigin:'{ox}px {oy}px'}}, {{scale:{z}, duration:.45, ease:'expo.out'}}, 0);")
        cam_js.append(f"tl.fromTo('#cam', {{scale:{z}}}, {{scale:{z * 1.025:.4f}, duration:{b - a - 0.45:.3f}, ease:'none', immediateRender:false}}, .45);")
        continue
    cam_js.append(f"tl.fromTo('#cam', {{scale:{z}, transformOrigin:'{ox}px {oy}px'}}, {{scale:{z * 1.025:.4f}, duration:{b - a:.3f}, ease:'none', immediateRender:false}}, {a:.3f});")

# Transitions back to A-roll: alternate invert flash and focus pull.
back_js = []
for n, (sid, a, b_end, _) in enumerate(scenes):
    if b_end >= AROLL_END - 0.01 or any(abs(b_end - s2[1]) < 0.02 for s2 in scenes):
        continue
    back_js.append(f"tl.fromTo('#{sid}', {{opacity:1}}, {{opacity:0, duration:.42, ease:'sine.inOut', immediateRender:false}}, {b_end - 0.42:.3f});")
    back_js.append(f"tl.fromTo('#{sid} .sheet', {{scale:1, filter:'blur(0px)'}}, {{scale:1.03, filter:'blur(10px)', duration:.42, ease:'sine.inOut', immediateRender:false}}, {b_end - 0.42:.3f});")

cut_starts = [s["start"] for s in SEGS[1:]]
# Cuts the last render's QA measured as same-size jumps also get a focus pull.
import os as _os
if _os.path.exists("edit/qa-latest.json"):
    soft_cuts += [j for j in json.load(open("edit/qa-latest.json"))["jumps"] if not any(abs(j - x) < 0.05 for x in soft_cuts)]
for a in soft_cuts:
    is_source_cut = any(abs(a - c) < 0.02 for c in cut_starts)
    in_style = any(sa + 0.05 < a < se - 0.05 for sa, se in style_windows)
    if is_source_cut and not in_style and not any(abs(a - s[2]) < 0.05 for s in scenes):
        back_js.append(f"focus({a:.3f});")

# ---------------------------------------------------------------- audio
sfx_html = []
for n, (name, at, vol) in enumerate(sorted(sfx, key=lambda x: x[1])):
    sfx_html.append(f'<audio id="sfx{n}" src="assets/audio/sfx/{name}.wav" data-start="{at:.3f}" data-track-index="{20 + n}" data-volume="{vol}"></audio>')

# ---------------------------------------------------------------- assemble
scene_html = []
for sid, a, b, body in scenes:
    scene_html.append(f"""<section class="scene clip" id="{sid}" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="3">
 <div class="sheet"><img class="paper" src="assets/img/paper-clean.jpg"/>
  <div class="content">{body}
  </div>
 </div>
</section>""")

ambient_js = []

page = open("edit/template.html").read()
page = (page.replace("{{DURATION}}", f"{DURATION:.3f}")
        .replace("{{AROLL_END}}", f"{AROLL_END:.3f}")
        .replace("{{SCENES}}", "\n".join(scene_html))
        .replace("{{CAPTIONS}}", "\n".join(cap_html) + STYLE_HTML)
        .replace("{{GRADE_LAYER}}", GRADE_HTML)
        .replace("{{SFX}}", "\n".join(sfx_html))
        .replace("{{JS}}", "\n".join(cam_js + back_js + ambient_js + js + cap_js))
        .replace("{{GRADE}}", GRADE)
        .replace("{{INK}}", INK).replace("{{PAPER}}", PAPER).replace("{{RED}}", RED).replace("{{MUTED}}", MUTED))
open("index.html", "w").write(page)
print(f"index.html: {len(scenes)} scenes, {len(CAPS)} caption groups, {len(sfx)} sfx, duration {DURATION:.2f}s")

# Music cuts out under the cliffhanger and comes back after the hit.
import subprocess as _sp
_cl = CLIFF
_sp.run(["ffmpeg", "-v", "error", "-y", "-i", "assets/audio/bgm/bed.wav", "-af",
         f"volume='if(between(t,{_cl - 0.75:.3f},{_cl + 0.1:.3f}),0.08,if(between(t,{_cl + 0.1:.3f},{_cl + 1.1:.3f}),0.08+0.92*(t-{_cl + 0.1:.3f}),1))':eval=frame",
         "assets/audio/bgm/bed-cliff.wav"], check=True)

# Carve the music bed around the voice (writes EQ + level lanes onto #bgm).
import subprocess
import os
subprocess.run(["node", os.path.expanduser("~/.claude/skills/hyperframes-audio/scripts/carve.mjs"),
                "--comp", "index.html", "--bed", "bgm", "--voice", "aroll"], check=True)
