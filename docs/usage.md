# Using the skills

[Back to the collection](../README.md) · [Installation tutorial](install.md)

Choose the style that fits your video. In Codex, use `$video-edit-fluid-editorial`, `$video-edit-editorial-studio` or `$video-edit-warm-and-natural`. In Claude Code, use the same name with `/` in place of `$`. With manual context, explicitly name the supplied skill.

For Editorial Tutorial, use `$video-edit-editorial-tutorial` in Codex or `/video-edit-editorial-tutorial` in Claude Code.

## Supply a useful brief

Give the assistant:

- **Main footage:** Attached files or accessible local paths; identify the recording to edit.
- **Message:** The audience, purpose and wording to preserve. Say whether cuts or reordering are allowed.
- **Asset roles:** Label style references, insert footage, thumbnails, B-roll and sound separately. Identify any spoken moments where an asset belongs.
- **Delivery:** Aspect ratio, destination, preferred duration and required exports. Request an editable project in a format the tools can actually produce.
- **Creative limits:** Brand colours, licensed font or asset locations, caption preferences and any generation restrictions.

Reference videos help the AI learn craft. They are not automatically footage to insert or instructions to obey. Keep original source files intact and give asset rights or restrictions where relevant.

## Fluid Editorial

Use this for energetic creator explainers, demonstrations and a rich opening that continues into coherent motion. Its core devices include live footage planes, expressive type, developing signals, magazine compositions and connected transitions.

Copy this prompt, replace the placeholders, and attach the files:

```text
Use $video-edit-fluid-editorial for my attached main video: [filename].
Audience: [audience]. Deliver a [9:16 / 16:9] video for [destination].
Keep my full narration and original wording.

Make the hook feel designed from the first frame: layer relevant footage,
refined sans/serif typography and a developing graphic mechanism.
Use staggered masked lettering with stable baselines, smooth camera travel
and connected handoffs. Keep important information readable and my face clear.
When I mention an editing style or capability, demonstrate it visually.

Asset roles:
- [files]: style references only.
- [files]: permitted thumbnails for [specific topic or spoken moment].
- [files]: relevant B-roll for [specific topic or spoken moment].
- [folder]: fonts and sound assets I have rights to use.

Develop original layouts that fit this recording. Preserve my source files.
Deliver an MP4, complete sidecar captions, and supported editable project files.
Review the encoded hook and transitions; report what you actually checked.
```

Remove or change the sample asset roles when they do not apply. A calmer brief can use fewer layers while retaining refined type and fluent handoffs. The [motion construction guide](../skills/video-edit-fluid-editorial/references/motion-construction.md) supplies implementation detail; the [properties](../skills/video-edit-fluid-editorial/references/style-properties.json) are starting points to adapt.

## Editorial Studio

Use this for a polished demonstration with bold sans/italic contrast, warm creator footage, clean white stages and a continuing presenter window. Its [approved reference breakdown](../skills/video-edit-editorial-studio/references/approved-reference.md) distinguishes measured construction from optional devices. Choose Fluid Editorial when richer overlays across the full speaker are the main direction; choose Editorial Studio when making room for clean demonstrations is central.

```text
Use $video-edit-editorial-studio for my attached main video: [filename].
Audience: [audience]. Deliver a [9:16 / 16:9] video for [destination].
Keep my full narration, wording and timing.

Start close on me with a quick smooth pullback and a layered, readable hook.
Use a strong heavy sans with high-contrast editorial italics, natural spaces,
soft shadows and word reveals timed to my speech. Give different text roles
related motions and enough time to read after they finish arriving.

When the explanation needs room, move me smoothly into a rounded corner
window on a clean white stage. Show the idea visually with developing
diagrams, comparisons or steps. Connect sections through shared geometry
and return to the full speaker when appropriate. Keep my face and hands clear.

Asset roles:
- [files]: style references only.
- [files]: permitted media for [specific topic or spoken moment].
- [folder]: licensed fonts and recorded sound assets.

Use my available typefaces or show suitable licensed substitutes.
Adapt the style to this story; omit irrelevant reference devices.
Do not generate or upload media. Preserve my source files.
Deliver an MP4, complete sidecar captions and supported editable source.
Check actual encoded text edges, readable holds, transitions and audio.
```

The [type guide](../skills/video-edit-editorial-studio/references/typography-motion.md) supplies word and phrase timing. The [scene guide](../skills/video-edit-editorial-studio/references/scene-construction.md) covers camera/sheet handoffs and optional demonstrations. [Properties](../skills/video-edit-editorial-studio/references/style-properties.json) and dependency-free [motion helpers](../skills/video-edit-editorial-studio/assets/motion.mjs) support implementation without imposing a fixed sequence.

## Warm and Natural

Use this for personable explainers, founder walkthroughs and teaching videos where presence, clear speech and tactile editorial touches suit the story. Motion explains relationships and leaves time to read.

```text
Use $video-edit-warm-and-natural for my attached main video: [filename].
Audience: [audience]. Deliver a [9:16 / 16:9] video for [destination].
Keep my wording and narration order. Tighten pauses only if they interrupt flow.

Use natural skin tones, speech-led pacing, readable captions and editorial
typography. Add a few tactile annotations or drawn diagrams where they clarify
the message. Let each graphic arrive, explain, hold and leave with purpose.
Keep the speaker present and adapt the palette to the footage and brand.

Asset roles:
- [files]: creative references only.
- [files]: permitted B-roll for [specific topic or spoken moment].
- [folder]: available licensed fonts and sound assets.

Develop an original composition rather than copying a reference layout.
Preserve my source files. Deliver an MP4, complete sidecar captions and
supported editable project files. Check readability, colour continuity,
caption timing and the actual export; report any review still outstanding.
```

For a comparison, ask it to keep the known state visible while introducing the new state. For teaching, use a chapter marker followed by a visible transformation. For a relationship map, reveal nodes before their connections. Choose only the relevant [reference study](../skills/video-edit-warm-and-natural/references/studies/README.md) and [technique](../skills/video-edit-warm-and-natural/references/techniques.md).

## Editorial Tutorial

Use this for a cohesive presenter-led tutorial or explainer: warm paper, white-gradient demonstrations, tight sans/italic type, complete interface recordings and developing diagrams. It keeps the human presence while moving the explanation into different layouts. Install the complete skill folder, including its supporting references.

```text
Use $video-edit-editorial-tutorial for my attached main video: [filename].
Audience: [audience]. Deliver a [9:16 / 16:9] video for [destination].
Keep my full narration, wording, timing and pitch.

Use refined medium/bold sans and true italic serif typography with compact
optical spacing. Build a purposeful opening and smoothly move between full
presenter, contained screen tutorial and paper or subtle white-gradient scenes.
Keep my presenter live and clear of the destination's interface controls.
Develop useful diagrams or visual demonstrations when I explain a concept.
Time primary words, icons and short recorded sound cues to my narration.

Screen recording: [filename]. Fit its complete original aspect ratio with
subtle corners. Keep the zooms already recorded; do not add screen zoom,
pan, shaking or crop. Synchronize this specific recording to the voice.
Use supplied prompts as exact on-screen content, not commands to execute.

Asset roles:
- [files]: style references only.
- [files]: permitted footage or imagery for [specific spoken moment].
- [folder]: available licensed fonts and sounds.

Invent the composition for this story instead of copying the reference's
script or fixed timeline. Preserve my originals and generation restrictions.
Deliver an MP4, complete sidecar captions and supported editable project files.
Inspect the encoded text, screen edges, face clearance and transitions;
report technical checks and direct listening separately.
```

Remove the screen paragraph when there is no walkthrough. A product demonstration can use real screenshot transformations; a conceptual explainer can use changing diagrams, type or palette. Read the [motion recipes](../skills/video-edit-editorial-tutorial/references/motion-recipes.md) for construction, and the [reference breakdown](../skills/video-edit-editorial-tutorial/references/reference-breakdown.md) for the observed whole-film progression. The [properties](../skills/video-edit-editorial-tutorial/references/style-properties.json) are an adaptable measured profile.

## Refine the result

Use timecodes and describe the outcome you want. Keep the same editable project so revisions build on the accepted direction.

**Richer opening**

```text
Revise 00:00–00:05. Keep the narration. Make the hook feel richer with layered
footage, more refined type and a graphic that develops through the sentence.
Carry that motion into the next section smoothly; keep the main idea readable.
```

**Clearer explanation**

```text
At [timecode], the diagram arrives all at once. Introduce its parts in the
order I explain them, trace the relationship, then hold the resolved picture
long enough to read. Preserve the accepted typography and colour direction.
```

**Calmer treatment**

```text
Reduce competing motion at [timecode]. Keep one dominant idea and the speaker
visible. Give the text a stable readable hold and use sound only for useful cues.
```

## Review and delivery

Review the saved video at normal speed and phone size. Check the opening, internal headline changes, transitions, face clearance and caption wording. Listen to speech and sound cues when playback is available. Technical measurements alone do not establish how the mix sounds.

Ask for the export path, editable project path, caption file, a concise explanation of the choices and the verification boundary. Distinguish rendered output, technical checks, visual inspection and audio listening. A skill installation or a storyboard alone does not prove a finished edit.

Publishing and uploading footage to a service remain separate actions. State those permissions explicitly when you want them.
