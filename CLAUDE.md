# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A collection of homegrown Claude skills. Most skills here target **Claude chat (claude.ai)** and **Claude CoWork**; a smaller number target **Claude Code**. The packaging format is identical across all three — what differs is the install target and what tools/environment the skill can assume at runtime.

Each skill ships as a single packaged `.skill` file (a zip archive following the standard Anthropic skill layout: `SKILL.md` with YAML frontmatter at the root, plus optional `references/`, `assets/`, scripts, etc.).

Skills are grouped into top-level **category directories** (e.g. `aivalue/`, `prd/`). One category per practice area or skill family; one `.skill` archive per skill.

## Source layout

Skill source lives as plain directories inside the repo:

```
<category>/
  <name>/          ← source tree (tracked)
    SKILL.md
    references/
    assets/
  <name>.skill     ← auto-generated archive (also tracked, for GitHub download)
```

Edit the source directory directly. The pre-commit hook rebuilds `.skill` archives automatically and stages them before every commit, so the archive in the repo always matches the source.

To rebuild archives manually at any time:

```bash
bash scripts/pack.sh
```

The archive's top-level directory name **must** match the skill `name:` in `SKILL.md` frontmatter — every Claude surface (chat, CoWork, Code) keys off that name when loading the skill.

## SKILL.md conventions used here

Frontmatter is a hard contract:

```yaml
---
name: <kebab-case slug, matches the archive's root directory>
description: <one-paragraph trigger description — when to invoke, what it produces>
---
```

The `description` is what Claude reads to decide whether to invoke the skill, so it must enumerate the trigger phrases and outputs clearly. Existing skills in this repo follow that pattern; mirror it when adding new skills.

## Adding a new skill

1. Pick or create a category directory (e.g. `prd/`, `aivalue/`, or a new one).
2. Create `<category>/<name>/SKILL.md` (plus any `references/`, `assets/` subdirectories).
3. Validate in the **target surface** for that skill — usually Claude chat or CoWork; Claude Code only if the skill genuinely needs filesystem/shell tooling. Exercise the trigger phrases from its `description`.
4. Commit — the pre-commit hook packages the `.skill` archive automatically.
5. Add a one-line entry to the skill table in `README.md`.

When authoring, remember that chat/CoWork skills run without Bash, Read, Write, or other Claude-Code-style tools — don't reference file paths, shell commands, or filesystem-state assumptions in instructions meant for those surfaces.

## One-time developer setup

After cloning, point git at the tracked hooks directory:

```bash
git config core.hooksPath .githooks
```

This wires up the pre-commit hook that repacks `.skill` archives before each commit.
