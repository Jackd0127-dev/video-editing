#!/bin/sh
# Convert iPhone HDR (HLG) clips to SDR with Apple's own pipeline, keeping the original audio.
# Usage: sh sdr.sh <out-dir> <clip.MOV>...      -> <out-dir>/<name>-mix.mov (H.264 bt709 + original audio)
# Never grade his footage: this is the only colour step. Browser HLG handling washes him out.
set -e
out=$1; shift; mkdir -p "$out"
for src in "$@"; do
  n=$(basename "$src" | sed 's/\.[^.]*$//')
  [ -f "$out/$n-mix.mov" ] && continue
  avconvert -s "$src" -p PresetHighestQuality -o "$out/$n.mov" --replace >/dev/null
  ffmpeg -v error -y -i "$out/$n.mov" -i "$src" -map 0:v:0 -map 1:a:0? -c copy "$out/$n-mix.mov"
  rm "$out/$n.mov"
  echo "$n -> $out/$n-mix.mov"
done
