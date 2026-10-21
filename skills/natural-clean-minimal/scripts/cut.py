"""Assemble kept source ranges into one A-roll file and retime the transcript.

Usage: python3 cut.py EDL.json

EDL.json:
{
  "source": "path/to/raw.mp4",
  "transcript": "path/to/transcript.json",   # [{text,start,end}] in source time
  "output": "path/to/aroll.mp4",
  "words_out": "path/to/words.json",
  "fade_ms": 12,
  "segments": [[in, out], ...],               # source seconds, in timeline order
  "fixes": {"codecs": "Codex", ...}           # optional caption text fixes
}

Each segment gets a short audio fade at both ends so butt-joined cuts never pop.
Writes words.json: kept words in output time, plus "segments" with their output starts.
"""
import json
import subprocess
import sys

cfg = json.load(open(sys.argv[1]))
fps = cfg.get("fps", 30)
# Snap to the frame grid so picture and sound segments are the same length (no drift).
segs = [[round(a * fps) / fps, round(b * fps) / fps] for a, b in cfg["segments"]]
fade = cfg.get("fade_ms", 12) / 1000

parts, labels = [], []
for i, (a, b) in enumerate(segs):
    d = b - a
    parts.append(
        f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS[v{i}];"
        f"[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,"
        f"afade=t=in:d={fade},afade=t=out:st={d - fade:.4f}:d={fade}[a{i}];"
    )
    labels.append(f"[v{i}][a{i}]")
graph = "".join(parts) + "".join(labels) + f"concat=n={len(segs)}:v=1:a=1[v][a]"

subprocess.run(
    [
        "ffmpeg", "-v", "error", "-y", "-i", cfg["source"],
        "-filter_complex", graph, "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p",
        "-r", "30", "-g", "15", "-c:a", "pcm_s16le", "-ar", "48000",
        cfg["output"],
    ],
    check=True,
)

words = json.load(open(cfg["transcript"]))
fixes = cfg.get("fixes", {})
out_words, seg_info, t = [], [], 0.0
for i, (a, b) in enumerate(segs):
    seg_info.append({"index": i, "src_in": a, "src_out": b, "start": round(t, 3), "end": round(t + b - a, 3)})
    for w in words:
        mid = (w["start"] + min(w["end"], w["start"] + 0.5)) / 2
        if a <= mid < b:
            text = w["text"]
            key = text.strip(".,!?").lower()
            if key in fixes:
                text = text.lower().replace(key, fixes[key]) if text[0].islower() else fixes[key] + text[len(key):]
            out_words.append({
                "text": text,
                "start": round(t + max(w["start"], a) - a, 3),
                "end": round(t + min(w["end"], b) - a, 3),
                "seg": i,
            })
    t += b - a
json.dump({"duration": round(t, 3), "segments": seg_info, "words": out_words}, open(cfg["words_out"], "w"), indent=1)
print(f"assembled {len(segs)} segments, {t:.2f}s, {len(out_words)} words")
