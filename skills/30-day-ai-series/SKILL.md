---
name: 30-day-ai-series
description: Edit a raw talking-head video into Jack's "30 Day AI Series" style — a clean, ink-on-paper editorial look that alternates his real footage (word-synced captions above the head, face-aware punch-ins) with short animated paper pages (kinetic type, animated logos, live infographics, UI mock-ups), finished with a carved music bed, sound design and a -14 LUFS master. Use when Jack asks for a 30 Day AI Series episode, a "Day N" video, or "edit this like Day 1". Built on HyperFrames + ffmpeg.
---

# 30 Day AI Series

A vertical (1080×1920, 30 fps) talking-head edit. Two worlds, cut between on ideas:

- **Face** — Jack's real footage, never cut out or regraded. Captions sit above his head; cuts hide behind face-aware punch-ins or a soft focus pull.
- **Pages** — plain grain paper with ink type and motion graphics. Short (≈1.5–3 s), except cards that must be read (prompts, templates) or a hero card he wants seen.

Approved reference: Day 1, "Claude motion graphics" (`assets/build-day01.py`, rendered as `exports/2026-10-21-day1-claude-motion-v6.mp4` in Jack's workspace). Every rule below came from his review notes — read `references/rules.md` before designing anything.

## Stack

HyperFrames (composition, render) · ffmpeg (cuts, voice, master) · `npx hyperframes transcribe --engine parakeet` (word timings) · Vision via `scripts/faces.swift` (face boxes) · MusicGen via `scripts/musicgen.py` when no licensed bed exists. Load `/hyperframes` and `/hyperframes-core` before writing composition HTML.

## Workflow

1. **Understand the take.** Probe it, transcribe it, contact-sheet it. Know the story, every product named, and every "this / here / like this" that needs a visual.
2. **Cut** (`references/workflow.md` § Cut): silences from `silencedetect`, words from Parakeet; keep the best take of each line; remove fillers, false starts, repeated takes, dead pauses, **and sniffs/breaths at segment edges** (noise-like, high-frequency, low level). Write `edit/edl.json`, run `scripts/make-aroll.sh`. Re-transcribe the cut and confirm every join reads cleanly.
3. **Plan the scenes.** Hook = first ~1.3 s on his face with a kinetic caption, then a page. Pick pages only where a visual earns it; pick from `references/scene-library.md` first.
4. **Build** from `assets/template.html` with a generator like `assets/build-day01.py`: tokens → caption groups, face samples → zoom windows, scenes → pages, SFX list, carved music bed.
5. **Check, then look properly.** `npx hyperframes check` must pass. Then step through every page at 0.1–0.25 s intervals (`npx hyperframes snapshot --at …`) — single snapshots miss peeking text and dead holds. Run a design-critique pass on the frames.
6. **Render, QA, master.** `npx hyperframes render -q delivery`, then `python3 -I scripts/qa.py <render> --out edit/qa-vN` (jump cuts, audio pops, captions over the face) and `scripts/master.sh <render>`. Copy the QA report to `edit/qa-latest.json`, rebuild (flagged jumps get focus pulls) and re-render until clean.
7. **Deliver** as `exports/<yyyy-mm-dd>-<job>-vN.mp4` and list what changed against his notes.

## References

| File | Use |
| --- | --- |
| `references/rules.md` | Jack's hard rules. Non-negotiable. |
| `references/style-system.md` | Palette, type, captions, page chrome, motion, transitions, sound, framing. |
| `references/scene-library.md` | Approved page patterns with timing and build notes. |
| `references/workflow.md` | Exact commands for every stage. |
| `assets/template.html` | Composition shell: fonts, CSS for every component, timeline helpers (`enter`, `rev`, `word`, `focus`). |
| `assets/build-day01.py` | Day 1 generator — the reference implementation. |
| `scripts/` | `cut.py`, `make-aroll.sh`, `retime.py`, `qa.py`, `faces.swift`, `master.sh`, `musicgen.py`. |

## Assets that are not in this repo

Fonts (Archivo, Playfair Display, IBM Plex Mono) and sound effects come from Jack's local asset library (LenoFX library, Kenney, Mixkit — see his memory notes for the path). They are licensed for his edits only; never commit them here. Logos come from `npx hyperframes media-use resolve --type logo` (official marks only, never redrawn).
