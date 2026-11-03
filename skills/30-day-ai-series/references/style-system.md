# Style system

All values live in `assets/template.html`; this is the why and the numbers.

## Palette
- Ink `#17120e`, paper `#ede7df` (page texture `paper-clean.jpg`: warm off-white with fine baked grain), muted `#7a6e63`.
- Card white `#fbf9f5`. Brand colour only inside real logos (Claude `#D97757`).
- No accent red. Emphasis comes from size, weight and the serif italic.

## Type
| Role | Font | Size (1080 wide) |
| --- | --- | --- |
| Display | Archivo ExtraBold, tracking −0.045em | 130–230 px on pages, 104 px captions |
| Accent | Playfair Display Italic | 90–170 px pages, 116 px captions |
| Lead-in | Archivo SemiBold | 52–56 px pages, 46 px captions |
| Notes / labels | IBM Plex Mono | 26–34 px |
Pages are centred. Display and accent lines stack tight (accent pulls up ~30 px into the line above).

## Captions on the face
- Group = one phrase, 1–3 lines: small lead-in / big bold / italic accent. Top edge never above y=422 (TikTok tabs); sits just above the head, or under the chin when the face is high (see rules.md § Captions; Day 8 build places them per face).
- Upcoming words at 22 % opacity with 7 px blur; each word resolves over 0.22 s at its timestamp.
- Group ends 0.75 s after its last word, never under a page; blur-out 0.12 s.
- Dark footage: soft dark scrim over the top 820 px, white words with text shadow `0 6px 28px rgba(0,0,0,.55)`. **Bright footage (Day 13): no scrim or vignette, ink words with a soft white halo** (`0 0 22px rgba(255,255,255,.6), 0 0 6px rgba(255,255,255,.45)`).
- Another speaker's lines (Day 13): typewriter tag above the words, 30 px, letter-spacing .14em, ink at 75 % ("JESS · AI RECEPTIONIST").
- Product names get their logo inline (e.g. OpenAI mark before "Codex").

## Face camera
- Every A-roll window gets a zoom from {1.0, 1.06, 1.12, 1.18, 1.24} with a slow 2.5 % push, origin on the face centre.
- At each cut the face size must change ≥ 14 % (measured from face samples at the cut) so it reads as a punch; if the zoom can't (face too high under the captions), add a focus pull (9 px → 0 over 0.2 s).
- Hook opens with a zoom-out from 1.3 → window zoom over 0.45 s.

## Pages
- Rounded sheet (44 px radius) over his footage; entrance = blur 22 px → 0 + scale 1.07 → 1 over ~0.32 s with a soft whoosh.
- Exit = the whole page crossfades out over 0.42 s while the sheet blurs 10 px and scales to 1.03 — his footage shows through.
- Accents: crosshair corner marks, mono notes, dot grid (for diagrams), hairline rules.

## Motion vocabulary
- `rev()` blur-rise (0.34 s, power3.out) · mask slide-up (`yPercent 150, opacity 0 → 0`, expo.out) · scale slam (1.4–1.8 → 1 with blur) · per-character stagger (0.025–0.04 s) for single key words · counters via a proxy object with `onUpdate` (deterministic).

## Sound
- Voice: highpass 75, gentle EQ, 3:1 compression, loudnorm −15 LUFS, 12 ms fades on every cut.
- Music: soft instrumental bed, carved under the voice (`hyperframes-audio/scripts/carve.mjs`), dropped under cliffhangers.
- SFX: whoosh into pages, soft pops/ticks on key words, drops for objects landing, riser → sub-boom for a cliffhanger. No clicks on transitions back to the face.
- **Never** put sound effects on sword slashes, fights, hits or clashes, and never use repeated whoosh/click bursts (the same effect firing again and again in a row). Fights and character action are silent unless Jack asks otherwise (Terra vs Sol, round 4: he hated the repeating whoosh + click on every slash and hit).
- Master: two-pass loudnorm to −14 LUFS / −1 dBTP (`scripts/master.sh`).

## Framing
- Keep text out of the bottom 18 % (platform UI) except transient UI mock-ups.
- Face top never above ~36 % of frame height after zoom.

## Paper notes (Day 13 — the default overlay)
- `.pn`: paper texture (`paper-clean.jpg`, 900 px), 6 px radius, padding 20/22 px, a strip of tape on top (110×34 px, rotated −3°), shadow `0 22px 44px rgba(0,0,0,.42), 0 3px 8px rgba(0,0,0,.25)`, drawn at 1.35× zoom, tilt −3° to 3°.
- Inside: a typewriter label (21 px caps, muted), the main line in Archivo ExtraBold (34–110 px), list rows with ink boxes; ticks/crosses are SVG strokes (3.6 px, round caps) drawn with `stroke-dashoffset` over 0.3 s with a soft scribble.
- Enter: y +50, rotation +9°, scale 0.85 → 1 (back.out(1.7), 0.42 s) with a paper drop sound; exit 0.25 s. Position from `spot()` (face track), never fixed.
- One note on screen at a time, ~2–6 s each, each line landing on its word.

## Pacing (Day 6)
- Change budget: a visible change (new element, layout switch, zoom, sticker) at least every 1–1.5 s; any single layout ≤ ~2.5 s.
- Pages and overlays alternate; overlays on his footage stay in the lower 60 % beside/below his face, captions stay above his head.
- Stickers: white 10 px border, 28–40 px radius, ink text or the brand logo, drop shadow `0 18px 40px rgba(0,0,0,.35)`, tilt ±4–10°, enter scale 0.2 → 1.15 → 1 (back.out) in 0.35 s, wiggle once, exit scale 0.6 + fade in 0.2 s; ~0.9–1.4 s on screen.
