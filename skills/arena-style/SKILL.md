---
name: arena-style
description: Edit a raw talking-head video in Jack's "Arena" style — a crowd of little animated pixel-art agents (coder, coffee, headphones, chef, wizard, reader, detective, rocket) acts out what he says on clean bone-paper pages and over his untouched footage: they battle with swords and guns, fill a tournament bracket, get knocked out, and the winner puts on a crown. Ink type, one coral accent, word-synced captions above his head. Best for AI-agent, competition, ranking, "X vs Y" and scale videos. Use when Jack asks for the Arena style, the pixel agents, or "like the 100 Claude agents video". Built on HyperFrames + ffmpeg.
---

# Arena

The idea he talks about is acted out by characters. Whatever the video is about, a crowd of small pixel agents does it: one agent gets a bad answer, 99 more pop out, they arm up and fight, they fill a bracket, a judge knocks them out, one picks up the crown. The characters are the hero; the page around them stays quiet and clean.

Approved reference: "100 Claude Agents Arena" (29 Oct 2026), project `projects/2026-10-28-claude-agents-arena/`, generator `assets/build-claude-agents-arena.py` on `assets/template.html`, sprites from `assets/sprites.py`. Read `references/rules.md` before designing; numbers live in `references/style-system.md`; commands in `references/workflow.md`.

## Workflow

1. **Understand the take.** Set up with `tools/new-video.sh`; all of a video's files live in one SSD folder (CLAUDE.md → Folders). iPhone HDR goes through `skills/30-day-ai-series/scripts/sdr.sh` first. Transcribe with Parakeet, contact-sheet it, and save any b-roll to `broll/`.
2. **Cast it.** List what he says as things characters can do: gets the prompt, thinks differently, fights, gets knocked out, wins. Each beat gets one causal action tied to one spoken word. Anything that can't be acted out stays his face and captions.
3. **Cut tight.** Last clean take of each line; retakes, half-words, untranscribed "uh"s, fillers and dead air out, every pause down to ~0.1 s. Keep off-script setup lines so each sentence makes sense. Check joins on the energy envelope and re-transcribe the cut: a doubled word at a join (his "Then… then a judge") is a fail. `endcheck.py` must be clean.
4. **One edit by default.** A second version only if Jack asks (`tools/TRIAL-REELS.md`): a different hook line and first frame (cold open on one agent becoming 100), 25–30 % shorter, different treatment for at least a third of the beats, one `edit/trials/<n>/plan.json` each. In a series it's evergreen.
5. **Rhythm before pixels.** Lay the beats out as face | page windows and decide what can be a chest-band overlay instead of a page (see the page budget in `references/rules.md`).
6. **Build.** Run `sprites.py` (add new personalities there), then write the beat functions from the library in the generator: `pg_crowd`, `pg_battle`, `pg_arena`, `pg_type`, `pg_judge`, `pg_crown`, `pg_zoom`, `pg_board`, `ov_vs`, `ov_cta`… Beats are timed from his words with `w("phrase")` / `T("phrase")`, never by hand. `TRIAL=n python3 -I edit/build.py`.
7. **Check and look.** `npx hyperframes check`, snapshots of every page at its key words, zoom anything suspicious. Show Jack a look strip before the final render of a new video type.
8. **Render, QA, master:** `sh tools/render-trials.sh projects/<project> <date>-<job>`, one render at a time; it writes to the video's `Exports/`. QA passes with 0 caption/face overlaps and 0 voice-cut pops. Send it with a suggested caption.

## References
| File | Use |
| --- | --- |
| `references/rules.md` | Arena-specific rules, Jack's notes on this style, the page budget, sound rules. |
| `references/style-system.md` | Palette, type, captions, agent anatomy, sprite scales, beat library, motion. |
| `references/workflow.md` | Every command from raw clip to delivered exports. |
| `assets/template.html` | Composition shell (fonts, tokens, captions, page and agent CSS, `enter` / `idle` / `zoomTo` / `focus`). |
| `assets/build-claude-agents-arena.py` | Reference generator: word timing, agent helpers, fights, bracket, beat library, captions, camera, assembly. |
| `assets/sprites.py` | Draws every agent layer, weapon, crown and the zoom-out crowd tile as native PNGs. |

Shared scripts: `skills/30-day-ai-series/scripts/` (cut, QA, master, faces) and `skills/route-style/scripts/tighten.py` (pause splitting).
