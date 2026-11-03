# Video Editing

Claude is the editor. Jack supplies footage and references; Claude cuts, designs, animates and renders.

## Locked stack

| Job | Tool |
| --- | --- |
| Composition, motion, captions, final render | HyperFrames (`npx hyperframes`), GSAP timelines |
| Cutting, conforming, loudness, frame grabs | ffmpeg / ffprobe |
| Word-level transcripts | `npx hyperframes transcribe` (Parakeet engine; whisper-cpp fallback for other languages) |
| Silence and dead-air removal | auto-editor |
| Downloading reference videos | yt-dlp |

Do not use Remotion. Do not use anything in `_archive/` as a source of style, code or decisions; it is old work kept only on disk.

## Folders

- `skills/` — custom style skills, one folder per style. Source of truth; install a finished skill by symlinking it into `~/.claude/skills/`.
- `references/<style>/` — reference videos and frame breakdowns for a style.
- `footage/<job>/` — raw clips for an edit. Never modify originals.
- `broll/` — Jack's shared b-roll library, catalogued in `broll/INDEX.md`. Check it before choosing cutaways; new clips get a sheet via `tools/broll-sheet.sh` and a row in the index.
- `projects/<yyyy-mm-dd>-<job>/` — one HyperFrames project per edit.
- `exports/` — renders land in `exports/<yyyy-mm-dd>-<job>/` on the Mac, then move to the SSD's `exports/`, sorted for Jack with readable names (no dates):
  - `Series/<series name>/Day N - <Title>/Day N - V1.mp4`, `Day N - V1 (music).mp4`, … (e.g. `Series/30 Day AI Series/Day 6 - Build Your Own App/`)
  - `Other Videos/<Title>/<Title> - V1.mp4` for one-offs (e.g. `Other Videos/Learn AI From Zero/`)
  - older versions in `Drafts/` (`… - draft v1.mp4`), hook tests in `Hook Tests/`. A new series gets its own folder under `Series/`.
- **Media lives on the SSD, not the Mac.** `footage/<job>`, `projects/<project>`, `broll/<clip>` and `_archive` are symlinks into `/Volumes/Extreme Pro/Jack - Organized/04 Media/Video Editing/Claude Edits/`; finished renders move to its `exports/` once delivered (layout above). The SSD must be mounted to edit.
- **On the SSD everything is named for Jack, not with dates or numbers.** `footage/`, `projects/` and `exports/` all use the same tree: `Series/<series name>/Day N - <Title>/` and `Other Videos/<Title>/`. Footage folders hold his clips directly (original file names, never renamed). Project folders hold the HyperFrames project(s) under their code id (`<yyyy-mm-dd>-<job>`, `…-trials`), because builds find siblings by that id. The Mac side keeps short code names as links (`footage/<job>`, `projects/<yyyy-mm-dd>-<job>`) pointing into the readable SSD folders.
- **New job:** pick its place and title first (`Series/<series>/Day N - <Title>` or `Other Videos/<Title>`; a new series gets its own folder under `Series/`), create `footage/<that>/` and `projects/<that>/<yyyy-mm-dd>-<job>/` on the SSD, link them back (`ln -s`), and move his clips out of Downloads into the footage folder. Keep the tree tidy as you go: no loose files, no date-only or number-only folder names, no duplicate copies.
- `tools/` — helper scripts shared across edits, including the trial-reel playbook (`tools/TRIAL-REELS.md`).

## Working rules

- Default canvas is 1080x1920 at 30fps unless the job says otherwise.
- Run `npx hyperframes check` and look at snapshots before every render.
- Show a draft (preview or snapshots) before the final render of a new style.
- Media files are git-ignored; only skills, tools and project source are committed.
- **Every edit feeds the b-roll library.** While reviewing a job's footage, save every piece of b-roll (whole cutaway clips, and cutaway moments inside longer clips: screen recordings, hands, desk, establishing shots) with `NAME="<what it shows>" sh tools/broll-save.sh <clip> [start end]`, look at its sheet and add a row to `broll/INDEX.md`. Skip only talking-to-camera footage and unusable shots (blurry, accidental). After the edit is approved, fill in "Used in" for every library clip it used.
- **Every video ships as 2 versions** for Jack to choose from (from Day 5 on, every series; he has no Instagram trial-reel option, so five was overkill). Same series style; hooks, script and editing mixed up so each is distinct. Follow `tools/TRIAL-REELS.md` (recipes, distinct-enough check, build with `TRIAL=n`, render with `sh tools/render-trials.sh <project> <job> 1 2`). His notes apply to both. Deliver to the SSD's `exports/Series/…` or `exports/Other Videos/…` folder as `<Title> - V1/V2.mp4` with a table of what differs.
- **Edits run in the chat on Jack's Claude plan.** Don't use `tools/api-edit.py` or the API credit for edits (Jack, 3 Nov 2026: the credit is nearly out).
- **Always load the style's skill first** (e.g. `30-day-ai-series`) for every episode and follow its rules and audits; never rebuild an episode by copying the last one from memory. **Day 13 is the approved series look** (Jack: "super good clean and nice … all our series days are now way more like that"): mostly his face with clean captions, one small taped paper note with ink ticks per key moment placed off his face, punch-ins through long takes, speaker tags for other voices, about three short pages (day card, CTA card, end card). Start every episode from `skills/30-day-ai-series/assets/day13-kit/` and read `references/day13-audit.md`. Pacing: something changes every ~1–1.5 s; real screenshots only, no drawn app UIs. **The video is mostly Jack with captions**: paper pages/canvases only to show one thing for a few seconds; everything else is an overlay on his footage. **He goes off-script, usually so the next sentence makes sense**: keep those lines and check every sentence in the cut makes sense.
- **No fight sound effects, no repeated whoosh/click bursts.** Never put sound effects on sword slashes, fights, hits or clashes, and never fire the same effect again and again in a row (Jack hated the repeating whoosh + click in Terra vs Sol). Character fights and action stay silent unless he asks for sound.
- **New ideas and scripts:** load `viral-shorts-course` and `viral-hook-creator` first and follow the style skill's "Script and hooks" section (3–5 hook options, foreshadow, but/therefore middle, payoff at the end, 5th-grade words).
- **In a series, V2 is evergreen.** V2 gets posted at a different time, so it never says which day it is: cut "this is day N of 30", "see you on day N+1" and "that wraps up day N", and drop the day page, the 30-block tracker and the Day N end card. End V2 on the CTA (or the payoff); its caption has no day number either. V1 keeps the series framing.
- **Ask for what the versions need when he films:** a couple of different hook takes, and the screen recordings, results and b-roll each beat needs.
