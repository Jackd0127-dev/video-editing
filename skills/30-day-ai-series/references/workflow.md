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

## Colour first (every iPhone job)
```bash
sh $S/sdr.sh edit/sdr footage/<job>/IMG_*.MOV      # Apple HDR->SDR, original audio kept -> edit/sdr/<name>-mix.mov
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
python3 -I $S/cut_multi.py edit/segments.json assets/video/aroll.mov edit/words.json   # per-source gain, frame-snapped, 12 ms fades
ffmpeg -i assets/video/aroll.mov -c:v copy -af "<voice chain from make-aroll.sh>" -c:a aac -b:a 320k assets/video/aroll.mp4
npx hyperframes transcribe assets/video/aroll.mp4 --engine parakeet -d edit/txc   # read every join
```
At every join check the energy envelope of both sides (no half syllable, no repeated word) — see rules.md.
Re-cutting later: keep `tokens.json`, re-transcribe the cut, then `python3 -I $S/realign.py old-tokens.json edit/txc/transcript.json edit/tokens.json`; append any new words at the end of the token list. Re-map b-roll windows segment by segment and re-run faces.

## Real website shots
```bash
npx hyperframes capture https://<site> -o edit/site-capture --skip-vision    # scroll-*.png + full-page.png
```
Hero card: `scroll-000.png` scaled to 1800 wide. Browser scroll: `full-page.png` scaled to 2x the window width.

## Build and check
```bash
python3 -I edit/build.py         # writes index.html (Day 1 also builds + carves a music bed; Day 2 has none)
npx hyperframes check            # must pass; layout/contrast errors are real
npx hyperframes snapshot --at <t1,t2,…>   # step every page at 0.1–0.25 s
```

## Render, QA, master
```bash
npx hyperframes render -q delivery --sdr --skill general-video -o exports/<date>-<job>-vN.mp4   # --sdr: footage is SDR already
python3 -I $S/qa.py exports/<date>-<job>-vN.mp4 --out edit/qa-vN
cp edit/qa-vN/qa-report.json edit/qa-latest.json    # flagged jumps get focus pulls on the next build
sh $S/master.sh exports/<date>-<job>-vN.mp4         # −14 LUFS / −1 dBTP
```
QA passes when: no pops, no caption/face overlaps, and every reported jump has a focus pull. A pop on a word onset after silence (a hard "T" or "S") is speech, not a click — compare with his other T/S peaks before acting.
Also compare one face frame with Apple's own (`AVAssetImageGenerator`) — skin and contrast must match.
