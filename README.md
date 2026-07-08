# slalom-claude-skills

Internal, homegrown [Claude skills](https://www.anthropic.com/news/skills) built at Slalom. Most are written for **Claude chat** (claude.ai) and **Claude CoWork**, with a smaller number targeting Claude Code. Each skill is packaged as a single `.skill` archive and dropped under a category directory by practice area.

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

## Contributing a new skill

See [`CLAUDE.md`](CLAUDE.md) for the layout conventions and SKILL.md frontmatter contract. Short version: create a source directory under the right category, validate in the target Claude surface, commit — the pre-commit hook packages the `.skill` archive automatically.

**One-time setup after cloning:**

```bash
git config core.hooksPath .githooks
```

This wires up the pre-commit hook that regenerates `.skill` archives from source before each commit, so source and archives stay in sync.

## License

[MIT](LICENSE).
