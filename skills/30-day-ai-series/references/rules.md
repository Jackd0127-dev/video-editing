# Jack's rules

Each one came from a review note. Breaking any of them got a version rejected.

## The approved look (Day 13 — the default for every episode)
Jack, 3 Nov 2026: "i loved day 13 it was super good clean and nice … all our series days are now way more like that." Details and the build kit: `references/day13-audit.md`, `assets/day13-kit/`.
- **Mostly his face with clean captions.** About three paper pages per video: the Day N card, a CTA card, the end card (each ≤ ~2.5 s).
- **One small taped paper note per key moment, on his footage**, landing on its word: counters, ink bars, checklists that tick, a "who/what" card. Placed from the face track (beside his face, or low on his chest in close-ups), **never on his face or hair**, never over what his hands are showing. One note at a time; between notes, his face + captions + a punch-in.
- **Hand-drawn ink ticks and crosses** that draw on with the word. **No liquid-glass boxes, no capsules, no stock tick icons** — Day 12: "they look like ai slop … but i dont want basic white capsules".
- **Every answer has its question first** (Day 12: "the answer is no, it can't" with no question before it "seems like a bomb drop out of nowhere"). Go find the line in the other takes.
- **Captions read on any background:** ink captions with a soft light halo over bright backgrounds (sky, white walls), white over dark rooms; no template top scrim or vignette on bright footage. Above his head, never under the chin when notes sit on his chest.
- **Other voices get a speaker tag** (a small typewriter label above their caption lines, e.g. "JESS · AI RECEPTIONIST"); caption groups break on every change of speaker.
- **Long single takes get a punch-in on every change of speaker** and on sentence starts more than ~3 s apart.
- **When he pre-cuts the footage himself, keep his edit** (his teaser, riser and on-screen text); add the zoom-out at 0 s, no captions over his own text.
- **End:** his last line → CTA card ("Want Part 2? comment PART 2" when the video promises more) → Day N+1 end card (V1). V2 ends on the CTA card.

## Cut tight, catch every stutter (Day 14 notes)
- **No dead air anywhere:** run `scripts/tighten.py` on every multi-take cut — every pause inside and between lines comes down to ~0.12 s, heads and tails trimmed to the speech ("so many blank spots … start or end or middle").
- **Notice stutters and fillers yourself** ("he-here's", an untranscribed "uh"): voiced audio before a line's first word or after its last word ends is not speech you keep; cut at the deepest dip. Jack: "u need to get better at noticing this stuff". A cut that must land mid-fricative gets a ~50 ms fade, never a click.
- **One sign-off per video** (no "let's go" mid-video when there's one at the end).
- **Screens at full resolution** (never downscale a recording that a card will zoom into). **The payoff site is shown big** (a full-width browser window that scrolls to what he names, ink rings on it), not a small card.
- **Keep page type clear of TikTok/IG's right-hand buttons:** x ≈ 120–900, headlines ≤ ~130 px.
- **When he turns his head, move with him:** a slight push, tilt (~1.5°) and pan in the turn's direction on `#aroll`, settling ~2 s later.
- **Real, current pages:** product sites (his CRM landing page, a client site Claude built) are captured live or from their own files, never an old clip.

## Story and pacing
- **He goes off-script, usually so the next sentence makes sense (Day 10 note).** Keep any setup line the next sentence depends on ("So, we have 20 minutes." before "I want you to do one take"). Read the cut back sentence by sentence: each one must make sense on its own and after the last.
- **Hook opens on his face** with a kinetic caption and a quick zoom, then cuts to a page. Never open on a graphic. Exception: when he records a separate hook voiceover, it plays over his own b-roll (still with the zoom slam), then his face.
- **The video is mostly him, with captions (Day 10 note).** Paper pages show one thing for a few seconds at most (≤ ~2.5 s); never chain pages for more than ~4 s, and his face comes back between them. Everything else — lists, counters, screens, footage, stickers — is an **overlay on his footage**. A line that doesn't need a picture stays on his face with captions.
- **Pages are short.** Cut back to his face quickly; a page that sits still is boring. Exceptions: prompt/template cards (reading time) and a hero product card (hold ~2 s after it lands).
- **Never a static hold.** If a page waits for a word, reveal the small lead-in words one by one with his voice ("i… wish… i…").
- When he says a stat in a sentence, the page can end mid-sentence and the rest goes back to his face as a caption ("this is Day 1 of my" → page; "30 day series" → face).

## Footage
- **Never cut him out or fake a green screen.** Keep his real background.
- **Every edit adds its b-roll to the shared library** (`broll/`, `broll/INDEX.md`) so it can be reused; originals are never moved or changed.
- **Never show stills of his own footage** inside graphics.
- **Never crop or letterbox his footage and never regrade it.** To show a style, layer that style's type and infographics over the untouched footage.
- Cut fillers, false starts, repeated takes, dead pauses and **sniffs/breaths** at edges.

## Look
- **No red.** Ink on paper only. Real brand logos keep their own colours.
- **Clean paper**: plain, fine grain. No moving leaf/blind shadows.
- **No bracketed tag headings** ("[ one ai trick ]") or "STEP 01" labels.
- **No oversized hero words** in big serif italic; keep type restrained and centred.
- **No squiggly hand-drawn underlines.**
- Text shadows must never be clipped (give masks room; reveal with opacity + mask).
- When he names a product, show its **real logo**; when the product is the topic, an **animated logo** beats a stack of text.
- Infographics must be rich enough to make viewers go "woah" — networks, flows, live counters — not two plain bars.

## Motion
- Words in a phrase enter **different ways** (blur-in, mask slide-up, scale slam).
- Text hidden behind a mask must be **fully invisible** until its word — nothing peeking.
- **No x-ray / colour-invert flashes.** Transitions back to his face are a **slow crossfade** (≈0.4 s, page fades over his live footage), never a cut or a dip to black.
- A dragged element must pass **over** its target, never underneath.
- Final zooms are one continuous eased move with the origin fixed from the start — no nudge.

## Captions
- **Below TikTok's top tabs (Day 8 note):** never in the top 22 % of the frame (y < 422), never over his face. Place each group from the face boxes mapped through the camera zoom: right above the head when there's room, otherwise under the chin on the chest (with the soft word scrim). Each caption writes its band (`data-band="top,bottom"`) and `scripts/qa.py` checks that band against the face in the render. (Days 1–7 used a fixed band ending at y≈590 — TikTok's tabs covered it.)
- Small lead-in words, a big bold phrase, an italic serif accent; upcoming words dim, each resolves when spoken.
- **Caption colour follows the background (Day 13):** white with shadow over dark rooms; ink `#17120e` with a soft white halo over bright sky or walls (and no top scrim/vignette). Notes on his chest → captions always above his head (top as high as y≈330); the face box starts at the brows, so allow ~0.9 of its height for forehead and hair.

## Footage and screens (Day 2 notes)
- **Never grade or filter his footage — no colour filter, no shade gradient, no grain over it.** iPhone clips are HDR (HLG): convert every source with `scripts/sdr.sh` (Apple's `avconvert`, original audio muxed back) before cutting, and render with `--sdr`. Grain lives on the paper pages only. Captions over a bright screen get a soft scrim behind the words only.
- **Keep every line he wrote for the hook.** Don't drop words you think are confusing ("on a napkin" was cut in v1 and he wanted it back). When a voiceover has several takes, default to his **last clean take** — he asked for take 2 over take 1.
- **No music bed by default.** He removed it on Day 2; add music only when he asks.
- Websites on cards, wipes or browser mock-ups are **real screenshots of the live site** (`npx hyperframes capture <url>`), never frames of his phone/screen footage. When he says "replace X", grep for **every** use of that asset — v2 fixed two scenes and missed the third.
- Typing a URL: a keyboard slides in, keys press in time with the letters, **return** goes down, then the page loads (progress line) and scrolls. No mouse click for that. Type the address that actually loads, and tell him if what he says out loud doesn't.
- A cursor that clicks must land exactly on its button: measure the button from a snapshot, never guess coordinates.
- **Take joins must not double or clip a sound** ("a developer-er", "or or"). Parakeet's word starts drift ±0.3 s on repeated phrases: find syllables from the energy envelope (10 ms RMS, dips below about −30 dB), cut inside a dip, and re-transcribe the cut to count the words at the join.
- **Never flash a different take before a page.** A page that covers a new clip starts on that clip's first frame — snapped *down* to the frame (`scene()` does this), because a `data-start` rounded up by 0.3 ms leaves one frame of face showing.
- A page's last word must be fully on screen ≥0.4 s before the crossfade starts (the fade eats the last 0.42 s). Extend the page and let the next caption group clamp.
- Strike-through lines go through the middle of the words, never along the baseline (reads as an underline).

## Motion, interaction and content (Day 3 notes)
- **Causality.** Things appear because something reached them: a line draws node to node as each node lands; a dot travels a line and the icon pops when it arrives, then ticks. Never draw a line ahead of its nodes, never leave lines pointing at nothing.
- **Connections happen once.** One slow line (with its dot) and then a payoff moment (pulse, rings, a "connected" tick + sound). No looping or rebounding packets.
- **Send moments get a real click.** When a prompt or comment is finished, the send button lights up and pulses, then a cursor glides in and clicks it. Measure the button's position from a snapshot.
- **Drag means drag.** A cursor grabs the file, carries it over the drop target (dashed drop zone lights), drops it, and it lands as a chosen chip (dark ring + tick).
- **Real over stills.** Any post, account or "video" on screen is one of his real playing videos when one exists (hook cards, grids, "5 videos" rows).
- **People stay centred.** Any clip shown in a phone or card is framed on its subject (`scripts/trackcrop.py`); never show a corner of a clip.
- **Flows read top to bottom.** Input at the top, the prompt in the middle, the output revealed *below* it — never wipe the output over the input.
- **Highlight rings** include the item's label/name strip.
- **Abstract words get a visual metaphor** ("hallucinate" → a face card glitching through different faces). Phrases with a number or plural ("multiple videos a day") get the many things popping up.
- **Before/after is a signature move:** original | AI side by side with a moving divider; at the payoff, the source clip's own music under his voice and a strobe between AI and original.
- **Step headers are one fixed layout:** small "step", big number, the title row underneath, centred and complete when it lands.
- **Pages hand to pages by dissolving;** never show his face for under ~1 s between two pages. Pages snap to cuts so a new take never flashes.
- **Hook captions must be exactly what he says** — re-check any odd hook word against the audio (Parakeet heard "can't do it" for "can too").
- **No clipped last words.** Every line ends after its last syllable has fully decayed (`scripts/endcheck.py` must report 0).
- **Music only when he asks:** then deliver the no-music master plus a music copy (bed ~15 dB under speech, ducked, voice band carved out, muted while a clip plays its own song).

## Trial reels (from Day 4)
- **One edit by default; a second version only when he asks.** It stays in this style, with a different hook line and first frame, a different structure or length (≥10 % apart), and at least a third of the graphics/b-roll beats changed. Never invent words he didn't say: re-order, trim and choose between his takes. Keep the CTA keyword. Playbook: `tools/TRIAL-REELS.md`.
- **A second version is evergreen (Day 7 note).** V2 is posted at a different time from V1, so a day number would be wrong by then. Cut every spoken day reference from V2's cut ("Hello, I'm Jack, this is day seven of 30…" → keep at most "Hello, I'm Jack" if the join is clean; "see you on day eight, let's go" / "that wraps up day six" → cut), and leave out `pg_day()`, `pg_end()` and any day tracker. V2 ends on the CTA or payoff, with a short tail (≈0.6 s) instead of the end card. Its caption has no day number. V1 keeps the series intro, day page and end card.

## Pacing, overlays and real assets (Day 6 notes)
- **Something changes every ~1–1.5 s.** No page or overlay layout holds longer than ~2.5 s without switching layout, scale or scene; a long sentence becomes several beats. A 6 s page with one change per clause makes viewers swipe away.
- **Overlay mode is allowed and wanted.** Stickers, tags, price tags, phones and small infographics can sit directly on his footage (off his face, captions above the head), not always on a blank paper page. Mix both.
- **Buzzword stickers** (Day 6; from Day 13 the key moments get paper notes instead — keep stickers rare). Every key word he says (products, money, "developers", "free", "subscription", "screenshots", "phone"…) gets a pop-up: a sticker or mini infographic over his footage — icon + word, white sticker border, slight tilt, bounce in, a wiggle, quick out. Several per minute.
- **No drawn app UIs.** Any app, website or phone screen is a real screenshot or recording (ask him when he films). Phones are proper device frames around real screens, animated (scroll, zoom to the button, ring it).
- **Logos keep their brand colour and shape.** Never recolour the Claude mark, never box it inside another shape or overlap shapes on it.
- **CTA pages are short** (≤ ~2.5 s) and always moving.
- **Load this skill at the start of every episode** and design from these rules and the scene library — never by copying last episode's code from memory (Days 5–6 drifted).

## Interactivity benchmark (Day 6 notes, round 2)
- The same sticker pill everywhere reads as generic. **Every phrase gets a prop that *is* the idea** (an object, a real screen, a counter, a tracker), not a label in a pill. Benchmark and its rules: `references/reference-motion-reel.md` — hook in the first second, time the voice, land every picture exactly on its word, moving until the last frame (~one new visual state every 0.5–1 s).

## Screens, zooms and page length (Day 9 notes)
- **Never crop a website or app screen.** The whole recorded frame / screenshot at its own aspect ratio, centred on the paper (landscape recordings sit ~1000 px wide). Zoom in on a part, but always rest on (and return to) the full page.
- **Rings and click rings live inside the zoom layer**, measured from the source's own pixels, so they fit the element at every zoom level and during the move. Check start/mid/end frames of every zoom.
- **Browser chrome is not the site.** When a screen recording shows the browser's tab strip / address bar (private tab titles), crop that chrome off (measure the row where the page starts, shift every measured box by it). The site below stays whole.
- **Screen recordings keep the real cursor;** click rings land on its real position at the real moment. Retime the recording to his words (speed up dead time) rather than cutting with jumps or cropping. Don't claim what it doesn't show.
- **Pages earn their time.** A page that only restates the line, or holds over ~2.5 s, becomes quick stickers on his face (Day 9: "open up", "professional speakers", "turn your videos", "for a long time" were all rejected as pages).
- **Caption groups break at phrase boundaries;** never make a preposition ("into", "to") the bold word.
- **V2 day-number check** covers sticker text too (a "SCENE 9" clapper leaked into V2).

## Overlays over pages (Day 10 notes)
- Q-lists, scrolling lists, schedules, clips and hooks are **cinematic overlays on his footage** (clean editorial cards, smooth motion), not paper pages. Places he names (river, field, lake…) are **real high-quality footage** in overlay screens, never drawn cards. "One take, one camera"-type actions are a short character animation. "All the content" moments can orbit his head. Full list: `references/day10-audit.md`.
