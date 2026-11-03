# Pre-delivery checklist

Run this before sending Jack any edit, draft or round. Every line is something he had to catch himself. Fix what fails, then say what you checked and what you couldn't: you can't hear audio, so anything judged only from numbers or waveforms gets flagged for his ear.

## Cut and words
- [ ] Pauses tightened on every line (`scripts/tighten.py`): no blank spots at the start, middle or end of lines.
- [ ] Each line's head and tail read in the energy envelope: no half-word stutters ("he-here's") and no "uh" the transcript missed.
- [ ] No clipped last words (`scripts/endcheck.py`). It skips a cut followed straight by the next word, so check those by hand and keep the sentence going to a real pause.
- [ ] Transcript gaps over ~2 s with loud audio re-transcribed with Whisper, and mishears fixed.
- [ ] The whole cut read back as sentences: every answer has its question first, and off-script setup lines the next sentence needs are kept.
- [ ] One sign-off only. No doubled sounds at joins, no retakes left in.
- [ ] No piece under 0.45 s: nothing flashes in for a split second.

## Captions and type
- [ ] Captions match what he actually says, and hook words are checked against the audio.
- [ ] Captions never cover his face and never sit in the top 22 % of the frame (TikTok's tabs).
- [ ] Captions read clean on the background: ink on bright, white on dark, no dark scrim on bright footage.
- [ ] Page and CTA type stays inside x ≈ 120–900, clear of the socials buttons.

## Picture
- [ ] Mostly his face: pages ≤ ~2.5 s, no run of pages over ~4 s. Something changes every ~1–1.5 s, and no layout holds past ~2.5 s.
- [ ] Every overlay snapshotted at its final position: nothing on his face or hair, or over what his hands show.
- [ ] Rings snapshotted when they finish drawing, and they go properly around the target.
- [ ] Apps and sites are real captures at native resolution, large enough to read, not pixelated. Logos are real, with their real colours.
- [ ] Footage has no grade or filter, and he isn't cut out of his background.
- [ ] Camera: no move during the opening zoom-out (first 0.55 s), no snapping, no constant zooming in and out.

## Sound
- [ ] No sound effects on fights or hits, and no repeated whoosh or click bursts.
- [ ] −14 LUFS master. `qa.py` shows 0 caption/face overlaps and 0 voice-cut pops, with flagged pops checked by eye (a consonant is speech; leave it).

## Round and delivery
- [ ] Only what he asked changed: captions and zoom stay put on a size change. Layout changes he can't picture get a still first.
- [ ] Every note from him is listed as done or not done.
- [ ] Any second version in a series has no day number anywhere, including sticker text.
- [ ] B-roll saved to the library, and the files are in the video's `Exports/` with old renders in `Drafts/`.
