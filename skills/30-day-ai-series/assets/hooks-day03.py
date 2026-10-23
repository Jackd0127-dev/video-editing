# Five experimental hooks for Day 3 (0 s → "Hello"). Executed inside build.py when HOOK=1..5.
# Same voice, same words; only what's on screen changes.
#   A  "five viral AI creator accounts"   (A0 → A1)
#   B  "and today I'm gonna show you"     (his face)
#   C  "exactly how you can too"           (C0 → C1), then his face on "Hello"
A0, A1 = t(2) - 0.06, cover_cut(t(7) - 0.06)
C0, C1 = t(13) - 0.08, t(19) - 0.12
POSTS = ["hook4", "hook3", "hook0", "hook1", "hook2"]  # VOLT, Lucas, Roos walkout, Roos fighters, Roos knight
SCRIM_WIN = []
TAGS = lambda pre, top: (f'<span id="{pre}-o" class="mtag" style="left:50%;top:{top}px;transform:translateX(-50%);font-size:40px">original</span>'
                         f'<span id="{pre}-a" class="mtag" style="left:50%;top:{top}px;transform:translateX(-50%);font-size:40px;background:#fbf9f5;color:{INK};opacity:0">AI</span>')


def tag_swap(pre, at):
    js.append(f"tl.to('#{pre}-o', {{opacity:0, scale:.6, duration:.15, immediateRender:false}}, {at:.3f});")
    js.append(f"tl.fromTo('#{pre}-a', {{opacity:0, scale:.6}}, {{opacity:1, scale:1, duration:.3, ease:'back.out(2.4)', immediateRender:false}}, {at + 0.1:.3f});")


def scan_swap(pre, box_h, at):
    """Original → AI: a bright line scans down and leaves the AI version behind it."""
    js.append(f"tl.fromTo('#{pre}-ai', {{clipPath:'inset(0% 0% 100% 0%)'}}, {{clipPath:'inset(0% 0% 0% 0%)', duration:.6, ease:'power2.inOut'}}, {at:.3f});")
    js.append(f"tl.fromTo('#{pre}-scan', {{y:0, opacity:1}}, {{y:{box_h - 6}, opacity:1, duration:.6, ease:'power2.inOut'}}, {at:.3f}); tl.to('#{pre}-scan', {{opacity:0, duration:.1, immediateRender:false}}, {at + 0.6:.3f});")
    sfx.append(("arrow-whoosh", at, 0.28))
    tag_swap(pre, at + 0.2)


def swap_box(pre, left, top, w, h, start, end, radius=48, extra=""):
    return (f'<div id="{pre}" style="position:absolute;left:{left}px;top:{top}px;width:{w}px;height:{h}px;{extra}">'
            f'<div style="position:absolute;inset:0;border-radius:{radius}px;overflow:hidden;box-shadow:0 0 0 10px #17120e, 0 50px 90px rgba(40,26,14,.32)">'
            f'{vid(pre + "-v0", "assets/video/br/w2-src.mp4", start, end - start + 0.5)}'
            f'<div id="{pre}-ai" style="position:absolute;inset:0;clip-path:inset(0% 0% 100% 0%)">{vid(pre + "-v1", "assets/video/br/w2-ai.mp4", start, end - start + 0.5)}</div>'
            f'<i id="{pre}-scan" style="position:absolute;left:0;right:0;top:0;height:6px;background:#fbf9f5;box-shadow:0 0 24px #fff;opacity:0"></i></div>'
            f'{TAGS(pre, -36)}</div>')


if HOOK == "1":
    # ------------------------------------------------ 1 · THE FEED: a phone swipes through his five accounts, one per word
    PH = (290, 430, 500, 889)
    s = scene("h1a", A0, A1, f"""
  <div class="stack" style="left:0;right:0;top:220px"><span class="sm" style="font-size:60px">{words_in('h1w', ['five', 'viral', 'AI', 'creator', 'accounts'], [2, 3, 4, 5, 6])}</span></div>
  <div class="phn" style="left:{PH[0]}px;top:{PH[1]}px;width:{PH[2]}px;height:{PH[3]}px"></div>
  <span id="h1-n" class="xb" style="position:absolute;left:820px;top:1180px;font-size:150px;line-height:1">1</span>
  <span class="note dim" style="position:absolute;left:830px;top:1340px">/ 5</span>""")
    strip = "".join(f'<div style="position:absolute;left:0;top:{k * PH[3]}px;width:{PH[2]}px;height:{PH[3]}px">{vid(f"h1-v{k}", f"assets/video/br/{POSTS[k]}.mp4", s, A1 - s + 0.3)}</div>' for k in range(5))
    overlay(f'<div id="h1-ph" style="position:absolute;left:{PH[0]}px;top:{PH[1]}px;width:{PH[2]}px;height:{PH[3]}px;border-radius:48px;overflow:hidden"><div id="h1-strip" style="position:absolute;inset:0">{strip}</div></div>', s, A1, sel="#h1-ph")
    js.append(f"tl.fromTo('#h1a .phn, #h1-ph', {{y:140, scale:.9}}, {{y:0, scale:1, duration:.45, ease:'power3.out'}}, {s:.3f});")
    for k, wi in enumerate([3, 4, 5, 6]):
        at = t(wi) - 0.12
        js.append(f"tl.to('#h1-strip', {{y:{-(k + 1) * PH[3]}, duration:.28, ease:'power3.inOut', immediateRender:false}}, {at:.3f});")
        js.append(f"tl.set('#h1-n', {{textContent:'{k + 2}'}}, {at + 0.14:.3f}); tl.fromTo('#h1-n', {{scale:1.4}}, {{scale:1, duration:.25, ease:'back.out(2)', immediateRender:false}}, {at + 0.14:.3f});")
        sfx.append(("fast-whoosh", at - 0.05, 0.2))
    slam("#h1-n", s + 0.1)
    # exactly how you can too → the same phone, original dancer, scans into the AI version
    s = scene("h1c", C0, C1 + 0.3, f"""
  <div class="stack" style="left:0;right:0;top:230px"><div class="row" style="align-items:baseline;gap:18px"><span class="sm" style="font-size:60px">{words_in('h1x', ['exactly', 'how', 'you'], [13, 14, 15])}</span><span id="h1-can" class="xb" style="font-size:112px">can too</span></div></div>
  <div class="phn" style="left:{PH[0]}px;top:{PH[1]}px;width:{PH[2]}px;height:{PH[3]}px"></div>""")
    VL.append(swap_box("h1s", PH[0], PH[1], PH[2], PH[3], s, C1 + 0.3, extra="opacity:0"))
    js.append(f"tl.fromTo('#h1s', {{opacity:0}}, {{opacity:1, duration:.25}}, {s + 0.05:.3f}); tl.to('#h1s', {{opacity:0, duration:.42, ease:'sine.inOut', immediateRender:false}}, {C1 + 0.3 - 0.42:.3f});")
    js.append(f"tl.set('#h1-can', {{opacity:0}}, {s:.3f});")
    slam("#h1-can", t(16) - 0.06, 1.3)
    scan_swap("h1s", PH[3], t(16) - 0.05)

elif HOOK == "2":
    # ------------------------------------------------ 2 · COLD OPEN ON THE RESULT: original | AI slider from frame one, then his five accounts
    X0, X1 = 0.0, A1
    VL.append(f'''<div id="h2" style="position:absolute;inset:0">
  {vid("h2-o", "assets/video/br/w2-src.mp4", X0, X1 - X0 + 0.4)}
  <div id="h2-ai" style="position:absolute;inset:0;clip-path:inset(0 0 0 50%)">{vid("h2-a", "assets/video/br/w2-ai.mp4", X0, X1 - X0 + 0.4)}</div>
  <i id="h2-line" style="position:absolute;top:0;bottom:0;left:537px;width:6px;background:#fbf9f5;box-shadow:0 0 18px rgba(0,0,0,.35)"></i>
  <span class="mtag" style="left:60px;top:1470px;font-size:40px">original</span>
  <span class="mtag" style="left:auto;right:60px;top:1470px;font-size:40px;background:#fbf9f5;color:{INK}">AI</span>
</div>''')
    js.append(f"tl.fromTo('#h2', {{scale:1.35}}, {{scale:1, duration:.5, ease:'expo.out'}}, 0); tl.to('#h2', {{opacity:0, duration:.35, ease:'sine.inOut', immediateRender:false}}, {X1 - 0.35:.3f});")
    D = X1 - X0
    for sel, prop, fmt in (("#h2-ai", "clipPath", "inset(0 0 0 {}%)"), ("#h2-line", "x", "{}")):
        pts = [(0.4, 50), (0.4 + D * 0.3, 20), (0.4 + D * 0.65, 80), (D - 0.1, 50)]
        for (ta, va), (tb, vb) in zip(pts, pts[1:]):
            fv = (lambda v: f"'{fmt.format(v)}'") if prop == "clipPath" else (lambda v: f"{(v - 50) * 10.8:.0f}")
            js.append(f"tl.fromTo('{sel}', {{{prop}:{fv(va)}}}, {{{prop}:{fv(vb)}, duration:{tb - ta:.3f}, ease:'sine.inOut', immediateRender:false}}, {X0 + ta:.3f});")
    SCRIM_WIN = [(X0, X1)]
    sfx += [("arrow-whoosh", 0.0, 0.32), ("fast-whoosh", 0.4 + D * 0.3, 0.2)]
    # exactly how you can too → his five accounts fan out, all playing
    FAN = [(215, -11, 520), (378, -5.5, 485), (540, 0, 465), (702, 5.5, 485), (865, 11, 520)]
    s = scene("h2c", C0, C1 + 0.3, f"""
  <div class="stack" style="left:0;right:0;top:260px"><div class="row" style="align-items:baseline;gap:18px"><span class="sm" style="font-size:60px">{words_in('h2x', ['exactly', 'how', 'you'], [13, 14, 15])}</span><span id="h2-can" class="xb" style="font-size:112px">can too</span></div></div>""")
    VL.append("".join(f'<div class="fan" id="h2-c{k}" style="left:{cx - 130}px;top:{y}px;width:260px;height:462px;z-index:{[1, 2, 3, 2, 1][k]};opacity:0">{vid(f"h2-v{k}", f"assets/video/br/{POSTS[[3, 1, 0, 2, 4][k]]}.mp4", s, C1 + 0.3 - s)}</div>' for k, (cx, r, y) in enumerate(FAN)))
    for j, k in enumerate([2, 1, 3, 0, 4]):
        js.append(f"tl.fromTo('#h2-c{k}', {{opacity:0, y:320, rotation:0, scale:.6}}, {{opacity:1, y:0, rotation:{FAN[k][1]}, scale:1, duration:.5, ease:'back.out(1.4)'}}, {s + 0.05 + j * 0.08:.3f});")
    js.append(f"tl.to('[id^=h2-c]', {{opacity:0, duration:.42, ease:'sine.inOut', immediateRender:false}}, {C1 + 0.3 - 0.42:.3f});")
    js.append(f"tl.set('#h2-can', {{opacity:0}}, {s:.3f});")
    slam("#h2-can", t(16) - 0.06, 1.3)
    sfx += [("hard-pop-click", s + 0.06, 0.3)]

elif HOOK == "3":
    # ------------------------------------------------ 3 · ZOOM OUT: one AI creator full screen, the camera pulls back to reveal all of them
    TW, TH, TOP = 360, 640, 320
    GRID = ["hook3-hd", "hook4-hd", "hook0-hd", "hook1-hd", "hook2-hd", "ai-track"]
    tiles = "".join(f'<div style="position:absolute;left:{(k % 3) * TW}px;top:{TOP + (k // 3) * TH}px;width:{TW}px;height:{TH}px;overflow:hidden;box-shadow:inset 0 0 0 3px #17120e">{vid(f"h3-v{k}", f"assets/video/br/{g}.mp4", A0, A1 - A0 + 0.3)}</div>' for k, g in enumerate(GRID))
    VL.append(f'<div id="h3" style="position:absolute;inset:0;background:#17120e;opacity:0;transform-origin:{TW * 1.5:.0f}px {TOP + TH / 2:.0f}px">{tiles}'
              f'<span id="h3-tag" class="mtag" style="left:50%;top:1640px;transform:translateX(-50%);font-size:46px;background:#fbf9f5;color:{INK}">5 AI creators · 0 humans</span></div>')
    # start zoomed into the centre tile (3x fills the frame exactly), then pull back
    js.append(f"tl.fromTo('#h3', {{opacity:0, scale:3.6, y:{960 - TOP - TH / 2:.0f}}}, {{opacity:1, scale:3, y:{960 - TOP - TH / 2:.0f}, duration:.3, ease:'expo.out'}}, {A0:.3f});")
    js.append(f"tl.to('#h3', {{scale:1, y:0, duration:1.1, ease:'expo.inOut', immediateRender:false}}, {t(3) - 0.05:.3f});")
    js.append(f"tl.fromTo('#h3-tag', {{opacity:0, y:30}}, {{opacity:1, y:0, duration:.35, ease:'back.out(2)'}}, {t(5) - 0.05:.3f});")
    js.append(f"tl.to('#h3', {{opacity:0, duration:.35, ease:'sine.inOut', immediateRender:false}}, {A1 - 0.35:.3f});")
    SCRIM_WIN = [(A0, A1), (C0, C1)]
    sfx += [("hard-pop-click", A0, 0.3), ("riser", t(3) - 0.1, 0.22)]
    # exactly how you can too → the original dancer full screen, scanned into the AI version
    VL.append(f'''<div id="h3c" style="position:absolute;inset:0;opacity:0">
  {vid("h3c-v0", "assets/video/br/w2-src.mp4", C0, C1 - C0 + 0.5)}
  <div id="h3c-ai" style="position:absolute;inset:0;clip-path:inset(0% 0% 100% 0%)">{vid("h3c-v1", "assets/video/br/w2-ai.mp4", C0, C1 - C0 + 0.5)}</div>
  <i id="h3c-scan" style="position:absolute;left:0;right:0;top:0;height:8px;background:#fbf9f5;box-shadow:0 0 30px #fff;opacity:0"></i>
  {TAGS("h3c", 1500)}
</div>''')
    js.append(f"tl.fromTo('#h3c', {{opacity:0, scale:1.2}}, {{opacity:1, scale:1, duration:.3, ease:'expo.out'}}, {C0:.3f}); tl.to('#h3c', {{opacity:0, duration:.35, ease:'sine.inOut', immediateRender:false}}, {C1 - 0.05:.3f});")
    scan_swap("h3c", 1920, t(16) - 0.05)

elif HOOK == "4":
    # ------------------------------------------------ 4 · STAY ON HIS FACE: five playing posts pop up around him, then become the before/after
    CARD = (220, 391)
    SPOTS = [(28, 620, -7), (832, 600, 6), (40, 1090, 5), (820, 1080, -6), (430, 1470, 2)]
    cards = "".join(f'<div class="fan" id="h4-c{k}" style="left:{x}px;top:{y}px;width:{CARD[0]}px;height:{CARD[1]}px;opacity:0;border-width:6px">{vid(f"h4-v{k}", f"assets/video/br/{POSTS[k]}.mp4", A0, C0 - A0 + 0.2)}</div>' for k, (x, y, r) in enumerate(SPOTS))
    VL.append(f'<div id="h4">{cards}</div>')
    for k, wi in enumerate([2, 3, 4, 5, 6]):
        x, y, r = SPOTS[k]
        js.append(f"tl.fromTo('#h4-c{k}', {{opacity:0, scale:.3, rotation:{r * 3}}}, {{opacity:1, scale:1, rotation:{r}, duration:.4, ease:'back.out(2.2)'}}, {t(wi) - 0.08:.3f});")
        js.append(f"tl.to('#h4-c{k}', {{y:{-14 if k % 2 else 14}, duration:{C0 - 0.15 - t(wi) - 0.35:.3f}, ease:'sine.inOut', immediateRender:false}}, {t(wi) + 0.35:.3f});")
        sfx.append(("pluck_001" if k % 2 else "hard-pop-click", t(wi) - 0.05, 0.18))
    # exactly → the cards fly off and one before/after card rises in front of his chest
    for k, (x, y, r) in enumerate(SPOTS):
        js.append(f"tl.to('#h4-c{k}', {{x:{-500 if x < 400 else 500 if x > 600 else 0}, y:{(-14 if k % 2 else 14) + (600 if x == 430 else 0)}, rotation:{r * 4}, opacity:0, duration:.4, ease:'power2.in', immediateRender:false}}, {C0 - 0.1 + k * 0.03:.3f});")
    VL.append(swap_box("h4s", 330, 1060, 420, 746, C0, C1 + 0.3, radius=40, extra="opacity:0"))
    js.append(f"tl.fromTo('#h4s', {{opacity:0, y:500}}, {{opacity:1, y:0, duration:.5, ease:'power3.out'}}, {C0 + 0.05:.3f}); tl.to('#h4s', {{y:900, opacity:0, duration:.4, ease:'power2.in', immediateRender:false}}, {C1 - 0.05:.3f});")
    scan_swap("h4s", 746, t(16) - 0.05)
    sfx += [("fast-whoosh", C0 - 0.12, 0.26)]

elif HOOK == "5":
    # ------------------------------------------------ 5 · THE DECK: a stack of his accounts swiped through one per word, then the top card flips to its AI twin
    CW, CH, CL, CT = 520, 924, 280, 450
    s = scene("h5a", A0, A1, f"""
  <div class="stack" style="left:0;right:0;top:220px"><span class="sm" style="font-size:60px">{words_in('h5w', ['five', 'viral', 'AI', 'creator', 'accounts'], [2, 3, 4, 5, 6])}</span></div>
  <span id="h5-n" class="xb" style="position:absolute;left:70px;top:1180px;font-size:150px;line-height:1">1</span>
  <span class="note dim" style="position:absolute;left:80px;top:1340px">/ 5</span>""")
    deck = "".join(f'<div class="fan" id="h5-c{k}" style="left:{CL + (4 - k) * 10}px;top:{CT + (4 - k) * 12}px;width:{CW}px;height:{CH}px;z-index:{10 - k}">{vid(f"h5-v{k}", f"assets/video/br/{POSTS[[1, 2, 3, 4, 0][k]]}.mp4", s, A1 - s + 0.3)}</div>' for k in range(5))
    overlay(f'<div id="h5d" style="position:absolute;inset:0">{deck}</div>', s, A1, sel="#h5d")
    js.append(f"tl.fromTo('[id^=h5-c]', {{y:200, opacity:0}}, {{y:0, opacity:1, duration:.4, stagger:.04, ease:'power3.out'}}, {s:.3f});")
    for k, wi in enumerate([3, 4, 5, 6]):
        at = t(wi) - 0.12
        d = -1 if k % 2 == 0 else 1
        js.append(f"tl.to('#h5-c{k}', {{x:{d * 900}, y:-120, rotation:{d * 24}, duration:.35, ease:'power2.in', immediateRender:false}}, {at:.3f});")
        js.append(f"tl.set('#h5-n', {{textContent:'{k + 2}'}}, {at + 0.15:.3f}); tl.fromTo('#h5-n', {{scale:1.4}}, {{scale:1, duration:.25, ease:'back.out(2)', immediateRender:false}}, {at + 0.15:.3f});")
        sfx.append(("fast-whoosh", at - 0.03, 0.2))
    slam("#h5-n", s + 0.1)
    # exactly how you can too → one card: the original dancer flips over into his AI version
    s = scene("h5c", C0, C1 + 0.3, f"""
  <div class="stack" style="left:0;right:0;top:230px"><div class="row" style="align-items:baseline;gap:18px"><span class="sm" style="font-size:60px">{words_in('h5x', ['exactly', 'how', 'you'], [13, 14, 15])}</span><span id="h5-can" class="xb" style="font-size:112px">can too</span></div></div>""")
    VL.append(f'''<div id="h5f" style="position:absolute;left:{CL}px;top:{CT}px;width:{CW}px;height:{CH}px;opacity:0;perspective:1600px">
  <div id="h5-front" class="fan" style="position:absolute;inset:0;width:auto;height:auto;backface-visibility:hidden">{vid("h5f-v0", "assets/video/br/w2-src.mp4", s, C1 + 0.3 - s)}</div>
  <div id="h5-back" class="fan" style="position:absolute;inset:0;width:auto;height:auto;backface-visibility:hidden;opacity:0">{vid("h5f-v1", "assets/video/br/w2-ai.mp4", s, C1 + 0.3 - s)}</div>
  {TAGS("h5f", -36)}
</div>''')
    js.append(f"tl.fromTo('#h5f', {{opacity:0, y:120}}, {{opacity:1, y:0, duration:.4, ease:'power3.out'}}, {s + 0.05:.3f}); tl.to('#h5f', {{opacity:0, duration:.42, ease:'sine.inOut', immediateRender:false}}, {C1 + 0.3 - 0.42:.3f});")
    f0 = t(16) - 0.1
    js.append(f"tl.to('#h5-front', {{rotationY:90, duration:.22, ease:'power2.in', immediateRender:false}}, {f0:.3f});")
    js.append(f"tl.fromTo('#h5-back', {{rotationY:-90, opacity:0}}, {{rotationY:0, opacity:1, duration:.3, ease:'back.out(1.6)'}}, {f0 + 0.22:.3f});")
    tag_swap("h5f", f0 + 0.2)
    js.append(f"tl.set('#h5-can', {{opacity:0}}, {s:.3f});")
    slam("#h5-can", t(16) - 0.06, 1.3)
    sfx += [("arrow-whoosh", f0, 0.28)]
