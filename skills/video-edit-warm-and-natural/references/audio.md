# Audio and synchronisation

## Evidence boundary of the initial study

All six complete AAC soundtracks were decoded locally. Their speech was processed with local `small.en` automatic speech recognition and word timing. Mixed-track loudness was measured with FFmpeg's loudness analysis. There was no direct auditory perception in this study environment.

Consequently, speech timing and signal measurements are available, but listening-based judgements about music instrumentation, tonal quality, specific whooshes/clicks, noise reduction, compression settings, and musical beat alignment remain unverified. ASR can mistake names and technical terms. Word probabilities are confidence indicators, not proof of transcription accuracy.

Do not turn an attractive visual hypothesis into a claim that a sound was heard. A cursor suggests a possible click cue; it does not prove one exists. Positive waveform jumps include speech consonants and do not identify effects or beats.

## Complete mixed-track measurements

Numbers below describe the supplied downloaded encodes, including their appended platform outros. They are not recommended delivery targets, isolated speech measurements, or evidence of a particular limiter.

| Reference | Integrated loudness (LUFS) | Estimated true peak (dBTP) | Loudness range (LU) | Approximate ASR speech end | ASR words/minute through speech end |
| --- | ---: | ---: | ---: | ---: | ---: |
| R01 | -18.18 | +0.04 | 4.40 | 39.56s | 235 |
| R02 | -17.88 | +0.05 | 4.40 | 37.30s | 217 |
| R03 | -17.06 | +0.05 | 4.80 | 44.28s | 251 |
| R04 | -18.54 | +0.04 | 1.60 | 70.38s | 218 |
| R05 | -18.21 | +0.05 | 5.20 | 49.26s | 258 |
| R06 | -18.78 | +0.05 | 1.60 | 78.32s | 257 |

The speech rates help explain the compact caption fragments and progressive diagrams. They do not establish an ideal speaking rate for future work. R04 and R06 have a narrower measured loudness range than the other encodes; the result alone cannot identify a production chain. Peaks near 0dBTP deserve headroom review rather than imitation, particularly after lossy encoding.

The prominent mixed-track amplitude rises near the platform outro in R02 (~37.7s) and R03 (~44.4s) are outside the argument. Do not infer an editorial beat or an intentional story-ending sound from these downloaded-file additions. The platform outro is identified by its visuals, not by a claimed musical signature.

## Visual events against estimated speech timing

Visual bounds come from selected frames at roughly 0.167s spacing; word times come from ASR. These are approximate relationships, not sample-accurate sync measurements.

| Reference and event | Visual evidence | ASR cue | Interpretation |
| --- | --- | --- | --- |
| R01 thought bubble and first icon | Bubble visible at 8.33s; first star by 8.67s | “create” 8.10–8.34s; “visuals” 8.52–8.90s | The idea is established, then populated near the noun being explained. |
| R01 raw-file metaphor | Filmstrip grows into place around 22.17–22.67s | “uncut” 22.62–22.88s | The metaphor is already recognisable at the meaningful word. |
| R02 comparison notes | First note visible by 4.50s; second by 7.50s | First number 4.26–4.70s; second 7.32–7.66s | New states arrive within the corresponding spoken explanation. |
| R03 save feedback | Action label visible by 33.00s; confirmed label by 33.33s | “save” 33.04–33.40s | Action and confirmation occupy the spoken action's window. |
| R04 stop state | Stamp begins to appear around 55.17s and is clearly readable by 55.33s | “stop” 55.16–55.42s | A decisive visual state change aligns closely to a decisive verb. |
| R05 interaction feedback | Top-up label by 47.67s; confirmed label by 48.17s | “top” 47.68–47.84s; “credits” 48.12–48.36s | Feedback resolves within the phrase, rather than waiting for another scene. |
| R06 distribution | Small symbols spread from the server to the field around 68.3–69.2s | “swarm” 68.30–68.70s | Population movement explains the idea as it is introduced. |

These support **semantic synchronisation**. They do not establish music synchronisation. For a new film, use speech, action, and music cue maps separately, then decide which event leads each moment.

## An adaptable sound plan

1. Establish the foreground: speech, a mechanical action, material sounds, or music according to the brief. Clean edits should preserve natural breaths and room tone where useful.
2. Map purposeful cues. A transition may need movement; a state change may need contact or confirmation; a complex explanatory hold may need no additional sound.
3. Choose a coherent sound family. Tactile paper and dry ink, precise interface ticks, subdued mechanical clicks, or organic room sound are different proposals. Do not layer them all by default.
4. If using music, audition a suitable licensed track. Mark real phrase changes, downbeats, fills, and accents. Let meaningful picture changes lead where a beat would harm comprehension. Use stems or ducking if music masks speech, and listen for pumping.
5. Adjust the start of each cue so its perceptual arrival matches the visual event. A long attack may need to begin before contact; a sharp click may align to the state-change frame. Confirm by ear at normal speed.
6. Check the entire mix for intelligibility, harshness, clicks, continuity, stereo/mono behaviour, endings, and loudness. Recheck the encoded export because compression and codec peaks can change the result.

Optional proposals for the initial visual devices: a soft tactile placement for an evidence card, a restrained contact cue for a stamp, a tiny confirmation tick for a changed label, and a sustained subtle bed only where the brief benefits. These sounds were not verified in the reference audio and are not mandatory.

## Reproducible measurement

With FFmpeg available, this measures the full mix without modifying the source. Read the `input_*` values, not the hypothetical normalised output values:

```sh
ffmpeg -nostdin -hide_banner -i INPUT.mp4 -vn \
  -af 'loudnorm=I=-16:TP=-1:LRA=11:print_format=json' \
  -f null -
```

`-16`, `-1`, and `11` configure the analysis filter's hypothetical output. They are not prescribed targets for this skill. Use the requirements of the actual delivery destination. For timing analysis, inspect full audio and frame boundaries around the cue; neither automatic transcript segments nor an amplitude peak alone establishes perceptual sync.
