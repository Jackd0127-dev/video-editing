# Workflow commands

Layout: everything for a video is in one SSD folder (CLAUDE.md → Folders): `Footage/`, `Project/<id>/`, `Exports/`, linked here as `footage/<job>` and `projects/<id>`. `$EXPORTS` = the video's `Exports/` folder. `$S` = this skill's `scripts/` folder.

## Setup
```bash
sh tools/new-video.sh "Series/30 Day AI Series/Day N - <Title>" <date>-<job> <short-name>
mkdir -p assets/{video,audio/sfx,audio/bgm,fonts,img} edit
ln footage/<job>/<file>.mp4 assets/video/raw.mp4
```
Copy fonts and SFX from the local asset library; resolve logos with `npx hyperframes media-use resolve --type logo --intent "<brand>"`.

## Analyse
```bash
ffmpeg -i assets/video/raw.mp4 -vn -ac 1 -ar 16000 edit/audio.wav
npx hyperframes transcribe edit/audio.wav --engine parakeet --dir edit/src
ffmpeg -nostats -i edit/audio.wav -af silencedetect=noise=-38dB:d=0.25 -f null -
ffmpeg -i assets/video/raw.mp4 -vf "fps=2,scale=540:960" edit/faces/f%04d.png && swift $S/faces.swift edit/faces > edit/faces-source-2fps.txt
```
Parakeet word *ends* stretch over pauses — trust starts plus silences. Breath/sniff test: frames where level > −55 dB and >3 kHz energy ≈ all of it (noise-like) at a segment edge.

## B-roll library (every job)
Jack's shared cutaways live in `broll/` at the workspace root, catalogued in `broll/INDEX.md` (shot, best windows, what to avoid, tags, which video used it).
```bash
FOLDER="<type folder>" NAME="<what it shows>" sh tools/broll-save.sh footage/<job>/<clip>                 # a whole cutaway clip -> broll/
FOLDER="<type folder>" NAME="<what it shows>" sh tools/broll-save.sh footage/<job>/<clip> <start> <end>   # a cutaway moment inside a longer clip
sh tools/broll-sheet.sh                                     # sheet for clips dropped in by hand
```
**Always harvest:** in step 1 of every edit, sort the job's clips into talking-to-camera and b-roll. Save every usable b-roll clip or moment to the library (never move or change the originals), look at its sheet, and add its row to `broll/INDEX.md` with the job it came from.
When planning scenes, pick b-roll from the index first (prefer windows not used in the last video), convert the chosen clips with `sdr.sh`, cut them muted from the listed windows, and add the video to the clip's "Used in" column when the edit is approved.

## Colour first (every iPhone job)
```bash
sh $S/sdr.sh edit/sdr footage/<job>/IMG_*.MOV broll/<chosen>.MOV   # Apple HDR->SDR, original audio kept -> edit/sdr/<name>-mix.mov
```
Cut, b-roll and faces all read the `-mix.mov` files. Never pass HLG clips to the browser and never add a grade.

## Cut — one take
Write `edit/edl.json` (`source`, `transcript`, `output`, `words_out`, `segments`, `fixes`), then:
```bash
sh $S/make-aroll.sh            # cut.py (frame-snapped, 12 ms fades) + voice chain → assets/video/aroll.mp4
npx hyperframes transcribe edit/aroll16k.wav --engine parakeet --dir edit/tx   # verify joins; build edit/tokens.json
```
Changing the EDL later: keep the old `words.json`/`tokens.json` and run `python3 -I $S/retime.py old-words.json old-tokens.json` so caption indexes don't shift.

## Cut — several takes (Day 2)
Transcribe every source (`edit/tx/<key>.json`), pick the best take of each line, write `edit/plan.json` (`sources`, `transcripts`, `segments: [[key, first_word_start, last_word_start, label]]`), then:
```bash
python3 -I $S/snap.py edit/plan.json edit/segments.json      # in/out snapped to the quiet around the words
python3 -I $S/tighten.py edit/segments.json                  # Day 14: every pause inside/between lines -> ~0.12 s (keeps segments-loose.json)
python3 -I $S/cut_multi.py edit/segments.json assets/video/aroll.mov edit/words.json   # per-source gain, frame-snapped, 12 ms fades
python3 -I $S/tighten.py --words edit                        # map every word through the tightened pieces (no lost caption words)
ffmpeg -i assets/video/aroll.mov -c:v copy -af "<voice chain from make-aroll.sh>" -c:a aac -b:a 320k assets/video/aroll.mp4
npx hyperframes transcribe assets/video/aroll.mp4 --engine parakeet -d edit/txc   # read every join
```
At every join check the energy envelope of both sides (no half syllable, no repeated word) — see rules.md. Then read every line's head and tail: voiced audio before the first word or past the last word's end is a stutter ("he-here's") or an untranscribed "uh" — move the in/out to the deepest dip (edit `segments-loose.json`, re-run `tighten.py`). If a cut has to land mid-fricative, fade it over ~50 ms (`volume='if(between(t,T-0.06,T),(T-t)/0.06,1)':eval=frame` on the A-roll audio). `endcheck.py` skips a cut followed straight by the next word, so never end a line where the next word is joined on.
```bash
python3 -I $S/endcheck.py edit/segments.json      # must print "0 suspect ending(s)"; it suggests a new out-point for each one
```
Re-cutting later: keep `tokens.json`, re-transcribe the cut, then `python3 -I $S/realign.py old-tokens.json edit/txc/transcript.json edit/tokens.json`; append any new words at the end of the token list. Re-map b-roll windows segment by segment and re-run faces.

## Real website shots
Payoff sites go big (Day 14): full page at 2× → `site_window()` + `scroll_to()` + `ring()` in `assets/day13-kit/pages14.py`. Live sites with scroll-reveal sections: `npx hyperframes capture` (it scrolls, so sections render) and use its `full-page.png`; a site Claude built: find its `index.html` in `~/Library/Application Support/Claude/scratch-workspaces` (`mdfind <business>`), serve it locally, screenshot with headless Chrome (`--user-data-dir` fresh, `--force-device-scale-factor=2`, freeze rotating words with an injected style).

```bash
npx hyperframes capture https://<site> -o edit/site-capture --skip-vision    # scroll-*.png + full-page.png
```
Hero card: `scroll-000.png` scaled to 1800 wide. Browser scroll: `full-page.png` scaled to 2x the window width.

## Screen recordings, generated images, third-party clips
- Find the originals first: `mdfind -name "<file name seen in the recording>"` (Claude's scratch workspaces keep the 4K images it generated; his `~/Documents/AI Content/<creator>/` folders hold character sheets, carousels and posts). Use those, not frames of a recording.
- Screen recordings: a few seconds at the key moment only, cropped to the main panel (no sidebars with private session names), shown inside a window card.
- A person in a clip shown in a phone/card is tracked:
```bash
ffmpeg -i clip.mp4 -vf fps=10 edit/track/f%04d.png && swift $S/people.swift edit/track > edit/track/boxes.txt
python3 -I $S/trackcrop.py edit/track/boxes.txt clip.mp4 assets/video/br/clip-track.mp4 1.7
```
- Page videos can't sit inside a timed page: put them in the build's video layer (`overlay()` in `build-day03.py`), mirroring the page's motion and fades. Captions sit above that layer.

## Build and check
```bash
python3 -I edit/build.py         # writes index.html (Day 1 also builds + carves a music bed; Day 2 has none)
npx hyperframes check            # must pass; layout/contrast errors are real
npx hyperframes snapshot --at <t1,t2,…>   # step every page at 0.1–0.25 s
```

## Render, QA, master
Check free disk first (`df -h .`). Under ~4 GB, add `--workers 1` (streams frames instead of storing them) and delete regenerable frames (`edit/faces`, `edit/track/*/`, `.hyperframes/artifacts/snapshots`).
```bash
npx hyperframes render -q delivery --sdr --skill general-video -o "$EXPORTS/<Video title>.mp4"   # --sdr: footage is SDR already
python3 -I $S/qa.py "$EXPORTS/<Video title>.mp4" --out edit/qa-vN
cp edit/qa-vN/qa-report.json edit/qa-latest.json    # flagged jumps get focus pulls on the next build
sh $S/master.sh "$EXPORTS/<Video title>.mp4"         # −14 LUFS / −1 dBTP
```
QA passes when: no pops, no caption/face overlaps, and every reported jump has a focus pull. A pop on a word onset after silence (a hard "T" or "S") is speech, not a click — compare with his other T/S peaks before acting.
Also compare one face frame with Apple's own (`AVAssetImageGenerator`) — skin and contrast must match.

Anything with video inside a page (phones, cards, slider) is checked in the render itself — snapshots don't always seek page videos correctly.

## Pre-cut footage (Day 13)
When Jack sends a file he already cut (dead air out, his own "Coming up.." teaser and riser), keep it as the A-roll: no cutting.
```bash
ffmpeg -i <his file> -t <after last word + 0.35> -c:v libx264 -crf 14 -pix_fmt yuv420p … -af "<voice chain from make-aroll.sh>" assets/video/aroll-t1.mp4
ffmpeg -i assets/video/aroll-t1.mp4 -vf "scale=270:480,scdet=threshold=2.5" -an -f null - 2>&1 | grep scd.time   # his cut points -> edit/trials/1/words.json segments
```
Parakeet can drop a whole sentence: find word gaps over ~2 s with speech energy and re-transcribe that stretch with `--engine whisper --model medium.en`, then merge the words into `mktokens.py`. If `transcribe` says "Parakeet is not installed", run `npx hyperframes models install parakeet` from a project folder.

## Music version (when he wants one)
```bash
~/.venvs/hf-audio/bin/python -I $S/musicgen.py seed23.wav 29 "upbeat modern lo-fi electronic beat for a tech creator video, warm plucky synths, soft punchy drums, steady groove, optimistic, no vocals, minimal and clean" 23
sh $S/bed.sh seed23.wav <video seconds> bed.wav           # crossfaded loop, fades, 1–4 kHz carved for the voice
sh $S/mixbed.sh "$EXPORTS/<Video title>.mp4" bed.wav "$EXPORTS/<Video title> (music).mp4" [mute_from mute_to]
```
Generate two seeds and pick the steadier one (spectrogram: no bright full-band bursts). Deliver both versions. Keep the prompt happy and bright (major key, acoustic/ukulele, "feel-good") — Jack called a darker lo-fi bed "kind of eerie" (Day 13), and wanted it quieter: for a "low volume" bed run `BED_DB=-14 sh $S/mixbed.sh …` (default −9 dB). Trim any breakdown gap out of the loop before `bed.sh`.

## Hook experiments
Hooks are A/B-tested: keep his words, change the visuals. `edit/hooks.py` (see `assets/hooks-day03.py`) defines variants; `HOOK=n python3 -I edit/build.py` writes a 0 s → "Hello" clip, `HOOK=n FULL=1` the whole video with that hook. Render them from a sibling project that symlinks `assets/` and `node_modules/` (HyperFrames allows one root composition per project).
