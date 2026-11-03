# Day 9 audit — what Jack flagged and the rules that came from it

"Speak any language with AI" (Higgsfield Audio → Translate, ElevenLabs). One take with retakes (IMG_5555), plus a 26 s Mac
screen recording of Higgsfield's Translate tool that came in round 2. Round 1 used still captures of the live sites; Jack's
round-2 notes:

| # | Note | Root cause | Fix (now in the skill) |
| --- | --- | --- | --- |
| 1 | "into" broken on the "turn your videos into any language" beat | Auto caption grouping made "into any" the bold line, so the half-revealed bold "into" read as "int" | Break caption groups at phrase boundaries ("turn your videos" / "into **any language**"); never leave a preposition as the bold word. Read every group against the line it shows |
| 2 | Web pages cropped | Screenshots were cropped to a panel to fill the card | **Never crop a website / app screen.** Show the whole frame at its own aspect ratio, centred on the paper with margin (landscape 3024×1820 → ~1000×602). Zoom in on a part, but the resting framing is the whole page and it comes back to it |
| 3 | Highlight border didn't fit when zoomed | Rings were screen-px overlays guessed beside a zooming image | Measure element boxes in the source image/video's own pixels; put rings and click rings **inside the same transformed layer** as the screen (`#rz` in `pages9.py`), so they hug the element at every zoom. Check zoom start/mid/end frames |
| 4 | Wanted the real Translate flow | Stills + a fake drag | Use his recording: real cursor kept; click rings at the cursor's real position and moment; retime the recording to his words piecewise (`edit/retime_rec.py`: speed up dead time, fast-forward scrolling) instead of cropping or cutting with jumps. Don't claim more than it shows (it never clicks Generate) |
| 5 | "Open up" page terrible and too long | Locked-padlock cards held ~4 s | A page must earn its time; three spoken items = three quick stickers on his face, each landing on its "open" |
| 6 | "Professional speakers" page terrible and too long | Crossed-out cards held ~5 s | Quick sticker beats (mic sticker, × stamp, one button click) on his face |
| 7 | "Turn your videos" page terrible and too long | A weak EN → ES/中文/FR branching diagram held ~7 s | Stickers on the words (your video → a sticker that flips through languages → more people) |
| 8 | "For a long time" page bad | Year counter + stamp page | Quick stickers (companies / clock / hand) |
| 9 | (round 3) Hide the browser tab strip | Round 2 kept the full recorded frame, so Chrome's tab titles showed | Crop the browser chrome (rows 0–173 here), never the site; shift every measured box/cursor/zoom region by that height and recompute the window aspect (1000×544) |

## Habits
- Before rendering, list every page with its on-screen length; anything over ~2.5 s without a layout change, or that only
  restates the caption, becomes stickers on his face.
- Ask for screen recordings when he films (this episode only got real screens in round 2).
- Day number check for V2: grep the built HTML's visible text, tokens and sticker text for 9/nine/10/ten/30/day (round 2 also
  caught "SCENE 9" on the clapper sticker).
- Click rings and highlight rings are created with `immediateRender: false` (or start at opacity 0) — a GSAP `fromTo` otherwise paints its
  from-state at load and leaves small circles on the screen before the click. A ring leaves as soon as its element changes (the
  Translate ring left after the click, not over the next page).
