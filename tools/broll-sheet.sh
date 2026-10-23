#!/bin/sh
# Contact sheet + facts for each b-roll clip that doesn't have a sheet yet.
# Usage (from the workspace root): sh tools/broll-sheet.sh            -> broll/_sheets/<name>.jpg
# Prints "name | length | orientation | HDR" so you can add a row to broll/INDEX.md after looking at the sheet.
# Sheets are decoded without tone-mapping, so iPhone HDR clips look washed here; the clips themselves are fine.
cd "$(dirname "$0")/.." || exit 1
mkdir -p broll/_sheets
for f in broll/*.MOV broll/*.mov broll/*.mp4; do
  [ -f "$f" ] || continue
  n=$(basename "$f"); n=${n%.*}
  [ -f "broll/_sheets/$n.jpg" ] && continue
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  tr=$(ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer -of csv=p=0 "$f")
  ffmpeg -v error -y -i "$f" -vf "fps=12/$d,scale=240:-2,tile=6x2:padding=4" -frames:v 1 "broll/_sheets/$n.jpg"
  # ffmpeg applies the phone's rotation when it builds the sheet, so the sheet's shape tells the orientation
  orient=$(ffprobe -v error -show_entries stream=width,height -of csv=p=0 "broll/_sheets/$n.jpg" | awk -F, '{print ($2 * 3 > $1) ? "vertical" : "horizontal"}')
  hdr=SDR; echo "$tr" | grep -q arib-std-b67 && hdr="HDR (HLG)"
  printf '%s | %.1fs | %s | %s\n' "$n" "$d" "$orient" "$hdr"
done
