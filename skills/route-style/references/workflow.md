# Route workflow (commands)

`$S` = `skills/30-day-ai-series/scripts` (shared cut/QA tools), `$R` = `skills/route-style`. Run from the workspace root unless noted.

## Setup (media on the SSD)
```bash
SSD="/Volumes/Extreme Pro/Jack - Organized/04 Media/Video Editing/Claude Edits"
npx hyperframes init "$SSD/projects/<date>-<job>" --non-interactive --example=blank --skill=general-video --resolution portrait
ln -s "$SSD/projects/<date>-<job>" projects/<date>-<job>
cd projects/<date>-<job> && mkdir -p assets/{video,audio/sfx,fonts,img/logos} edit/trials/1 edit/trials/2
cp $R/assets/template.html edit/template.html && cp $R/assets/build-socials-1026.py edit/build.py && cp $R/scripts/tighten.py edit/
```
Fonts: `RedHatDisplay-{Black,Bold,Medium}.ttf` and `DIN Alternate Bold.otf` (→ `DINAlternate-Bold.otf`) from `Asset Library/Fonts`. SFX: copy the wavs from a recent project's `assets/audio/sfx` or convert Kenney `.ogg` with ffmpeg. Logos: `curl -sfL https://unpkg.com/@lobehub/icons-static-svg@1.95.1/icons/<name>.svg` into `assets/img/logos/` (check none render white on white).

## Analyse
```bash
sh $S/sdr.sh edit/sdr footage/<job>/IMG_*.MOV
ffmpeg -i edit/sdr/<name>-mix.mov -vn -ac 1 -ar 16000 edit/audio.wav
npx hyperframes transcribe edit/audio.wav --engine parakeet --dir edit/src
ffmpeg -nostats -i edit/audio.wav -af silencedetect=noise=-38dB:d=0.25 -f null -
```
Print a 10 ms energy envelope (`#` > −28 dB, `+` > −38, `-` > −46, `.` quiet) around every join to place in/out points; Parakeet word times drift up to ±0.2 s. Cross-check odd words: cut the snippet and `npx hyperframes transcribe <snip> --engine whisper --model medium.en`.

## Cut (per version)
Write `edit/trials/<n>/segments.json` (`sources`, `transcripts`, `segments: [[key, in, out, label]]`, explicit in/out from the envelope), then:
```bash
python3 -I edit/tighten.py edit/trials/<n>/segments.json
python3 -I $S/endcheck.py edit/trials/<n>/segments.json
python3 -I $S/cut_multi.py edit/trials/<n>/segments.json assets/video/aroll-t<n>.mov edit/trials/<n>/words.json
ffmpeg -i assets/video/aroll-t<n>.mov -c:v copy -af "<voice chain from $S/make-aroll.sh>" -c:a aac -b:a 320k assets/video/aroll-t<n>.mp4
ffmpeg -i assets/video/aroll-t<n>.mp4 -vn -ac 1 -ar 16000 edit/trials/<n>/aroll16k.wav
npx hyperframes transcribe edit/trials/<n>/aroll16k.wav --engine parakeet --dir edit/trials/<n>/txc   # read every join
```
Build `edit/trials/<n>/tokens.json` from `txc/transcript.json` with fixes (wanna, £5,000, brand spellings). Faces:
```bash
ffmpeg -i assets/video/aroll-t<n>.mp4 -vf "fps=2,scale=540:960" edit/faces/f%04d.png && swift $S/faces.swift edit/faces > edit/trials/<n>/faces-2fps.txt
```

## Build, check, look
```bash
TRIAL=1 python3 -I edit/build.py      # prints every page window: check the face | page rhythm
cp ../<project>-trials/out/trial-1.html ../<project>-trials/index.html   # the trials project is made by render-trials.sh (or by hand: link assets/, copy package.json + hyperframes.json)
cd ../<project>-trials && npx hyperframes check && npx hyperframes snapshot --at <t1,t2,…> --no-end -o snap
npx hyperframes snapshot --at <t> --no-end --zoom x,y,w,h -o snapz   # anything odd
```
Link the trials folder into `projects/` too (`ln -s "$SSD/projects/<project>-trials" projects/`). Look strip for Jack: `ffmpeg -pattern_type glob -i 'snap/frame-*.png' -vf "scale=360:640,tile=9x1:padding=8:color=white" look.jpg`.

## Render, QA, master, deliver
```bash
sh tools/render-trials.sh projects/<project> <date>-<job> 1 2
mv exports/<date>-<job>-trial{1,2}.mp4 "$SSD/exports/"
rm -rf "$TMPDIR"/hyperframes-extract-cache-*      # only when no other render is running
```
Report per version: hook line, length, what differs (table), QA (caption/face overlaps, voice-cut pops, jumps with focus pulls, LUFS), and a suggested post caption.
