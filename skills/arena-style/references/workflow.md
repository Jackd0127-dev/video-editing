# Arena workflow (commands)

`$S` = `skills/30-day-ai-series/scripts` (shared cut/QA tools), `$A` = `skills/arena-style`. Run from the workspace root unless noted. Edits run in the chat, not through the API credit.

## Setup (media on the SSD)
```bash
SSD="/Volumes/Extreme Pro/Jack - Organized/04 Media/Video Editing/Claude Edits"
PD="$SSD/projects/Other Videos/<Title>/<date>-<job>"
npx hyperframes init "$PD" --non-interactive --example=blank --skill=general-video --resolution portrait
ln -s "$PD" projects/<date>-<job>
A="$PWD/skills/arena-style"; cd projects/<date>-<job> && mkdir -p assets/{video,audio/sfx,fonts,img/px} edit/trials/1 edit/trials/2
cp "$A/assets/template.html" edit/template.html
cp "$A/assets/build-claude-agents-arena.py" edit/build.py
cp "$A/assets/sprites.py" edit/sprites.py
python3 edit/sprites.py    # writes assets/img/px/, including kinds.json and crowd-tile.png
```
- **Fonts** (Google Fonts): `Archivo_Condensed-Black`, `Archivo_Condensed-ExtraBold`, `Archivo-ExtraBold`, `Archivo-SemiBold`, `IBMPlexMono-SemiBold`, `IBMPlexMono-Medium` `.ttf` into `assets/fonts/`.
- **SFX:** copy the wavs from a recent project's `assets/audio/sfx` (not in this repo).
- **Claude UI:** `assets/img/claude-prompt-empty.png` (1008×194) is a real Claude desktop prompt box from the b-roll library, with the text area left clear for typing over. `assets/img/claude-mark.svg` is the real mark; copy it from a recent project.

## Analyse
```bash
sh $S/sdr.sh edit/sdr footage/<job>/IMG_*.MOV
ffmpeg -i edit/sdr/<name>-mix.mov -vn -ac 1 -ar 16000 edit/audio.wav
npx hyperframes transcribe edit/audio.wav --engine parakeet --dir edit/src
ffmpeg -nostats -i edit/audio.wav -af silencedetect=noise=-38dB:d=0.25 -f null -
```
Parakeet word times drift up to ±0.2 s and it skips some "uh"s, so read an energy envelope around every join.

## Cut (per version)
Write `edit/trials/<n>/segments.json` (`sources`, `transcripts`, `segments: [[key, in, out, label]]`), then:
```bash
python3 -I skills/route-style/scripts/tighten.py edit/trials/<n>/segments.json
python3 -I $S/endcheck.py edit/trials/<n>/segments.json
python3 -I $S/cut_multi.py edit/trials/<n>/segments.json assets/video/aroll-t<n>.mov edit/trials/<n>/words.json
ffmpeg -i assets/video/aroll-t<n>.mov -c:v copy -af "<voice chain from $S/make-aroll.sh>" -c:a aac -b:a 320k assets/video/aroll-t<n>.mp4
ffmpeg -i assets/video/aroll-t<n>.mp4 -vn -ac 1 -ar 16000 edit/trials/<n>/aroll16k.wav
npx hyperframes transcribe edit/trials/<n>/aroll16k.wav --engine parakeet --dir edit/trials/<n>/txc   # read every join
```
Build `edit/trials/<n>/tokens.json` from `txc/transcript.json` with spelling fixes (`/arena`, numbers). Faces:
```bash
ffmpeg -i assets/video/aroll-t<n>.mp4 -vf "fps=2,scale=540:960" edit/faces/f%04d.png && swift $S/faces.swift edit/faces > edit/trials/<n>/faces-2fps.txt
```

## Adapt the generator
In `edit/build.py` keep the helpers and change: `EMPH` (caption key words per version), `PROMPT`, `PERSONAS`, `LSEED` / `RSEED` / `BOARD`, the V2 beats, and the `# the edit` section at the bottom, which is the whole timeline written as beat calls keyed to his words. The build raises an error if a phrase isn't in the cut. The page windows print on every build: use them to check the page budget.

## Build, check, look
```bash
TRIAL=1 python3 -I edit/build.py      # prints every page and overlay window
cp ../<project>-trials/out/trial-1.html ../<project>-trials/index.html   # the trials project is made by render-trials.sh (or by hand: link assets/, copy package.json + hyperframes.json)
cd ../<project>-trials && npx hyperframes check && npx hyperframes snapshot --at <t1,t2,…> --no-end -o snap
```
Look strip: `ffmpeg -pattern_type glob -i 'snap/frame-*.png' -vf "scale=360:640,tile=9x1:padding=8:color=white" look.jpg`.

## Render, QA, master, deliver
Other edits may share the machine: check `pgrep -f "hyperframes render"` and wait before each render.
```bash
sh tools/render-trials.sh projects/<project> <date>-<job> 1 2
D="$SSD/exports/Other Videos/<Title>"; mkdir -p "$D"
mv exports/<date>-<job>/<date>-<job>-trial1.mp4 "$D/<Title> - V1.mp4"
mv exports/<date>-<job>/<date>-<job>-trial2.mp4 "$D/<Title> - V2.mp4"; rmdir exports/<date>-<job>
```
Later rounds move the old renders to `Drafts/` first. Report per version: hook line, length, what differs (table), QA (caption/face overlaps, voice-cut pops, jumps, LUFS), and a suggested post caption.

## Music, only if he asks
No re-render: `sh $S/mixbed.sh in.mp4 bed.wav out.mp4` with a real, licensed track trimmed to the video length. Check the bed's loudness first: he wants it very low, about 20 dB under his voice. If the licence needs a credit, put it in the caption text.
