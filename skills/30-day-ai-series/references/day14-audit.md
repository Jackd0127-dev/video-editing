# Day 14 audit — "sell websites to local businesses"

**This is the approved look, the default for every episode** (Jack, 3 Nov 2026: "i really loved the vid u made today"). Read this first, then `day13-audit.md`. The round 4 settings are final: where earlier rounds conflict, round 4 wins.

Four phone takes (hook, intro, a long walk-through at the desk, the payoff + sign-off) plus a silent 3024×1900 screen recording (Google → Advanced Search → Maps → Karizma → Claude). Shipped as **three versions** at Jack's request: V1 series (3:04), V2 evergreen (2:06), V3 evergreen 60 s (1:03), each with and without a quiet music bed. Build: `projects/2026-11-03-day14` (`edit/pages14.py`, `edit/tighten.py`); the reusable parts are in `assets/day13-kit/` and `scripts/tighten.py`.

## Jack's notes (two rounds) and their fixes

| # | Note | Root cause | Fix (now a rule) |
| --- | --- | --- | --- |
| 1 | "so many blank spots where u havnt cut out empty sound space … start or end or middle words" | Only the joins between takes were trimmed; pauses inside a kept line stayed | **Tighten every cut:** `scripts/tighten.py` cuts every quiet run (< −42 dB, ≥ 0.18 s) inside each line down to ~0.12 s and trims each line's head/tail to the speech; it maps every word through the pieces so no caption word is lost |
| 2 | "he-here's … u need to cut out the he ffs u need to get better at noticing this stuff" | A half-word stutter just before the first word: Parakeet folded it into the word | **Read every line's head and tail in the energy envelope:** voiced audio before the first word or past the last word's natural end is a stutter or filler. Cut at the deepest dip (here 14.54 s, the dip between "he" and "here's") |
| 3 | A big gap after "web development services" | A 0.45 s "uh" Parakeet never transcribed, kept because it is loud | Same check: a voiced chunk after the last word that is not part of it gets cut. A cut that must land mid-fricative ("servic**es**") is faded over ~50 ms, or it clicks (QA flagged it) |
| 4 | The screen recording "looks very pixelated" | Clips were scaled to 1512 px, then shown in a card that zooms up to 2.6× | **Keep recordings at their native width** (3024 px, crf 17, `-tune stillimage`); only the browser chrome is cropped |
| 5 | "when showing the website make it bigger instead of so small" | The site sat in a 600 px card above his head (his face was low in that take) | **The payoff site is a big browser window** (1000 × 1230, full page captured at 2×, `site_window()` + `scroll_to()`), scrolling to the part he names with an ink ring on it; captions sit below the window. A cutaway is right here: the site is the subject |
| 6 | "make the what's next text smaller so it doesn't get clipped by socials overlays" | 190 px headline ran into TikTok/IG's right-hand buttons | CTA/page type stays inside x ≈ 120–900: headline ≤ 130 px, lines ≤ 44 px |
| 7 | "at 1:37 I turn my head … when u zoom in a bit do a subtle tilt or pan to the right" | — | When he turns, the A-roll itself (`#aroll`, inside the camera) pushes to ~1.15×, tilts ~1.4° and pans with him, then settles ~2 s later. It's on `#aroll`, not `#cam`, so it stacks on a card's camera hold |
| 8 | "change the crm screen … showcase our crm landing page, brand new" | Used an old library clip of the CRM agent | Real, current pages: capture the live site (`npx hyperframes capture` scrolls it, so scroll-reveal sections render; a plain tall screenshot leaves them blank) and show it like the client site, ringing what he names |
| 9 | "remove that let's go as we have a let's go at the end" | Kept a mid-video sign-off | One sign-off per video |
| 10 | 3 versions + music versions | — | V3 = 60 s: one beat per step, its own hook line, evergreen. Music: a steady happy acoustic MusicGen bed, loudness-normalised to −20 LUFS, then `BED_DB=-14 mixbed.sh` (~20 LU under the voice) |

## Also learned
- **Low framing:** in his payoff take his face sat at y ≈ 0.5–0.72, so a 1000 px card under the chin covered his face. `screen()` measures the room under the chin; when there isn't any, the card goes above his head (600 px), the camera eases down 1.1× from the top edge, and captions go under his chin (`CAPBELOW`).
- **Parakeet start drift at line edges:** a line's last word whose start lands past the trimmed tail must still be mapped (it was dropping "it", "yet", "us", "go").
- **`endcheck.py` skips a cut followed straight by the next word.** V2's "anywhere else," ran into "and" with no pause, so the cut clipped it (QA pop). Never end a version's line where the next word is joined on: keep the sentence going to a real pause.
- Client sites Claude built live in `~/Library/Application Support/Claude/scratch-workspaces/…/index.html` (`mdfind <business name>`). Serve them locally and screenshot with headless Chrome (fresh `--user-data-dir`). Freeze any rotating hero word with an injected style, or the capture lands mid-fade.

## Round 3 notes
| # | Note | Fix (now a rule) |
| --- | --- | --- |
| 11 | The top card is too small | Above-head screen cards are 880 px wide (see round 4: the card moves up, never a big push-in) |
| 12 | "the circles aren't going around the things properly … add a nice draw-in" | `ring()` is a rounded rectangle a fixed number of screen px outside the target (an ellipse cuts the corners of anything wide), constant on-screen stroke, drawn on in ~0.6 s with a small pen overshoot. Snapshot every ring at the moment it finishes (`RINGLOG`) |
| 13 | Show the real CRM dashboard, not lots of circles on the landing page | Landing hero first, then his real dashboard pages (Overview, Leads/Campaigns, Calls) captured from his signed-in Chrome, switching on his words; one ring for sign-up, one for revenue |
| 14 | The site windows covered his face | `low_window()`: 940 px wide, ~510–530 tall, sitting ~150 px above the bottom; the footage pushes in from the bottom edge (max 1.25×, more crops his head) so his face shows above; captions above his head |
| 15 | Show a preview before a size change | For layout changes he can't picture, send a side-by-side still of 2–3 options on real frames first |

## Round 4 notes
| # | Note | Fix (now a rule) |
| --- | --- | --- |
| 16 | "u zoomed in wayyy too much … u changed the captions" | Make room by moving the card, not by zooming him: keep the 1.1× push, card bottom stays clear of his head (top ≈ 140). Never change captions or zoom when he only asked for a size change. Say the plan back and send a still before re-rendering |
| 17 | A different clip flashes in for a split second (2:05) | `tighten.py` merges any piece under 0.45 s: a sliver shot plus two re-framings reads as a glitch |
| 18 | V2 glitches at the start | Never start a camera move during the opening zoom-out (first 0.55 s) |
| 19 | V3: constant zooming in and out | `cam_chain()`: cards under 1.5 s apart hold the zoom or glide to the next framing; camera moves ease back, never snap |
| 20 | Sound effects when needed, a riser on a cliffhanger open | A soft riser into the reveal of a cold open (with a low hit), quiet builds into hooks, a small chime on a payoff reveal |
