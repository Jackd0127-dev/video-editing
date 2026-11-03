# Day 10 audit — "one video, a month of content"

Jack's notes on the first Day 10 render (30 Oct 2026). V1 spent ~40 s in a row on blank paper pages.

| # | Note | Root cause | Fix (now a rule) |
| --- | --- | --- | --- |
| 1 | "So, we have 20 minutes" was cut, so the next sentence didn't make sense | Lines were picked against the planned script; his off-script setup line was treated as a filler | **He goes off-script on purpose, usually so the next sentence makes sense.** Keep any line the following sentence depends on. Read the cut back sentence by sentence: every sentence must make sense on its own and after the one before it |
| 2 | ~40 s straight of blank screen with motion graphics | Every line got its own paper page, and pages chained into each other | **The video is mostly him, with captions.** A paper page is for showing one thing and lasts a few seconds at most (≤ ~2.5 s, never two pages back to back for more than ~4 s, and his face between pages). Everything else is an **overlay on his footage** |
| 3 | The "edit" screen (film strip, scissors, big X) was "terrible and hideous" | Literal prop on a blank page | Overlays that look like editorial motion design over his footage, not clip-art pages |
| 4 | "One take, one camera" page | Static camera on a tripod | Character animation: a little figure walks into a studio, sets up the camera, sits down (a short page or an overlay card) |
| 5 | The Claude "questions" composer page | A page for a line that only needed captions | Keep him on screen with captions when the line doesn't need a picture |
| 6 | Q1 / Q2 / Q3 | Paper cards on a page | A clean list that pops in over him, item by item, cinematic |
| 7 | "Full list of 100 questions" | Paper page | An overlay list over him that scrolls smoothly |
| 8 | River / field / lake | Drawn landscape cards | **Real, high-quality, cinematic footage** of a river, a field and a lake, shown as overlay screens over him, with editorial type |
| 9 | The story/schedule planner | Plain grid | A much better-looking planner overlay (real thumbnails, clean editorial layout, a story line through it) |
| 10 | "All the content you need" | Paper grid | The content flies in and orbits around his head |

## Habits
- Before building, add up page time: pages are the exception (a few seconds each); overlays on his footage are the default.
- Check page chains in the build log (`scene` list): no run of pages longer than ~4 s.
- Read the cut transcript back as sentences before building.
