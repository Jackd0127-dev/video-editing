---
name: 30-day-ai-series
description: Edit a raw talking-head video into Jack's "30 Day AI Series" style — a clean, ink-on-paper editorial look that alternates his real footage (word-synced captions above the head, face-aware punch-ins) with short animated paper pages (kinetic type, animated logos, live infographics, UI mock-ups), finished with sound design (a music bed only if he asks) and a -14 LUFS master. Handles single-take and multi-take recordings from an iPhone. Use when Jack asks for a 30 Day AI Series episode, a "Day N" video, or "edit this like Day 1 / Day 2". Built on HyperFrames + ffmpeg.
---

# 30 Day AI Series

A vertical (1080×1920, 30 fps) talking-head edit. Two worlds, cut between on ideas:

- **Face** — Jack's real footage, never cut out or regraded. Captions sit above his head; cuts hide behind face-aware punch-ins or a soft focus pull.
- **Pages** — plain grain paper with ink type and motion graphics. Short (≈1.5–3 s), except cards that must be read (prompts, templates) or a hero card he wants seen.

Approved references: Day 1, "Claude motion graphics" (`assets/build-day01.py`, `exports/2026-10-21-day1-claude-motion-v6.mp4`), Day 2, "sketch to website" (`assets/build-day02.py`, `exports/2026-10-22-day2-sketch-to-site-v4.mp4`: several takes, hook voiceover, no music), and Day 3, "make your own AI creator" (`assets/build-day03.py`, `exports/2026-10-23-day3-ai-creator-v5.mp4`: screen recordings, before/after slider, music version, hook experiments). Every rule came from his review notes — read `references/rules.md`, `references/day2-audit.md` and `references/day3-audit.md` before designing anything.

## Stack

HyperFrames (composition, render) · ffmpeg (cuts, voice, master) · `npx hyperframes transcribe --engine parakeet` (word timings) · Vision via `scripts/faces.swift` (face boxes) · MusicGen via `scripts/musicgen.py` when no licensed bed exists. Load `/hyperframes` and `/hyperframes-core` before writing composition HTML.

## Workflow

0. **Colour.** iPhone footage is HDR: run `scripts/sdr.sh` on every clip first. Never grade or filter his footage.
1. **Understand the take.** Probe it, transcribe it, contact-sheet it. Know the story, every product named, and every "this / here / like this" that needs a visual. **Save every piece of b-roll** in the footage to the shared library (`tools/broll-save.sh`, then a row in `broll/INDEX.md`) — every edit adds to it.
2. **Cut** (`references/workflow.md` § Cut): silences from `silencedetect`, words from Parakeet; keep the best take of each line; remove fillers, false starts, repeated takes, dead pauses, **and sniffs/breaths at segment edges** (noise-like, high-frequency, low level). One take: `edit/edl.json` + `scripts/make-aroll.sh`. Several takes: `scripts/snap.py` + `scripts/cut_multi.py`. Re-transcribe the cut and check every join: word count and energy envelope, no doubled or clipped syllable; `scripts/endcheck.py` must report no clipped endings. Read every hook word against the audio.
3. **Plan the scenes.** Check `broll/INDEX.md` (workspace root) for cutaways before anything else; it lists each clip's usable windows and where it was used.
    Hook = first ~1.3 s on his face with a kinetic caption, then a page. Pick pages only where a visual earns it; pick from `references/scene-library.md` first.
4. **Build** from `assets/template.html` with a generator like `assets/build-day03.py` (latest; Day 1 and 2 for their patterns): tokens → caption groups, face samples → zoom windows, scenes → pages, SFX list (music bed only if he asks). Websites use real captures (`npx hyperframes capture`); generated images and posts are the real originals found on disk; clips in phones/cards are subject-tracked (`scripts/trackcrop.py`). Animations are causal (things appear when something reaches them), clicks are real cursor clicks.
5. **Check, then look properly.** `npx hyperframes check` must pass. Then step through every page at 0.1–0.25 s intervals (`npx hyperframes snapshot --at …`) — single snapshots miss peeking text and dead holds. Run a design-critique pass on the frames.
6. **Render, QA, master.** `npx hyperframes render -q delivery --sdr`, then `python3 -I scripts/qa.py <render> --out edit/qa-vN` (jump cuts, audio pops, captions over the face) and `scripts/master.sh <render>`. Copy the QA report to `edit/qa-latest.json`, rebuild (flagged jumps get focus pulls) and re-render until clean.
7. **Music and hooks.** If he wants music, deliver a no-music master and a music version (`scripts/bed.sh` + `scripts/mixbed.sh`). Offer hook experiments (`HOOK=n`) when the hook could go several ways.
8. **Deliver** as `exports/<yyyy-mm-dd>-<job>-vN.mp4` and list what changed against his notes. Once approved, fill in "Used in" in `broll/INDEX.md` for the library clips this edit used.

## References

| File | Use |
| --- | --- |
| `references/rules.md` | Jack's hard rules. Non-negotiable. |
| `references/style-system.md` | Palette, type, captions, page chrome, motion, transitions, sound, framing. |
| `references/scene-library.md` | Approved page patterns with timing and build notes. |
| `references/workflow.md` | Exact commands for every stage. |
| `references/day2-audit.md` | Every Day 2 mistake, its root cause and the fix — read before multi-take or iPhone jobs. |
| `references/day3-audit.md` | Every Day 3 note, root cause and fix, plus what he loved — read before jobs with screen recordings, generated images or before/after clips. |
| `assets/template.html` | Composition shell: fonts, CSS for every component, timeline helpers (`enter`, `rev`, `word`, `focus`). |
| `assets/build-day01.py` | Day 1 generator (single take, music bed). |
| `assets/build-day02.py` | Day 2 generator (multi-take, mini apps, keyboard URL, real-site shots, no music). |
| `assets/build-day03.py` | Day 3 generator (video layer, before/after slider + payoff strobe, drag-and-drop, causal network pages, hook experiments via `assets/hooks-day03.py`). |
| `scripts/` | `sdr.sh`, `cut.py`, `make-aroll.sh`, `snap.py`, `cut_multi.py`, `endcheck.py`, `retime.py`, `realign.py`, `qa.py`, `faces.swift`, `people.swift`, `trackcrop.py`, `master.sh`, `musicgen.py`, `bed.sh`, `mixbed.sh`. |

## Assets that are not in this repo

Fonts (Archivo, Playfair Display, IBM Plex Mono) and sound effects come from Jack's local asset library (LenoFX library, Kenney, Mixkit — see his memory notes for the path). They are licensed for his edits only; never commit them here. Logos come from `npx hyperframes media-use resolve --type logo` (official marks only, never redrawn).
