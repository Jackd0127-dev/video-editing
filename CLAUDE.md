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
- `projects/<yyyy-mm-dd>-<job>/` — one HyperFrames project per edit.
- `exports/` — finished renders, named `<yyyy-mm-dd>-<job>-v<n>.mp4`.
- `tools/` — helper scripts shared across edits.

## Working rules

- Default canvas is 1080x1920 at 30fps unless the job says otherwise.
- Run `npx hyperframes check` and look at snapshots before every render.
- Show a draft (preview or snapshots) before the final render of a new style.
- Media files are git-ignored; only skills, tools and project source are committed.
