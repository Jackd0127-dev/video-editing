#!/bin/sh
# Master a rendered MP4's audio to -14 LUFS / -1 dBTP (two-pass, linear) without re-encoding video.
# Usage: tools/master.sh exports/<file>.mp4
set -e
F="$1"
STATS=$(ffmpeg -nostats -i "$F" -af loudnorm=I=-14:TP=-1:LRA=9:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
MEASURED=$(echo "$STATS" | python3 -I -c "import json,sys;d=json.load(sys.stdin);print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
ffmpeg -v error -y -i "$F" -c:v copy -af "loudnorm=I=-14:TP=-1:LRA=9:${MEASURED}:linear=true" -c:a aac -b:a 320k -ar 48000 -movflags +faststart "$F.master.mp4"
mv "$F.master.mp4" "$F"
