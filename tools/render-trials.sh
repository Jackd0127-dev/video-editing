#!/bin/sh
# Build, render, QA and master a video into its own Exports folder.
# Usage (workspace root): sh tools/render-trials.sh projects/<project> <date>-<job> [n ...]
#   No numbers (or just 1): one edit -> Exports/<Video title>.mp4. Extra versions only when Jack asks: 1 2 -> "<Label> - V1.mp4", "<Label> - V2.mp4" (tools/TRIAL-REELS.md).
#   MUSIC=path/bed.wav also makes a "(music)" copy, only when he asks for one (scripts/mixbed.sh).
# The project's edit/build.py must honour TRIAL=<n> and write ../<project>-trials/out/trial-<n>.html.
# A trial with its own cut keeps it in edit/trials/<n>/ (segments.json, words.json); otherwise the main cut is used.
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
S="$ROOT/skills/30-day-ai-series/scripts"
P=$(cd "$1" && pwd -P); shift 2
TRIALS=${*:-1}
T="$P-trials"
[ "$(basename "$(dirname "$P")")" = Project ] || { echo "$P is not in a video's Project folder (see tools/new-video.sh)"; exit 1; }
VIDEO=$(dirname "$(dirname "$P")"); TITLE=$(basename "$VIDEO"); EXPORTS="$VIDEO/Exports"
case "$TITLE" in "Day "[0-9]*" - "*) LABEL=${TITLE%% - *} ;; *) LABEL=$TITLE ;; esac
mkdir -p "$EXPORTS"
ln -sfn "$T" "$ROOT/projects/$(basename "$T")"
failed=0

# a sibling project that shares the assets (HyperFrames allows one root composition per project)
mkdir -p "$T/out"
ln -sfn "$P/assets" "$T/assets"
[ -e "$P/node_modules" ] && ln -sfn "$P/node_modules" "$T/node_modules"
cp "$P/package.json" "$P/hyperframes.json" "$T/" 2>/dev/null || true
[ -f "$T/meta.json" ] || printf '{"id":"%s","name":"%s"}\n' "$(basename "$T")" "$(basename "$T")" > "$T/meta.json"

for n in $TRIALS; do
  echo "== version $n"
  (cd "$P" && TRIAL=$n python3 -I edit/build.py)
  cp "$T/out/trial-$n.html" "$T/index.html"
  (cd "$T" && npx hyperframes check 2>&1 | grep -E "✗|Check passed|failed" | head -5)
  free=$(df -g "$ROOT" | awk 'NR==2 {print $4}')
  workers=auto; [ "$free" -lt 6 ] && workers=1
  if [ "$TRIALS" = 1 ]; then out="$EXPORTS/$TITLE.mp4"; else out="$EXPORTS/$LABEL - V$n.mp4"; fi
  # keep the last round: an old export must not pass for a failed render, and must not be lost either
  for old in "$out" "${out%.mp4} (music).mp4"; do
    if [ -f "$old" ]; then mkdir -p "$EXPORTS/Drafts"; mv "$old" "$EXPORTS/Drafts/$(basename "${old%.mp4}") - before $(date +%Y-%m-%d-%H%M%S).mp4"; fi
  done
  log="$P/edit/render-$n.log"; mkdir -p "$P/edit"
  (cd "$T" && npx hyperframes render -q delivery --sdr --workers $workers --skill general-video -o "$out" >"$log" 2>&1) || rm -f "$out"
  [ -f "$out" ] || { echo "version $n: render failed (free ${free}G), see $log"; tail -3 "$log"; failed=1; continue; }
  words="$P/edit/words.json"; [ -f "$P/edit/trials/$n/words.json" ] && words="$P/edit/trials/$n/words.json"
  [ -f "$P/edit/trials/$n/segments.json" ] && (cd "$P" && python3 -I "$S/endcheck.py" "edit/trials/$n/segments.json" | tail -1)
  (cd "$P" && python3 -I "$S/qa.py" "$out" --out "edit/qa-trial$n" --html "$T/out/trial-$n.html" --words "$words" 2>&1 | tail -1)
  if ! sh "$S/master.sh" "$out" >>"$log" 2>&1; then
    rm -f "$out.master.mp4"; mv "$out" "${out%.mp4} (not mastered).mp4"
    echo "version $n: master failed, see $log; kept as (not mastered)"; failed=1; continue
  fi
  if [ -n "$MUSIC" ] && ! sh "$S/mixbed.sh" "$out" "$MUSIC" "${out%.mp4} (music).mp4" >>"$log" 2>&1; then
    echo "version $n: music mix failed, see $log"; failed=1
  fi
  echo "version $n: $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out") s -> $out"
done
exit $failed
