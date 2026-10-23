# B-roll library

Jack's reusable cutaway shots, shared across all edits. Check this before choosing b-roll for any video.
Contact sheets (12 frames each): `_sheets/<name>.jpg`. **Every edit adds to this library:** any b-roll in a job's footage (whole cutaway clips, or cutaway moments inside longer clips) is saved here with `sh tools/broll-save.sh <clip> [start end]`, then looked at and given a row below. Clips dropped in by hand: `sh tools/broll-sheet.sh`, then add the row.

iPhone clips (IMG_*.MOV) are vertical, 30 fps, **HDR (HLG)**: run them through `skills/30-day-ai-series/scripts/sdr.sh` before use. Screen recordings are Mac captures (3024×1820, 60 fps, SDR): crop to the main panel and keep personal sidebars and session names out of frame. Use everything muted. Times are seconds into the clip.

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
| claude generating character.mp4 | Day 3 (2026-10-23) | 138.4 | Screen recording, Claude desktop app | Prompt "create me a new AI social media character… make me an image sheet with 10 different characters"; Claude runs Higgsfield; a 10-character grid appears (~115+) | 0–6 prompt; 100–138 grid lands | Left sidebar shows private session names: crop it out | screen, claude, higgsfield, character, ai-creator, image-generation | — |
| Recording 2026-10-23 at 13.02.10.mp4 | Day 3 (2026-10-23) | 122.0 | Screen recording, Claude desktop app | Picks the 2nd character (Bev); prompt for a 16:9 five-panel reference sheet (body shots cropped at the shoulders + two face close-ups); the sheet generates and lands (~110+) | 8–30 prompt; 105–122 sheet lands | Long waiting spinners in the middle; sidebar | screen, claude, higgsfield, character-sheet, ai-creator | — |
| Running higgs genjutsu.mp4 | Day 3 (2026-10-23) | 43.3 | Screen recording, new Claude session | Attaches a source dance video + the VOLT character sheet, types "Use higgsfield Genjutsu lite and replace the main character in the source video with my character", sends; tools start | 0–28 typing; 28–43 running | Model menu opens ~20; sidebar | screen, claude, higgsfield, genjutsu, video, ai-creator | — |
| Recording 2026-10-23 at 13.08.47.mp4 | Day 3 (2026-10-23) | 16.6 | Screen recording, Chrome: content.novasagency.com | Nova content planner: Create content → title, brand, picks accounts, creates the post; list updates | 1–16 | Browser tabs bar at top; account handles visible | screen, content-planner, scheduling, novas, posting | — |
| Video-3031.mp4 | Day 3 (2026-10-23) | 14.1 | Third-party viral clip (not Jack's footage), vertical 720p | Man in a waistcoat and yellow gloves dancing in a Paris street riot with fires | 0–14 | Not his footage: use only as the "before" of an AI swap | source-video, dance, before-after, third-party | — |
| result.mp4 | Day 3 (2026-10-23) | 14.1 | AI result (Higgsfield Genjutsu), vertical 720p, 24 fps | Same dance with Jack's character VOLT (cream suit, huge brown hat) swapped in | 0–14 | — | ai-result, genjutsu, dance, before-after, ai-creator | — |

## Rules for using b-roll
- Real footage only, muted, never graded; never a still frame of it.
- Prefer a clip or window not used in the last video. Update "Used in" after each edit.
- Cut on movement; 1.3–3 s per shot unless the line needs longer.
- Captions over b-roll still never cover his face (lift them when his head is at the top of frame).
