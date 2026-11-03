# ================================================================= Day 10 pages: "one video, a month of content". Series look (his face, then
# paper pages) with a prop per phrase that moves on its words. Real things only: Claude's real composer (Anthropic's tutorial
# frames, assets/img/ui), real frames and real hooks from his Day 1–9 videos (assets/img/days); everything else is a code-built
# prop, never a drawn app UI.
ICON.update({
    "msg": '<path d="M4 5h16a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H9l-5 4V6a1 1 0 0 1 1-1z"/>',
    "star": '<path d="M12 3l2.6 5.6 6.1.7-4.5 4.2 1.2 6L12 16.6 6.6 19.5l1.2-6L3.3 9.3l6.1-.7z"/>',
    "cam": '<rect x="2.5" y="6.5" width="14" height="11" rx="2.5"/><path d="M16.5 10.5l5-3v9l-5-3z"/>',
    "pin2": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
})
DAYS = [f"assets/img/days/d{k}.jpg" for k in range(1, 10)]
# Real hooks from his own episodes (spoken lines), with a real frame of each.
HOOKS = [(9, "“One take. That's how many takes I had to do…”"), (8, "“This isn't actually real…”"),
         (7, "“One file stops Claude sounding like a robot.”"), (6, "“Please stop paying for apps…”")]
CMP_SC = 960 / 1090


def composer(pid, top, text, size=34):
    """Claude's real empty composer (Anthropic's tutorial frame), placeholder covered, our words typed in."""
    sc = CMP_SC
    return f"""<div class="ui shd" id="{pid}" style="top:{top}px"><img src="assets/img/ui/composer.png"/>
      <i class="patch" style="left:{22 * sc:.0f}px;top:{26 * sc:.0f}px;width:{560 * sc:.0f}px;height:{52 * sc:.0f}px"></i>
      <div class="ty" style="left:{28 * sc:.0f}px;top:{30 * sc:.0f}px;font-size:{size}px">{typed_words(pid + 't', text)}<span class="car" id="{pid}-car"></span></div></div>"""


SEND10 = (60 + 1036 * CMP_SC, 152 * CMP_SC)


def type_follow(pid, text, a, b):
    """Words appear one by one between a and b with the caret riding at the end of the text."""
    n = len(text.split())
    type_on(pid + "t", n, a, b)
    ft(f"#{pid}-car", a - 0.4, {"opacity": 1}, {"opacity": 0, "yoyo": True, "repeat": 5}, 0.16, "steps(1)")


def stopwatch(sid, x, y, scale=1.0):
    return f"""<div id="{sid}" style="position:absolute;left:{x}px;top:{y}px;width:{330 * scale:.0f}px;height:{380 * scale:.0f}px;z-index:5"><div class="sw10" style="left:0;top:0;transform:scale({scale});transform-origin:0 0"><i class="crown"></i><i class="face"></i>
      <svg viewBox="0 0 298 298"><circle class="rim" cx="149" cy="149" r="125"/><circle class="arc" id="{sid}-a" cx="149" cy="149" r="125" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"/></svg>
      <div class="rd" id="{sid}-t">0:00</div></div></div>"""


def watch_run(sid, at, d, m0, m1, f0=0.0, f1=1.0):
    """Stopwatch counts m0 -> m1 minutes over d seconds; its arc fills f0 -> f1."""
    count_js(f"{sid}-t", m0, m1, at, d, "Math.floor(o.n) + ':' + String(Math.round((o.n % 1) * 60) % 60).padStart(2,'0')")
    ft(f"#{sid}-a", at, {"strokeDashoffset": 100 - f0 * 100}, {"strokeDashoffset": 100 - f1 * 100}, d, "power1.inOut")
    sfx.extend([("tick_002", at + k * 0.18, 0.07) for k in range(max(1, int(d / 0.18)))])


LAND = {  # simple code-drawn landscapes (location cards)
    "river": '<svg viewBox="0 0 290 400"><rect width="290" height="400" fill="#cfd8d4"/><path d="M0 170 Q70 120 150 160 T290 140 V400 H0z" fill="#7f9478"/><path d="M110 400 C130 300 170 260 150 170 C200 250 220 320 250 400z" fill="#9fb6c0"/><path d="M135 330 q20 -8 40 0 M150 270 q16 -6 30 0" stroke="#e8eef0" stroke-width="5" fill="none" stroke-linecap="round"/></svg>',
    "field": '<svg viewBox="0 0 290 400"><rect width="290" height="400" fill="#dfe2d2"/><circle cx="220" cy="90" r="34" fill="#f3ead2"/><path d="M0 210 Q140 170 290 200 V400 H0z" fill="#8d9a63"/><path d="M0 270 Q140 240 290 268 V400 H0z" fill="#76854f"/><path d="M30 330 v-26 M60 340 v-22 M200 320 v-26 M240 350 v-24 M120 360 v-20" stroke="#5d6a3c" stroke-width="5" stroke-linecap="round"/></svg>',
    "lake": '<svg viewBox="0 0 290 400"><rect width="290" height="400" fill="#d7dde0"/><path d="M0 220 L70 120 L120 180 L180 90 L290 210 V260 H0z" fill="#8a8f93"/><path d="M150 110 l30 -20 l25 30z" fill="#eef0f1"/><rect y="255" width="290" height="145" fill="#a7b9c2"/><path d="M40 300 h50 M150 330 h70 M60 360 h40" stroke="#e3ebee" stroke-width="5" stroke-linecap="round"/></svg>',
}


def pg_day():
    """'This is day ten of thirty' — the series stat page; today's block lifts."""
    i = w("this is day ten")
    s, e = t(i) - 0.06, cover_cut(t(i + 5) + 0.6)
    scene("pday", s, e, f"""
  <div class="stack" style="left:0;right:0;top:600px">
    <span class="sm" style="font-size:56px">{words_in('pdw', i, 2)}</span>
    <div class="row" style="align-items:flex-end;justify-content:center;margin-top:10px">
      <span id="pday-d" class="xb" style="font-size:230px;line-height:1">Day</span>
      <span id="pday-n" class="xb" style="font-size:230px;line-height:1;margin-left:40px">10</span>
    </div>
    <span class="sm" style="font-size:56px;margin-top:22px">{words_in('pdo', i + 4, 2)}</span>
  </div>
  <div id="pday-bar" class="bar big" style="top:1250px">{BLOCKS.replace('{p}', 'pday')}</div>""")
    ft("#pday-d", t(i + 2) - 0.05, {"opacity": 0, "y": 60, "filter": "blur(14px)"}, {"opacity": 1, "y": 0, "filter": "blur(0px)"}, 0.4, "expo.out")
    slam("#pday-n", t(i + 3) - 0.05)
    ft("#pday-bar .seg", t(i + 3), {"scaleY": 0, "opacity": 0}, {"scaleY": 1, "opacity": 1, "stagger": 0.01}, 0.22, "power2.out")
    ft(", ".join(f"#pday-s{k}" for k in range(9)), t(i + 3) + 0.25, {"backgroundColor": "rgba(23,18,14,.14)"}, {"backgroundColor": INK, "stagger": 0.045}, 0.15)
    ft("#pday-s9", t(i + 5), {"backgroundColor": "rgba(23,18,14,.14)", "scaleY": 1}, {"backgroundColor": INK, "scaleY": 1.9}, 0.45, "back.out(2.2)")
    sfx.extend([("dry-pop-alert", t(i + 3), 0.24), ("pluck_001", t(i + 5), 0.26)])


def pg_end():
    """'(and I will) see you in the next one' after 'stay for day eleven' — 30 blocks, ten lit, zoom into today's block."""
    i = w("see you in")
    s = t(i) + 0.05
    ZX, ZY = 90 + 9 * (SEG_W + 6) + SEG_W / 2, 1340 - 40 * 1.9 / 2
    scene("ed", s, DURATION, f"""
  <div id="ed-zoom" style="position:absolute;inset:0;transform-origin:{ZX:.1f}px {ZY:.1f}px">
    <div class="stack" style="left:0;right:0;top:560px">
      <span class="sm" style="font-size:56px">{words_in('edw', i, 2)} on</span>
      <div class="row" style="align-items:flex-end;justify-content:center;margin-top:6px">
        <span id="ed-day" class="xb" style="font-size:230px;line-height:1">Day</span>
        <span id="ed-n" class="xb" style="font-size:230px;line-height:1;margin-left:40px">11</span>
      </div>
    </div>
    <span id="ed-lbl" class="note" style="position:absolute;left:{90 + 9 * (SEG_W + 6) - 40:.0f}px;top:1186px">day 10 / 30</span>
    <div id="ed-bar" class="bar big" style="top:1300px">{BLOCKS.replace('{p}', 'ed')}</div>
  </div>""")
    rev("#ed-day", s + 0.25, 30)
    slam("#ed-n", s + 0.45)
    ft("#ed-bar .seg", s + 0.1, {"scaleY": 0, "opacity": 0}, {"scaleY": 1, "opacity": 1, "stagger": 0.014}, 0.3, "power2.out")
    lit = s + 0.9
    ft(", ".join(f"#ed-s{k}" for k in range(9)), lit - 0.3, {"backgroundColor": "rgba(23,18,14,.14)"}, {"backgroundColor": INK, "stagger": 0.06}, 0.2)
    ft("#ed-s9", lit, {"backgroundColor": "rgba(23,18,14,.14)", "scaleY": 1}, {"backgroundColor": INK, "scaleY": 1.9}, 0.5, "back.out(2.2)")
    ft("#ed-lbl", lit + 0.15, {"opacity": 0, "y": 12}, {"opacity": 1, "y": 0}, 0.35, "power2.out")
    ft("#ed-s9", lit + 0.6, {"scaleY": 1.9}, {"scaleY": 2.2, "yoyo": True, "repeat": 1}, 0.6, "sine.inOut", False)
    zoom_at = DURATION - 1.4
    to("#ed-lbl", zoom_at, {"opacity": 0}, 0.3)
    ft("#ed-zoom", zoom_at, {"scale": 1, "x": 0, "y": 0}, {"scale": 60, "x": round(540 - ZX, 1), "y": round(960 - ZY, 1)}, 1.3, "power3.inOut")
    sfx.extend([("dry-pop-alert", s + 0.45, 0.24), ("pluck_001", lit, 0.3), ("riser", zoom_at + 0.25, 0.35), ("boom", DURATION - 0.12, 0.3)])


def hook_v1():
    """'Stop asking Claude to edit your videos and instead ask it this.' — his real episodes on a film strip get snipped by
    scissors on 'edit your videos'; 'instead' tears an X through it; 'ask it this' brings up Claude with a question."""
    i_ed, i_in, i_ask = w("edit your videos"), w("instead"), w("ask it this")
    s, e = t(i_ed) - 0.12, cover_cut(te(i_ask + 2) + 0.4)
    thumbs = "".join(f'<img src="{DAYS[k]}"/>' for k in (8, 7, 6, 5, 4, 3))
    SC = '<svg class="sc10" id="hk-sc" viewBox="0 0 220 220"><g id="hk-b1"><path class="bl" d="M110 110 L200 60 L206 72 Z"/></g><g id="hk-b2"><path class="bl" d="M110 110 L200 160 L206 148 Z"/></g><circle class="hd" cx="70" cy="80" r="28"/><circle class="hd" cx="70" cy="140" r="28"/><path class="hd" d="M92 92 L112 110 M92 128 L112 110"/></svg>'
    s = scene("hk", s, e, f"""
{head('hk', 'stop asking Claude to', 'edit', 200, 140)}
  <div class="strip10" id="hk-st">{thumbs}</div>
  {SC}
  <svg class="bigx2" viewBox="0 0 1080 1920"><path id="hk-x0" d="M150 640 L930 1100"/><path id="hk-x1" d="M930 640 L150 1100"/></svg>
  <div class="q10" id="hk-q"><div class="bb">{CLAUDE.format(110)}?</div></div>""")
    rev("#hk-a", s + 0.02, 14)
    slam("#hk-h", t(i_ed) - 0.02, 1.4)
    ft("#hk-st", s + 0.03, {"opacity": 0, "x": 400}, {"opacity": 1, "x": 0}, 0.35, "power3.out")
    ft("#hk-sc", s + 0.1, {"x": -60, "y": 650, "rotation": 0, "opacity": 0}, {"x": 860, "y": 650, "rotation": 0, "opacity": 1}, max(0.6, t(i_in) - s - 0.15), "power1.inOut")
    for k in range(4):
        at = s + 0.15 + k * 0.17
        ft("#hk-b1", at, {"rotation": 0, "svgOrigin": "110 110"}, {"rotation": -16, "svgOrigin": "110 110", "yoyo": True, "repeat": 1}, 0.07, "none", None if k == 0 else False)
        ft("#hk-b2", at, {"rotation": 0, "svgOrigin": "110 110"}, {"rotation": 16, "svgOrigin": "110 110", "yoyo": True, "repeat": 1}, 0.07, "none", None if k == 0 else False)
        sfx.append(("scratch_002", at, 0.12))
    x = t(i_in) - 0.05
    to("#hk-sc", x, {"opacity": 0}, 0.15)
    for k in range(2):
        ft(f"#hk-x{k}", x + k * 0.12, {"strokeDashoffset": 1300}, {"strokeDashoffset": 0}, 0.2, "power2.out")
        sfx.append(("scratch_002", x + k * 0.12, 0.2))
    to("#hk-st", x + 0.3, {"opacity": 0.3, "scale": 0.94}, 0.3)
    ft("#hk-q", t(i_ask) - 0.1, {"opacity": 0, "scale": 0.3, "y": 80}, {"opacity": 1, "scale": 1, "y": 0}, 0.4, "back.out(2)")
    ft("#hk-q img", t(i_ask + 2) - 0.05, {"rotation": 0}, {"rotation": 180}, 0.6, "power2.inOut")
    sfx.append(("hard-pop-click", t(i_ask), 0.26))


def hook_v2():
    """V2 'Everybody is talking about how Claude can edit your videos, but no one is talking about this.' — topic tags about
    Claude video editing pile up on 'everybody is talking'; 'but no one' dims them all under a spotlight; 'this' = a Claude '?'."""
    i_h, i_no = w("how claude"), w("no one")
    i_this = w("about this", t(i_no)) + 1
    s, e = t(i_h) - 0.12, cover_cut(te(i_this) + 0.45)
    TAGS = [("#claudeedit", 90, 560, -6), ("#aivideoediting", 520, 520, 5), ("#editwithclaude", 160, 760, 4), ("#autocaptions", 600, 760, -5),
            ("#claudecode", 80, 980, -3), ("#aieditor", 620, 990, 6), ("#videoediting", 300, 880, -2), ("#contentcreator", 330, 1100, 3)]
    tags = "".join(f'<span class="ch10 shd" id="h2-c{k}" style="left:{x}px;top:{y}px;transform:rotate({r}deg)">{ic("film", 44)}{tg}</span>' for k, (tg, x, y, r) in enumerate(TAGS))
    s = scene("h2", s, e, f"""
{head('h2', 'everybody is talking about', 'editing', 200, 120)}
  {tags}
  <div class="spot10" id="h2-sp"></div>
  <div class="q10" id="h2-q" style="top:1060px"><div class="bb">{CLAUDE.format(110)}?</div></div>
  <div class="stack" style="left:0;right:0;top:1440px;z-index:6"><span id="h2-n" class="xb" style="font-size:84px;color:#fbf9f5;text-shadow:none">no one's talking about this</span></div>""")
    rev("#h2-a", s + 0.02, 14)
    slam("#h2-h", t(w("edit", t(i_h))) - 0.05, 1.4)
    span = max(0.8, t(i_no) - s - 0.3)
    for k in range(len(TAGS)):
        at = s + 0.05 + span * k / len(TAGS)
        ft(f"#h2-c{k}", at, {"opacity": 0, "scale": 0.3, "y": 40}, {"opacity": 1, "scale": 1, "y": 0}, 0.3, "back.out(2.2)")
        sfx.append(("dry-pop-alert" if k % 2 else "click_004", at, 0.14))
    a = t(i_no) - 0.08
    ft("#h2-sp", a, {"opacity": 0}, {"opacity": 1}, 0.35, "power2.out")
    ft("#h2-n", a + 0.1, {"opacity": 0, "y": 30}, {"opacity": 1, "y": 0}, 0.35)
    ft("#h2-q", t(i_this) - 0.15, {"opacity": 0, "scale": 0.3}, {"opacity": 1, "scale": 1}, 0.4, "back.out(2)")
    sfx.extend([("glitch_002", a, 0.18), ("hard-pop-click", t(i_this), 0.26)])


def pg_month(var):
    """'(how you can get) a month's worth of content (in/with) just 20 to 30 minutes of filming.' — a month of days fills with
    his real episodes, then a stopwatch runs to 30:00."""
    i_m = w("month's worth")
    i_20 = w("20 to 30", t(i_m))
    i_f = w("filming", t(i_m))
    s, e = t(i_m) - 0.3, cover_cut(te(i_f) + 0.45)
    cells = "".join(f'<div class="dc" id="mo-c{k}"><span>{k + 1}</span><img src="{DAYS[k % 9]}"/><b>{TICK}</b></div>' for k in range(28))
    top = 470 if var == "A" else 520
    s = scene("mo", s, e, f"""
{head('mo', "a month's worth of", 'content', 200, 130)}
  <div class="mon10 card10" id="mo-cal" style="top:{top}px"><div class="mh">month<small>1 a day</small></div><div class="gd">{cells}</div></div>
  {stopwatch('mo-sw', 640 if var == 'A' else 60, 1380, 0.82)}""")
    rev("#mo-a", s + 0.02, 14)
    slam("#mo-h", t(i_m + 3) - 0.05, 1.4)
    ft("#mo-cal", s + 0.04, {"opacity": 0, "y": 100, "rotation": -2}, {"opacity": 1, "y": 0, "rotation": 0}, 0.4, "back.out(1.4)")
    a, d = s + 0.35, max(0.9, t(i_20) - s - 0.55)
    order = list(range(28)) if var == "A" else [r * 7 + c for c in range(7) for r in range(4)]
    for n, k in enumerate(order):
        at = a + d * n / 28
        ft(f"#mo-c{k} img", at, {"opacity": 0, "scale": 1.4}, {"opacity": 1, "scale": 1}, 0.18, "power2.out")
        ft(f"#mo-c{k} b", at + 0.1, {"opacity": 0, "scale": 0}, {"opacity": 1, "scale": 1}, 0.15, "back.out(2.6)")
        if n % 3 == 0:
            sfx.append(("click_004", at, 0.06))
    b = t(i_20) - 0.25
    ft("#mo-sw", b, {"opacity": 0, "y": 200, "rotation": 12}, {"opacity": 1, "y": 0, "rotation": -4}, 0.4, "back.out(1.6)")
    to("#mo-cal", b, {"scale": 0.92, "y": -30}, 0.4)
    watch_run("mo-sw", b + 0.3, max(0.7, te(i_f) - b - 0.3), 0, 30)


def last_tip(final=False):
    """'And the last tip is the most important, by the way.' — a star sticker on his chest."""
    i = w("last tip")
    out = te(w("the way", t(i)) + 1) + 0.25
    sticker("lt", sk_ic("star", "the last tip matters most"), 140, 1590, -4, t(i) - 0.05, out)
    ft("#lt svg", t(w("most important", t(i))) - 0.05, {"scale": 1, "rotation": 0}, {"scale": 1.35, "rotation": 72, "yoyo": True, "repeat": 1}, 0.18, "power2.out", False)


def pg_take():
    """'I want you to do one take with one camera.' — a camera on a tripod starts recording; '1 take' and '1 camera' land."""
    i_t, i_c = w("one take"), w("one camera")
    s, e = t(i_t) - 0.35, cover_cut(te(i_c + 1) + 0.45)
    LEGS = '<svg viewBox="0 0 540 540"><path id="tk-l0" d="M270 10 L80 520"/><path id="tk-l1" d="M270 10 L460 520"/><path id="tk-l2" d="M270 10 L270 500"/></svg>'
    s = scene("tk", s, e, f"""
{head('tk', 'one take,', 'one camera', 200, 120)}
  <div class="cam10" id="tk-cam"><i class="tp"></i><div class="bd"></div><i class="ln"></i><div class="rec"><i id="tk-rd"></i>REC</div>{LEGS}</div>
  <div class="cnt10" id="tk-n1" style="left:90px;top:1420px">1<small>take</small></div>
  <div class="cnt10" id="tk-n2" style="right:90px;top:1420px">1<small>camera</small></div>""")
    rev("#tk-a", s + 0.02, 14)
    rev("#tk-h", t(i_c) - 0.05, 22)
    for k in range(3):
        ft(f"#tk-l{k}", s + 0.05 + k * 0.06, {"scaleY": 0, "transformOrigin": "270px 10px"}, {"scaleY": 1}, 0.3, "power3.out")
    ft("#tk-cam .bd, #tk-cam .ln, #tk-cam .tp, #tk-cam .rec", s + 0.2, {"opacity": 0, "y": -200}, {"opacity": 1, "y": 0}, 0.4, "back.out(1.5)")
    ft("#tk-rd", t(i_t) - 0.05, {"backgroundColor": "#e8e2d8"}, {"backgroundColor": "#fbf9f5", "opacity": 0.2, "yoyo": True, "repeat": 7}, 0.18, "steps(1)")
    ft("#tk-cam .ln", t(i_t), {"rotation": 0}, {"rotation": 90}, 1.2, "power1.inOut", False)
    pop("#tk-n1", t(i_t + 1) - 0.08, 0.4, 40)
    pop("#tk-n2", t(i_c + 1) - 0.08, 0.4, 40)
    sfx.extend([("drop_002", s + 0.3, 0.24), ("switch_003", t(i_t), 0.2), ("tick_002", t(i_t + 1), 0.22), ("tick_002", t(i_c + 1), 0.22)])


def take_sticker():
    """V2: 'one take with one camera' — a camera sticker on his chest."""
    i_t, i_c = w("one take"), w("one camera")
    sticker("tk2", sk_ic("cam", "1 take · 1 camera"), 190, 1590, -4, t(i_t) - 0.05, te(i_c + 1) + 0.35)


def pg_ask(examples):
    """'So first, get Claude to ask you questions within your niche.' — typed into Claude's real composer; V1 adds 'For example,
    what you do, who you are, why you're posting content' as three question cards landing on their words."""
    i_c, i_n = w("get claude to ask"), w("niche")
    end_i = (w("posting content") + 1) if examples else i_n
    s, e = t(i_c) - 0.1, cover_cut(te(end_i) + 0.4)
    TXT = "Ask me questions about my niche"
    QS = [("what you do", "What do you do?"), ("who you are", "Who are you?"), ("why you're posting", "Why do you post?")]
    qc = "".join(f'<div class="qc10 card10" id="ak-q{k}" style="top:{820 + k * 180}px"><span class="qn">Q{k + 1}</span><b>{q}</b></div>' for k, (_, q) in enumerate(QS)) if examples else ""
    s = scene("ak", s, e, f"""
{head('ak', 'questions in', 'your niche', 200, 120)}
  {composer('akc', 500, TXT)}
  {qc}""")
    rev("#ak-a", s + 0.02, 14)
    rev("#ak-h", t(i_n) - 0.1 if t(i_n) - 0.1 > s + 0.2 else s + 0.15, 22)
    ft("#akc", s + 0.04, {"opacity": 0, "y": 60}, {"opacity": 1, "y": 0}, 0.35)
    type_follow("akc", TXT, s + 0.35, te(i_n) - 0.15)
    sfx.extend([("click_004", s + 0.35 + k * 0.13, 0.06) for k in range(int((te(i_n) - s - 0.5) / 0.13))])
    if examples:
        for k, (ph, _) in enumerate(QS):
            at = t(w(ph)) - 0.1
            ft(f"#ak-q{k}", at, {"opacity": 0, "x": 500, "rotation": 4}, {"opacity": 1, "x": 0, "rotation": (-1, 1, -0.5)[k]}, 0.38, "back.out(1.5)")
            sfx.append(("dry-pop-alert", at, 0.2))


def pg_hundred():
    """'Then literally ask it to make a full list of a hundred different questions, almost like a Q&A.' — a list scrolls past
    while the count runs to 100; Q&A stamps down."""
    i_mk, i_h = w("ask it to make"), w("hundred")
    i_qa = w("q&a", t(i_h))
    s, e = t(i_mk) - 0.1, cover_cut(te(i_qa) + 0.45)
    rows = "".join(f'<div class="row"><span>Q{k + 1}.</span><i style="width:{(70, 52, 84, 60, 76, 46, 66)[k % 7]}%"></i></div>' for k in range(100))
    s = scene("hq", s, e, f"""
{head('hq', 'a full list of', 'questions', 200, 120)}
  <div class="ql10 card10" id="hq-l"><div class="in" id="hq-in">{rows}</div></div>
  <div class="cnt10" id="hq-n" style="right:110px;top:470px"><span id="hq-c">0</span><small>questions</small></div>
  <div class="stp4" id="hq-st" style="left:300px;top:1440px">Q&amp;A</div>""")
    rev("#hq-a", s + 0.02, 14)
    rev("#hq-h", t(w("different questions", t(i_h)) + 1) - 0.05, 22)
    ft("#hq-l", s + 0.04, {"opacity": 0, "y": 80}, {"opacity": 1, "y": 0}, 0.35)
    pop("#hq-n", t(i_h) - 0.25, 0.4, 30)
    d = max(0.8, t(i_qa) - t(i_h))
    count_js("hq-c", 0, 100, t(i_h) - 0.1, d)
    ft("#hq-in", t(i_h) - 0.1, {"y": 0}, {"y": -(100 * 74 - 760)}, d + 0.2, "power1.inOut")
    sfx.extend([("tick_002", t(i_h) + k * 0.15, 0.06) for k in range(int(d / 0.15))])
    stamp("#hq-st", t(i_qa) - 0.05, -8)


def pg_place():
    """'go find some river, find some field, find some lake, set your camera up, and just film yourself 15, 20 minutes, maybe
    half an hour.' — the three places land on their words, then a stopwatch runs 15 -> 20 -> 30 minutes."""
    i_r, i_f, i_l = w("river"), w("field"), w("lake")
    i_s = w("set your camera up")
    i_15 = w("15", t(i_s))
    i_20 = w("20", t(i_15))
    i_hh = w("half an hour", t(i_15))
    s, e = t(i_r) - 0.45, cover_cut(te(i_hh + 2) + 0.4)
    L = [("river", 90, 560, -5), ("field", 395, 520, 2), ("lake", 700, 560, 6)]
    cards = "".join(f'<div class="loc10 shd" id="pl-{k}" style="left:{x}px;top:{y}px;transform:rotate({r}deg)">{LAND[k]}<span>{k}</span></div>' for k, x, y, r in L)
    s = scene("pl", s, e, f"""
{head('pl', 'somewhere', 'nice', 200, 140)}
  {cards}
  <span class="tag7" id="pl-tg" style="left:330px;top:1040px">{ic('cam', 44, '#fbf9f5')} set your camera up</span>
  {stopwatch('pl-sw', 375, 1180, 1.0)}""")
    rev("#pl-a", s + 0.02, 14)
    slam("#pl-h", s + 0.12, 1.4)
    for k, i in zip(("river", "field", "lake"), (i_r, i_f, i_l)):
        at = t(i) - 0.15
        ft(f"#pl-{k}", at, {"opacity": 0, "y": 200, "scale": 0.6}, {"opacity": 1, "y": 0, "scale": 1}, 0.38, "back.out(1.7)")
        sfx.append(("dry-pop-alert", at, 0.2))
    ft("#pl-tg", t(i_s) - 0.1, {"opacity": 0, "scale": 1.6, "rotation": -10}, {"opacity": 1, "scale": 1, "rotation": -3}, 0.3, "back.out(2)")
    ft("#pl-sw", t(i_s + 3) - 0.1, {"opacity": 0, "y": 200}, {"opacity": 1, "y": 0}, 0.4, "back.out(1.5)")
    sfx.append(("switch_003", t(i_s), 0.2))
    watch_run("pl-sw", t(i_15) - 0.1, max(0.4, t(i_20) - t(i_15)), 0, 15, 0, 0.5)
    watch_run("pl-sw", t(i_20) - 0.05, max(0.3, t(i_hh) - t(i_20) - 0.1), 15, 20, 0.5, 0.67)
    watch_run("pl-sw", t(i_hh) - 0.05, max(0.4, te(i_hh + 2) - t(i_hh)), 20, 30, 0.67, 1.0)


def place_stickers():
    """V2: the places as photo stickers round him, then a stopwatch sticker for '15, 20 minutes, maybe half an hour'."""
    i_r, i_f, i_l = w("river"), w("field"), w("lake")
    i_hh = w("half an hour")
    out = t(w("set your camera up")) + 0.2
    for k, (i, x, y, r) in zip(("river", "field", "lake"), ((i_r, 40, 1380, -7), (i_f, 400, 1420, 3), (i_l, 760, 1380, 8))):
        sticker(f"ps-{k}", f'<div style="width:220px;height:260px;border-radius:16px;overflow:hidden">{LAND[k]}</div><span style="font-size:36px">{k}</span>', x, y, r, t(i) - 0.12, out, "photo")
    OV.append(stopwatch("ps-sw", 760, 1520, 0.62))
    i_15 = w("15", t(i_r))
    ft("#ps-sw", t(i_15) - 0.3, {"opacity": 0, "scale": 0.3}, {"opacity": 1, "scale": 1}, 0.35, "back.out(2)")
    watch_run("ps-sw", t(i_15) - 0.1, max(0.6, te(i_hh + 2) - t(i_15)), 0, 30)
    to("#ps-sw", te(i_hh + 2) + 0.3, {"opacity": 0, "scale": 0.5}, 0.2)


def pg_drop():
    """'drop your full footage into Claude.' — the cursor drags his full video file into Claude's real composer."""
    i_d = w("drop your full footage")
    i_c = w("claude", t(i_d))
    s, e = t(i_d) - 0.35, cover_cut(te(i_c) + 0.5)
    s = scene("dp", s, e, f"""
{head('dp', 'drop it into', 'Claude', 200, 140)}
  <img id="dp-cl" src="assets/img/claude-mark.svg" style="position:absolute;left:470px;top:440px;width:140px;height:140px"/>
  {composer('dpc', 1000, '')}
  <i class="dropz" id="dp-dz" style="position:absolute;left:60px;top:990px;width:960px;height:200px;border-radius:34px;opacity:0"></i>
  <div class="vf10" id="dp-f" style="left:300px;top:680px">{ic('film', 64, '#fbf9f5')}<div><b>full-video.mov</b><small>20–30 minutes</small></div></div>
  <div id="dp-cur" class="cursor">{CUR}</div>""")
    rev("#dp-a", s + 0.02, 14)
    slam("#dp-h", t(i_c) - 0.05, 1.4)
    ft("#dp-cl", s + 0.02, {"opacity": 0, "scale": 0.2, "rotation": -200}, {"opacity": 1, "scale": 1, "rotation": 0}, 0.5, "back.out(1.8)")
    ft("#dpc", s + 0.06, {"opacity": 0, "y": 60}, {"opacity": 1, "y": 0}, 0.35)
    pop("#dp-f", s + 0.15, 0.6, 30)
    g = t(i_d) - 0.05
    ft("#dp-cur", g - 0.45, {"x": 1100, "y": 1500, "opacity": 0}, {"x": 520, "y": 740, "opacity": 1}, 0.4)
    to("#dp-cur", g, {"scale": 0.85}, 0.08)
    to("#dp-cur", g + 0.1, {"x": 520, "y": 1060}, 0.5, "power2.inOut")
    to("#dp-f", g + 0.1, {"y": 320, "rotation": -4, "scale": 1.04}, 0.5, "power2.inOut")
    ft("#dp-dz", g + 0.3, {"opacity": 0}, {"opacity": 1}, 0.15, ir=False)
    drop = g + 0.62
    to("#dp-cur", drop, {"scale": 1}, 0.08)
    to("#dp-f", drop, {"scale": 0.62, "x": -200, "y": 365, "rotation": 0}, 0.25, "power2.in")
    to("#dp-dz", drop + 0.05, {"opacity": 0}, 0.2)
    to("#dp-cur", drop + 0.3, {"x": 1150, "y": 1700, "opacity": 0}, 0.4, "power2.in")
    ft("#dp-cl", t(i_c) - 0.05, {"scale": 1}, {"scale": 1.2, "yoyo": True, "repeat": 1}, 0.15, "power2.out", False)
    sfx.extend([("click_002", g, 0.24), ("drop_002", drop, 0.3), ("hard-pop-click", t(i_c), 0.22)])


def pg_skill():
    """'use this skill, it's gonna transcribe every single word with an exact time stamp.' — the skill file lands, then his
    own words from this video stream in line by line, each with its real time stamp."""
    i_s = w("skill")
    i_tr = w("transcribe", t(i_s))
    i_ev = w("every single word", t(i_s))
    i_ts = w("time stamp", t(i_s)) if has("time stamp") else w("timestamp", t(i_s))
    i_tse = i_ts + 1 if has("time stamp") else i_ts
    s, e = t(i_s) - 0.3, cover_cut(te(i_tse) + 0.45)
    LINES = [("stop asking Claude to edit your videos", "stop asking"), ("I want you to do one take with one camera", "one take"),
             ("get Claude to ask you questions", "get claude to ask"), ("a full list of a hundred different questions", "hundred"),
             ("find some river, find some field", "river")]
    rows = ""
    for k, (txt, ph) in enumerate(LINES):
        ts = t(w(ph)) if has(ph) else 0.0
        stamp_ = f"{int(ts // 60):02d}:{ts % 60:04.1f}"
        rows += f'<div class="ln" id="sk-r{k}"><em id="sk-e{k}">{stamp_}</em><span>{typed_words(f"sk{k}w", txt)}</span></div>'
    s = scene("sk", s, e, f"""
{head('sk', 'a skill that', 'transcribes', 200, 120)}
  {doc('sk-doc', 'SKILL.md', 6, True, 'left:360px;top:400px;width:360px;height:440px;padding-top:86px')}
  <div class="tr10 card10" id="sk-tr"><div class="in">{rows}</div></div>""")
    rev("#sk-a", s + 0.02, 14)
    rev("#sk-h", t(i_tr) - 0.05, 22)
    ft("#sk-doc", s + 0.03, {"opacity": 0, "y": -400, "rotation": -14}, {"opacity": 1, "y": 0, "rotation": -3}, 0.45, "back.out(1.5)")
    ft("#sk-doc .dl", s + 0.3, {"scaleX": 0}, {"scaleX": 1, "stagger": 0.07}, 0.14, "power2.out")
    ft("#sk-tr", t(i_tr) - 0.2, {"opacity": 0, "y": 80}, {"opacity": 1, "y": 0}, 0.35)
    to("#sk-doc", t(i_tr) - 0.2, {"scale": 0.7, "y": -90}, 0.35)
    st(".tr10 em", s, {"opacity": 0})
    a, d = t(i_tr), max(1.2, t(i_ts) - t(i_tr))
    for k, (txt, _) in enumerate(LINES):
        n = len(txt.split())
        a0 = a + d * k / len(LINES)
        for j in range(n):
            ft(f"#sk{k}w{j}", a0 + (d / len(LINES)) * j / n, {"opacity": 0.12}, {"opacity": 1}, 0.08, "none")
    for k in range(len(LINES)):
        at = t(i_ts) - 0.1 + k * 0.08
        ft(f"#sk-e{k}", at, {"opacity": 0, "scale": 0.4}, {"opacity": 1, "scale": 1}, 0.22, "back.out(2.4)", False)
        sfx.append(("tick_002", at, 0.12))
    sfx.extend([("drop_002", s + 0.3, 0.24), ("click_004", t(i_ev), 0.1)])


def pg_clips():
    """'It'll create engaging social media clips between 20 and 45 seconds that works for someone who's never seen you
    before.' — the long recording is sliced and vertical clips (his real episodes) drop out of it with their lengths."""
    i_c = w("it'll create")
    i_cl = w("social media clips", t(i_c)) + 2
    i_20 = w("20 and 45", t(i_c))
    i_nv = w("never seen you", t(i_c))
    s, e = t(i_c) - 0.1, cover_cut(te(i_nv + 3) + 0.4)
    bars_ = "".join(f'<i style="height:{int(18 + 70 * abs(math.sin(k * 0.9)) * (0.4 + 0.6 * abs(math.cos(k * 0.37))))}%"></i>' for k in range(80))
    CUTX = [12, 26, 41, 57, 72, 88]
    cuts = "".join(f'<i class="cut" id="cp-x{k}" style="left:{x}%"></i>' for k, x in enumerate(CUTX))
    LEN = ["0:20", "0:34", "0:45", "0:27", "0:38"]
    clips = "".join(f'<div class="clp10" id="cp-c{k}" style="left:{40 + k * 204}px;top:900px"><img src="{DAYS[(8 - k) % 9]}"/><span id="cp-l{k}">{LEN[k]}</span></div>' for k in range(5))
    s = scene("cp", s, e, f"""
{head('cp', 'engaging', 'clips', 200, 140)}
  <div class="tl10" id="cp-tl"><div class="wv">{bars_}</div>{cuts}<span class="lb">full video</span></div>
  {clips}
  <span class="tag7" id="cp-tg" style="left:200px;top:1360px">{ic('people', 44, '#fbf9f5')} works for new viewers</span>""")
    rev("#cp-a", s + 0.02, 14)
    slam("#cp-h", t(i_cl) - 0.05, 1.4)
    ft("#cp-tl", s + 0.04, {"opacity": 0, "scaleX": 0.6}, {"opacity": 1, "scaleX": 1}, 0.35, "power3.out")
    for k in range(len(CUTX)):
        at = t(i_cl) - 0.3 + k * 0.07
        ft(f"#cp-x{k}", at, {"opacity": 0, "scaleY": 0}, {"opacity": 1, "scaleY": 1}, 0.12, "power2.out")
        sfx.append(("scratch_002", at, 0.08))
    for k in range(5):
        at = t(i_cl) + 0.1 + k * 0.12
        ft(f"#cp-c{k}", at, {"opacity": 0, "y": -260, "rotation": (k - 2) * 8, "scale": 0.5}, {"opacity": 1, "y": 0, "rotation": (k - 2) * 2, "scale": 1}, 0.4, "back.out(1.6)")
        sfx.append(("drop_002", at + 0.3, 0.12))
    st(".clp10 span", s, {"opacity": 0})
    for k in range(5):
        ft(f"#cp-l{k}", t(i_20) - 0.05 + k * 0.08, {"opacity": 0, "y": 10}, {"opacity": 1, "y": 0}, 0.2, "power2.out", False)
    ft("#cp-tg", t(i_nv) - 0.1, {"opacity": 0, "scale": 1.6, "rotation": -10}, {"opacity": 1, "scale": 1, "rotation": -3}, 0.3, "back.out(2)")
    sfx.append(("dry-pop-alert", t(i_nv), 0.22))


def pg_hooks(long):
    """'It's gonna extract the most engaging hooks that you said (across your full 20 to 30 minute video).' — real hooks from
    his own episodes lift out of the recording one by one."""
    i_x = w("extract")
    i_h = w("engaging hooks", t(i_x)) + 1
    i_end = (w("minute video", t(i_x)) + 1) if long and has("minute video") else w("you said", t(i_x)) + 1
    s, e = t(i_x) - 0.25, cover_cut(te(i_end) + 0.45)
    bars_ = "".join(f'<i style="height:{int(18 + 70 * abs(math.sin(k * 1.3 + 1)) * (0.4 + 0.6 * abs(math.cos(k * 0.23))))}%"></i>' for k in range(80))
    rows = "".join(f'<div class="hk10 card10" id="hx-{k}" style="top:{800 + k * 170}px"><span class="tg">HOOK</span><img src="{DAYS[d - 1]}"/><b>{esc(txt)}</b></div>' for k, (d, txt) in enumerate(HOOKS))
    s = scene("hx", s, e, f"""
{head('hx', 'the best', 'hooks', 200, 140)}
  <div class="tl10" id="hx-tl" style="top:560px"><div class="wv">{bars_}</div><span class="lb" id="hx-lb">20–30 min</span></div>
  {rows}""")
    rev("#hx-a", s + 0.02, 14)
    slam("#hx-h", t(i_h) - 0.05, 1.4)
    ft("#hx-tl", s + 0.04, {"opacity": 0, "y": 40}, {"opacity": 1, "y": 0}, 0.3)
    span = max(1.0, te(i_end) - t(i_h) - 0.2)
    for k in range(len(HOOKS)):
        at = t(i_h) - 0.25 + span * k / len(HOOKS)
        ft(f"#hx-{k}", at, {"opacity": 0, "y": -230 - k * 170, "scale": 0.5}, {"opacity": 1, "y": 0, "scale": 1}, 0.42, "back.out(1.5)")
        sfx.append(("dry-pop-alert", at + 0.2, 0.16))


def pg_sched():
    """'make a full schedule with every single video so you can almost tell a story across a week, (across a few weeks,)
    across a month.' — the month fills one video a day, a story line threads the first week, then the weeks fill."""
    i_s = w("full schedule")
    i_st = w("story", t(i_s))
    i_wk = w("a week", t(i_s))
    i_fw = w("few weeks", t(i_s)) if has("few weeks") else None
    i_m = w("a month", t(i_wk))
    s, e = t(i_s) - 0.3, cover_cut(te(i_m + 1) + 0.45)
    DAYN = "".join(f'<span style="text-align:center;font-family:Typewriter;font-size:22px;color:#7a6e63">{d}</span>' for d in ("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"))
    cells = "".join(f'<div class="dc" id="sc-c{k}"><span>{k + 1}</span><img src="{DAYS[(k * 4) % 9]}"/><b>{TICK}</b></div>' for k in range(28))
    TOP = 500
    cw = (840 - 60) / 7
    ch = cw * 13 / 9
    y0 = TOP + 30 + 84 + 32
    xs = [120 + cw / 2 + k * (cw + 10) for k in range(7)]
    path = "M" + " L".join(f"{x:.0f} {y0 + ch / 2 + (18 if k % 2 else -18):.0f}" for k, x in enumerate(xs))
    s = scene("sc", s, e, f"""
{head('sc', 'a full', 'schedule', 200, 140)}
  <div class="mon10 card10" id="sc-cal" style="top:{TOP}px"><div class="mh">your month<small>1 video a day</small></div>
    <div class="gd" style="margin-bottom:8px">{DAYN}</div><div class="gd">{cells}</div></div>
  <svg class="st10" viewBox="0 0 1080 1920"><path id="sc-p" d="{path}"/></svg>
  <div class="stp4" id="sc-st" style="left:300px;top:1500px">1 month</div>""")
    rev("#sc-a", s + 0.02, 14)
    slam("#sc-h", t(i_s + 1) - 0.05, 1.4)
    ft("#sc-cal", s + 0.04, {"opacity": 0, "y": 100}, {"opacity": 1, "y": 0}, 0.4, "back.out(1.4)")

    def fill(ks, a, d):
        for n, k in enumerate(ks):
            at = a + d * n / max(1, len(ks))
            ft(f"#sc-c{k} img", at, {"opacity": 0, "scale": 1.4}, {"opacity": 1, "scale": 1}, 0.18, "power2.out")
            ft(f"#sc-c{k} b", at + 0.1, {"opacity": 0, "scale": 0}, {"opacity": 1, "scale": 1}, 0.15, "back.out(2.6)")
            if n % 2 == 0:
                sfx.append(("click_004", at, 0.06))
    fill(range(7), s + 0.35, max(0.6, t(i_st) - s - 0.45))
    ft("#sc-p", t(i_st) - 0.1, {"strokeDashoffset": 2600}, {"strokeDashoffset": 0}, max(0.5, t(i_wk) - t(i_st) + 0.2), "power1.inOut")
    sfx.append(("scribble", t(i_st), 0.16))
    if i_fw is not None:
        fill(range(7, 21), t(i_fw) - 0.2, max(0.5, t(i_m) - t(i_fw)))
        fill(range(21, 28), t(i_m) - 0.1, 0.4)
    else:
        fill(range(7, 28), t(i_m) - 0.3, 0.6)
    stamp("#sc-st", te(i_m + 1) - 0.1, -6)


def pg_hours():
    """'So instead of spending hours every day editing, filming, planning content,' — every day of the week stacks up hours,
    one colour per job, on its word."""
    i_sp = w("instead of spending")
    i_h = w("hours", t(i_sp))
    i_e = w("editing", t(i_sp))
    i_f = w("filming", t(i_e))
    i_p = w("planning", t(i_f))
    s, e = t(i_sp) - 0.1, cover_cut(te(i_p + 1) + 0.4)
    DAYS7 = ("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN")
    H = [(26, 22, 14), (30, 18, 16), (24, 26, 12), (32, 20, 18), (28, 24, 14), (22, 28, 16), (30, 16, 20)]
    cols = "".join(f'<div class="col"><span>{d}</span><i class="e" id="hr-e{k}" style="height:{a}%"></i><i class="f" id="hr-f{k}" style="height:{b}%"></i><i class="p" id="hr-p{k}" style="height:{c}%"></i></div>' for k, (d, (a, b, c)) in enumerate(zip(DAYS7, H)))
    s = scene("hr", s, e, f"""
{head('hr', 'spending', 'hours', 200, 140)}
  <div class="hb10">{cols}</div>
  <div class="lg10"><span id="hr-k0"><i style="background:#17120e"></i>editing</span><span id="hr-k1"><i style="background:#5d5650"></i>filming</span><span id="hr-k2"><i style="background:#b9b0a5"></i>planning</span></div>""")
    rev("#hr-a", s + 0.02, 14)
    slam("#hr-h", t(i_h) - 0.05, 1.4)
    for j, (cls, i) in enumerate((("e", i_e), ("f", i_f), ("p", i_p))):
        at = t(i) - 0.1
        ft(f".hb10 i.{cls}", at, {"scaleY": 0}, {"scaleY": 1, "stagger": 0.04}, 0.3, "back.out(1.4)")
        ft(f"#hr-k{j}", at, {"opacity": 0, "y": 16}, {"opacity": 1, "y": 0}, 0.25)
        sfx.append(("pluck_001" if j % 2 else "tick_002", at, 0.18))


def once_stickers():
    """'pick one time a month, one time a week, film for 20 to 30 minutes' — a calendar sticker flips month -> week, then a
    stopwatch sticker runs to 30:00."""
    i_m = w("one time a month")
    i_w = w("one time a week", t(i_m))
    i_f = w("film for", t(i_w))
    i_end = w("minutes", t(i_f))
    sticker("on1", f'<span class="ic8">{ic("cal", 62)}</span><span id="on1-t">once a month</span>', 150, 1590, -4, t(i_m) - 0.05, t(i_f) - 0.1)
    text_at("on1-t", t(i_w) - 0.05, "once a week", "once a month")
    ft("#on1", t(i_w) - 0.05, {"rotationX": 0}, {"rotationX": 360}, 0.35, "power2.inOut", False)
    sfx.append(("click_004", t(i_w), 0.14))
    OV.append(stopwatch("on2", 760, 1520, 0.62))
    ft("#on2", t(i_f) - 0.15, {"opacity": 0, "scale": 0.3}, {"opacity": 1, "scale": 1}, 0.35, "back.out(2)")
    watch_run("on2", t(i_f) + 0.1, max(0.6, te(i_end) - t(i_f) - 0.1), 0, 30)
    to("#on2", te(i_end) + 0.35, {"opacity": 0, "scale": 0.4}, 0.2)


def pg_done():
    """'(and you have all the content you need.) Claude will handle all of it.' — the month of clips fills round the Claude
    mark, which spins in on 'Claude'; HANDLED stamps down on 'all of it'."""
    i0 = w("you have all") if has("you have all") else w("claude will handle")
    i_c = w("claude will handle")
    i_all = w("all of it", t(i_c)) + 2
    s, e = t(i0) - 0.1, cover_cut(te(i_all) + 0.45)
    grid = "".join(f'<div class="clp10" id="dn-{k}" style="left:{90 + (k % 4) * 232}px;top:{460 + (k // 4) * 330}px;width:200px;height:300px"><img src="{DAYS[k % 9]}"/></div>' for k in range(12))
    s = scene("dn", s, e, f"""
{head('dn', 'all the', 'content', 200, 140)}
  {grid}
  <div style="position:absolute;left:390px;top:780px;width:300px;height:300px;border-radius:90px;background:#fbf9f5;box-shadow:0 30px 60px rgba(60,40,24,.3);display:flex;align-items:center;justify-content:center;z-index:6" id="dn-cl">{CLAUDE.format(200)}</div>
  <div class="stp4" id="dn-st" style="left:300px;top:1500px">handled</div>""")
    rev("#dn-a", s + 0.02, 14)
    slam("#dn-h", s + 0.1, 1.4)
    span = max(0.6, t(i_c) - s - 0.3)
    for k in range(12):
        at = s + 0.1 + span * k / 12
        ft(f"#dn-{k}", at, {"opacity": 0, "scale": 0.4, "rotation": (k % 3 - 1) * 10}, {"opacity": 1, "scale": 1, "rotation": (k % 3 - 1) * 2}, 0.3, "back.out(1.8)")
        if k % 2 == 0:
            sfx.append(("click_004", at, 0.07))
    ft("#dn-cl", t(i_c) - 0.15, {"opacity": 0, "scale": 0.2, "rotation": -220}, {"opacity": 1, "scale": 1, "rotation": 0}, 0.5, "back.out(1.8)")
    sfx.append(("hard-pop-click", t(i_c), 0.26))
    stamp("#dn-st", t(i_all - 2) + 0.05, -7)


def cta10(final):
    """'leave me a follow' — a Follow button sticker; a cursor clicks it on 'follow'."""
    i = w("leave me a follow")
    i_f = i + 3
    out = DURATION - 0.1 if final else t(w("see you in")) + 0.05
    sticker("cta", f'<span class="ic8">{ic("user", 62, "#fbf9f5")}</span><span id="cta-t">Follow</span>', 330, 1590, -4, t(i) - 0.1, out, "dk")
    OV.append(f'<div id="cta-cur" class="cursor" style="z-index:30">{CUR}</div>')
    click("#cta-cur", 520, 1660, t(i_f) + 0.05, frm=(1000, 1750), leave=(1150, 1800))
    text_at("cta-t", t(i_f) + 0.1, "Following ✓", "Follow")
    ft("#cta", t(i_f) + 0.08, {"scale": 1}, {"scale": 0.92, "yoyo": True, "repeat": 1}, 0.08, "power2.out", False)
