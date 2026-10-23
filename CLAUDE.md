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
- `exports/` — finished renders, named `<yyyy-mm-dd>-<job>-v<n>.mp4`.
- `tools/` — helper scripts shared across edits.

## Working rules

- Default canvas is 1080x1920 at 30fps unless the job says otherwise.
- Run `npx hyperframes check` and look at snapshots before every render.
- Show a draft (preview or snapshots) before the final render of a new style.
- Media files are git-ignored; only skills, tools and project source are committed.
- **Every edit feeds the b-roll library.** While reviewing a job's footage, save every piece of b-roll (whole cutaway clips, and cutaway moments inside longer clips: screen recordings, hands, desk, establishing shots) with `sh tools/broll-save.sh <clip> [start end]`, look at its sheet and add a row to `broll/INDEX.md`. Skip only talking-to-camera footage and unusable shots (blurry, accidental). After the edit is approved, fill in "Used in" for every library clip it used.
