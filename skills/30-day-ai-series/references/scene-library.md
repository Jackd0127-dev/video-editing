# Scene library (approved in Days 1–3)

Each pattern exists in `assets/build-day01.py` under the matching `# P…` block. Times are relative to word tokens (`t(i)`).

| Pattern | When | Build notes | Length |
| --- | --- | --- | --- |
| **Hook face** | First line | Face + caption "one / AI trick", zoom-out slam 1.3 → 1 | ~1.3 s |
| **Stacked phrase page** | Punchline of the hook | Lead-in words one by one; bold word mask slide-up; italic word scale-slam tucked under | ~2 s, holds ~1 s after last word |
| **Stat page** | "This is day one of my…" | Centred "Day 1" in display sans, 30-block tracker with block 1 lit; cut back to face on the rest of the sentence | ~1.4 s |
| **Animated logo** | Product is the topic | Official mark spins in from blur, 3 ripple echoes, ray burst, orbit line, topic in italic letter-by-letter; low hit | ~2 s |
| **Product card** | "I bought the X plan" | 3D card (brand colours), logo above, chip, member name, sheen sweep, mono note; enters at scene start | ~2.2 s |
| **Sizzle** | "insane motion graphics like this" | 4 sub-cards pushed in: scrolling outline/solid word rows, motion-blur echoes + speed lines, shapes on a grid, zoom-in "this." → riser + boom + music drop back to face | ~1.9 s |
| **Network infographic** | Any "the more you give it…" idea | Dot grid, crosshairs, 12 input chips around a logo node, lines draw in, packets flow, counters (inputs, output %) and a fill ring | ~3 s |
| **Prompt card** | "paste this prompt" | Title + window card (Claude Code bar, Copy → Copied ✓), lines blur in; lower caption lines | ~5 s (reading) |
| **Style on footage** | Naming a visual style | No page: type and infographics over untouched footage — e.g. italic "cinematic" built word by word; bold = label blocks + huge "BOLD" + bar chart | ~3 s each |
| **Drag & drop** | "drag in your footage" | File icons, cursor grab (press scale 0.86), carried above the composer, drop → attachment chips with upload bars → send button lights | ~3 s |
| **Template card** | "use this prompt template" | Window with fill-in chips + model wheel picker scrolling to the model, plan badge | ~7 s (reading) |
| **Clock** | Durations | SVG clock, minute hand sweeps to each number, wedge fills, time-lapse second hand, big "15–20 min" | ~1.7 s |
| **Role cards** | "without needing a designer…" | Full-width cards swing in (rotationY), icons draw themselves, mono subtitles; on the last word they fold into one dark product card | ~5 s |
| **End card** | "stay tuned for day N+1" | "Day N+1", 30 blocks with only today's lit + label, hold ~2 s, then one eased zoom into the lit block until it fills the frame (riser + soft hit) | ~5 s |

For Day N, update: the tracker's lit block, the end card number, and the hook's day label.

## Added in Day 2 (`assets/build-day02.py`)

| Pattern | When | Build notes | Length |
| --- | --- | --- | --- |
| **Hook over b-roll** | He records a separate hook voiceover | VO over his b-roll (drawing, then the result on screen), quick zoom slam, kinetic caption; then his face | ~3.3 s |
| **Before → after wipe** | "turning X into Y" | Card with the "before" photo; real screenshot wipes across with a scan line; italic label swaps to a bold one | ~3.5 s |
| **Mini-app pile** | Listing jobs/tools you supposedly need | Three live mini apps drop in tilted, each with a dark name pill: design canvas (blocks pop, pen curve draws, selection, swatches), code editor (lines type in, caret), drag-and-drop builder (block dragged over the drop zone, clock racing). On the "you don't" they fly off sideways and the line slams in | ~5 s |
| **Drop into Claude** | "drop them into Claude" | Photo flies into a composer; placeholder steps down; attachment chip pops; send button lights; "drop them into ✳ Claude" header | ~1.2 s |
| **Brief card** | Listing what to tell Claude | "tell ✳ Claude" + card filling row by row (vibe, who, colour swatches, feel, component chips) | ~7 s |
| **Prompt window + send** | "here's the exact prompt" | Window with the template, highlighted swap parts, cursor lands on send (measured) and clicks | ~6 s (reading) |
| **Sketch vs site** | "look at that compared to that" | Sketch card, arrow draws, real-site card below | ~3 s |
| **Keyboard URL** | "it's live at …" | Browser window + keyboard; keys press as the address types; return goes down; load line; real full-page screenshot scrolls; keyboard drops away | ~5 s |
| **Comment CTA** | "comment X and I'll send you…" | Pill types the keyword in heavy caps, send lights, lead-in words below | ~2 s |

## Added in Day 3 (`assets/build-day03.py`)

| Pattern | When | Build notes | Length |
| --- | --- | --- | --- |
| **Playing fan** | "I run five … accounts" | Five of his real posts fan out as playing cards (video layer), big number slams in, words arrive one by one | ~2.5 s |
| **Before/after slider** | Showing an AI swap (hook "exactly how you can too", payoff) | Original \| AI full screen, white divider glides left then right, tags low; on exit the divider splits into two lines that glide outwards and reveal his face | ~2 s |
| **Road map** | "from start to finish" | Five icon nodes land in turn; each line segment draws from the last node to the next as it lands; "start" / "finish" labels | ~2.5 s |
| **Animated logo** | "Claude does all the heavy lifting" | Logo spins in from blur, rings, ray burst, slow rotation; the key phrase drops in | ~2 s |
| **Many videos** | "multiple videos a day" | Six real posts pop into a tilted grid one after another | ~1.5 s |
| **Prompt types out** | "tell Claude who your character is…" | His real prompt types word by word in a Claude window; spoken items get highlighted and tick chips appear | ~4 s |
| **Connected** | "I've connected Claude to Higgsfield" | Two logos, one slow line with a dot, then a pulse, two rings and a green "connected" tick; real screen recording of the result below | ~4 s |
| **Input → prompt → output** | "follow this prompt and you've got your image sheet" | Source grid on top with the chosen item ringed (label included), prompt window in the middle, the result wipes in below | ~5 s |
| **Same everywhere** | Consistency claims | One sheet at the top, curved lines to three real posts, "✓ same" chips | ~3 s |
| **Cut the face off** | Explaining a crop | Sheet with a dashed crop line drawn at the shoulders, body panels ringed, two tags | ~4 s |
| **Hallucination** | "it won't hallucinate between faces" | Face card glitches through other characters' faces with jitter and ghosting; the word gets ghost copies; "which face?" | ~2.5 s |
| **Step header** | Every step | `step_head()`: small "step", big number, complete title row, centred | — |
| **Drag onto Claude** | "drop the clip and the character sheet into Claude" | Cursor drags each file over the prompt box (drop zone lights), drops, chip ringed + ticked; prompt types; send lights and the cursor clicks it | ~6 s |
| **Genjutsu swap phone** | "keeps the moves, timing, camera angle… swaps in your character" | Tracked original in a phone, chips tick, scan line wipes it into the AI version, tag swaps | ~6 s |
| **Payoff strobe** | "Claude comes back with this" | Result full screen with the source clip's music, strobe AI/original with a punch per switch, then side by side | ~2.8 s |
| **5 × 5 × 5** | "hours … five videos on five accounts on five platforms" | Playing videos → avatars → platform logos, a web of lines between each row, a clock spinning | ~5 s |
| **API dispatch** | "it posts through the APIs" | Planner card, one line + dot per platform in turn; each icon pops on arrival then ticks; centred "✓ posted" holds under the line | ~4 s |
| **Course card** | Announcing a product | Card rises, three heavy words land, a tilted "very very soon" pill | ~2 s |
| **Comment + click** | "comment X" | Keyword types in the pill, send lights, cursor clicks it; the promised items (prompt cards) rise below | ~3 s |

Hook variants tried for Day 3 (`assets/hooks-day03.py`): the feed (phone swipes one account per word), cold open on the slider, zoom-out mosaic, playing cards around his face, swipe deck with a 3D flip.
