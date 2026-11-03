# ================================================================= Day 14: "sell websites to local businesses" (find a barber with no website on
# Google, have Claude build the site, do the outreach from the CRM). The Day 13 look: mostly his face with captions, one taped paper
# note per key moment placed off his face (pages12 helpers). His screen recording plays in a white card under his chin, retimed to
# his words, browser chrome cropped (never the page); the finished site is Claude's real build (edit/site, captured). Pages: the
# Day 14 card, a "what next?" comment card, the Day 15 end card.
import hashlib
import subprocess

TAIL = 5.2
UNDER_CHIN = False  # notes and screens sit on his chest: captions stay above his head
TEASER_END = 0.0
HAIR = 0.9
REC = "/Users/jackd/Documents/Video Editing/footage/day14/Recording 2026-11-03 at 16.18.03.mp4"
CRMREC = "/Users/jackd/Documents/Video Editing/broll/My crm.mp4"
RW, RH, RY = 3024, 1726, 174  # the recording's page area (Chrome's tab strip + address bar = rows 0-173)
CW = 1000  # card width on screen
SITE = "assets/img/site"


def rec_clip(src, r0, r1, dur, crop_y=RY, crop_h=RH):
    """Recording window [r0, r1] retimed to `dur` seconds, browser chrome cropped, at the recording's full 3024 px width (Jack:
    the half-size clips looked pixelated once the card zoomed in), cached in assets/video/rec."""
    key = hashlib.md5(f"full|{src}|{r0:.3f}|{r1:.3f}|{dur:.3f}|{crop_y}|{crop_h}".encode()).hexdigest()[:12]
    out = f"assets/video/rec/{key}.mp4"
    if not os.path.exists(out):
        os.makedirs("assets/video/rec", exist_ok=True)
        sp = (r1 - r0) / dur
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{r0:.3f}", "-t", f"{r1 - r0:.3f}", "-i", src, "-vf",
                        f"crop=iw:{crop_h}:0:{crop_y},setpts=(PTS-STARTPTS)/{sp:.5f},fps=30,tpad=stop_mode=clone:stop_duration=2",
                        "-t", f"{dur + 0.5:.3f}", "-an", "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-tune", "stillimage", "-pix_fmt", "yuv420p", "-g", "15", "-movflags", "+faststart", out], check=True)
    return out


CAPBELOW = []  # (a, b): captions under his chin while a card sits above his head


def screen(sid, a, b, parts, sw=RW, sh=RH, imgs=False):
    """A real screen in a white card. Normally under his chin (1000 wide); when his face sits too low for that (his last take),
    a smaller card above his head, the camera eased down a little (origin at the top edge) and captions under his chin.
    parts: [(src, r0, r1, t0, t1)] recording windows retimed onto [t0, t1] (abutting), or with imgs=True stills the caller swaps."""
    fs = [f for f in FACES if a - 0.4 <= f[0] <= b + 0.4]
    bot = max(((f[2] + f[4]) * 1920 for f in fs), default=900)
    ch = round(CW * sh / sw)
    if bot + 50 + ch <= 1720:
        cw, left, top = CW, 40, int(min(max(bot + 50, 960), 1700 - ch))
        hold_cam(a - 0.1, b + 0.2)
    else:
        z = float(os.environ.get("CARD_UP_Z", 1.1))  # Jack, round 4: the gentle round-2 zoom, not a big push
        cw = int(os.environ.get("CARD_UP_W", 880))
        ch = round(cw * sh / sw)
        top = max(110, 642 - ch)  # the big card moves up instead: its bottom stays where the 600 px card's was, clear of his head
        left = (1080 - cw) // 2
        r0 = max(a - 0.6, 0.55)  # the push finishes before the card lands; never during the opening zoom-out (it fought it: V2's glitch)
        CAM_WINS.append((r0, b, z, 0))
        CAPBELOW.append((r0, b + 0.2))
    inner = ""
    if imgs:
        inner = "".join(f'<img class="sci" id="{sid}-i{k}" src="{p}"/>' for k, p in enumerate(parts))
    else:
        for k, (src, r0, r1, t0, t1) in enumerate(parts):
            crop = (RY, RH) if src == REC else (172, 1648)
            inner += vtag(f"{sid}-v{k}", rec_clip(src, r0, r1, t1 - t0, *crop), t0, t1 - t0, "scv")
    inner += f'<svg class="rgs" id="{sid}-rg" viewBox="0 0 {sw} {sh}"><!--RG:{sid}--></svg>'
    VL.append(f'<div class="scr" id="{sid}" style="left:{left}px;top:{top}px;width:{cw}px;height:{ch}px"><div class="scz" id="{sid}-z" style="width:{cw}px;height:{ch}px">{inner}</div></div>')
    ft(f"#{sid}", a, {"opacity": 0, "y": 140 if cw == CW else -60, "scale": 0.9, "rotation": -2.5}, {"opacity": 1, "y": 0, "scale": 1, "rotation": 0}, 0.55, "expo.out")
    to(f"#{sid}", b - 0.3, {"opacity": 0, "y": 90 if cw == CW else -40, "scale": 0.94}, 0.3, "power2.in")
    sfx.append(("arrow-whoosh", a - 0.05, 0.12))
    CARDS[sid] = (top, ch, sw, sh, cw, left)
    return top, ch


CARDS = {}


def zoom_to(sid, at, rect, d=0.6, smax=2.6, e="power3.inOut"):
    """Zoom the card's screen onto a source-pixel rect (kept inside the card)."""
    top, ch, sw, sh, cw, left = CARDS[sid]
    k = cw / sw
    x0, y0, x1, y1 = rect
    s = min(smax, cw / ((x1 - x0) * k) * 0.92, ch / ((y1 - y0) * k) * 0.92)
    tx = cw / 2 - (x0 + x1) / 2 * k * s
    ty = ch / 2 - (y0 + y1) / 2 * k * s
    tx = min(0, max(cw - cw * s, tx))
    ty = min(0, max(ch - ch * s, ty))
    to(f"#{sid}-z", at, {"scale": round(s, 3), "x": round(tx, 1), "y": round(ty, 1)}, d, e)


def zoom_out(sid, at, d=0.55):
    to(f"#{sid}-z", at, {"scale": 1, "x": 0, "y": 0}, d, "power3.inOut")


RGN = [0]
RINGS = {}


CAM_WINS = []  # (start, end, zoom, origin y) for every card / site window


def cam_chain():
    """One camera path for all the cards (Jack: 'constant zooming out and in'): cards under 1.5 s apart hold the zoom or glide
    straight to the next one, instead of easing out and back in. Written as scale + y from the top edge so any two framings blend."""
    wins = sorted(CAM_WINS)
    for k, (r0, b, z, oy) in enumerate(wins):
        y = round(oy * (1 - z), 1)
        prev = wins[k - 1] if k else None
        nxt = wins[k + 1] if k + 1 < len(wins) else None
        chained_in = prev is not None and r0 - prev[1] < 1.5
        chained_out = nxt is not None and nxt[0] - b < 1.5
        pz, py = (prev[2], round(prev[3] * (1 - prev[2]), 1)) if chained_in else (1, 0)
        at = max(r0, prev[1] - 0.25) if chained_in else r0
        if (pz, py) != (z, y):
            CAMJS.append(f"tl.fromTo('#cam', {{scale:{pz}, y:{py}, transformOrigin:'540px 0px'}}, {{scale:{z}, y:{y}, duration:.5, ease:'power2.inOut', immediateRender:false}}, {at:.3f});")
        if not chained_out:
            CAMJS.append(f"tl.fromTo('#cam', {{scale:{z}, y:{y}, transformOrigin:'540px 0px'}}, {{scale:1, y:0, duration:.45, ease:'power2.inOut', immediateRender:false}}, {b - 0.25:.3f});")
        end = nxt[0] if chained_out else b + 0.2
        CAMFIX.append((r0, end))
        CAMMAP.append((r0, end, z, z, 540, oy))


def finalize14():
    """Ring paths go into their card's svg (built before the rings were known)."""
    cam_chain()
    for k, v in enumerate(VL):
        for sid, paths in RINGS.items():
            v = v.replace(f"<!--RG:{sid}-->", "".join(paths))
        VL[k] = v
    print("  rings drawn at: " + ", ".join(f"{sid}@{t_:.2f}" for sid, _, t_ in RINGLOG))


def ring(sid, rect, at, out, pad=10, sw_=None, px=4.5, dur=0.62):
    """A hand-drawn ink loop round a source-pixel rect (Jack, Day 14: rings must go round the thing, every time). A rounded
    rectangle `pad` screen px outside the rect — an ellipse cuts the corners of anything wide — drawn on in one stroke that
    overshoots its start a little, like a pen. It lives inside the zoom layer, so it stays on the element at any zoom."""
    RGN[0] += 1
    rid = f"{sid}-r{RGN[0]}"
    top, ch, sw, sh, cw, left = CARDS[sid]
    k = cw / sw  # screen px per source px (before zoom)
    pu = pad / k
    x0, y0, x1, y1 = rect[0] - pu, rect[1] - pu, rect[2] + pu, rect[3] + pu
    w, h = x1 - x0, y1 - y0
    r = min(16 / k, h / 2, w / 2)
    sx, ex, dr = x0 + 0.3 * w, x0 + 0.46 * w, 3 / k
    d = (f"M{sx:.1f} {y0:.1f} L{x1 - r:.1f} {y0:.1f} Q{x1:.1f} {y0:.1f} {x1:.1f} {y0 + r:.1f} L{x1:.1f} {y1 - r:.1f} Q{x1:.1f} {y1:.1f} {x1 - r:.1f} {y1:.1f} "
         f"L{x0 + r:.1f} {y1:.1f} Q{x0:.1f} {y1:.1f} {x0:.1f} {y1 - r:.1f} L{x0:.1f} {y0 + r:.1f} Q{x0:.1f} {y0:.1f} {x0 + r:.1f} {y0:.1f} L{ex:.1f} {y0 - dr:.1f}")
    RINGS.setdefault(sid, []).append(f'<path id="{rid}" class="rgp" pathLength="100" stroke-width="{px / k:.1f}" d="{d}"/>')
    ft(f"#{rid}", at, {"strokeDashoffset": 100, "opacity": 1}, {"strokeDashoffset": 0, "opacity": 1}, dur, "power2.inOut", False)
    to(f"#{rid}", out, {"opacity": 0}, 0.2)
    sfx.append(("scribble", at, 0.14))
    RINGLOG.append((sid, rid, at + 0.7))


RINGLOG = []


def cut_out(k_phrase, after=0.0, pad=0.35):
    return te(w(k_phrase, after) + len(k_phrase.split()) - 1) + pad


# ---------------------------------------------------------------- hook, day card, today
def hook14():
    """'If you're good at sales and you wanna make some quick cash, here's a really really good way…'"""
    if not has("good at sales"):
        return
    i_s, i_c = w("good at sales"), w("quick cash")
    note("hk14", f'<div class="k">if you\'re good at</div><div class="ln" style="margin-top:6px">{mark("hk14-t")}<span class="b" style="font-size:58px">sales</span></div>'
                 f'<div class="ln" id="hk14-r" style="opacity:0;font-size:40px">→ <span>quick cash</span></div>', 300, 170, t(i_s + 2) - 0.25, cut_out("streamline it"))
    draw("hk14-t", t(i_s + 2) + 0.1)
    ft("#hk14-r", t(i_c) - 0.1, {"opacity": 0, "x": -16}, {"opacity": 1, "x": 0}, 0.25)
    sfx.append(("pluck_001", t(i_c + 1), 0.18))
    if N == 1:  # a short build into the day card
        sfx.append(("riser", t(w("day fourteen")) - 0.95, 0.14))


def pg_day14():
    """'today is day fourteen of thirty different things' — the series stat page; thirteen blocks lit, today's lifts."""
    i = w("day fourteen")
    s, e = t(i - 2) - 0.06, cover_cut(t(i + 3) + 0.6)
    scene("pday", s, e, f"""
  <div class="stack" style="left:0;right:0;top:600px">
    <span class="sm" style="font-size:56px">{words_in('pdw', i - 2, 2)}</span>
    <div class="row" style="align-items:flex-end;justify-content:center;margin-top:10px">
      <span id="pday-d" class="xb" style="font-size:230px;line-height:1">Day</span>
      <span id="pday-n" class="xb" style="font-size:230px;line-height:1;margin-left:40px">14</span>
    </div>
    <span class="sm" style="font-size:56px;margin-top:22px">{words_in('pdo', i + 2, 2)}</span>
  </div>
  <div id="pday-bar" class="bar big" style="top:1250px">{BLOCKS.replace('{p}', 'pday')}</div>""")
    ft("#pday-d", t(i) - 0.05, {"opacity": 0, "y": 60, "filter": "blur(14px)"}, {"opacity": 1, "y": 0, "filter": "blur(0px)"}, 0.4, "expo.out")
    slam("#pday-n", t(i + 1) - 0.05)
    ft("#pday-bar .seg", t(i + 1), {"scaleY": 0, "opacity": 0}, {"scaleY": 1, "opacity": 1, "stagger": 0.01}, 0.22, "power2.out")
    ft(", ".join(f"#pday-s{k}" for k in range(13)), t(i + 1) + 0.2, {"backgroundColor": "rgba(23,18,14,.14)"}, {"backgroundColor": INK, "stagger": 0.03}, 0.15)
    ft("#pday-s13", t(i + 3), {"backgroundColor": "rgba(23,18,14,.14)", "scaleY": 1}, {"backgroundColor": INK, "scaleY": 1.9}, 0.45, "back.out(2.2)")
    sfx.extend([("dry-pop-alert", t(i + 1), 0.24), ("pluck_001", t(i + 3), 0.26)])


def today14():
    """'scrape Google reviews, automate a website builder, and then automate the outreach' — today's three steps, ticked."""
    if N == 3:  # V3 opens on this line: a soft build into its last step
        sfx.append(("riser-long", max(0.05, t(w("the outreach")) - 2.7), 0.14))
    at = [t(w("scrape google")), t(w("website builder")), t(w("the outreach"))]
    plist("td14", "today", ["find leads on Google", "build the website", "automate the outreach"], [at[0], at[1] - 0.3, at[2] - 0.2],
          cut_out("the outreach"), [a + 0.35 for a in at], w_=400)


def pitch14():
    """'pitching some web development services to whatever niche … that don't have a website yet'"""
    if not has("web development services"):
        return
    i_p, i_n = w("web development services"), w("don't have a website yet")
    note("pt14", f'<div class="k">pitch</div><div class="b" style="font-size:52px;margin-top:6px">web design</div>'
                 f'<div class="ln" id="pt14-r" style="opacity:0;font-size:30px">{mark("pt14-x", "cross")}<span>businesses with no website</span></div>', 420, 170, t(i_p) - 0.2, cut_out("website yet"))
    ft("#pt14-r", t(i_n) - 0.15, {"opacity": 0, "x": -16}, {"opacity": 1, "x": 0}, 0.25)
    draw("pt14-x", t(i_n + 3))


# ---------------------------------------------------------------- Google: the niche, Advanced Search, past year
def google14():
    """'open Google and type in our niche. Today I'm gonna be doing barbers' — his recording: barbers near me -> results."""
    i_o = w("open google")
    if has("doing barbers"):
        i_b = w("doing barbers")
        a, b = t(i_o) - 0.15, cut_out("works for you", t(i_b)) if has("works for you") else cut_out("doing barbers")
        m = t(i_b) + 0.2
    else:  # V3: "…type in our niche." only
        a, b = t(i_o) - 0.15, cut_out("in our niche")
        m = (a + b) / 2 + 0.3
    screen("sg", a, b, [(REC, 0.4, 6.6, a, m), (REC, 6.6, 11.2, m, b)])
    zoom_to("sg", a + 0.35, (100, 0, 1900, 900), 0.6, 1.6)
    zoom_out("sg", m + 0.1)


def adv14():
    """'go into Tools, Advanced Search … scroll down until you find last update. You're gonna set this to past year.'"""
    i_t = w("tools advanced search")
    i_y = w("past year", t(i_t))
    a, b = t(i_t) - 0.45, te(i_y + 1) + 0.7
    if has("scroll down until you find last update"):
        i_s = w("scroll down until", t(i_t))
        i_l = w("last update", t(i_s))
        T = [a, t(i_t + 1) - 0.1, t(i_s), t(i_l), t(i_y) - 0.15, t(i_y) + 0.45, b]
        R = [10.3, 13.7, 18.6, 21.4, 24.9, 26.2, 28.6]
    else:  # V3: straight from Advanced Search to "past year"
        T = [a, t(i_t + 1) - 0.1, (t(i_t + 1) + t(i_y)) / 2, t(i_y) - 0.15, t(i_y) + 0.45, b]
        R = [10.3, 13.7, 18.6, 24.9, 26.2, 28.6]
    screen("sa", a, b, [(REC, R[k], R[k + 1], T[k], T[k + 1]) for k in range(len(T) - 1)])
    zoom_to("sa", T[-4] - 0.2, (120, 820, 1500, 1500), 0.55, 2.0)
    ring("sa", (468, 948, 1146, 1034), T[4] + 0.2, b - 0.35)


def active14():
    """'This means any businesses that you find are actually going to be active businesses rather than … five or ten years old'"""
    if not has("active businesses"):
        return
    i_a = w("active businesses")
    out = cut_out("redundant") if has("redundant") else te(i_a + 1) + 0.45
    nxt = next((t(w(ph)) for ph in ("head over to google maps", "okay so in google maps") if has(ph) and t(w(ph)) > t(i_a)), None)
    if nxt is not None:  # leave before the Maps card pushes the camera in (the note would slide onto his face)
        out = min(out, nxt - 1.0)
    rows = f'<div class="ln" id="ac14-a" style="opacity:0">{mark("ac14-t")}<span>active businesses</span></div>'
    if has("five or ten years old"):
        rows += f'<div class="ln" id="ac14-b" style="opacity:0">{mark("ac14-x", "cross")}<span>5–10 years old</span></div>'
    note("ac14", f'<div class="k">last update: past year</div>{rows}', 360, 160 if has("five or ten") else 110, t(i_a) - 0.6, out)
    ft("#ac14-a", t(i_a) - 0.15, {"opacity": 0, "x": -16}, {"opacity": 1, "x": 0}, 0.25)
    draw("ac14-t", t(i_a + 1))
    if has("five or ten years old"):
        i_f = w("five or ten years old")
        ft("#ac14-b", t(i_f) - 0.15, {"opacity": 0, "x": -16}, {"opacity": 1, "x": 0}, 0.25)
        draw("ac14-x", t(w("redundant")))


# ---------------------------------------------------------------- Google Maps: the barbers, Karizma, its reviews
def maps14():
    """'head over to Google Maps … type in your niche … scroll down / find ones with … four to five stars. Here you can see we find
    Karizma Turkish Barber Club. 75 reviews, 4.7 stars. (V3: But no, they do not have any sort of custom website.)' — one card,
    retimed to each phrase; zoom to the panel, ring the 4.7, then (V3) the Overview with no website row."""
    i_h = w("head over to google maps") if has("head over to google maps") else None
    i_m = w("okay so in google maps") if has("okay so in google maps") else None
    i_s = w("scroll down", t(i_m)) if i_m is not None else w("find ones with")
    i_f = w("four to five stars")
    a = t(i_h if i_h is not None else i_m) - 0.2
    T, R = [a], [49.6 if i_h is not None else 52.4]
    if i_m is not None:
        T.append(t(i_m)); R.append(52.6)
    T.append(t(i_s)); R.append(59.2)
    k_here = w("here you can see we find") if has("here you can see we find") and t(w("here you can see we find")) > t(i_f) else None
    nosite = k_here is not None and has("custom website") and not has("fresha link") and t(w("custom website")) > t(k_here)
    if k_here is not None:
        i_r = w("75 reviews", t(k_here))
        T += [t(k_here), t(i_r) - 0.1]; R += [65.6, 67.85]
        if nosite:
            i_n = w("custom website")
            b = te(i_n + 1) + 0.7
            T += [t(i_r + 3) + 0.45]; R += [69.4]
        else:
            b = te(i_r + 3) + 0.6
        T += [b]; R += [69.6]
        parts = [(REC, R[k], R[k + 1], T[k], T[k + 1]) for k in range(len(T) - 2)]
        parts.append((REC, 66.9, 67.6, T[-2], T[-1]) if nosite else (REC, R[-2], R[-1], T[-2], T[-1]))
        screen("sm", a, b, parts)
        zoom_to("sm", t(k_here + 4) - 0.1, (990, 0, 1810, 1000), 0.6, 2.0)
        ring("sm", (1570, 200, 1770, 400), t(i_r) + 0.25, T[-2] - 0.05 if nosite else b - 0.35)
        if nosite:
            zoom_to("sm", T[-2] + 0.05, (1000, 1000, 1800, 1520), 0.5, 2.2)
            ring("sm", (1030, 1030, 1780, 1500), T[-2] + 0.5, b - 0.35, pad=20)
            nosite_tag("sm", t(i_n) - 0.1, b - 0.3)
    else:
        b = te(i_f + 3) + 0.6
        T += [b]; R += [65.0]
        screen("sm", a, b, [(REC, R[k], R[k + 1], T[k], T[k + 1]) for k in range(len(T) - 1)])
    zoom_to("sm", t(i_s) + 0.3, (140, 150, 960, 1700), 0.6, 1.8)
    ring("sm", (150, 990, 950, 1300), t(i_f) - 0.1, t(i_f) + 1.0 if k_here is None else t(k_here) - 0.1)


def open14():
    """V2 cold open: 'Here you can see we find Karizma Turkish Barber Club. 75 reviews, 4.7 stars. But no, they do not have any
    sort of custom website.' — the Maps panel, its 4.7, then the Overview with no website row."""
    i_h = w("here you can see we find")
    i_r = w("75 reviews")
    i_n = w("custom website")
    a, b = 0.75, te(i_n + 1) + 0.7
    T = [a, t(i_r) - 0.1, t(i_r + 3) + 0.5, b]
    parts = [(REC, 65.9, 67.85, T[0], T[1]), (REC, 67.85, 69.4, T[1], T[2]), (REC, 66.9, 67.6, T[2], T[3])]
    screen("so", a, b, parts)
    zoom_to("so", a + 0.45, (990, 0, 1810, 1000), 0.6, 2.0)
    ring("so", (1570, 200, 1770, 400), t(i_r) + 0.25, T[2] - 0.05)
    zoom_to("so", T[2] + 0.05, (1000, 1000, 1800, 1520), 0.5, 2.2)
    ring("so", (1030, 1030, 1780, 1500), T[2] + 0.5, b - 0.35, pad=20)
    nosite_tag("so", t(i_n) - 0.1, b - 0.3)
    sfx.extend([("riser-long", max(0.05, t(i_n) - 3.0), 0.2), ("boom", t(i_n + 1), 0.2)])  # the cliffhanger builds to "custom website"


def nosite_tag(sid, at, out):
    """A small taped note on the card's corner: 'website' with an ink cross."""
    top, ch, sw, sh, cw, left = CARDS[sid]
    nid = f"{sid}-ns"
    VL.append(f'<div class="pn" id="{nid}" style="left:{(left + cw - 330) / 1.35:.0f}px;top:{(top - 70 if cw == CW else top + ch - 50) / 1.35:.0f}px;width:230px;zoom:1.35"><div class="ln" style="margin-top:0">{mark(nid + "-x", "cross")}<span>website</span></div></div>')
    ft(f"#{nid}", at, {"opacity": 0, "y": 40, "rotation": 8, "scale": 0.85}, {"opacity": 1, "y": 0, "rotation": 4, "scale": 1}, 0.4, "back.out(1.7)")
    to(f"#{nid}", out, {"opacity": 0, "y": 20}, 0.22, "power2.in")
    draw(f"{nid}-x", at + 0.3)
    sfx.append(("drop_002", at + 0.05, 0.12))


def validate14():
    """'validate this prospect. We're just gonna look them up, see if they have any sort of website anywhere else, and it's maybe
    just not linked to their Google profile.' — the check, as questions."""
    if not has("look them up"):
        return
    i_l = w("look them up")
    i_w = w("website anywhere else")
    a = (t(w("validate this prospect")) - 0.1) if has("validate this prospect") else t(i_l) - 0.2
    rows = f'<div class="ln" id="vl14-a" style="opacity:0;font-size:32px">{ic("search", 32)}<span>a website anywhere?</span></div>'
    if has("google profile"):
        rows += f'<div class="ln" id="vl14-b" style="opacity:0;font-size:32px">{ic("pin", 32)}<span>linked on Google?</span></div>'
    out = cut_out("google profile") if has("google profile") else cut_out("anywhere else")
    note("vl14", f'<div class="k">validate the lead</div>{rows}', 380, 170 if has("google profile") else 120, a, out)
    ft("#vl14-a", t(i_w) - 0.15, {"opacity": 0, "x": -16}, {"opacity": 1, "x": 0}, 0.25)
    sfx.append(("click_004", t(i_w), 0.08))
    if has("google profile"):
        ft("#vl14-b", t(w("not linked")) - 0.1, {"opacity": 0, "x": -16}, {"opacity": 1, "x": 0}, 0.25)
        sfx.append(("click_004", t(w("not linked")), 0.08))


def nosite14():
    """V1: 'we can see they have a Fresha link here, but no, they do not have any sort of custom website.' — the Overview: address,
    hours, phone, and no website row."""
    if not has("fresha link"):
        return
    i_a, i_n = w("we can see they have"), w("custom website")
    a, b = t(i_a) - 0.2, te(i_n + 1) + 0.6
    screen("sn", a, b, [(REC, 66.55, 67.6, a, b)])
    zoom_to("sn", a + 0.4, (1000, 0, 1800, 1520), 0.6, 1.4)
    zoom_to("sn", t(w("but no")) - 0.1, (1000, 1000, 1800, 1520), 0.5, 2.2)
    ring("sn", (1030, 1030, 1780, 1500), t(w("but no")) + 0.4, b - 0.35, pad=20)
    nosite_tag("sn", t(i_n) - 0.1, b - 0.3)


def qualified14():
    """'So that is a validated prospect, that's a qualified lead' — an ink stamp beside him."""
    if not has("qualified lead"):
        return
    i_q = w("qualified lead")
    x, y = spot(t(i_q) - 0.3, te(i_q + 1) + 0.6, 660, 150)
    OV.append(f'<div class="inkst q14" id="ql14" style="left:{x:.0f}px;top:{y:.0f}px">qualified lead</div>')
    stamp("#ql14", t(i_q) - 0.05, -7)
    to("#ql14", cut_out("build the website") - 0.1, {"opacity": 0}, 0.22)
    hold_cam(t(i_q) - 0.3, cut_out("build the website") + 0.2)


# ---------------------------------------------------------------- Claude: the prompt, smart delegation
def claude14():
    """'head over to Claude here. (I'm gonna open up a new chat,) and I'm gonna paste this special skill … (we're gonna use smart
    delegation.)' — his recording: new chat, the prompt pasted, /smart-delegation highlighted. He turns his head to the laptop
    on 'So I'm gonna head over': the footage pushes in with a slight tilt and pans right with him, then settles (Jack's note)."""
    i_c = w("head over to claude")
    i_p = w("paste this special skill")
    i_s = w("smart delegation", t(i_p)) if has("use smart delegation") else None
    end_w = (i_s + 1) if i_s is not None else w("builder", t(i_p))
    a, b = t(i_c) - 0.2, te(end_w) + 0.7
    T, R = [a], [88.2]
    if has("open up a new chat"):
        T.append(t(w("open up a new chat"))); R.append(91.4)
    T.append(t(i_p) + 0.2); R.append(96.7)
    if i_s is not None:
        T.append(t(i_s) - 0.2); R.append(99.9)
    T.append(b); R.append(101.9 if i_s is not None else 99.6)
    screen("sc", a, b, [(REC, R[k], R[k + 1], T[k], T[k + 1]) for k in range(len(T) - 1)])
    zoom_to("sc", t(i_p) + 0.1, (1144, 640, 2456, 1020), 0.6, 2.3)
    if i_s is not None:
        ring("sc", (1556, 830, 1824, 880), t(i_s) + 0.1, b - 0.35, pad=12, sw_=7)
    # the head turn: on the A-roll itself (inside the camera), so it rides on top of the card's camera hold
    t0 = t(i_c - 3) - 0.05  # "So I'm gonna head over…"
    js.append(f"tl.fromTo('#aroll', {{scale:1, rotation:0, x:0, transformOrigin:'540px 760px'}}, {{scale:1.15, rotation:1.4, x:-40, duration:.85, ease:'power2.inOut', immediateRender:false}}, {t0:.3f});")
    js.append(f"tl.to('#aroll', {{scale:1.17, x:-48, duration:1.4, ease:'none'}}, {t0 + 0.85:.3f});")
    js.append(f"tl.to('#aroll', {{scale:1, rotation:0, x:0, duration:.8, ease:'power2.inOut'}}, {t0 + 2.25:.3f});")


def smart14():
    """'Now smart delegation is a custom skill I've used to basically complete tasks as efficient and as fast as possible.'"""
    if not has("smart delegation is a custom skill"):
        return
    i = w("smart delegation is a custom skill")
    i_e, i_f = w("as efficient"), w("as fast as possible")
    note("sd14", f'<div class="k">smart delegation</div><div class="b" style="font-size:46px;margin-top:6px">a custom skill</div>'
                 f'<div class="ln" id="sd14-a" style="opacity:0">{mark("sd14-t")}<span>efficient</span></div><div class="ln" id="sd14-b" style="opacity:0">{mark("sd14-u")}<span>fast</span></div>',
         320, 230, t(i + 4) - 0.2, cut_out("as fast as possible"))
    ft("#sd14-a", t(i_e + 1) - 0.15, {"opacity": 0, "x": -16}, {"opacity": 1, "x": 0}, 0.25)
    draw("sd14-t", t(i_e + 1) + 0.1)
    ft("#sd14-b", t(i_f + 1) - 0.15, {"opacity": 0, "x": -16}, {"opacity": 1, "x": 0}, 0.25)
    draw("sd14-u", t(i_f + 1) + 0.1)


def models14():
    """'all my tasks are always delegating to smaller models while higher models are always reviewing.' — an ink diagram."""
    if not has("smaller models"):
        return
    i_s, i_h, i_r = w("smaller models"), w("higher models"), w("always reviewing")
    small = "".join(f'<i class="m14s" id="md14-s{k}"></i>' for k in range(3))
    note("md14", f'<div class="k">how it works</div>'
                 f'<div class="mdl"><div class="mr" id="md14-h" style="opacity:0"><i class="m14b"></i><span>big model</span><em id="md14-rv" style="opacity:0">reviews {mark("md14-t")}</em></div>'
                 f'<div class="ar" id="md14-ar" style="opacity:0">↑</div>'
                 f'<div class="mr"><span class="m14g">{small}</span><span>small models</span><em id="md14-dw" style="opacity:0">do the tasks</em></div></div>',
         400, 250, t(w("all my tasks")) - 0.2, cut_out("always reviewing"))
    for k in range(3):
        pop(f"#md14-s{k}", t(i_s) - 0.1 + k * 0.08, 0.3, 10, 0.3)
    ft("#md14-dw", t(i_s + 1), {"opacity": 0}, {"opacity": 1}, 0.25)
    ft("#md14-ar", t(i_h) - 0.25, {"opacity": 0, "y": 10}, {"opacity": 1, "y": 0}, 0.25)
    ft("#md14-h", t(i_h) - 0.1, {"opacity": 0, "x": -16}, {"opacity": 1, "x": 0}, 0.3)
    ft("#md14-rv", t(i_r + 1) - 0.1, {"opacity": 0}, {"opacity": 1}, 0.2)
    draw("md14-t", t(i_r + 1) + 0.1)
    sfx.extend([("click_004", t(i_s), 0.08), ("click_004", t(i_h), 0.08)])


def easy14():
    """'As long as you know how to actually spot a potential prospect and actually type out a few words, you're completely fine.'"""
    if not has("potential prospect"):
        return
    at = [t(w("potential prospect")), t(w("type out a few words"))]
    if has("okay now when"):  # leave before the next card pushes the camera in
        out_ = min(cut_out("completely fine"), t(w("okay now when")) - 1.0)
    else:
        out_ = cut_out("completely fine")
    plist("ez14", "all you need", ["spot a prospect", "type a few words"], [at[0] - 0.4, at[1] - 0.3], out_, [a + 0.4 for a in at], w_=360)


def wait14():
    """'now when that's set up, we're just gonna wait until Claude comes back with us with the fully made site.' — he sends it."""
    if not has("okay now when"):
        return
    i = w("okay now when")
    a, b = t(i) - 0.1, te(w("fully made site") + 2) + 0.15
    screen("sw", a, b, [(REC, 104.6, 115.8, a, b)])
    zoom_to("sw", a + 0.3, (1144, 640, 2456, 1020), 0.5, 2.0)
    zoom_out("sw", a + 0.3 + (b - a) * 0.55)


# ---------------------------------------------------------------- the site Claude built (captured from its own files)
CAPAT = []  # (a, b, top): captions at a fixed band (unused since Day 14 round 3: captions go above his head)
PG_W, PG_H = 2560, 8700  # Claude's site, full page at 2x (edit/site/index-cap.html: hero word held still for the capture)
LOW_W = 940


def low_window(sid, a, b, w=LOW_W, h=540, fit=None):
    """Jack, Day 14 round 3: the site windows a little smaller and lower so his face shows above them, a gap under them,
    captions above his head. The footage pushes in from the bottom edge (up to 1.45x) so his chin clears the window.
    Returns (left, top, w, h)."""
    fs = [f for f in FACES if a - 0.4 <= f[0] <= b + 0.4]
    chins = sorted((f[2] + f[4]) * 1920 for f in fs) or [1300]
    chin = chins[int(len(chins) * 0.9) - 1 if len(chins) > 1 else 0]
    top = 1770 - h
    z = min(1.25, max(1.0, (1920 - (top - 24)) / max(1920 - chin, 1)))  # more than 1.25x crops the top of his head
    chin2 = 1920 - z * (1920 - chin)
    if chin2 + 24 > top:  # still not clear at the push limit: shrink the window instead of covering his mouth
        top = int(chin2 + 24)
        h2 = max(480, 1770 - top)
        if fit:
            w = int(h2 * fit)
        h = h2
    left = (1080 - w) // 2
    CAM_WINS.append((a - 0.15, b, z, 1920))
    print(f"  low window {sid} {a:.1f}-{b:.1f}s: chin {chin:.0f} -> push {z:.2f}x, window {w}x{h} at y {top}")
    return left, top, w, h


def site_window(sid, a, b, img=None, pw=PG_W, ph=PG_H):
    """A site in a browser window under his face (a page that scrolls; the caller moves it)."""
    img = img or f"{SITE}/full.jpg"
    left, top, w, h = low_window(sid, a, b)
    k = w / pw
    VL.append(f'<div class="scr bigw" id="{sid}" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px"><div class="scz" id="{sid}-z" style="width:{w}px;height:{h}px">'
              f'<div class="pg14" id="{sid}-p" style="width:{w}px;height:{ph * k:.0f}px"><img src="{img}" style="width:{w}px;display:block"/>'
              f'<svg class="rgs" id="{sid}-rg" viewBox="0 0 {pw} {ph}" style="height:{ph * k:.0f}px"><!--RG:{sid}--></svg></div></div></div>')
    ft(f"#{sid}", a, {"opacity": 0, "y": 120, "scale": 0.92}, {"opacity": 1, "y": 0, "scale": 1}, 0.5, "expo.out")
    to(f"#{sid}", b - 0.32, {"opacity": 0, "y": 80, "scale": 0.95}, 0.32, "power2.in")
    sfx.append(("arrow-whoosh", a - 0.05, 0.12))
    CARDS[sid] = (top, h, pw, ph, w, left)
    return h / k  # page px visible


def scroll_to(sid, at, y_px, d=0.7):
    top, h, pw, ph, w, left = CARDS[sid]
    y_px = max(0, min(ph - h * pw / w, y_px))
    to(f"#{sid}-p", at, {"y": round(-y_px * w / pw, 1)}, d, "power3.inOut")


def site14():
    """'And there we go, the site is fully made … (as you can see, it's perfect … nothing extreme …) It tells them where they are,
    what they do, and how to book.' — Claude's real site: hero, services, then the map, the menu and the Book button, ringed."""
    i_g = w("and there we go")
    i_wh, i_wt, i_bk = w("where they are"), w("what they do"), w("how to book")
    sfx.append(("confirmation_002", t(i_g + 3), 0.16))  # the reveal
    b1 = te(w("fully made", t(i_g)) + 1) + 0.35
    a2 = (t(w("as you can see")) - 0.1) if has("as you can see") else b1
    b2 = cut_out("simple as that") + 0.1 if has("simple as that") else te(i_bk + 2) + 0.55
    if a2 - b1 < 1.0:  # V2 / V3: no line between them, one window
        view = site_window("ss", t(i_g) - 0.05, b2)
    else:
        site_window("s1", t(i_g) - 0.05, b1)
        to("#s1-p", t(i_g) + 0.5, {"y": -40}, b1 - t(i_g) - 0.8, "sine.inOut")
        view = site_window("ss", a2, b2)
    def centre(y0, y1):  # scroll so a page band sits in the middle of the window
        return (y0 + y1) / 2 - view / 2
    if has("nothing extreme"):
        scroll_to("ss", t(w("nothing extreme")) - 0.15, centre(2500, 4200), 0.9)
    scroll_to("ss", t(i_wh) - 0.55, centre(6300, 7480), 0.5)
    ring("ss", (1200, 6360, 2384, 7424), t(i_wh) - 0.05, t(i_wt) - 0.3, dur=0.42)
    scroll_to("ss", t(i_wt) - 0.3, centre(3040, 4080), 0.45)
    ring("ss", (160, 3040, 2400, 4080), t(i_wt) + 0.15, t(i_bk) - 0.3, dur=0.42)
    scroll_to("ss", t(i_bk) - 0.3, centre(7800, 8200), 0.45)
    ring("ss", (1104, 8064, 1464, 8160), t(i_bk) + 0.15, b2 - 0.35, pad=12)


# ---------------------------------------------------------------- the CRM: his new landing page, then the real dashboard
CRM_SLIDES = {"hero": ("assets/img/crm/landing-hero.png", 1920, 1080), "overview": ("assets/img/crm/dash-overview.jpg", 1493, 812),
              "campaigns": ("assets/img/crm/dash-campaigns.jpg", 1493, 812), "research": ("assets/img/crm/dash-research.jpg", 1493, 812),
              "leads": ("assets/img/crm/dash-leads.jpg", 1493, 812), "calls": ("assets/img/crm/dash-calls.jpg", 1493, 812)}


def crmsite14():
    """'use my CRM at admin.novasagency.com. (You're gonna sign up there, you're gonna connect this into the CRM,) and that's gonna
    automate your outreach completely for free. And it means that you can make some real money.' — Jack, round 3: the new landing
    page, then his real Novas HQ dashboard (Overview, Leads, Campaigns, Calls); one ring for sign-up, one for revenue."""
    i_c = w("my crm at")
    i_a, i_f, i_m = w("automate your outreach"), w("completely for free"), w("real money")
    a, b = t(i_c) - 0.15, te(i_m + 1) + 0.45
    seq = [("hero", a)]
    if has("connect this into"):
        seq.append(("overview", t(w("connect this into")) - 0.15))
    else:
        seq.append(("leads", t(i_a) - 0.2))
    seq += [("campaigns", t(i_a + 2) - 0.05), ("calls", t(i_f) + 0.1), ("overview", t(i_m) - 0.5)]
    W = LOW_W
    left, top, Wd, H = low_window("sr", a, b, W, round(W * 1080 / 1920), fit=1920 / 1080)
    imgs = "".join(f'<div class="sl14" id="sr-s{k}"><img src="{CRM_SLIDES[n][0]}"/><svg class="rgs" id="sr{k}-rg" viewBox="0 0 {CRM_SLIDES[n][1]} {CRM_SLIDES[n][2]}" style="height:{Wd * CRM_SLIDES[n][2] / CRM_SLIDES[n][1]:.0f}px"><!--RG:sr{k}--></svg></div>'
                   for k, (n, _) in enumerate(seq))
    VL.append(f'<div class="scr bigw" id="sr" style="left:{left}px;top:{top}px;width:{Wd}px;height:{H}px"><div class="scz" id="sr-z" style="width:{Wd}px;height:{H}px">{imgs}</div></div>')
    ft("#sr", a, {"opacity": 0, "y": 120, "scale": 0.92}, {"opacity": 1, "y": 0, "scale": 1}, 0.5, "expo.out")
    to("#sr", b - 0.32, {"opacity": 0, "y": 80, "scale": 0.95}, 0.32, "power2.in")
    sfx.append(("arrow-whoosh", a - 0.05, 0.12))
    for k, (n, at) in enumerate(seq):
        img, pw, ph = CRM_SLIDES[n]
        h_img = Wd * ph / pw  # slides keep their own aspect, top-aligned on the window's white
        CARDS[f"sr{k}"] = (top, h_img, pw, ph, Wd, left)
        if k == 0:
            st("#sr-s0", a, {"opacity": 1})
        else:
            ft(f"#sr-s{k}", at, {"opacity": 0, "x": 60}, {"opacity": 1, "x": 0}, 0.4, "power3.out", False)
            to(f"#sr-s{k - 1}", at + 0.05, {"opacity": 0, "x": -40}, 0.35, "power2.in")
            sfx.append(("click_002", at, 0.12))
    if has("sign up there"):
        i_s = w("sign up there")
        ring("sr0", (817, 580, 984, 632), t(i_s) + 0.1, seq[1][1] - 0.05, pad=10)
    ring(f"sr{len(seq) - 1}", (253, 162, 853, 272), t(i_m) + 0.15, b - 0.35, pad=8)


# ---------------------------------------------------------------- ending
def pg_next(s, e):
    """'I am running out of ideas, so leave a comment of what you want to see next.' — what next? / comment your idea."""
    scene("cta", s, e, f"""
  <div class="stack" style="left:0;right:0;top:520px">
    <span id="cta-w" class="sm" style="font-size:42px">I'm running out of ideas</span>
    <span id="cta-p" class="xb" style="font-size:124px;line-height:1;margin-top:8px">What next?</span>
    <span id="cta-s" class="sm" style="font-size:36px;margin-top:18px">tell me what you want to see</span>
  </div>
  <div id="cta-c" class="cm13" style="top:1060px;left:220px;right:220px"><div class="av">{ic("user", 44, "#fbf9f5")}</div><div class="tx"><div class="ck">comment</div><div class="cbb">{typed_words("cta-tw", "your idea")}<i class="caret"></i></div></div></div>""")
    rev("#cta-w", s + 0.05, 14)
    slam("#cta-p", s + 0.2)
    rev("#cta-s", s + 0.55, 16)
    ft("#cta-c", s + 0.8, {"opacity": 0, "y": 50, "scale": 0.9}, {"opacity": 1, "y": 0, "scale": 1}, 0.4, "back.out(1.7)")
    type_on("cta-tw", 2, s + 1.15, s + 1.45)
    ft("#cta-c", s + 1.75, {"scale": 1}, {"scale": 1.06, "yoyo": True, "repeat": 1}, 0.14, "power2.out", False)
    sfx.extend([("dry-pop-alert", s + 0.2, 0.24), ("drop_002", s + 0.8, 0.14), ("pluck_001", s + 1.75, 0.22)])


def pg_end14(s):
    """End card: see you on Day 15 tomorrow; fourteen blocks lit, zoom into today's."""
    ZX, ZY = 90 + 13 * (SEG_W + 6) + SEG_W / 2, 1340 - 40 * 1.9 / 2
    scene("ed", s, DURATION, f"""
  <div id="ed-zoom" style="position:absolute;inset:0;transform-origin:{ZX:.1f}px {ZY:.1f}px">
    <div class="stack" style="left:0;right:0;top:560px">
      <span id="ed-sy" class="sm" style="font-size:56px">see you on</span>
      <div class="row" style="align-items:flex-end;justify-content:center;margin-top:6px">
        <span id="ed-day" class="xb" style="font-size:230px;line-height:1">Day</span>
        <span id="ed-n" class="xb" style="font-size:230px;line-height:1;margin-left:40px">15</span>
      </div>
      <span id="ed-tm" class="sm" style="font-size:52px;margin-top:20px">tomorrow</span>
    </div>
    <span id="ed-lbl" class="note" style="position:absolute;left:{90 + 13 * (SEG_W + 6) - 40:.0f}px;top:1186px">day 14 / 30</span>
    <div id="ed-bar" class="bar big" style="top:1300px">{BLOCKS.replace('{p}', 'ed')}</div>
  </div>""", whoosh=False)
    rev("#ed-sy", s + 0.05, 14)
    rev("#ed-day", s + 0.2, 30)
    slam("#ed-n", s + 0.4)
    rev("#ed-tm", s + 0.7, 16)
    ft("#ed-bar .seg", s + 0.1, {"scaleY": 0, "opacity": 0}, {"scaleY": 1, "opacity": 1, "stagger": 0.01}, 0.25, "power2.out")
    lit = s + 0.9
    ft(", ".join(f"#ed-s{k}" for k in range(13)), lit - 0.3, {"backgroundColor": "rgba(23,18,14,.14)"}, {"backgroundColor": INK, "stagger": 0.035}, 0.18)
    ft("#ed-s13", lit, {"backgroundColor": "rgba(23,18,14,.14)", "scaleY": 1}, {"backgroundColor": INK, "scaleY": 1.9}, 0.5, "back.out(2.2)")
    ft("#ed-lbl", lit + 0.15, {"opacity": 0, "y": 12}, {"opacity": 1, "y": 0}, 0.35, "power2.out")
    zoom_at = DURATION - 1.4
    to("#ed-lbl", zoom_at, {"opacity": 0}, 0.3)
    ft("#ed-zoom", zoom_at, {"scale": 1, "x": 0, "y": 0}, {"scale": 60, "x": round(540 - ZX, 1), "y": round(960 - ZY, 1)}, 1.3, "power3.inOut")
    sfx.extend([("dry-pop-alert", s + 0.4, 0.24), ("pluck_001", lit, 0.3), ("riser", zoom_at + 0.25, 0.35), ("boom", DURATION - 0.12, 0.3)])


def call_edges():
    """Punch-ins through long takes: sentence starts more than ~3 s apart inside one segment."""
    out = []
    for s_ in SEGS:
        last = s_["start"]
        for k in range(1, len(TOK)):
            tt = t(k)
            if not (s_["start"] + 1.0 < tt < s_["end"] - 1.0):
                continue
            if TOK[k - 1]["text"].endswith((".", "?", "!", ",")) and tt - last > 3.0:
                out.append(round(tt - 0.12, 3))
                last = tt
    return out
