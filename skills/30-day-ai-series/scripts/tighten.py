"""Tighten a multi-take cut (Day 14 note: "so many blank spots … empty sound space … start or end or middle"): every quiet run
inside a kept line longer than MIN_GAP is cut down to ~0.1 s, and each line's head and tail are trimmed to the speech.

Usage: python3 -I <skill>/scripts/tighten.py edit/trials/<n>/segments.json   (rewrites it; the loose version is kept as segments-loose.json)
Then cut_multi.py, then  python3 -I <skill>/scripts/tighten.py --words edit/trials/<n>   to map every word through the sub-segments.
Quiet = 10 ms RMS under QUIET dB (his room floor sits near -60, breaths near -40, speech -10…-30).
"""
import json
import math
import os
import shutil
import struct
import subprocess
import sys

QUIET, MIN_GAP = -42, 0.18
KEEP_AFTER, KEEP_BEFORE = 0.07, 0.05  # silence left after a word ends / before the next one starts
HEAD, TAIL = 0.05, 0.09
MIN_PIECE = 0.45
CACHE = {}


def energy(src):
    if src not in CACHE:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-map", "0:a:0", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
        x = struct.unpack(f"{len(raw) // 4}f", raw)
        CACHE[src] = [20 * math.log10(math.sqrt(sum(v * v for v in x[i:i + 160]) / 160) + 1e-9) for i in range(0, len(x) - 160, 160)]
    return CACHE[src]


def tighten(path):
    d = json.load(open(path))
    loose = path.replace("segments.json", "segments-loose.json")
    if not os.path.exists(loose):
        shutil.copy(path, loose)
    d = json.load(open(loose))
    out = []
    for g, (key, a, b, lab) in enumerate(d["segments"]):
        e = energy(d["sources"][key])
        k0, k1 = int(a * 100), min(int(b * 100), len(e))
        loud = [k for k in range(k0, k1) if e[k] >= QUIET]
        if not loud:
            continue
        a2 = max(a, loud[0] / 100 - HEAD)
        b2 = min(b, (loud[-1] + 1) / 100 + TAIL)
        pieces, start = [], a2
        k = int(a2 * 100)
        while k < int(b2 * 100):
            if e[k] < QUIET:
                j = k
                while j < int(b2 * 100) and e[j] < QUIET:
                    j += 1
                if (j - k) / 100 >= MIN_GAP and j < int(b2 * 100):
                    pieces.append([key, round(start, 3), round(k / 100 + KEEP_AFTER, 3), f"{lab} [{g}]"])
                    start = j / 100 - KEEP_BEFORE
                k = j
            else:
                k += 1
        pieces.append([key, round(start, 3), round(b2, 3), f"{lab} [{g}]"])
        k = 0
        while k < len(pieces) and len(pieces) > 1:  # no sliver shots: a piece under MIN_PIECE reads as another clip flashing in (Day 14, 2:05)
            if pieces[k][2] - pieces[k][1] < MIN_PIECE:
                if k + 1 < len(pieces):
                    pieces[k + 1][1] = pieces[k][1]
                else:
                    pieces[k - 1][2] = pieces[k][2]
                del pieces[k]
            else:
                k += 1
        out += pieces
    d["segments"] = out
    json.dump(d, open(path, "w"), indent=1)
    lo = json.load(open(loose))["segments"]
    print(f"{len(lo)} lines -> {len(out)} pieces; {sum(s[2] - s[1] for s in lo):.2f}s -> {sum(s[2] - s[1] for s in out):.2f}s")


def words(tdir):
    """Map every word of the loose lines through the tight pieces (a word whose Parakeet start fell in a removed pause lands
    on the next piece's first frame), so no caption word is lost."""
    loose = json.load(open(f"{tdir}/segments-loose.json"))
    wj = json.load(open(f"{tdir}/words.json"))
    tx = {k: json.load(open(v)) for k, v in loose["transcripts"].items()}
    pieces = wj["segments"]
    out = []
    for g, (key, a, b, lab) in enumerate(loose["segments"]):
        mine = [p for p in pieces if p["label"].endswith(f"[{g}]")]
        for w in tx[key]:
            s = w["start"]
            if not (a - 0.02 <= s < b - 0.01):
                continue
            p = next((p for p in mine if p["src_in"] - 0.03 <= s < p["src_out"]), None)
            if p is None:
                p = next((p for p in mine if p["src_in"] > s), None)
                if p is not None:
                    s = p["src_in"] + 0.03
                elif mine and s < mine[-1]["src_out"] + 0.3:  # a line's last word whose start Parakeet put past the trimmed tail
                    p = mine[-1]
                    s = p["src_out"] - 0.15
                else:
                    continue
            out.append({"text": w["text"], "start": round(p["start"] + max(s, p["src_in"]) - p["src_in"], 3), "seg": p["index"]})
    wj["words"] = out
    json.dump(wj, open(f"{tdir}/words.json", "w"), indent=1)
    print(f"{len(out)} words mapped")


if __name__ == "__main__":
    if sys.argv[1] == "--words":
        words(sys.argv[2])
    else:
        tighten(sys.argv[1])
