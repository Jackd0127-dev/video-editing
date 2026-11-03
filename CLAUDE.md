# Video Editing

Claude is the editor. Jack supplies footage and references; Claude cuts, designs, animates and renders. This workspace is for editing only: scripts, hooks and content plans are written elsewhere.

## Locked stack

| Job | Tool |
| --- | --- |
| Composition, motion, captions, final render | HyperFrames (`npx hyperframes`), GSAP timelines |
| Cutting, conforming, loudness, frame grabs | ffmpeg / ffprobe |
| Word-level transcripts | `npx hyperframes transcribe` (Parakeet engine; whisper-cpp fallback for other languages) |
| Silence and dead-air removal | auto-editor |
| Downloading reference videos | yt-dlp |
| Ready-made effects, overlays, kinetic type, transitions, charts | `hyperframes-registry` (about 450 blocks, `hyperframes add`): check it before hand-building any effect, then restyle it to the video's look |
| Fonts, sound effects, overlays (optional) | Jack's LenoFX library on the SSD, `/Volumes/Extreme Pro/Jack - Organized/04 Media/Video Editing/Asset Library/` (index: `Catalog/assets.csv`; no music in it). Use it when an edit wants it; licensed for his edits only, so never commit it. |

Do not use Remotion.

## Folders

- `skills/` — custom style skills, one folder per style. Source of truth; install a finished skill by symlinking it into `~/.claude/skills/`.
- `references/<style>/` — reference videos and frame breakdowns for a style.
- `broll/` — Jack's shared b-roll library, catalogued in `broll/INDEX.md`. Check it before choosing cutaways.
- **Everything for a video lives in one folder on the SSD.** `/Volumes/Extreme Pro/Jack - Organized/04 Media/Video Editing/Claude Edits/` holds only `projects/`, `broll/` and `references/`. Each video is `projects/Series/<series name>/Day N - <Title>/` or `projects/Other Videos/<Title>/`, always with three folders inside:
  - `Footage/` — his raw clips, original file names. Never modify or rename them.
  - `Project/<yyyy-mm-dd>-<job>/` (and `…-trials`) — the HyperFrames project(s), under their code id because builds find siblings by that id.
  - `Exports/` — finished videos: `<Video title>.mp4` (extra versions `Day N - V2.mp4` or `<Title> - V2.mp4`, music `… (music).mp4`), `NOTES.md`, older renders in `Drafts/`, hook tests in `Hook Tests/`. `tools/render-trials.sh` writes here directly.
- **Named for Jack:** folders and files say what they are, no date-only or number-only names, no loose files, no duplicate copies. A new series gets its own folder under `Series/`.
- **The Mac side only holds short links** into those folders for the code: `footage/<job>`, `projects/<yyyy-mm-dd>-<job>`, `broll/<clip id>`. No video files on the Mac. The SSD must be mounted to edit.
- **New video:** `sh tools/new-video.sh "Series/30 Day AI Series/Day N - <Title>" <yyyy-mm-dd>-<job> <short-name>` (or `"Other Videos/<Title>"`), then move his clips out of Downloads into its `Footage/`.
- `tools/` — helper scripts shared across edits, including the trial-reel playbook (`tools/TRIAL-REELS.md`).

## Working rules

- Default canvas is 1080x1920 at 30fps unless the job says otherwise.
- Run `npx hyperframes check` and look at snapshots before every render.
- Show a draft (preview or snapshots) before the final render of a new style.
- Media files are git-ignored; only skills, tools and project source are committed.
- **Every edit feeds the b-roll library, so it keeps growing.** Whenever footage has any b-roll, always extract it: whole cutaway clips and cutaway moments inside longer clips (screen recordings, hands, desk, establishing shots). Save each with `FOLDER="<type folder>" NAME="<what it shows>" sh tools/broll-save.sh <clip> [start end]`. Clips are sorted by type of shot in detailed folders (`Screen Recordings/Claude`, `Working at a Laptop/Typing`, `Phone Calls`…): use the folder that fits, and if none does, name a new detailed one and it gets created. Look at its sheet and add a row to `broll/INDEX.md`. Skip only talking-to-camera footage and unusable shots (blurry, accidental). After the edit is approved, fill in "Used in" for every library clip it used.
- **One edit by default.** Make one version of each video. Jack asks by hand when he wants extras: a second version or a music version only when he says so for that video (`tools/TRIAL-REELS.md`, `sh tools/render-trials.sh <project> <job> 1 2`; music with `MUSIC=` and a happy bright acoustic bed).
- **Edits run in the chat on Jack's Claude plan.** Don't spend API credit on edits.
- **Always load the style's skill first** (e.g. `30-day-ai-series`) for every episode and follow its rules and audits; never rebuild an episode by copying the last one from memory. **Day 13 is the approved series look** (Jack: "super good clean and nice … all our series days are now way more like that"): mostly his face with clean captions, one small taped paper note with ink ticks per key moment placed off his face, punch-ins through long takes, speaker tags for other voices, about three short pages (day card, CTA card, end card). Start every episode from `skills/30-day-ai-series/assets/day13-kit/` and read `references/day13-audit.md`. Pacing: something changes every ~1–1.5 s; real screenshots only, no drawn app UIs. **The video is mostly Jack with captions**: paper pages/canvases only to show one thing for a few seconds; everything else is an overlay on his footage. **He goes off-script, usually so the next sentence makes sense**: keep those lines and check every sentence in the cut makes sense.
- **Before sending Jack anything, run `tools/PRE-DELIVERY.md`** and say what you checked and what you couldn't.
- **Thumbnails only when he asks:** `tools/THUMBNAILS.md`.
- **No fight sound effects, no repeated whoosh/click bursts.** Never put sound effects on sword slashes, fights, hits or clashes, and never fire the same effect again and again in a row (Jack hated the repeating whoosh + click in Terra vs Sol). Character fights and action stay silent unless he asks for sound.
- **If he asks for a second version of a series video, it's evergreen.** It gets posted at a different time, so it never says which day it is: cut "this is day N of 30", "see you on day N+1" and "that wraps up day N", and drop the day page, the 30-block tracker and the Day N end card. It ends on the CTA (or the payoff), and its caption has no day number either. The main edit keeps the series framing.
- **Ask for what the edit needs when he films:** the screen recordings, results and b-roll each beat needs.
