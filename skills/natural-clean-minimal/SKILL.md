---
name: natural-clean-minimal
description: Edit a raw talking-head video in Jack's "Natural Clean Minimal" style — fast jump cuts with alternating punch-ins, one-word white ALL-CAPS captions on the chest, a quick zoom hook, and a few premium liquid-glass overlays (banner titles, a pixel Claude character, comment composers with natural typing and a clicking cursor). Footage stays natural and ungraded. Use when Jack asks for the natural/clean/minimal style, a short CTA or tip video "like the comment video", or one-word captions. Built on HyperFrames + ffmpeg.
---

# Natural Clean Minimal

Footage-first and fast. The talking head carries the video; graphics appear only when they earn it and they look like premium UI (liquid glass), not paper pages.

Approved reference: the comment-CTA ("tell me what you're building"), built by `assets/build-comment-cta.py` on `assets/template.html`. Style source: `references/reference-breakdown.md`. Read `references/rules.md` before designing.

## Workflow

1. **Understand the take**: probe, transcribe (`npx hyperframes transcribe --engine parakeet`, whisper as fallback), contact-sheet, `silencedetect`. Save every piece of b-roll in the footage to the shared library (`sh tools/broll-save.sh <clip> [start end]`, then a row in `broll/INDEX.md`).
2. **Cut tight**: remove the intro filler ("alright everyone"), repeated phrases, every pause between *and inside* sentences (>0.3 s), sniffs/breaths. Split a segment to remove a mid-sentence gap. Write `edit/edl.json`, run `sh <skill>/scripts/make-aroll.sh`, re-transcribe the cut, confirm joins read cleanly. When the EDL changes later, `scripts/retime.py` moves caption tokens across.
3. **Plan**: hook = quick zoom (1.38→1 in 0.55 s) + one designed overlay (glass banner title with the pixel Claude character). For cutaways, pick from the shared b-roll library first (`broll/INDEX.md` at the workspace root; iPhone HDR clips go through `skills/30-day-ai-series/scripts/sdr.sh`, muted, never graded). One or two emphasis cards. A glass UI payoff at the end that matches the CTA (composer → typing → cursor click → posted card).
4. **Build** from `assets/template.html` with a generator like `assets/build-comment-cta.py`: tokens → one-word captions (hard switch, no overlap), hook, emphasis card, ending, punch-ins alternating 1.0/1.15 at every cut and phrase break, SFX, music bed carved under the voice.
5. **Check and look**: `npx hyperframes check`, then snapshot every overlay at 0.25–0.3 s steps and zoom into glass edges at 2× (corners must be smooth).
6. **Render, QA, master**: `npx hyperframes render -q delivery`; `python3 -I scripts/qa.py <render> --out edit/qa-vN --caption-top 1395` (chest captions); `sh scripts/master.sh <render>` (−14 LUFS / −1 dBTP).

## References
| File | Use |
| --- | --- |
| `references/rules.md` | Jack's rules for this style (and the ones shared with every edit). |
| `references/style-system.md` | Type, captions, glass recipe, motion, sound, framing numbers. |
| `references/reference-breakdown.md` | Breakdown of the TikTok reference this style comes from. |
| `assets/template.html` / `assets/build-comment-cta.py` | Composition shell and reference generator. |
| `scripts/` | Cut, retime, QA, face detection, master, local music bed. |

Fonts (Montserrat, free on Google Fonts) and SFX come from Jack's local asset library and are not in this repo.
