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
- Group = one phrase, 1–3 lines: small lead-in / big bold / italic accent. Bottom edge at y=590, grows upward.
- Upcoming words at 22 % opacity with 7 px blur; each word resolves over 0.22 s at its timestamp.
- Group ends 0.75 s after its last word, never under a page; blur-out 0.12 s.
- Soft dark scrim over the top 820 px for legibility; text shadow `0 6px 28px rgba(0,0,0,.55)`.
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
- Master: two-pass loudnorm to −14 LUFS / −1 dBTP (`scripts/master.sh`).

## Framing
- Keep text out of the bottom 18 % (platform UI) except transient UI mock-ups.
- Face top never above ~36 % of frame height after zoom.
