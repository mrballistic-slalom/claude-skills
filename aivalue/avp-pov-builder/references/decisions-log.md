# Decisions Log Companion

Every build produces a `decisions-{client}.md` companion file alongside the engagement config and the HTML. It captures the **judgment calls** made during the build — the things that aren't derivable from the engagement config or the AVP exports, and that would otherwise force re-debate on resume.

**Why this exists.** Without it, every revision session re-litigates matrix selection, hero tradeoffs, downselection overrides, and design choices. With it, resume sessions read the log and continue. The cost is one short file; the saving is hours of re-iteration.

---

## What goes in the decisions log

Six sections, in order. Skip a section only when no decision was made in that category.

### 1. Hero lock

The title + tagline + big-one + 2×3 KPI strip the user signed off on at Phase 8.5 (per SKILL.md Phase 8.5 — Hero lock).

```markdown
## 1. Hero lock — confirmed YYYY-MM-DD

- **Title:** "<chosen title>"
  - Options presented: <list of 3-5>
  - Why this one: <rationale>
- **Tagline:** "<chosen tagline>"
  - Options presented: <list of 2-3>
- **Big-one:** "<metric label + value>"
  - Options presented: <list>
  - Audience driver: <CEO/CFO/CIO/CMO framing>
- **Supporting 2×3 KPI strip:**
  - Top row ("What it delivers"): <metric 1> · <metric 2> · <metric 3>
  - Bottom row ("What it costs"): <metric 4> · <metric 5> · <metric 6>
```

### 2. Matrix selection (Phase 6.5)

Which matrices were chosen, which were demoted, why.

```markdown
## 2. Matrix selection — confirmed YYYY-MM-DD

- **Primary matrix:** <axis pair> — <why>
- **Secondary matrix:** <axis pair> — <why>
- **Demoted:** <axis pair> — <reason: IQR too low, audience mismatch, etc.>
- **Rendering order:** <list>
```

### 3. Downselection overrides (Phase 7)

Where the user pulled lower-ranked candidates up or pushed higher-ranked candidates down, against the composite MC rank.

```markdown
## 3. Downselection overrides — confirmed YYYY-MM-DD

- **Pulled up:** UC-N (composite rank #X → into portfolio)
  - Reason: <audience priority / strategic anchor / domain knowledge>
- **Pushed down:** UC-M (composite rank #Y → deprioritized)
  - Reason: <won't land / political / wrong moment>
- **Final portfolio size:** N net-new UCs
- **Deprioritized count:** M
```

### 3a. Portfolio view toggle (Phase 7 / Phase 9)

Whether the Prioritized ↔ All Evaluated toggle was rendered on the AI Portfolio tab — see `portfolio-view-toggle.md`. Captured explicitly because the guardrail says: suppress the toggle entirely when downselect ratio = 1.0 (broad pool == final portfolio). Single-state toggles are noise.

```markdown
## 3a. Portfolio view toggle — confirmed YYYY-MM-DD

- **Downselect ratio:** <final_count> / <broad_pool_count> = <ratio>
- **Toggle state:** rendered | suppressed
- **If suppressed:** <reason — typically ratio = 1.0 or user explicitly opted out>
- **Default view on load:** prio (only relevant when toggle is rendered)
```

### 4. Design variant in use

Which variant was applied — canonical or named override.

```markdown
## 4. Design variant — confirmed YYYY-MM-DD

- **Variant:** canonical | multifile | extended | <custom variant name>
- **Overlay file applied (if non-canonical):** references/design-variants/<name>.md
- **Deltas from canonical:** <short list — palette, type stack, structure>
```

### 5. Open questions / parking lot

Things the user wants to revisit before final but not now.

```markdown
## 5. Open questions

- [ ] Suppress portfolio view toggle if downselect ratio = 1.0? (forces an explicit decision rather than implicit behavior — see `portfolio-view-toggle.md` — Defaults & guardrails)
- [ ] <question 1>
- [ ] <question 2>
```

---

## Where the file lives

Same directory as the AVP exports and the HTML output. Filename: `decisions-{client-slug}.md` (e.g., `decisions-acme-corp.md`). On resume, read this file first.

---

## When to update

- **At each milestone bump** (per Cost mode rules in SKILL.md): write or update the relevant section before bumping the version
- **At final delivery:** flush all sections; mark the file as `_final` next to the HTML

The log is for *the user's future-self and a future Slalom team member*. Avoid build-time chatter; capture only the load-bearing judgment calls.

---

## What does NOT go in the decisions log

- Engagement config values (those live in `engagement-config-{client}.md`)
- AVP feature lists (those live in the AVP exports)
- Use case financial details (those live in the rendered HTML modal + Sources/Assumptions tabs)
- General build chatter or commit-style messages
