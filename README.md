# Video Editing

Open-source video editing and motion design skills for AI assistants. Choose a style, give your AI the footage and brief, and use the skill to guide an original edit.

## Choose your style

| Skill | What it brings | Example |
| --- | --- | --- |
| [Layered Motion Video Editing](skills/video-edit-fluid-editorial/SKILL.md) | Energetic layered hooks, refined sans/serif typography, masked lettering and continuous graphic handoffs. | A creator explainer with a busy opening, live magazine treatment and developing diagrams. |
| [Bold Typography Video Editing](skills/video-edit-editorial-studio/SKILL.md) | Bold editorial type, clean white demonstrations, speech-timed words and fluid corner-camera handoffs. | A polished creator demonstration that moves between warm footage, animated graphics and clear process steps. |
| [Warm Natural Video Editing](skills/video-edit-warm-and-natural/SKILL.md) | Personable, speech-led pacing, editorial type, tactile annotations and purposeful explanatory motion. | A founder walkthrough with natural colour, readable captions and a few useful drawn annotations. |
| [Presenter Tutorial Video Editing](skills/video-edit-editorial-tutorial/SKILL.md) | Warm paper, subtle white gradients, compact sans/italic type, complete screen recordings and connected graphics around a live presenter. | A creator tutorial that moves between full presenter, screen walkthrough and developed editorial demonstrations. |

Display names describe the editing approach. Install folder names and invocation IDs remain stable so existing links and installations keep working.

Each style is an adaptable toolkit. Choose the techniques that fit your story; invent the composition and sequence around your brief.

## Quick start with Codex

Paste **one** of these into Codex:

**Layered Motion Video Editing**

```text
$skill-installer install https://github.com/Jackd0127-dev/video-editing/tree/main/skills/video-edit-fluid-editorial
```

**Warm Natural Video Editing**

```text
$skill-installer install https://github.com/Jackd0127-dev/video-editing/tree/main/skills/video-edit-warm-and-natural
```

**Bold Typography Video Editing**

```text
$skill-installer install https://github.com/Jackd0127-dev/video-editing/tree/main/skills/video-edit-editorial-studio
```

**Presenter Tutorial Video Editing**

```text
$skill-installer install https://github.com/Jackd0127-dev/video-editing/tree/main/skills/video-edit-editorial-tutorial
```

Then start your next request with the skill name and your footage:

```text
Use $video-edit-fluid-editorial to edit my attached video.
Keep my full narration. Build a layered opening with refined typography
and smooth motion that develops with the explanation. Use the supplied
references for creative direction and B-roll only at relevant spoken moments.
Deliver an MP4, captions and editable project files supported by your tools.
```

Codex supports installing skills from GitHub through `$skill-installer`. If a new skill does not appear, restart your session and check again. See the [official installer examples](https://github.com/openai/skills/blob/main/README.md#installing-a-skill).

**Using Claude Code, installing manually, or adding skills to one project?** Follow the [installation tutorial](docs/install.md).

## How to use each skill

The [usage guide](docs/usage.md) includes ready-to-copy prompts for all four styles, a footage checklist, a revision workflow and instructions for keeping reference clips separate from footage intended for the edit.

1. Install the complete skill folder.
2. Select a style by name.
3. Supply your footage, references and constraints.
4. Review the exported video, then request specific refinements.

## What you need

These skills supply creative direction, motion recipes and review guidance. They do not bundle an editor, footage, fonts or a model. To export a video, your assistant needs file access and a working editing or compositing toolchain, such as a local FFmpeg-based workflow. Check its available tools before promising an editable timeline or final render.

No particular editor or paid provider is required by the instructions. Use your own assets and licensed fonts or sounds. Private media can stay in your local project when you use local tools.

## Explore the collection

- [Presenter Tutorial Video Editing motion recipes](skills/video-edit-editorial-tutorial/references/motion-recipes.md): compact type, presenter windows, complete walkthroughs, white-gradient demonstrations and connected diagrams.
- [Presenter Tutorial Video Editing reference breakdown](skills/video-edit-editorial-tutorial/references/reference-breakdown.md): the full approved reference sequence, exact font identities and measured properties.
- [Layered Motion Video Editing motion construction](skills/video-edit-fluid-editorial/references/motion-construction.md): glyph baselines, masks, easing, camera movement and handoffs.
- [Layered Motion Video Editing style properties](skills/video-edit-fluid-editorial/references/style-properties.json): adaptable palette, type and motion roles.
- [Bold Typography Video Editing typography and motion](skills/video-edit-editorial-studio/references/typography-motion.md): exact reference faces, word reveals, phrase slots, spacing and shadows.
- [Bold Typography Video Editing scene construction](skills/video-edit-editorial-studio/references/scene-construction.md): white stages, presenter windows, grade gestures, media orbits and developing diagrams.
- [Bold Typography Video Editing style properties](skills/video-edit-editorial-studio/references/style-properties.json): measured starting values for adapting the approved style.
- [Warm Natural Video Editing techniques](skills/video-edit-warm-and-natural/references/techniques.md): editing, typography, annotations and explanatory motion.
- [Warm Natural Video Editing audio guidance](skills/video-edit-warm-and-natural/references/audio.md): sound design, timing and honest verification.
- [Warm Natural Video Editing reference studies](skills/video-edit-warm-and-natural/references/studies/README.md): six approaches to visual explanation.

## Contribute a style

Add one folder under `skills/` with a concise `SKILL.md`, `name` and `description` frontmatter, and supporting material under `references/`. Explain the style's purpose, how to construct its techniques, how to adapt them, and what evidence was actually verified. Add the style to the table and usage guide.

Keep source footage, private transcripts, credentials and non-redistributable assets outside the repository. Proposed techniques and inferred implementations should be labelled clearly. Use a pull request for contributions.

## Licence

[MIT](LICENSE) covers original instructions and documentation. Referenced third-party footage, fonts, sounds and logos retain their own rights. This repository distributes no private source media or proprietary font binaries.
