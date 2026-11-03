"""Reference generator for the Arena style: "100 Claude Agents Arena" (round 2), the approved edit.

His footage untouched (SDR via Apple's avconvert); bone-paper pages that fade in smoothly; ink type, one coral accent,
Archivo Condensed / Archivo / IBM Plex Mono. The hero is a crowd of animated pixel agents (edit/sprites.py, drawn from
Jack's reference art): each agent is stacked layers (body, eyes, prop, fx, weapon) that bob, blink and do their own move.
Claude UI is only the real Claude desktop prompt box (b-roll library capture), typed over like a real caret.
Two versions (tools/TRIAL-REELS.md): TRIAL=1 main (face-first hook, full), TRIAL=2 (cold open on 1 agent -> 100, tight).
Run from the project root:  TRIAL=1 python3 -I edit/build.py  -> ../<project>-trials/out/trial-1.html
Sound: no effects on fights, hits or clashes; the assembly step drops any effect that repeats within 3 s.
"""
import html
import json
import math
import os
import re

N = int(os.environ.get("TRIAL", "1"))
D = f"edit/trials/{N}"
TOK = json.load(open(f"{D}/tokens.json"))
SEGS = json.load(open(f"{D}/words.json"))["segments"]
AROLL_END = SEGS[-1]["end"]
TAIL = 0.6
DURATION = round(AROLL_END + TAIL, 3)
CUTS = [g["start"] for g in SEGS[1:]]
INK, BONE, CORAL, WHITE = "#161513", "#efebe3", "#d97757", "#ffffff"
PX = "assets/img/px"
KINDEYE = json.load(open(f"{PX}/kinds.json"))
CROWD = ["coder", "coffee", "music", "chef", "wizard", "reader", "sleuth", "rocket", "plain"]
EYEV = ["open", "happy", "closed", "wink", "wide", "open"]

EMPH = ({"100", "hundred", "thousand", "million", "claude", "arena", "battle", "battlefield", "judge", "winner", "leaderboard",
         "bracket", "tournament", "free", "personality", "death", "bad"} if N == 1 else
        {"instead", "one", "best", "special", "turns", "type", "slash", "initial", "own", "attacking", "knock", "loser", "won",
         "lost", "follow", "arena", "learn"})


# ---------------------------------------------------------------- words
def norm(s):
    return re.sub(r"[^a-z0-9']", "", s.lower().replace("’", "'"))


NT = [norm(x["text"]) for x in TOK]


def w(phrase, after=0.0):
    ws = [norm(p) for p in phrase.split()]
    for i in range(len(NT) - len(ws) + 1):
        if TOK[i]["start"] >= after - 1e-6 and NT[i:i + len(ws)] == ws:
            return i
    raise KeyError(f"trial {N}: '{phrase}' not in the cut")


def t(i):
    return TOK[i]["start"] if i < len(TOK) else AROLL_END


def T(phrase, after=0.0):
    return t(w(phrase, after))


def seg_end_at(x):
    return next((s["end"] for s in SEGS if s["start"] - 0.01 <= x < s["end"]), AROLL_END)


def te(i):
    return min(TOK[i].get("end", t(i) + 0.3), t(i + 1), seg_end_at(t(i)))


def TE(phrase, after=0.0):
    return te(w(phrase, after) + len(phrase.split()) - 1)


def esc(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------- timeline helpers
scenes, overlays, js, sfx = [], [], [], []


def scene(sid, start, end, body, opened=False):
    for c in CUTS:  # a page that starts just after a cut starts on it (never flash a new take)
        if c <= start < c + 0.4:
            start = c - 0.02
    start = max(0.0, math.floor(start * 30 + 1e-6) / 30 - 0.002)
    scenes.append([sid, start, end, body])
    if not opened:
        js.append(f"enter('#{sid}', {start:.3f});")
        sfx.append(("fast-whoosh", max(0, start - 0.15), 0.16))
    return start


def overlay(oid, start, end, body):
    overlays.append((oid, start, end, body))
    js.append(f"tl.fromTo('#{oid}', {{opacity:0}}, {{opacity:1, duration:.16}}, {start:.3f});")
    js.append(f"tl.to('#{oid}', {{opacity:0, duration:.2, immediateRender:false}}, {end - 0.2:.3f});")
    return start


def ft(sel, at, a, b, d=0.35, e="power3.out", ir=None):
    b = dict(b, duration=round(d, 3), ease=e)
    if ir is not None:
        b["immediateRender"] = ir
    js.append(f"tl.fromTo('{sel}', {json.dumps(a)}, {json.dumps(b)}, {at:.3f});")


def to(sel, at, b, d=0.3, e="power2.out"):
    js.append(f"tl.to('{sel}', {json.dumps(dict(b, duration=round(d, 3), ease=e, immediateRender=False))}, {at:.3f});")


def st(sel, at, b):
    js.append(f"tl.set('{sel}', {json.dumps(b)}, {at:.3f});")


def kf(sel, at, frames, repeat=0):
    js.append(f"tl.to('{sel}', {{keyframes:{json.dumps(frames)}, repeat:{repeat}, immediateRender:false}}, {at:.3f});")


def pop(sel, at, s=0.4, y=24, d=0.42, ir=None, snd=None):
    ft(sel, at, {"opacity": 0, "scale": s, "y": y}, {"opacity": 1, "scale": 1, "y": 0}, d, "back.out(1.7)", ir)
    if snd:
        sfx.append((snd, at, 0.26))


def rise(sel, at, y=40, d=0.5, ir=None):
    ft(sel, at, {"opacity": 0, "y": y}, {"opacity": 1, "y": 0}, d, "power3.out", ir)


def mask_up(sel, at):
    ft(sel, at, {"opacity": 0, "y": 80, "clipPath": "inset(0% 0% 100% 0%)"}, {"opacity": 1, "y": 0, "clipPath": "inset(-30% -10% -30% -10%)"}, 0.5, "expo.out")


def wipe(sel, at, d=0.45):
    ft(sel, at, {"clipPath": "inset(0% 100% 0% 0%)"}, {"clipPath": "inset(0% 0% 0% 0%)"}, d, "power3.out")


def gone(sel, at, d=0.25):
    to(sel, at, {"opacity": 0, "scale": 0.9}, d, "power2.in")


def count(sel, at, a, b, d, ease="power2.out"):
    js.append(f"(function(){{ const o = {{v:{a}}}; tl.fromTo(o, {{v:{a}}}, {{v:{b}, duration:{d:.3f}, ease:'{ease}', immediateRender:false, onUpdate(){{ const e = document.querySelector('{sel}'); if (e) e.textContent = Math.round(o.v).toLocaleString('en-US'); }}}}, {at:.3f}); }})();")


def setnum(sel, at, txt):
    js.append(f"tl.call(() => {{ const e = document.querySelector('{sel}'); if (e) e.textContent = {json.dumps(txt)}; }}, null, {at:.3f});")


def bars(pfx, widths, x, y, gap=34, h=16):
    return "".join(f'<i class="bar" id="{pfx}{k}" style="left:{x}px;top:{y + k * gap}px;width:{wd}px;height:{h}px"></i>' for k, wd in enumerate(widths))


def mark(size):
    return f'<img class="mk" src="assets/img/claude-mark.svg" style="width:{size}px;height:{size}px">'


def chip_count(cid, top, label, value):
    return f'<div class="cnt" id="{cid}" style="top:{top}px"><span class="lab ink">{esc(label)}</span><b id="{cid}n">{value}</b></div>'


CUR = '<svg viewBox="0 0 24 24"><path d="M5 3 L5 19 L9 15 L12 22 L15 20.5 L11.5 14 L18 14 Z" fill="#fff" stroke="#161513" stroke-width="1.4" stroke-linejoin="round"/></svg>'


# ---------------------------------------------------------------- pixel agents
def ag(aid, kind, cx, cy, s, eyes=None, flip=False, weapon=None, alt=(), crown=False, poof=False, flash=False, z=None):
    """An agent whose body centre (canvas 16, 23) sits at (cx, cy); s = screen px per sprite pixel.
    Layers: body, eyes (default + alternates, swapped with eyes_to), prop/fx for its personality, an optional weapon."""
    eyes = eyes or (KINDEYE.get(kind, "open") if kind != "plain" else "open")
    W = 32 * s
    L = [f'<img src="{PX}/body.png">']
    for k, e in enumerate((eyes,) + tuple(alt)):
        L.append(f'<img class="ey e{k}" src="{PX}/eyes-{e}.png"{" style=opacity:0" if k else ""}>')
    if kind not in ("plain", None):
        L.append(f'<img class="pr pr-{kind}" src="{PX}/{kind}-prop.png"><img class="fx fx-{kind}" src="{PX}/{kind}-fx.png">')
    if crown:
        L.append(f'<img class="cr" src="{PX}/crown.png" style="left:{9 * s}px;top:{10 * s}px;width:{14 * s}px;height:{10 * s}px">')
    if weapon == "sword":
        L.append(f'<img class="wp" src="{PX}/sword.png" style="left:{22 * s}px;top:{19.5 * s}px;width:{18 * s}px;height:{6 * s}px;transform-origin:12% 55%">')
    elif weapon == "gun":
        L.append(f'<img class="wp" src="{PX}/gun.png" style="left:{22.5 * s}px;top:{19.5 * s}px;width:{13 * s}px;height:{8 * s}px;transform-origin:20% 40%">')
        if flash:
            L.append(f'<img class="fl" src="{PX}/flash.png" style="left:{35 * s}px;top:{17.5 * s}px;width:{7 * s}px;height:{7 * s}px;opacity:0">')
    extra = f'<img class="pf" src="{PX}/poof.png" style="left:{4 * s}px;top:{11 * s}px;width:{24 * s}px;height:{18 * s}px;opacity:0">' if poof else ""
    zs = f"z-index:{z};" if z is not None else ""
    return (f'<div class="px" id="{aid}" style="left:{cx - 16 * s:.1f}px;top:{cy - 23 * s:.1f}px;width:{W}px;height:{W}px;{zs}">'
            f'<div class="fp{" flip" if flip else ""}"><div class="in">{"".join(L)}</div></div>{extra}</div>')


def idle(aid, kind, s, t0, t1):
    if t1 - t0 > 0.3:
        js.append(f"idle('#{aid}','{kind}',{s},{t0:.3f},{t1:.3f});")


def eyes_to(aid, k, at):
    st(f"#{aid} .ey", at, {"opacity": 0})
    st(f"#{aid} .e{k}", at, {"opacity": 1})


def arm(aid, at):
    ft(f"#{aid} .wp", at, {"opacity": 0, "scale": 0.2, "rotation": -60}, {"opacity": 1, "scale": 1, "rotation": 0}, 0.3, "back.out(2)")


def swing(aid, at):
    kf(f"#{aid} .wp", at, [{"rotation": -80, "duration": 0.1}, {"rotation": 40, "duration": 0.09}, {"rotation": 0, "duration": 0.16}])


def fire(aid, at):
    kf(f"#{aid} .wp", at, [{"rotation": -18, "duration": 0.05}, {"rotation": 0, "duration": 0.15}])
    kf(f"#{aid} .fl", at, [{"opacity": 1, "scale": 1.2, "duration": 0.03}, {"opacity": 0, "scale": 0.6, "duration": 0.12}])


def dash(aid, at, dx, d=0.16):
    kf(f"#{aid}", at, [{"x": dx, "duration": d, "ease": "power2.out"}, {"x": 0, "duration": d * 1.4, "ease": "power2.inOut"}])


def knock(aid, at, k_ko, push=0):
    """Hit: flinch, KO eyes, then a pixel poof and the agent is gone."""
    eyes_to(aid, k_ko, at)
    kf(f"#{aid} .in", at, [{"x": push, "rotation": -12 if push < 0 else 12, "duration": 0.08}, {"x": 0, "rotation": 0, "duration": 0.12}])
    to(f"#{aid} .fp", at + 0.2, {"opacity": 0, "scale": 0.6}, 0.18, "power2.in")
    ft(f"#{aid} .pf", at + 0.18, {"opacity": 0, "scale": 0.4}, {"opacity": 1, "scale": 1.1}, 0.12, "power2.out", False)
    to(f"#{aid} .pf", at + 0.32, {"opacity": 0, "scale": 1.5}, 0.25, "power1.out")


def spawn(aid, at, s0=0.2, d=0.42):
    ft(f"#{aid}", at, {"opacity": 0, "scale": s0, "y": 18}, {"opacity": 1, "scale": 1, "y": 0}, d, "back.out(1.8)")


def kind_of(i):
    return CROWD[(i * 7 + (i // 10) * 3) % len(CROWD)]


def eye_of(i):
    return EYEV[(i * 5 + (i // 10)) % len(EYEV)]


def crowd_grid(pfx, x0, y0, dx, dy, s, weapons=False, alt=("angry", "ko"), poof=True):
    out_, cells = [], []
    for r in range(10):
        for c in range(10):
            i = r * 10 + c
            k = kind_of(i)
            wpn = None
            if weapons:
                wpn = "sword" if (r + c) % 2 == 0 else "gun"
                if k in ("coder", "rocket", "chef", "wizard", "sleuth", "coffee"):
                    k = "plain"
            aid = f"{pfx}{r}_{c}"
            cx, cy = x0 + c * dx, y0 + r * dy
            out_.append(ag(aid, k, cx, cy, s, eyes=eye_of(i) if weapons else None, flip=weapons and c % 2 == 1, weapon=wpn,
                           alt=alt, poof=poof, flash=wpn == "gun"))
            cells.append(dict(id=aid, r=r, c=c, cx=cx, cy=cy, kind=k, wpn=wpn))
    return "".join(out_), cells


def battle_rounds(cells, t_first, t_last, keep_id, dash_px=40):
    """Pair survivors in order, the attacker strikes (sword swing or gun fire), the loser is knocked out; repeat to one."""
    alive = list(cells)
    rounds = []
    while len(alive) > 1:
        nxt, pairs = [], []
        for k in range(0, len(alive) - 1, 2):
            a, b = alive[k], alive[k + 1]
            win = a if (a["id"] == keep_id or (b["id"] != keep_id and (a["r"] * 7 + a["c"] * 3 + len(rounds)) % 5 < 3)) else b
            pairs.append((win, b if win is a else a))
            nxt.append(win)
        if len(alive) % 2:
            nxt.append(alive[-1])
        rounds.append(pairs)
        alive = nxt
    n = len(rounds)
    times = [t_first + (t_last - t_first) * (1 - (1 - k / max(1, n - 1)) ** 1.4) for k in range(n)] if n > 1 else [t_first]
    left = len(cells)
    out_ = []
    for k, (pairs, at) in enumerate(zip(rounds, times)):
        spread = 0.5 if k == 0 else 0.2
        for j, (win, lose) in enumerate(pairs):
            a = at + (j * 0.37 % 1.0) * spread
            dx = lose["cx"] - win["cx"]
            if win["wpn"] == "gun":
                fire(win["id"], a)
            else:
                dash(win["id"], a, max(-dash_px, min(dash_px, dx * 0.4)))
                swing(win["id"], a + 0.05)
            knock(lose["id"], a + 0.1, 2, push=12 if dx > 0 else -12)
        left -= len(pairs)
        out_.append((at, left))
    return out_


# ---------------------------------------------------------------- bracket with agents in the slots
LSEED = [("coder", 7), ("chef", 42), ("music", 88), ("wizard", 23), ("sleuth", 61), ("coffee", 14), ("reader", 35), ("rocket", 96)]
RSEED = [("wizard", 71), ("coder", 3), ("coffee", 50), ("music", 19), ("chef", 64), ("reader", 27), ("sleuth", 80), ("rocket", 9)]
SY = [600 + k * 140 for k in range(8)]
XL = [92, 250, 360, 452]
CHP = (540, 1090)
WINS = {("L", 0): [1, 3, 4, 7], ("L", 1): [1, 7], ("L", 2): [1], ("R", 0): [0, 2, 5, 6], ("R", 1): [0, 6], ("R", 2): [0]}


def node_y(rnd, k):
    return SY[k] if rnd == 0 else (node_y(rnd - 1, 2 * k) + node_y(rnd - 1, 2 * k + 1)) / 2


def bx(side, rnd):
    return XL[rnd] if side == "L" else 1080 - XL[rnd]


def elbow(side, rnd, k):
    x1, y1 = bx(side, rnd), node_y(rnd, k)
    if rnd == 3:
        x2, y2 = CHP
        return f"M{x1} {y1} L{x2} {y2}", abs(x2 - x1)
    x2, y2 = bx(side, rnd + 1), node_y(rnd + 1, k // 2)
    xm = (x1 + x2) / 2
    return f"M{x1} {y1} H{xm} V{y2} H{x2}", abs(xm - x1) + abs(y2 - y1) + abs(x2 - xm)


def bracket_html(pfx, s=3.2):
    paths, slots, agents = [], [], []
    for side, seeds in (("L", LSEED), ("R", RSEED)):
        for rnd in range(4):
            for k in range(8 >> rnd):
                d, ln = elbow(side, rnd, k)
                paths.append(f'<path class="bl" id="{pfx}g{side}{rnd}{k}" d="{d}" style="stroke-dasharray:{ln:.1f};stroke-dashoffset:{ln:.1f}"/>')
                paths.append(f'<path class="blw" id="{pfx}w{side}{rnd}{k}" d="{d}" style="stroke-dasharray:{ln:.1f};stroke-dashoffset:{ln:.1f}"/>')
                if rnd > 0:
                    slots.append(f'<i class="nd" id="{pfx}n{side}{rnd}{k}" style="left:{bx(side, rnd)}px;top:{node_y(rnd, k)}px"></i>')
        for k, (kind, num) in enumerate(seeds):
            x, y = bx(side, 0), SY[k]
            slots.append(f'<div class="slot" id="{pfx}sl{side}{k}" style="left:{x}px;top:{y}px"></div>')
            slots.append(f'<span class="snum" id="{pfx}lb{side}{k}" style="left:{x - 40}px;top:{y + 58}px">{num:02d}</span>')
            agents.append(ag(f"{pfx}a{side}{k}", kind, x, y + 10, s, alt=("happy", "ko"), poof=True, z=3))
    champ = f'<div class="champ" id="{pfx}ch" style="left:{CHP[0]}px;top:{CHP[1]}px"><img src="{PX}/crown.png" class="pxi" style="width:84px;height:60px"></div>'
    return f'<svg class="bsvg" viewBox="0 0 1080 1920">{"".join(paths)}</svg>{"".join(slots)}{champ}{"".join(agents)}'


def bracket_build(pfx, at, d=1.0, immediate=False, drop="down"):
    for side in "LR":
        for k in range(8):
            if immediate:
                for sel in (f"#{pfx}sl{side}{k}", f"#{pfx}a{side}{k}", f"#{pfx}lb{side}{k}"):
                    st(sel, at, {"opacity": 1})
                continue
            a = at + k * 0.07 + (0.035 if side == "R" else 0)
            ft(f"#{pfx}sl{side}{k}", a, {"opacity": 0, "scale": 0.6}, {"opacity": 1, "scale": 1}, 0.3, "power3.out")
            if drop == "down":
                ft(f"#{pfx}a{side}{k}", a + 0.08, {"opacity": 0, "y": -90}, {"opacity": 1, "y": 0}, 0.5, "bounce.out")
            else:
                ft(f"#{pfx}a{side}{k}", a + 0.08, {"opacity": 0, "x": -160 if side == "L" else 160}, {"opacity": 1, "x": 0}, 0.5, "power3.out")
            ft(f"#{pfx}lb{side}{k}", a + 0.2, {"opacity": 0}, {"opacity": 1}, 0.3, "power1.out")
    base = at + (0 if immediate else 0.6)
    for rnd in range(4):
        for side in "LR":
            for k in range(8 >> rnd):
                sel = f"#{pfx}g{side}{rnd}{k}"
                if immediate:
                    st(sel, at, {"strokeDashoffset": 0})
                    if rnd:
                        st(f"#{pfx}n{side}{rnd}{k}", at, {"opacity": 1, "scale": 1})
                    continue
                ft(sel, base + rnd * d / 4, {"strokeDashoffset": elbow(side, rnd, k)[1]}, {"strokeDashoffset": 0}, d / 4 + 0.15, "power2.inOut", False)
                if rnd:
                    ft(f"#{pfx}n{side}{rnd}{k}", base + rnd * d / 4 + 0.15, {"opacity": 0, "scale": 0.3}, {"opacity": 1, "scale": 1}, 0.25, "back.out(2)")
    if immediate:
        st(f"#{pfx}ch", at, {"opacity": 1, "scale": 1})
    else:
        ft(f"#{pfx}ch", base + d, {"opacity": 0, "scale": 0.3}, {"opacity": 1, "scale": 1}, 0.4, "back.out(2)")
        for k in range(4):
            sfx.append(("tick_001", base + k * d / 4, 0.18))


def bracket_round(pfx, rnd, at):
    """The judge knocks out the loser of every match; the winner hops along its line to the next node."""
    for side in "LR":
        prev = list(range(8)) if rnd == 0 else WINS[(side, rnd - 1)]
        for k in range(8 >> (rnd + 1)):
            a, b = prev[2 * k], prev[2 * k + 1]
            win = WINS[(side, rnd)][k]
            lose = b if win == a else a
            knock(f"{pfx}a{side}{lose}", at, 2)
            x0, y0 = bx(side, 0), SY[win] + 10
            x1, y1 = bx(side, rnd + 1), node_y(rnd + 1, k) + 10
            kf(f"#{pfx}a{side}{win}", at + 0.12, [{"x": (x0 + x1) / 2 - x0 if rnd == 0 else (bx(side, rnd) + x1) / 2 - x0, "y": (y1 - y0) / 2 - 50 if rnd == 0 else (node_y(rnd, prev.index(win)) + y1) / 2 - y0 - 50, "duration": 0.18, "ease": "power2.out"},
                                                  {"x": x1 - x0, "y": y1 - y0, "duration": 0.2, "ease": "power2.in"}])
            wi = prev.index(win) if rnd else win
            ft(f"#{pfx}w{side}{rnd}{wi}", at + 0.05, {"strokeDashoffset": elbow(side, rnd, wi)[1]}, {"strokeDashoffset": 0}, 0.38, "power2.inOut", False)


def bracket_final(pfx, at):
    """Left semi-final winner takes the centre; the right one is knocked out."""
    knock(f"{pfx}aR0", at, 2)
    x0, y0 = bx("L", 0), SY[1] + 10
    kf(f"#{pfx}aL1", at + 0.12, [{"x": (CHP[0] - 60) - x0, "y": CHP[1] - 120 - y0, "duration": 0.22, "ease": "power2.out"},
                                 {"x": CHP[0] - x0, "y": CHP[1] + 10 - y0, "duration": 0.2, "ease": "power2.in"}])
    ft(f"#{pfx}wL30", at + 0.05, {"strokeDashoffset": elbow("L", 3, 0)[1]}, {"strokeDashoffset": 0}, 0.3, "power2.inOut", False)
    gone(f"#{pfx}ch", at + 0.2)
    to(f"#{pfx}aL1", at + 0.45, {"scale": 1.4}, 0.3, "back.out(2)")
    eyes_to(f"{pfx}aL1", 1, at + 0.45)
    sfx.append(("confirmation_002", at + 0.4, 0.3))


# ---------------------------------------------------------------- pages and overlays
def head(pid, label, title, y=230, size=None):
    st_ = f' style="margin-top:14px;font-size:{size}px"' if size else ' style="margin-top:14px"'
    return f'<div class="stack" style="top:{y}px"><span class="lab" id="{pid}lab">{esc(label)}</span><span class="h1" id="{pid}tt"{st_}>{title}</span></div>'


def head_in(pid, s):
    rise(f"#{pid}lab", s + 0.1, 20)
    mask_up(f"#{pid}tt", s + 0.18)


def ov_bad(at, i_stop, end, oid="obad"):
    """One agent at its laptop gets a bad answer and gets fed up (no reprompting graphic)."""
    body = (ag(f"{oid}a", "coder", 300, 1600, 11, alt=("angry", "closed")) +
            f'<div class="card ans abs" id="{oid}c" style="left:560px;top:1330px;width:420px;height:250px;transform:rotate(3deg)">'
            f'<span class="lab ink" style="position:absolute;left:30px;top:26px">ai answer</span>{bars(oid + "b", [340, 260, 300, 180], 30, 86, 40, 16)}'
            f'<div class="xx" id="{oid}x">✕</div></div>')
    overlay(oid, at - 0.15, end, body)
    rise(f"#{oid}a", at - 0.1, 60)
    idle(f"{oid}a", "coder", 11, at, end)
    pop(f"#{oid}c", at + 0.1, 0.6, 30, snd="pluck_001")
    for k in range(4):
        wipe(f"#{oid}b{k}", at + 0.2 + k * 0.08, 0.3)
    pop(f"#{oid}x", at + 0.65, 0.3, 0, 0.3)
    sfx.append(("hard-pop-click", at + 0.65, 0.16))
    eyes_to(f"{oid}a", 1, t(i_stop) - 0.05)
    kf(f"#{oid}c", t(i_stop), [{"x": 10, "duration": 0.05}, {"x": -10, "duration": 0.05}, {"x": 6, "duration": 0.05}, {"x": 0, "duration": 0.05}])
    kf(f"#{oid}a .in", t(i_stop) + 0.4, [{"y": -18, "duration": 0.12}, {"y": 0, "duration": 0.14}])


def pg_crowd(start, i_100, i_battle, i_death, end, pid="pg", title=None, opened=False):
    """One agent fills the page, then 99 more pop out around it, every one a different personality. On 'battle' they arm up."""
    s = 4.2
    g, cells = crowd_grid(pid, 117, 690, 94, 104, s, weapons=i_battle is not None, alt=("angry", "ko"))
    hero = cells[45]
    lbl = title or ("your prompt goes to", f'<span class="num" id="{pid}n">1</span> <span class="acc" id="{pid}u">agent</span>')
    body = head(pid, lbl[0], lbl[1], 210) + f'<div class="cam2" id="{pid}cam">{g}</div>'
    sc = scene(pid, start, end, body, opened=opened)
    if opened:
        st(f"#{pid}lab", sc, {"opacity": 1})
        st(f"#{pid}tt", sc, {"opacity": 1})
    else:
        head_in(pid, sc)
    t100 = t(i_100)
    st(f"#{hero['id']}", sc, {"opacity": 1})
    ft(f"#{hero['id']}", sc, {"scale": 3.3, "x": 540 - hero["cx"], "y": 1180 - hero["cy"]}, {"scale": 3.0, "x": 540 - hero["cx"], "y": 1180 - hero["cy"]},
       max(0.3, t100 - sc - 0.1), "sine.inOut", True)
    to(f"#{hero['id']}", t100 - 0.1, {"scale": 1, "x": 0, "y": 0}, 0.6, "power3.inOut")
    idle(hero["id"], hero["kind"], s, sc, end)
    for c in cells:
        if c is hero:
            continue
        dist = math.hypot(c["r"] - 4.5, c["c"] - 5) / 7
        spawn(c["id"], t100 + 0.15 + dist * 0.75)
        idle(c["id"], c["kind"], s, t100 + 0.6 + dist * 0.75, end)
    for k in range(6):
        sfx.append(("tick_001", t100 + 0.15 + k * 0.14, 0.16))
    count(f"#{pid}n", t100, 1, 100, 1.0)
    if title is None:
        setnum(f"#{pid}u", t100 + 0.2, "agents")
    else:
        st(f"#{pid}s", sc, {"opacity": 0})
        st(f"#{pid}s", t100 + 0.2, {"opacity": 1})
    if i_battle is not None:
        st(f"#{pid}cam .wp", sc, {"opacity": 0})
        for c in cells:
            arm(c["id"], t(i_battle) + (c["r"] + c["c"]) * 0.012)
            eyes_to(c["id"], 1, t(i_battle) + 0.1)
        ft(f"#{pid}cam", t(i_battle), {"scale": 1}, {"scale": 1.08}, max(0.5, end - t(i_battle)), "sine.inOut", False)
        rounds = battle_rounds(cells, t(i_death) - 0.1, t(i_death) + 0.2, hero["id"])
        # only the first waves land before the page leaves: the field thins "to the death"


def pg_arena(start, end, pid="pa", drop="down", title="ARENA"):
    """'Arena': the tournament bracket sheet, every slot an agent, the crown waiting in the middle."""
    body = (f'<div class="stack" style="top:200px"><span class="lab" id="{pid}lab">a free claude skill</span>'
            f'<span class="h1 big" id="{pid}tt" style="margin-top:6px">{title}</span></div>' + bracket_html(pid))
    s = scene(pid, start, end, body)
    rise(f"#{pid}lab", s + 0.1, 20)
    mask_up(f"#{pid}tt", s + 0.12)
    bracket_build(pid, s + 0.2, 0.9, drop=drop)
    for side, seeds in (("L", LSEED), ("R", RSEED)):
        for k, (kind, _) in enumerate(seeds):
            idle(f"{pid}a{side}{k}", kind, 2, s + 0.9, end)
    sfx.append(("maximize_002", s + 0.1, 0.22))


def ov_free(at, end):
    oid = "ofree"
    body = f'<div class="tag big" id="{oid}t" style="left:300px;top:1450px;transform:rotate(-5deg)">FREE</div>' + ag(f"{oid}a", "coffee", 830, 1660, 7)
    overlay(oid, at - 0.1, end, body)
    pop(f"#{oid}t", at - 0.05, 0.3, 30, 0.42, snd="pluck_002")
    rise(f"#{oid}a", at, 50)
    idle(f"{oid}a", "coffee", 7, at, end)


def pg_split(start, i_question, i_prompt, i_battle, i_hundred, end, pid="pf"):
    """One prompt card glides in, '1 question' becomes '1 prompt', then the card splits into 100 agents that spread out."""
    s = 4.2
    g, cells = crowd_grid(pid, 117, 800, 94, 96, s, alt=("wide",), poof=False)
    body = (f'<div class="pcard" id="{pid}c"><span class="lab ink">your prompt</span>'
            f'<div class="pline"><span class="h2 ink" id="{pid}q">1 question</span><span class="h2 coral" id="{pid}p">1 prompt</span></div></div>'
            f'{g}{chip_count(pid + "k", 1790, "agents", "0")}')
    sc = scene(pid, start, end, body)
    ft(f"#{pid}c", sc + 0.05, {"opacity": 0, "y": 260, "scale": 0.92}, {"opacity": 1, "y": 0, "scale": 1}, 0.7, "power3.out")
    ft(f"#{pid}q", max(sc + 0.3, t(i_question) - 0.15), {"clipPath": "inset(0% 100% 0% 0%)"}, {"clipPath": "inset(0% 0% 0% 0%)"}, 0.45, "steps(10)")
    to(f"#{pid}q", t(i_prompt) - 0.05, {"opacity": 0, "y": -30}, 0.25, "power2.in")
    ft(f"#{pid}p", t(i_prompt) + 0.05, {"opacity": 0, "y": 30}, {"opacity": 1, "y": 0}, 0.35, "power3.out")
    tb = t(i_battle)
    to(f"#{pid}c", tb - 0.6, {"y": -440, "scale": 0.8}, 0.65, "power3.inOut")
    cy0 = 960 - 440 + 30
    for c in cells:
        dist = math.hypot(c["cx"] - 540, c["cy"] - cy0) / 1150
        a = tb + dist * 0.75
        ft(f"#{c['id']}", a, {"opacity": 0, "x": 540 - c["cx"], "y": cy0 - c["cy"], "scale": 0.3},
           {"opacity": 1, "x": 0, "y": 0, "scale": 1}, 0.65, "power3.out")
        idle(c["id"], c["kind"], s, a + 0.65, end)
    for k in range(5):
        sfx.append(("tick_001", tb + k * 0.15, 0.16))
    rise(f"#{pid}k", tb, 30)
    count(f"#{pid}kn", tb, 1, 100, max(0.6, t(i_hundred) - tb + 0.2))


PROMPT = "Find me 20 plumbers in Belfast"


def pg_type(start, i_task, i_claude, i_type, i_slash, i_arena, i_end, end, pid="pt", prefill=False):
    """The real Claude prompt box: the task types in, then /arena, which lights up like a skill starting; an agent launches."""
    chars = "".join(f'<span class="tc" id="{pid}c{k}">{esc(ch) if ch != " " else "&nbsp;"}</span>' for k, ch in enumerate(PROMPT))
    tok = "".join(f'<span class="tc" id="{pid}s{k}">{ch}</span>' for k, ch in enumerate("/arena"))
    body = (head(pid, "at the end of any task", 'type <span class="coral">/arena</span>', 230)
            + f'<div class="ubox" id="{pid}b"><img src="assets/img/claude-prompt-empty.png"><i class="ucover"></i>'
            f'<div class="utext">{chars}<span class="tc" id="{pid}sp">&nbsp;</span><span class="tokin" id="{pid}ti">{tok}</span><i class="ucaret" id="{pid}ca"></i></div></div>'
            f'<div class="halo" id="{pid}h"></div><span class="lab abs" id="{pid}src" style="left:60px;top:860px">real claude app</span>'
            + ag(f"{pid}a", "rocket", 470, 1330, 15, alt=("wide", "happy")))
    s = scene(pid, start, end, body)
    rise(f"#{pid}lab", s + 0.1, 20)
    ft(f"#{pid}b", s + 0.05, {"opacity": 0, "y": 80}, {"opacity": 1, "y": 0}, 0.6, "power3.out")
    rise(f"#{pid}src", s + 0.4, 10)
    rise(f"#{pid}a", s + 0.3, 80)
    idle(f"{pid}a", "plain", 15, s + 0.8, end)
    to(f"#{pid}ca", s, {"opacity": 0, "repeat": int((end - s) / 0.3), "yoyo": True}, 0.3, "steps(1)")
    a0 = max(s + 0.35, t(i_task))
    a1 = max(a0 + 1.0, te(i_claude))
    if prefill:
        st(f"#{pid} .utext > .tc", s, {"display": "inline-block"})
        st(f"#{pid}sp", s, {"display": "none"})
        a1 = s
    for k in range(len(PROMPT) if not prefill else 0):
        at = a0 + (a1 - a0) * k / len(PROMPT) + (0.02 if k % 3 == 0 else 0)
        st(f"#{pid}c{k}", at, {"display": "inline-block"})
        if k % 3 == 0:
            sfx.append(("click_004" if k % 2 else "click_002", at, 0.35))
    mask_up(f"#{pid}tt", max(a1 + 0.1, t(i_type) - 0.1))
    st(f"#{pid}sp", t(i_slash) - 0.05, {"display": "inline-block"})
    st(f"#{pid}ti", t(i_slash) - 0.02, {"display": "inline-block"})
    times = [t(i_slash)] + [t(i_arena) + k * max(0.07, (te(i_arena) - t(i_arena)) / 5) for k in range(5)]
    for k, at in enumerate(times):
        st(f"#{pid}s{k}", at, {"display": "inline-block"})
        sfx.append(("click_002", at, 0.4))
    on = t(i_end)
    to(f"#{pid}ti", on, {"backgroundColor": CORAL, "color": WHITE}, 0.18)
    ft(f"#{pid}h", on, {"opacity": 0.85, "scale": 0.5}, {"opacity": 0, "scale": 1.5}, 0.9, "power2.out")
    ft(f"#{pid}ti", on, {"boxShadow": "0 0 0px 0px rgba(217,119,87,0)"}, {"boxShadow": "0 0 34px 10px rgba(217,119,87,0.55)"}, 0.3, "power2.out", False)
    to(f"#{pid}ti", on + 0.35, {"boxShadow": "0 0 16px 4px rgba(217,119,87,0.35)"}, 0.4)
    sfx.append(("confirmation_002", on, 0.3))
    eyes_to(f"{pid}a", 1, on + 0.05)
    kf(f"#{pid}a .in", on + 0.1, [{"y": -40, "duration": 0.14}, {"y": 0, "duration": 0.16}])
    ft(f"#{pid}a .fx", on + 0.25, {"y": 0, "opacity": 1}, {"y": -640, "opacity": 0}, 0.9, "power2.in", False)
    sfx.append(("riser", on + 0.1, 0.16))


def ov_task(i_task, i_claude, end, oid="otask"):
    """'Any task you give Claude': the real Claude prompt box on his chest, the task typing in like a real caret."""
    chars = "".join(f'<span class="tc" id="{oid}c{k}">{esc(ch) if ch != " " else "&nbsp;"}</span>' for k, ch in enumerate(PROMPT))
    body = (f'<div class="ubox" id="{oid}b" style="top:1430px"><img src="assets/img/claude-prompt-empty.png"><i class="ucover"></i>'
            f'<div class="utext">{chars}<i class="ucaret" id="{oid}ca"></i></div></div>'
            f'<span class="tl" id="{oid}l" style="left:60px;top:1650px;width:auto;text-align:left">real claude app</span>' + ag(f"{oid}a", "coder", 880, 1350, 6))
    a0 = t(i_task) - 0.2
    overlay(oid, a0, end, body)
    ft(f"#{oid}b", a0, {"opacity": 0, "y": 60}, {"opacity": 1, "y": 0}, 0.5, "power3.out")
    rise(f"#{oid}l", a0 + 0.3, 10)
    rise(f"#{oid}a", a0 + 0.2, 30)
    idle(f"{oid}a", "coder", 6, a0, end)
    to(f"#{oid}ca", a0, {"opacity": 0, "repeat": int((end - a0) / 0.3), "yoyo": True}, 0.3, "steps(1)")
    b0, b1 = t(i_task) + 0.1, max(t(i_task) + 1.1, te(i_claude))
    for k in range(len(PROMPT)):
        at = b0 + (b1 - b0) * k / len(PROMPT) + (0.02 if k % 3 == 0 else 0)
        st(f"#{oid}c{k}", at, {"display": "inline-block"})
        if k % 3 == 0:
            sfx.append(("click_004" if k % 2 else "click_002", at, 0.35))


def ov_crowned(i_winner, end, oid="owin"):
    body = ag(f"{oid}a", "plain", 540, 1660, 7, eyes="happy", crown=True) + f'<div class="tag" id="{oid}t" style="left:400px;top:1360px">the winner</div>'
    overlay(oid, t(i_winner) - 0.15, end, body)
    rise(f"#{oid}a", t(i_winner) - 0.1, 50)
    idle(f"{oid}a", "plain", 7, t(i_winner), end)
    pop(f"#{oid}t", t(i_winner) + 0.1, 0.4, 0, 0.3, snd="pluck_002")


def pg_broadcast(start, i_prompt, end, pid="pb"):
    """'All 100 agents get your initial prompt': the prompt drops and every agent catches a copy, wave by wave."""
    s = 4.2
    g, cells = crowd_grid(pid, 117, 800, 94, 96, s, alt=("wide",), poof=False)
    notes = "".join(f'<img class="note pxi" id="{pid}nt{c["r"]}_{c["c"]}" src="{PX}/note.png" style="left:{c["cx"] - 20}px;top:{c["cy"] - 5 * s - 44}px;width:40px;height:35px">' for c in cells)
    body = (f'<div class="pcard sm" id="{pid}c"><span class="lab ink">your prompt</span><div class="pline"><span class="h3 ink">{PROMPT} <span class="coral">/arena</span></span></div></div>'
            f'{g}{notes}{chip_count(pid + "k", 1790, "got your prompt", "0")}')
    sc = scene(pid, start, end, body)
    ft(f"#{pid}c", sc + 0.05, {"opacity": 0, "y": -60}, {"opacity": 1, "y": 0}, 0.55, "power3.out")
    for c in cells:
        st(f"#{c['id']}", sc, {"opacity": 1})
        idle(c["id"], c["kind"], s, sc, end)
    a = max(sc + 0.7, t(i_prompt) - 0.3)
    for c in cells:
        at = a + c["r"] * 0.08 + abs(c["c"] - 4.5) * 0.015
        ft(f"#{pid}nt{c['r']}_{c['c']}", at, {"opacity": 0, "y": -120}, {"opacity": 1, "y": 0}, 0.35, "power2.in")
        eyes_to(c["id"], 1, at + 0.3)
    for k in range(6):
        sfx.append(("tick_001", a + k * 0.14, 0.16))
    rise(f"#{pid}k", a - 0.1, 30)
    count(f"#{pid}kn", a, 0, 100, 1.1, "none")


def ov_march(at, i_battlefield, end, oid="omarch"):
    row = "".join(ag(f"{oid}m{k}", "plain", 80 + k * 132, 1640, 5.5, eyes="angry", weapon="sword" if k % 2 else "gun") for k in range(8))
    body = row + f'<div class="tag" id="{oid}t" style="left:440px;top:1380px">×100</div>'
    overlay(oid, at - 0.1, end, body)
    st(f"#{oid} .wp", at - 0.1, {"opacity": 0})
    for k in range(8):
        ft(f"#{oid}m{k}", at + k * 0.06, {"opacity": 0, "x": -260}, {"opacity": 1, "x": 0}, 0.6, "power3.out")
        js.append(f"tl.to('#{oid}m{k} .in', {{keyframes:[{{y:-8,duration:.14,ease:'steps(1)'}},{{y:0,duration:.14,ease:'steps(1)'}}], repeat:{int((end - at) / 0.28)}, immediateRender:false}}, {at + k * 0.03:.3f});")
        arm(f"{oid}m{k}", t(i_battlefield) + k * 0.04)
    pop(f"#{oid}t", at + 0.4, 0.4, 0, 0.3, snd="pluck_001")


def pg_battle(start, i_battling, i_top, i_best, end, pid="pw"):
    """They actually battle: 100 armed agents pair off, swing swords and fire guns, poof out wave by wave, one is left."""
    s = 4.0
    g, cells = crowd_grid(pid, 117, 630, 94, 104, s, weapons=True, alt=("angry", "ko"))
    body = (f'<div class="cam2" id="{pid}cam">{g}</div>{chip_count(pid + "k", 240, "agents left", "100")}'
            f'<div class="card abs" id="{pid}ans" style="left:240px;top:1560px;width:600px;height:220px">'
            f'<span class="lab coral" style="position:absolute;left:36px;top:28px">best answer</span>{bars(pid + "b", [500, 420, 460], 36, 86, 38, 16)}</div>')
    sc = scene(pid, start, end, body)
    rise(f"#{pid}k", sc + 0.1, 20)
    for c in cells:
        st(f"#{c['id']}", sc, {"opacity": 1})
        eyes_to(c["id"], 1, sc)
        idle(c["id"], "plain", s, sc, end)
    keep = next(c for c in cells if c["r"] == 4 and c["c"] == 4)
    for at, left in battle_rounds(cells, max(sc + 0.25, t(i_battling)), t(i_top) - 0.15, keep["id"]):
        setnum(f"#{pid}kn", at + 0.12, str(left))
    ft(f"#{pid}cam", sc, {"scale": 1}, {"scale": 1.12}, max(0.5, t(i_top) - sc), "sine.inOut", False)
    z = 3.2
    to(f"#{pid}cam", t(i_top) + 0.1, {"scale": z, "x": (540 - keep["cx"]) * z, "y": (1060 - keep["cy"]) * z - (1060 - 960) * (z - 1) * 0}, 0.7, "power3.inOut")
    eyes_to(keep["id"], 0, t(i_top) + 0.3)
    sfx.append(("confirmation_002", t(i_top) + 0.4, 0.28))
    rise(f"#{pid}ans", t(i_best) - 0.1, 60)
    for k in range(3):
        wipe(f"#{pid}b{k}", t(i_best) + k * 0.1, 0.35)


PERSONAS = [("coder", "the coder"), ("coffee", "coffee addict"), ("music", "the music head"), ("chef", "the chef"), ("wizard", "the wizard"), ("sleuth", "the detective")]


def pg_personas(start, ats, end, pid="pp"):
    cards = []
    for k, (kind, lab) in enumerate(PERSONAS):
        x, y = 70 + (k % 2) * 480, 470 + (k // 2) * 410
        cards.append(f'<div class="card pcd abs" id="{pid}c{k}" style="left:{x}px;top:{y}px;width:460px;height:380px">'
                     + ag(f"{pid}a{k}", kind, 230, 196, 8) + f'<span class="lab ink abs" style="left:0;right:0;top:318px;text-align:center">{lab}</span></div>')
    body = head(pid, "every agent thinks differently", 'own <span class="acc">personality</span>', 220, 112) + "".join(cards)
    s = scene(pid, start, end, body)
    head_in(pid, s)
    for k, (kind, _) in enumerate(PERSONAS):
        ft(f"#{pid}c{k}", ats[k], {"opacity": 0, "y": 50, "scale": 0.94}, {"opacity": 1, "y": 0, "scale": 1}, 0.45, "power3.out")
        idle(f"{pid}a{k}", kind, 8, ats[k], end)
        sfx.append(("pluck_001" if k % 2 else "pluck_002", ats[k], 0.18))


def ov_answers(i_every, i_all, i_come, i_diff, end, oid="oans"):
    W_ = [[250, 190, 220, 140], [250, 220, 160, 200], [230, 250, 180, 130]]
    kinds = ["reader", "coffee", "wizard"]
    parts = []
    for k in range(3):
        x = 40 + k * 340
        parts.append(f'<div class="card ans abs" id="{oid}c{k}" style="left:{x}px;top:1300px;width:320px;height:220px">'
                     f'<span class="lab ink" style="position:absolute;left:22px;top:20px">answer {k + 1}</span>{bars(f"{oid}b{k}", W_[k], 22, 74, 36, 15)}</div>')
        parts.append(ag(f"{oid}a{k}", kinds[k], x + 160, 1730, 6.5))
    overlay(oid, t(i_every) - 0.15, end, "".join(parts))
    for k, i in enumerate((i_every, i_all, i_come)):
        rise(f"#{oid}a{k}", t(i) - 0.1, 60)
        pop(f"#{oid}c{k}", t(i) + 0.05, 0.6, 30, snd="pluck_001")
        idle(f"{oid}a{k}", kinds[k], 6.5, t(i), end)
    for k, row in enumerate((1, 3, 2)):
        to(f"#{oid}b{k}{row}", t(i_diff) + k * 0.12, {"backgroundColor": CORAL}, 0.15)
    sfx.append(("glass_002", t(i_diff), 0.22))


def pg_bracket_pair(start, i_bracket, i_tournament, end, pid="pk"):
    body = head(pid, "100 agents · 50 matches", 'the <span class="acc">bracket</span>', 200) + bracket_html(pid)
    s = scene(pid, start, end, body)
    head_in(pid, s)
    bracket_build(pid, max(s + 0.2, t(i_bracket) - 0.4), 1.0, drop="side")
    for side, seeds in (("L", LSEED), ("R", RSEED)):
        for k, (kind, _) in enumerate(seeds):
            idle(f"{pid}a{side}{k}", kind, 2, s + 0.9, end)
    setnum(f"#{pid}lab", t(i_tournament), "like a tournament")


def ov_vs(i_attack, i_each, i_answers, end, oid="ovs"):
    """Agent vs agent: sword against gun, a short fight and a knockout."""
    s = 11
    y = 1600
    body = (ag(f"{oid}L", "plain", 250, y, s, eyes="angry", weapon="sword", alt=("ko",), poof=True) +
            ag(f"{oid}R", "plain", 830, y, s, eyes="angry", weapon="gun", flip=True, alt=("ko",), poof=True, flash=True) +
            f'<div class="vs" id="{oid}vs" style="left:540px;top:{y - 60}px">VS</div>')
    a0 = t(i_attack) - 0.55
    overlay(oid, a0, end, body)
    ft(f"#{oid}L", a0, {"opacity": 0, "x": -300}, {"opacity": 1, "x": 0}, 0.45, "power3.out")
    ft(f"#{oid}R", a0 + 0.05, {"opacity": 0, "x": 300}, {"opacity": 1, "x": 0}, 0.45, "power3.out")
    pop(f"#{oid}vs", a0 + 0.3, 0.3, 0, 0.35)
    idle(f"{oid}L", "plain", s, a0 + 0.5, end)
    idle(f"{oid}R", "plain", s, a0 + 0.5, end)
    dash(f"{oid}L", t(i_attack), 150, 0.18)
    swing(f"{oid}L", t(i_attack) + 0.08)
    kf(f"#{oid}R .in", t(i_attack) + 0.18, [{"x": 30, "rotation": 10, "duration": 0.08}, {"x": 0, "rotation": 0, "duration": 0.14}])
    fire(f"{oid}R", t(i_each))
    kf(f"#{oid}L .in", t(i_each) + 0.06, [{"x": -30, "rotation": -10, "duration": 0.08}, {"x": 0, "rotation": 0, "duration": 0.14}])
    dash(f"{oid}L", t(i_answers) - 0.05, 170, 0.18)
    swing(f"{oid}L", t(i_answers))
    knock(f"{oid}R", t(i_answers) + 0.12, 1, push=40)


def pg_vs_magic(start, i_attack, i_each, i_answers, end, pid="pv"):
    """V2: a wizard and a chef face off: a sparkle bolt, a pan swing, a knockout."""
    s = 12
    body = (head(pid, "every match", 'agent <span class="acc">vs</span> agent', 300, 120) +
            ag(f"{pid}L", "wizard", 290, 1180, s, alt=("ko",), poof=True) + ag(f"{pid}R", "chef", 790, 1180, s, flip=True, alt=("ko",), poof=True) +
            f'<div class="vs" id="{pid}vs" style="left:540px;top:1120px">VS</div><i class="bolt" id="{pid}bo" style="left:450px;top:1100px;width:250px"></i>')
    sc = scene(pid, start, end, body)
    head_in(pid, sc)
    ft(f"#{pid}L", sc + 0.1, {"opacity": 0, "x": -300}, {"opacity": 1, "x": 0}, 0.5, "power3.out")
    ft(f"#{pid}R", sc + 0.15, {"opacity": 0, "x": 300}, {"opacity": 1, "x": 0}, 0.5, "power3.out")
    pop(f"#{pid}vs", sc + 0.4, 0.3, 0, 0.35)
    idle(f"{pid}L", "wizard", s, sc + 0.5, end)
    idle(f"{pid}R", "chef", s, sc + 0.5, end)
    for at in (t(i_attack), t(i_answers)):
        ft(f"#{pid}bo", at, {"opacity": 1, "scaleX": 0}, {"opacity": 1, "scaleX": 1}, 0.14, "power2.out", False)
        to(f"#{pid}bo", at + 0.18, {"opacity": 0}, 0.12)
    kf(f"#{pid}R .in", t(i_attack) + 0.14, [{"x": -24, "rotation": 10, "duration": 0.08}, {"x": 0, "rotation": 0, "duration": 0.14}])
    kf(f"#{pid}R", t(i_each), [{"x": -260, "duration": 0.16, "ease": "power2.out"}, {"x": 0, "duration": 0.24}])
    kf(f"#{pid}R .in", t(i_each) + 0.1, [{"rotation": 25, "duration": 0.08}, {"rotation": 0, "duration": 0.12}])
    kf(f"#{pid}L .in", t(i_each) + 0.16, [{"x": -24, "rotation": -10, "duration": 0.08}, {"x": 0, "rotation": 0, "duration": 0.14}])
    knock(f"{pid}R", t(i_answers) + 0.14, 1, push=30)


def pg_judge(start, rounds, t_final, end, pid="pj"):
    body = (f'<div class="stack" style="top:200px"><span class="lab" id="{pid}lab">the judge knocks out every loser</span></div>'
            + chip_count(pid + "k", 290, "agents left", "16") + bracket_html(pid) + f'<div class="gavel" id="{pid}gv" style="left:540px;top:1770px">JUDGE</div>')
    s = scene(pid, start, end, body)
    bracket_build(pid, s, immediate=True)
    rise(f"#{pid}lab", s + 0.1, 20)
    rise(f"#{pid}k", s + 0.15, 20)
    pop(f"#{pid}gv", s + 0.2, 0.5, 20, 0.3)
    for side, seeds in (("L", LSEED), ("R", RSEED)):
        for k, (kind, _) in enumerate(seeds):
            idle(f"{pid}a{side}{k}", kind, 2, s, end)
    for rnd, at in enumerate(rounds):
        bracket_round(pid, rnd, at)
        kf(f"#{pid}gv", at - 0.1, [{"rotation": -14, "duration": 0.08}, {"rotation": 0, "duration": 0.1}])
        setnum(f"#{pid}kn", at + 0.15, str([8, 4, 2][rnd]))
    bracket_final(pid, t_final)
    kf(f"#{pid}gv", t_final - 0.1, [{"rotation": -14, "duration": 0.08}, {"rotation": 0, "duration": 0.1}])
    setnum(f"#{pid}kn", t_final + 0.15, "1")


def pg_crown(start, end, pid="pcr"):
    """1 left: the winner walks to the crown, lifts it, puts it on, celebrates, then holds."""
    s = 12
    cx, cy = 360, 1200
    body = (f'<div class="stack" style="top:300px"><span class="lab" id="{pid}lab">the winner</span>'
            f'<span class="h1" id="{pid}tt" style="margin-top:12px">1 <span class="acc">left</span></span></div>'
            f'<i class="pedestal" id="{pid}pd" style="left:690px;top:1180px"></i>'
            f'<img class="pxi abs" id="{pid}cr" src="{PX}/crown.png" style="left:690px;top:1060px;width:168px;height:120px">'
            + ag(f"{pid}a", "plain", cx, cy, s, eyes="open", alt=("happy",))
            + "".join(f'<i class="spark" id="{pid}sp{k}" style="left:{cx + 150}px;top:{cy - 190}px"></i>' for k in range(10)))
    sc = scene(pid, start, end, body)
    head_in(pid, sc)
    rise(f"#{pid}pd", sc + 0.05, 30)
    pop(f"#{pid}cr", sc + 0.15, 0.6, -20, 0.35)
    rise(f"#{pid}a", sc + 0.05, 40)
    idle(f"{pid}a", "plain", s, sc + 0.3, end)
    walk = sc + 0.35
    kf(f"#{pid}a", walk, [{"x": 60, "duration": 0.2, "ease": "steps(2)"}, {"x": 120, "duration": 0.2, "ease": "steps(2)"}, {"x": 150, "duration": 0.15, "ease": "steps(1)"}])
    # the crown goes from the pedestal up and onto its head (crown box: 9..23 x 10..20 of the canvas)
    hx = cx + 150 - 16 * s + 9 * s
    hy = cy - 23 * s + 10 * s
    lift = walk + 0.6
    kf(f"#{pid}cr", lift, [{"x": (hx - 690) / 2, "y": -230, "duration": 0.3, "ease": "power2.out"},
                           {"x": hx - 690, "y": hy - 1060, "duration": 0.28, "ease": "power2.in"}])
    sfx.append(("maximize_002", lift, 0.22))
    on = lift + 0.6
    sfx.append(("confirmation_002", on, 0.32))
    eyes_to(f"{pid}a", 1, on)
    for sel, base in ((f"#{pid}a", 0), (f"#{pid}cr", hy - 1060)):
        kf(sel, on + 0.05, [{"y": base - 70, "duration": 0.16, "ease": "power2.out"}, {"y": base, "duration": 0.16, "ease": "power2.in"},
                            {"y": base - 50, "duration": 0.14, "ease": "power2.out"}, {"y": base, "duration": 0.14, "ease": "power2.in"}])
    for k in range(10):
        ang = k / 10 * math.tau
        ft(f"#{pid}sp{k}", on + 0.05, {"opacity": 1, "x": 0, "y": 0, "scale": 1}, {"opacity": 0, "x": math.cos(ang) * 230, "y": math.sin(ang) * 200 - 40, "scale": 0.5}, 0.7, "power2.out")
    to(f"#{pid}tt", on, {"opacity": 0, "y": -20}, 0.25)
    setnum(f"#{pid}lab", on, "1 left · the winner")


def ov_hard(i_say, i_extremely, i_task, end, oid="ohard"):
    segs = "".join(f'<i class="hs" id="{oid}s{k}"></i>' for k in range(5))
    body = (f'<div class="chip wide" id="{oid}c" style="left:150px;top:1440px;width:780px"><span>difficult task</span><span class="hb">{segs}</span></div>'
            + ag(f"{oid}a", "sleuth", 540, 1730, 6.5))
    overlay(oid, t(i_say), end, body)
    pop(f"#{oid}c", t(i_say) + 0.05, 0.6, 30, snd="pluck_002")
    rise(f"#{oid}a", t(i_say) + 0.15, 40)
    idle(f"{oid}a", "sleuth", 6.5, t(i_say), end)
    for k in range(5):
        ft(f"#{oid}s{k}", t(i_extremely) + k * 0.16, {"scaleY": 0.2, "backgroundColor": "rgba(22,21,19,.14)"}, {"scaleY": 1, "backgroundColor": CORAL}, 0.18, "back.out(2)", False)
        sfx.append(("tick_001", t(i_extremely) + k * 0.16, 0.18))
    kf(f"#{oid}c", t(i_task), [{"rotation": -2, "duration": 0.06}, {"rotation": 2, "duration": 0.06}, {"rotation": 0, "duration": 0.06}])


ZK = ["coffee", "wizard", "coder", "chef", "music"]


def pg_zoom(start, i_thousand, i_million, end, pid="pz"):
    """The camera pulls back from a handful of agents to an ocean of a million (one tiled sprite field)."""
    s0 = 8  # one tile cell = 256 px at zoom 1; the 9x9 tile is centred on the page
    near = "".join(f'<i class="zc" style="left:{540 + dx * 256 - 128}px;top:{960 - 128}px"></i>' + ag(f"{pid}a{k}", ZK[k], 540 + dx * 256, 960 - 128 + 23 * s0, s0)
                   for k, dx in enumerate((-2, -1, 0, 1, 2)))
    body = f'<div class="field2" id="{pid}f"></div><div class="zwrap" id="{pid}z">{near}</div>' + chip_count(pid + "k", 230, "agents", "100").replace('class="cnt"', 'class="cnt big"')
    sc = scene(pid, start, end, body)
    for k in range(5):
        idle(f"{pid}a{k}", ZK[k], s0, sc, end)
    rise(f"#{pid}k", sc + 0.1, 20)
    tt, tm = t(i_thousand), t(i_million)
    js.append(f"zoomTo('#{pid}', 1, 0.6, {sc:.3f}, {max(0.4, tt - sc - 0.2):.3f}, 'sine.inOut');")
    js.append(f"zoomTo('#{pid}', 0.6, 0.1, {tt - 0.15:.3f}, 0.9, 'power3.inOut');")
    count(f"#{pid}kn", tt - 0.15, 100, 1000, 0.6)
    js.append(f"zoomTo('#{pid}', 0.1, 0.004, {tm - 0.15:.3f}, {max(0.8, end - tm - 0.3):.3f}, 'power2.inOut');")
    count(f"#{pid}kn", tm - 0.15, 1000, 1000000, max(0.8, end - tm - 0.5), "power2.inOut")
    sfx.append(("riser", tm - 0.9, 0.2))
    sfx.append(("boom", tm + 0.2, 0.16))


BOARD = [("plain", 42, "7–0", 1.0), ("wizard", 71, "6–1", 0.86), ("rocket", 96, "5–1", 0.74), ("sleuth", 80, "5–1", 0.7),
         ("coder", 23, "4–1", 0.6), ("coffee", 50, "4–1", 0.55), ("chef", 61, "3–1", 0.46)]


def pg_board(start, i_full, end, pid="pl"):
    rows = []
    for k, (kind, num, rec, sc_) in enumerate(BOARD):
        y = 600 + k * 140
        rows.append(f'<div class="row lb{" first" if k == 0 else ""}" id="{pid}r{k}" style="top:{y}px"><span class="rk">{k + 1}</span><span class="lg"></span>'
                    f'<span class="nm">agent {num}</span><span class="sb"><i id="{pid}sb{k}" style="width:{int(sc_ * 100)}%"></i></span><span class="rc">{rec}</span></div>'
                    + ag(f"{pid}a{k}", kind, 205, y + 76, 4.0, crown=k == 0, eyes="happy" if k == 0 else None, z=2))
    body = head(pid, "when the winner has won", 'leader<span class="acc">board</span>', 200) + "".join(rows)
    s = scene(pid, start, end, body)
    rise(f"#{pid}lab", s + 0.1, 20)
    mask_up(f"#{pid}tt", s + 0.2)
    a = max(s + 0.3, t(i_full) - 0.2)
    for j, k in enumerate([6, 5, 4, 3, 2, 1, 0]):
        ft(f"#{pid}r{k}", a + j * 0.14, {"opacity": 0, "x": -80}, {"opacity": 1, "x": 0}, 0.45, "power3.out")
        ft(f"#{pid}a{k}", a + j * 0.14 + 0.05, {"opacity": 0, "y": -40}, {"opacity": 1, "y": 0}, 0.45, "bounce.out")
        ft(f"#{pid}sb{k}", a + j * 0.14 + 0.1, {"scaleX": 0}, {"scaleX": 1}, 0.5, "power3.out")
        idle(f"{pid}a{k}", BOARD[k][0], 4.0, a + j * 0.14 + 0.5, end)
        sfx.append(("tick_001", a + j * 0.14, 0.16))
    kf(f"#{pid}r0", a + 7 * 0.14 + 0.1, [{"scale": 1.04, "duration": 0.14}, {"scale": 1, "duration": 0.14}])


def ov_why(i_why, i_won, end, oid="owhy"):
    body = (f'<div class="card ans abs" id="{oid}c" style="left:70px;top:1380px;width:940px;height:260px">'
            f'<span class="lab coral" style="position:absolute;left:210px;top:40px">why agent 42 won</span>'
            f'{bars(oid + "b", [600, 480], 210, 110, 50, 18)}<div class="tick" id="{oid}tk">✓</div></div>'
            + ag(f"{oid}a", "plain", 150, 1560, 4.2, eyes="happy", crown=True, z=6))
    overlay(oid, t(i_why) - 0.15, end, body)
    rise(f"#{oid}c", t(i_why) - 0.1, 50)
    rise(f"#{oid}a", t(i_why), 30)
    idle(f"{oid}a", "plain", 4.2, t(i_why), end)
    for k in range(2):
        wipe(f"#{oid}b{k}", t(i_why) + 0.2 + k * 0.12, 0.35)
    pop(f"#{oid}tk", t(i_won), 0.3, 0, 0.3, snd="confirmation_002")


def ov_lost(i_why, i_lost, end, oid="olost"):
    parts = []
    for k, (kind, n) in enumerate((("wizard", 71), ("rocket", 96), ("coder", 23))):
        y = 1360 + k * 130
        parts.append(f'<div class="chip lost" id="{oid}{k}" style="left:{180 + k * 40}px;top:{y}px;padding-left:120px"><span>agent {n}</span><b>✕</b></div>')
        parts.append(ag(f"{oid}a{k}", kind, 240 + k * 40, y + 50, 2.8, eyes="ko", z=6))
    overlay(oid, t(i_why) - 0.15, end, "".join(parts) + f'<div class="tag" id="{oid}t" style="left:660px;top:1290px">why it lost</div>')
    for k in range(3):
        pop(f"#{oid}{k}", t(i_why) + k * 0.2, 0.6, 20, 0.32, snd="pluck_001")
        pop(f"#{oid}a{k}", t(i_why) + k * 0.2 + 0.05, 0.4, 20, 0.32)
    pop(f"#{oid}t", t(i_lost) - 0.1, 0.4, 0, 0.3)


def pg_champ(start, i_one, i_won, i_tour, end, pid="pc"):
    s = 12
    body = (f'<div class="stack" style="top:250px"><span class="lab" id="{pid}lab">tournament winner</span></div>'
            + ag(f"{pid}a", "plain", 540, 700, s, eyes="happy", crown=True)
            + "".join(f'<i class="spark" id="{pid}sp{k}" style="left:540px;top:560px"></i>' for k in range(10))
            + f'<div class="stack" style="top:860px"><span class="h1 ink" id="{pid}nm">agent 42</span><span class="h2 coral" id="{pid}rc" style="margin-top:8px">7–0</span></div>'
            f'<div class="card abs" id="{pid}c" style="left:120px;top:1170px;width:840px;height:380px">'
            f'<span class="lab coral" style="position:absolute;left:44px;top:34px">why it won</span>'
            + "".join(f'<div class="tick sm" id="{pid}t{k}" style="left:44px;top:{100 + k * 84}px">✓</div><i class="bar" id="{pid}b{k}" style="left:120px;top:{116 + k * 84}px;width:{[620, 560, 600][k]}px;height:18px"></i>' for k in range(3))
            + '</div>')
    sc = scene(pid, start, end, body)
    rise(f"#{pid}lab", sc + 0.1, 20)
    ft(f"#{pid}a", sc + 0.05, {"opacity": 0, "y": 80}, {"opacity": 1, "y": 0}, 0.5, "back.out(1.6)")
    idle(f"{pid}a", "plain", s, sc + 0.6, end)
    for k in range(10):
        ang = k / 10 * math.tau
        ft(f"#{pid}sp{k}", sc + 0.4, {"opacity": 1, "x": 0, "y": 0}, {"opacity": 0, "x": math.cos(ang) * 260, "y": math.sin(ang) * 200, "scale": 0.5}, 0.7, "power2.out")
    mask_up(f"#{pid}nm", max(sc + 0.2, t(i_one) - 0.15))
    rise(f"#{pid}c", sc + 0.3, 50)
    for k, i in enumerate((i_one, i_won, i_tour)):
        pop(f"#{pid}t{k}", t(i), 0.3, 0, 0.3, snd="pluck_002")
        wipe(f"#{pid}b{k}", t(i) + 0.05, 0.35)
    pop(f"#{pid}rc", t(i_won), 0.5, 10, 0.35)
    kf(f"#{pid}a", t(i_tour), [{"y": -50, "duration": 0.15}, {"y": 0, "duration": 0.15}])
    sfx.append(("confirmation_002", t(i_tour), 0.28))


def ov_cta(i_learn, i_ai, i_leave, i_follow, end, oid="octa"):
    body = (f'<div class="tag big" id="{oid}t" style="left:250px;top:1380px;transform:rotate(-4deg)">ALL THINGS AI</div>'
            f'<div class="follow" id="{oid}f" style="left:380px;top:1580px"><span>{mark(54)}</span><b>Follow</b></div>'
            + ag(f"{oid}a", "plain", 210, 1670, 6, eyes="happy") + f'<div class="cursor" id="{oid}cur">{CUR}</div>')
    overlay(oid, t(i_learn) - 0.1, end, body)
    pop(f"#{oid}t", t(i_ai) - 0.1, 0.4, 30, snd="pluck_002")
    pop(f"#{oid}f", t(i_leave) - 0.1, 0.5, 40)
    rise(f"#{oid}a", t(i_leave), 40)
    idle(f"{oid}a", "plain", 6, t(i_leave), end)
    kf(f"#{oid}a .in", t(i_leave) + 0.3, [{"rotation": -8, "duration": 0.15}, {"rotation": 8, "duration": 0.15}, {"rotation": 0, "duration": 0.15}], 2)
    # the cursor tip (14, 8 of a 72 px box) lands on the button centre (380 + 250, 1580 + 55)
    ft(f"#{oid}cur", t(i_follow) - 0.55, {"x": 960, "y": 1860, "opacity": 0}, {"x": 630 - 14, "y": 1635 - 8, "opacity": 1}, 0.5, "power3.out")
    kf(f"#{oid}cur", t(i_follow), [{"scale": 0.8, "duration": 0.08}, {"scale": 1, "duration": 0.08}])
    kf(f"#{oid}f", t(i_follow), [{"scale": 0.95, "backgroundColor": INK, "duration": 0.1}, {"scale": 1, "duration": 0.1}])
    setnum(f"#{oid}f b", t(i_follow) + 0.1, "Following")
    sfx.append(("click_002", t(i_follow), 0.5))


# ---------------------------------------------------------------- V2-only treatments
def ov_best(i_battle, i_best, end, oid="obest"):
    """Eight armed agents fight on his chest band until one is left with the best answer."""
    s = 6
    parts, cells = [], []
    for k in range(8):
        cx = 80 + k * 132
        wpn = "sword" if k % 2 == 0 else "gun"
        parts.append(ag(f"{oid}m{k}", "plain", cx, 1560, s, eyes="angry", weapon=wpn, flip=k % 2 == 1, alt=("ko",), poof=True, flash=wpn == "gun"))
        cells.append(dict(id=f"{oid}m{k}", r=0, c=k, cx=cx, cy=1560, kind="plain", wpn=wpn))
    body = "".join(parts) + f'<div class="chip y" id="{oid}c" style="left:290px;top:1690px">best possible answer</div>'
    overlay(oid, t(i_battle) - 0.15, end, body)
    for k in range(8):
        pop(f"#{oid}m{k}", t(i_battle) - 0.1 + k * 0.04, 0.3, 20, 0.3)
        idle(f"{oid}m{k}", "plain", s, t(i_battle), end)
    battle_rounds(cells, t(i_battle) + 0.5, t(i_best) - 0.5, f"{oid}m4", dash_px=60)
    to(f"#{oid}m4", t(i_best) - 0.1, {"x": 540 - (80 + 4 * 132), "scale": 1.5}, 0.45, "power3.inOut")
    pop(f"#{oid}c", t(i_best), 0.5, 30, snd="confirmation_002")


def pg_sign(start, i_prompt, i_battle, i_hundred, end, pid="ps2"):
    """V2: an agent holds up a sign ('1 question' flips to '1 prompt'), then two armies march in for a full-scale battle."""
    s = 4.5
    army = []
    for side in (0, 1):
        for r in range(3):
            for c in range(4):
                cx = (90 + c * 112 + (r % 2) * 40) if side == 0 else (990 - c * 112 - (r % 2) * 40)
                army.append(ag(f"{pid}m{side}{r}{c}", "plain", cx, 1330 + r * 150, s, eyes="angry", weapon="sword" if side == 0 else "gun", flip=side == 1))
    body = (f'<div class="sign" id="{pid}sg"><span class="h2 ink" id="{pid}q">1 question</span><span class="h2 coral" id="{pid}p">1 prompt</span></div>'
            + ag(f"{pid}a", "reader", 540, 1040, 11) + "".join(army) + chip_count(pid + "k", 1790, "agents", "2"))
    sc = scene(pid, start, end, body)
    rise(f"#{pid}a", sc + 0.05, 80)
    idle(f"{pid}a", "reader", 11, sc + 0.5, end)
    ft(f"#{pid}sg", sc + 0.2, {"opacity": 0, "y": 60, "rotation": -6}, {"opacity": 1, "y": 0, "rotation": -3}, 0.5, "back.out(1.6)")
    kf(f"#{pid}sg", t(i_prompt) - 0.15, [{"rotationX": 90, "duration": 0.15, "ease": "power2.in"}, {"rotationX": 0, "duration": 0.2, "ease": "power2.out"}])
    st(f"#{pid}q", t(i_prompt), {"opacity": 0})
    st(f"#{pid}p", t(i_prompt), {"opacity": 1})
    sfx.append(("switch_001", t(i_prompt), 0.18))
    tb = t(i_battle)
    for sel in (f"#{pid}a", f"#{pid}sg"):
        to(sel, tb - 0.3, {"y": -320, "scale": 0.7}, 0.6, "power3.inOut")
    for side in (0, 1):
        for r in range(3):
            for c in range(4):
                aid = f"{pid}m{side}{r}{c}"
                a = tb + c * 0.06 + r * 0.1
                st(f"#{aid} .wp", sc, {"opacity": 0})
                ft(f"#{aid}", a, {"opacity": 0, "x": -500 if side == 0 else 500}, {"opacity": 1, "x": 0}, 0.6, "power3.out")
                idle(aid, "plain", s, a + 0.6, end)
                arm(aid, a + 0.55)
    rise(f"#{pid}k", tb, 30)
    count(f"#{pid}kn", tb, 2, 100, max(0.6, t(i_hundred) - tb + 0.2))


def ov_bcast(i_give, i_prompt, end, oid="obc"):
    s = 5
    parts = []
    for k in range(8):
        cx = 80 + k * 132
        parts.append(ag(f"{oid}a{k}", CROWD[k], cx, 1650, s, alt=("wide",)))
        parts.append(f'<img class="pxi abs" id="{oid}n{k}" src="{PX}/note.png" style="left:{cx - 24}px;top:{1650 - 23 * s - 6}px;width:48px;height:42px;opacity:0">')
    body = f'<div class="chip y" id="{oid}c" style="left:330px;top:1380px">your prompt</div>' + "".join(parts) + f'<div class="tag" id="{oid}t" style="left:820px;top:1290px">×100</div>'
    overlay(oid, t(i_give) - 0.15, end, body)
    pop(f"#{oid}c", t(i_give), 0.5, 20, snd="pluck_002")
    for k in range(8):
        rise(f"#{oid}a{k}", t(i_give) + k * 0.04, 40)
        idle(f"{oid}a{k}", CROWD[k], s, t(i_give), end)
        a = t(i_prompt) - 0.25 + k * 0.08
        ft(f"#{oid}n{k}", a, {"opacity": 0, "y": -140}, {"opacity": 1, "y": 0}, 0.32, "power2.in")
        eyes_to(f"{oid}a{k}", 1, a + 0.3)
    pop(f"#{oid}t", t(i_give) + 0.4, 0.4, 0, 0.3)


def ov_traits(ats, end, oid="otr"):
    pos = [(150, 1430), (930, 1430), (330, 1620), (750, 1620), (150, 1790), (930, 1790)]
    parts = []
    for k, ((kind, lab), (x, y)) in enumerate(zip(PERSONAS, pos)):
        parts.append(ag(f"{oid}a{k}", kind, x, y, 5) + f'<span class="tl" id="{oid}l{k}" style="left:{x - 120}px;top:{y + 40}px">{lab}</span>')
    overlay(oid, ats[0] - 0.15, end, "".join(parts))
    for k in range(6):
        pop(f"#{oid}a{k}", ats[k], 0.3, 30, 0.38, snd="pluck_001" if k % 2 else "pluck_002")
        rise(f"#{oid}l{k}", ats[k] + 0.1, 10)
        idle(f"{oid}a{k}", PERSONAS[k][0], 5, ats[k], end)


def ov_reasons(i_why, i_won, i_lost, end, oid="orsn"):
    body = (f'<div class="chip wide" id="{oid}w" style="left:110px;top:1400px;width:860px;padding-left:140px"><span>agent 42</span><span class="wl coral">WON</span></div>'
            + ag(f"{oid}aw", "plain", 185, 1462, 3, eyes="happy", crown=True, z=6)
            + f'<div class="chip wide lost" id="{oid}l" style="left:110px;top:1580px;width:860px;padding-left:140px"><span>agent 71</span><span class="wl">LOST</span></div>'
            + ag(f"{oid}al", "wizard", 185, 1642, 3, eyes="ko", z=6))
    overlay(oid, t(i_why) - 0.15, end, body)
    pop(f"#{oid}w", t(i_won) - 0.15, 0.6, 30, snd="pluck_002")
    pop(f"#{oid}aw", t(i_won) - 0.1, 0.4, 20, 0.3)
    pop(f"#{oid}l", t(i_lost) - 0.15, 0.6, 30, snd="pluck_001")
    pop(f"#{oid}al", t(i_lost) - 0.1, 0.4, 20, 0.3)


# ---------------------------------------------------------------- the edit
if N == 1:
    ov_bad(T("bad"), w("stop"), T("give it 100") - 0.1)
    pg_crowd(T("give it 100") - 0.05, w("100"), w("battle"), w("death"), TE("death") + 0.35)
    pg_arena(T("called") - 0.1, TE("arena") + 0.85)
    ov_free(T("free"), T("turns") - 0.05)
    pg_split(T("turns") - 0.05, w("question"), w("prompt", T("turns")), w("battle", T("turns")), w("hundred", T("turns")), TE("agents", T("different")) + 0.4)
    ov_task(w("any task"), w("claude", T("any task")), T("type") - 0.1)
    pg_type(T("type") - 0.1, w("any task"), w("claude", T("any task")), w("type"), w("slash"), w("arena", T("slash")), w("end of it"), TE("of it") + 0.45, prefill=True)
    pg_broadcast(T("give all 100") - 0.15, w("initial prompt") + 1, TE("initial prompt") + 0.45)
    ov_march(T("then all 100"), w("battlefield"), T("start battling") - 0.1)
    pg_battle(T("start battling") - 0.1, w("battling"), w("comes out on top") + 3, w("best answer"), TE("for you") + 0.4)
    pg_personas(T("personality") - 0.3, [T("personality") - 0.15, T("personality") + 0.1, T("personality") + 0.35, T("its own way"), T("way"), T("of thinking")], TE("thinking") + 0.4)
    ov_answers(w("every answer"), w("all 100", T("every answer")), w("come out"), w("slightly different"), TE("the rest") + 0.25)
    pg_bracket_pair(T("then they're") - 0.05, w("bracket"), w("tournament"), TE("tournament") + 0.35)
    ov_vs(w("attacking"), w("each other's"), w("answers", T("attacking")), TE("answers", T("attacking")) + 0.35)
    pg_judge(T("knock out") - 0.35, [T("loser"), T("single"), T("until you're")], T("left with"), T("one winner") - 0.1)
    pg_crown(T("one winner") - 0.15, T("say", T("winner")) + 0.75)
    ov_hard(w("let's say"), w("extremely"), w("task", T("difficult")), T("you could even") - 0.05)
    pg_zoom(T("you could even") - 0.05, w("thousand"), w("million"), T("when the winner") + 0.75)
    ov_crowned(w("when the winner"), T("full leaderboard") - 0.3)
    pg_board(T("full leaderboard") - 0.3, w("full leaderboard"), TE("well", T("as")) + 0.4)
    ov_why(w("exactly why"), w("won", T("exactly why")), T("why each agent lost") - 0.05)
    ov_lost(w("why each agent lost"), w("lost"), T("and why that") - 0.05)
    pg_champ(T("and why that") - 0.05, w("one agent", T("and why that")), w("won the tournament"), w("tournament", T("won the")), TE("tournament", T("won the")) + 0.4)
    ov_cta(w("if you want to learn"), w("things ai"), w("leave me"), w("follow"), AROLL_END)
else:
    pg_crowd(0.0, w("a hundred agents"), None, None, TE("different answers") + 0.4, pid="ph",
             title=("stop asking one ai", '<span class="num" id="phn">1</span> agent<span id="phs">s</span>'), opened=True)
    ov_best(w("all battle"), w("best possible"), TE("can get") + 0.2)
    pg_arena(T("called") - 0.1, TE("arena") + 0.9, drop="side")
    ov_free(T("free"), T("turns") - 0.05)
    pg_sign(T("turns") - 0.05, w("prompt", T("turns")), w("battle", T("turns")), w("hundred", T("turns")), TE("agents", T("different")) + 0.4)
    ov_task(w("any task"), w("claude", T("any task")), T("type") - 0.1)
    pg_type(T("type") - 0.1, w("any task"), w("claude", T("any task")), w("type"), w("slash"), w("arena", T("slash")), w("after it"), TE("after it") + 0.45, prefill=True)
    ov_bcast(w("give all 100"), w("initial prompt") + 1, TE("initial prompt") + 0.3)
    ov_traits([T("every agent"), T("agent", T("every")) + 0.2, T("own"), T("personality"), T("its own way"), T("thinking")], TE("thinking") + 0.3)
    pg_bracket_pair(T("then they're") - 0.05, w("bracket"), w("tournament"), TE("tournament") + 0.2)
    pg_vs_magic(T("and they're gonna start") - 0.05, w("attacking"), w("each other's"), w("answers", T("attacking")), T("answers", T("attacking")) + 0.55)
    pg_judge(T("knock out") - 0.15, [T("loser"), T("single"), T("until you're")], T("left with"), T("one winner") - 0.1)
    pg_crown(T("one winner") - 0.15, T("it's actually") - 0.1)
    pg_board(T("full leaderboard") - 0.3, w("full leaderboard"), TE("well", T("as")) + 0.45)
    ov_reasons(w("exactly why"), w("won", T("exactly why")), w("lost"), TE("lost") + 0.3)
    ov_cta(w("if you want to learn"), w("things ai"), w("leave me"), w("follow"), AROLL_END)

# ---------------------------------------------------------------- page windows (crossfade back to his face, dissolve page to page)
scenes.sort(key=lambda x: x[1])
handoff = set()
for k in range(len(scenes) - 1):
    sid, a, b_end, body = scenes[k]
    nid, na, nb, nbody = scenes[k + 1]
    if na <= b_end + 1.0:  # never show his face for under a second between two pages
        scenes[k][2] = max(b_end, na + 0.4)
        handoff.add(sid)
for sid, a, b_end, _ in scenes:
    if b_end >= AROLL_END - 0.01 or sid in handoff:
        continue
    js.append(f"tl.fromTo('#{sid}', {{opacity:1}}, {{opacity:0, duration:.42, ease:'sine.inOut', immediateRender:false}}, {b_end - 0.42:.3f});")
WIN = [(a, b) for _, a, b, _ in scenes]


def covered(x, pad=0.0):
    return any(a - pad <= x < b + pad for a, b in WIN)


overlays = [(o, a, b, body) for o, a, b, body in overlays if not covered((a + b) / 2)]


# ---------------------------------------------------------------- captions (above his head; off while a page covers him)
def groups():
    out_, cur = [], []
    for i in range(len(TOK)):
        if cur:
            gap = t(i) - te(cur[-1])
            chars = sum(len(TOK[j]["text"]) + 1 for j in cur) + len(TOK[i]["text"])
            cut_between = any(t(cur[-1]) < c <= t(i) for c in CUTS)
            if len(cur) >= 3 or chars > 16 or gap > 0.3 or cut_between or TOK[cur[-1]]["text"][-1] in ",.?!" or covered(t(i)) != covered(t(cur[-1])):
                out_.append(cur)
                cur = []
        cur.append(i)
    if cur:
        out_.append(cur)
    return out_


cap_html, cap_js = [], []
for gi, g in enumerate(groups()):
    g_start = t(g[0]) - 0.06
    end = min(te(g[-1]) + 0.35, t(g[-1] + 1) - 0.04 if g[-1] + 1 < len(TOK) else AROLL_END)
    if covered(t(g[0]) + 0.02):
        continue
    nxt_page = min([a for a, _ in WIN if a > g_start] + [1e9])
    end = min(end, nxt_page + 0.02)
    if end - g_start < 0.1:
        continue
    spans = "".join(f'<span class="w{" em" if norm(TOK[i]["text"]) in EMPH else ""}" id="w{i}">{esc(TOK[i]["text"].rstrip(",.") if TOK[i]["text"][-1] in ",." else TOK[i]["text"])}</span>' for i in g)
    cap_html.append(f'<div class="cap clip" id="cap{gi}" data-start="{g_start:.3f}" data-duration="{end - g_start:.3f}" data-track-index="2"><div class="capi">{spans}</div></div>')
    for i in g:
        a = max(g_start, t(i) - 0.05)
        cap_js.append(f"tl.fromTo('#w{i}', {{opacity:0, y:26, scale:.9}}, {{opacity:1, y:0, scale:1, duration:.16, ease:'back.out(2)'}}, {a:.3f});")
        if norm(TOK[i]["text"]) in EMPH:
            cap_js.append(f"tl.fromTo('#w{i}', {{backgroundColor:'rgba(217,119,87,0)'}}, {{backgroundColor:'rgba(217,119,87,1)', duration:.1}}, {a + 0.02:.3f});")
    cap_js.append(f"tl.to('#cap{gi} .capi', {{opacity:0, y:-12, duration:.1, ease:'power1.in', immediateRender:false}}, {end - 0.1:.3f});")

# ---------------------------------------------------------------- camera: hook slam on his first face shot, punch-ins at every cut, slow push between
FACES = []
for line in open(f"{D}/faces-2fps.txt"):
    p = line.split()
    if len(p) == 5:
        FACES.append((int(p[0][1:5]) / 2 - 0.5 + 0.25, *map(float, p[1:])))
cam_js = []
bounds = [0.0] + CUTS + [AROLL_END]
first_face = next((a for a in bounds[:-1] if not covered(a + 0.05)), 0.0)
for k in range(len(bounds) - 1):
    a, b = bounds[k], bounds[k + 1]
    win = [f for f in FACES if a <= f[0] < b] or [min(FACES, key=lambda f: abs(f[0] - a))]
    cx = sum(f[1] + f[3] / 2 for f in win) / len(win)
    cy = sum(f[2] + f[4] / 2 for f in win) / len(win)
    z = 1.0 if k % 2 == 0 else 1.12
    org = f"{int(cx * 1080)}px {int(cy * 1920)}px"
    if a == first_face:
        cam_js.append(f"tl.fromTo('#cam', {{scale:1.35, transformOrigin:'{org}'}}, {{scale:1, duration:.5, ease:'expo.out', immediateRender:{'true' if a == 0 else 'false'}}}, {a:.3f});")
        cam_js.append(f"tl.to('#cam', {{scale:1.03, duration:{max(0.1, b - a - 0.5):.3f}, ease:'none', immediateRender:false}}, {a + 0.5:.3f});")
        continue
    cam_js.append(f"tl.fromTo('#cam', {{scale:{z}, transformOrigin:'{org}'}}, {{scale:{z * 1.03:.4f}, duration:{b - a:.3f}, ease:'none', immediateRender:false}}, {a:.3f});")
    if not covered(a + 0.02):
        cam_js.append(f"focus({a:.3f});")
sfx.append(("boom", 0.0, 0.2))

# ---------------------------------------------------------------- assemble
sfx = [x for x in sfx if x[1] < DURATION - 0.1]
heard, kept = {}, []
for x in sorted(sfx, key=lambda x: x[1]):  # never the same effect again and again: one per family every 3 s
    fam = re.sub(r"_\d+$", "", x[0])
    if x[1] - heard.get(fam, -9) >= 3.0:
        heard[fam] = x[1]
        kept.append(x)
sfx = kept
sfx_html = "\n".join(f'<audio id="sfx{n}" src="assets/audio/sfx/{name}.wav" data-start="{max(0.0, at):.3f}" data-track-index="{30 + n}" data-volume="{vol}"></audio>'
                     for n, (name, at, vol) in enumerate(sorted(sfx, key=lambda x: x[1])))
scene_html = "\n".join(f"""<section class="scene clip" id="{sid}" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="3">
 <div class="sheet"><div class="content">{body}</div></div>
</section>""" for sid, a, b, body in scenes)
ov_html = "\n".join(f'<div class="ov clip" id="{o}" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="4">{body}</div>' for o, a, b, body in overlays)
page = open("edit/template.html").read()
page = (page.replace("{{DURATION}}", f"{DURATION:.3f}").replace("{{AROLL_END}}", f"{AROLL_END:.3f}").replace("{{AROLL}}", f"assets/video/aroll-t{N}.mp4")
        .replace("{{OVERLAYS}}", ov_html).replace("{{SCENES}}", scene_html).replace("{{VIDEOS}}", "").replace("{{CAPTIONS}}", "\n".join(cap_html))
        .replace("{{SFX}}", sfx_html).replace("{{JS}}", "\n".join(cam_js + js + cap_js)))
out_path = f"../{os.path.basename(os.getcwd())}-trials/out/trial-{N}.html"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
open(out_path, "w").write(page)
open("index.html", "w").write(page) if N == 1 else None
print(f"trial {N}: {len(scenes)} pages, {len(overlays)} overlays, {len(cap_html)} caption groups, {len(sfx)} sfx, {DURATION:.2f}s, {len(page) // 1024} KB")
for sid, a, b, _ in scenes:
    print(f"  {sid:4s} {a:6.2f} – {b:6.2f}  ({b - a:.2f}s)")
for o, a, b, _ in overlays:
    print(f"  ov {o:7s} {a:6.2f} – {b:6.2f}")
