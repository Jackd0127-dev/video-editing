# Trial reels — 5 per video

From Day 4 on, **every video Jack makes becomes 5 trial reels**. He posts all five as Instagram trial reels
(shown to non-followers first), then promotes the one that performs best. Same series style in all five;
hooks, script and editing are mixed up so each reel is clearly its own video, not a re-upload.

## What must differ between the five

| Lever | How to vary it (pick a different option per trial) |
| --- | --- |
| **Hook (first 3 s)** — the biggest lever | Use a different opening line and a different first frame in every trial: his strongest claim on his face; cold open on the result/payoff; a question; a number/list ("3 things…"); a contrarian or "stop doing X" line; a before/after slider; a "POV" text hook over b-roll. If he recorded several hook takes, each trial gets a different one. |
| **Script / structure** | Full version · tight version (secondary lines cut, 25–40 % shorter) · result-first (payoff, then how) · steps-only · story framing (problem → discovery → result). Never invent words he didn't say: re-order, trim and choose between his takes. |
| **Editing treatment** | Within the series style: a different page/graphic for at least a third of the visual beats (pick alternates from the scene library), different caption emphasis words, faster or calmer zoom rhythm, different b-roll windows, music on/off or a different bed. |
| **Ending** | Same CTA keyword (it drives his comment automation) unless he says otherwise; vary where it lands and how it's shown. |

**Distinct-enough check before rendering** (all five must pass):
- First frame and first 3 s are visually different from every other trial, with a different opening line or on-screen hook text.
- Lengths differ: no two trials within 10 % of each other.
- At least a third of the graphics or b-roll beats differ from each other trial.
- Every trial still obeys the series rules and Jack's notes (no grade, no clipped words, captions off his face, real assets, causal animations).

Keep the series identity: palette, type, caption system, end card and the series' signature moves stay the same in all five.

## The five default recipes (adapt per video)

| Trial | Hook | Structure | Treatment |
| --- | --- | --- | --- |
| **T1 · Main** | His best hook line on his face, quick zoom | Full | The main edit, everything he has approved |
| **T2 · Result first** | Cold open on the payoff (result, before/after) | Result → how it's done → CTA | Payoff graphics up front, steps quicker |
| **T3 · Tight** | Number/list or question hook (text + his line) | 25–40 % shorter, steps only | Faster rhythm, fewer pages, punchier captions |
| **T4 · Story** | Problem / contrarian line | Problem → discovery → result | Calmer pacing, more b-roll, music version |
| **T5 · Wildcard** | The most experimental hook (feed/deck/zoom-out, POV over b-roll) | Full or result-first | Alternate graphics for most beats |

## How to build them (one cut, five recipes)

1. Make the main edit (T1) as usual and get the notes in. **Notes apply to all five.**
2. Plan the other four in `edit/trials/<n>/spec.json` — hook, structure, treatment, target length, why it's distinct — and show Jack the five-line plan with the first round.
3. Structure changes get their own cut: `edit/trials/<n>/segments.json` → `cut_multi.py` → `assets/video/aroll-t<n>.mp4` + `edit/trials/<n>/words.json`, re-transcribe, `endcheck.py`, faces. Hook-only changes reuse the main cut.
4. The project's `edit/build.py` reads `TRIAL=<n>` (like Day 3's `HOOK`/`FULL`) and writes `../<project>-trials/out/trial-<n>.html`.
5. Render, QA and master all five: `sh tools/render-trials.sh projects/<project> <date>-<job> [1 2 3 4 5]` (add `MUSIC=path/to/bed.wav` for music versions).
6. Deliver `exports/<date>-<job>-trial<n>.mp4` (and `-music`), with a table: trial, hook line, length, what's different, suggested on-screen title.
