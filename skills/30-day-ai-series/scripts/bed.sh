#!/bin/sh
# Build a full-length music bed from a MusicGen loop (any length over ~6 s). Usage: sh bed.sh loop.wav SECONDS out.wav
# Crossfades copies of the loop, fades in/out, and cuts 1–4 kHz so the voice stays clear on top.
set -e
loop=$1; len=$2; out=$3
# a path with spaces breaks the -i list below: work from a space-free link (Day 13)
tmp=$(mktemp -d); ln -s "$(cd "$(dirname "$loop")" && pwd)/$(basename "$loop")" "$tmp/loop.wav"; loop="$tmp/loop.wav"
# copies needed from the loop's real length (2 s crossfades), not an assumed 29 s
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$loop")
n=$(python3 -c "import math; print(math.ceil($len / ($d - 2)) + 1)")
args=""; graph=""; prev="[0]"
i=0; while [ $i -lt $n ]; do args="$args -i $loop"; i=$((i+1)); done
i=1; while [ $i -lt $n ]; do graph="$graph$prev[$i]acrossfade=d=2[x$i];"; prev="[x$i]"; i=$((i+1)); done
ffmpeg -v error -y $args -filter_complex "${graph}${prev}aresample=48000,aformat=channel_layouts=stereo,atrim=0:$len,afade=t=in:d=0.6,afade=t=out:st=$(python3 -c "print($len-3)"):d=3,equalizer=f=2500:t=q:w=1.4:g=-5,equalizer=f=1000:t=q:w=1.2:g=-2,highpass=f=40[o]" -map "[o]" "$out"
