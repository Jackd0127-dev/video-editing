#!/bin/sh
# faces-2fps.txt + env30.json for a trial. Usage: sh edit/mkfaces.sh <n>
n=$1; S=/Users/jackd/.claude/skills/30-day-ai-series/scripts
rm -rf edit/faces$n && mkdir -p edit/faces$n
ffmpeg -v error -i assets/video/aroll-t$n.mp4 -vf "fps=2,scale=540:960" edit/faces$n/f%04d.png
swift $S/faces.swift edit/faces$n > edit/trials/$n/faces-2fps.txt 2>/dev/null
rm -rf edit/faces$n
python3 - <<PY
import subprocess, struct, math, json
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", "assets/video/aroll-t$n.mp4", "-map", "0:a:0", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout
x = struct.unpack(f"{len(raw)//4}f", raw); hop = 16000 // 30
e = [math.sqrt(sum(v * v for v in x[i:i + hop]) / hop) for i in range(0, len(x) - hop, hop)]
m = sorted(e)[int(len(e) * 0.95)] or 1
json.dump([round(min(1, v / m), 3) for v in e], open("edit/trials/$n/env30.json", "w"))
PY
echo "trial $n faces+env done"
