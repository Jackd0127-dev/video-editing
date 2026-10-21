# Workflow commands

Project layout (Jack's workspace): `footage/<job>/` raw · `projects/<yyyy-mm-dd>-<job>/` HyperFrames project · `exports/` renders. `$S` = this skill's `scripts/` folder.

## Setup
```bash
npx hyperframes init projects/<date>-<job> --non-interactive --example=blank --skill=general-video --resolution portrait
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

## Cut
Write `edit/edl.json` (`source`, `transcript`, `output`, `words_out`, `segments`, `fixes`), then:
```bash
sh $S/make-aroll.sh            # cut.py (frame-snapped, 12 ms fades) + voice chain → assets/video/aroll.mp4
npx hyperframes transcribe edit/aroll16k.wav --engine parakeet --dir edit/tx   # verify joins; build edit/tokens.json
```
Changing the EDL later: keep the old `words.json`/`tokens.json` and run `python3 -I $S/retime.py old-words.json old-tokens.json` so caption indexes don't shift.

## Build and check
```bash
python3 -I edit/build.py         # writes index.html, regenerates the cliffhanger bed, runs carve.mjs
npx hyperframes check            # must pass; layout/contrast errors are real
npx hyperframes snapshot --at <t1,t2,…>   # step every page at 0.1–0.25 s
```

## Render, QA, master
```bash
npx hyperframes render -q delivery --skill general-video -o exports/<date>-<job>-vN.mp4
python3 -I $S/qa.py exports/<date>-<job>-vN.mp4 --out edit/qa-vN
cp edit/qa-vN/qa-report.json edit/qa-latest.json    # flagged jumps get focus pulls on the next build
sh $S/master.sh exports/<date>-<job>-vN.mp4         # −14 LUFS / −1 dBTP
```
QA passes when: no pops, no caption/face overlaps, and every reported jump has a focus pull.
