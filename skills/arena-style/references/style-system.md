# Arena style system

Canvas 1080×1920 at 30 fps. All tokens are in `assets/template.html`.

## Palette
| Token | Value | Use |
| --- | --- | --- |
| Ink | `#161513` | Type, tags, VS badge |
| Bone | `#efebe3` | Pages, with faint ruled lines every 136 px |
| Card | `#f8f6f1` | Cards, bracket slots, chips |
| Coral | `#d97757` | The one accent: caption blocks, winning bracket lines, halo, Follow button |
| Coral ink | `#bf5a37` | Coral type on paper |
| Spark yellow | `#f7c945` | Sparkles and bolts only |

Agents: body `#f7845a` with shade `#d6653e`; props navy `#22356b` / `#3a57a0`, cream `#f6ecd6`, yellow `#f7c945`.

## Type
| Font | Use |
| --- | --- |
| Archivo Condensed Black | Page titles: `.h1` 150 px, `.h1.big` 220 px, `.h2` 84 px, uppercase. Lighter second word in Archivo Condensed ExtraBold at 58 % opacity (`.acc`). |
| Archivo ExtraBold | Captions, buttons |
| Archivo SemiBold | Prompt text on cards |
| IBM Plex Mono SemiBold | Labels: 30 px uppercase, 0.14 em tracking |

## Captions
Word by word, 76 px Archivo ExtraBold, white with a soft shadow, above his head (`.cap`, `bottom: 1410px`). Max 3 words or 16 characters per group, so they stay out of the top 22 %. Each word pops in (`y 26 → 0`, `scale .9 → 1`, 0.16 s). Key words get a coral block. V1 emphasises numbers and nouns of the idea; V2 emphasises action words. Captions are off while a page covers him.

## Agent anatomy
Every agent is stacked 32×32 layers scaled with `image-rendering: pixelated`, so parts move separately:
`.px` (position) → `.fp` (flip) → `.in` (bob, flinch) → `body`, `.ey` eyes, `.pr` prop, `.fx` moving bit, `.wp` weapon, `.fl` muzzle flash, `.cr` crown; `.pf` poof sits outside the flip.

`ag(id, kind, cx, cy, s, …)` puts the body centre (canvas 16, 23) at `(cx, cy)`; `s` is screen px per sprite pixel.

| Use | `s` |
| --- | --- |
| Crowd grid (10×10, ~94×100 px spacing) | 4–4.2 |
| Bracket slots, leaderboard | 3.2–4 |
| Chest-band overlays | 5–7 |
| Heroes (VS, crown, rocket) | 11–15 |

**Kinds and their idle moves** (`idle()` in the template): `coder` screen flicker, `coffee` sip + steam, `music` nod + notes, `chef` pan flip, `wizard` wand sparkle, `reader` slow bob, `sleuth` magnifier sway, `rocket` launch loop, `sky` parachute sway (too wide for grids), `plain` bob + blink. Everyone blinks.

**Eyes:** `open`, `happy`, `closed`, `angry`, `wink`, `wide`, `ko`. Swap with `eyes_to(id, k, at)`.

**Actions:** `spawn`, `arm`, `swing`, `fire`, `dash`, `knock`. Weapons: one `sword` and one `gun` in the same style.

## Beat library
| Function | Beat |
| --- | --- |
| `ov_bad` | One agent at its laptop, a wrong answer card, gets fed up |
| `pg_crowd` | One big agent → 99 pop out around it, optionally arming up |
| `pg_arena` | Hero word over a bracket with an agent in every slot and the crown in the centre |
| `pg_split` | One prompt card glides in, then 100 agents fly out of it |
| `pg_sign` | An agent holds a flipping sign, then two armies march in |
| `ov_task` / `pg_type` | Real Claude box: the task types in, `/arena` lights up with a halo, the rocket launches |
| `pg_broadcast` / `ov_bcast` | A note lands on every agent, wave by wave |
| `pg_battle` / `ov_best` | Armed crowd pairs off, knocks out wave by wave, camera pushes in on the last one |
| `pg_personas` / `ov_traits` | Personalities one by one, on cards or around him |
| `ov_answers` | Three agents with three different answers |
| `pg_bracket_pair` | The bracket builds, line by line |
| `ov_vs` / `pg_vs_magic` | Agent vs agent, ending in a knockout |
| `pg_judge` | Losers poof round by round, winners hop along coral lines to the centre |
| `pg_crown` | The winner puts on the crown |
| `pg_zoom` | Camera pulls back over the crowd tile with a running count |
| `pg_board` | Leaderboard with agent avatars, the crowned #1 last |
| `ov_why` / `ov_lost` / `ov_reasons` / `pg_champ` | Why it won or lost |
| `ov_cta` | Follow button, a waving agent, a real cursor click landing on the button |

## Motion
- **Pages:** sheet fades in 0.38 s (`sine.inOut`), content rises 36 px (0.55 s, `power3.out`). Leaving: 0.42 s crossfade to his face, or a dissolve into the next page.
- **Agents move in steps:** bob and blink use `steps(1)` so they feel like sprites. Things travelling across the page (fly-outs, camera) use smooth eases.
- **Stagger from the source:** crowds spawn outward by distance from the hero or the prompt.
- **Camera on him:** 1.35 → 1 zoom slam in 0.5 s on the hook, alternating 1.0 / 1.12 punch-ins at cuts on his face, 3 % slow push, 8 px focus pull on returns.
- **Bracket lines draw once** with `strokeDashoffset`; winners' lines overdraw in coral. Never loop them.
