# claude-skills

A collection of homegrown [Claude skills](https://www.anthropic.com/news/skills). Most are written for **Claude chat** (claude.ai) and **Claude CoWork**, with a smaller number targeting Claude Code. Each skill is packaged as a single `.skill` archive and dropped under a category directory by practice area.

## Skills

| Skill | Category | What it does |
| --- | --- | --- |
| [`prd-writer`](prd/prd-writer.skill) | `prd/` | Writes zero-ambiguity Product Requirements Documents and Technical Design Documents intended to drive autonomous Claude Code CLI execution. |

More skills will land here as they're built.

## Installing a skill

A `.skill` file is a zip archive containing a single top-level directory (e.g. `prd-writer/`) with a `SKILL.md` and any supporting files. Download the `.skill` file from this repo (or clone the repo), then install it into whichever Claude surface you're using:

- **Claude chat (claude.ai)** — Settings → Capabilities → Skills → upload the `.skill` file. It becomes available in any new conversation.
- **Claude CoWork** — upload the `.skill` file through your workspace's skill management. The skill is then available to anyone with access to that workspace.
- **Claude Code** — unzip the archive into your skills directory and start a new session:
  ```bash
  unzip path/to/prd-writer.skill -d ~/.claude/skills/
  ```

Skill triggers are described in each skill's `SKILL.md` frontmatter — peek at them without unpacking:

```bash
unzip -p prd/prd-writer.skill prd-writer/SKILL.md | head -5
```

## Cloning or forking this repo

If you only want to *use* a skill, you don't need any of this — just download the `.skill` file (see [Installing a skill](#installing-a-skill) above). These steps are for when you clone or fork the repo to edit or add skills.

1. Fork the repo (via the GitHub "Fork" button), or clone it directly:

   ```bash
   git clone https://github.com/<your-account>/claude-skills.git
   cd claude-skills
   ```

2. Arm the pre-commit hook — a **required one-time step per clone**:

   ```bash
   git config core.hooksPath .githooks
   ```

   This points git at the tracked [`.githooks/`](.githooks) directory so the pre-commit hook can regenerate `.skill` archives from source before each commit, keeping source trees and archives in sync. It's local-only git config (stored in `.git/config`, never committed), so every fresh clone or fork has to run it once.

If you'd rather not use the hook, repack manually before committing instead:

```bash
bash scripts/pack.sh
```

## Contributing a new skill

See [`CLAUDE.md`](CLAUDE.md) for the layout conventions and SKILL.md frontmatter contract. Short version: create a source directory under the right category, validate in the target Claude surface, commit — the pre-commit hook packages the `.skill` archive automatically (assuming you armed it per [Cloning or forking this repo](#cloning-or-forking-this-repo) above).

## License

[MIT](LICENSE).
