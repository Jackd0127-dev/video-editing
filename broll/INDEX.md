# B-roll library

Jack's reusable cutaway shots, shared across all edits. Check this before choosing b-roll for any video.
Contact sheets (12 frames each): `_sheets/<name>.jpg`. **Every edit adds to this library:** any b-roll in a job's footage (whole cutaway clips, or cutaway moments inside longer clips) is saved here with `sh tools/broll-save.sh <clip> [start end]`, then looked at and given a row below. Clips dropped in by hand: `sh tools/broll-sheet.sh`, then add the row.

All current clips are iPhone, vertical, 30 fps, **HDR (HLG)**. Run them through `skills/30-day-ai-series/scripts/sdr.sh` before use, and use them muted. Times are seconds into the clip.

| Clip | From | Length | Shot | What happens | Best windows | Avoid | Tags | Used in |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IMG_5070 | Day 2 (2026-10-22) | 11.8 | Wide, high angle across the desk; bright sun, big monitor behind | Walks in, sits and sketches on loose paper | 2–10 | 0–1.5 walk-in; 10.5+ looks at camera | sketching, desk, working, sunlight | — |
| IMG_5071 | Day 2 (2026-10-22) | 6.8 | Side angle, leaning over the desk | Sketching, then looks up at the lens | 0.8–5.5 | 6+ looks at camera | sketching, desk, focus | — |
| IMG_5072 | Day 2 (2026-10-22) | 22.9 | High angle over the desk by the window; laptop and notebook | Walks in (body fills frame), sits, sketches in the notebook | 6–19 | 2–5 walk-in blocks frame; 21+ leans into lens | sketching, laptop, window, establishing | Day 2 (from 14.0) |
| IMG_5074 | Day 2 (2026-10-22) | 39.4 | Same setup as 5072, slightly wider | Continuous sketching in the notebook beside the laptop | 3–38 | — | sketching, laptop, long take | — |
| IMG_5075 | Day 2 (2026-10-22) | 35.9 | Side profile at the desk; window light behind, guitar on the wall | Sketching in a spiral notebook; calm, cinematic | 2–35 | — | sketching, profile, guitar, cinematic, establishing | Day 2 (from 8.0) |
| IMG_5076 | Day 2 (2026-10-22) | 85.9 | Over the shoulder, close; laptop open, window behind | Uses the laptop, then sketches; close side-profile drawing | 28–45, 50–85 | 12–26 exposure dips dark | sketching, laptop, close-up, over the shoulder | Day 2 (from 43.0) |
| IMG_5086 | Day 2 (2026-10-22) | 30.6 | Phone over the keyboard, filming the laptop screen; warm room light | Scrolls the live Hullabaloo café site top to bottom, hovers cards, flips a card. Clip has his voice: use muted | 1.5–15, 19.5–30 | 0–1.5 hand blur; 16.5–19.5 holds the notebook up (blurry) | website, laptop, screen, scrolling, hover, cafe | Day 2 hook (from 2.2) and "look at the animations" (from 22.0) |
| IMG_5077 | Day 2 (2026-10-22) | 17.4 | Top-down close on hands, notebook beside the laptop | Draws wireframe boxes for a site layout | 1–17 | — | hands, wireframe, drawing, top-down, website | Day 2 hook (from 10.0) and step 1 (from 4.0) |
| IMG_5079 | Day 2 (2026-10-22) | 10.5 | Top-down on the desk and notebook | Picks up his phone and photographs the sketch, then leaves | 2.5–6.5 | 7+ empty desk | phone, photo, sketch, top-down | Day 2 "take a photo" (from 3.0) |

## Rules for using b-roll
- Real footage only, muted, never graded; never a still frame of it.
- Prefer a clip or window not used in the last video. Update "Used in" after each edit.
- Cut on movement; 1.3–3 s per shot unless the line needs longer.
- Captions over b-roll still never cover his face (lift them when his head is at the top of frame).
