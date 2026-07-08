# slalom-claude-skills

Internal, homegrown [Claude skills](https://www.anthropic.com/news/skills) built at Slalom. Most are written for **Claude chat** (claude.ai) and **Claude CoWork**, with a smaller number targeting Claude Code. Each skill is packaged as a single `.skill` archive and dropped under a category directory by practice area.

## Skills

| Skill | Category | What it does |
| --- | --- | --- |
| [`avp-input-builder`](aivalue/avp-input-builder.skill) | `aivalue/` | Builds the intake side of an AVP (AI Value Platform) client demo: Demo Brief, client research, Business Function setup, Enhance input generation (process- and role-based), and Business Context Questions. Stops at the Enhance hand-off; pairs upstream with `avp-pov-builder`. |
| [`avp-pov-builder`](aivalue/avp-pov-builder.skill) | `aivalue/` | Turns AVP Enhance outputs (Task Analysis + Use Case Generation) into a standalone HTML "Slalom PoV on AI Transformation" dashboard — a provocative, defensible case for AI at a client. Two-stage portfolio downselect with 10K Monte Carlo, canonical 7-tab layout, industry overlays. Pairs downstream with `avp-input-builder`; runs standalone if AVP outputs already exist. |
| [`prd-writer`](prd/prd-writer.skill) | `prd/` | Writes zero-ambiguity Product Requirements Documents and Technical Design Documents intended to drive autonomous Claude Code CLI execution. |
| [`meetingviewer`](meetings/meetingviewer.skill) | `meetings/` | Paste a meeting transcript (VTT, Markdown, or plain text) and receive a polished single-page HTML report with executive summary, themes, sentiment analysis, action items, and Slalom brand styling. Works in Claude chat, CoWork, and Claude Code. |
| [`slalom-sow`](engagements/slalom-sow.skill) | `engagements/` | Generate a professional Slalom Statement of Work from engagement inputs (proposal, SPRO, scope notes, team roster, pricing, timeline). Delivers a complete, client-ready SOW as a Markdown artifact. |
| [`slalom-blog-writer`](content/slalom-blog-writer.skill) | `content/` | Write a publication-ready Slalom thought leadership blog post using notes, transcripts, presentations, or raw ideas as source material. Applies full Slalom brand voice and editorial standards. |
| [`doc-to-markdown`](utils/doc-to-markdown.skill) | `utils/` | Convert a PDF, Word (.docx), or PowerPoint (.pptx) to clean Markdown. Upload the file in chat/CoWork to receive a Markdown artifact; provide a file path in Claude Code to write the .md file to disk. |

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
unzip -p aivalue/avp-pov-builder.skill avp-pov-builder/SKILL.md | head -5
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
