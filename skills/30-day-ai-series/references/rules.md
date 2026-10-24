# Jack's rules

Each one came from a review note. Breaking any of them got a version rejected.

## Story and pacing
- **Hook opens on his face** with a kinetic caption and a quick zoom, then cuts to a page. Never open on a graphic. Exception: when he records a separate hook voiceover, it plays over his own b-roll (still with the zoom slam), then his face.
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
- Above his head, never over his face (face boxes from Vision; caption band ends at y≈590).
- Small lead-in words, a big bold phrase, an italic serif accent; upcoming words dim, each turns white when spoken.

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
- **Two deliverables when music is wanted:** no-music master and a music version (bed ~15 dB under speech, ducked, voice band carved out, muted while a clip plays its own song).

## Trial reels (from Day 4)
- **Every episode = 5 trial reels**, all in this style, each with a different hook line and first frame, a different structure or length (≥10 % apart), and at least a third of the graphics/b-roll beats changed. Never invent words he didn't say: re-order, trim and choose between his takes. Keep the CTA keyword. Playbook: `tools/TRIAL-REELS.md`.
