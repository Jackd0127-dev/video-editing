"""Snap rough word-based segment boundaries to the quiet just before/after speech.

Usage: python3 -I snap.py PLAN.json OUT.json
PLAN.json: {"sources": {"A": "path.mov", ...}, "transcripts": {"A": "words.json", ...}, "segments": [["A", first_word_start, last_word_start, "label"], ...]}
Writes OUT.json: {"sources": {...}, "segments": [["A", in, out, "label"], ...]} with in/out in source seconds.
In-point: last quiet 10 ms frame (< -45 dB) within 0.35 s before the first word, minus 0.03 s.
Out-point: first run of 5 quiet frames after the last word's start + 0.12 s, plus 0.04 s.
"""
import json
import math
import struct
import subprocess
import sys

plan = json.load(open(sys.argv[1]))
cache = {}


def energy(src):
    if src not in cache:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-map", "0:a:0", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                             capture_output=True, check=True).stdout
        x = struct.unpack(f"{len(raw) // 4}f", raw)
        hop = 160
        cache[src] = [20 * math.log10(math.sqrt(sum(v * v for v in x[i:i + hop]) / hop) + 1e-9) for i in range(0, len(x) - hop, hop)]
    return cache[src]


QUIET = -45
TX = {k: json.load(open(v)) for k, v in plan.get("transcripts", {}).items()}
out = []
for key, w0, w1, label in plan["segments"]:
    e = energy(plan["sources"][key])
    k0 = int(w0 * 100)
    a = None
    for k in range(k0, max(0, k0 - 35), -1):
        if e[k] < QUIET:
            a = k / 100
            break
    a = (a if a is not None else w0 - 0.08) - 0.03
    k = int((w1 + 0.12) * 100)
    b = None
    while k < len(e) - 5 and k < int((w1 + 1.6) * 100):
        if all(v < QUIET for v in e[k:k + 5]):
            b = k / 100 + 0.04
            break
        k += 1
    b = b if b is not None else w1 + 0.6
    if key in TX:  # never run into the next spoken word, never start inside the previous one
        nxt = [w["start"] for w in TX[key] if w["start"] > w1 + 0.05]
        if nxt:
            b = min(b, nxt[0] - 0.03)
        prv = [w["start"] for w in TX[key] if w["start"] < w0 - 0.05]
        if prv:
            a = max(a, prv[-1] + 0.12)
    out.append([key, round(max(0, a), 3), round(b, 3), label])
json.dump({"sources": plan["sources"], "segments": out}, open(sys.argv[2], "w"), indent=1)
for s in out:
    print(f"{s[0]:5s} {s[1]:7.2f} {s[2]:7.2f} ({s[2] - s[1]:.2f}s) {s[3]}")
