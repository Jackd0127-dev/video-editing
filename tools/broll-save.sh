#!/bin/sh
# Save b-roll from an edit's footage into the shared library (broll/). Originals are never touched.
# Usage (from the workspace root):
#   sh tools/broll-save.sh <clip>               whole clip is b-roll -> copied as broll/<name>.<ext>
#   sh tools/broll-save.sh <clip> <start> <end>  b-roll moment inside a longer clip -> broll/<name>_<start>-<end>.<ext>
# Extracts are stream-copied (no re-encode, HDR and rotation kept), so they snap out to the nearest keyframes.
# Then makes the contact sheet; look at it and add the clip's row to broll/INDEX.md (with the job it came from).
set -e
cd "$(dirname "$0")/.."
src=$1; n=$(basename "$src"); ext=${n##*.}; n=${n%.*}
if [ -n "$3" ]; then
  out="broll/${n}_$2-$3.$ext"
  [ -f "$out" ] || ffmpeg -v error -ss "$2" -to "$3" -i "$src" -map 0 -map_metadata 0 -c copy -movflags +faststart "$out"
else
  out="broll/$n.$ext"
  [ -f "$out" ] || cp -p "$src" "$out"
fi
echo "saved $out"
sh tools/broll-sheet.sh
