"""Assemble segments from several takes into one A-roll, loudness-matched per source.

Usage: python3 -I cut_multi.py SEGMENTS.json OUT.mov WORDS_OUT.json
SEGMENTS.json: {"sources": {key: path}, "transcripts": {key: words.json}, "segments": [[key, in, out, label], ...]}
- Every source is conformed to 1080x1920 @30 fps (rotation metadata is honoured by ffmpeg).
- Each source gets one gain so its speech sits at -18 LUFS before the voice chain.
- Segments are frame-snapped and get 12 ms audio fades so joins never click.
WORDS_OUT lists every kept word in output time plus each segment's output window.
"""
import json
import re
import subprocess
import sys

cfg = json.load(open(sys.argv[1]))
out_path, words_out = sys.argv[2], sys.argv[3]
FPS, FADE = 30, 0.012
src_keys = list(cfg["sources"])
gain = {}
for k in src_keys:
    log = subprocess.run(["ffmpeg", "-nostats", "-i", cfg["sources"][k], "-map", "0:a:0", "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", log)
    gain[k] = round(-18 - float(m[-1]), 2) if m else 0.0

segs = [[k, round(a * FPS) / FPS, round(b * FPS) / FPS, lab] for k, a, b, lab in cfg["segments"]]
inputs, parts, labels = [], [], []
for k in src_keys:
    inputs += ["-i", cfg["sources"][k]]
for i, (k, a, b, _) in enumerate(segs):
    n = src_keys.index(k)
    d = b - a
    parts.append(
        f"[{n}:v:0]trim=start={a}:end={b},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps={FPS}[v{i}];"
        f"[{n}:a:0]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=mono,volume={gain[k]}dB,"
        f"afade=t=in:d={FADE},afade=t=out:st={d - FADE:.4f}:d={FADE}[a{i}];")
    labels.append(f"[v{i}][a{i}]")
graph = "".join(parts) + "".join(labels) + f"concat=n={len(segs)}:v=1:a=1[v][a]"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", graph, "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p", "-r", str(FPS), "-g", "15",
                "-c:a", "pcm_s16le", "-ar", "48000", out_path], check=True)

tx = {k: json.load(open(v)) for k, v in cfg.get("transcripts", {}).items()}
words, info, t = [], [], 0.0
for i, (k, a, b, lab) in enumerate(segs):
    info.append({"index": i, "src": k, "src_in": a, "src_out": b, "start": round(t, 3), "end": round(t + b - a, 3), "label": lab})
    for w in tx.get(k, []):
        if a - 0.02 <= w["start"] < b - 0.05:
            words.append({"text": w["text"], "start": round(t + max(w["start"], a) - a, 3), "seg": i})
    t += b - a
json.dump({"duration": round(t, 3), "gain": gain, "segments": info, "words": words}, open(words_out, "w"), indent=1)
print(f"assembled {len(segs)} segments from {len(src_keys)} sources, {t:.2f}s, {len(words)} words; gains {gain}")
