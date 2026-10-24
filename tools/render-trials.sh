#!/bin/sh
# Build, render, QA and master a video's trial reels (see tools/TRIAL-REELS.md).
# Usage (workspace root): sh tools/render-trials.sh projects/<project> <date>-<job> [1 2 3 4 5]
#   MUSIC=path/bed.wav also makes a -music version of each trial (scripts/mixbed.sh).
# The project's edit/build.py must honour TRIAL=<n> and write ../<project>-trials/out/trial-<n>.html.
# A trial with its own cut keeps it in edit/trials/<n>/ (segments.json, words.json); otherwise the main cut is used.
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
S="$ROOT/skills/30-day-ai-series/scripts"
P=$(cd "$1" && pwd); JOB=$2; shift 2
TRIALS=${*:-1 2 3 4 5}
T="$P-trials"

# a sibling project that shares the assets (HyperFrames allows one root composition per project)
mkdir -p "$T/out"
[ -e "$T/assets" ] || ln -s "$P/assets" "$T/assets"
[ -e "$T/node_modules" ] || ln -s "$P/node_modules" "$T/node_modules"
cp "$P/package.json" "$P/hyperframes.json" "$T/" 2>/dev/null || true
[ -f "$T/meta.json" ] || printf '{"id":"%s","name":"%s"}\n' "$(basename "$T")" "$(basename "$T")" > "$T/meta.json"

for n in $TRIALS; do
  echo "== trial $n"
  (cd "$P" && TRIAL=$n python3 -I edit/build.py)
  cp "$T/out/trial-$n.html" "$T/index.html"
  (cd "$T" && npx hyperframes check 2>&1 | grep -E "✗|Check passed|failed" | head -5)
  free=$(df -g "$ROOT" | awk 'NR==2 {print $4}')
  workers=auto; [ "$free" -lt 6 ] && workers=1
  out="$ROOT/exports/$JOB-trial$n.mp4"
  (cd "$T" && npx hyperframes render -q delivery --sdr --workers $workers --skill general-video -o "$out" 2>&1 | grep -E "✗" | head -3) || true
  [ -f "$out" ] || { echo "trial $n: render failed (free ${free}G)"; continue; }
  words="$P/edit/words.json"; [ -f "$P/edit/trials/$n/words.json" ] && words="$P/edit/trials/$n/words.json"
  [ -f "$P/edit/trials/$n/segments.json" ] && (cd "$P" && python3 -I "$S/endcheck.py" "edit/trials/$n/segments.json" | tail -1)
  (cd "$P" && python3 -I "$S/qa.py" "$out" --out "edit/qa-trial$n" --html "$T/out/trial-$n.html" --words "$words" 2>&1 | tail -1)
  sh "$S/master.sh" "$out" >/dev/null 2>&1
  [ -n "$MUSIC" ] && sh "$S/mixbed.sh" "$out" "$MUSIC" "${out%.mp4}-music.mp4" >/dev/null 2>&1
  echo "trial $n: $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out") s -> $out"
done
