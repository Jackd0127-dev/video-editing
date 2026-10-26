# Route style system

## Palette (CSS tokens in `assets/template.html`)
| Token | Value | Use |
| --- | --- | --- |
| `--cob` | `#1838f0` | page ground, app accents |
| `--cobd` | `#0f27c4` | depth |
| `--navy` | `#0a176e` | ink on white/lime, HUD pill (72 %), night state, caption hard shadow |
| `--lime` | `#d4ff3c` | progress, the spoken word, highlight blocks, ticks, buttons (lime is never decoration) |
| white | `#fff` | type on cobalt, cards; muted white 62 % for labels |

No gradients on pages except the lock-screen wallpaper; no grain; no red. Real logos keep their colours on white tiles.

## Type
- **Red Hat Display** Black (display/captions), Bold (UI copy), Medium. **DIN Alternate Bold** for station sub-lines, labels, HUD (tracked 0.08–0.14 em, caps).
- Display: `.h1` 120 px, `.h2` 84 px, `.h3` 54 px, tracking −0.035/−0.03/−0.01 em. Labels `.lab` 30 px DIN, 0.14 em.
- `.hl` = a word in a lime rounded block with navy text (one per title).
- Fonts come from the LenoFX library on the SSD (`Asset Library/Fonts/RedHatDisplay-*.ttf`, `DIN Alternate Bold.otf`) into `assets/fonts/`.

## Route map (1080×1920 page)
- Path `RPTS = [(230,1700),(230,1290),(420,1100),(850,1100),(850,740),(660,550),(470,550)]`: vertical, 45° bend, horizontal, vertical, 45° bend, horizontal. Stations sit on it; labels right (r), left (l), below (d) or above (u) so no two collide.
- Track 22 px white 20 %; fill 22 px lime; round caps. Dash pattern `L (L+60)` and an "empty" offset of `L+30` (a plain `L` dasharray leaves a round-cap dot at the end).
- Station: 64 px cobalt disc, 12 px white-35 % border; lit = lime ring (back.out 2.4) + 6 px lime burst ring (scale 0.6 → 1.6, 0.7 s) + label turns lime + pluck. Payoff station: burst to 2.4 and confirmation sound.
- Name: Red Hat Black 58 px (payoff station 96 px). Sub: DIN 26 px muted.
- Train: 92 px lime disc, navy ▲, 14 px lime-25 % halo; moves along the arc with `sine.inOut`; station arrival times are solved from the ease so they light exactly on arrival.
- Faint city-map lines (white 9 %, 10 px) sit behind every page (`MAPBG`).

## HUD (over his footage)
- Pill `left/right 90, top 118, height 96`, navy 72 %; track 6 px white 28 %, fill lime (scaleX), 5 stations 24 px, labels DIN 21 px, "you are here" 36 px lime dot with an 8 px halo.
- z-index below pages (pages cover it), above the footage. Move = fill + dot `x` 0.6 s sine.inOut, stations turn lime, HUD pulses 1 → 1.12 → 1, pluck.

## Captions
- Above his head, bottom edge at y = 590 (`.cap { bottom: 1330px }`), max 900 px wide, groups of ≤3 words / ≤15 characters, broken at punctuation, pauses >0.3 s, cuts and page edges.
- Red Hat Black 82 px caps, white, hard navy shadow `0 5px 0` + soft shadow. Each word pops in as he says it (scale 0.6 → 1, back.out 2.2, 0.18 s); the spoken word sits in a lime block (navy text); the block leaves when the next word starts. No captions while a page covers him.

## Pages and components
- Enter: `clip-path` inset wipe from the bottom with a 16 px lime edge line riding it (0.42 s expo.out); content settles 1.06 → 1. Exit to face: 0.42 s crossfade. Page → page within 1 s: dissolve.
- Cards white, radius 36–48, navy shadow `0 34px 70px rgba(4,12,80,.4)`. Logo tiles 110–260 px white, radius ~25 %. Buttons lime with a hard `0 10px 0 #9fc21a` key edge. Chips white pills with a stroke icon.
- Cursor: white arrow, navy outline, tip at (14, 8); glides in 0.55 s power3.out, presses 0.8 scale for 0.08 s.
- Proven page library (in the generator, two variants each where marked): route plan (hook), days grid ("every single day"), tools flood (grid + Skip click | phone feed swiped), price (course card + strike | checkout + Cancel click), pick one (two logos → feature network | model dropdown + click), real-life grid (4 widget cards | Mon–Sun planner), problem cards, automation (flow sun → moon | lock screen notifications), app on a phone, payoff (route arrival | before/after split with a lime divider), follow card (Follow → Following ✓ click).

## Camera
Hook slam 1.35 → 1 (0.5 s expo.out) on the face centre; every cut alternates 1.0 / 1.1 punch-ins centred on the face (`faces.swift` boxes) with a slow 3 % push; uncovered cuts get an 8 px focus pull.

## Sound
Kenney/Mixkit SFX only, no music: fast-whoosh before each page (0.32), pluck on stations, hard-pop-click on tiles, click_002 on cursor clicks, tick_002 on ticks, drop_002 on cards landing, confirmation_002 on payoffs, arrow-whoosh on train runs, a soft boom under the hook slam. Master −14 LUFS / −1 dBTP.
