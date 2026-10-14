# Installation tutorial

[Back to the collection](../README.md) · [Using the skills](usage.md)

Install whichever styles you want. Always copy the **whole folder**, including `references/` and `agents/`, and keep its name and relative paths intact.

## Codex: install from GitHub

Use the copyable `$skill-installer` requests in the [quick start](../README.md#quick-start-with-codex). The installer downloads the selected skill folder and preserves an existing installation by refusing to overwrite it. Its default destination is `~/.codex/skills/`, or your configured `$CODEX_HOME/skills/`.

On your next turn, ask Codex to use `$video-edit-fluid-editorial`, `$video-edit-editorial-studio` `$video-edit-warm-and-natural` or `$video-edit-editorial-tutorial`. If it cannot find the new skill, restart your session. The supported GitHub install syntax is shown in [OpenAI's skills repository](https://github.com/openai/skills/blob/main/README.md#installing-a-skill).

## Manual install: get the repository

If you have Git, run this once in a folder where you keep repositories:

```sh
git clone https://github.com/Jackd0127-dev/video-editing.git
cd video-editing
```

Already cloned it? Open that folder instead. Before updating it, preserve any local changes; a clean clone can be updated with `git pull --ff-only`.

Without Git, open the [repository](https://github.com/Jackd0127-dev/video-editing), choose **Code → Download ZIP**, extract it, and copy the desired folders from `skills/` to one of the locations below using your file manager. Include hidden parent folders where necessary.

## Codex: manual personal install

Run these commands from the cloned repository to install all four styles for your local projects:

```sh
mkdir -p "$HOME/.agents/skills"
if [ ! -e "$HOME/.agents/skills/video-edit-fluid-editorial" ]; then
  cp -R skills/video-edit-fluid-editorial "$HOME/.agents/skills/"
fi
if [ ! -e "$HOME/.agents/skills/video-edit-warm-and-natural" ]; then
  cp -R skills/video-edit-warm-and-natural "$HOME/.agents/skills/"
fi
if [ ! -e "$HOME/.agents/skills/video-edit-editorial-studio" ]; then
  cp -R skills/video-edit-editorial-studio "$HOME/.agents/skills/"
fi
if [ ! -e "$HOME/.agents/skills/video-edit-editorial-tutorial" ]; then
  cp -R skills/video-edit-editorial-tutorial "$HOME/.agents/skills/"
fi
```

Omit a copy command to install just one style. These copy commands target macOS/Linux; on Windows, copy the folders with your file manager. The guards skip any existing skill folder, so this is a first-install recipe, not an update recipe.

Codex discovers personal skills under `~/.agents/skills/` and project skills under `.agents/skills/`. For a project install, copy each complete style folder to `<your-project>/.agents/skills/` instead. See [Codex skill locations](https://learn.chatgpt.com/docs/build-skills).

Do not install the same name through both methods or scopes unless intentional. The built-in installer and manual method may use different locations; choose one and check which copy your session loads.

## Claude Code: personal install

From the cloned repository:

```sh
mkdir -p "$HOME/.claude/skills"
if [ ! -e "$HOME/.claude/skills/video-edit-fluid-editorial" ]; then
  cp -R skills/video-edit-fluid-editorial "$HOME/.claude/skills/"
fi
if [ ! -e "$HOME/.claude/skills/video-edit-warm-and-natural" ]; then
  cp -R skills/video-edit-warm-and-natural "$HOME/.claude/skills/"
fi
if [ ! -e "$HOME/.claude/skills/video-edit-editorial-studio" ]; then
  cp -R skills/video-edit-editorial-studio "$HOME/.claude/skills/"
fi
if [ ! -e "$HOME/.claude/skills/video-edit-editorial-tutorial" ]; then
  cp -R skills/video-edit-editorial-tutorial "$HOME/.claude/skills/"
fi
```

For one project, copy to `<your-project>/.claude/skills/` instead. Then invoke the installed skill in Claude Code:

```text
/video-edit-fluid-editorial Edit the attached video with a layered hook and fluid editorial motion.
```

```text
/video-edit-warm-and-natural Edit the attached video with natural pacing and purposeful annotations.
```

```text
/video-edit-editorial-studio Edit the attached video with editorial type, clean demonstrations and fluid presenter handoffs.
```

These paths apply to **local Claude Code**. Claude's web, cloud and Cowork environments have separate installation flows and do not read your local personal folder. See [Claude Code's official skills guide](https://code.claude.com/docs/en/skills).

## Other AI assistants

Use the product's documented custom-skill import if available. A GitHub link by itself does not guarantee installation, file access or rendering support.

Without a native skill loader, attach or paste the selected `SKILL.md` together with the references needed for your task, and explicitly ask the assistant to follow them. If the product requires an upload package, follow its packaging instructions and include the supporting files. This supplies guidance; the product still needs tools capable of editing your media.

## Presenter Tutorial Video Editing

Install Presenter Tutorial Video Editing through the [GitHub quick start](../README.md#quick-start-with-codex), or copy the complete `video-edit-editorial-tutorial` folder from this repository into your chosen personal/project skill location. Preserve any existing installation.

For example, from the cloned repository, this guarded macOS/Linux copy installs it into the manual Codex personal location:

```sh
mkdir -p "$HOME/.agents/skills"
if [ ! -e "$HOME/.agents/skills/video-edit-editorial-tutorial" ]; then
  cp -R skills/video-edit-editorial-tutorial "$HOME/.agents/skills/"
fi
```

If you already installed the same name through another location or method, use that copy rather than creating a duplicate. For Claude Code, copy the complete folder into the appropriate `.claude/skills/` location above. Invoke `$video-edit-editorial-tutorial` in Codex or `/video-edit-editorial-tutorial` in Claude Code. Restart the session if the installed folder is not discovered.

## Check the installation

Ask your assistant:

```text
Find the video-edit-fluid-editorial skill. Tell me the path you loaded,
its style character, and which linked reference covers motion construction.
Do not edit or render anything yet.
```

For Warm Natural Video Editing, substitute its skill name and ask which reference covers sound. For Bold Typography Video Editing, use `video-edit-editorial-studio` and ask which reference covers typography and motion. For Presenter Tutorial Video Editing, use `video-edit-editorial-tutorial` and ask which reference covers motion recipes. A successful check identifies the actual loaded folder and its linked reference. Before rendering, ask which local media tools it can use and supply a small test clip if you need to prove the toolchain.

## Troubleshooting and updates

| Problem | What to check |
| --- | --- |
| Skill is missing | Confirm the supported location contains `<skill-name>/SKILL.md`, with no extra nested repository folder. Restart the session if needed. |
| References are missing | Copy the complete skill folder, not just `SKILL.md`. Preserve the `references/` directory structure. |
| Installer says it already exists | Compare the installed folder with the repository. Back up local changes, then intentionally replace the complete folder if you want the update. |
| Old instructions still appear | Ask for the loaded path. Check for duplicate personal/project copies and refresh the session. |
| AI can discuss the edit but cannot export | Check local file access, decoding, compositing, audio and encoding tools. Installing instructions does not install those tools. |
| Fonts or sound assets are unavailable | Supply licensed assets you own, or ask for suitable available alternatives. No proprietary binaries are included. |

Installation instructions were checked against the linked primary documentation on 13 October 2026. Product locations and discovery behavior can change; use the current official guide if your environment differs.
