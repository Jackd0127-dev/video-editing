# ================================================================= Day 12: "can Claude start a business from nothing?" One version (Jack: one
# clean edit). Mostly his face with captions (day10-audit): glass overlays under his chin, his own laptop shots of what Claude
# made stay clean, paper pages only for the day card and the Day 13 end card.


def pg_day():
    """'Welcome to day twelve of thirty' — the series stat page; today's block lifts."""
    i = w("day twelve")
    s, e = t(i - 2) - 0.06, cover_cut(t(i + 3) + 0.6)
    scene("pday", s, e, f"""
  <div class="stack" style="left:0;right:0;top:600px">
    <span class="sm" style="font-size:56px">{words_in('pdw', i - 2, 2)}</span>
    <div class="row" style="align-items:flex-end;justify-content:center;margin-top:10px">
      <span id="pday-d" class="xb" style="font-size:230px;line-height:1">Day</span>
      <span id="pday-n" class="xb" style="font-size:230px;line-height:1;margin-left:40px">12</span>
    </div>
    <span class="sm" style="font-size:56px;margin-top:22px">{words_in('pdo', i + 1, 2)}</span>
  </div>
  <div id="pday-bar" class="bar big" style="top:1250px">{BLOCKS.replace('{p}', 'pday')}</div>""")
    ft("#pday-d", t(i) - 0.05, {"opacity": 0, "y": 60, "filter": "blur(14px)"}, {"opacity": 1, "y": 0, "filter": "blur(0px)"}, 0.4, "expo.out")
    slam("#pday-n", t(i + 1) - 0.05)
    ft("#pday-bar .seg", t(i + 1), {"scaleY": 0, "opacity": 0}, {"scaleY": 1, "opacity": 1, "stagger": 0.01}, 0.22, "power2.out")
    ft(", ".join(f"#pday-s{k}" for k in range(11)), t(i + 1) + 0.2, {"backgroundColor": "rgba(23,18,14,.14)"}, {"backgroundColor": INK, "stagger": 0.035}, 0.15)
    ft("#pday-s11", t(i + 3), {"backgroundColor": "rgba(23,18,14,.14)", "scaleY": 1}, {"backgroundColor": INK, "scaleY": 1.9}, 0.45, "back.out(2.2)")
    sfx.extend([("dry-pop-alert", t(i + 1), 0.24), ("pluck_001", t(i + 3), 0.26)])


def pg_end():
    """End card for the last beat ('…a little bit more interesting'): Day 13 / tomorrow, twelve blocks lit, zoom into today's.
    Kept short (day10-audit): he says 'see you on day thirteen' on his face, the card only closes the video."""
    s = AROLL_END - 1.3
    ZX, ZY = 90 + 11 * (SEG_W + 6) + SEG_W / 2, 1340 - 40 * 1.9 / 2
    scene("ed", s, DURATION, f"""
  <div id="ed-zoom" style="position:absolute;inset:0;transform-origin:{ZX:.1f}px {ZY:.1f}px">
    <div class="stack" style="left:0;right:0;top:560px">
      <span id="ed-sy" class="sm" style="font-size:56px">see you on</span>
      <div class="row" style="align-items:flex-end;justify-content:center;margin-top:6px">
        <span id="ed-day" class="xb" style="font-size:230px;line-height:1">Day</span>
        <span id="ed-n" class="xb" style="font-size:230px;line-height:1;margin-left:40px">13</span>
      </div>
      <span id="ed-tm" class="sm" style="font-size:52px;margin-top:20px">tomorrow</span>
    </div>
    <span id="ed-lbl" class="note" style="position:absolute;left:{90 + 11 * (SEG_W + 6) - 40:.0f}px;top:1186px">day 12 / 30</span>
    <div id="ed-bar" class="bar big" style="top:1300px">{BLOCKS.replace('{p}', 'ed')}</div>
  </div>""")
    rev("#ed-sy", s + 0.05, 14)
    rev("#ed-day", s + 0.2, 30)
    slam("#ed-n", s + 0.4)
    rev("#ed-tm", s + 0.7, 16)
    ft("#ed-bar .seg", s + 0.1, {"scaleY": 0, "opacity": 0}, {"scaleY": 1, "opacity": 1, "stagger": 0.01}, 0.25, "power2.out")
    lit = s + 0.9
    ft(", ".join(f"#ed-s{k}" for k in range(11)), lit - 0.3, {"backgroundColor": "rgba(23,18,14,.14)"}, {"backgroundColor": INK, "stagger": 0.04}, 0.18)
    ft("#ed-s11", lit, {"backgroundColor": "rgba(23,18,14,.14)", "scaleY": 1}, {"backgroundColor": INK, "scaleY": 1.9}, 0.5, "back.out(2.2)")
    ft("#ed-lbl", lit + 0.15, {"opacity": 0, "y": 12}, {"opacity": 1, "y": 0}, 0.35, "power2.out")
    zoom_at = DURATION - 1.4
    to("#ed-lbl", zoom_at, {"opacity": 0}, 0.3)
    ft("#ed-zoom", zoom_at, {"scale": 1, "x": 0, "y": 0}, {"scale": 60, "x": round(540 - ZX, 1), "y": round(960 - ZY, 1)}, 1.3, "power3.inOut")
    sfx.extend([("dry-pop-alert", s + 0.4, 0.24), ("pluck_001", lit, 0.3), ("riser", zoom_at + 0.25, 0.35), ("boom", DURATION - 0.12, 0.3)])


# ---------------------------------------------------------------- round 2 (Jack's notes): paper notes stuck beside him, placed off his
# face from the face track; ink-drawn ticks and crosses; no glass capsules.
FACES = []
for _ln in open(f"{D}/faces-2fps.txt"):
    _p = _ln.split()
    if _p[1] != "none":
        FACES.append(((int(_p[0][1:5]) - 1) / 2, *[float(v) for v in _p[1:5]]))
TICK_D, CROSS_D = "M4 13 L10 19 L22 4", "M5 5 L19 19 M19 5 L5 19"


def spot(a, b, w_, h_):
    """First note position (left, top) that stays clear of his face (and the caption band above it) between a and b."""
    fs = [f for f in FACES if a - 0.4 <= f[0] <= b + 0.4]
    boxes = [(x * 1080 - 30, y * 1920 - 60, (x + fw) * 1080 + 30, (y + fh) * 1920 + 40) for (_, x, y, fw, fh) in fs]
    ftop = min((bx[1] for bx in boxes), default=760)
    y0 = max(840, ftop + 20)
    cands = [(40, y0), (1040 - w_, y0), (40, y0 + 330), (1040 - w_, y0 + 330), (540 - w_ / 2, max((bx[3] for bx in boxes), default=1300) + 10)]
    for (x, y) in cands:
        if y + h_ > 1680:
            continue
        if all(x + w_ < bx[0] or x > bx[2] or y + h_ < bx[1] or y > bx[3] for bx in boxes):
            return x, y
    # close-ups: nothing is fully clear, so take the spot that covers the least of his face (usually low on his chest)
    cands += [(40, 1680 - h_), (1040 - w_, 1680 - h_), (540 - w_ / 2, 1680 - h_)]
    def cover(c):
        x, y = c
        return sum(max(0, min(x + w_, bx[2]) - max(x, bx[0])) * max(0, min(y + h_, bx[3]) - max(y, bx[1])) for bx in boxes)
    return min((c for c in cands if c[1] + h_ <= 1680), key=cover)


def note(nid, inner, w_, h_, a, out, rot=-3, pos=None):
    Z = 1.35
    x, y = pos or spot(a, out, w_ * Z, h_ * Z)
    OV.append(f'<div class="pn" id="{nid}" style="left:{x / Z:.0f}px;top:{y / Z:.0f}px;width:{w_}px;zoom:{Z}">{inner}</div>')
    ft(f"#{nid}", a, {"opacity": 0, "y": 50, "rotation": rot + 9, "scale": 0.85}, {"opacity": 1, "y": 0, "rotation": rot, "scale": 1}, 0.42, "back.out(1.7)")
    to(f"#{nid}", out, {"opacity": 0, "y": 30, "rotation": rot - 6, "scale": 0.9}, 0.25, "power2.in")
    sfx.append(("drop_002", a + 0.05, 0.12))
    hold_cam(a - 0.1, out + 0.3)
    return x, y


def mark(mid, kind="tick"):
    return f'<svg class="mk2" id="{mid}" viewBox="0 0 24 24"><path pathLength="100" d="{TICK_D if kind == "tick" else CROSS_D}"/></svg>'


def draw(mid, at):
    ft(f"#{mid} path", at, {"strokeDashoffset": 100}, {"strokeDashoffset": 0}, 0.3, "power2.out")
    sfx.append(("scribble", at, 0.14))


def plist(nid, title, items, word_times, out, ticks=None, w_=280):
    """A paper list; each line lands on its word; ticks=[time,...] draws an ink tick in each box."""
    rows = "".join(f'<div class="ln" id="{nid}-{k}" style="opacity:0"><span class="bx"><svg class="mk" id="{nid}-m{k}" viewBox="0 0 24 24"><path pathLength="100" d="{TICK_D}"/></svg></span><span>{esc(it)}</span></div>' for k, it in enumerate(items))
    note(nid, f'<div class="k">{title}</div>{rows}', w_, 70 + 52 * len(items), word_times[0] - 0.35, out)
    for k, at in enumerate(word_times):
        ft(f"#{nid}-{k}", at - 0.1, {"opacity": 0, "x": -16}, {"opacity": 1, "x": 0}, 0.25, "power2.out")
        sfx.append(("click_004", at, 0.08))
    for k, at in enumerate(ticks or []):
        draw(f"{nid}-m{k}", at)


def timer(nid, label, a, out, run_a, run_d, m1=60):
    note(nid, f'<div class="k">{label}</div><div class="b" style="font-size:66px;font-family:Typewriter;letter-spacing:0;margin-top:6px" id="{nid}-t">0:00</div><div class="bar"><i id="{nid}-b"></i></div>', 240, 170, a, out, 3)
    count_js(f"{nid}-t", 0, m1, run_a, run_d, "Math.floor(o.n) + ':' + String(Math.round((o.n % 1) * 60) % 60).padStart(2,'0')")
    ft(f"#{nid}-b", run_a, {"scaleX": 0}, {"scaleX": 1}, run_d, "power1.inOut")
    sfx.extend([("tick_002", run_a + k * 0.2, 0.06) for k in range(int(run_d / 0.2))])


def hook12():
    """'Can Claude start a business from the bottom in just under one hour?' — a note: 'a business from £0'; then an hour timer."""
    i_b, i_h = w("start a business"), w("one hour")
    out = te(w("today", t(i_h))) + 0.3
    note("hk12", '<div class="k">a business from</div><div class="b" style="font-size:96px;margin-top:4px">£0</div>', 220, 150, t(i_b) - 0.1, t(i_h) - 0.1)
    timer("hk12w", "under 1 hour", t(i_h) - 0.05, out, t(i_h) + 0.2, max(0.8, out - t(i_h) - 0.4), 59.98)


def today12():
    """'create us a product and bring it to life ... build us a business that we can launch today' — the plan, boxes empty."""
    words_ = [t(w("a product")), t(w("bring it to life")), t(w("build us a business")) + 0.3, t(w("launch today"))]
    plist("td", "the plan", ["a product", "brought to life", "a business", "launched today"], words_, te(w("launch today") + 1) + 0.35, w_=300)


def money12():
    """'you need money to start a business. Well, I gave Claude a zero pound budget.' — a budget note counting down to £0."""
    i_m, i_z = w("need money"), w("zero pound budget")
    note("bd12", '<div class="k">budget</div><div class="b" style="font-size:96px;margin-top:4px">£<span id="bd12-n">500</span></div>', 250, 150, t(i_m + 1) - 0.1, te(i_z + 2) + 0.4)
    count_js("bd12-n", 500, 0, t(i_z), max(0.5, t(i_z + 2) - t(i_z) + 0.2))
    sfx.extend([("tick_002", t(i_z) + k * 0.1, 0.07) for k in range(6)])


def ask12():
    """'create me a full product, a brand, an idea, a campaign, and to turn me into a millionaire.' — the ask list, then
    £0 rolling up to £1,000,000."""
    at = [t(w("full product")) + 0.3, t(w("a brand")) + 0.15, t(w("an idea")) + 0.15, t(w("a campaign")) + 0.15]
    i_mil = w("millionaire")
    plist("ak12", "I asked for", ["a full product", "a brand", "an idea", "a campaign"], at, t(i_mil) - 0.55, w_=290)
    note("ml12", '<div class="k">turn me into a</div><div class="b" style="font-size:50px;margin-top:6px">£<span id="ml12-n">0</span></div>', 290, 120, t(i_mil) - 0.45, te(i_mil) + 0.45, 2)
    count_js("ml12-n", 0, 1000000, t(i_mil) - 0.2, 0.9, "Math.round(o.n).toLocaleString('en-GB')")
    sfx.extend([("tick_002", t(i_mil) - 0.2 + k * 0.08, 0.06) for k in range(10)] + [("pluck_001", t(i_mil) + 0.7, 0.22)])


def no12():
    """'Well, the answer is no, it can't. And the reason why is because AI is a tool. It's not the brain.' — an ink NO. stamp
    beside him, then 'a tool' (ink tick) / 'not the brain' (ink cross)."""
    i_no = w("is no")
    i_t, i_b = w("a tool"), w("the brain")
    x, y = spot(t(i_no), te(i_no + 3), 300, 160)
    OV.append(f'<div class="inkst" id="no12" style="left:{x:.0f}px;top:{y:.0f}px">NO.</div>')
    stamp("#no12", t(i_no + 1) - 0.05, -8)
    to("#no12", te(i_no + 3) + 0.2, {"opacity": 0}, 0.2)
    hold_cam(t(i_no) - 0.2, te(i_no + 3) + 0.4)
    note("tb12", f'<div class="ln" style="margin-top:0">{mark("tb12-a")}<span>a tool</span></div><div class="ln" id="tb12-r2" style="opacity:0">{mark("tb12-b", "cross")}<span>the brain</span></div>', 270, 120, t(i_t + 1) - 0.2, te(i_b + 1) + 0.35)
    draw("tb12-a", t(i_t + 1))
    ft("#tb12-r2", t(i_b) - 0.15, {"opacity": 0}, {"opacity": 1}, 0.2)
    draw("tb12-b", t(i_b))


def tried12():
    """'I spent an hour. I gave it a really, really detailed prompt. I told it it has full creativity…' — an hour timer, then
    the prompt note types out."""
    i_h, i_p, i_c = w("spent an hour"), w("detailed prompt"), w("full creativity")
    timer("tr12w", "1 hour", t(i_h) - 0.2, t(i_p) - 0.5, t(i_h) + 0.1, 0.8)
    PR = "Start a business from £0: the product, the brand, the idea and the campaign. Full creativity, start to finish."
    note("pr12", f'<div class="k">my prompt</div><div style="font-family:ArchivoSB;font-size:27px;line-height:1.28;margin-top:8px">{typed_words("pr12w", PR)}</div>', 300, 250, t(i_p) - 0.4, te(w("the finish", t(i_c)) + 1) + 0.35, 2)
    type_on("pr12w", len(PR.split()), t(i_p) - 0.2, te(i_c + 5) - 0.3, 2)


def slop12():
    """'this is just AI slop' — an 'AI slop' label stuck on his own laptop shot."""
    i = w("ai slop")
    note("sl12", '<div class="b" style="font-size:60px">AI slop</div>', 270, 90, t(i) - 0.1, te(w("it's called", t(i)) + 1) + 0.2, -6, pos=(360, 1420))
    ft("#sl12", t(i) + 0.45, {"rotation": -6}, {"rotation": 3, "yoyo": True, "repeat": 3}, 0.14, "sine.inOut", False)


def base12():
    """'see what it can actually do without human input' — a note with an ink cross."""
    i = w("without human input")
    note("hi12", f'<div class="ln" style="margin-top:0">{mark("hi12-x", "cross")}<span>human input</span></div>', 300, 70, t(i) - 0.15, te(i + 2) + 0.4)
    draw("hi12-x", t(i) + 0.15)


def rich12():
    """'So if you're thinking AI is just gonna make you rich, well, that's not the case.' — '£1,000,000' struck through in ink."""
    i_r, i_c = w("make you rich"), w("not the case")
    note("rc12", '<div class="k">"AI will make me rich"</div><div class="b" style="font-size:50px;margin-top:6px"><span class="st">£1,000,000<i id="rc12-x"></i></span></div>', 300, 120, t(i_r + 2) - 0.2, te(i_c + 2) + 0.35)
    ft("#rc12-x", t(i_c) - 0.05, {"scaleX": 0}, {"scaleX": 1}, 0.3, "power3.out")
    sfx.append(("scratch_002", t(i_c), 0.22))


def skill12():
    """'I probably could have set up a skill, I probably could have refined it more' — what he skipped on purpose, ticked in ink."""
    at = [t(w("set up a skill")), t(w("refined it more"))]
    plist("sk12", "I could have", ["set up a skill", "refined it more"], at, te(w("pretty good result", at[-1]) + 2) + 0.3, [a + 0.3 for a in at], w_=320)


def calc12():
    """'it's the same as when a calculator was brought out. People probably thought that using a calculator was cheating. But
    … a calculator is a tool.' — 'cheating?' gets an ink cross, 'a tool' an ink tick."""
    i_c = w("a calculator was brought")
    i_ch = w("cheating")
    i_tool = w("is a tool", t(i_ch))
    note("ca12", f'<div class="k">a calculator</div><div class="ln">{mark("ca12-x", "cross")}<span>cheating?</span></div><div class="ln" id="ca12-r2" style="opacity:0">{mark("ca12-t")}<span>a tool</span></div>', 320, 160, t(i_c + 1) - 0.2, te(i_tool + 2) + 0.4)
    draw("ca12-x", t(i_ch) + 0.3)
    ft("#ca12-r2", t(i_tool + 2) - 0.2, {"opacity": 0}, {"opacity": 1}, 0.2)
    draw("ca12-t", t(i_tool + 2))


def need12():
    """'you still need to have the understanding, the knowledge, and the willpower' — ink ticks on each word."""
    at = [t(w(p)) for p in ("understanding", "knowledge", "willpower")]
    plist("nd12", "you still need", ["understanding", "knowledge", "willpower"], at, te(w("for you", at[-1])) + 0.35, [a + 0.25 for a in at], w_=340)
