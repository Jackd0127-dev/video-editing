"""QA a rendered edit at every cut: picture jumps, audio pops, captions over the face.

Usage (from a project root): python3 -I ../../tools/qa.py RENDER.mp4 [--out DIR]

Reads index.html for paper-scene and caption windows, and edit/words.json for A-roll cut
points. Needs ffmpeg and swift (tools/faces.swift).
  - Jumps: at each visible A-roll cut, compares the face box just before and after. Same
    size with a shifted position reads as a jump cut; a size change reads as a punch-in.
  - Pops: highpass the mix and look for a click spike at each cut versus the local floor.
  - Face cover: samples every caption window, finds the face and checks it stays below
    the caption band.
Writes qa-report.json and cuts-sheet.jpg (before|after pair for every cut) to --out.
"""
import json
import math
import os
import re
import struct
import subprocess
import sys
import tempfile

TOOLS = os.path.dirname(os.path.abspath(__file__))
video = sys.argv[1]
out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "qa"
os.makedirs(out, exist_ok=True)
FPS = 30
CAPTION_BOTTOM = 590 / 1920  # captions are anchored with their bottom edge at y=590

page = open("index.html").read()
scenes = [(float(a), float(a) + float(d)) for a, d in re.findall(r'class="scene clip" id="p\d+" data-start="([\d.]+)" data-duration="([\d.]+)"', page)]
caps = [(float(a), float(a) + float(d)) for a, d in re.findall(r'class="cap clip" id="cap\d+" data-start="([\d.]+)" data-duration="([\d.]+)"', page)]
segs = json.load(open("edit/words.json"))["segments"]


def covered(t):
    return any(a - 0.01 <= t < b for a, b in scenes)


cuts = []
for s in segs[1:]:
    cuts.append({"t": s["start"], "kind": "aroll-cut", "visible": not covered(s["start"])})
for a, b in scenes:
    cuts.append({"t": a, "kind": "to-paper", "visible": True})
    if not any(abs(b - a2) < 0.02 for a2, _ in scenes):
        cuts.append({"t": b, "kind": "to-aroll", "visible": True})
end = float(re.search(r'data-composition-id="main"[^>]*data-duration="([\d.]+)"', page).group(1))
cuts = sorted([c for c in cuts if 0.05 < c["t"] < end - 0.1], key=lambda c: c["t"])

tmp = tempfile.mkdtemp(dir=out)


def frame(t, name):
    path = os.path.join(tmp, name)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(t, 0):.4f}", "-i", video, "-frames:v", "1", "-vf", "scale=540:960", path], check=True)
    return path


def faces(paths):
    d = os.path.join(tmp, "faces")
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        os.remove(os.path.join(d, f))
    for i, p in enumerate(paths):
        os.link(p, os.path.join(d, f"f{i:05d}.png"))
    res = subprocess.run(["swift", os.path.join(TOOLS, "faces.swift"), d], capture_output=True, text=True, check=True).stdout.split("\n")
    boxes = {}
    for line in res:
        p = line.split()
        if len(p) == 5:
            boxes[int(p[0][1:6])] = tuple(map(float, p[1:]))
    return [boxes.get(i) for i in range(len(paths))]


# ---- jumps
pairs = []
for i, c in enumerate(cuts):
    c["before"] = frame(c["t"] - 2 / FPS, f"c{i:03d}a.png")
    c["after"] = frame(c["t"] + 1 / FPS, f"c{i:03d}b.png")
    pairs += [c["before"], c["after"]]
fb = faces(pairs)
for i, c in enumerate(cuts):
    a, b = fb[2 * i], fb[2 * i + 1]
    c["face_before"], c["face_after"] = a, b
    if c["kind"] == "aroll-cut" and c["visible"] and a and b:
        size = b[2] / a[2]
        shift = math.hypot((b[0] + b[2] / 2) - (a[0] + a[2] / 2), (b[1] + b[3] / 2) - (a[1] + a[3] / 2))
        c["size_ratio"], c["shift"] = round(size, 3), round(shift, 3)
        c["jump"] = abs(size - 1) < 0.06 and shift > 0.015

# ---- pops
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-vn", "-ac", "1", "-ar", "48000", "-af", "highpass=f=3500", "-f", "f32le", "-"], capture_output=True, check=True).stdout
n = len(raw) // 4
x = struct.unpack(f"{n}f", raw)
hop = 144  # 3 ms
energy = [math.sqrt(sum(v * v for v in x[k:k + hop]) / hop) + 1e-9 for k in range(0, n - hop, hop)]
sfx_starts = [float(s) for s in re.findall(r'<audio id="sfx\d+" src="[^"]+" data-start="([\d.]+)"', page)]
for c in cuts:
    k = int(c["t"] * 48000 / hop)
    near = energy[max(0, k - 4):k + 5]
    ctx = sorted(energy[max(0, k - 120):k - 10] + energy[k + 10:k + 120])
    floor = ctx[len(ctx) // 2] if ctx else 1e-6
    c["pop_ratio"] = round(max(near) / floor, 1)
    # A transient that coincides with a placed sound effect is the effect, not a click.
    c["sfx_at_cut"] = any(-0.4 <= c["t"] - s <= 0.1 for s in sfx_starts)
    c["pop"] = c["pop_ratio"] > 8 and 20 * math.log10(max(near)) > -45 and not c["sfx_at_cut"]

# ---- clicks in the voice edit itself (before music and effects are mixed in)
voice_pops = []
if os.path.exists("assets/video/aroll.mp4"):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", "assets/video/aroll.mp4", "-vn", "-ac", "1", "-ar", "48000", "-af", "highpass=f=3500", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    v = struct.unpack(f"{len(raw) // 4}f", raw)
    ve = [math.sqrt(sum(s * s for s in v[k:k + hop]) / hop) + 1e-9 for k in range(0, len(v) - hop, hop)]
    for s in segs[1:]:
        k = int(s["start"] * 48000 / hop)
        near = ve[max(0, k - 4):k + 5]
        ctx = sorted(ve[max(0, k - 120):k - 10] + ve[k + 10:k + 120])
        ratio = max(near) / ctx[len(ctx) // 2]
        if ratio > 8 and 20 * math.log10(max(near)) > -45:
            voice_pops.append({"t": s["start"], "ratio": round(ratio, 1)})

# ---- captions vs face
samples = []
for a, b in caps:
    t = a + 0.15
    while t < b - 0.05:
        samples.append(t)
        t += 0.2
sframes = [frame(t, f"s{i:04d}.png") for i, t in enumerate(samples)]
sf = faces(sframes)
cover = []
for t, f in zip(samples, sf):
    if f and f[1] < CAPTION_BOTTOM + 0.01:
        cover.append({"t": round(t, 2), "face_top": round(f[1], 3)})
min_top = min((f[1] for f in sf if f), default=None)

# ---- sheet
rows = []
for i, c in enumerate(cuts):
    rows.append(f"[{2 * i}:v][{2 * i + 1}:v]hstack[r{i}]")
inputs = sum([["-i", c["before"], "-i", c["after"]] for c in cuts], [])
cols = 6
grid = []
for i in range(len(cuts)):
    grid.append(f"[r{i}]scale=360:-2[s{i}]")
pad = (-len(cuts)) % cols
layout = "".join(f"[s{i}]" for i in range(len(cuts)))
fc = ";".join(rows + grid) + f";{layout}xstack=inputs={len(cuts)}:layout=" + "|".join(f"{(i % cols) * 360}_{(i // cols) * 320}" for i in range(len(cuts))) + ":fill=black[o]"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[o]", "-frames:v", "1", "-q:v", "3", os.path.join(out, "cuts-sheet.jpg")], check=True)

report = {
    "cuts": [{k: v for k, v in c.items() if k not in ("before", "after")} for c in cuts],
    "jumps": [c["t"] for c in cuts if c.get("jump")],
    "pops": [{"t": c["t"], "ratio": c["pop_ratio"]} for c in cuts if c.get("pop")],
    "voice_cut_pops": voice_pops,
    "caption_face_overlaps": cover,
    "min_face_top_during_captions": min_top,
    "caption_bottom": CAPTION_BOTTOM,
}
json.dump(report, open(os.path.join(out, "qa-report.json"), "w"), indent=1)
print(f"cuts {len(cuts)} | jumps {len(report['jumps'])} {report['jumps']} | pops {len(report['pops'])} {report['pops']} | voice-cut pops {len(voice_pops)} | "
      f"caption/face overlaps {len(cover)} | min face top {min_top:.3f} vs caption bottom {CAPTION_BOTTOM:.3f}")
