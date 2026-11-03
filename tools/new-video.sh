#!/bin/sh
# Set up a new video: one folder on the SSD holding its Footage, Project and Exports, with short links back here.
# Usage (workspace root): sh tools/new-video.sh "<place>" <yyyy-mm-dd>-<job> <short-name>
#   <place>  "Series/30 Day AI Series/Day 15 - Title" or "Other Videos/Title" (named for Jack, no dates or numbers-only names)
# Creates  <SSD>/projects/<place>/Footage, Exports, Project/<id> (+ the links footage/<short-name>, projects/<id>).
set -e
cd "$(dirname "$0")/.."
SSD="/Volumes/Extreme Pro/Jack - Organized/04 Media/Video Editing/Claude Edits"
[ -d "$SSD" ] || { echo "SSD not mounted"; exit 1; }
[ $# -eq 3 ] || { sed -n 3,4p "$0"; exit 1; }
V="$SSD/projects/$1"; ID=$2; SHORT=$3
check() { # refuse to repoint a link another video depends on
  if [ -L "$2" ] && [ "$(readlink "$2")" != "$1" ]; then echo "$2 already points to $(readlink "$2"); pick another name"; exit 1; fi
  if [ -e "$2" ] && [ ! -L "$2" ]; then echo "$2 exists and is not a link"; exit 1; fi
}
check "$V/Footage" "footage/$SHORT"
check "$V/Project/$ID" "projects/$ID"
mkdir -p "$V/Footage" "$V/Exports" "$V/Project"
[ -e "$V/Project/$ID" ] || npx hyperframes init "$V/Project/$ID" --non-interactive --example=blank --skill=general-video --resolution portrait
ln -sfn "$V/Footage" "footage/$SHORT"
ln -sfn "$V/Project/$ID" "projects/$ID"
echo "Footage: $V/Footage (move his clips here, out of Downloads)"
echo "Project: projects/$ID"
echo "Exports: $V/Exports"
