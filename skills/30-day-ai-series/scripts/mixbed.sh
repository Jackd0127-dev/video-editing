#!/bin/sh
# Make the "with music" version from a finished, mastered no-music render (no re-render needed).
# Usage: sh mixbed.sh in.mp4 bed.wav out.mp4 [mute_from mute_to]
#   bed.wav: full-length bed (MusicGen loop crossfaded to the video length, 1–4 kHz cut so the voice sits on top).
#   The bed is ducked under the voice (sidechain), sits ~15 dB under speech, and is muted between mute_from
#   and mute_to (e.g. while a clip plays its own song). Then the result is mastered to -14 LUFS.
set -e
in=$1; bed=$2; out=$3; m0=${4:-0}; m1=${5:-0}
ffmpeg -v error -y -i "$in" -i "$bed" -filter_complex \
  "[0:a]aresample=48000,asplit=2[v][key];[1:a]volume=-9dB,volume='if(between(t,$m0,$m1),0,1)':eval=frame[b0];[b0][key]sidechaincompress=threshold=0.06:ratio=3:attack=30:release=450:makeup=1[bd];[v][bd]amix=inputs=2:duration=first:normalize=0[o]" \
  -map 0:v -map "[o]" -c:v copy -c:a aac -b:a 320k -movflags +faststart "$out"
sh "$(dirname "$0")/master.sh" "$out"
