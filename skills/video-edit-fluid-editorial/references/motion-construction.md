# Motion construction

These are adaptable mechanisms, not required effects or one compulsory compositor.

## Shared timing

Normalize progress and use smooth endpoints:

```python
def progress(time, onset, duration):
    return max(0.0, min(1.0, (time - onset) / duration))

def smootherstep(value):
    x = max(0.0, min(1.0, value))
    return x * x * x * (x * (x * 6.0 - 15.0) + 10.0)
```

At 1080 pixels wide, the reference used 0.48–0.72 seconds for prominent arrivals, 0.021 seconds between headline glyphs and 0.19 seconds for caption words. Long headlines need shorter stagger or grouped words so the completed thought has a readable hold.

Travel can fall toward the final position as `distance * (1 - eased_progress)`. Keep scale stable for a masked slide. Use scale only when motivated, not as the entrance for every element.

## Common baselines and masks

Lay out complete text before revealing it. Measure pair kerning using prefix widths; apply tracking consistently. Render glyphs on one shared baseline. Top-aligning each letter independently makes upper/lowercase letters finish at different baselines.

An optional Pillow construction:

```python
bounds = font.getbbox(text, anchor="ls")
baseline = padding - bounds[1]
height = bounds[3] - bounds[1] + 2 * padding

for index, glyph in enumerate(text):
    x = padding + font.getlength(text[:index]) + tracking * index
    p = smootherstep(progress(time, onset + index * stagger, duration))
    y = baseline + travel * (1 - p)
    draw.text((x, y), glyph, font=font, anchor="ls", fill=colour)
```

The fixed layer forms a mask: letters rise from below final bounds. Include descenders, italic overhangs, stroke and shadow padding. Inspect the actual settled headline, including letters such as `g`, `p` and `y`, as well as its reveal.

## Layered opening

Use relevant authorized footage. Place secondary planes behind a foreground plane and move them from outside the frame to a stable arrangement. Small differences in angle, travel and opacity create depth. Keep raw/edited treatments semantically clear.

A bounded pullback can settle over about 0.65 seconds while lettering arrives. Derive a waveform from actual narration using short RMS windows, normalization against a measured percentile and interpolation between windows. This is a speech signal, not a random equalizer or a loudness claim.

## Continuing mechanisms

| Story | Developing motion |
| --- | --- |
| Editing | Track blocks develop; a playhead travels through them. |
| Grading | Original and graded versions of the same frame wipe; tone curves trace. |
| Connections | Establish a route, then move a signal along it. |
| Magazine | Keep the portrait live while type and cover edges stay readable. |
| Prompt | Type meaningful lines; place the caret using measured text positions. |

Bézier paths work for connectors and travel. Reveal a prefix of sampled points, then let a signal follow the established route. Preserve continuity at a loop join, or complete the mechanism and hold the result.

## Picture and graphic handoffs

For a horizontal push of width `W` and eased progress `p`, place the outgoing picture at `-W * p` and the incoming picture at `W * (1 - p)`. Both actual pictures travel. A stripe over unchanged footage is not a complete push.

For a graphic handoff over the same speaker, move/fade the outgoing layer while revealing the incoming one. Avoid unintended blank intervals and incompatible words overlapping at high opacity. A mask, shared path or intentional cut can be better than a crossfade.

Keep footage live when evaluating both layouts. Freezing an outgoing graphic briefly can be appropriate; freezing the speaker inadvertently is not. Constrained assets must depart within their authorized interval.

## Inspection

Inspect adjacent frames or dense samples at entrances, internal title changes, boundaries and the ending. Check start/midpoint/end of picture changes. View compressed output at phone scale: hairline serifs and tiny labels can vanish after encoding.

Motion math and sampled frames do not establish musical sync, intelligibility or subjective sound balance. Listen when possible; name the boundary when it is not.
