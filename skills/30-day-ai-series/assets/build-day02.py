"""Day 2 — "sketch to website" (approved v4). Multi-take cut, no music bed, real-site screenshots. Generates index.html from the multi-take cut (edit/words.json),
caption tokens (edit/tokens.json), b-roll list (edit/broll.json) and face samples on the cut.
Run from the project root:  python3 -I edit/build.py
"""
import html
import json
import math
import os
import re
import subprocess

TOK = json.load(open("edit/tokens.json"))
TOK[3]["text"] = "nah,"
TOK[216]["text"] = "20"
SEGS = json.load(open("edit/words.json"))["segments"]
BROLL = json.load(open("edit/broll.json"))
AROLL_END = SEGS[-1]["end"]
DURATION = round(AROLL_END + 3.0, 3)

INK, PAPER, RED, MUTED = "#17120e", "#ede7df", "#17120e", "#7a6e63"
GRADE = ""  # footage stays exactly as shot (Apple HDR->SDR conversion, no grade)


def t(i):
    return TOK[i]["start"]


def esc(s):
    return html.escape(s, quote=True)


scenes, js, sfx = [], [], []


def scene(sid, start, end, body, whoosh=True):
    start = math.floor(start * 30 + 1e-6) / 30 - 0.002  # land on a frame, never one frame late
    scenes.append((sid, start, end, body))
    js.append(f"enter('#{sid}', {start:.3f});")
    if whoosh:
        sfx.append(("fast-whoosh", max(0, start - 0.32), 0.36))


def rev(sel, at, **o):
    js.append(f"rev('{sel}', {at:.3f}, {json.dumps(o)});")


def words_in(sel_prefix, words, idxs):
    """Lead-in words that appear one by one with his voice."""
    spans = " ".join(f'<span class="ch" id="{sel_prefix}{k}">{w}</span>' for k, w in enumerate(words))
    for k, i in enumerate(idxs):
        js.append(f"tl.fromTo('#{sel_prefix}{k}', {{opacity:0, y:14, filter:'blur(10px)'}}, {{opacity:1, y:0, filter:'blur(0px)', duration:.25, ease:'power2.out'}}, {t(i) - 0.05:.3f});")
    return spans


SEG_W = (900 - 29 * 6) / 30
BLOCKS = "".join(f'<i class="seg" id="{{p}}-s{k}"></i>' for k in range(30))

# ---------------------------------------------------------------- P1 "This is day two of 30" — stat page
assert SEGS[3]["label"].startswith("this is day two")
s, e = SEGS[3]["start"] - 0.02, t(24) + 0.36  # cover the new take from its first frame
scene("p1", s, e, f"""
  <div class="stack" style="left:0;right:0;top:600px">
    <span class="sm" style="font-size:56px">{words_in('p1w', ['this', 'is'], [18, 19])}</span>
    <div class="row" style="align-items:flex-end;justify-content:center;margin-top:10px">
      <span id="p1-day" class="xb" style="font-size:230px;line-height:1">Day</span>
      <span id="p1-two" class="xb" style="font-size:230px;line-height:1;margin-left:40px">2</span>
    </div>
    <span class="sm" style="font-size:56px;margin-top:22px">{words_in('p1o', ['of', '30'], [22, 23])}</span>
  </div>
  <div id="p1-bar" class="bar big" style="top:1250px">{BLOCKS.replace('{p}', 'p1')}</div>""")
js.append(f"tl.fromTo('#p1-day', {{opacity:0, y:60, filter:'blur(14px)'}}, {{opacity:1, y:0, filter:'blur(0px)', duration:.4, ease:'expo.out'}}, {t(20) - 0.05:.3f});")
js.append(f"tl.fromTo('#p1-two', {{opacity:0, scale:1.5, filter:'blur(18px)'}}, {{opacity:1, scale:1, filter:'blur(0px)', duration:.4, ease:'expo.out'}}, {t(21) - 0.05:.3f});")
js.append(f"tl.fromTo('#p1-bar .seg', {{scaleY:0, opacity:0}}, {{scaleY:1, opacity:1, duration:.22, stagger:.01, ease:'power2.out'}}, {t(21):.3f});")
js.append(f"tl.fromTo('#p1-s0', {{backgroundColor:'rgba(23,18,14,.14)'}}, {{backgroundColor:'{INK}', duration:.15}}, {t(21) + 0.25:.3f});")
js.append(f"tl.fromTo('#p1-s1', {{backgroundColor:'rgba(23,18,14,.14)', scaleY:1}}, {{backgroundColor:'{INK}', scaleY:1.9, duration:.45, ease:'back.out(2.2)'}}, {t(23):.3f});")
sfx += [("dry-pop-alert", t(21), 0.24), ("pluck_001", t(23), 0.26)]

# ---------------------------------------------------------------- P2 "rough sketch into a fully working website" — sketch wipes into the site
s, e = t(34) - 0.06, t(45) + 0.15
scene("p2", s, e, f"""
  <div class="stack" style="left:0;right:0;top:380px"><span class="sm" style="font-size:52px">{words_in('p2w', ["today", "we're", "turning", "a"], [34, 35, 36, 37])}</span></div>
  <div id="p2-card" class="pcard" style="top:510px">
    <img src="assets/img/sketch-crop.jpg" class="pimg"/>
    <div id="p2-site" class="pwipe"><img src="assets/img/site-hero.jpg" class="pimg" style="object-position:50% 0%"/></div>
    <i id="p2-scan" class="scan"></i>
  </div>
  <div class="stack" style="left:0;right:0;top:1140px;height:160px">
    <span id="p2-l1" class="ital lbl" style="font-size:88px">rough sketch</span>
    <span id="p2-l2" class="xb lbl" style="font-size:84px">fully working website</span>
  </div>""")
js.append(f"tl.fromTo('#p2-card', {{opacity:0, y:50, scale:.95}}, {{opacity:1, y:0, scale:1, duration:.5, ease:'power3.out'}}, {s + 0.08:.3f});")
rev("#p2-l1", t(38) - 0.05, y=26)
w0 = t(40) - 0.05
js.append(f"tl.fromTo('#p2-site', {{clipPath:'inset(0% 100% 0% 0%)'}}, {{clipPath:'inset(0% 0% 0% 0%)', duration:.95, ease:'power2.inOut'}}, {w0:.3f});")
js.append(f"tl.fromTo('#p2-scan', {{x:0, opacity:1}}, {{x:900, duration:.95, ease:'power2.inOut'}}, {w0:.3f}); tl.to('#p2-scan', {{opacity:0, duration:.1, immediateRender:false}}, {w0 + 0.95:.3f});")
js.append(f"tl.to('#p2-l1', {{opacity:0, y:-20, filter:'blur(10px)', duration:.25, immediateRender:false}}, {t(41) - 0.1:.3f});")
rev("#p2-l2", t(42) - 0.05, y=26)
sfx += [("arrow-whoosh", w0, 0.3), ("dry-pop-alert", t(43), 0.2)]

# ---------------------------------------------------------------- P3 "you need a designer, a developer, or hours in a website builder. You don't."
# Three live mini apps pile up as he lists them (a design canvas, a code editor, a drag-and-drop builder
# with a running clock), then all three drop off the page on "You don't."
s, e = t(56) - 0.12, t(68) + 0.4
AB = [("nav", 16, 14, 348, 22, "rgba(23,18,14,.85)"), ("h1", 16, 54, 196, 28, "rgba(23,18,14,.78)"), ("p1", 16, 94, 168, 10, "rgba(23,18,14,.18)"),
      ("p2", 16, 112, 140, 10, "rgba(23,18,14,.18)"), ("img", 228, 54, 136, 92, "#ffd83d"), ("c1", 16, 170, 108, 98, "#ff9ed6"),
      ("c2", 136, 170, 108, 98, "#cfc6e6"), ("c3", 256, 170, 108, 98, "#a3de4e")]
ab = "".join(f'<b class="abk" id="p3-ab-{n}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{c}"></b>' for n, x, y, w, h, c in AB)
CODE = [
    '<em class="sx-t">&lt;nav</em> <em class="sx-a">class</em>=<em class="sx-s">"menu"</em><em class="sx-t">&gt;</em>',
    '&nbsp;&nbsp;<em class="sx-t">&lt;a</em> <em class="sx-a">href</em>=<em class="sx-s">"#about"</em><em class="sx-t">&gt;</em>About<em class="sx-t">&lt;/a&gt;</em>',
    '<em class="sx-t">&lt;/nav&gt;</em>',
    '<em class="sx-t">.hero</em> { <em class="sx-a">display</em>: grid;',
    '&nbsp;&nbsp;<em class="sx-a">gap</em>: <em class="sx-s">32px</em>; }',
    '<em class="sx-t">export default</em> <em class="sx-a">Cafe</em>()',
]
CODE_LEN = [17, 31, 6, 23, 16, 22]
code = "".join(f'<div class="cln"><u>{k + 1}</u><span class="cty" id="p3-c{k}">{ln}</span></div>' for k, ln in enumerate(CODE))
SIDE = "".join(f'<div class="bsi"><i style="background:{c}"></i><b></b></div>' for c in ("rgba(23,18,14,.75)", "#ffd83d", "#ff9ed6", "#cfc6e6"))
scene("p3", s, e, f"""
  <div class="stack" style="left:0;right:0;top:215px"><span class="sm" style="font-size:52px">most people think you need</span></div>
  <div class="mw" id="p3-a" style="left:58px;top:360px">
    <div class="mwh"><i></i><i></i><i></i><span class="mwt">cafe — layout</span></div>
    <div class="mwb dgrid">
      <div class="ab">{ab}
        <div class="sel" id="p3-sel"><i style="left:-7px;top:-7px"></i><i style="right:-7px;top:-7px"></i><i style="left:-7px;bottom:-7px"></i><i style="right:-7px;bottom:-7px"></i></div>
        <svg class="pen" viewBox="0 0 380 284"><path id="p3-curve" d="M24 250 C 110 150, 210 330, 352 196"/><path class="hd" id="p3-h1" d="M24 250 L110 150"/><path class="hd" id="p3-h2" d="M352 196 L210 330"/></svg>
      </div>
      <div class="dpan"><span class="xb" style="font-size:66px;line-height:1">Aa</span><span class="note dim" style="font-size:20px">archivo · 800</span>
        <div class="sws"><i style="background:#ffd83d"></i><i style="background:#ff9ed6"></i><i style="background:#2f45f0"></i><i style="background:#1a0f2e"></i></div></div>
    </div>
    <span class="mtag">a designer</span>
  </div>
  <div class="mw dark" id="p3-b" style="left:420px;top:735px">
    <div class="mwh"><i></i><i></i><i></i><span class="mwt">cafe.tsx</span></div>
    <div class="mwb code">{code}<div class="cln"><u>7</u><span class="ccar" id="p3-car"></span></div></div>
    <span class="mtag rt">a developer</span>
  </div>
  <div class="mw" id="p3-c" style="left:40px;top:1110px">
    <div class="mwh"><i></i><i></i><i></i><span class="mwt">site builder</span>
      <span class="tmr"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path id="p3-hand" d="M12 12 L12 5"/></svg><span id="p3-tm">0h 00m</span></span></div>
    <div class="mwb bld">
      <div class="bside">{SIDE}</div>
      <div class="bcan"><b style="left:20px;top:18px;width:410px;height:26px;background:rgba(23,18,14,.8)"></b><b style="left:20px;top:62px;width:250px;height:14px;background:rgba(23,18,14,.18)"></b>
        <b style="left:20px;top:86px;width:200px;height:14px;background:rgba(23,18,14,.18)"></b><div class="bdz" id="p3-dz"></div></div>
      <div class="bdrag" id="p3-drag"><i></i><b></b></div>
      <div class="cursor small" id="p3-cur"><svg viewBox="0 0 24 24"><path d="M5 3 L5 19 L9 15 L12 22 L15 20.5 L11.5 14 L18 14 Z" fill="#fff" stroke="#141414" stroke-width="1.4" stroke-linejoin="round"/></svg></div>
    </div>
    <span class="mtag">hours in a builder</span>
  </div>
  <div class="stack" style="left:0;right:0;top:820px"><span id="p3-no" class="xb" style="font-size:150px">you don't.</span></div>""")
rev("#p3 .stack .sm", s + 0.05, y=12)
for k, (sel, wi, rot) in enumerate((("#p3-a", 57, -4), ("#p3-b", 59, 3), ("#p3-c", 61, -2.5))):
    a = t(wi) - 0.12
    js.append(f"tl.fromTo('{sel}', {{opacity:0, y:90, scale:.82, rotation:{rot * -2}}}, {{opacity:1, y:0, scale:1, rotation:{rot}, duration:.55, ease:'back.out(1.5)'}}, {a:.3f});")
    js.append(f"tl.fromTo('{sel} .mtag', {{opacity:0, scale:.6, rotation:-10}}, {{opacity:1, scale:1, rotation:0, duration:.4, ease:'back.out(2.4)'}}, {a + 0.18:.3f});")
    sfx.append(("hard-pop-click", a + 0.05, 0.3))
# designer: artboard blocks pop in, a selection snaps onto the image, the pen draws a curve
a = t(57) + 0.05
js.append(f"tl.fromTo('#p3 .abk', {{scale:0, transformOrigin:'0% 50%'}}, {{scale:1, duration:.3, stagger:.07, ease:'back.out(1.7)'}}, {a:.3f});")
js.append(f"tl.fromTo('#p3-sel', {{opacity:0, scale:1.25}}, {{opacity:1, scale:1, duration:.25, ease:'power3.out'}}, {a + 0.62:.3f});")
js.append(f"tl.fromTo('#p3-curve', {{strokeDashoffset:520}}, {{strokeDashoffset:0, duration:.9, ease:'power2.inOut'}}, {a + 0.3:.3f});")
js.append(f"tl.fromTo('#p3-h1, #p3-h2', {{opacity:0}}, {{opacity:1, duration:.2, stagger:.3}}, {a + 0.4:.3f});")
js.append(f"tl.fromTo('#p3 .sws i', {{scale:0}}, {{scale:1, duration:.25, stagger:.06, ease:'back.out(2)'}}, {a + 0.5:.3f});")
# developer: code types in line by line, caret blinks
a = t(59) + 0.02
for k, n in enumerate(CODE_LEN):
    js.append(f"tl.fromTo('#p3-c{k}', {{clipPath:'inset(0% 100% 0% 0%)'}}, {{clipPath:'inset(0% 0% 0% 0%)', duration:{0.012 * n + 0.05:.3f}, ease:'steps({n})'}}, {a + k * 0.2:.3f});")
js.append(f"tl.fromTo('#p3-car', {{opacity:1}}, {{opacity:0, duration:.01, yoyo:true, repeat:9, repeatDelay:.22}}, {a:.3f});")
sfx += [("tick_002", a + k * 0.2, 0.08) for k in range(6)]
# builder: the clock runs, a block is dragged over the drop zone, overshoots and settles
a = t(61) + 0.02
js.append(f"(function(){{ const o = {{m:0}}; tl.fromTo(o, {{m:0}}, {{m:400, duration:1.6, ease:'power1.in', onUpdate(){{ const m = Math.round(o.m); document.getElementById('p3-tm').textContent = Math.floor(m / 60) + 'h ' + String(m % 60).padStart(2, '0') + 'm'; }}}}, {a:.3f}); }})();")
js.append(f"tl.fromTo('#p3-hand', {{rotation:0, svgOrigin:'12 12'}}, {{rotation:2880, svgOrigin:'12 12', duration:1.6, ease:'power1.in'}}, {a:.3f});")
js.append(f"tl.fromTo('#p3-drag, #p3-cur', {{x:0, y:0, opacity:0}}, {{opacity:1, duration:.12}}, {a + 0.1:.3f});")
js.append(f"tl.to('#p3-drag, #p3-cur', {{x:352, y:128, duration:.55, ease:'power2.inOut', immediateRender:false}}, {a + 0.25:.3f});")
js.append(f"tl.to('#p3-drag, #p3-cur', {{x:322, y:111, duration:.28, ease:'back.out(2)', immediateRender:false}}, {a + 0.8:.3f});")
js.append(f"tl.fromTo('#p3-dz', {{backgroundColor:'rgba(47,69,240,0)', borderColor:'rgba(23,18,14,.25)'}}, {{backgroundColor:'rgba(47,69,240,.08)', borderColor:'rgba(47,69,240,.7)', duration:.2}}, {a + 0.55:.3f});")
sfx.append(("drop_002", a + 0.85, 0.22))
# "You don't." — everything drops off the page and the line slams in
a = t(66) - 0.36
for k, (sel, dx, dy, rot) in enumerate((("#p3-a", -1000, -160, -24), ("#p3-b", 1000, 40, 20), ("#p3-c", -1000, 260, -18))):
    js.append(f"tl.to('{sel}', {{x:{dx}, y:'+={dy}', rotation:{rot}, duration:.38, ease:'power2.in', immediateRender:false}}, {a + k * 0.03:.3f});")
js.append(f"tl.to('#p3 .stack .sm', {{opacity:0, y:-20, duration:.25, immediateRender:false}}, {a:.3f});")
js.append(f"tl.fromTo('#p3-no', {{opacity:0, scale:1.6, filter:'blur(18px)'}}, {{opacity:1, scale:1, filter:'blur(0px)', duration:.35, ease:'expo.out'}}, {t(66) - 0.04:.3f});")
sfx += [("fast-whoosh", a, 0.32), ("hard-pop-click", t(66), 0.4)]

# ---------------------------------------------------------------- P4 "So step one, I want you to draw your vision of your website."
WIRE = ('<rect x="20" y="10" width="560" height="44" rx="16"/><rect x="20" y="78" width="120" height="210" rx="20"/>'
        '<rect x="160" y="78" width="120" height="250" rx="20"/><rect x="300" y="78" width="120" height="180" rx="20"/><rect x="440" y="78" width="140" height="290" rx="20"/>')
s, e = t(82) - 0.08, t(94) - 0.06
scene("p4", s, e, f"""
  <div class="stack" style="left:0;right:0;top:330px">
    <span id="p4-step" class="sm" style="font-size:56px">step</span>
    <span id="p4-n" class="xb" style="font-size:300px;line-height:.95">1</span>
    <div class="row" style="align-items:baseline;gap:22px;margin-top:10px">
      <span id="p4-draw" class="xb" style="font-size:96px">draw your</span><span id="p4-vis" class="ital" style="font-size:110px">vision</span>
    </div>
  </div>
  <svg id="p4-wire" class="wire" viewBox="0 0 600 380" style="left:240px;top:1130px;width:600px;height:380px">{WIRE}</svg>""")
rev("#p4-step", s + 0.04, y=12)
js.append(f"tl.fromTo('#p4-n', {{opacity:0, scale:1.5, filter:'blur(18px)'}}, {{opacity:1, scale:1, filter:'blur(0px)', duration:.4, ease:'expo.out'}}, {t(83) - 0.08:.3f});")
rev("#p4-draw", t(88) - 0.05, y=26)
rev("#p4-vis", t(90) - 0.05, y=26)
js.append(f"tl.fromTo('#p4-wire rect', {{strokeDashoffset:1200}}, {{strokeDashoffset:0, duration:.7, stagger:.12, ease:'power2.inOut'}}, {t(88):.3f});")
sfx += [("dry-pop-alert", t(83), 0.24), ("scribble", t(88) + 0.1, 0.3)]

# ---------------------------------------------------------------- P5 "Step two" — then b-roll of the photo being taken
s, e = t(125) - 0.06, BROLL[6]["start"]
scene("p5", s, e, f"""
  <div class="stack" style="left:0;right:0;top:620px">
    <span id="p5-step" class="sm" style="font-size:56px">step</span>
    <span id="p5-n" class="xb" style="font-size:300px;line-height:.95">2</span>
    <span id="p5-t" class="sm" style="font-size:56px;margin-top:6px">{words_in('p5w', ['i', 'want', 'you', 'to'], [127, 128, 129, 130])}</span>
  </div>""")
rev("#p5-step", s + 0.04, y=12)
js.append(f"tl.fromTo('#p5-n', {{opacity:0, scale:1.5, filter:'blur(18px)'}}, {{opacity:1, scale:1, filter:'blur(0px)', duration:.4, ease:'expo.out'}}, {t(126) - 0.08:.3f});")
sfx += [("dry-pop-alert", t(126), 0.24), ("switch_003", t(133), 0.4)]

# ---------------------------------------------------------------- P6 "...and drop them into Claude."
s, e = BROLL[6]["end"], t(143) - 0.06
scene("p6", s, e, f"""
  <div class="stack" style="left:0;right:0;top:420px">
    <div class="row" style="align-items:center;gap:22px"><span class="sm" style="font-size:56px">drop them into</span><img id="p6-logo" src="assets/img/claude-mark.svg" style="width:96px;height:96px"/><span id="p6-cl" class="xb" style="font-size:110px">Claude</span></div>
  </div>
  <div id="p6-box" class="composer" style="top:1000px">
    <span id="p6-ph" class="ph">Message Claude…</span>
    <div id="p6-att" class="att"><img src="assets/img/sketch-crop.jpg"/><span>sketch.jpg</span></div>
    <span id="p6-send" class="wsend" style="position:absolute;right:30px;bottom:30px">&#8593;</span>
  </div>
  <img id="p6-fly" class="flyimg" src="assets/img/sketch-crop.jpg"/>""", whoosh=False)
js.append(f"tl.fromTo('#p6-box', {{opacity:0, y:40}}, {{opacity:1, y:0, duration:.35, ease:'power3.out'}}, {s:.3f});")
js.append(f"tl.fromTo('#p6-logo', {{opacity:0, scale:.3, rotation:-160}}, {{opacity:1, scale:1, rotation:0, duration:.55, ease:'back.out(1.8)'}}, {t(141) - 0.05:.3f});")
js.append(f"tl.fromTo('#p6-cl', {{opacity:0, x:-30, filter:'blur(10px)'}}, {{opacity:1, x:0, filter:'blur(0px)', duration:.4, ease:'expo.out'}}, {t(141) + 0.05:.3f});")
js.append(f"tl.fromTo('#p6-send', {{backgroundColor:'rgba(23,18,14,.12)', color:'{MUTED}'}}, {{backgroundColor:'{INK}', color:'#fbf9f5', duration:.2, immediateRender:false}}, {t(139) + 0.4:.3f});")
js.append(f"tl.fromTo('#p6-fly', {{opacity:0, x:0, y:-260, rotation:-8, scale:1}}, {{opacity:1, y:-160, duration:.12, ease:'power2.out'}}, {s:.3f});")
js.append(f"tl.to('#p6-fly', {{x:-250, y:330, rotation:0, scale:.32, duration:.42, ease:'power3.in', immediateRender:false}}, {max(t(139) - 0.1, s + 0.13):.3f});")
js.append(f"tl.to('#p6-fly', {{opacity:0, duration:.1, immediateRender:false}}, {t(139) + 0.32:.3f});")
js.append(f"tl.to('#p6-ph', {{y:118, duration:.2, ease:'power3.out', immediateRender:false}}, {t(139) + 0.12:.3f}); tl.fromTo('#p6-att', {{opacity:0, scale:.8}}, {{opacity:1, scale:1, duration:.25, ease:'back.out(2)'}}, {t(139) + 0.3:.3f});")
sfx += [("drop_002", t(139) + 0.32, 0.38), ("pluck_001", t(141), 0.22)]

# ---------------------------------------------------------------- P7 "Step three, this is the part that most people miss"
s, e = t(143) - 0.06, t(155) + 0.1
scene("p7", s, e, f"""
  <div class="stack" style="left:0;right:0;top:520px">
    <span id="p7-step" class="sm" style="font-size:56px">step</span>
    <span id="p7-n" class="xb" style="font-size:300px;line-height:.95">3</span>
    <span class="sm" style="font-size:56px;margin-top:6px">{words_in('p7w', ['the', 'part', 'most', 'people'], [147, 148, 150, 151])}</span>
    <span id="p7-miss" class="xb" style="font-size:110px;line-height:1.05;margin-top:10px">miss.</span>
  </div>""", whoosh=False)
rev("#p7-step", s + 0.02, y=12)
js.append(f"tl.fromTo('#p7-n', {{opacity:0, scale:1.5, filter:'blur(18px)'}}, {{opacity:1, scale:1, filter:'blur(0px)', duration:.4, ease:'expo.out'}}, {t(144) - 0.08:.3f});")
js.append(f"tl.fromTo('#p7-miss', {{opacity:0, scale:1.35, filter:'blur(16px)'}}, {{opacity:1, scale:1, filter:'blur(0px)', duration:.38, ease:'expo.out'}}, {t(152) - 0.05:.3f});")
sfx += [("dry-pop-alert", t(144), 0.24), ("tick_002", t(152), 0.3)]

# ---------------------------------------------------------------- P8 "tell Claude the vibe, who it's for, the colours, the feel, the components" — a brief builds
SW = ["#f2cf3b", "#ef8a2e", "#e9c3e6", "#2a1f6e"]
COMP = ["nav", "menu cards", "about", "testimonials", "contact"]
brief = [
    ("vibe", 169, '<span class="xb" style="font-size:50px">bold, playful indie café</span>'),
    ("who it's for", 170, '<span class="xb" style="font-size:50px">locals &amp; remote workers</span>'),
    ("colours", 174, "".join(f'<i class="sw" style="background:{c}"></i>' for c in SW)),
    ("feel", 179, '<span class="ital" style="font-size:56px">warm, loud, a bit cheeky</span>'),
    ("components", 184, "".join(f'<span class="cmp">{c}</span>' for c in COMP)),
]
s, e = t(162) - 0.06, t(187) - 0.06
items = "".join(f'<div class="brow" id="p8-b{k}"><span class="note dim">{lab}</span><div class="bval">{val}</div></div>' for k, (lab, wi, val) in enumerate(brief))
scene("p8", s, e, f"""
  <div class="stack" style="left:0;right:0;top:250px">
    <div class="row" style="align-items:center;gap:22px"><span class="sm" style="font-size:56px">tell</span><img id="p8-logo" src="assets/img/claude-mark.svg" style="width:96px;height:96px"/><span id="p8-cl" class="xb" style="font-size:110px">Claude</span></div>
  </div>
  <div id="p8-card" class="bcard" style="top:470px">{items}</div>""")
js.append(f"tl.fromTo('#p8-logo', {{opacity:0, scale:.3, rotation:-160}}, {{opacity:1, scale:1, rotation:0, duration:.55, ease:'back.out(1.8)'}}, {t(166) - 0.1:.3f});")
rev("#p8-cl", t(167) - 0.06, y=24)
js.append(f"tl.fromTo('#p8-card', {{opacity:0, y:50}}, {{opacity:1, y:0, duration:.45, ease:'power3.out'}}, {t(167):.3f});")
for k, (lab, wi, val) in enumerate(brief):
    js.append(f"tl.fromTo('#p8-b{k}', {{opacity:0, x:60, filter:'blur(10px)'}}, {{opacity:1, x:0, filter:'blur(0px)', duration:.4, ease:'power3.out'}}, {t(wi) - 0.08:.3f});")
    sfx.append(("tick_002", t(wi), 0.22))
js.append(f"tl.fromTo('#p8-b2 .sw', {{scale:0}}, {{scale:1, duration:.3, stagger:.06, ease:'back.out(2.2)'}}, {t(174):.3f});")
js.append(f"tl.fromTo('#p8-b4 .cmp', {{opacity:0, y:14}}, {{opacity:1, y:0, duration:.25, stagger:.06, ease:'power2.out'}}, {t(185):.3f});")

# ---------------------------------------------------------------- P9 the exact prompt (reading card) + cursor hits send
P2_LINES = [
    "Build a website from the sketch I've attached.",
    'Vibe: <b class="fill">bold, playful indie café</b>',
    'Who it\'s for: <b class="fill">locals &amp; remote workers</b>',
    'Colours: <b class="fill">sunny yellow, orange, lilac, deep navy</b>',
    'Feel: <b class="fill">warm, loud, a little cheeky</b>',
    'Components: <b class="fill">nav, menu cards, about, who we are, testimonials, contact</b>',
    "Follow my layout closely, add hover animations and make it fully responsive.",
]
s, e = t(187) - 0.06, t(209) - 0.06
lines9 = "".join(f'<div class="pl" id="p9-l{k}">{ln}</div>' for k, ln in enumerate(P2_LINES))
scene("p9", s, e, f"""
  <div class="stack" style="left:80px;top:230px;align-items:flex-start">
    <div class="row" style="align-items:baseline;gap:22px"><span id="p9-a" class="xb" style="font-size:100px">the exact</span><span id="p9-b" class="ital" style="font-size:112px">prompt</span></div>
  </div>
  <div id="p9-win" class="win" style="top:450px">
    <div class="bar-top"><i></i><i></i><i></i><span class="wt">Claude</span></div>
    <div class="pbody">{lines9}</div>
    <div class="wfoot"><img src="assets/img/claude-mark.svg" style="width:44px;height:44px"/><span class="note dim">template — swap the highlighted parts</span><span id="p9-send" class="wsend">&#8593;</span></div>
  </div>
  <div id="p9-cur" class="cursor"><svg viewBox="0 0 24 24"><path d="M5 3 L5 19 L9 15 L12 22 L15 20.5 L11.5 14 L18 14 Z" fill="#fff" stroke="#141414" stroke-width="1.4" stroke-linejoin="round"/></svg></div>""")
rev("#p9-a", s + 0.05, y=22)
rev("#p9-b", t(190) - 0.06, y=24)
js.append(f"tl.fromTo('#p9-win', {{opacity:0, y:90, scale:.96}}, {{opacity:1, y:0, scale:1, duration:.45, ease:'power3.out'}}, {s + 0.1:.3f});")
js.append(f"tl.fromTo('#p9-win .pl', {{opacity:0, y:14, filter:'blur(8px)'}}, {{opacity:1, y:0, filter:'blur(0px)', duration:.32, stagger:.11, ease:'power2.out'}}, {s + 0.35:.3f});")
js.append(f"tl.fromTo('#p9-win .fill', {{backgroundColor:'rgba(23,18,14,0)'}}, {{backgroundColor:'rgba(23,18,14,.09)', duration:.3, stagger:.08}}, {t(199) - 0.05:.3f});")
click = t(207)
js.append(f"tl.fromTo('#p9-cur', {{x:1060, y:1700, opacity:0}}, {{x:931, y:1188, opacity:1, duration:.7, ease:'power3.out'}}, {click - 0.8:.3f});")
js.append(f"tl.to('#p9-cur', {{scale:.82, duration:.08, yoyo:true, repeat:1, immediateRender:false}}, {click:.3f});")
js.append(f"tl.fromTo('#p9-send', {{backgroundColor:'rgba(23,18,14,.12)', color:'{MUTED}', scale:1}}, {{backgroundColor:'{INK}', color:'#fbf9f5', scale:1.08, duration:.18}}, {click:.3f});")
sfx += [("maximize_006", s + 0.1, 0.28), ("click_002", click, 0.45), ("explainer-light-pop-whoosh", click + 0.05, 0.25)]

# ---------------------------------------------------------------- P10 "Look at that compared to that" — sketch vs site
s, e = t(231) - 0.06, t(240) - 0.08
scene("p10", s, e, f"""
  <div id="p10-a" class="vcard" style="top:250px"><img src="assets/img/sketch-crop.jpg" class="pimg"/><span class="tagnote">the sketch</span></div>
  <svg id="p10-arrow" class="arr" viewBox="0 0 60 120" style="left:510px;top:770px;width:60px;height:120px"><path d="M30 6 L30 110 M10 88 L30 110 L50 88"/></svg>
  <div id="p10-b" class="vcard" style="top:900px"><img src="assets/img/site-hero.jpg" class="pimg" style="object-position:50% 0%"/><span class="tagnote">the website</span></div>""")
js.append(f"tl.fromTo('#p10-a', {{opacity:0, y:-40, scale:.95}}, {{opacity:1, y:0, scale:1, duration:.45, ease:'power3.out'}}, {t(233) - 0.08:.3f});")
js.append(f"tl.fromTo('#p10-arrow path', {{strokeDashoffset:200}}, {{strokeDashoffset:0, duration:.35, ease:'power2.out'}}, {t(234):.3f});")
js.append(f"tl.fromTo('#p10-b', {{opacity:0, y:40, scale:.95}}, {{opacity:1, y:0, scale:1, duration:.45, ease:'power3.out'}}, {t(236) - 0.1:.3f});")
sfx += [("drop_002", t(233), 0.26), ("drop_002", t(236), 0.28)]

# ---------------------------------------------------------------- P11 "It's live right now at ... hullabaloo. Check it out."
# The address is typed on a keyboard (each key presses in time), return is hit, and the real site loads and scrolls.
URL = "hullabaloo.scriptai.space"  # the live address (scriptai.space/hullabaloo returns 404)
s, e = t(268) - 0.06, t(279) + 0.35
ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm."]
kid = lambda c: "dot" if c == "." else c
kb = (f'<div class="kr">{"".join(f"<b class=k id=k-{kid(c)}>{c}</b>" for c in ROWS[0])}</div>'
      f'<div class="kr">{"".join(f"<b class=k id=k-{kid(c)}>{c}</b>" for c in ROWS[1])}<b class="k ret" id="k-ret">return&nbsp;&#8629;</b></div>'
      f'<div class="kr"><b class="k w">&#8679;</b>{"".join(f"<b class=k id=k-{kid(c)}>{c}</b>" for c in ROWS[2])}<b class="k w">&#8679;</b></div>'
      f'<div class="kr"><b class="k cmd">&#8984;</b><b class="k w" id="k-space"></b><b class="k cmd">&#8984;</b></div>')
scene("p11", s, e, f"""
  <div class="stack" style="left:0;right:0;top:250px"><div class="row" style="align-items:baseline;gap:20px"><span class="sm" style="font-size:56px">it's</span><span id="p11-live" class="ital" style="font-size:84px">live</span><span class="sm" style="font-size:56px">right now</span></div></div>
  <div id="p11-win" class="bwin" style="top:390px;height:600px">
    <div class="bbar"><i></i><i></i><i></i><div class="urlpill"><i class="ldot"></i><span id="p11-url"></span><span id="p11-caret" class="ucaret"></span><i id="p11-load" class="uload"></i></div></div>
    <div class="newtab" id="p11-nt"><b></b><b></b><b></b><b></b></div>
    <div class="bview" id="p11-view"><img id="p11-page" src="assets/img/site-full.jpg"/></div>
  </div>
  <div id="p11-kb" class="kb" style="top:1050px">{kb}</div>""")
rev("#p11-live", t(269) - 0.06, y=24)
js.append(f"tl.fromTo('#p11-win', {{opacity:0, y:70, scale:.96}}, {{opacity:1, y:0, scale:1, duration:.45, ease:'power3.out'}}, {s + 0.12:.3f});")
u0, u1 = t(273) - 0.05, t(275) + 0.4
js.append(f"tl.fromTo('#p11-kb', {{opacity:0, y:260}}, {{opacity:1, y:0, duration:.55, ease:'expo.out'}}, {u0 - 0.6:.3f});")
js.append(f"(function(){{ const s = {json.dumps(URL)}, o = {{n:0}}; tl.fromTo(o, {{n:0}}, {{n:s.length, duration:{u1 - u0:.3f}, ease:'none', onUpdate(){{ document.getElementById('p11-url').textContent = s.slice(0, Math.round(o.n)); }}}}, {u0:.3f}); }})();")
for i, c in enumerate(URL):
    at = u0 + (u1 - u0) * (i + 0.5) / len(URL)
    js.append(f"tl.fromTo('#k-{kid(c)}', {{y:0, backgroundColor:'#fbf9f5', boxShadow:'0 4px 0 rgba(40,26,14,.2)'}}, {{y:4, backgroundColor:'#e6e0d6', boxShadow:'0 0px 0 rgba(40,26,14,.2)', duration:.045, yoyo:true, repeat:1, immediateRender:false}}, {at:.3f});")
    if i % 2 == 0:
        sfx.append(("click_004", at, 0.12))
ent = max(u1 + 0.25, t(276) - 0.3)
js.append(f"tl.fromTo('#k-ret', {{y:0, scale:1, backgroundColor:'#fbf9f5', color:'{INK}'}}, {{y:6, scale:.95, backgroundColor:'{INK}', color:'#fbf9f5', duration:.09, ease:'power2.out', immediateRender:false}}, {ent:.3f});")
js.append(f"tl.to('#k-ret', {{y:0, scale:1, backgroundColor:'#fbf9f5', color:'{INK}', duration:.3, ease:'power2.out', immediateRender:false}}, {ent + 0.16:.3f});")
js.append(f"tl.set('#p11-caret', {{opacity:0}}, {ent:.3f});")
js.append(f"tl.fromTo('#p11-load', {{scaleX:0, opacity:1}}, {{scaleX:1, duration:.4, ease:'power2.inOut'}}, {ent + 0.04:.3f}); tl.to('#p11-load', {{opacity:0, duration:.15, immediateRender:false}}, {ent + 0.44:.3f});")
js.append(f"tl.to('#p11-nt', {{opacity:0, duration:.2, immediateRender:false}}, {ent + 0.25:.3f});")
js.append(f"tl.fromTo('#p11-view', {{opacity:0, y:30}}, {{opacity:1, y:0, duration:.35, ease:'power3.out'}}, {ent + 0.3:.3f});")
js.append(f"tl.fromTo('#p11-page', {{y:0}}, {{y:-980, duration:{max(0.6, e - 0.45 - (ent + 0.75)):.3f}, ease:'power2.inOut'}}, {ent + 0.75:.3f});")
js.append(f"tl.to('#p11-kb', {{y:40, opacity:.0, duration:.4, ease:'power2.in', immediateRender:false}}, {ent + 0.5:.3f});")
js.append(f"tl.to('#p11-win', {{y:150, scale:1.04, duration:.6, ease:'power3.inOut', immediateRender:false}}, {ent + 0.45:.3f});")
sfx += [("hard-pop-click", ent, 0.42), ("explainer-light-pop-whoosh", ent + 0.3, 0.22)]

# ---------------------------------------------------------------- P12 "Comment sketch and I'll send you the prompt"
s, e = t(307) - 0.06, t(315) + 0.25
WORD = "SKETCH"
scene("p12", s, e, f"""
  <div class="stack" style="left:0;right:0;top:560px"><span id="p12-c" class="sm" style="font-size:56px">comment</span></div>
  <div id="p12-box" class="cbox" style="top:720px"><span id="p12-tx" class="xb" style="font-size:96px"></span><span class="ucaret big"></span><span id="p12-send" class="wsend">&#8593;</span></div>
  <div class="stack" style="left:0;right:0;top:1000px"><span class="sm" style="font-size:52px">{words_in('p12w', ["and", "i'll", "send", "you", "the", "prompt"], [309, 310, 311, 312, 313, 314])}</span></div>""")
rev("#p12-c", s + 0.04, y=12)
js.append(f"tl.fromTo('#p12-box', {{opacity:0, y:40}}, {{opacity:1, y:0, duration:.35, ease:'power3.out'}}, {s + 0.08:.3f});")
c0, c1 = t(308) - 0.05, t(308) + 0.42
js.append(f"(function(){{ const s = {json.dumps(WORD)}, o = {{n:0}}; tl.fromTo(o, {{n:0}}, {{n:s.length, duration:{c1 - c0:.3f}, ease:'none', onUpdate(){{ document.getElementById('p12-tx').textContent = s.slice(0, Math.round(o.n)); }}}}, {c0:.3f}); }})();")
js.append(f"tl.fromTo('#p12-send', {{backgroundColor:'rgba(23,18,14,.12)', color:'{MUTED}'}}, {{backgroundColor:'{INK}', color:'#fbf9f5', duration:.18}}, {c1 + 0.05:.3f});")
for k in range(len(WORD)):
    sfx.append(("click_002", c0 + (c1 - c0) * k / len(WORD), 0.14))

# ---------------------------------------------------------------- P13 end card "see you on day three" — 30 blocks, today's two lit, zoom into day 2
s = t(320) - 0.06
ZX, ZY = 90 + 1 * (SEG_W + 6) + SEG_W / 2, 1340 - 40 * 1.9 / 2
scene("p13", s, DURATION, f"""
  <div id="p13-zoom" style="position:absolute;inset:0;transform-origin:{ZX:.1f}px {ZY:.1f}px">
    <div class="stack" style="left:0;right:0;top:560px">
      <span id="p13-lead" class="sm" style="font-size:56px">see you on</span>
      <div class="row" style="align-items:flex-end;justify-content:center;margin-top:6px">
        <span id="p13-day" class="xb" style="font-size:230px;line-height:1">Day</span>
        <span id="p13-n" class="xb" style="font-size:230px;line-height:1;margin-left:40px">3</span>
      </div>
    </div>
    <span id="p13-lbl" class="note" style="position:absolute;left:{90 + SEG_W + 6:.0f}px;top:1186px">day 02 / 30</span>
    <div id="p13-bar" class="bar big" style="top:1300px">{BLOCKS.replace('{p}', 'p13')}</div>
  </div>""")
rev("#p13-lead", s + 0.04, y=12)
rev("#p13-day", t(321) - 0.05, y=30)
js.append(f"tl.fromTo('#p13-n', {{opacity:0, scale:1.5, filter:'blur(18px)'}}, {{opacity:1, scale:1, filter:'blur(0px)', duration:.45, ease:'expo.out'}}, {t(322) - 0.05:.3f});")
js.append(f"tl.fromTo('#p13-bar .seg', {{scaleY:0, opacity:0}}, {{scaleY:1, opacity:1, duration:.3, stagger:.014, ease:'power2.out'}}, {s + 0.1:.3f});")
lit = t(322) + 0.45
js.append(f"tl.fromTo('#p13-s0', {{backgroundColor:'rgba(23,18,14,.14)'}}, {{backgroundColor:'{INK}', duration:.2}}, {lit - 0.25:.3f});")
js.append(f"tl.fromTo('#p13-s1', {{backgroundColor:'rgba(23,18,14,.14)', scaleY:1}}, {{backgroundColor:'{INK}', scaleY:1.9, duration:.5, ease:'back.out(2.2)'}}, {lit:.3f});")
js.append(f"tl.fromTo('#p13-lbl', {{opacity:0, y:12}}, {{opacity:1, y:0, duration:.35, ease:'power2.out'}}, {lit + 0.15:.3f});")
js.append(f"tl.fromTo('#p13-s1', {{scaleY:1.9}}, {{scaleY:2.2, duration:.6, yoyo:true, repeat:1, ease:'sine.inOut', immediateRender:false}}, {lit + 0.6:.3f});")
zoom_at = DURATION - 1.4
js.append(f"tl.to('#p13-lbl', {{opacity:0, duration:.3, immediateRender:false}}, {zoom_at:.3f});")
js.append(f"tl.fromTo('#p13-zoom', {{scale:1, x:0, y:0}}, {{scale:60, x:{540 - ZX:.1f}, y:{960 - ZY:.1f}, duration:1.3, ease:'power3.inOut'}}, {zoom_at:.3f});")
sfx += [("dry-pop-alert", t(322), 0.24), ("pluck_001", lit, 0.3), ("riser", zoom_at + 0.25, 0.35), ("boom", DURATION - 0.12, 0.3)]

# ---------------------------------------------------------------- hook: quick zoom on the b-roll + a whoosh
sfx += [("arrow-whoosh", 0.0, 0.32), ("dry-pop-alert", t(6), 0.2)]

# ---------------------------------------------------------------- captions (Day 1 layout: small lead-in, bold phrase, italic accent)
CAPS = [
    [["s:0", "s:1", "s:2"], ["s:325", "s:326"], ["b:327"]],
    [["s:3", "s:4", "s:5"], ["b:6", "b:7"]],
    [["s:8", "s:9", "s:10", "s:11", "s:12", "s:13", "s:14"], ["s:15", "s:16"], ["b:17"]],
    [["s:24", "s:25", "s:26", "s:27", "s:28"], ["b:29", "b:30", "b:31"], ["s:32", "i:33"]],
    [["s:45", "s:46", "s:47", "s:48", "s:49"], ["b:50"]],
    [["s:51", "s:52", "s:53"], ["s:54", "s:55"]],
    [["s:68", "s:69", "s:70"], ["b:71", "b:72"], ["s:73", "i:74"]],
    [["s:75", "s:76", "s:77"], ["b:78", "b:79", "b:80"]],
    [["s:94", "s:95", "s:96"], ["i:97"]],
    [["s:98"], ["b:99"], ["s:100", "s:101", "i:102"]],
    [["s:103", "s:104", "s:105", "s:106", "s:107", "s:108"], ["b:109"], ["s:110", "s:111", "s:112"]],
    [["s:113", "s:114", "s:115", "s:116", "s:117"], ["b:118"]],
    [["s:119", "s:120", "s:121", "s:122", "s:123"], ["i:124"]],
    [["s:131", "s:132"], ["b:133"], ["s:134", "s:135", "s:136", "i:137"]],
    [["s:153", "s:154", "s:155"], ["b:156", "b:157", "b:158"], ["s:159", "s:160", "i:161"]],
    [["s:208", "s:209"], ["b:210", "b:211"]],
    [["s:212", "s:213", "s:214"], ["b:215", "b:216"], ["i:217"]],
    [["s:218", "s:219", "s:220"], ["b:221"]],
    [["s:222", "b:223"], ["s:224", "b:225"]],
    [["s:226", "s:227", "s:228", "s:229"], ["i:230"]],
    [["b:240"], ["s:241", "s:242", "b:243"]],
    [["s:244", "s:245", "i:246"]],
    [["s:247", "s:248", "b:249"]],
    [["s:250", "s:251"], ["b:252"], ["s:253", "s:254"]],
    [["s:255", "s:256"], ["b:257"], ["s:258", "s:259", "i:260"]],
    [["s:261", "s:262", "s:263"], ["s:264", "s:265"], ["b:266", "b:267"]],
    [["s:279", "s:280", "s:281", "s:282", "s:283"], ["b:284", "b:285"], ["s:286", "s:287", "b:288"]],
    [["s:289", "s:290"], ["b:291", "b:292"]],
    [["s:293", "s:294"], ["i:295"]],
    [["s:296", "s:297"], ["b:298", "b:299", "b:300"]],
    [["s:301", "s:302"], ["b:303"], ["s:304", "s:305", "i:306"]],
    [["s:315", "s:316", "s:317"], ["b:318", "b:319"]],
]
KEEP_CASE = ("I", "I'm", "AI.", "Claude", "Claude.", "Jack.")
cap_cover = [(a, b) for _, a, b, _ in scenes]


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
    if end - g_start < 0.25:
        continue
    rows = []
    for ln in lines:
        spans = []
        for tok in ln:
            style, i = tok.split(":")
            cls = {"s": "cs", "b": "cb", "i": "ci"}[style[0]]
            text = TOK[int(i)]["text"]
            if style[0] == "s" and text not in KEEP_CASE:
                text = text.lower()
            spans.append(f'<span class="w {cls}" id="w{i}">{esc(text)}</span>')
        rows.append(f'<div class="cl">{" ".join(spans)}</div>')
    # In b-roll where his head reaches the top of frame, lift the caption clear of it.
    lift = ' style="bottom:1450px"' if any(g_start < bb["end"] and end > bb["start"] for bb in (BROLL[3],)) else ""
    # over the bright laptop-screen footage the words get a soft local scrim (only behind the text)
    scrim = " scrim" if any(g_start < bb["end"] and end > bb["start"] for bb in (BROLL[1], BROLL[7])) else ""
    cap_html.append(f'<div class="cap clip{scrim}" id="cap{g}"{lift} data-start="{g_start:.3f}" data-duration="{end - g_start:.3f}" data-track-index="2"><div class="capi">{"".join(rows)}</div></div>')
    for i in idx:
        cap_js.append(f"word('#w{i}', {max(0.0, t(i) - 0.05):.3f});")
    cap_js.append(f"tl.fromTo('#cap{g} .capi', {{opacity:1, filter:'blur(0px)', y:0}}, {{opacity:0, filter:'blur(10px)', y:-10, duration:.12, ease:'power1.in', immediateRender:false}}, {end - 0.12:.3f});")

# ---------------------------------------------------------------- b-roll layer (inside the camera, muted)
br_html = "".join(f'<video id="br{n}" class="clip brl" src="{b["file"]}" data-start="{b["start"]:.3f}" data-duration="{b["end"] - b["start"]:.3f}" data-track-index="1" muted playsinline></video>'
                  for n, b in enumerate(BROLL))
br_windows = [(b["start"], b["end"]) for b in BROLL]

# ---------------------------------------------------------------- camera: hook slam, face-aware punch-ins, slow push on b-roll
samples = []
for line in open("edit/faces-cut-2fps.txt"):
    p = line.split()
    if p[1] != "none":
        samples.append(((int(p[0][1:5]) - 1) / 2, *map(float, p[1:5])))
extra = [t(29), t(98), t(279), t(293), t(301), t(255), t(68)]
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
    zmax = max(1.0, (cy - CAP_CLEAR) / max(cy - top, 1e-3) / 1.025)
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
back_js = []
for sid, a, b_end, _ in scenes:
    if b_end >= AROLL_END - 0.01 or any(abs(b_end - s2[1]) < 0.02 for s2 in scenes) or any(abs(b_end - w[0]) < 0.02 for w in br_windows):
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
sfx_html = "\n".join(f'<audio id="sfx{n}" src="assets/audio/sfx/{name}.wav" data-start="{at:.3f}" data-track-index="{20 + n}" data-volume="{vol}"></audio>'
                     for n, (name, at, vol) in enumerate(sorted(sfx, key=lambda x: x[1])))
scene_html = "\n".join(f"""<section class="scene clip" id="{sid}" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="3">
 <div class="sheet"><img class="paper" src="assets/img/paper-clean.jpg"/>
  <div class="content">{body}
  </div>
 </div>
</section>""" for sid, a, b, body in scenes)
page = open("edit/template.html").read()
page = re.sub(r'\s*<audio id="bgm"[^>]*></audio>', "", page)  # Jack asked for no music on Day 2
page = (page.replace("{{DURATION}}", f"{DURATION:.3f}").replace("{{AROLL_END}}", f"{AROLL_END:.3f}")
        .replace("{{SCENES}}", scene_html).replace("{{CAPTIONS}}", "\n".join(cap_html)).replace("{{GRADE_LAYER}}", br_html)
        .replace("{{SFX}}", sfx_html).replace("{{JS}}", "\n".join(cam_js + back_js + js + cap_js))
        .replace("{{GRADE}}", GRADE).replace("{{INK}}", INK).replace("{{PAPER}}", PAPER).replace("{{RED}}", RED).replace("{{MUTED}}", MUTED)
        .replace("assets/audio/bgm/bed-cliff.wav", "assets/audio/bgm/bed.wav"))
open("index.html", "w").write(page)
# No music bed on Day 2 (Jack asked for it removed), so nothing to carve.
print(f"index.html: {len(scenes)} pages, {len(cap_html)} caption groups, {len(BROLL)} b-roll, {len(sfx)} sfx, {DURATION:.2f}s")
