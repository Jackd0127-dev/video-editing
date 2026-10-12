# Video Editing

Open-source video editing and motion design styles for Codex, Claude, and other AI assistants. Choose a style that suits the brief, learn its craft, and make something original.

## Style collection

| Style skill | Use it for |
| --- | --- |
| [Video-Edit-Warm-and-Natural](skills/video-edit-warm-and-natural/SKILL.md) | Warm, natural, personable editing with editorial typography, tactile annotations, speech-led pacing and purposeful explanatory motion. |

This is the first style in the collection, drawn from six supplied vertical videos. Each future style can have its own visual language and references. Select a style deliberately; do not impose this one on every video. Its techniques are optional building blocks, not a prescribed template. Detailed reference studies live separately from the core instructions. The supplied media, extracted frames, and full transcripts are not distributed here.

## Install

Clone this repository and copy the **whole skill folder**, including `references/`, into your assistant's skills directory. Install only the skills you want. The instructions require no paid service or specific editor; executing an edit requires tools appropriate to its deliverable.

```sh
git clone https://github.com/Jackd0127-dev/video-editing.git
cd video-editing
```

For **Codex**, run from the cloned repository:

```sh
mkdir -p ~/.agents/skills
cp -Rn skills/video-edit-warm-and-natural ~/.agents/skills/
```

For **Claude Code**, run from the cloned repository:

```sh
mkdir -p ~/.claude/skills
cp -Rn skills/video-edit-warm-and-natural ~/.claude/skills/
```

`-n` preserves an existing installation. To update one, compare your installed folder with this repository and replace it intentionally. Project-scoped installation uses `.agents/skills/` for Codex or `.claude/skills/` for Claude Code in the target project instead of the personal directories above. These are local CLI locations; account-based and cloud products may have different installation flows.

Start a fresh session and check that your assistant lists the skill. Invoke `$video-edit-warm-and-natural` in Codex or `/video-edit-warm-and-natural` in Claude Code. These installation locations were checked against [Codex documentation](https://learn.chatgpt.com/docs/build-skills) and [Claude Code documentation](https://code.claude.com/docs/en/skills) on 12 October 2026; loading in a running product must still be checked in your environment.

For other assistants supporting the [Agent Skills format](https://agentskills.io/specification), use their documented installation flow. Otherwise supply `SKILL.md` as context, together with any linked references relevant to your task. Plain context does not automatically provide file access or editing tools.

## Example requests

- “Use Video-Edit-Warm-and-Natural for this explainer. Keep the narration, develop original layouts, and use motion only where it helps.”
- “Give this founder walkthrough a warm, natural direction with readable captions and a few useful annotations.”
- “Study this reference, distinguish evidence from reconstruction, and adapt one useful principle to my brief.”

## Contribute

Use one folder per style skill under `skills/`, with a `SKILL.md` containing `name` and `description` frontmatter. Keep essential decisions in the core skill and substantial recipes or studies under `references/`. Prefer portable instructions; name tool dependencies only where they are needed.

Explain the purpose, construction, alternatives, and quality checks for a technique. Distinguish observed details, inferred implementations, and proposed settings. Try the skill against briefs with different tones before recommending it. Do not add private footage, credentials, full third-party transcripts, or unlicensed assets. A proposed addition does not authorize publishing someone else's media.

## Licence

[MIT](LICENSE) covers this repository's original instructions and documentation. It does not grant rights to the third-party videos, fonts, music, screenshots, logos, or other reference assets discussed in the studies. Use assets you have permission to use.
