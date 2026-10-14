# Scene construction and handoffs

## The two stages

The warm camera stage uses the real room, natural skin, cream and gold typography, selective soft shadow and restrained foreground depth. The demonstration stage uses white, dark ink, cobalt, open spacing and a live corner camera. Switch their proportions with the explanation. Neither needs a dark dashboard or decorative card grid by default.

At 1080×1920, the reference's common white-stage text starts about 88px from the left, with roughly 70px remaining at the right. This is about 8%/6.5% of width. Headings sit in the upper third; diagrams occupy the middle; presenter and captions occupy reserved lower areas. Recompute these regions for another aspect ratio or platform UI.

Presenter windows were 274–292px wide with 32px corners, close to one quarter of the canvas width. A soft `0 16px 55px rgba(16,24,32,.15)` shadow gives them separation. Keep the source aspect ratio during the entire move, or fit/letterbox deliberately. A tutorial screen needs a different window shape and must retain essential screen edges. Do not crop or zoom a screen recording simply to fit the portrait recipe.

## Hook and proof planes

Start approximately 1.6× close and pull back near 1.025× over about 0.55s using ease-out-quart. Choose transform origin from the actual face; the reference used 50%/63%. Check the tightest frame, not just the destination. After settling, the example had very small camera drift, around 0.7% of scale; omit it if it harms legibility.

Keep the dominant statement visible from frame zero. A short qualifier and an italic emphasis arrive next. Small relevant portrait planes flank a central mechanism surface, with a narration waveform below. The approved side portraits were stills with different treatments, not a live before/after comparison. Use honest labels when demonstrating changes.

The waveform uses an actual recorded-audio envelope. The source extracts it from the final speech-led mix, including effects, at 50Hz and displays 58 rounded bars with restrained alternating cream/gold. Prefer an isolated narration stem when available if the signal should represent speech alone. Smooth/limit the amplitude to keep it subordinate to the headline. A waveform-looking decoration should not be presented as measured speech if it is synthetic.

## Moving into the sheet

Interpolate `[x, y, width, height, radius]` from full camera to its corner window over roughly 0.58–0.65s, using cubic smoothstep `3u² − 2u³`. Keep the same playback time in both states. Grow a white rectangle from the outgoing scene's visual region to fill the canvas while its corner radius resolves toward zero.

The reference reuses visual anchors and a growing sheet; it does not continuously morph every object. For a literal morph, align the outgoing rectangle and incoming origin precisely and retain the object across the boundary. Otherwise design a coherent replacement with shared scale, position or colour, and describe it accurately.

Reverse the camera movement over roughly 0.53–0.60s when returning to the speaker. Check layer order at intermediate states; a white panel should not flash over the returning face or expose a stale headline. A short plain-white typographic interruption is also part of the style. It can intentionally hide the presenter, with the first words arriving promptly and no accidental leftover fragments.

## Demonstration devices

**Grade.** Measure palm positions in the actual recording and drive the wipe from those positions. Feather the boundary; the reference used about a 130px transition band. Its hand moved rapidly across about 0.17s, while grade strength developed over 1.35s. Thus the slower visible result was a separate strength envelope, not slow exact tracking of a fast hand. Retain natural skin and show a meaningful tonal change. Reverse the boundary at the end, restoring the original image before the next demonstration. Remove floating endpoint balls or dotted guides unless they explain an actual control.

The reference grade increases contrast to 1.14, lowers saturation to 0.78 and nudges shadows cooler/highlights warmer. These are source-specific FFmpeg parameters, not a reusable skin-tone preset. Match the new footage's exposure, white balance and dynamic range first.

**Media orbit.** Use an ellipse around the head, with `x = cx + rx cos(theta)` and `y = cy + ry sin(theta)`. In the reference, the centre was approximately (540,1180), radii (430,405), and speed −0.84rad/s. Six 186×282px cards use depth sorting, mild scale change and about ±6° rotation. The curve encloses the face rather than stacking everything above it. Reposition its centre/radii from the new face bounds and preserve eyes, mouth, hand and captions. Use the user's allowed media count and interval. Collecting the cards toward the next chapter is optional.

**Magazine.** A permitted portrait fills an editorial cover with a dedicated masthead, a short italic cover line and small footer. Cream/gold can bridge it to the warm footage. The reference used a still portrait, mild −4° tilt and a small settling scale, not a live magazine video. A live portrait is optional when useful and supported. Meaningful hierarchy matters more than adding cover decorations.

**Independent infographics.** The approved white stage has a typographic ring, capsule bars and a fan of colour swatches. They develop concurrently with staggered starts: drawn arcs continue rotating, bars vary, swatches open into a row. There is no large enclosing backplate. The bar motion is illustrative, not numerical evidence. Use real scales and labels if representing data. Keep each module's name stable while its mechanism moves.

**Graphic-to-process handoff.** Small modules contract toward the positions of the upcoming step markers while the heading leaves through a mask. New numbered rows arrive on speech, a prompt types in, rules extend and the active row receives cobalt emphasis. Existing geometry supplies continuity, while the text remains readable. Another story may need a relationship map or comparison instead of three steps.

**Relevant B-roll.** Bring the insert from a rounded inset toward full frame, then cut through meaningful actions. The approved food insert used four short cuts, about 0.40–0.50s each, within the relevant spoken line. This is a reference rhythm, not permission to add food footage to every edit. Preserve user-assigned roles and original sources, and tone-map mixed phone HDR footage before compositing.

**Files and closing.** A white instruction stage can pair large text with simple outlined icons and restrained rules. Return to the full speaker for the final invitation. Emphasize only the CTA currently spoken; avoid making several actions compete at equal intensity.

## Edge treatment

Rounded live windows and permitted media surfaces supply softness. Thin SVG outlines use round caps/joins, with the original icon stroke at about 2.3 units in a 36-unit viewbox. Maintain that proportion when scaling. Use a faint boundary only when needed to distinguish adjacent white surfaces. Keep dense explanatory layouts open; do not surround every label in a pill or card.
