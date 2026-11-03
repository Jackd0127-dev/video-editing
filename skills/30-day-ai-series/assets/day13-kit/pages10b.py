# ================================================================= Day 10, round 2 (Jack's notes, references/day10-audit.md): the video is mostly
# him with captions. Graphics are cinematic glass overlays on his footage (below his chin; captions sit above his head),
# places are real footage (Pexels, assets/video/br), "one take, one camera" is a short character animation page, and the
# content orbits his head at the end. Paper pages only for the day card, the studio animation and the end card.
VTRACK = [7]


def vtag(vid_id, src, start, dur, cls, style="", media=0.0):
    VTRACK[0] += 1
    return (f'<video id="{vid_id}" class="clip {cls}" src="{src}" data-start="{start:.3f}" data-duration="{dur:.3f}" '
            f'data-media-start="{media:.3f}" data-track-index="{VTRACK[0]}" muted playsinline style="{style}"></video>')


def g_in(sel, at, y=60, d=0.5):
    ft(sel, at, {"opacity": 0, "y": y, "scale": 0.96, "filter": "blur(12px)"}, {"opacity": 1, "y": 0, "scale": 1, "filter": "blur(0px)"}, d, "expo.out")


def g_out(sel, at, y=30, d=0.32):
    to(sel, at, {"opacity": 0, "y": y, "filter": "blur(10px)"}, d, "power2.in")


def hold_cam(a, b, z=1.0, ox=540, oy=860):
    """Keep the camera steady while an overlay sits under his chin (captions stay above his head)."""
    CAMFIX.append((a, b))
    CAMMAP.append((a, b, z, z * 1.02, ox, oy))
    CAPFORCE.append((a, b, 0.22 * 1920))  # captions above his head while the overlay sits under his chin
    CAMJS.append(f"tl.fromTo('#cam', {{scale:{z}, transformOrigin:'{ox}px {oy}px'}}, {{scale:{z * 1.02:.4f}, duration:{b - a:.3f}, ease:'none', immediateRender:false}}, {a:.3f});")


def glass_watch(sid, x, y, label="minutes"):
    return f"""<div class="gl sw2" id="{sid}" style="left:{x}px;top:{y}px;opacity:0"><svg viewBox="0 0 232 232"><circle class="rim" cx="116" cy="116" r="100"/><circle class="arc" id="{sid}-a" cx="116" cy="116" r="100" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"/></svg><div class="rd" id="{sid}-t">0:00</div><div class="lb">{label}</div></div>"""


# ---------------------------------------------------------------- hooks
def hook_v1b():
    """'Stop asking Claude to edit your videos and instead ask it this.' — a glass editing timeline of his real episodes
    rises under his chin, the playhead runs; 'instead' slices through it; 'ask it this' = a glass Claude tile."""
    i_ed, i_in, i_ask = w("edit your videos"), w("instead"), w("ask it this")
    a, out = t(i_ed) - 0.25, te(i_ask + 2) + 0.35
    trk = "".join(f'<i style="background-image:url({DAYS[k]})"></i>' for k in (8, 7, 6, 5, 4))
    OV.append(f"""<div class="gl tlb" id="h1-tl" style="opacity:0"><div class="gk">editing</div><div class="trk">{trk}</div><i class="ph" id="h1-ph" style="left:40px"></i><i class="sl" id="h1-sl"></i></div>
  <div class="gl askt" id="h1-q" style="opacity:0">{CLAUDE.format(120)}<span>?</span></div>""")
    g_in("#h1-tl", a)
    ft("#h1-ph", a + 0.2, {"x": 0}, {"x": 820}, max(0.8, t(i_in) - a - 0.1), "none")
    ft("#h1-sl", t(i_in) - 0.05, {"scaleX": 0}, {"scaleX": 1}, 0.25, "power3.out")
    to("#h1-tl", t(i_in) + 0.25, {"opacity": 0, "y": 40, "scale": 0.94, "filter": "blur(12px)"}, 0.35, "power2.in")
    g_in("#h1-q", t(i_ask) - 0.12, 80, 0.45)
    ft("#h1-q img", t(i_ask) + 0.2, {"rotation": 0}, {"rotation": 180}, 0.7, "power2.inOut")
    g_out("#h1-q", out)
    hold_cam(a, out + 0.3)
    sfx.extend([("fast-whoosh", a, 0.18), ("scratch_002", t(i_in), 0.2), ("hard-pop-click", t(i_ask), 0.24)])


def hook_v2b():
    """V2 'Everybody is talking about how Claude can edit your videos, but no one is talking about this.' — glass hashtag
    chips about Claude video editing drift in all round him; 'but no one' blurs them away under a vignette; 'this' = a
    glass Claude '?' tile."""
    i_h, i_no = w("how claude"), w("no one")
    i_this = w("about this", t(i_no)) + 1
    TAGS = [("#claudeedit", 60, 1120), ("#aivideoediting", 520, 1150), ("#editwithclaude", 120, 1260), ("#autocaptions", 600, 1290),
            ("#claudecode", 70, 1400), ("#videoediting", 560, 1430), ("#contentcreator", 250, 1540)]
    OV.append("".join(f'<div class="gl tagx" id="h2b-{k}" style="left:{x}px;top:{y}px;opacity:0">{ic("film", 40, "#fbf9f5")}{tg}</div>' for k, (tg, x, y) in enumerate(TAGS)))
    OV.append(f'<div class="vig" id="h2b-v"></div><div class="gl askt" id="h2b-q" style="opacity:0">{CLAUDE.format(120)}<span>?</span></div>')
    a = t(i_h) - 0.2
    span = max(0.8, t(i_no) - a - 0.2)
    for k in range(len(TAGS)):
        at = a + span * k / len(TAGS)
        ft(f"#h2b-{k}", at, {"opacity": 0, "y": 40, "scale": 0.8, "filter": "blur(10px)"}, {"opacity": 1, "y": 0, "scale": 1, "filter": "blur(0px)"}, 0.4, "expo.out")
        ft(f"#h2b-{k}", at + 0.4, {"x": 0}, {"x": (k % 2 * 2 - 1) * 24, "yoyo": True, "repeat": 3}, 0.9, "sine.inOut", False)
        sfx.append(("dry-pop-alert" if k % 2 else "click_004", at, 0.12))
    b = t(i_no) - 0.08
    for k in range(len(TAGS)):
        to(f"#h2b-{k}", b + k * 0.03, {"opacity": 0, "filter": "blur(16px)", "scale": 0.9}, 0.35)
    ft("#h2b-v", b, {"opacity": 0}, {"opacity": 1}, 0.4, "power2.out")
    g_in("#h2b-q", t(i_this) - 0.15, 80, 0.45)
    out = te(i_this) + 0.4
    to("#h2b-v", out, {"opacity": 0}, 0.3)
    g_out("#h2b-q", out)
    hold_cam(a, out + 0.3)
    sfx.extend([("glitch_002", b, 0.16), ("hard-pop-click", t(i_this), 0.24)])


# ---------------------------------------------------------------- the month
def month_ov(var):
    """'(get) a month's worth of content (in/with) just 20 to 30 minutes of filming.' — a glass month fills with his real
    episodes; a glass stopwatch runs to 30:00 beside it."""
    i_m = w("month's worth")
    i_20 = w("20 to 30", t(i_m))
    i_f = w("filming", t(i_m))
    a, out = t(i_m) - 0.3, te(i_f) + 0.35
    cells = "".join(f'<div class="c"><img id="m2-{k}" src="{DAYS[(k * 2) % 9]}"/></div>' for k in range(28))
    OV.append(f"""<div class="gl mo2" id="m2" style="opacity:0;right:{110 if var == 'A' else 330}px"><div class="top"><span class="gh" style="font-size:52px">a month</span><span class="gk">of content</span></div><div class="gd">{cells}</div></div>
  {glass_watch('m2-sw', 760 if var == 'A' else 760, 1240 if var == 'A' else 1180, 'filming')}""")
    g_in("#m2", a)
    span = max(0.9, t(i_20) - a - 0.5)
    order = list(range(28)) if var == "A" else [r * 7 + c for c in range(7) for r in range(4)]
    for n, k in enumerate(order):
        ft(f"#m2-{k}", a + 0.3 + span * n / 28, {"opacity": 0, "scale": 1.3}, {"opacity": 1, "scale": 1}, 0.2, "power2.out")
        if n % 4 == 0:
            sfx.append(("click_004", a + 0.3 + span * n / 28, 0.05))
    b = t(i_20) - 0.2
    if var == "A":
        to("#m2", b, {"x": -110}, 0.4, "power3.inOut")
    g_in("#m2-sw", b, 40, 0.4)
    watch_run("m2-sw", b + 0.25, max(0.6, te(i_f) - b - 0.25), 0, 30)
    g_out("#m2", out)
    g_out("#m2-sw", out)
    hold_cam(a, out + 0.3)


def twenty_ov():
    """'So we have 20 minutes.' — a glass stopwatch runs to 20:00."""
    i = w("we have 20")
    a, out = t(i) - 0.35, te(w("minutes", t(i))) + 0.3
    OV.append(glass_watch("tw", 410, 1150, "your time"))
    g_in("#tw", a, 50, 0.4)
    watch_run("tw", a + 0.3, max(0.6, out - a - 0.45), 0, 20)
    g_out("#tw", out)
    hold_cam(a, out + 0.3)


def pg_studio():
    """V1 'I want you to do one take with one camera.' — a little figure walks into a studio carrying his camera, sets it up on
    the tripod, sits down, and the REC light comes on."""
    i0, i_t, i_c = w("i want you to do one"), w("one take"), w("one camera")
    s, e = t(i0) - 0.1, cover_cut(te(i_c + 1) + 0.35)
    FIG = """<g id="st-fig"><g id="st-legL"><path class="ln" d="M0 -40 L-12 62"/></g><g id="st-legR"><path class="ln" d="M0 -40 L14 62"/></g>
      <path class="ln" d="M0 -40 L0 -138"/><circle class="fl" cx="0" cy="-176" r="36"/>
      <g id="st-arm"><path class="ln" d="M0 -120 L44 -78"/><g id="st-carry"><rect class="fl" x="34" y="-108" width="56" height="40" rx="8"/><path class="ln" d="M40 -70 L22 10 M60 -70 L60 14 M80 -70 L98 10" style="stroke-width:6"/></g></g>
      <path class="ln" d="M0 -120 L-40 -76"/></g>"""
    TRI = """<g id="st-tri"><path id="st-t0" class="ln" d="M700 1060 L640 1250"/><path id="st-t1" class="ln" d="M700 1060 L760 1250"/><path id="st-t2" class="ln" d="M700 1060 L700 1250"/>
      <g id="st-cam"><rect class="fl" x="640" y="980" width="130" height="86" rx="16"/><circle cx="672" cy="1023" r="26" fill="#5d5650" stroke="#fbf9f5" stroke-width="5"/><circle id="st-rec" cx="752" cy="996" r="9" fill="#e8e2d8"/></g></g>"""
    s = scene("st", s, e, f"""
{head('st', 'one take,', 'one camera', 200, 120)}
  <svg class="studio" viewBox="0 0 1080 1920">
    <rect class="pp" id="st-bg" x="150" y="520" width="780" height="730" rx="18"/>
    <path class="ln" d="M90 1250 L990 1250"/>
    <g id="st-light"><path class="beam" id="st-beam" d="M230 640 L520 1250 L120 1250 Z"/><path class="ln" d="M180 1250 L180 700"/><rect class="lt" x="120" y="600" width="140" height="110" rx="14"/></g>
    <g id="st-chair"><path class="ln" d="M380 1120 L470 1120 M395 1120 L385 1250 M455 1120 L465 1250 M470 1120 L476 1010"/></g>
    {TRI}
    <g id="st-figw" transform="translate(-120 1132) scale(1.9)">{FIG}</g>
  </svg>
  <span class="tag7" id="st-tg" style="left:330px;top:1340px">{ic('cam', 44, '#fbf9f5')} 1 take · 1 camera</span>""")
    rev("#st-a", s + 0.02, 14)
    rev("#st-h", t(i_c) - 0.05, 22)
    ft("#st-bg, #st-light", s + 0.02, {"opacity": 0}, {"opacity": 1}, 0.3)
    ft("#st-beam", s + 0.1, {"opacity": 0}, {"opacity": 1, "yoyo": True, "repeat": 1}, 0.12, "steps(2)")
    walk_end = s + 0.95
    ft("#st-figw", s + 0.05, {"x": -120}, {"x": 560}, walk_end - s - 0.05, "power1.out")
    steps_ = max(4, int((walk_end - s) / 0.16))
    for k in range(steps_):
        at = s + 0.05 + k * 0.16
        ft("#st-legL", at, {"rotation": 0, "svgOrigin": "0 -40"}, {"rotation": 22 if k % 2 else -22, "svgOrigin": "0 -40"}, 0.16, "sine.inOut", None if k == 0 else False)
        ft("#st-legR", at, {"rotation": 0, "svgOrigin": "0 -40"}, {"rotation": -22 if k % 2 else 22, "svgOrigin": "0 -40"}, 0.16, "sine.inOut", None if k == 0 else False)
        sfx.append(("tick_002", at, 0.05))
    to("#st-legL, #st-legR", walk_end, {"rotation": 0}, 0.1)
    # set the camera up on the tripod
    st("#st-tri", s, {"opacity": 0})
    put = walk_end + 0.05
    st("#st-tri", put, {"opacity": 1})
    for k in range(3):
        ft(f"#st-t{k}", put + k * 0.05, {"scaleY": 0, "svgOrigin": "700 1060"}, {"scaleY": 1, "svgOrigin": "700 1060"}, 0.2, "power2.out", False)
    to("#st-carry", put, {"opacity": 0}, 0.1)
    ft("#st-cam", put + 0.1, {"y": -60, "opacity": 0}, {"y": 0, "opacity": 1}, 0.25, "back.out(2)", False)
    sfx.append(("click_002", put + 0.15, 0.2))
    # walk back to the chair and sit
    sit = put + 0.45
    to("#st-figw", sit, {"x": 430}, 0.35, "power1.inOut")
    to("#st-figw", sit + 0.35, {"y": -14}, 0.25, "power2.out")
    to("#st-legL", sit + 0.35, {"rotation": -82}, 0.25)
    to("#st-legR", sit + 0.35, {"rotation": -70}, 0.25)
    to("#st-arm", sit + 0.35, {"rotation": 30, "svgOrigin": "0 -120"}, 0.25)
    ft("#st-rec", sit + 0.6, {"fill": "#e8e2d8"}, {"fill": "#fbf9f5", "opacity": 0.2, "yoyo": True, "repeat": 5}, 0.14, "steps(1)")
    ft("#st-tg", t(i_t) + 0.1, {"opacity": 0, "scale": 1.6, "rotation": -10}, {"opacity": 1, "scale": 1, "rotation": -3}, 0.3, "back.out(2)")
    sfx.extend([("switch_003", sit + 0.6, 0.2), ("dry-pop-alert", t(i_t) + 0.1, 0.2)])


def take_ov():
    """V2 'I want you to do one take with one camera.' — a glass REC chip."""
    i_t, i_c = w("one take"), w("one camera")
    a, out = t(i_t) - 0.2, te(i_c + 1) + 0.3
    OV.append(f'<div class="gl chip" id="tk3" style="left:250px;top:1220px;opacity:0"><i id="tk3-r" style="width:22px;height:22px;border-radius:50%;background:#fbf9f5;display:block"></i>REC · 1 take · 1 camera</div>')
    g_in("#tk3", a, 40, 0.4)
    ft("#tk3-r", a + 0.3, {"opacity": 1}, {"opacity": 0.2, "yoyo": True, "repeat": 5}, 0.18, "steps(1)")
    g_out("#tk3", out)
    hold_cam(a, out + 0.3)
    sfx.append(("switch_003", a + 0.1, 0.18))


# ---------------------------------------------------------------- questions
def qlist_ov():
    """'For example, what you do, who you are, why you're posting content.' — a clean glass list, each question on its word."""
    QS = [("what you do", "What do you do?"), ("who you are", "Who are you?"), ("why you're posting", "Why do you post?")]
    i0 = w("for example")
    out = te(w("posting content") + 1) + 0.35
    OV.append('<div class="gl ql2" id="ql">' + "".join(f'<div class="qi" id="ql-{k}" style="opacity:0"><span>Q{k + 1}</span><b>{q}</b></div>' for k, (_, q) in enumerate(QS)) + '</div>')
    for k, (ph, _) in enumerate(QS):
        at = t(w(ph, t(i0))) - 0.12
        ft(f"#ql-{k}", at, {"opacity": 0, "x": -60, "filter": "blur(10px)"}, {"opacity": 1, "x": 0, "filter": "blur(0px)"}, 0.45, "expo.out")
        sfx.append(("dry-pop-alert", at, 0.16))
    to("#ql", out, {"opacity": 0, "y": 30, "filter": "blur(10px)"}, 0.32, "power2.in")
    hold_cam(t(w(QS[0][0], t(i0))) - 0.2, out + 0.3)


QS100 = ["What do you do?", "Who is it for?", "Why did you start?", "What's your biggest mistake?", "What do people get wrong?",
         "What's one tip you'd give?", "What does a normal day look like?", "What's the hardest part?", "Why should people care?",
         "What would you do differently?", "What's your best result?", "What tools do you use?", "What surprised you most?",
         "What do you wish you knew?", "What's next for you?"]


def hundred_ov():
    """'Then literally ask it to make a full list of a hundred different questions, almost like a Q&A.' — a glass list that
    scrolls smoothly while the count runs to 100."""
    i_mk, i_h = w("ask it to make"), w("hundred")
    i_qa = w("q&a", t(i_h))
    a, out = t(i_mk) - 0.15, te(i_qa) + 0.4
    rows = "".join(f'<div class="r"><em>Q{k + 1}</em>{esc(QS100[k % len(QS100)])}</div>' for k in range(100))
    OV.append(f"""<div class="gl sc2" id="hd" style="opacity:0"><div class="hd"><span class="gh" style="font-size:46px">questions</span><span class="gh" style="font-size:46px"><span id="hd-n">0</span><span class="gk" style="margin-left:8px">/ 100</span></span></div>
  <div class="scw"><div class="in" id="hd-in">{rows}</div></div></div>""")
    g_in("#hd", a)
    d = max(1.0, te(i_qa) - t(i_h) + 0.2)
    count_js("hd-n", 0, 100, t(i_h) - 0.15, d)
    ft("#hd-in", a + 0.3, {"y": 0}, {"y": -(100 * 64 - 380)}, out - a - 0.3, "power1.inOut")
    sfx.extend([("tick_002", t(i_h) + k * 0.2, 0.05) for k in range(int(d / 0.2))])
    g_out("#hd", out)
    hold_cam(a, out + 0.3)


# ---------------------------------------------------------------- places: real footage
PLACES = [("river", "assets/video/br/river.mp4"), ("field", "assets/video/br/field.mp4"), ("lake", "assets/video/br/lake.mp4")]


def places_cards():
    """V1 'go find some river, find some field, find some lake' — real footage of each place rises as a tall screen over him
    on its word, with an italic label; 'set your camera up … 15, 20 minutes, maybe half an hour' = a glass stopwatch."""
    idx = [w(p) for p, _ in PLACES]
    i_s = w("set your camera up")
    i_15 = w("15", t(i_s))
    i_20 = w("20", t(i_15))
    i_hh = w("half an hour", t(i_15))
    end_cards = t(i_s) + 0.3
    X = [60, 390, 720]
    for k, ((name, src), i) in enumerate(zip(PLACES, idx)):
        a = t(i) - 0.35
        VL.append(vtag(f"pc-{name}", src, a, end_cards - a + 0.4, "lc", f"left:{X[k]}px;top:1060px"))
        OV.append(f'<span class="lcl" id="pc-l{k}" style="left:{X[k] + 30}px;top:1500px">{name}.</span>')
        ft(f"#pc-{name}", a, {"opacity": 0, "y": 160, "rotation": (k - 1) * 6, "scale": 0.85}, {"opacity": 1, "y": 0, "rotation": (k - 1) * 3, "scale": 1}, 0.5, "expo.out")
        ft(f"#pc-l{k}", a + 0.2, {"opacity": 0, "y": 20, "filter": "blur(8px)"}, {"opacity": 1, "y": 0, "filter": "blur(0px)"}, 0.35, "power2.out")
        to(f"#pc-{name}, #pc-l{k}", end_cards + k * 0.05, {"opacity": 0, "y": 80, "filter": "blur(10px)"}, 0.35, "power2.in")
        sfx.append(("arrow-whoosh", a, 0.16))
    OV.append(glass_watch("pc-sw", 410, 1150, "film yourself"))
    g_in("#pc-sw", t(i_15) - 0.35, 40, 0.4)
    watch_run("pc-sw", t(i_15) - 0.1, max(0.4, t(i_20) - t(i_15)), 0, 15, 0, 0.5)
    watch_run("pc-sw", t(i_20) - 0.05, max(0.3, t(i_hh) - t(i_20) - 0.1), 15, 20, 0.5, 0.67)
    watch_run("pc-sw", t(i_hh) - 0.05, max(0.4, te(i_hh + 2) - t(i_hh)), 20, 30, 0.67, 1.0)
    g_out("#pc-sw", te(i_hh + 2) + 0.3)
    hold_cam(t(idx[0]) - 0.4, te(i_hh + 2) + 0.6)


def places_full():
    """V2: each place fills the screen as a real cutaway on its word (his voice over it), then back to him for 'set your
    camera up'; the stopwatch is a glass chip."""
    idx = [w(p) for p, _ in PLACES]
    i_s = w("set your camera up")
    i_15 = w("15", t(i_s))
    i_hh = w("half an hour", t(i_15))
    starts = [t(i) - 0.3 for i in idx] + [t(i_s) - 0.1]
    for k, (name, src) in enumerate(PLACES):
        a, b = starts[k], starts[k + 1]
        BROLL.append({"file": src, "start": a, "end": b, "media": 0.3})
        OV.append(f'<span class="lcl" id="pf-l{k}" style="left:90px;top:1330px;font-size:120px">{name}.</span>')
        ft(f"#pf-l{k}", a + 0.08, {"opacity": 0, "y": 30, "filter": "blur(10px)"}, {"opacity": 1, "y": 0, "filter": "blur(0px)"}, 0.35, "power2.out")
        to(f"#pf-l{k}", b - 0.12, {"opacity": 0}, 0.1)
    OV.append(glass_watch("pf-sw", 410, 1150, "film yourself"))
    g_in("#pf-sw", t(i_15) - 0.35, 40, 0.4)
    watch_run("pf-sw", t(i_15) - 0.1, max(0.6, te(i_hh + 2) - t(i_15)), 0, 30)
    g_out("#pf-sw", te(i_hh + 2) + 0.3)
    hold_cam(t(i_15) - 0.4, te(i_hh + 2) + 0.6)


# ---------------------------------------------------------------- the workflow
def drop_ov():
    """'drop your full footage into Claude.' — a glass file chip slides across and drops into a glass Claude tile."""
    i_d = w("drop your full footage")
    i_c = w("claude", t(i_d))
    a, out = t(i_d) - 0.3, te(i_c) + 0.45
    OV.append(f"""<div class="gl chip" id="dp2-f" style="left:80px;top:1240px;opacity:0">{ic('film', 46, '#fbf9f5')}full-video.mov<span class="gk" style="margin-left:6px">20–30 min</span></div>
  <div class="gl askt" id="dp2-c" style="left:720px;top:1170px;width:240px;height:240px;opacity:0">{CLAUDE.format(110)}</div>""")
    g_in("#dp2-f", a, 40, 0.4)
    g_in("#dp2-c", a + 0.1, 40, 0.4)
    to("#dp2-f", t(i_d) + 0.25, {"x": 560, "y": -10, "scale": 0.4, "opacity": 0}, 0.55, "power3.in")
    ft("#dp2-c", t(i_d) + 0.75, {"scale": 1}, {"scale": 1.12, "yoyo": True, "repeat": 1}, 0.14, "power2.out", False)
    ft("#dp2-c img", t(i_c) - 0.05, {"rotation": 0}, {"rotation": 120}, 0.6, "power2.inOut")
    g_out("#dp2-c", out)
    hold_cam(a, out + 0.3)
    sfx.extend([("arrow-whoosh", t(i_d) + 0.25, 0.18), ("drop_002", t(i_d) + 0.78, 0.26)])


def skill_ov():
    """'use this skill that's gonna transcribe every single word with an exact time stamp' — a glass transcript of his real
    words from this video, lighting up word by word, real time stamps landing on 'time stamp'."""
    i_s = w("skill")
    i_tr = w("transcribe", t(i_s))
    i_ts = w("time stamp", t(i_s)) if has("time stamp") else w("timestamp", t(i_s))
    i_tse = i_ts + 1 if has("time stamp") else i_ts
    a, out = t(i_s) - 0.3, te(i_tse) + 0.4
    LINES = [("stop asking Claude to edit your videos", "stop asking"), ("so we have 20 minutes", "we have 20"),
             ("I want you to do one take with one camera", "one take"), ("get Claude to ask you questions", "get claude to ask"),
             ("a full list of a hundred different questions", "hundred")]
    rows = ""
    for k, (txt, ph) in enumerate(LINES):
        ts = t(w(ph)) if has(ph) else 0.0
        rows += f'<div class="ln"><em id="sk2-e{k}">{int(ts // 60):02d}:{ts % 60:04.1f}</em><span>{typed_words(f"sk2{k}w", txt)}</span></div>'
    OV.append(f"""<div class="gl tr2" id="sk2" style="opacity:0"><div class="hd">{CLAUDE.format(46)}<span class="gh" style="font-size:40px">skill</span><span class="gk" style="margin-left:auto">transcript</span></div><div class="in">{rows}</div></div>""")
    g_in("#sk2", a)
    st(".tr2 em", a, {"opacity": 0})
    t0, d = t(i_tr) - 0.1, max(1.2, t(i_ts) - t(i_tr))
    for k, (txt, _) in enumerate(LINES):
        n = len(txt.split())
        for j in range(n):
            ft(f"#sk2{k}w{j}", t0 + d * (k + j / n) / len(LINES), {"opacity": 0.2}, {"opacity": 1}, 0.08, "none")
    for k in range(len(LINES)):
        ft(f"#sk2-e{k}", t(i_ts) - 0.1 + k * 0.07, {"opacity": 0, "scale": 0.4}, {"opacity": 1, "scale": 1}, 0.22, "back.out(2.4)", False)
        sfx.append(("tick_002", t(i_ts) - 0.1 + k * 0.07, 0.1))
    g_out("#sk2", out)
    hold_cam(a, out + 0.3)


def clips_ov():
    """'create engaging social media clips between 20 and 45 seconds that works for someone who's never seen you before' —
    his real episodes drop in as vertical clips with their lengths; 'never seen you before' = a glass 'new viewers' tag."""
    i_c = w("it'll create")
    i_cl = w("social media clips", t(i_c)) + 2
    i_20 = w("20 and 45", t(i_c))
    i_nv = w("never seen you", t(i_c))
    a, out = t(i_cl) - 0.4, te(i_nv + 3) + 0.35
    LEN = ["0:20", "0:34", "0:45", "0:27"]
    X = [70, 300, 530, 760]
    OV.append("".join(f'<div class="cl2" id="c2-{k}" style="left:{X[k]}px;top:1140px;opacity:0"><img src="{DAYS[8 - k]}"/><span id="c2-l{k}" style="opacity:0">{LEN[k]}</span></div>' for k in range(4)))
    OV.append(f'<div class="gl tagx" id="c2-t" style="left:250px;top:1520px;opacity:0">{ic("people", 40, "#fbf9f5")}made for new viewers</div>')
    for k in range(4):
        at = a + k * 0.12
        ft(f"#c2-{k}", at, {"opacity": 0, "y": 200, "rotation": (k - 1.5) * 8, "scale": 0.7}, {"opacity": 1, "y": 0, "rotation": (k - 1.5) * 2.5, "scale": 1}, 0.5, "expo.out")
        ft(f"#c2-l{k}", t(i_20) - 0.05 + k * 0.08, {"opacity": 0, "y": 8}, {"opacity": 1, "y": 0}, 0.2, "power2.out", False)
        sfx.append(("drop_002", at + 0.25, 0.1))
    g_in("#c2-t", t(i_nv) - 0.1, 30, 0.4)
    for k in range(4):
        to(f"#c2-{k}", out + k * 0.04, {"opacity": 0, "y": 80, "filter": "blur(10px)"}, 0.3, "power2.in")
    g_out("#c2-t", out)
    hold_cam(a, out + 0.35)


def hooks_ov(long):
    """'extract the most engaging hooks that you said (across your full 20 to 30 minute video)' — a glass panel: the long
    recording's waveform with the hook moments lit, his real hooks listed under it."""
    i_x = w("extract")
    i_h = w("engaging hooks", t(i_x)) + 1
    i_end = (w("minute video", t(i_x)) + 1) if long and has("minute video") else w("you said", t(i_x)) + 1
    a, out = t(i_x) - 0.25, te(i_end) + 0.35
    if has("last tip") and t(w("last tip")) > t(i_x):
        out = min(out, t(w("last tip")) - 0.45)
    wv = "".join(f'<i id="hw-{k}" style="height:{int(20 + 75 * abs(math.sin(k * 1.3 + 1)) * (0.4 + 0.6 * abs(math.cos(k * 0.23))))}%"></i>' for k in range(70))
    rows = "".join(f'<div class="row" id="hr-{k}" style="opacity:0"><img src="{DAYS[d - 1]}"/><b>{esc(txt)}</b></div>' for k, (d, txt) in enumerate(HOOKS[:3]))
    OV.append(f"""<div class="gl hk2" id="hk2" style="opacity:0"><div style="display:flex;justify-content:space-between;align-items:baseline"><span class="gh" style="font-size:46px">best hooks</span><span class="gk">20–30 min video</span></div><div class="wv">{wv}</div>{rows}</div>""")
    g_in("#hk2", a)
    LIT = [9, 31, 54]
    span = max(0.9, te(i_end) - t(i_h))
    for k in range(3):
        at = t(i_h) - 0.2 + span * k / 3
        ft(f"#hw-{LIT[k]}, #hw-{LIT[k] + 1}, #hw-{LIT[k] + 2}", at, {"backgroundColor": "rgba(255,255,255,.45)", "scaleY": 1}, {"backgroundColor": "#fbf9f5", "scaleY": 1.3}, 0.2, "back.out(2)")
        ft(f"#hr-{k}", at + 0.12, {"opacity": 0, "y": 30, "filter": "blur(8px)"}, {"opacity": 1, "y": 0, "filter": "blur(0px)"}, 0.4, "expo.out")
        sfx.append(("dry-pop-alert", at + 0.12, 0.14))
    g_out("#hk2", out)
    hold_cam(a, out + 0.3)


def planner_ov():
    """'make a full schedule with every single video so you can almost tell a story across a week, (a few weeks,) a month' —
    a glass planner: the first week fills with his real episodes and a glowing story line threads them, then the weeks fill."""
    i_s = w("full schedule")
    i_st = w("story", t(i_s))
    i_wk = w("a week", t(i_s))
    i_fw = w("few weeks", t(i_s)) if has("few weeks") else None
    i_m = w("a month", t(i_wk))
    a, out = t(i_s) - 0.3, te(i_m + 1) + 0.45
    DN = "".join(f"<span>{d}</span>" for d in ("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"))
    cells = "".join(f'<div class="c"><b>{k + 1}</b><img id="pl2-{k}" src="{DAYS[(k * 4 + 8) % 9]}"/></div>' for k in range(28))
    W = 940 - 48
    cw = (W - 60) / 7
    ch = cw * 13 / 9
    y1 = 24 + 52 + 14 + 28 + 8 + ch / 2
    xs = [24 + cw / 2 + k * (cw + 10) for k in range(7)]
    path = "M" + " L".join(f"{x:.0f} {y1 + (14 if k % 2 else -14):.0f}" for k, x in enumerate(xs))
    OV.append(f"""<div class="gl pl2" id="pl2" style="opacity:0"><div class="top"><span class="gh" style="font-size:48px">your posting plan</span><span class="gk">1 a day</span></div>
  <div class="dn">{DN}</div><div class="gd">{cells}</div><svg><path id="pl2-p" d="{path}"/></svg></div>""")
    g_in("#pl2", a)

    def fill(ks, t0, d):
        for n, k in enumerate(ks):
            ft(f"#pl2-{k}", t0 + d * n / max(1, len(ks)), {"opacity": 0, "scale": 1.35}, {"opacity": 1, "scale": 1}, 0.2, "power2.out")
            if n % 2 == 0:
                sfx.append(("click_004", t0 + d * n / max(1, len(ks)), 0.05))
    fill(range(7), a + 0.35, max(0.6, t(i_st) - a - 0.5))
    ft("#pl2-p", t(i_st) - 0.1, {"strokeDashoffset": 2000}, {"strokeDashoffset": 0}, max(0.5, t(i_wk) - t(i_st) + 0.3), "power1.inOut")
    sfx.append(("scribble", t(i_st), 0.14))
    if i_fw is not None:
        fill(range(7, 21), t(i_fw) - 0.2, max(0.5, t(i_m) - t(i_fw)))
        fill(range(21, 28), t(i_m) - 0.1, 0.4)
    else:
        fill(range(7, 28), t(i_m) - 0.3, 0.6)
    g_out("#pl2", out)
    hold_cam(a, out + 0.3)


def hours_ov():
    """'So instead of spending hours every day editing, filming, planning content,' — glass bars, one per job, grow on their word."""
    i_sp = w("instead of spending")
    i_e = w("editing", t(i_sp))
    i_f = w("filming", t(i_e))
    i_p = w("planning", t(i_f))
    a, out = t(w("hours", t(i_sp))) - 0.3, te(i_p + 1) + 0.35
    ROWS = [("editing", i_e, 0.82, "2–3 h"), ("filming", i_f, 0.62, "1–2 h"), ("planning", i_p, 0.5, "1 h")]
    OV.append('<div class="gl hr2" id="hr2" style="opacity:0"><div style="display:flex;justify-content:space-between;align-items:baseline"><span class="gh" style="font-size:48px">every day</span><span class="gk">hours</span></div>'
              + "".join(f'<div class="r"><span>{n}</span><i id="hr2-{k}" style="width:{int(wd * 440)}px"></i></div>' for k, (n, _, wd, _) in enumerate(ROWS)) + '</div>')
    g_in("#hr2", a)
    st(".hr2 .r i", a, {"scaleX": 0})
    for k, (_, i, _, _) in enumerate(ROWS):
        ft(f"#hr2-{k}", t(i) - 0.1, {"scaleX": 0}, {"scaleX": 1}, 0.45, "expo.out", False)
        sfx.append(("tick_002", t(i), 0.14))
    g_out("#hr2", out)
    hold_cam(a, out + 0.3)


def once_ov():
    """'pick one time a month, one time a week, film for 20 to 30 minutes' — a glass chip flips month -> week, then a glass
    stopwatch runs to 30:00."""
    i_m = w("one time a month")
    i_w = w("one time a week", t(i_m))
    i_f = w("film for", t(i_w))
    i_end = w("minutes", t(i_f))
    OV.append(f'<div class="gl chip" id="on3" style="left:270px;top:1200px;opacity:0">{ic("cal", 46, "#fbf9f5")}<span id="on3-t">once a month</span></div>')
    g_in("#on3", t(i_m) - 0.15, 40, 0.4)
    text_at("on3-t", t(i_w) - 0.05, "once a week", "once a month")
    ft("#on3", t(i_w) - 0.05, {"rotationX": 0}, {"rotationX": 360}, 0.4, "power2.inOut", False)
    g_out("#on3", t(i_f) - 0.15)
    OV.append(glass_watch("on4", 410, 1150, "once"))
    g_in("#on4", t(i_f) - 0.1, 40, 0.4)
    watch_run("on4", t(i_f) + 0.15, max(0.6, te(i_end) - t(i_f) - 0.15), 0, 30)
    g_out("#on4", te(i_end) + 0.3)
    hold_cam(t(i_m) - 0.2, te(i_end) + 0.6)
    sfx.append(("click_004", t(i_w), 0.14))


def orbit_ov():
    """'(and you have all the content you need.) Claude will handle all of it.' — his real episodes fly in and orbit his head;
    a glass Claude tile lands on 'Claude'."""
    i0 = w("you have all") if has("you have all") else w("claude will handle")
    i_c = w("claude will handle")
    i_all = w("all of it", t(i_c)) + 2
    a, out = t(i0) - 0.2, te(i_all) + 0.45
    n = 8
    OV.append("".join(f'<div class="orb" id="ob-{k}"><img src="{DAYS[k % 9]}"/></div>' for k in range(n)))
    OV.append(f'<div class="gl askt" id="ob-c" style="left:420px;top:1230px;width:240px;height:240px;opacity:0">{CLAUDE.format(110)}</div>')
    CX, CY, RX, RY = 540, 820, 470, 150
    d = out - a
    js.append(f"""(function(){{ const o = {{a:0, r:0}}; const N = {n};
  const put = () => {{ for (let k = 0; k < N; k++) {{ const el = document.getElementById('ob-' + k); if (!el) continue;
      const th = o.a + k * 2 * Math.PI / N, s = Math.sin(th), c = Math.cos(th);
      const depth = (s + 1) / 2, sc = (0.55 + 0.45 * depth) * o.r;
      const x = {CX} + {RX} * c * o.r - 85, y = {CY} + {RY} * s - 150;
      const behind = s < 0 && Math.abs(c) < 0.45;
      el.style.transform = 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px) scale(' + sc.toFixed(3) + ') rotate(' + (c * -8).toFixed(1) + 'deg)';
      el.style.opacity = o.r <= 0.01 ? 0 : (behind ? 0 : (0.55 + 0.45 * depth));
      el.style.zIndex = s > 0 ? 9 : 6; }} }};
  tl.fromTo(o, {{a:0}}, {{a:{2 * math.pi * 1.1:.3f}, duration:{d:.3f}, ease:'none', immediateRender:false, onUpdate:put}}, {a:.3f});
  tl.fromTo(o, {{r:0}}, {{r:1, duration:.6, ease:'expo.out', immediateRender:false, onUpdate:put}}, {a:.3f});
  tl.to(o, {{r:0, duration:.35, ease:'power2.in', immediateRender:false, onUpdate:put}}, {out - 0.35:.3f});
}})();""")
    g_in("#ob-c", t(i_c) - 0.15, 60, 0.45)
    g_out("#ob-c", out)
    hold_cam(a, out + 0.3, 1.0, 540, 820)
    sfx.extend([("riser", a, 0.16), ("hard-pop-click", t(i_c), 0.24)])


def last_tip_ov():
    """'And the last tip is the most important, by the way.' — a glass star chip."""
    i = w("last tip")
    out = te(w("the way", t(i)) + 1) + 0.25
    OV.append(f'<div class="gl chip" id="lt2" style="left:200px;top:1210px;opacity:0">{ic("star", 46, "#fbf9f5")}the last tip matters most</div>')
    g_in("#lt2", t(i) - 0.1, 40, 0.4)
    ft("#lt2 svg", t(w("most important", t(i))) - 0.05, {"scale": 1, "rotation": 0}, {"scale": 1.35, "rotation": 72, "yoyo": True, "repeat": 1}, 0.18, "power2.out", False)
    g_out("#lt2", out)
    hold_cam(t(i) - 0.2, out + 0.3)
    sfx.append(("dry-pop-alert", t(i), 0.18))


def cta_ov(final):
    """'leave me a follow' — a glass Follow button; a cursor clicks it on 'follow'."""
    i = w("leave me a follow")
    i_f = i + 3
    out = DURATION - 0.1 if final else t(w("see you in")) + 0.05
    OV.append(f'<div class="gl chip" id="ct2" style="left:330px;top:1220px;opacity:0">{ic("user", 46, "#fbf9f5")}<span id="ct2-t">Follow</span></div>')
    OV.append(f'<div id="ct2-cur" class="cursor" style="z-index:30">{CUR}</div>')
    g_in("#ct2", t(i) - 0.1, 40, 0.4)
    click("#ct2-cur", 520, 1270, t(i_f) + 0.05, frm=(1000, 1700), leave=(1150, 1800))
    text_at("ct2-t", t(i_f) + 0.1, "Following ✓", "Follow")
    ft("#ct2", t(i_f) + 0.08, {"scale": 1}, {"scale": 0.92, "yoyo": True, "repeat": 1}, 0.08, "power2.out", False)
    if not final:
        g_out("#ct2", out)
    hold_cam(t(i) - 0.2, min(out + 0.3, AROLL_END))
