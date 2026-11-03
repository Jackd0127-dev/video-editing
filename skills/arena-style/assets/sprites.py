"""Pixel-art agents for the Arena style, drawn by hand as character grids.

Every character is a stack of same-size layers on a 32x32 canvas (body, eyes, prop, fx) so they line up and animate
separately (bob, blink, prop moves, fx sparkles). Weapons, crown, poof and bullets are their own small sprites.
Writes native-resolution PNGs to assets/img/px/ (plus crowd-tile.png for the zoom-out); the page scales them with
image-rendering: pixelated.
Run from the project root:  python3 edit/sprites.py
"""
import json
import os
from PIL import Image

OUT = "assets/img/px"
PAL = {
    "C": (247, 132, 90), "c": (214, 101, 62), "K": (28, 27, 26), "N": (34, 53, 107), "n": (58, 87, 160),
    "W": (246, 236, 214), "w": (220, 203, 166), "Y": (247, 201, 69), "y": (228, 155, 31), "G": (206, 211, 219),
    "g": (139, 147, 161), "D": (46, 47, 54), "B": (110, 75, 54), "b": (154, 107, 71), "H": (92, 83, 76),
    "h": (124, 112, 103), "R": (217, 72, 59), "L": (160, 190, 235), "P": (255, 255, 255), "S": (22, 21, 19, 46),
}
CW = CH = 32
BX, BY = 8, 18          # body origin on the canvas


def canvas(w=CW, h=CH):
    return [[None] * w for _ in range(h)]


def put(g, x, y, rows):
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch != "." and 0 <= y + j < len(g) and 0 <= x + i < len(g[0]):
                g[y + j][x + i] = ch


def line(g, x0, y0, x1, y1, ch):
    n = max(abs(x1 - x0), abs(y1 - y0))
    for k in range(n + 1):
        g[round(y0 + (y1 - y0) * k / n)][round(x0 + (x1 - x0) * k / n)] = ch


def outline(g):
    h, w = len(g), len(g[0])
    o = [r[:] for r in g]
    for y in range(h):
        for x in range(w):
            if g[y][x] is None and any(0 <= y + dy < h and 0 <= x + dx < w and g[y + dy][x + dx] not in (None, "K")
                                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                o[y][x] = "K"
    return o


def save(g, name):
    h, w = len(g), len(g[0])
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y in range(h):
        for x in range(w):
            if g[y][x]:
                c = PAL[g[y][x]]
                im.putpixel((x, y), c if len(c) == 4 else c + (255,))
    im.save(f"{OUT}/{name}.png")


BODY = ["..CCCCCCCCCCCC..",
        "..CCCCCCCCCCCC..",
        "..CCCCCCCCCCCC..",
        "..CCCCCCCCCCCC..",
        "CCCCCCCCCCCCCCCc",
        "CCCCCCCCCCCCCCCc",
        "..CCCCCCCCCCCC..",
        "..cccccccccccc..",
        "...C.C....C.C...",
        "...c.c....c.c..."]
EYES = {
    "open": [(5, 2), (5, 3), (10, 2), (10, 3)],
    "happy": [(4, 3), (5, 2), (6, 3), (9, 3), (10, 2), (11, 3)],
    "closed": [(4, 3), (5, 3), (10, 3), (11, 3)],
    "angry": [(4, 1), (5, 2), (5, 3), (11, 1), (10, 2), (10, 3)],
    "ko": [(4, 1), (6, 1), (5, 2), (4, 3), (6, 3), (9, 1), (11, 1), (10, 2), (9, 3), (11, 3)],
    "wide": [(5, 2), (6, 2), (5, 3), (6, 3), (9, 2), (10, 2), (9, 3), (10, 3)],
    "wink": [(5, 2), (5, 3), (9, 3), (10, 3), (11, 3)],
}


def body():
    g = canvas()
    put(g, BX, BY, BODY)
    put(g, BX + 1, BY + 10, ["SSSSSSSSSSSSSS"])
    return g


def eyes(kind):
    g = canvas()
    for x, y in EYES[kind]:
        g[BY + y][BX + x] = "K"
    return g


# ---------------------------------------------------------------- personalities: prop (moves with the hand/head) and fx (animated bits)
def coder():
    p, f = canvas(), canvas()
    put(p, 5, 22, ["KKKKKKKKKKKK", "KDDDDDDDDDDK", "KDDDDDDDDDDK", "KDDDDDDDDDDK", "KDDDDDDDDDDK", "KKKKKKKKKKKK"])
    put(p, 3, 28, ["KKKKKKKKKKKKKKKK", ".DDDDDDDDDDDDDD."])
    put(f, 7, 24, ["L.LL.L", "..L.LL"])
    return p, f


def coffee():
    p, f = canvas(), canvas()
    put(p, 1, 21, ["WWWWW..", "WBBBWw.", "WWWWW.w", "WWWWWw.", ".www..."])
    put(f, 2, 15, [".W.", "W..", ".W.", "..W"])
    return outline(p), f


def music():
    p, f = canvas(), canvas()
    put(p, 9, 15, [".NNNNNNNNNNNN.", "N............N", "N............N"])
    put(p, 6, 19, ["NNN", "NnN", "NnN", "NNN"])
    put(p, 23, 19, ["NNN", "NnN", "NnN", "NNN"])
    put(f, 23, 6, [".YY", ".Y.", ".Y.", "YY.", "YY."])
    put(f, 27, 10, [".Y", ".Y", "YY"])
    return p, f


def sky():
    p, f = canvas(), canvas()
    put(p, 0, 0, ["..........NNNNNNNNNNNN..........",
                  ".......NNNNNNNNNNNNNNNNNN.......",
                  ".....NNNNNNWWWWWWWWWWNNNNNN.....",
                  "....NNNNNNWWWWWWWWWWWWNNNNNN....",
                  "...NNNNNNWWWWWWWWWWWWWWNNNNNN...",
                  "...nnn.nnnn.nnnnnnnn.nnnn.nnn..."])
    for x0, x1 in ((4, 8), (11, 12), (20, 19), (27, 23)):
        line(p, x0, 6, x1, 21, "K")
    return p, f


def chef():
    p, f = canvas(), canvas()
    put(p, 10, 9, ["..WWW..WWW..", ".WWWWWWWWWW.", "WWWWWWWWWWWW", "WWWWWWWWWWWW", ".WWWWWWWWWW.",
                   ".wWWWWWWWWw.", ".wwwwwwwwww.", ".WWWWWWWWWW.", ".WWWWWWWWWW."])
    put(p, 24, 22, ["DDKKKKKK", "...KKKK."])
    put(f, 27, 18, [".Y..", "Y.Y.", "..YY"])
    return p, f


def wizard():
    p, f = canvas(), canvas()
    put(p, 7, 5, ["..........NN......", ".........NNN......", "........NNNN......", "........NNNNN.....",
                  ".......NNNNNN.....", "......NNNNNNNN....", "......NNNNNNNN....", ".....NNNNNNNNNN...",
                  "....WWWWWWWWWWWW..", "....wwwwwwwwwwww..", "NNNNNNNNNNNNNNNNNN", ".nnnnnnnnnnnnnnnn."])
    for k in range(5):
        p[22 - k][24 + k] = "B"
    p[17][29] = "W"
    put(f, 28, 12, [".Y.", "YYY", ".Y."])
    f[10][26] = "Y"
    f[15][31] = "Y"
    return p, f


def reader():
    p, f = canvas(), canvas()
    put(p, 6, 13, ["..WWWWWWwWWWWWWW....", ".WWwwWWWwWWwwWWWW...", "WWWWWWWWwWWWWWWWWW..", "bbbbbbbbbbbbbbbbbb.."])
    return p, f


def sleuth():
    p, f = canvas(), canvas()
    put(p, 8, 12, [".....HHHHHH.....", "...HHhHHHHhHH...", "..HHHHhHHhHHHH..", "..HHHHHHHHHHHH..",
                   "HHHHHHHHHHHHHHHH", ".hhhhhhhhhhhhhh."])
    put(p, 25, 16, [".GGG.", "GWWWG", "GWPWG", "GWWWG", ".GGG."])
    put(p, 24, 21, ["K.", ".K"])
    p[23][23] = "K"
    return p, f


def rocket():
    p, f = canvas(), canvas()
    put(p, 24, 25, [".RRR.", "DDDDD", "DDDDD"])
    put(f, 25, 7, ["..N..", ".NWN.", ".WWW.", ".WnW.", ".WWW.", ".WWW.", "NWWWN", "N.W.N"])
    put(f, 25, 15, [".YyY.", "..Y.."])
    f = outline(f)
    return p, f


KINDS = {"coder": (coder, "open"), "coffee": (coffee, "happy"), "music": (music, "closed"), "sky": (sky, "angry"),
         "chef": (chef, "wink"), "wizard": (wizard, "wink"), "reader": (reader, "closed"), "sleuth": (sleuth, "open"),
         "rocket": (rocket, "open")}

CROWN = ["Y....YY....Y", "YY..YYYY..YY", "YYYYYYYYYYYY", "YYYyYYYYyYYY", "YYYYYYYYYYYY", "yyyyyyyyyyyy", "YRYYYWWYYYRY", "yyyyyyyyyyyy"]
SWORD = ["...Y............", "BB.YGGGGGGGGGGG.", "BBYYgggggggggggG", "...Y............"]
GUN = [".DDDDDDDDDD", "DgggggggDDD", "DDDDDDDD...", ".DDB.......", ".DDB.......", ".DD........"]
WAND = ["BBBBBBBBW", "BBBBBBBB."]
PAN = ["DDDKKKKKKK", "...KKKKKK."]
POOF = ["..WW..WW..", ".WWWWWWWW.", "WWWwWWWwWW", ".WWWWWWWW.", "WWwWWWWwWW", ".WWWWWWWW.", "..WW..WW.."]
FLASH = [".Y.Y.", "YYYYY", ".YYY.", "YYYYY", ".Y.Y."]
NOTE = ["WWWWWW", "WggggW", "WWWWWW", "WgggWW", "WWWWWW"]

def crowd_tile():
    """9x9 mixed agents at native 32 px cells: the tiled field the zoom-out pulls back over."""
    kinds = ["coder", "coffee", "music", "chef", "wizard", "reader", "sleuth", "rocket", None]
    faces = ["open", "happy", "closed", "angry", "wink", "wide"]
    tile = Image.new("RGBA", (9 * CW, 9 * CH), (0, 0, 0, 0))
    for r in range(9):
        for c in range(9):
            k = kinds[(r * 4 + c * 7) % 9]
            layers = ["body", f"eyes-{faces[(r * 5 + c * 3) % 6]}"] + ([f"{k}-prop", f"{k}-fx"] if k else [])
            for layer in layers:
                tile.alpha_composite(Image.open(f"{OUT}/{layer}.png"), (c * CW, r * CH))
    tile.save(f"{OUT}/crowd-tile.png")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    save(body(), "body")
    for k in EYES:
        save(eyes(k), f"eyes-{k}")
    meta = {}
    for name, (fn, eye) in KINDS.items():
        p, f = fn()
        save(p, f"{name}-prop")
        save(f, f"{name}-fx")
        meta[name] = eye
    for name, rows in (("crown", CROWN), ("sword", SWORD), ("gun", GUN), ("wand", WAND), ("pan", PAN), ("poof", POOF),
                       ("flash", FLASH), ("note", NOTE)):
        w = max(len(r) for r in rows)
        g = canvas(w + 2, len(rows) + 2)
        put(g, 1, 1, rows)
        save(outline(g) if name in ("crown", "sword", "gun", "wand", "note") else g, name)
    json.dump(meta, open(f"{OUT}/kinds.json", "w"))
    crowd_tile()
    print("sprites ->", OUT, sorted(os.listdir(OUT)))
