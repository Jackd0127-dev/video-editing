"""Split segments at pauses inside a line (>= 0.26 s below -42 dB) so no dead air survives. Usage: tighten.py segments.json"""
import json, math, struct, subprocess, sys
p = sys.argv[1]; d = json.load(open(p)); env = {}
def E(path):
    if path not in env:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-map", "0:a:0", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout
        x = struct.unpack(f"{len(raw)//4}f", raw)
        env[path] = [20 * math.log10(math.sqrt(sum(v * v for v in x[i:i + 160]) / 160) + 1e-9) for i in range(0, len(x) - 160, 160)]
    return env[path]
out = []
for key, a, b, lab in d["segments"]:
    e = E(d["sources"][key]); i = int(a * 100) + 6; runs = []; st = None
    while i < int(b * 100) - 6:
        if e[i] < -42: st = i if st is None else st
        else:
            if st is not None and i - st >= 26: runs.append((st / 100, i / 100))
            st = None
        i += 1
    cur = a; parts = []
    for g0, g1 in runs:
        if g0 - cur < 0.15: cur = g1 - 0.03; continue
        parts.append([cur, g0 + 0.07]); cur = g1 - 0.07
    parts.append([cur, b])
    for n, (x, y) in enumerate(parts):
        out.append([key, round(x, 3), round(y, 3), lab + (f" ({n + 1})" if len(parts) > 1 else "")])
d["segments"] = out; json.dump(d, open(p, "w"), indent=1)
print(f"{len(out)} segments, {sum(y - x for _, x, y, _ in out):.1f}s")
