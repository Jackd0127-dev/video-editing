# Thumbnails (only when Jack asks)

Based on Day 14's. One 1080×1920 PNG, built from his footage so it matches the video. Use `tools/thumbnail-template.html` as the starting point.

- **Frame:** a real frame of him from the SDR footage, face clear and expression alive, no grade.
- **Headline:** a small line, then a big one (64 px and 128 px Archivo, white with a soft shadow), above his head and below the top 22 %. A few words of the video's promise, using his words, not a copy of the caption.
- **One taped paper note** with ink ticks and crosses, off his face, showing the proof in 2–3 short lines.
- **Series:** a small "Day N" tag, plus a second PNG without it for evergreen posts.

Copy the template to `edit/thumb/thumb.html`, swap the frame and text, then render it:
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=1080,1920 --screenshot="$PWD/thumb.png" "file://$(python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$PWD/thumb.html")"
```
Look at it at phone size, then save to the video's `Exports/` as `<Label> - Thumbnail.png` (and `<Label> - Thumbnail (no day number).png`).
