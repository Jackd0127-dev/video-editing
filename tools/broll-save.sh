#!/bin/sh
# Save b-roll from an edit's footage into the shared library (broll/). Originals are never touched.
# Usage (from the workspace root):
#   FOLDER="<type folder>" NAME="<what it shows>" sh tools/broll-save.sh <clip>               whole clip is b-roll -> id <name>
#   FOLDER="<type folder>" NAME="<what it shows>" sh tools/broll-save.sh <clip> <start> <end>  b-roll moment inside a longer clip -> id <name>_<start>-<end>
# FOLDER is the library folder for this type of shot, e.g. "Working at a Laptop/Typing". Use one that fits; if none does, name a new detailed one and it is created.
# The file goes to the SSD library as "<FOLDER>/<NAME> [<id>].<ext>" (e.g. "Typing at laptop - over shoulder [IMG_5267].MOV")
# and is linked back as broll/<id>.<ext>; INDEX.md rows and contact sheets use the id.
# Extracts are stream-copied (no re-encode, HDR and rotation kept), so they snap out to the nearest keyframes.
# Then makes the contact sheet; look at it and add the clip's row to broll/INDEX.md (with the job it came from).
set -e
cd "$(dirname "$0")/.."
src=$1; n=$(basename "$src"); ext=${n##*.}; n=${n%.*}
SSD="/Volumes/Extreme Pro/Jack - Organized/04 Media/Video Editing/Claude Edits/broll"
[ -d "$SSD" ] || { echo "SSD not mounted"; exit 1; }
id=$n; [ -n "$3" ] && id="${n}_$2-$3"
[ -n "$FOLDER" ] && [ -n "$NAME" ] || { echo "FOLDER and NAME are required. Folders so far:"; (cd "$SSD" && find . -mindepth 1 -type d -not -path "./_sheets*" | sed 's|^\./||' | sort); exit 1; }
mkdir -p "$SSD/$FOLDER"
real="$SSD/$FOLDER/$NAME [$id].$ext"; out="broll/$id.$ext"
if [ -L "$out" ] || [ -e "$out" ]; then
  echo "$out already exists -> $(readlink "$out"). Not saved: if this is a different clip, rename the source or use a different time range."; exit 1
fi
if [ -n "$3" ]; then
  ffmpeg -v error -ss "$2" -to "$3" -i "$src" -map 0 -map_metadata 0 -c copy -movflags +faststart "$real"
else
  cp -p "$src" "$real"
fi
ln -s "$real" "$out"
echo "saved $out"
sh tools/broll-sheet.sh
