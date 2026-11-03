# Day 13 audit — the approved look ("an AI receptionist for wedding venues")

Jack, 3 Nov 2026: "i loved day 13 it was super good clean and nice … all our series days are now way more like that." **Day 13 is the default look for every episode from now on.** Day 12's round-2 notes (1 Nov) led straight into it, so they are listed first.

Reference: `projects/Series/30 Day AI Series/Day 13 - AI Receptionist for Wedding Venues/Exports/Day 13 - V1.mp4` (V2 evergreen alongside). Build kit: `assets/day13-kit/` (see its README).

## Day 12 notes that shaped it
| # | Note | Root cause | Fix (now a rule) |
| --- | --- | --- | --- |
| 1 | "sometimes stuff is on top of my face when u add the liquid glass prompt boxes" | Overlays placed at fixed positions under the chin; his face is big and low in the frame | **Every overlay is placed from the face track** (`spot()`): beside his face, or low on his chest in close-ups, never over it. Check every overlay in snapshots |
| 2 | Glass boxes, ticks "look like ai slop … but i dont want basic white capsules" | Frosted-glass capsules and stock tick icons | **Small taped paper notes** (the series' paper texture, a strip of tape, ink type) with **hand-drawn ink ticks and crosses** that draw on with the word. No glass, no capsules, no emoji ticks |
| 3 | At 0:33 "the answer is no, it can't" came out of nowhere | The question line was in another clip and got left out | **Every answer needs its question on screen first.** Read the cut back as sentences; when a line answers or refers to something, the line it depends on must be in the cut (go find it in the other takes) |

## What Day 13 did (do this every episode)
1. **Mostly his face with captions.** Only three paper pages in 2:20: the Day N card (~2.5 s), a closing CTA card (~2.5 s) and the end card (~2.8 s). Everything else is on his footage.
2. **Paper notes on his footage, one per key moment**, each landing on its word: a number that counts up (200 guests), ink bars that grow on each number (capacity 140 / 180 vs 200, crossed out when it doesn't fit), checklists that tick as he says each item (vegetarian ✓ vegan ✓), a "who answered" card (Jess — AI, not a person), "call ended 1:24". Small (≈320–420 px wide at 1.35× zoom), slight tilt, taped, placed by the face track. One note at a time; gaps between notes stay clean face + captions.
3. **Captions read clean on any background.** Ink captions with a soft light halo when the background above his head is bright (sky, white wall); white captions on dark rooms. No template top scrim / vignette over bright footage (it reads as a grade). Captions always sit above his head (as high as y≈330), never under the chin when notes live on his chest. Face boxes start at the brows, so the build adds ~0.9 of the face height for forehead + hair.
4. **Other voices are tagged.** When someone else speaks (a phone call, an AI voice), their caption groups get a small typewriter tag above the words ("JESS · AI RECEPTIONIST"); groups break on every change of speaker.
5. **Long single takes still move.** A punch-in (face-aware zoom change ≥14 %) on every change of speaker and on sentence starts more than ~3 s apart, so a 86 s phone call never sits still.
6. **His own edit is kept.** When he pre-cuts the footage himself (dead air out, his "Coming up.." teaser, his riser), keep it: no re-cutting, no captions over his own on-screen text, the usual zoom-out at 0 s still on top.
7. **The ending:** his last line on his face → a short CTA card when the video promises more ("Want Part 2? / how to build it & sell it / comment PART 2" typed into a comment bubble) → the Day N+1 end card (V1). V2 ends on the CTA card.
8. **Real footage stays the hero.** His dialling shot stayed clean (the note moved to the other side of the frame); nothing covered the phone or his hands when they were the point.
9. **Small fixes made it feel finished:** every Parakeet mishear fixed and dropped sentences restored from Whisper, a click in his source ducked at the sample, −14 LUFS master, QA with 0 pops and 0 caption/face overlaps.

## Habits
- Start from `assets/day13-kit/` (copy the files into `edit/`, write a new `pagesNN.py`), not from an older day.
- Before building: list each key moment and the one note it gets; count page time (pages ≈ 3 per video).
- After building: snapshot every note window and check none touches his face or hair, and none covers what his hands are showing.
- Run `qa.py`; then check flagged pops by eye (a "pop" on a consonant like the "ch" of "touch" is speech, leave it).
