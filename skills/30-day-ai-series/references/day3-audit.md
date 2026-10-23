# Day 3 audit — what went wrong, what fixed it, what Jack loved

"Make your own viral AI creator": one 8-minute take full of retakes and interruptions, six Mac screen
recordings, a third-party dance clip and its AI swap. Approved at v5 (plus music version and hook experiments).
Read this with `day2-audit.md` before any job that uses screen recordings, generated images or before/after clips.

## Jack's notes and their fixes

| # | Note | Root cause | Fix (now in the skill) |
| --- | --- | --- | --- |
| 1 | Hook caption said "how you can't do it" — he says "can too" | Parakeet misheard; I trusted it on the hook | Read every hook word against the audio; when a phrase looks odd, re-transcribe that window with whisper medium and listen |
| 2 | "anything", "MCP", "platforms", "simple" cut off early | `snap.py` ended a line at the first 50 ms quiet run, which happens *inside* words | `snap.py` now waits for 150 ms of quiet; `scripts/endcheck.py` flags any line whose voice is still going after the cut (it catches all four) |
| 3 | Dancer not centred in the phone, "can barely see the character" (twice) | Page video wasn't sized (showed its corner) and the clip wasn't framed on the person | `video.pv` sizing in the template; `people.swift` + `trackcrop.py` keep the person centred; check phone/card videos in the real render, not snapshots |
| 4 | Step 4 titles and numbers badly laid out | Each step page improvised its header | One `step_head()`: small "step", big number, title row complete and centred |
| 5 | Wanted a real drag: cursor drags the clip and the sheet onto the prompt box, they highlight as chosen | Files just flew in | Cursor grabs → carries over the box (dashed drop zone lights) → drops → attachment chip with a dark ring and tick |
| 6 | Wanted the result with the source song and a strobe back to the original | Result played silent, alone | Payoff: AI full screen + source music → strobe AI/original with a punch on every switch → side by side with labels |
| 7 | Too much glitching between pages at the end, his face for a split second | Back-to-back pages each crossfaded to the face | Page-to-page handoffs dissolve directly; the old page waits until the new one is in; no face shot under ~1 s between pages |
| 8 | Road-map line was already drawn before its nodes | One path animated independently of the nodes | Draw each segment from node to node as the next node lands |
| 9 | Hook cards should play his real posts | Stills | Any "post / account / video" on screen is a playing video when one exists |
| 10 | Claude → Higgsfield line kept rebounding | A packet on `repeat:4` | Connections happen once, slowly, then a payoff (pulse, rings, "connected" tick) |
| 11 | Character highlight ring cut off her name; output covered the input | Ring sized to the photo only; result wiped over the grid | Highlight rings include the label strip; flows read top → bottom: input, prompt, then the output below |
| 12 | "hallucinate" needed a visual | Plain face | Abstract words get a metaphor: the face card glitches through other characters' faces, ghosted word, "which face?" |
| 13 | Prompt done → send should light up and a mouse click it (step 4 and the comment) | Send just changed colour | Send highlights and pulses, cursor glides in and clicks it (position measured with a temporary marker colour) |
| 14 | API lines arrived at nothing, then icons; "posted" too small and too quick | Lines, dots and icons on separate timings | Causal: each line draws with its dot, the icon pops when it arrives, then ticks; "posted" centred under the text and held |
| 15 | "Multiple videos a day" needed a visual | Face only | Six real posts pop into a grid on the phrase |

## What I caught myself
- Page videos nested in a timed page don't play (HyperFrames rule) → page videos live in one top layer (`VL` / `overlay()`), mirroring their page's motion and fade.
- Captions ended up under that layer → `.cap { z-index: 60 }`, layer at 40.
- Class-name clashes again (`.chip`, `.ct`) → every new component gets a prefix.
- A page starting 0.2 s after a cut flashed the new take → `scene()` snaps starts back onto a cut; `cover_cut()` holds a page end over a nearby cut.
- The disk filled twice mid-render → check free space first; under ~4 GB render with `--workers 1`; delete regenerable frames (faces, tracking, snapshots).
- Tracking/timing values for a cursor were guessed once → measure the target in a snapshot (paint it a marker colour, find the pixels).

## What Jack loved
- The original | AI side by side ("so cool") — it became the hook on "exactly", with the line gliding left/right and splitting outwards to reveal him.
- Real everything: his own posts in cards, his real prompts typed out, the original 4K generated images (found on disk under Claude's scratch workspaces / his AI Content folder), real screen recordings for a few seconds only.
- Mouse interactions that actually click things; smooth, causal animations (things appear because something arrived).
- Two versions (with/without music) and hook experiments to test.

## Habits that worked
- Find the real source assets on disk (`mdfind -name`) instead of screenshots of screen recordings.
- Frame-step every page, then check the *render* for anything with video in it.
- After each note, apply the same fix everywhere the pattern appears (both phones, both send buttons, every page handoff).
