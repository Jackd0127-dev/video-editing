# Typography and motion

## Roles and spacing

The approved example used five real faces across three families:

| Role | Actual face | Reference size at 1080px width |
| --- | --- | --- |
| Dominant hook | Avenir LT Std Black | 154–170px |
| Demonstration heading | Avenir LT Std Black | 92–106px |
| Editorial accent | Bauer Bodoni Std Italic | 91–153px |
| Step/feature label | Avenir LT Std Heavy or Black | 66–91px |
| Supporting copy | Avenir LT Std Roman | 37–43px |
| Captions | Avenir LT Std Heavy | 48px on white; 60px over footage |
| Magazine masthead | Didot LT Std Headline | 62px inside a 480px cover |

These sizes reflect different jobs, not one global scale. Use the glyphs' optical size and available width to adapt them. A high-contrast italic often needs a larger nominal size than the sans to feel equally important. Main statement line heights were roughly 1.08–1.16. Important display tracking stayed around zero to −0.018em, while ordinary word spaces remained natural.

Await font loading before rendering frame zero. In a browser compositor, set explicit family, weight and style; enable native kerning/common ligatures and disable synthetic faces. Do not request an unavailable bold weight of the italic. Do not guess the font from appearance when the editable project identifies it.

Lay out the completed phrase first. Animate whole words in inline boxes separated by actual spaces, so the final widths and baseline remain stable. For wraps, reserve each completed line independently; reflowing the line on every spoken word causes jitter. The reference's `nowrap` setting suited its short phrases, not arbitrary future captions.

Protect overhangs and shadows before clipping. The source used roughly 15px vertical and 18px horizontal word padding with compensating margins; phrase slots used 12px/20px. Treat these as starting clearance, then inspect the actual font and effect radius. Keep a gap between successive lines even while both are moving. A settled phrase must show its complete descenders and italic terminal strokes.

## Motion vocabulary

Let `u = clamp((t − onset) / duration, 0, 1)` and `p = 6u⁵ − 15u⁴ + 10u³`. This smootherstep gives text a gentle departure and landing without an overshooting bounce. Use seconds derived from the composition's frame clock, not wall-clock CSS animation.

**Primary word rise.** The source moves each word from about 112% of its own height to zero inside a fixed mask. Common arrivals last 0.42–0.60s; offsets between words are about 0.055–0.12s. Exact speech onsets override these regular offsets. Very short concluding words used 0.16–0.34s arrivals to leave a readable hold before the section ended.

**Editorial reveal.** A clip boundary moves from 100% right inset to zero while the word travels only 15px horizontally. Typical duration is 0.50–0.68s. Reserve the full italic width from the start. Do not let the clip's left boundary shave off an overhanging first glyph. This is a whole-word masked reveal, not a typing effect or a letter-by-letter spacing routine.

**Phrase slot.** Old and new phrases share a fixed-height clipped area. During a 0.62s change, the old phrase travels by `−height × p` and the new by `height × (1 − p)`. Use separately sized slots for a small qualifier and a large headline. Check intermediate frames: partial glyphs are intentional during a mask reveal, but colliding rows or remnants outside the slot are not. Only use this where replacing the phrase explains a change.

**Supporting line.** A 12px vertical glide settles over roughly 0.48s, with a short 0.15s ease-out alpha. This motion remains subordinate to primary words. No blur or scale is needed.

**Caption.** A 12px rise settles over 0.17s, with about 0.07s ease-out alpha. Earlier words stay in position as the current word takes the accent colour. Phrase positions and word timing come from the narration, not the animated headline's timing.

**Graphic or media surface.** The source uses restrained Remotion springs for cards/icons: damping 24, stiffness 190, mass 0.85, usually bounded to 0.35–0.55s. This is distinct from the smootherstep used for type. Start near the resolved scale; large bounce conflicts with the composed editorial tone.

The dependency-free [motion helpers](../assets/motion.mjs) provide easing, word reveals, phrase slots, rectangles and orbit poses. They produce poses only; the host compositor supplies masks, glyph layout, video and rendering.

## Separation and readable holds

The footage shadow was two soft layers: `0 3px 12px rgba(16,12,8,.48), 0 10px 28px rgba(16,12,8,.22)`. White stages use dark text without that shadow. Scale the shadow with output size and inspect the encoded edge; adding a hard stroke to a small raster word rarely repairs a poor text render.

Choose onsets, durations and departure together. The last word must finish before departure with enough reading time; shortening its arrival is better than cutting a partly revealed word. Some lines overlap in time but occupy separate reserved rows. Intentional movement should not make the reader chase the whole sentence.

Review both dense transition samples and settled frames. Rasterize native text at adequate resolution, composite once where possible and use high-quality final encoding. Supersampling is useful for a raster workflow when necessary; it does not repair bad spacing or clipped masks.
