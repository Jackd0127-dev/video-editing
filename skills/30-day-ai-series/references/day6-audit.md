# Day 6 audit — what went wrong and the rules that came from it

"Build your own app with Claude" (Photo Sorter rebuilt from screenshots). Three clips: IMG_5404 hook + intro,
IMG_5405 the build, IMG_5407 note + CTA + sign-off. V1/V2 were rejected as "didn't edit great". Read this with
`day3-audit.md` before any episode. Days 5 and 6 were also built by copying the previous day's code without loading
this skill — **always load the skill first** and design from `rules.md` + `scene-library.md`, never from memory.

## Jack's notes and their fixes

| # | Note | Root cause | Fix (now in the skill) |
| --- | --- | --- | --- |
| 1 | "Paying for apps" page terrible | A generic list of made-up subscription rows on a blank paper sheet | Don't invent stand-in UI. Use real assets, or motion design over his footage (stickers, price tags) |
| 2 | £70 page terrible and on screen ~6 s with nothing changing — "the user will click off" | One page held a whole sentence with one change per clause | **Pacing rule:** something visibly changes at least every ~1–1.5 s; no page or layout holds longer than ~2.5 s without switching layout, scale or scene; split long sentences across several beats |
| 3 | Overlays don't always need a blank canvas | Every visual was a full paper page | **Overlay mode:** stickers, tags, infographics and phones can sit straight on his footage (off his face, captions still above his head). Mix pages and overlays |
| 4 | "Building your own app" page: Claude mark black, circle over a square — awful | Recoloured the mark white on an ink square and stacked shapes | Official logos keep their brand colour and shape, never recoloured, never boxed inside other shapes or overlapping them |
| 5 | "One shot" page looked bad | Generic composer + chips + icon on a blank sheet | Same as 1 and 3 |
| 6 | Photo Sorter looked terrible — "use a real screenshot" | Drew a fake app UI | **Any app on screen is a real screenshot or recording** (ask him for it, or capture it). Hand-drawn app mock-ups are banned |
| 7 | All the phone screens look bad | Flat CSS phones with drawn content | A phone is a proper device frame around a real screenshot/recording; animate the screenshot (scroll, zoom to the button, ring it) |
| 8 | Comment page bad and on too long | Static box + three fake comments held ~5 s | CTA ≤ ~2.5 s with constant motion; overlay it on his face if possible |
| 9 | Buzzwords should get pop-ups | Captions were the only thing reacting to key words | **Buzzword stickers:** whenever he says a key word ("developers", "free", "£70", "subscription", "screenshots", "phone", product names), a sticker / mini infographic pops in over his footage (icon + word, white sticker border, tilt, bounce in, wiggle, out) |

## Habits
- Before building, list every beat with its on-screen change times; if any stretch has > 1.5 s without a change, redesign it.
- When the content is an app or a website, ask for screenshots/recordings when he films; never fill the gap with a drawn UI.
- Load the skill and read the audits at the start of every episode.
