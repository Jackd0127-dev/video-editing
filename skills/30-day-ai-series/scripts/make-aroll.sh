#!/bin/sh
# Rebuild the A-roll from the raw take: cut (edl.json), clean and level the voice, encode.
# Run from the project root (sh <skill>/scripts/make-aroll.sh), then `python3 -I edit/build.py`.
set -e
python3 -I "$(dirname "$0")/cut.py" edit/edl.json
ffmpeg -v error -y -i assets/video/aroll.mov -c:v copy \
  -af "highpass=f=75,lowpass=f=15500,equalizer=f=250:t=q:w=1.2:g=-2,equalizer=f=3500:t=q:w=1.0:g=2,acompressor=threshold=-22dB:ratio=3:attack=6:release=90:makeup=3,alimiter=limit=0.9,loudnorm=I=-15:TP=-1.5:LRA=7" \
  -c:a aac -b:a 320k -ar 48000 -movflags +faststart assets/video/aroll.mp4
rm assets/video/aroll.mov
# Caption timing comes from a transcript of the cut itself (edit/tx), corrected into edit/tokens.json.
