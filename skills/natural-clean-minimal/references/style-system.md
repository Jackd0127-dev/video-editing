# Style system

## Captions
- Montserrat ExtraBold 70 px, letter-spacing 0.01em, white, `top: 1395px` (chest; check against face boxes from `scripts/faces.swift`).
- Legibility on light clothing: `-webkit-text-stroke: 2px rgba(20,14,8,.35); paint-order: stroke fill;` plus shadows `0 0 22px rgba(0,0,0,.55), 0 3px 10px rgba(0,0,0,.6)`.
- Timing: show from word start −0.02 s until the next caption starts (−0.02) or 0.75 s after the word; pair a ≤4-letter word with the next ≤4-letter word when they start <0.3 s apart.
- Emphasis card: one bigger word (Montserrat ExtraBold 96 px) + small tracked subline, same position, ~1.5 s.

## Liquid glass recipe
```css
.glass { overflow: hidden; isolation: isolate; transform: translateZ(0);
  -webkit-mask-image: -webkit-radial-gradient(white, black);   /* smooth rounded corners with backdrop blur */
  background: linear-gradient(160deg, rgba(255,255,255,.30), rgba(255,255,255,.10) 55%, rgba(255,255,255,.16));
  backdrop-filter: blur(26px) saturate(170%);
  border: 1.5px solid rgba(255,255,255,.55);
  box-shadow: inset 0 1.5px 0 rgba(255,255,255,.75), inset 0 -10px 30px rgba(255,255,255,.08), 0 24px 60px rgba(0,0,0,.28); }
```
Add a skewed white sheen bar swept across once after entrance (0.8–0.9 s).

## Pixel Claude character
11×8 grid of 20 px squares in `#d97757` (body cols 2–8 rows 0–5, arms cols 0–1 / 9–10 rows 3–4, four legs rows 6–7), two dark 20 px eyes. It sits on the banner's top edge; animations: pop up from behind (back.out), hops with alternating legs, blinks (eyes scaleY), arm wave, exits upward.

## Motion
- Hook zoom: `#cam` scale 1.38 → 1, 0.55 s, expo.out, origin on the face.
- Glass entrance: opacity 0, y −24, blur 10 px → 0 over 0.8–0.9 s, power3.out. Title words follow with a 0.12 s stagger.
- Typing: per-character times with deterministic jitter (45–80 ms, +70 ms after spaces) driven from one proxy tween; caret blinks (steps) after typing.
- Cursor: glides in power3.out, press 0.82 scale yoyo, button press + expanding ring, result card drops out (y −110, scale .7, blur 12 → 0, back.out 1.5).

## Sound
- Voice chain from `make-aroll.sh` (−15 LUFS pre-master). Quiet acoustic guitar bed (`scripts/musicgen.py` prompt "warm acoustic guitar fingerpicking, soft and optimistic…") carved under the voice at volume 0.2.
- SFX sparing: whoosh on hook, soft ticks on character hops, quiet key clicks, click + pop-whoosh + pluck on send.
- Master −14 LUFS / −1 dBTP.

## Framing
- Overlays in the top third (banner top ≈ 300 px, composer ≈ 330 px), clear of the face; captions on the chest; nothing in the bottom 18 %.
