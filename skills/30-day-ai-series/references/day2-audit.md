# Day 2 audit — what went wrong and how it was fixed

"Sketch to website", 17 raw clips, several takes per line, a separate hook voiceover. Approved at v4.
Read this before any multi-take or iPhone job.

| # | Mistake | Caught by | Root cause | Fix (now in the skill) |
| --- | --- | --- | --- | --- |
| 1 | Footage looked washed out — "colour grade over the top" | Jack, v1 | iPhone HLG clips cut to 8-bit with HLG tags; Chrome's tone-mapping plus a light `contrast/saturate` grade, a dark gradient over bright b-roll and grain on top | `scripts/sdr.sh` (Apple `avconvert`), `GRADE = ""`, grain on paper only, `--sdr` render, scrim behind caption words only |
| 2 | Render failed: "HDR pre-extraction needs 43 GB" | Me, v1 | Same HLG tags | Same as 1 |
| 3 | Hook lost "on a napkin" | Jack, v1 | I cut a line I thought was confusing | Keep every hook line he wrote; default to his last clean take (he chose take 2) |
| 4 | A different take flashed after "hey, I'm Jack" | Jack, v1 and again v3 | Page started on the word (0.24 s late), then a `data-start` rounded 0.3 ms past the cut frame | Page starts on the clip's first frame; `scene()` snaps starts down to the frame |
| 5 | "a developer-er" then "or or" | Jack, v1–v3 | Joining two takes using Parakeet word starts, which were 0.3 s off on repeated phrases | Read syllables from the energy envelope, cut inside dips, re-transcribe and count words at the join |
| 6 | Designer/developer page "terrible" | Jack, v1 | Plain rows with struck-through labels (lines also sat on the baseline like underlines) | Mini-app pile with live animation; strike lines through the word middles |
| 7 | Cursor missed the send button | Jack, v1 | Guessed coordinates | Measure the button in a snapshot |
| 8 | Website shown from his phone footage | Jack, v1 and v4 | Used a frame of his screen recording; v2 replaced two scenes but missed the wipe | `hyperframes capture` the live site; grep every use of an asset when replacing it |
| 9 | Mouse click to open a link | Jack, v1 | Default to cursor | Keyboard + return + load + scroll |
| 10 | Background music | Jack, v4 | Assumed a bed like Day 1 | No bed unless asked |
| 11 | Pages faded out before their last word was readable ("of 30", "you don't", "miss", send click, "the prompt") | Me, v1 frame-step | Page end = next word; the 0.42 s crossfade ate the payoff | Hold ≥0.4 s after the last reveal before the fade |
| 12 | Oversized serif italic words, caption over his head in b-roll, low caption contrast on bright screens | Me, v1 frame-step + QA | Defaults carried from Day 1 | Same-size accents; lift captions over that b-roll; local scrim |
| 13 | Small caption words turned green | Me, v2 frame-step | New CSS class `.cs` collided with the caption class | Prefix component classes (`sx-*`) |
| 14 | On-screen URL 404'd | Me, v1 | He says `scriptai.space/hullabaloo`; the live site is `hullabaloo.scriptai.space` | Type the address that loads; tell him |

## Habits that caught the most
- Frame-step every page at 0.1–0.25 s and read the frames as a viewer would; every self-caught issue above came from that.
- Measure, don't guess: button positions, page hold times (`last reveal` vs `fade start`), join energy, colour against Apple's frame.
- Treat each note as a class of problem: "use a real screenshot" means every website image, "fix the flash" means every page that starts on a cut.
