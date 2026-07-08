# Hero Lock — Phase 8.5

Phase 8.5 sits between Phase 8 (AI Success Patterns mapping) and Phase 9 (Build the HTML). It is a **gated user sign-off** on the hero composition before tokens are spent rendering 3,000-line HTML.

**Why this exists.** Historical iteration data shows that the highest churn happens *after* the first complete render — title swaps, tagline rewrites, big-one swaps, KPI strip reorderings. Each post-render revision re-renders the full HTML and re-reads it on the next turn. A pre-render hero lock catches the same decisions at a fraction of the cost.

---

## What gets locked

Five components, in order:

1. **Title** — the chosen option from Phase 9's options-driven flow (3–5 candidates → user picks one)
2. **Tagline** — the chosen option (2–3 candidates → user picks one, predicated on the locked title)
3. **The big-one** — metric label + value + timing modifier, picked specifically for the audience
4. **Supporting 2×3 KPI strip** — six metrics: top row "What it delivers", bottom row "What it costs"
5. **Phase 0 strip preview** — Phase 0/1/2/3 chips with UC counts (auto-derived from the locked portfolio, not user-picked)

---

## The hero-lock preview format

A one-screen markdown preview presented to the user before any HTML render. Not the rendered HTML — a tight text representation of what the hero will say.

```markdown
═══════════════════════════════════════════════════════════════════
HERO LOCK — {Client}
═══════════════════════════════════════════════════════════════════

TITLE:    "<chosen title>"
TAGLINE:  "<chosen tagline>"

BIG-ONE:  $XXM    <metric label>     (timing modifier)
          [audience driver: CEO/CFO/CIO/CMO]

KPI STRIP (2 × 3):

  WHAT IT DELIVERS
  ┌─────────────┬─────────────┬─────────────┐
  │ <metric 1>  │ <metric 2>  │ <metric 3>  │
  │ $X.XB/yr    │ N UCs       │ X.X yr      │
  └─────────────┴─────────────┴─────────────┘

  WHAT IT COSTS
  ┌─────────────┬─────────────┬─────────────┐
  │ <metric 4>  │ <metric 5>  │ <metric 6>  │
  │ $X.XM ot    │ $X.XM/yr    │ N mo        │
  └─────────────┴─────────────┴─────────────┘

PHASE STRIP:  P0 ↦ P1 (N UCs) ↦ P2 (N UCs) ↦ P3 (N UCs)

NARRATIVE TRIANGLE CHECK:
- Title → tagline → big-one: ✓ coherent / ✗ pulling apart
- Each grounded in a stated client priority: ✓ / ✗
- Big-one timing modifier explicit: ✓ / ✗

═══════════════════════════════════════════════════════════════════
LOCK THIS? [y/n/edit which element]
═══════════════════════════════════════════════════════════════════
```

The preview is plain text in the chat — no rendered HTML yet. The user has three responses:
- **y** / "lock it" → proceed to Phase 9 with these five components frozen
- **n** / "rethink" → return to Phase 9's options flow for whichever element needs alternatives
- **edit <element>** → swap that specific element (e.g., "edit big-one — try after-tax NPV instead")

---

## Anti-patterns

- **Skipping the lock and proceeding to render.** The whole point is to gate the expensive step. Render only after the user says "lock it."
- **Locking partially.** If the user says "the title's right but I want to see other tagline options," do not lock and proceed — return to Phase 9 for the tagline, re-present the full preview, and only lock when all five are confirmed.
- **Auto-locking on user silence.** Wait for an explicit confirmation. The cost of pausing is low; the cost of an unwanted render is high.
- **Sneaking in a render with the preview.** The preview is text only. No HTML, no styling, no embedded chart sketches. That would defeat the cost-saving purpose.

---

## Output

When the user locks, write the locked hero to the decisions log (`decisions-{client}.md` — 1 — Hero lock). On any subsequent revision that touches the hero, update that section in the log with the new lock and the revision date.

---

## Relationship to Phase 9

Phase 9 (Build the HTML) consumes the locked hero as input. It does not re-present options. It does not auto-tune the hero. It renders what was locked.

If the user wants to change the hero after Phase 9, that becomes a **post-lock revision** — return to Phase 8.5, update the preview, get a new lock, then edit-in-place (Optimized cost mode) or write a new version (Full-fidelity).
