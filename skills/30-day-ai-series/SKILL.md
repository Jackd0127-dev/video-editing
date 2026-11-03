---
name: 30-day-ai-series
description: Edit a raw talking-head video into Jack's "30 Day AI Series" style — the approved Day 13 look: mostly his real footage with clean word-synced captions above the head and face-aware punch-ins, small taped paper notes with hand-drawn ink ticks placed beside him (never on his face) on each key moment, and only a few short ink-on-paper pages (day card, CTA card, end card), finished with sound design (a music bed only if he asks) and a -14 LUFS master. Handles single-take and multi-take recordings from an iPhone. Use when Jack asks for a 30 Day AI Series episode, a "Day N" video, or "edit this like Day 1 / Day 2". Built on HyperFrames + ffmpeg. Also use for every new Day N idea, script, hook or caption (loads hook-lab, short-script, viral-shorts-course + viral-hook-creator).
---

# 30 Day AI Series

A vertical (1080×1920, 30 fps) talking-head edit. **The default look is Day 13** (Jack, 3 Nov 2026: "super good clean and nice … all our series days are now way more like that"):

- **Face, most of the time** — Jack's real footage, never cut out or regraded. Clean captions sit above his head; cuts and long takes move with face-aware punch-ins.
- **Paper notes on his footage** — one small taped paper note per key moment (a counter, ink bars, a checklist that ticks, a "who/what" card), landing on its word, placed from the face track beside him or low on his chest, never over his face. Ink ticks and crosses draw on by hand. No glass boxes, no capsules (Day 12 note).
- **A few paper pages** — plain grain paper with ink type, ≤ ~2.5 s each: the Day N card, a CTA card, the end card. Never chained.

Approved references: **Day 13, "AI receptionist for wedding venues" — the default** (`assets/day13-kit/`, `projects/Series/30 Day AI Series/Day 13 - AI Receptionist for Wedding Venues/Exports/Day 13 - V1.mp4`; read `references/day13-audit.md` first, then `references/day14-audit.md` for cutting and screens). Older: Day 1, "Claude motion graphics" (`assets/build-day01.py`, `projects/Series/30 Day AI Series/Day 1 - Claude Motion Graphics/Exports/Day 1 - Final.mp4`), Day 2, "sketch to website" (`assets/build-day02.py`, `projects/Series/30 Day AI Series/Day 2 - Sketch to Website/Exports/Day 2 - Final.mp4`: several takes, hook voiceover, no music), and Day 3, "make your own AI creator" (`assets/build-day03.py`, `projects/Series/30 Day AI Series/Day 3 - Make Your Own AI Creator/Exports/Day 3 - Final.mp4`: screen recordings, before/after slider, music version, hook experiments). Every rule came from his review notes — read `references/day13-audit.md`, `references/day14-audit.md`, `references/rules.md`, `references/day2-audit.md`, `references/day3-audit.md`, `references/day6-audit.md`, `references/day9-audit.md` and `references/day10-audit.md` before designing anything. Load this skill at the start of every episode; never rebuild an episode by copying the last one from memory.

## Stack

HyperFrames (composition, render) · ffmpeg (cuts, voice, master) · `npx hyperframes transcribe --engine parakeet` (word timings) · Vision via `scripts/faces.swift` (face boxes) · MusicGen via `scripts/musicgen.py` when no licensed bed exists. Load `/hyperframes` and `/hyperframes-core` before writing composition HTML.

## Script and hooks (new ideas, before he films)

Whenever Jack has a new idea or asks for a script, load `hook-lab` (hooks), `short-script` (scripts), `viral-shorts-course` (structure, retention) and `viral-hook-creator` (extra hook patterns) first, and write the script with them before anything is filmed. Put the plan in his Notion Social content database with `notion-socials`:
- **Hooks:** 3–5 options from different patterns; each works muted on the first frame and opens a loop in ≤5 words where possible.
- **Structure:** hook → foreshadow the payoff (line 2, hook + foreshadow < 4 s) → first action (never "let's get started") → middle written as "but / therefore", never "and then" → payoff held to the end, with a twist → end right after it. The series sign-off/CTA stays, but ≤2.5 s.
- **Words:** 5th-grade reading level; swap "business", "strategy", "profit", "workflow" for plain words.
- **Shot list:** with the script, list the screen recordings, results and b-roll each beat needs, so they're filmed the same day.

## Workflow

0. **Colour.** iPhone footage is HDR: run `scripts/sdr.sh` on every clip first. Never grade or filter his footage.
1. **Understand the take.** Set up with `tools/new-video.sh` (CLAUDE.md → Folders). Probe it, transcribe it, contact-sheet it. Parakeet sometimes drops a whole sentence: look for word gaps over ~2 s where the audio is loud and re-transcribe that stretch with Whisper (`--engine whisper --model medium.en`). If he sends footage he already cut himself (dead air out, his own teaser or riser), keep his edit: skip step 2 and use his file as the A-roll (cut points from `ffmpeg -vf scdet`). Know the story, every product named, and every "this / here / like this" that needs a visual. **Save every piece of b-roll** in the footage to the shared library (`FOLDER="<type folder>" NAME="<what it shows>" sh tools/broll-save.sh`, then a row in `broll/INDEX.md`) — every edit adds to it.
2. **Cut** (`references/workflow.md` § Cut) — he goes off-script so sentences make sense: keep the setup lines the next sentence needs, and read the cut back sentence by sentence: silences from `silencedetect`, words from Parakeet; keep the best take of each line; remove fillers, false starts, repeated takes, dead pauses, **and sniffs/breaths at segment edges** (noise-like, high-frequency, low level). Then `scripts/tighten.py` takes every pause inside and between lines down to ~0.12 s, and you read each line's head and tail for stutters ("he-here's") and untranscribed "uh"s — Day 14: he expects you to catch these, not him. One take: `edit/edl.json` + `scripts/make-aroll.sh`. Several takes: `scripts/snap.py` + `scripts/cut_multi.py`. Re-transcribe the cut and check every join: word count and energy envelope, no doubled or clipped syllable; `scripts/endcheck.py` must report no clipped endings. Read every hook word against the audio.
3. **Plan the scenes** as a beat sheet with on-screen change times: nothing holds longer than ~1.5 s without a change, no layout longer than ~2.5 s; each key moment gets one paper note over his footage (Day 13), with punch-ins between notes; every answer has its question in the cut; apps and sites are real screenshots/recordings (never drawn UIs). Check `broll/INDEX.md` (workspace root) for cutaways before anything else; it lists each clip's usable windows and where it was used.
    Hook = first ~1.3 s on his face with a kinetic caption, then a page. Pick pages only where a visual earns it; pick from `references/scene-library.md` first.
4. **Build** from `assets/day13-kit/` (copy its files into `edit/`, write a new `pagesNN.py` for the episode's notes and pages; see the kit's README). Older generators (`assets/build-day03.py`, Day 1 and 2) only for their patterns: tokens → caption groups, face samples → zoom windows, scenes → pages, SFX list (music bed only if he asks). Websites use real captures (`npx hyperframes capture`); generated images and posts are the real originals found on disk; clips in phones/cards are subject-tracked (`scripts/trackcrop.py`). Animations are causal (things appear when something reaches them), clicks are real cursor clicks.
5. **Check, then look properly.** `npx hyperframes check` must pass. Then step through every page at 0.1–0.25 s intervals (`npx hyperframes snapshot --at …`) — single snapshots miss peeking text and dead holds. Run a design-critique pass on the frames.
6. **Render, QA, master.** `npx hyperframes render -q delivery --sdr`, then `python3 -I scripts/qa.py <render> --out edit/qa-vN` (jump cuts, audio pops, captions over the face) and `scripts/master.sh <render>`. Copy the QA report to `edit/qa-latest.json`, rebuild (flagged jumps get focus pulls) and re-render until clean.
7. **One edit by default.** Make one version unless Jack asks for another. If he does: `tools/TRIAL-REELS.md`, a contrasting recipe (different hook and first frame, a third of the beats changed), `sh tools/render-trials.sh <project> <job> 1 2`. A second version is evergreen: no "day seven of 30", no "see you on day eight", no day page, 30-block tracker or Day N end card; it ends on the CTA (`references/rules.md` § Trial reels).
8. **Music and hook tests only when he asks.** Music: `scripts/bed.sh` + `scripts/mixbed.sh`, happy bright acoustic bed, low. Hook experiments: `HOOK=n`.
9. **Deliver** to the video's `Exports/` folder (`projects/Series/30 Day AI Series/Day N - <Title>/Exports/`, `tools/render-trials.sh` writes there), older renders in `Drafts/`, and list what changed against his notes. Once approved, fill in "Used in" in `broll/INDEX.md` for the library clips this edit used.

## References

| File | Use |
| --- | --- |
| `references/day13-audit.md` | **The approved look (Day 13) and the Day 12 notes behind it**: paper notes off his face, ink ticks, captions that read on any background, speaker tags, punch-ins through long takes, the CTA + end card. Read first, every episode. |
| `references/day14-audit.md` | **Day 14 notes:** tighten every pause (`scripts/tighten.py`), catch stutters and untranscribed "uh"s yourself, full-resolution screens, the payoff site big, a head-turn push/tilt/pan, live product pages, page type clear of the social buttons, 3 versions + music. Read every episode. |
| `references/rules.md` | Jack's hard rules. Non-negotiable. |
| `references/style-system.md` | Palette, type, captions, page chrome, motion, transitions, sound, framing. |
| `references/scene-library.md` | Approved page patterns with timing and build notes. |
| `references/workflow.md` | Exact commands for every stage. |
| `references/day2-audit.md` | Every Day 2 mistake, its root cause and the fix — read before multi-take or iPhone jobs. |
| `references/day6-audit.md` | Day 6 notes: pacing (a change every 1–1.5 s), overlays on his footage, buzzword stickers, real screenshots only, logos never recoloured. Read before every episode. |
| `references/day10-audit.md` | Day 10 notes: mostly his face with captions, pages ≤ ~2.5 s, overlays for lists/schedules/footage, real footage for places, keep off-script setup lines so sentences make sense. Read before every episode. |
| `references/day9-audit.md` | Day 9 notes: never crop web pages, rings inside the zoom layer, real screen recordings retimed to his words, pages that don't earn their time become stickers. Read before every episode with screens. |
| `references/reference-motion-reel.md` | Jack's interactivity benchmark ("5M views in 35 days" reel): a prop per phrase, a new visual state every ~0.5–1 s, pictures land on their word. Read before planning scenes. |
| `references/day3-audit.md` | Every Day 3 note, root cause and fix, plus what he loved — read before jobs with screen recordings, generated images or before/after clips. |
| `assets/day13-kit/` | **Start here.** The Day 13 build: `build.py` (captions, camera, assembly), `pages12.py` (paper-note helpers: `spot`, `note`, `plist`, `mark`/`draw`, `timer`), `pages13.py` (Day 13's notes, day card, part 2 card, end card, call punch-ins), CSS, `mktokens.py`, `mkfaces.sh`. |
| `assets/template.html` | Composition shell: fonts, CSS for every component, timeline helpers (`enter`, `rev`, `word`, `focus`). |
| `assets/build-day01.py` | Day 1 generator (single take, music bed). |
| `assets/build-day02.py` | Day 2 generator (multi-take, mini apps, keyboard URL, real-site shots, no music). |
| `assets/build-day03.py` | Day 3 generator (video layer, before/after slider + payoff strobe, drag-and-drop, causal network pages, hook experiments via `assets/hooks-day03.py`). |
| `scripts/` | `sdr.sh`, `cut.py`, `make-aroll.sh`, `snap.py`, `tighten.py`, `cut_multi.py`, `endcheck.py`, `retime.py`, `realign.py`, `qa.py`, `faces.swift`, `people.swift`, `trackcrop.py`, `master.sh`, `musicgen.py`, `bed.sh`, `mixbed.sh`. |

## Assets that are not in this repo

Fonts (Archivo, Playfair Display, IBM Plex Mono) and sound effects come from Jack's local asset library (LenoFX library, Kenney, Mixkit — see his memory notes for the path). They are licensed for his edits only; never commit them here. Logos come from `npx hyperframes media-use resolve --type logo` (official marks only, never redrawn).
