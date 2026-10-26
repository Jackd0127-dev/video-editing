---
name: route-style
description: Edit a raw talking-head video in Jack's "Route" style — a cobalt-and-lime transit map of the video's steps (ZERO → … → the payoff station) that a lime train travels as he talks, a small route HUD over his untouched footage, cobalt pages that wipe in on a lime line, real logos and real cursor clicks, and captions above his head with the spoken word in a lime block. Best for roadmap / step-by-step / "how I'd do X from zero" videos. Use when Jack asks for the Route style, "like the learn-AI-from-zero video", or a roadmap/steps video in a new look. Built on HyperFrames + ffmpeg; ships 2 versions.
---

# Route

The video is a journey, so the edit draws the map. A transit route of the video's steps appears in the hook, a lime train travels it as he reaches each step, a small HUD over his footage shows "you are here", and the payoff is the train arriving at the last station. Everything else is cobalt pages with white cards, real logos and real clicks.

Approved reference: "If I had to learn AI from zero" (26 Oct 2026), project `projects/2026-10-26-socials/`, generator `assets/build-socials-1026.py` on `assets/template.html`. Read `references/rules.md` before designing; numbers live in `references/style-system.md`; commands in `references/workflow.md`.

## Workflow

1. **Understand the take.** Media lives on the SSD (`footage/<job>` → `.../Claude Edits/footage/<job>`). iPhone HDR goes through `skills/30-day-ai-series/scripts/sdr.sh` first. Transcribe with Parakeet, contact-sheet it, and save any b-roll to `broll/` (talking head only → nothing to save).
2. **Find the route.** List the steps he actually names (e.g. ZERO → ONE TOOL → WEEK 1 → WEEK 2 → BUILDER). 4–6 stations; the first is where the viewer starts, the last is the payoff word he says ("building", "booked", "fit"…). Short labels he says himself, plus a DIN sub-line.
3. **Cut tight.** Last clean take of each line, retakes/self-corrections/fillers/dead air out (`scripts/tighten.py` splits mid-line pauses ≥0.26 s). Check joins on the energy envelope and re-transcribe the cut; cross-check odd words with whisper (`--model medium.en`). `endcheck.py` must be clean (a flagged out-point that drops an intended duplicate word is fine).
4. **Plan two versions** (`tools/TRIAL-REELS.md`): V1 = his hook, full; V2 = a different hook line (contrarian/skip line or result first), 25–35 % shorter, alternate page variants for at least a third of the beats. Write one `edit/trials/<n>/plan.json` each.
5. **Rhythm before pixels.** Lay the beats out as face | page windows: never more than ~6 s of pages in a row, never under 1 s of face between pages (pages within 1 s hand off by dissolving). Steps he names while on camera move the HUD instead of getting a page.
6. **Build** from `assets/template.html` with a generator like `assets/build-socials-1026.py` (`TRIAL=n python3 -I edit/build.py` → `../<project>-trials/out/trial-n.html`): set `STATIONS`/`RPTS` for this video's route, write the page functions (each has 2 variants where V2 differs), captions, camera, HUD plan.
7. **Check and look.** `npx hyperframes check` (word-by-word caption `line_unread` warnings and HUD-under-page overlap warnings are expected), snapshots of every page at its key words, zoom anything suspicious. Show Jack a look strip before the final render.
8. **Render, QA, master both:** `sh tools/render-trials.sh projects/<project> <date>-<job> 1 2`. QA passes with 0 caption/face overlaps and 0 voice-cut pops; flagged mix "pops" must be matched against the A-roll (word onsets are speech) or a placed SFX. Move renders to the SSD `exports/`, clear `$TMPDIR/hyperframes-extract-cache-*` when no other render runs, send both with a table and a suggested caption.

## References
| File | Use |
| --- | --- |
| `references/rules.md` | Route-specific rules + the shared hard rules every edit follows. |
| `references/style-system.md` | Palette, type, route map geometry, HUD, captions, page components, motion, sound. |
| `references/workflow.md` | Every command from raw clip to delivered exports. |
| `assets/template.html` | Composition shell (fonts, tokens, HUD, captions, page/route CSS, `enter`/`rev`/`focus`). |
| `assets/build-socials-1026.py` | Reference generator: route/HUD/train helpers, the page library with variants, captions, camera, assembly. |
| `scripts/tighten.py` | Splits segments at pauses inside a line. Other scripts are shared from `skills/30-day-ai-series/scripts/`. |
