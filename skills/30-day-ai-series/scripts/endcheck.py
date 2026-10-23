"""Flag segment ends that clip the last word ("anything" → "anythi").

Usage: python3 -I endcheck.py SEGMENTS.json [source-key=path ...]
Reads SEGMENTS.json ({"sources": {key: path}, "segments": [[key, in, out, label], ...]}); transcripts come from it or from plan.json next to it.
A cut is suspect when the voice is still loud (> -38 dB) in the 120 ms after the out-point and no new word
starts there (so it isn't just the next word you meant to drop). Fix by moving the out-point to the start of
the next run of >= 150 ms of quiet, then re-cut and listen.
"""
import json
import math
import struct
import subprocess
import sys

cfg = json.load(open(sys.argv[1]))
srcs = dict(cfg["sources"], **dict(a.split("=", 1) for a in sys.argv[2:]))
import os
plan = os.path.join(os.path.dirname(sys.argv[1]) or ".", "plan.json")  # snap.py's output drops the transcripts; read them from plan.json
txs = cfg.get("transcripts") or (json.load(open(plan)).get("transcripts", {}) if os.path.exists(plan) else {})
tx = {k: json.load(open(v)) for k, v in txs.items()}
env = {}


def energy(path):
    if path not in env:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-map", "0:a:0", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout
        x = struct.unpack(f"{len(raw) // 4}f", raw)
        env[path] = [20 * math.log10(math.sqrt(sum(v * v for v in x[i:i + 160]) / 160) + 1e-9) for i in range(0, len(x) - 160, 160)]
    return env[path]


seg = cfg["segments"]
bad = 0
for k, (key, a, b, lab) in enumerate(seg):
    if k + 1 < len(seg) and seg[k + 1][0] == key and abs(seg[k + 1][1] - b) < 0.6:
        continue  # a split of the same line (a pause removed), not a line ending
    E = energy(srcs[key])
    i = int(b * 100)
    loud = max(E[i:i + 12] or [-99])
    next_word = any(b - 0.02 <= w["start"] <= b + 0.15 for w in tx.get(key, []))
    if loud > -38 and not next_word:
        q = i
        while q < len(E) - 15 and not all(v < -44 for v in E[q:q + 15]):
            q += 1
        print(f"CLIPPED? seg {k:2d} out {b:.2f} (voice {loud:.0f} dB after the cut) -> try {q / 100 + 0.05:.2f}  | {lab[:60]}")
        bad += 1
print(f"{bad} suspect ending(s) in {len(seg)} segments")
