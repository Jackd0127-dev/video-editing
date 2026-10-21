"""Generate index.html for the comment-CTA edit (theme 2: minimal one-word captions).
Run from the project root:  python3 -I edit/build.py
"""
import json

W = json.load(open("edit/tokens-raw.json"))
SEGS = json.load(open("edit/words.json"))["segments"]
END = SEGS[-1]["end"]
DUR = round(END, 3)
FACE_CX, FACE_CY = 0.55, 0.55


def t(i):
    return W[i]["start"]


# ---------------------------------------------------------------- one-word captions (hard switch)
DOC_FROM, DOC_TO = 61, 64          # "documenting my journey too." becomes an emphasis card
groups = []
i = 0
while i < len(W):
    if DOC_FROM <= i <= DOC_TO:
        i += 1
        continue
    word = W[i]["text"].strip(",.").upper()
    j = i + 1
    nxt = W[j] if j < len(W) and not (DOC_FROM <= j <= DOC_TO) else None
    if nxt and len(word) <= 4 and len(nxt["text"].strip(",.")) <= 4 and nxt["start"] - W[i]["start"] < 0.3:
        word += " " + nxt["text"].strip(",.").upper()
        j += 1
    end_txt = W[j - 1]["text"]
    groups.append([W[i]["start"], word + ("." if end_txt.endswith(".") else ""), j])
    i = j
for k, g in enumerate(groups):
    nxt = groups[k + 1][0] - 0.02 if k + 1 < len(groups) else DUR
    last_tok = W[g[2] - 1]
    g.append(min(nxt, last_tok["start"] + 0.75, t(DOC_FROM) - 0.03 if g[0] < t(DOC_FROM) else DUR))
caps = "".join(f'<div class="cap clip" id="c{n}" data-start="{max(0, a - 0.02):.3f}" data-duration="{b - max(0, a - 0.02):.3f}" data-track-index="2">{w}</div>' for n, (a, w, _, b) in enumerate(groups))

# ---------------------------------------------------------------- hook: quick zoom + glass banner with a little pixel Claude character
js, sfx = [], []
PS = 20
px = []
def blk(c0, c1, r0, r1, cls):
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            px.append(f'<i class="px {cls}" style="left:{c * PS}px;top:{r * PS}px"></i>')
blk(2, 8, 0, 5, "bd"); blk(0, 1, 3, 4, "bd arm l"); blk(9, 10, 3, 4, "bd arm r")
for k, c in enumerate([2, 4, 6, 8]):
    blk(c, c, 6, 7, f"bd leg g{k % 2}")
eyes = "".join(f'<i class="eye" style="left:{c * PS}px;top:{2 * PS}px"></i>' for c in (3, 7))
CHAR = f'<div id="crab">{"".join(px)}{eyes}</div>'
TITLE = ["WHAT", "YOU'RE", "BUILDING?"]
BANNER = f"""<div id="banner" class="clip" data-start="0" data-duration="{{HB}}" data-track-index="3">
  <div id="bglass" class="glass"><i class="sheen" id="bsheen"></i>
    <span id="bkick">tell me</span>
    <div id="btitle">{"".join(f'<span class="bw" id="bw{k}">{w}</span>' for k, w in enumerate(TITLE))}</div>
  </div>
  <div id="crabwrap">{CHAR}</div>
</div>"""
hook_end = t(16) + 0.35
js.append("tl.fromTo('#cam', {scale:1.38}, {scale:1, duration:.55, ease:'expo.out', immediateRender:true}, 0);")
js.append("tl.fromTo('#bglass', {opacity:0, y:-24, filter:'blur(10px)'}, {opacity:1, y:0, filter:'blur(0px)', duration:.9, ease:'power3.out'}, .1);")
js.append("tl.fromTo('#bkick', {opacity:0, y:10}, {opacity:1, y:0, duration:.4, ease:'power2.out'}, .45);")
for k in range(len(TITLE)):
    js.append(f"tl.fromTo('#bw{k}', {{opacity:0, y:26, scale:1.15}}, {{opacity:1, y:0, scale:1, duration:.32, ease:'back.out(2)'}}, {0.55 + k * 0.12:.2f});")
js.append("tl.fromTo('#bsheen', {xPercent:-120}, {xPercent:420, duration:.9, ease:'power2.inOut'}, .75);")
js.append("tl.fromTo('#crabwrap', {y:150, opacity:0}, {y:0, opacity:1, duration:.45, ease:'back.out(2)'}, .3);")
hops = [0.95, 1.6, 2.45, 3.05, 3.7]
for h in hops:
    js.append(f"tl.fromTo('#crab', {{y:0}}, {{y:-30, duration:.16, ease:'power2.out', yoyo:true, repeat:1, immediateRender:false}}, {h:.2f});")
    js.append(f"tl.fromTo('#crab .g0', {{y:0}}, {{y:-8, duration:.08, yoyo:true, repeat:3, immediateRender:false}}, {h:.2f});")
    js.append(f"tl.fromTo('#crab .g1', {{y:-8}}, {{y:0, duration:.08, yoyo:true, repeat:3, immediateRender:false}}, {h:.2f});")
for b_ in (1.3, 2.75, 4.0):
    js.append(f"tl.fromTo('#crab .eye', {{scaleY:1}}, {{scaleY:.15, duration:.06, yoyo:true, repeat:1, immediateRender:false}}, {b_:.2f});")
js.append("tl.fromTo('#crab .arm.r', {y:0}, {y:-16, duration:.12, yoyo:true, repeat:5, ease:'sine.inOut', immediateRender:false}, 1.9);")
js.append(f"tl.to('#crabwrap', {{y:-260, opacity:0, duration:.45, ease:'power2.in', immediateRender:false}}, {hook_end - 0.3:.3f});")
js.append(f"tl.to('#bglass', {{y:-80, opacity:0, filter:'blur(14px)', duration:.4, ease:'power2.in', immediateRender:false}}, {hook_end - 0.15:.3f});")
sfx += [("fast-whoosh", 0.0, 0.32), ("pluck_001", 0.32, 0.3)] + [("tick_002", h, 0.16) for h in hops]

# ---------------------------------------------------------------- emphasis card on "documenting my journey too."
d0, d1 = t(DOC_FROM) - 0.03, t(DOC_TO) + 0.42
js.append(f"tl.fromTo('#doc-big', {{opacity:0, scale:1.25}}, {{opacity:1, scale:1, duration:.25, ease:'expo.out'}}, {d0:.3f});")
js.append(f"tl.fromTo('#doc-sub', {{opacity:0}}, {{opacity:1, duration:.15}}, {t(62) - 0.03:.3f});")
sfx.append(("dry-pop-alert", d0, 0.2))

# ---------------------------------------------------------------- ending: glass composer, natural typing, cursor clicks send, comment posts
TYPED = "i'm building my first app"
c0 = t(55) - 0.1
type_from = c0 + 0.45
gaps = [0.045 + 0.035 * (((k * 37) % 11) / 10) + (0.07 if TYPED[k - 1:k] == " " else 0) for k in range(len(TYPED))]
times, acc = [], type_from
for g in gaps:
    acc += g
    times.append(round(acc, 3))
type_to = times[-1]
click = type_to + 0.5
js.append(f"tl.fromTo('#comp', {{opacity:0, y:-24, filter:'blur(10px)'}}, {{opacity:1, y:0, filter:'blur(0px)', duration:.8, ease:'power3.out'}}, {c0:.3f});")
js.append(f"tl.fromTo('#csheen', {{xPercent:-120}}, {{xPercent:420, duration:.9, ease:'power2.inOut'}}, {c0 + 0.25:.3f});")
js.append(f"(function(){{ const s = {json.dumps(TYPED)}, T = {json.dumps(times)}, o = {{v:{type_from}}}; tl.fromTo(o, {{v:{type_from}}}, {{v:{click + 0.12:.3f}, duration:{click + 0.12 - type_from:.3f}, ease:'none', onUpdate(){{ let n = 0; while (n < T.length && T[n] <= o.v) n++; const posted = o.v >= {click + 0.1:.3f}; document.getElementById('ctx').textContent = posted ? '' : s.slice(0, n); document.getElementById('cph').style.opacity = (n === 0 || posted) ? 1 : 0; }}}}, {type_from:.3f}); }})();")
js.append(f"tl.fromTo('#caret', {{opacity:1}}, {{opacity:0, duration:.28, yoyo:true, repeat:{max(1, int((click - type_to) / 0.28)) | 1}, ease:'steps(1)', immediateRender:false}}, {type_to:.3f});")
js.append(f"tl.set('#caret', {{opacity:0}}, {click + 0.1:.3f});")
js.append(f"tl.fromTo('#csend', {{scale:1, backgroundColor:'rgba(255,255,255,.16)'}}, {{scale:1.08, backgroundColor:'rgba(255,255,255,.95)', duration:.25, ease:'power2.out'}}, {type_to + 0.05:.3f});")
js.append(f"tl.fromTo('#csend svg', {{fill:'#ffffff'}}, {{fill:'#111111', duration:.25}}, {type_to + 0.05:.3f});")
js.append(f"tl.fromTo('#cur', {{x:1060, y:820, opacity:0}}, {{x:930, y:385, opacity:1, duration:{click - type_to - 0.05:.3f}, ease:'power3.out'}}, {type_to:.3f});")
js.append(f"tl.to('#cur', {{scale:.82, duration:.08, yoyo:true, repeat:1, immediateRender:false}}, {click:.3f});")
js.append(f"tl.to('#csend', {{scale:.86, duration:.08, yoyo:true, repeat:1, immediateRender:false}}, {click:.3f});")
js.append(f"tl.fromTo('#cring', {{scale:.4, opacity:.8}}, {{scale:2.2, opacity:0, duration:.45, ease:'power2.out'}}, {click:.3f});")
js.append(f"tl.to('#csend', {{backgroundColor:'rgba(255,255,255,.16)', duration:.25, immediateRender:false}}, {click + 0.18:.3f}); tl.to('#csend svg', {{fill:'#ffffff', duration:.25, immediateRender:false}}, {click + 0.18:.3f});")
js.append(f"tl.fromTo('#post', {{opacity:0, y:-110, scale:.7, filter:'blur(12px)'}}, {{opacity:1, y:0, scale:1, filter:'blur(0px)', duration:.6, ease:'back.out(1.5)'}}, {click + 0.12:.3f});")
js.append(f"tl.fromTo('#psheen', {{xPercent:-120}}, {{xPercent:420, duration:.8, ease:'power2.inOut'}}, {click + 0.45:.3f});")
js.append(f"tl.fromTo('#pheart', {{scale:0}}, {{scale:1, duration:.35, ease:'back.out(3)'}}, {click + 0.55:.3f});")
js.append(f"tl.to('#cur', {{x:1100, y:900, opacity:0, duration:.5, ease:'power2.in', immediateRender:false}}, {click + 0.3:.3f});")
for k in range(0, len(TYPED), 2):
    sfx.append(("click_002", times[k] - 0.02, 0.1))
sfx += [("arrow-whoosh", c0 - 0.05, 0.25), ("click_002", click, 0.45), ("explainer-light-pop-whoosh", click + 0.1, 0.35), ("pluck_001", click + 0.55, 0.25)]

# ---------------------------------------------------------------- punch-ins: alternate 1.0 / 1.15 at every cut and a few phrase breaks
edges = sorted(set([0.55] + [s["start"] for s in SEGS[1:]] + [t(12) - 0.05, t(17) - 0.05, t(55) - 0.05, t(65) - 0.05])) + [DUR]
cam = []
for n, (a, b) in enumerate(zip(edges, edges[1:])):
    z = 1.0 if n % 2 == 0 else 1.15
    cam.append(f"tl.fromTo('#cam', {{scale:{z}}}, {{scale:{z * 1.02:.4f}, duration:{b - a:.3f}, ease:'none', immediateRender:false}}, {a:.3f});")

sfx_html = "".join(f'<audio id="sfx{n}" src="assets/audio/sfx/{f}.wav" data-start="{max(0, a):.3f}" data-track-index="{20 + n}" data-volume="{v}"></audio>' for n, (f, a, v) in enumerate(sorted(sfx, key=lambda x: x[1])))

page = open("edit/template.html").read()
page = (page.replace("{{DUR}}", f"{DUR:.3f}").replace("{{OX}}", f"{FACE_CX * 1080:.0f}px").replace("{{OY}}", f"{FACE_CY * 1920:.0f}px")
        .replace("{{CAPS}}", caps).replace("{{BANNER}}", BANNER.replace("{HB}", f"{hook_end + 0.5:.3f}"))
        .replace("{{DOC_START}}", f"{d0:.3f}").replace("{{DOC_DUR}}", f"{d1 - d0:.3f}")
        .replace("{{BOX_START}}", f"{c0:.3f}").replace("{{BOX_DUR}}", f"{DUR - c0:.3f}")
        .replace("{{SFX}}", sfx_html).replace("{{JS}}", "\n".join(js + cam)))
open("index.html", "w").write(page)
import subprocess, os
subprocess.run(["node", os.path.expanduser("~/.claude/skills/hyperframes-audio/scripts/carve.mjs"), "--comp", "index.html", "--bed", "bgm", "--voice", "aroll"], check=True, capture_output=True)
print(f"index.html: {len(groups)} captions, {len(sfx)} sfx, {DUR:.2f}s")
