# Sound, synchronization and export

## Voice and useful cues

Keep requested narration timing, pitch and wording. Build a beat map from the actual voice and recording rather than guessing from a script alone. The reference used short recorded notification, glass, click, whoosh, pullback and confirmation cues. Use distinct sounds for distinct semantic actions, with softer travel cues beneath speech. Do not interpret its 51 cues as a target count.

Measure leading quiet material before positioning an effect. The reference preparation examined 5 ms RMS windows, trimmed to just before active sound, faded the tail and normalized each reusable clip before setting its mix level. Measured clip peaks were placed around -15.5 to -23 dBFS before the final narration/effects normalization. A different waveform or recording level needs different gain. Avoid setting a quiet file to a nominal volume and assuming it will be audible.

Retain an effects stem when useful for revision. Keep the voice dominant and inspect crowded cue intervals. The reference used a gentle 65 Hz voice high-pass and final loudness control; neither is mandatory for already clean footage. Its actual AAC measured -16.07 LUFS / -1.75 dBTP. Select delivery levels for the brief and measure the encoded file rather than copying those numbers blindly.

Listen when playback is available. Correlation, peak/RMS measurements and encoded waveform detection establish timing or presence, not subjective mix quality. Report direct listening honestly.

## Separate screen synchronization

The observed screen recording had a strong shared-audio match to the narrator. The measured start offset was 16.631 s; 11 independent five-second windows agreed. At 60 fps, frame 998 corresponds to 16.6333 s, giving 2.33 ms rounding error. The screen's audio was used for this measurement only, then omitted from the final soundtrack.

These are source-specific measurements. Recompute an offset for each replacement recording; check for drift instead of retaining an earlier file's offset. If audio is absent, use recorded interaction markers or reliable visual events. Keep the recording's own framing and zooms unless instructed otherwise.

## Render the actual media

The observed film used Remotion 4.0.535 with deterministic frame-driven React/SVG/CSS graphics, real loaded fonts and video sources. This proves the chosen local implementation, not a requirement to install that version or renderer. Another capable compositor can implement the same mechanisms.

Important observed parameters were 1080 × 1920, 60 fps graphics, H264/AAC 48 kHz stereo, BT.709 SDR, zero stream starts and MP4 fast-start. Presenter footage was 30 fps and the walkthrough 60 fps. Preserve source timing when mixing frame rates. Respect source colour/rotation metadata and perform an intentional HDR-to-SDR conversion when relevant.

Source frames need not be visible during every graphic cutaway, but their timeline should keep running so the walkthrough returns to the correct action. A brief final-frame hold can cover the rounding difference between narration and picture duration; do not silently repeat or omit narration.

## The browser-capture fault lesson

An earlier export in the reference workflow contained blank and tiled picture frames despite passing decode and sampled reviews. In that local environment, using the existing pinned headless-shell browser, lossless PNG captures and separate compositor layers for wide opacity/SVG content removed the known faults. Full desktop Chrome with concurrent captures had been the failing configuration.

This is environment-specific evidence. Do not claim every browser or concurrent renderer is broken, or install a new renderer as a default workaround. Reproduce the current failure, make a bounded change and inspect the encoded output. Browser flags can change capture semantics and should not be applied blindly.

For a renderer with that failure history, scan every decoded frame for near-uniform output, repeated tiles and isolated temporal anomalies. Review flagged frames visually: an intentional clean page or cut is not automatically a fault. A successful decode only proves that frames are decodable; it does not prove that the compositor captured the intended scene.

## Useful completion evidence

Match verification to the change and retain reusable passing evidence when relevant media and settings are unchanged. Inspect the encoded opening, title swaps, prompt start/end, screen edges, live inset and layout departures. Check masks, natural word spaces, optical line gaps, face clearance and destination safe areas at phone size; use native frames for font edges and clipping.

Verify duration, dimensions, frame rate/count, colour, stream starts and full decode as appropriate. When reusing a separately mixed audio file, copy-mux payload and decoded-audio identity can establish that prior measurements still apply. Check narration alignment in separated windows and review actual cue presence rather than assuming the mix succeeded.

Keep the requested movie, sidecar captions, supported editable source, source/provenance notes and a concise verification boundary together. State rendered, visually inspected, technically checked, directly auditioned and creatively accepted status separately. A studied reference or a validated skill folder is not proof that a new film has been rendered with the skill.
