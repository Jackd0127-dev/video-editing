# Day 13 kit — start every episode here

The build behind the approved Day 13 look (`references/day13-audit.md`). Copy these files into a new project's `edit/` and keep the machinery; write only the episode's own `pagesNN.py`.

| File | What it is | Change per episode? |
| --- | --- | --- |
| `build.py` | Tokens → caption groups (speaker tags, breaks on speaker change), face-aware camera (zoom-out at 0 s, punch-ins on segment starts + `call_edges()`), caption placement above the head (hair-aware), pages, SFX, assembly | Only the recipe block (`if N == 1: …`), `DURATION` tail, `KEEP`/`ITAL` word sets, and the `exec(open("edit/pagesNN.py"))` line |
| `pages10.py`, `pages10b.py` | Older helpers still used (`hold_cam`, stopwatch, glass helpers — don't use glass) | No |
| `pages12.py` | **Paper-note helpers:** `spot()` (position off the face from the face track), `note()` (taped paper note, 1.35× zoom, holds the camera, forces captions above the head), `plist()` (checklist with ink ticks), `mark()`/`draw()` (ink tick/cross that draws on), `timer()` | No (its `hook12()` etc. are Day 12 examples) |
| `pages13.py` | **Day 13 examples to copy from:** `pg_day13()` day card, notes (`jess13` who-answered card, `guests13` counter, `capacity13` ink bars + cross, `menu13` checklist ticked by the other speaker, `always13` 24/7), `pg_part2()` CTA card, `pg_end13()` end card, `call_edges()` punch-ins through a long take; `TEASER_END`, `HAIR`, `UNDER_CHIN` settings | Write a new `pagesNN.py` from it: day number, blocks lit, the episode's notes |
| `pages14.py` | **Day 14 helpers to copy from:** `screen()` (his screen recording in a white card, retimed to his words at full resolution; moves above his head with captions under the chin when his face sits low), `zoom_to()`/`ring()` (zoom + hand-drawn ink ring inside the zoom layer), `site_window()`/`scroll_to()` (a site big, scrolled to what he names), the head-turn push/tilt/pan (in `claude14()`), `crmsite14()` (his CRM landing page), `pg_next()` ("What next?" CTA kept clear of the social buttons), `pg_end14()` | Write a new `pagesNN.py`; reuse the helpers |
| `day6.css` … `day12.css`, `day13.css`, `day14.css` | Component CSS; `day13.css` = speaker tag, ink bars, comment card, **bright-footage captions (no scrim/vignette, ink words)** — drop that last block for dark rooms; `day14.css` = screen cards, ink rings, big site window, white captions for dark rooms | Only the caption-colour block |
| `template.html` | Composition shell | No |
| `mktokens14.py` | Day 14 version for multi-take cuts: tokens from `edit/trials/<n>/words.json` (after `scripts/tighten.py --words`) + mishear fixes | Yes |
| `mktokens.py` | Parakeet words + mishear fixes + words Whisper recovered + speaker tags (`JESS = [...]`) | Yes: this episode's fixes |
| `mkfaces.sh` | Face boxes (2 fps) + energy envelope for a trial | No |

`build.py` here is Day 14's (its recipe block runs three versions, `TRIAL=1/2/3`; captions honour `CAPBELOW`/`CAPAT` from `pages14.py`). Day 13's recipe is in the Day 13 project.

Run from the project root: `TRIAL=1 python3 -I edit/build.py` → `../<project>-trials/out/trial-1.html`; render with `sh tools/render-trials.sh projects/<project> <project> 1 2`.
