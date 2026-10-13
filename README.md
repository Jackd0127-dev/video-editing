# Video Editing

Open-source video editing styles for Codex, Claude and other AI assistants. Select a style that fits the brief, learn its craft and make an original edit.

## Style collection

| Style skill | Use it for |
| --- | --- |
| [Fluid Editorial](skills/video-edit-fluid-editorial/SKILL.md) | Layered hooks, refined sans/serif typography, masked lettering, developing graphics and fluent handoffs. |

Fluid Editorial is an adaptable toolkit, not a fixed storyboard. Its skill links to motion construction, reference properties and a sequence breakdown. It requires no paid service or particular editor; rendering requires suitable tools in the target environment.

The earlier [Warm and Natural style](https://github.com/Jackd0127-dev/video-editing/blob/codex/video-motion-skill/skills/video-edit-warm-and-natural/SKILL.md) remains on its existing branch. This addition does not merge or replace that work.

## Use a skill

Copy the complete `skills/video-edit-fluid-editorial/` folder, including `references/`, into your assistant's supported skill location. Keep folder names and relative paths intact. Installation/discovery depend on the assistant; verify loading in your environment.

Example Codex invocation:

```text
Use $video-edit-fluid-editorial to edit this explainer with a richer hook,
refined typography and fluent motion. Keep my full narration and use each
supplied asset only at its relevant spoken moment.
```

Without native skill loading, supply `SKILL.md` and its relevant linked references as context. Guidance alone does not provide file access or rendering tools.

## Contribute

Use one folder per style under `skills/`. Keep `SKILL.md` concise and substantial recipes/properties under `references/`. Describe purpose, construction, adaptation and evidence limits. Keep source media, credentials, private transcripts and non-redistributable assets out of the repository.

## Licence

[MIT](LICENSE) covers original instructions and documentation, not referenced third-party footage, fonts, sounds or logos. Use assets with appropriate rights. This repository distributes no source media or proprietary font binaries.
