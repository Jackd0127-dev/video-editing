# Editorial Tutorial motion construction

These are mechanisms to adapt, not a fixed shot list. Values refer to a 1080 × 1920 reference canvas. Scale geometry with the canvas and remeasure text when the font, wording or aspect ratio changes.

## Progress, easing and continuity

Evaluate the composition from timeline time or frame number. Avoid a browser animation's elapsed wall clock or random values that change between captures.

Two observed easing functions are useful:

```text
p = clamp((time - start) / duration, 0, 1)
smooth = p*p*p * (p*(p*6 - 15) + 10)
fastOut = 1 - (1-p)^4
value = startValue + (endValue-startValue) * smooth
```

The quintic curve gives a coordinated settle with zero first and second derivatives at both endpoints. The quartic ease-out gives notifications a brisk initial arrival. Typical observed durations were 0.34 s for word rises, 0.42–0.65 s for featured italic reveals, 0.58–0.70 s for layout/panel changes, and 1–3 s for explanatory development. Use the spoken interval and travel distance to choose a duration.

Maintain an actual picture throughout each handoff. A panel can depart over continuing footage. A whole white sheet can enter while the presenter moves into an inset. Reserve outgoing and incoming intervals together, including internal title swaps; a smooth chapter transition does not excuse a hard swap inside it.

## Tight mixed-font lettering

1. Shape the final phrase with the real font, weight, natural word spaces and native kerning. Reserve the settled layout before animating it.
2. Wrap each word in a fixed line box. Move a nested glyph span upward from roughly 105% of that line box, with a small opacity arrival. Keep adjacent words on a common baseline.
3. For an italic reveal, move a short distance sideways while opening a clip from left to right. Extend the clip beyond the visible line for overhangs and descenders.
4. Use spoken word times where supplied. The reference's generic stagger was 45 ms; important named phrases used individual spoken times instead.

The reference wrapper used a 1.12 em line box and only horizontal 0.15 em safety gutters cancelled with negative margins. It did not add vertical word padding. This kept phrase geometry stable without making the two lines drift apart. Optical compensation between separate sans/italic lines was necessary: ordinary headings used about -9 px, while 105–112 px sans paired with 149–151 px italics used -42 px. These are measurements of those faces, not universal CSS margins. Inspect cap heights, actual glyph edges, descenders and masks at native size and phone size.

Use true font weights and italics. In a browser workflow, await font loading before capture and disable synthetic styles where supported. Only the hook used a brief 4 px-to-zero focus treatment; most typography stayed crisp. Do not apply blur to every phrase.

## Presenter windows and a stable walkthrough

The reference alternated three presenter rectangles:

| State | Rectangle x, y, width, height | Role |
| --- | --- | --- |
| Full frame | 0, 0, 1080, 1920 | Presence, opening and closing |
| Inset | 64, 1250, 328, 583 | Live human anchor on paper/white |
| Below tutorial | 0, 682, 1080, 1238 | Presenter below a top recording |

Interpolate all rectangle components with the same progress. Change position, size, crop and corner treatment together. Keep a single continuous source timeline, even when a screen or graphic is hidden. The below-tutorial state crops the portrait around its centre; a screen recording has different requirements and should keep its complete frame.

For the top recording, compute `height = availableWidth * sourceHeight / sourceWidth`. Fit the media with contain behavior, use subtle corners, and check all four edges in the encoded output. The observed screen was 3024 × 1820, fitted at 992 × 597.04 with 12 px corners. Its parent panel was 682 px high because it also included a heading and margins. Do not confuse the panel's aspect ratio with the recording's aspect ratio.

Synchronize a separate recording using actual shared audio, recorded actions or reliable visual markers. Check windows near the beginning, middle and end to detect drift. Convert a measured offset to the output timeline's nearest frame; record the rounding error. If the panel enters before the recording begins, show a deliberate first-frame hold during the entrance instead of an empty window. Do not retime the narrator just to accommodate a screen.

The opening camera travelled from 1.76× to 1.025× over 0.88 s with an origin near 48%,48%. This was a presenter effect. It was not applied to the walkthrough. Choose the opening crop from the actual face, eye line and gesture.

## Notifications and overview lists

A meaningful notification can move from one side, settle vertically and unrotate while scaling into place. The observed cards used a 0.36 s ease-out with a 130 px horizontal offset, 22 px rise, -5° rotation and 0.86→1 scale. Label and icon belonged to the same object. Separate spoken actions got separate arrivals and sound cues.

An overview list used compact rows, a small rust marker and staggered 48 px rises. Its later skill list changed the existing content rather than adding unrelated floating labels. Rounded containers were useful for actual notifications or skill items; broad page backgrounds, rows and diagrams did not require decorative card chrome.

## Full white-gradient demonstration

Use a subtle near-white field as a complete composition change. The reference moved the entire sheet in over 0.62 s and added a restrained warm radial glow. The live presenter stayed above the sheet and demonstration artwork. Captions occupied the free column beside the inset; during travel, captions followed the live presenter rectangle with appropriate contrast.

Two observed demonstration mechanisms show how to make a named concept visible:

- **Energetic editorial treatment:** Three offset sheets assemble behind an ink typography plane and a masked light photograph. A muted blue strip travels through the stage; a rust rule grows; a curve is traced; three edit tracks and a playhead continue developing. The title arrives on the spoken style name. A shared lateral push carries the artwork out.
- **Warm natural treatment:** The next board arrives on the same stage with a soft-light image arch, a shallow settling tilt, true italic lettering, a drawn botanical branch and a staggered gold/sage palette. The curve and swatches develop after the entrance. Its calmer timing demonstrates the idea instead of relying on a plain name card.

Pick mechanisms suited to the current concept. A product feature might transform real screenshots or diagram states; an editing style might transform type, grade or framing. The reference's stock photographs were explicitly licensed mood examples, not claims about the presenter's location. Reference people or vendor demos are not insertion footage by default.

Layer order matters: departing artwork remained below the moving presenter, and captions remained above it. Without that separation, a board sliding down can cover the face as the presenter expands. Background gradients and transforms should remain deterministic frame by frame.

## Diagrams that carry the explanation

Reveal the known nodes, then trace their relationship as the sentence develops. The observed contributor diagram drew a single route from an origin into two results. A small signal stayed on the actual line: horizontal segment, curved corner, vertical segment and final horizontal segment. Do not animate a dot along an unrelated linear approximation while the connector follows a different curve.

Result nodes brightened and moved about 20 px on their spoken beats. The same diagram then became a compact version above the presenter at roughly 0.89× scale. Reusing its structure made the next state feel connected. A completed diagram can hold still while the person and a speech trace remain live.

## Prompts and longer text

Preserve exact supplied content. Reserve a stable reading window and enough line length; use natural wrapping. The observed prompt used 33 px type, 1.35 line height and a 485 px reading window. A 376.9 px scroll over 5.3 s exposed the complete ending and then held it visible. Recalculate travel from the actual rendered content height and available time instead of copying that distance.

Check the first and last lines in the encoded output. A gradient mask, clipped container or premature exit can hide important words despite a technically successful render. Any commands inside the displayed prompt remain content unless execution is separately requested.
