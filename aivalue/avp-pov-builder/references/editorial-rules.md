# Editorial Rules

Content discipline for what is otherwise a content-heavy artefact. Most of these rules exist because the absence of them produces work that reads as AI-assisted (over-labeled, over-structured, over-decorated) rather than executive-crafted.

These rules apply to the rendered HTML; they don't constrain the content itself.

**Visual design specs (type scale, card system, spacing, color palette, chrome, print fidelity, visual anti-patterns) have moved to `design.md`.** This file now focuses exclusively on content and editorial discipline — what you write and how it reads, not how it renders.

---

## Less is more — the Summary tab is the executive summary, full stop

**The Summary tab carries the hero and nothing else.** Title, tagline, big-one metric, supporting 2×3 KPI strip, phase strip, single-line context bridge. That's the entire tab.

All supporting depth — bridge waterfall, Why Now (forcing functions), Strategic alignment, AI Success Patterns, phase deep-dive, anchors, audit trails — lives on dedicated tabs (Why Now, AI Portfolio, Roadmap, Assumptions, Sources, optionally AVP Analysis).

**Why this matters:** An executive reader gives the Summary tab ~30 seconds. If those 30 seconds carry the title, tagline, and big-one cleanly, the dashboard has done its job. Cramming the bridge waterfall and four pattern cards onto the same screen dilutes the headline. The audience either skims past or gives up.

**Anti-patterns:**
- Bridge waterfall on the Summary tab — moves to Why Now
- "Why Now" forcing-functions block on the Summary tab — moves to Why Now
- Strategic alignment cards on the Summary tab — moves to Why Now
- AI Success Patterns cards on the Summary tab — moves to Why Now
- Phase cards with full UC tile lists on the Summary tab — slim Phase strip only; full deep-dive on Roadmap

The Summary tab is not a summary of the dashboard; it IS the dashboard's executive summary. Other tabs are the analytical defense.

---

## Narrative cohesion — title + tagline + big-one form a triangle

The hero's three written/numerical elements must cohere as a single message. They are not independent decorative choices.

**Cohesion test:** read title, tagline, and big-one in sequence. If the three together form a coherent claim, the hero works. If they pull in three different directions, rebuild.

**Examples that cohere (industry-agnostic):**

> Title: *"Three platforms. One AI strategy."*
> Tagline: *"An AI-enabled operating roadmap for [client]'s replatforming program."*
> Big-one: *"[$N]M after-tax NPV"*

The triangle: aspiration (title, tied to a publicly named replatforming program) → scope (tagline, the same program reframed for AI) → financial proof (big-one, CFO-defensible). Reader gets a three-beat story, each beat anchored in a stated client priority.

> Title: *"[N] million customers. One AI engine."*
> Tagline: *"Customer-experience acceleration at the scale of the [stated commitment]."*
> Big-one: *"+[$N]M incremental annual revenue"*

The triangle: scale (title, customer-base disclosure from annual report) → strategic frame (tagline, anchors to a stated commitment) → growth proof (big-one, top-line story).

**Examples that don't cohere (rebuild):**

> Title: "Three platforms. One AI strategy."
> Tagline: "AI-driven cost reduction across global operations."
> Big-one: "[$N]M incremental revenue"

The title implies platform unification; the tagline pivots to cost; the big-one is revenue. Three different stories, no triangle. None of the three even ties to the same stated objective.

**Truthfulness rules within the triangle:**

- The big-one must be defensible against the financial model — never an aspirational round-up
- The title must use the client's own brand language or stated priorities (no generic positioning copy)
- The tagline must accurately frame the dashboard's scope (no overclaim of what's covered)
- No element contradicts another

When a title or tagline candidate could only be true if the financial model is over-rounded, the candidate is wrong — pick a different candidate. Don't bend the model to the copy.

**Why this matters:** the title + tagline + big-one are the most likely things to get screenshotted, forwarded, or quoted. They get more downstream readers than the rest of the dashboard combined. A coherent triangle compounds; an incoherent one undermines everything that follows.

---

## Banned vocabulary — substitutes required

These read as either AI-assembled, MBA-jargon, or unprofessional in C-level deliverables. Replace before delivery.

| Banned | Substitute | Why it fails |
|---|---|---|
| plays / AI plays / 11 plays / in-flight play | initiatives / AI initiatives / in-flight initiative | "plays" reads as gambling or tactical; "initiatives" is neutral and covers all statuses |
| moats / moat | structural defenses / structural defense / long-term insulation | "moat" is MBA-deck jargon; substitutes are precise |
| named publicly / publicly named / has named publicly / has named (in this sense) | in flight / already in flight | "named publicly" is awkward construction; "in flight" covers all statuses (deployed, announced, in build) |
| Slalom-additive / additive PoV / additive proposal | Slalom-identified / Slalom's PoV / identified use cases | "additive" implies value-stacking; "identified" is honest about the analytical work |
| C-suite (in user-visible body) | executive audience / executives / decision-makers / [omit and describe work] | "C-suite" reads as agency-deck shorthand |
| Plan→Scale / Execute Initial / Execute Deepen (phase-card labels) | Foundation work / Deploy Year 0 / Deploy Year 1 / Deploy Year 2 (or topic-specific plain language) | Arrow-and-verb-noun jargon obscures what the phases actually do |
| AVP-grounded / AVP-driven (in user-visible body) | grounded in AVP Task Analysis / built from AVP outputs | "-grounded" suffix reads as marketing copy; explicit phrasing is clearer |
| never overlapping / non-overlapping bundles | distinct bundles / each bundle traces to its own anchor | unnecessary qualifier; the property is implicit in the methodology |
| forcing-function context (in body) | what makes this urgent today / why now / the case for moving now | jargon transitional copy that doesn't earn its place |
| Required HEAVY disclaimer posture / HEAVY (in body) | [internal authoring note — must not appear in body at all] | this is an internal label that has leaked into shipped work |
| Velocity wins (phase label) | Quick wins (Year 0) | consultant-cute label; plain English wins |
| Compounding (phase label) | Scale (Year 1) | same — describe the work, not the metaphor |
| Backlog activation (phase label) | Backlog (Year 2+) | same |
| Capacity bolt-on, not org build / [any X-bolt-on construction] | Add capacity through partners — not headcount / [explicit substitute] | "bolt-on" reads as tactical jargon |
| The window for AI is open and closing / window is open and closing | First movers are pulling ahead — the gap is widening / [equivalent forward statement] | mixed metaphor that lands awkwardly |
| Where the financial value lives (matrix subtitle) | The financial value / Portfolio map: NPV vs payback / [plain alternative] | "lives" is consultant-speak |
| How $XM run-rate value lands / [any "where it lands" copy in body] | Where the $XM comes from / The run-rate breakdown | same — "lands" and "lives" are both consultant tics |
| bundled from N AVP features across N tasks (legacy phrasing) | assembled from N AI enhancements identified across N key activities in the [function name] processes | aligns with the client-facing terminology table in SKILL.md |
| 0 UCs / 0 use cases (in count cells when count is genuinely zero) | UCs N/A / — | a literal `0` in a count slot reads as "we missed something"; explicit N/A signals "by design" |
| TBC (in dollar cells, including Phase 0 placeholders) | order-of-magnitude anchor (e.g., `~$8–12M*`) per `engagement-config.md` — 4 | TBC in a financial cell undermines credibility of every other number on the tab |

This list grows over time; flag any candidate addition during a build by checking the qa-checklist.md banned-words count test.

---

## First-use spell-outs — every acronym, on first body appearance

A non-finance VP reading a Slalom PoV dashboard hits ~30 acronyms in the first three tabs. Most are familiar to that reader; a meaningful minority are not. Spell-out discipline closes the gap without bloating the body copy.

**Universal acronyms** (always spell out on first use, regardless of in-scope functions):

| Acronym | First-use spell-out |
|---|---|
| P50, P10–P90, P>90 | percentile outcomes from the 10,000-trial Monte Carlo |
| NPV | Net Present Value |
| IRR | Internal Rate of Return |
| WACC | Weighted Average Cost of Capital |
| hurdle rate | internal hurdle (target return) — typically WACC + 3–5% risk premium |
| UC | use case |
| AVP | AI Value Platform |
| L3 task | third level of the AVP task hierarchy: function → process → subprocess → task |
| LOE | Level of Effort |
| WBS | Work Breakdown Structure |
| Big Four | Deloitte, EY, KPMG, PwC |

**Function-specific acronyms** — see `engagement-config.md` — 9 for the per-function tables (CPQ, OEE, FP&A, AHT, MMM, etc.). Spell out on first occurrence within the relevant function's tab content.

**Mechanism options:**

1. **Inline parenthetical** on first occurrence: `Big Four (Deloitte, EY, KPMG, PwC) publications cite 30–40% productivity…`
2. **Tooltip on first occurrence** (preferred for concise body copy): use the CSS tooltip component per `design.md` — 11
3. **Glossary panel coverage** (for terms used heavily) — see `design.md` — 17 for the template

The glossary panel covers all universal acronyms; inline spell-outs and tooltips are the lighter-weight options for terms the glossary doesn't carry or where the reader has already passed it.

**Anti-pattern:** scattered, inconsistent spell-outs (Big-4 in one place, Big Four in another). Pick one form per term and use it everywhere after first use.

---

## Headings — sentence case, no terminal periods

- All h2 / h3 / h4 in sentence case
- Title Case reserved for proper-noun-style identifiers (use case names, brand-style offering names)
- **No terminal period on headings** — they're not sentences
- **No eyebrow + title duplication** — if the eyebrow says "Where this came from" and the h2 says "Where this came from", delete the eyebrow

**Eyebrow usage rules:**
- Reserved for *category context*, not section titles
- Used only where a small-caps tag genuinely adds meaning the heading doesn't carry (e.g., "AI SUCCESS PATTERNS" eyebrow above a section that needs the framing)
- Never used as a redundant restating of the section title

---

## Forcing-card tagline — every Why Now card needs a one-liner

Each forcing-function card on the Why Now tab carries a one-sentence plain-English tagline directly under the title. See `design.md` — 17 for the HTML template.

The tagline gives a non-finance VP an instant read of the card's stake. Without it, the title can feel slogan-like and the body forces the reader to do the framing work themselves.

**Examples:**

| Title | Tagline |
|---|---|
| AI is now table stakes — and the 5%/25% gap is widening | Peers are deploying. Standing still costs more than moving. |
| Sales Enablement is the highest-leverage commercial AI domain | A 1% productivity lift across thousands of sellers compounds across millions of customer interactions. |
| Customer Service is the most demonstrably-ready AI domain in the enterprise | Voice AI, agent assist, and warranty automation — the easiest wins to land first. |

**Rule:** every forcing card with a `<div class="forcing-title">` must have a matching `<div class="forcing-tagline">` immediately after. The QA sweep verifies title-count == tagline-count.

---

## Narrative uniqueness — phase cards, function panes, modal sections

Boilerplate copy that repeats across function panes signals "this was templated, not written for me." The opposite — function-specific narratives — signals analytical depth.

**Phase cards** (Roadmap tab, four phases × seven function panes = 28 cards):

- Phase 0 description: shared across functions (it's the same shared platform investment, by design — one description × 7 panes is correct)
- Phase 1, 2, 3 descriptions: **unique per function**, referencing function-specific work (Sales Enablement Phase 1 should describe pipeline analytics + deal velocity; Finance Phase 1 should describe close acceleration + AP/AR; etc.)

The QA sweep counts unique descriptions per phase across the 7 function panes. Phase 0 should have exactly 1 unique description; Phases 1, 2, 3 should each have 7 unique descriptions. Anything less is boilerplate that needs rewriting.

**Forcing-function cards:** every card body should reference function-specific evidence (function-named systems, function-specific peers, function-tied benchmarks) — never a generic "AI in [function] is high-leverage" stub.

**UC modal narratives:** every UC's "Where it lands" + "Risks & mitigations" should reference function-specific tooling, process names, or anchor codes. Boilerplate like "improves productivity" without function context is a red flag.

---

## No contradictory metrics juxtaposed in the same surface

When two metrics describing the same thing appear together (in a hero, KPI strip, or per-UC modal), they must agree directionally and rhyme in scale.

**Failure example:** `5-yr ROI 1.3x` next to `IRR 125%` in the same UC modal. Both true; juxtaposed they read as conflict (ROI 1.3 sounds modest; IRR 125% sounds exceptional). A reader pauses to reconcile.

**Resolutions:**

1. Drop one (usually the weaker framing — `1.3x` is less defensible than `IRR 125%`)
2. Rename the weaker one to clarify scope (`5-yr Benefit-to-cost ratio: 1.3 to 1`)
3. Show only the stronger metric in the surface; carry the other in the disclosure-level table

The rule applies to: hero KPI tile, modal KPI strip, phase cards, and any "at-a-glance" summary block. Inside long-form analytical text, juxtaposition is fine — context disambiguates.

---

## Repetition — say it once

Any single fact in the artefact should appear in *at most* two places: the executive surfacing and the analytical detail. If a fact appears in three places (e.g., hero number + section heading + sub-section + table column), collapse.

**Common offenders:**
- The headline financial total (often appears in hero, breakdown footer, econ strip, phase summary, modal stat — pick two homes)
- Use case category labels (often appear in pill + table column + chart legend + matrix legend — pick the two that matter most)
- Strategic anchor names (often appear in card title + UC modal + Tab N section — list relationships at most twice)

---

## Asterisk system for the realization factor

When a portfolio realization factor is applied (per `financial-model.md` — Portfolio realization factor):

- Every benefit-derived metric in user-visible body text carries an asterisk (`*`) after the number — hero, KPI strip, range cards, modal KPIs, bucket cards, table cells, chart axis labels
- Cost-side metrics (implementation, ongoing run cost, capital outlay) carry NO asterisk — they are 100% as modeled
- One definition line per tab, placed near the disclaimer band. Use the locked language from `financial-model.md` — Asterisk system
- Per-UC modals additionally show both "full deployment" and "modeled" values for benefit-derived metrics — that's not asterisk repetition, it's drill-down disclosure

Don't over-explain. Don't repeat "modeled at 65%" in every KPI sub-text — the asterisk + single definition does the work.

---

## Disclaimer placement

Per `structural-rules.md`: disclaimer at the top of every tab. **Don't repeat the same long disclaimer multiple times within a single tab.**

If a tab has multiple disclaimer-warranting blocks (e.g., hero metric + sensitivity range + per-UC modal), the tab-level disclaimer is sufficient; sub-section "ILLUSTRATIVE" eyebrows are the right granularity for inline reminders.

---

## Repetition-bounded basis phrasings

Tables that show source/basis text often end up with the same phrase repeated 6+ times because every row genuinely traces to the same composite (e.g., "Industrial mid-cap composite" used as the basis for half a dozen assumption rows).

**Cap repetition at 2 per phrase per table.** If the same basis phrase shows up 3+ times, vary the wording:

- First instance: `Industrial mid-cap composite (8.5–9.5% range)`
- Second: `Mid-cap industrial composite (target 8–12%)`
- Third: `Industrial composite, 1–2% of revenue`
- (or refactor to a single anchor row that subsequent rows reference)

A column of identical text reads as "one source typed seven times" rather than "seven independently anchored assumptions."
