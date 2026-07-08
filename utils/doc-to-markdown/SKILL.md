---
name: doc-to-markdown
description: Convert a document to clean, well-structured Markdown. Use when the user wants to convert or extract a PDF, Word document (.docx), or PowerPoint (.pptx) to Markdown. In Claude chat and CoWork, the user uploads the file and receives a Markdown artifact. In Claude Code, the user provides a file path and the converted .md file is written alongside the original.
---

# Doc to Markdown

Convert a document to clean, well-structured Markdown, preserving all substantive content exactly — headings, tables, lists, inline formatting, and speaker notes.

---

## Step 1 — Get the document

**In Claude chat or CoWork:** Ask the user to upload their PDF, DOCX, or PPTX file if they haven't already. Once uploaded, read the file using your native document-reading capabilities.

**In Claude Code:** Ask the user for the file path if not already provided. Read the file from disk.

Detect the file type from the extension and follow the appropriate section below.

---

## PDF (`.pdf`)

1. Extract full text, preserving reading order.
2. Identify and map structure:
   - ALL-CAPS lines or visually prominent text → `##` headings
   - Numbered or bulleted items → ordered or unordered lists
   - Tabular data → Markdown tables with a header row and `| --- |` separator
   - Page boundaries → `<!-- Page N -->` comments (remove these in the final clean-up pass if pagination context isn't meaningful)
3. Decode any encoding artifacts:
   - `(cid:NN)` tokens → map to `chr(N + 29)`, applying Windows-1252 overrides for range 130–159 (curly quotes, em-dashes, bullets, etc.)
   - Leave legitimate Unicode characters (●, ☐, •, ", ", –, —) in place
4. Clean up:
   - Remove lines that are only underscores (blank form fields)
   - Collapse 3+ consecutive blank lines to 2

---

## Word document (`.docx`)

Map styles to Markdown:

| Word style | Markdown |
|---|---|
| Heading 1–6 | `#`–`######` |
| Normal / Body Text | Plain paragraph |
| List Bullet / List Bullet 2 | `- ` / `  - ` |
| List Number / List Number 2 | `1. ` / `   1. ` |
| Quote / Block Text | `> ` blockquote |

Preserve inline formatting: `**bold**`, `*italic*`, `` `inline code` ``.

Render tables as Markdown tables with a header row (first row) and `| --- |` separator.

Collapse 3+ consecutive blank lines to 2.

---

## PowerPoint (`.pptx`)

Render each slide as a Markdown section:

- `---` slide divider before each slide
- Slide title → `## Slide N: <title text>`
- Body text: top-level bullets as `- item`, nested as `  - item`
- Tables: Markdown tables with `| --- |` separator
- Speaker notes: append under `> **Notes:**` blockquote after slide content
- Strip empty placeholder frames (no text content)

---

## Common post-processing (all formats)

After extraction:

- Convert ALL-CAPS section headings to the appropriate `##` level if not already mapped
- Replace decorative bullet symbols (➢, ✓, •, ▪, ►) with standard `-`
- Convert bare URLs to `[text](url)` hyperlinks where link text is apparent
- Add an `---` divider and italicise footer/copyright lines
- Preserve all substantive content exactly — do not paraphrase or summarise

---

## Deliver the output

**In Claude chat or CoWork:** Deliver the Markdown as a downloadable artifact named after the original file with a `.md` extension (e.g., `report.pdf` → `report.md`).

**In Claude Code:** Write the `.md` file to the same directory as the input file, replacing the original extension.

After delivering, confirm: total sections/slides found, any encoding issues encountered, and anything that may need a manual review pass (e.g., complex diagrams, scanned pages, embedded images).
