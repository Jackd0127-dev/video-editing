# ================================================================= Day 13: "an AI receptionist for wedding venues". Jack's own pre-cut take
# (dead air out, his "Coming up.." teaser and riser kept). Mostly his face with captions (day10-audit): paper notes beside him,
# placed off his face from the face track (pages12 helpers), punch-ins on every turn of the 86 s phone call, Jess's lines tagged
# as the AI. Pages: the Day 13 card, a "comment PART 2" card and the Day 14 end card.

TAIL = 5.2  # after his last word (V1): the part 2 card, then the end card
UNDER_CHIN = False  # the notes live on his chest: captions always sit above his head
TEASER_END = 2.3 if N == 1 else 0.0  # V1 opens on his own 'Coming up..' teaser: his text is on screen, no captions
HAIR = 0.9  # Vision's face box starts at the brows; his forehead and hair add ~0.9 of its height against the sky


def pg_day13():
    """'this is day thirteen of thirty different things' — the series stat page; twelve blocks lit, today's lifts."""
    i = w("day thirteen")
    s, e = t(i - 2) - 0.06, cover_cut(t(i + 3) + 0.6)
    scene("pday", s, e, f"""
  <div class="stack" style="left:0;right:0;top:600px">
    <span class="sm" style="font-size:56px">{words_in('pdw', i - 2, 2)}</span>
    <div class="row" style="align-items:flex-end;justify-content:center;margin-top:10px">
      <span id="pday-d" class="xb" style="font-size:230px;line-height:1">Day</span>
      <span id="pday-n" class="xb" style="font-size:230px;line-height:1;margin-left:40px">13</span>
    </div>
    <span class="sm" style="font-size:56px;margin-top:22px">{words_in('pdo', i + 2, 2)}</span>
  </div>
  <div id="pday-bar" class="bar big" style="top:1250px">{BLOCKS.replace('{p}', 'pday')}</div>""")
    ft("#pday-d", t(i) - 0.05, {"opacity": 0, "y": 60, "filter": "blur(14px)"}, {"opacity": 1, "y": 0, "filter": "blur(0px)"}, 0.4, "expo.out")
    slam("#pday-n", t(i + 1) - 0.05)
    ft("#pday-bar .seg", t(i + 1), {"scaleY": 0, "opacity": 0}, {"scaleY": 1, "opacity": 1, "stagger": 0.01}, 0.22, "power2.out")
    ft(", ".join(f"#pday-s{k}" for k in range(12)), t(i + 1) + 0.2, {"backgroundColor": "rgba(23,18,14,.14)"}, {"backgroundColor": INK, "stagger": 0.03}, 0.15)
    ft("#pday-s12", t(i + 3), {"backgroundColor": "rgba(23,18,14,.14)", "scaleY": 1}, {"backgroundColor": INK, "scaleY": 1.9}, 0.45, "back.out(2.2)")
    sfx.extend([("dry-pop-alert", t(i + 1), 0.24), ("pluck_001", t(i + 3), 0.26)])


def today13():
    """'an AI receptionist I've built for wedding and event venues … how you can build the same and monetize it.'"""
    i_r = w("an AI receptionist")
    i_v = w("wedding and event venues")
    note("rc13", f'<div class="k">I built an</div><div class="row" style="align-items:center;gap:12px;margin-top:6px">{ic("phone", 50)}<span class="b" style="font-size:54px">AI receptionist</span></div>', 420, 120, t(i_r + 1) - 0.1, t(i_v) - 0.25)
    plist("vn13", "for", ["wedding venues", "event venues"], [t(i_v), t(i_v + 2)], t(w("and I'm gonna be showing")) + 0.1, [t(i_v) + 0.3, t(i_v + 2) + 0.3], w_=320)
    i_b, i_m = w("build the same"), w("monetize it")
    plist("hw13", "how to", ["build it", "make money from it"], [t(i_b), t(i_m)], min(te(i_m + 1) + 0.35, min(c for c in CUTS if c > t(i_m)) - 0.05), w_=360)


def dial13():
    """He dials (real phone in shot): 'calling Willowmere House…' until Jess answers."""
    i_j = w("hey this is jess")
    a = CUTS_ALL[3] + 0.15  # 17.7 s: the dialling shot
    note("dl13", f'<div class="k">calling</div><div class="b" style="font-size:52px;margin-top:6px">Willowmere House</div><div class="dots"><i></i><i></i><i></i></div>', 420, 140, a, t(i_j) - 0.05, pos=(470, 1470))  # right of the phone he's dialling
    for k in range(3):
        ft(f"#dl13 .dots i:nth-child({k + 1})", a + 0.3 + k * 0.18, {"opacity": 0.15}, {"opacity": 1, "yoyo": True, "repeat": 7}, 0.36, "sine.inOut")


def jess13():
    """'Hey, this is Jess from Willowmere House. How can I help?' — who answered: Jess, the AI receptionist."""
    i = w("hey this is jess")
    note("js13", f'<div class="k">answered by</div><div class="b" style="font-size:84px;margin-top:4px">Jess</div><div class="ln" style="margin-top:6px;font-size:30px">{mark("js13-t")}<span>AI, not a person</span></div>', 330, 190, t(i + 3) - 0.1, te(w("how can i help") + 3) + 0.3)
    draw("js13-t", t(w("how can i help")))


def weddings13():
    """'We do weddings, yes. I'm not sure about other types of events, so I'd need to check with the team on that.'"""
    i_y = w("we do weddings")
    i_o, i_c = w("other types of events"), w("check with the team")
    note("wd13", f'<div class="ln" style="margin-top:0">{mark("wd13-t")}<span>weddings</span></div><div class="ln" id="wd13-r" style="opacity:0">{mark("wd13-q", "cross")}<span>other events?</span></div><div class="k" id="wd13-k" style="opacity:0;margin-top:10px">→ asks the team</div>', 320, 190, t(i_y) - 0.1, te(i_c + 4) + 0.3)
    draw("wd13-t", t(i_y + 3))
    ft("#wd13-r", t(i_o) - 0.1, {"opacity": 0, "x": -16}, {"opacity": 1, "x": 0}, 0.25)
    ft("#wd13-k", t(i_c), {"opacity": 0, "x": -16}, {"opacity": 1, "x": 0}, 0.25)
    sfx.append(("click_004", t(i_c), 0.08))


def guests13():
    """'a wedding venue that would accommodate around 200 guests' — the head count rolls up to 200."""
    i = w("around 200 guests")
    note("gs13", '<div class="k">guests</div><div class="b" style="font-size:110px;margin-top:2px" id="gs13-n">0</div>', 240, 170, t(i) - 0.2, t(w("i checked all around")) + 0.2)
    count_js("gs13-n", 0, 200, t(i + 1) - 0.1, 0.7)
    sfx.extend([("tick_002", t(i + 1) - 0.1 + k * 0.07, 0.06) for k in range(9)])


def capacity13():
    """'maximum seated daytime capacity is 140, and our total evening capacity is 180. So 200 guests would be above what we can
    accommodate.' — three ink bars; the 200 bar overflows and gets crossed out."""
    i140, i180 = w("140"), w("180")
    i_ab = w("above what we can")
    rows = "".join(f'<div class="br" id="cp13-r{k}"{" style=\"opacity:0\"" if k else ""}><span>{lb}</span><i><b id="cp13-b{k}" style="width:{pct}%"></b></i><em>{n}</em></div>'
                   for k, (lb, pct, n) in enumerate([("seated", 70, 140), ("evening", 90, 180), ("you", 100, 200)]))
    note("cp13", f'<div class="k">capacity</div>{rows}<svg class="mk2 cpx" id="cp13-x" viewBox="0 0 24 24"><path pathLength="100" d="{CROSS_D}"/></svg>', 400, 230, t(i140) - 0.6, te(w("accommodate", t(i_ab))) + 0.4)
    for k, at in enumerate([t(i140), t(i180), t(w("200 guests", t(i180)))]):
        if k:
            ft(f"#cp13-r{k}", at - 0.15, {"opacity": 0, "x": -16}, {"opacity": 1, "x": 0}, 0.25)
        ft(f"#cp13-b{k}", at - 0.05, {"scaleX": 0}, {"scaleX": 1}, 0.5, "power3.out")
        sfx.append(("click_004", at, 0.08))
    draw("cp13-x", t(i_ab))


def dates13():
    """'I'd need to check our wedding date availability to give you a proper answer.'"""
    i = w("wedding date availability")
    note("dt13", f'<div class="row" style="align-items:center;gap:14px">{ic("cal", 56)}<div><div class="k">dates?</div><div class="b" style="font-size:40px;margin-top:4px">checks the diary</div></div></div>', 360, 110, t(i) - 0.1, te(w("proper answer") + 1) + 0.35)


def menu13():
    """'Do you accommodate for vegetarians and vegans?' / 'Yes, we do offer both vegetarian and vegan catering options.'"""
    i_q = w("vegetarians and vegans")
    i_a = w("both vegetarian and vegan")
    plist("mn13", "menu", ["vegetarian", "vegan"], [t(i_q), t(i_q + 2)], te(w("in house") + 1) + 0.3, [t(i_a + 1) + 0.1, t(i_a + 3) + 0.1], w_=280)


def viewing13():
    """'I'm gonna give you a phone back tomorrow … book a viewing or something like that.'"""
    i_t = w("phone back tomorrow")
    i_v = w("book a viewing")
    note("vw13", f'<div class="k">next step</div><div class="ln" style="margin-top:8px">{ic("phone", 36)}<span>call back tomorrow</span></div><div class="ln" id="vw13-r" style="opacity:0">{ic("cal", 36)}<span>book a viewing</span></div>', 380, 170, t(i_t + 2) - 0.2, te(w("like that", t(i_v)) + 1) + 0.35)
    ft("#vw13-r", t(i_v + 2) - 0.1, {"opacity": 0, "x": -16}, {"opacity": 1, "x": 0}, 0.25)
    sfx.append(("click_004", t(i_v + 2), 0.08))


def ended13():
    """Jess's last 'Bye.' — the call ends: how long it ran."""
    i = w("bye", 104)
    a = t(i)
    dur = a - t(w("hey this is jess"))
    note("en13", f'<div class="k">call ended</div><div class="b" style="font-size:72px;font-family:Typewriter;letter-spacing:0;margin-top:4px">{int(dur // 60)}:{int(dur % 60):02d}</div>', 230, 140, a - 0.05, CUTS_ALL[6] - 0.05)
    sfx.append(("pluck_001", a, 0.2))


def db13():
    """'I had to set up a bit of a database so it can take bookings and stuff like that.'"""
    i_d, i_b = w("a bit of a database"), w("take bookings")
    note("db13", f'<div class="k">behind Jess</div><div class="b" style="font-size:52px;margin-top:6px">a database</div><div class="ln" id="db13-r" style="opacity:0">{mark("db13-t")}<span>takes bookings</span></div>', 330, 170, t(i_d + 4) - 0.2, te(w("like that", t(i_b)) + 1) + 0.3)
    ft("#db13-r", t(i_b) - 0.1, {"opacity": 0, "x": -16}, {"opacity": 1, "x": 0}, 0.25)
    draw("db13-t", t(i_b + 1))


def trained13():
    """'once it actually gets trained on your internal data … the tools that you use … fully automated.'"""
    at = [t(w("internal data")) + 0.2, t(w("tools that you use")), t(w("fully automated"))]
    plist("tr13", "once it's", ["trained on your data", "plugged into your tools", "fully automated"], at, te(w("fully automated") + 1) + 0.3, [a + 0.35 for a in at], w_=420)


def always13():
    """'24/7, no downtime, no workers taking off sick.'"""
    i = w("24/7")
    i_d, i_s = w("no down time"), w("off sick")
    note("al13", f'<div class="b" style="font-size:110px">24/7</div><div class="ln" id="al13-a" style="opacity:0">{mark("al13-t")}<span>no downtime</span></div><div class="ln" id="al13-b" style="opacity:0">{mark("al13-u")}<span>no sick days</span></div>', 320, 250, t(i) - 0.15, te(i_s + 1) + 0.35)
    ft("#al13-a", t(i_d) - 0.1, {"opacity": 0, "x": -16}, {"opacity": 1, "x": 0}, 0.25)
    draw("al13-t", t(i_d + 1))
    ft("#al13-b", t(i_s - 3) - 0.1, {"opacity": 0, "x": -16}, {"opacity": 1, "x": 0}, 0.25)
    draw("al13-u", t(i_s))


def pg_part2(s, e):
    """Jack's ask: 'leave a comment if you want part 2' — want part 2? / comment PART 2 (how to build it and sell it)."""
    scene("cta", s, e, f"""
  <div class="stack" style="left:0;right:0;top:520px">
    <span id="cta-w" class="sm" style="font-size:60px">want</span>
    <span id="cta-p" class="xb" style="font-size:210px;line-height:1">Part 2?</span>
    <span id="cta-s" class="sm" style="font-size:44px;margin-top:20px">how to build it &amp; sell it</span>
  </div>
  <div id="cta-c" class="cm13" style="top:1150px"><div class="av">{ic("user", 44, "#fbf9f5")}</div><div class="tx"><div class="ck">comment</div><div class="cbb">{typed_words("cta-tw", "PART 2")}<i class="caret"></i></div></div></div>""")
    rev("#cta-w", s + 0.05, 14)
    slam("#cta-p", s + 0.2)
    rev("#cta-s", s + 0.55, 16)
    ft("#cta-c", s + 0.8, {"opacity": 0, "y": 50, "scale": 0.9}, {"opacity": 1, "y": 0, "scale": 1}, 0.4, "back.out(1.7)")
    type_on("cta-tw", 2, s + 1.15, s + 1.45)
    ft("#cta-c", s + 1.75, {"scale": 1}, {"scale": 1.06, "yoyo": True, "repeat": 1}, 0.14, "power2.out", False)
    sfx.extend([("dry-pop-alert", s + 0.2, 0.24), ("drop_002", s + 0.8, 0.14), ("pluck_001", s + 1.75, 0.22)])


def pg_end13(s):
    """End card: see you on Day 14 tomorrow; thirteen blocks lit, zoom into today's."""
    ZX, ZY = 90 + 12 * (SEG_W + 6) + SEG_W / 2, 1340 - 40 * 1.9 / 2
    scene("ed", s, DURATION, f"""
  <div id="ed-zoom" style="position:absolute;inset:0;transform-origin:{ZX:.1f}px {ZY:.1f}px">
    <div class="stack" style="left:0;right:0;top:560px">
      <span id="ed-sy" class="sm" style="font-size:56px">see you on</span>
      <div class="row" style="align-items:flex-end;justify-content:center;margin-top:6px">
        <span id="ed-day" class="xb" style="font-size:230px;line-height:1">Day</span>
        <span id="ed-n" class="xb" style="font-size:230px;line-height:1;margin-left:40px">14</span>
      </div>
      <span id="ed-tm" class="sm" style="font-size:52px;margin-top:20px">tomorrow</span>
    </div>
    <span id="ed-lbl" class="note" style="position:absolute;left:{90 + 12 * (SEG_W + 6) - 40:.0f}px;top:1186px">day 13 / 30</span>
    <div id="ed-bar" class="bar big" style="top:1300px">{BLOCKS.replace('{p}', 'ed')}</div>
  </div>""", whoosh=False)
    rev("#ed-sy", s + 0.05, 14)
    rev("#ed-day", s + 0.2, 30)
    slam("#ed-n", s + 0.4)
    rev("#ed-tm", s + 0.7, 16)
    ft("#ed-bar .seg", s + 0.1, {"scaleY": 0, "opacity": 0}, {"scaleY": 1, "opacity": 1, "stagger": 0.01}, 0.25, "power2.out")
    lit = s + 0.9
    ft(", ".join(f"#ed-s{k}" for k in range(12)), lit - 0.3, {"backgroundColor": "rgba(23,18,14,.14)"}, {"backgroundColor": INK, "stagger": 0.035}, 0.18)
    ft("#ed-s12", lit, {"backgroundColor": "rgba(23,18,14,.14)", "scaleY": 1}, {"backgroundColor": INK, "scaleY": 1.9}, 0.5, "back.out(2.2)")
    ft("#ed-lbl", lit + 0.15, {"opacity": 0, "y": 12}, {"opacity": 1, "y": 0}, 0.35, "power2.out")
    zoom_at = DURATION - 1.4
    to("#ed-lbl", zoom_at, {"opacity": 0}, 0.3)
    ft("#ed-zoom", zoom_at, {"scale": 1, "x": 0, "y": 0}, {"scale": 60, "x": round(540 - ZX, 1), "y": round(960 - ZY, 1)}, 1.3, "power3.inOut")
    sfx.extend([("dry-pop-alert", s + 0.4, 0.24), ("pluck_001", lit, 0.3), ("riser", zoom_at + 0.25, 0.35), ("boom", DURATION - 0.12, 0.3)])


def call_edges():
    """Punch-in points through the one-take phone call: every change of speaker, and sentence starts inside long turns."""
    a0, a1 = (CUTS_ALL[5], CUTS_ALL[6]) if N == 1 else (SEGS[2]["start"], SEGS[2]["end"])
    out, last = [], a0
    for k in range(1, len(TOK)):
        tt = t(k)
        if not (a0 + 1.0 < tt < a1 - 1.0):
            continue
        turn = TOK[k].get("spk") != TOK[k - 1].get("spk")
        sent = TOK[k - 1]["text"].endswith((".", "?", "!"))
        if (turn and tt - last > 1.6) or (sent and tt - last > 3.0):
            out.append(round(tt - 0.12, 3))
            last = tt
    return out
