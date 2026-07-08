# Intake Checklist

Use this script for Phase 1 of the build. The first question gates everything — this skill cannot run without AVP Enhance output.

**Goal of intake:** Get enough to build a defensible PoV without over-engineering the conversation. The whole intake should fit in 3-5 turns, not 15.

---

## Question 1 — AVP output (REQUIRED, ask first)

*"What AVP Enhance output do you have for me to work with? One or more of:*
- *Raw AVP business function export file(s) (`eiq_business_function_*.xlsx`) — I'll handle the bundling*
- *Pre-bundled use cases you've already clustered from AVP features — I'll render what you've built*
- *A mix of the above"*

**Possible user responses:**

- **"Here are the AVP export files"** (with files attached) → **Mode B.** Read files, proceed to Q2.
- **"Here are the bundled use cases"** (with list or file) → **Mode A.** Validate bundle data, proceed to Q2.
- **"Some of each"** → **Hybrid mode.** Proceed to Q2.
- **"I don't have AVP output"** or **"Let's do it from industry research"** → **STOP.** Respond:

> *"This skill requires AVP Enhance output as its source of truth for use cases. If you don't have AVP output, the options are:*
> - *Run AVP Enhance on the topic first, then come back here (happy to help scope the Enhance run)*
> - *Use a different deliverable type — happy to help draft an industry PoV memo, slide deck, or narrative without the dashboard structure*
>
> *Which would you like?"*

Do not proceed past this question without AVP output in hand.

---

## Question 2 — Topic

*"What's the PoV subject — process, industry, function, or company?"*

Examples:
- **Process:** "Mortgage Loan Origination & Underwriting", "Credit Risk & Default Management", "Pharmaceutical Trial Design"
- **Industry:** "Specialty Pharma", "Consumer Banking", "Medical Aesthetics"
- **Function:** "HR", "Corporate FP&A", "Product Marketing"

If the user's AVP files don't clearly map to the stated topic, flag it: *"The AVP output I have covers [X business unit/function], but you're framing the PoV around [Y]. Are we using the AVP output as the basis, with the topic as framing? Or is there a disconnect I should flag before bundling?"*

---

## Question 3 — Pattern type

*"Is this a process, an industry, or a business function?"*

This determines:
- Vocabulary for "phases" (for industry, phases describe market evolution; for process, operational maturity; for function, capability build-out)
- How archetypes are shaped
- Whether the Four Winning Patterns "In [topic]:" callouts lean operational or strategic

---

## Question 4 — Target audience

*"Who would you be sending this to? What role, in what kind of company?"*

Examples: *"Chief Lending Officers at super-regional banks"*, *"Heads of Medical Affairs at top-20 pharma"*, *"CHROs at $1-5B revenue companies"*

This shapes:
- The hero's 5% hook framing
- Which AVP-sourced bundles get foregrounded (Starting Three)
- The Ask language

---

## Question 5 — Supporting documentation

*"What additional materials do you have beyond the AVP output? Industry reports, prior Slalom pursuits, prospect public materials, any relevant benchmarks we should use for financial sizing?"*

Read everything before generating. Don't ask follow-up questions on things that are already in the docs.

---

## Question 5b — Client AI backlog (optional, ask once)

*"Does the client have an internal list of AI work already underway or in planning that they've shared with us? If yes, share it now — we'll merge it with public-source findings into the dashboard's 'in flight' acknowledgment section, alongside what we surface from secondary research.*

*If no, that's fine — we'll source the in-flight section entirely from public research. If neither yields anything, the section is omitted with a small disclosure."*

Record the answer. The combined set (client backlog + public-source acceleration plays) becomes the in-flight acknowledgment per `bundling-logic.md` — Step 1. The Slalom proposal portfolio sits net-new on top.

---

## Question 5c — Industry profile (REQUIRED, hard gate)

*"Which industry profile fits this client? Pick one — this drives the financial composite (WACC, hurdle rate, EBITDA margin or sector proxy, IT/marketing spend ratios, realization factor):*

- *Financial services — Banking* (depositories, full-service banks, credit unions when commercial-framed)
- *Financial services — Insurance* (P&C, Life, reinsurance, brokers)
- *SaaS / Tech* (mature; pre-revenue or pure-play crypto/biotech → custom)
- *Retail* (mass merchandise, specialty, e-commerce-led)
- *Hospitality / consumer services* (hotels, restaurants, experiences, leisure)
- *Telco* (carriers, MVNOs, cable/broadband)
- *Industrial / manufacturing mid-cap* (discrete + process manufacturers, industrial distributors)
- *Energy / utilities (regulated)* (vertically integrated utilities, regulated transmission)
- *Custom* (clear outlier — pick the closest profile and override every field from disclosed 10-K values)

*See `engagement-config.md` — 2a for the composite ranges per profile.*

*For non-standard structures (nonprofit health systems, government agencies, cooperatives, sovereign-backed entities), pick the closest profile above AND we'll layer on the financial-structure override (see 13) for tax/hurdle framing. Healthcare providers: most are nonprofit — let me know if so."*

**This is a hard gate.** Do not proceed past this question without a profile selected. There is no silent fallback to "industrial mid-cap" — the default is to ask, not to assume.

**When the user picks a profile, restate the composite back:** *"Got it — using the [profile name] composite: WACC X–Y%, hurdle X–Y%, [EBITDA or sector proxy] X–Y%, IT spend X% of revenue, realization factor 0.XX. I'll tighten these from [client]'s 10-K disclosures during Phase 2 research and document any swaps in the Assumptions tab. Sound right?"*

**Handle pushback:**
- *"Just use defaults"* → respond: *"There is no default — the composite affects every financial number in the dashboard. Pick the closest profile from the list above and we'll override fields from the 10-K. Takes 30 seconds."* Do not proceed.
- *"I don't know"* → ask one targeted question: *"What kind of business is this — broadly: bank, insurer, software, retailer, hotel/restaurant, telco, manufacturer, utility, or something else?"* Use the answer to pick.

**Writes to:** `engagement-config.md` — 2 (`industry_profile` field) and seeds the initial values for `wacc_pct`, `hurdle_rate_pct`, `ebitda_margin_pct`, `it_spend_ratio_pct`, `marketing_spend_ratio_pct`, `portfolio_realization_factor`. Phase 2 research tightens these from 10-K disclosures.

---

## Question 6 — Use AVP `strategic_fit_score` as a bundling input?

*"Should I use AVP's `strategic_fit_score` as a primary bundling filter, or derive strategic fit independently from the Phase 2 research framework?"*

**Default: No** — strategic fit is derived from research-grounded strategic anchors. This produces stronger C-suite framing because anchors come from the company's own stated priorities, not AVP's domain-agnostic scoring.

**Set Yes** only when:
- Research is thin or anchors are ambiguous
- The user wants AVP scores as a tiebreaker during clustering
- The build is time-pressured and full anchor mapping is impractical

Record the answer and pass it to `bundling-logic.md`.

---

## Question 7 — Tab structure

*"Which tabs do you want? Pick from the canonical menu:"*

**Default 7-tab structure (canonical):**
1. **Summary** — single-screen executive summary (hero only: title, tagline, big-one + 6 KPIs, phase strip, 1-line context). Nothing else.
2. **Why Now** — In-flight acknowledgment (when applicable) + portfolio bridge waterfall + Why Now (forcing functions) + Strategic alignment ("Your goals. Our analysis.") + AI Success Patterns
3. **AI Portfolio** — 1–5 matrices selected at Phase 6.5 (audience-driven; see `portfolio-matrices.md`) + filterable use case table + considered-but-cut panel + evaluated-but-deprioritized panel
4. **AVP Analysis** — *(optional, only if user provides one or more value-chain images — see Question 10)*. AVP Task Analysis visualization showing AI-readiness across the value chain.
5. **Roadmap** — cost-vs-benefit cumulative chart + 3 callouts + 4 phase cards (Phase 0/1/2/3) + 3 benefit-bucket cards
6. **Assumptions** — Monte Carlo portfolio confidence + Company/sector profile + Inferred assumptions table `[I#]` + Gaps & limitations + Model methodology
7. **Sources** — Primary source signals `[S#]` + Benchmark library `[B#]` + Research methodology

**Tighter 5-tab variant (when editorial restraint matters most):**
1. Summary
2. AI Portfolio (with Why Now content folded in as a top section)
3. Roadmap
4. Assumptions
5. Sources

(AVP Analysis is optional regardless of variant — depends on Question 10.)

**Mandatory minimum:** Summary + AI Portfolio + Roadmap + Assumptions + Sources. Assumptions and Sources are never dropped — they are the audit backbone. Why Now becomes its own tab in the 7-tab default and folds into AI Portfolio in the 5-tab variant. AVP Analysis is added only when value-chain images are provided.

If the user has no preference, default to 7-tab and proceed. Confirm the choice before building.

**Editorial discipline (mandatory regardless of tab count):** *"Summary"* is the executive summary — title, tagline, hero metrics. **Nothing else.** All supporting depth — bridge, anchors, patterns, phase detail — lives on other tabs. This is the "tell the story with less, not more content" principle. See `editorial-rules.md` — Narrative cohesion.

**Citation routing.** Body-text references route to the correct tab on click: `[S#]` and `[B#]` → Sources tab; `[I#]` → Assumptions tab. Tab IDs are case-folded slugs of each tab name (`tab-summary`, `tab-whynow`, `tab-aiportfolio`, `tab-avpanalysis`, `tab-roadmap`, `tab-assumptions`, `tab-sources`). See `structural-rules.md` — Citation routing.

---

## Question 8 — Localization

*"I'm assuming US English / US$ based on the client being headquartered in the U.S. — confirm that's right, or specify a different convention (Canadian / British / Australian / European)."*

Make a guess from the client's HQ. **Always confirm** — don't infer silently. If the company operates primarily in a different market than its HQ (e.g., Canadian company with 60%+ U.S. revenue), ask which convention to follow.

Default rules per HQ:
- **U.S.:** US English, US$, MM/DD/YYYY dates
- **Canada:** Canadian English (colour, centre, organisation), C$, DD/MM/YYYY dates
- **U.K. / Australia:** British English (-ise endings), £ or A$, DD/MM/YYYY dates
- **Europe:** Locale-appropriate spelling, €, DD/MM/YYYY dates

---

## Question 9 — Output path

*"Where should I write the final HTML?"*

Don't assume `/mnt/user-data/outputs/` — that's a Claude.ai pattern. For local builds, default to the same directory as the input materials (e.g., the project folder containing the AVP exports). Confirm with the user before writing.

---

## Question 10 — AVP Analysis value-chain images (optional, multi-image)

*"Do you have value-chain images to embed on the AVP Analysis tab? Two modes:*

- ***Single-image mode** — one combined visual covering the topic. Provide the file path.*
- ***Multi-image mode** — one image per business function assessed by AVP (preferred when the AVP run covers ≥2 functions). Provide a path per function, keyed by function ID (e.g., F1 / F2 / F3). The dashboard renders a section per function, in function-number order, each with its own image card.*

*If neither, skip the AVP Analysis tab entirely (don't ship a placeholder).*

*If multi-image, prompt the user explicitly: 'Please provide [N] images, one per function. List file paths keyed by function: F1 → ... / F2 → ... / etc.' The build cannot proceed on assumed sequential file ordering — the user must confirm which image is which function."*

This is the AVP-derived visual showing the L1 → L2 → L3 hierarchy with AI-readiness color coding (typical: green = high readiness, yellow = medium-high, orange = medium-low, red = low).

If the user provides image path(s):
- Read each file, base64-encode it, embed inline in the AVP Analysis tab
- Tab name in the nav: **"AVP Analysis"** (tab ID `tab-avpanalysis`); section eyebrow inside the tab: **"AVP TASK ANALYSIS"** — visible AVP positioning on this tab is intentional
- Tab content per `structural-rules.md` — AVP Analysis tab (single- or multi-image mode)

If the user has no image, **skip the AVP Analysis tab entirely** — don't build a placeholder.

---

## Question 11 — Function-filter side panel (optional)

*"Should I add a left-side **function-filter side panel** to the dashboard? It's a vertical sidebar that stacks the in-scope functions as filter buttons. Clicking a function filters the entire dashboard — hero KPIs, AI portfolio cards, matrices, phasing chart, AVP Analysis section, assumptions — to that function's content. 'All Functions' is the default view.*

*This is most useful when the dashboard covers **≥2 business functions** and the audience wants to slice the portfolio by function (e.g., a CXO who'll spend time on Finance and another stretch on Supply Chain). For a single-function PoV, skip it."*

**Default:**
- **≥2 functions in scope:** include the side panel (recommended)
- **Single function:** skip (no value)
- User can override either way

**Behaviour when included:**
- 56-240px wide left rail/panel (style choice — solid sidebar or hover-to-expand rail)
- "All Functions" button at top + one button per function
- Each button: small color dot + 3-letter abbreviation + full function label
- Active button: highlighted with that function's color stripe
- Clicking a button: applies a `body.filter-<fn-id>` class; CSS hides non-matching UC cards, hero panes, function panes, chart panes, AVP Analysis sections, etc.
- "All Functions" view shows aggregated/all content (one combined hero, all UC cards visible, etc.)

**Implementation note for the build:** every per-function content block (hero, value section, AI portfolio cards, phasing chart, AVP Analysis section, function-specific assumptions) gets a `data-fn="<fn-id>"` attribute. Body class drives visibility via CSS — instant, no re-render. JavaScript only updates the body class and active-button state.

If included, also confirm:
- **Style:** solid 240px sidebar (always-visible labels) or 56px hover-to-expand rail (collapsed dots; expand on mouseover)?
- **Default solid 240px** unless the dashboard is content-heavy and screen real-estate is at a premium.

If skipped: don't render the sidebar; the body uses normal flow with no left padding.

---

## Question 12 — Cost mode

*"How should I handle revision economics? Three options:*

- ***Standard*** — *mixed: small edits in place, substantive revisions get a new version file*
- ***Optimized (default)*** — *edit in place for all revisions; bump the version number only at named milestones (first complete render, after user review, final delivery). Final artifact is identical to full-fidelity, ~65–75% less token cost.*
- ***Full-fidelity*** — *new version file on every revision; preserves every iteration as a snapshot. Pick this for high-stakes client-facing runs where audit trail of every change matters."*

**Default: Optimized.** This is the right answer for ~95% of Slalom internal builds — the final HTML is identical to full-fidelity. Only escalate to Full-fidelity when the user explicitly wants every iteration preserved on disk.

When the user picks **Optimized**, restate the implication: *"Got it — I'll edit the file in place between milestones rather than writing a new version on every change. I'll snapshot v1 at first complete render, vN+1 after you've reviewed end-to-end, and a final version when you say 'done.' If at any point you want me to snapshot an intermediate state, just ask."*

See `SKILL.md` — Cost mode for the full rules and the opt-in advanced levers (multi-session workflow, externalized assets, Haiku QA).

**Writes to:** `engagement-config.md` — `cost_mode: standard | optimized | full-fidelity` field.

---

## Hero options (presented during Phase 8.5 hero lock, not at intake)

These three decisions are presented to the user **at Phase 8.5 — Hero lock**, after Phase 8 (AI Success Patterns mapping) and before Phase 9 (HTML render). They are not in initial intake because they require Phase 2 research and the Phase 7 downselected portfolio to be complete. The skill proposes options with a recommendation, the user picks, then the skill presents the one-screen lock preview per `hero-lock.md` and waits for an explicit lock before Phase 9 renders.

### Title — 3 to 5 options

The skill presents 3–5 hero title candidates with rationale. Each option:
- Is grounded in the client's actual brand language, stated priorities, or competitive positioning
- Implies transformation or aspiration (verb-led where possible)
- Is truthful — never overclaims

Generic examples (each ties to a publicly stated client priority — see `structural-rules.md` — Hero element examples):
- *"Three platforms. One AI strategy."* (ties to a replatforming program named in 10-K and earnings calls)
- *"[N] million customers. One AI engine."* (leads with customer-base scale disclosed in annual report)
- *"From [N] [pilots/initiatives] to a portfolio."* (positions the PoV as scaler of publicly disclosed plays)
- *"The next decade of [domain] starts here."* (aspirational, future-facing — anchors to a stated horizon goal)

The skill ranks options by fit to audience + compelling-story potential and recommends one. The user picks one, requests more options, or writes their own.

### Tagline — 2 to 3 options under the chosen title

A 1-line subtitle that bridges the title to the dashboard content. Same options-with-recommendation flow.

### Hero metrics — including the "big one"

The skill proposes:
- One "big one" — the single most important takeaway, sized larger than the supporting strip
- Six supporting KPIs in the 2×3 grid below

Recommendations grounded in audience and the financial story. See `financial-model.md` — Hero metric selection.

The user picks the big one and confirms the six supporting metrics, or asks for alternatives.

**Compelling but truthful:** title + tagline + big-one form a coherent narrative triangle. The skill enforces no overclaim and no contradiction across the three. See `editorial-rules.md` — Narrative cohesion.

---

## Optional — ask only if relevant

### 14. Audience-relevant competitive context
*"What's the audience already thinking about this topic? Specific pain points, competitive pressure, recent industry events?"*

### 15. Slalom prior work on this topic
*"Has Slalom done relevant work in this space? Anything we should reference or build on?"*

### 16. Financial parameter validation
*"Are any financial estimates in your AVP output already validated by a prospect or comparable engagement? If so, I can downgrade the disclaimer from HEAVY to STANDARD or TIGHT. Default is HEAVY."*

Treat this as a **narrow** question — default assumption is HEAVY, and user has to affirmatively confirm validation before downgrading.

### 17. Final portfolio size (post-downselection target)
*"Phase 3 will bundle ~50 candidates from the AVP output — intentionally broad. After full financial sizing and Monte Carlo analysis, I'll composite-rank them and downselect. What's your target for the final portfolio — tight (8-12), standard (12-18), or comprehensive (18-25)? The candidates that don't make the cut stay visible as 'evaluated but deprioritized' with their MC metrics — they're a validated backlog, not waste."*

The broad pool size is driven by the AVP output, not by this question. This question sets the post-downselection target only. If the user says "just give me the best 10," that's tight. If they say "I want breadth," that's comprehensive.

---

## After intake — confirm scope before building

Restate back to the user in 6-8 lines:

*"Building a Slalom PoV on AI Transformation for [TOPIC] — a [PATTERN_TYPE]-level dashboard targeting [AUDIENCE]. Source: [N] AVP business function export files covering [list functions]. Mode: [A / B / hybrid]. **Industry profile: [profile name]** — composite WACC X%, hurdle Y%, [EBITDA or sector proxy] Z%, realization 0.XX (will tighten from 10-K in Phase 2). Financial structure: [for-profit / nonprofit / government / cooperative]. AVP `strategic_fit_score` as bundling input: [Yes / No]. In-flight inputs: [secondary research / client backlog / both / neither]. Tab structure: [7-tab default / 5-tab variant / custom subset]; AVP Analysis tab: [included / omitted (no images)]. Function-filter side panel: [included (solid 240px / hover-rail) / omitted]. Localization: [US English / Canadian / British / Australian]. Output path: [path]. Cost mode: [Standard / **Optimized (default)** / Full-fidelity] — Optimized means edit-in-place between milestones (v1 at first render, vN+1 after your review, final when you say 'done'). **Design variant: [canonical (default) / Multifile / Extended / custom]** — canonical is the default; named overlays apply only on explicit request. Broad pool: ~50 candidates → full financial sizing + Monte Carlo → composite-rank downselection to [N] final portfolio (target: [tight/standard/comprehensive]). Evaluated-but-deprioritized candidates rendered as validated backlog. Disclaimer: HEAVY (default). Four Winning Patterns framework, anchor-driven bundling, validation Ask. I'll present the broad pool for review, then the ranked downselection for confirmation, **then present a Phase 8.5 hero-lock preview before rendering HTML**. A `decisions-{client}.md` companion file will capture load-bearing judgment calls alongside the HTML. Proceed?"*

Wait for user confirmation before moving to Phase 2 research.

---

## Handling unclear or incomplete input

Don't guess silently. Ask one targeted question per turn until the gap is filled.

- **User says "PoV on HR" (or similar function-scoped ask) and attaches one AVP file** → confirm the AVP file is HR-scoped; if yes, proceed. If it's one of several functions that'll feed HR, ask whether other function files are coming.
- **User provides a thick brief plus AVP files but doesn't state pattern type** → ask Q3 only.
- **User provides bundled UCs but no AVP source** → ask: *"Do you have the AVP exports the bundles came from? Good to have them for QA trace and for identifying any high-strategic-fit features we might want to add to existing bundles."*

---

## Anti-patterns

- **Don't ask all 10 questions in one turn.** User will answer 3 and miss the rest.
- **Don't ask questions answered in supporting docs.** Read the docs first.
- **Don't proceed past Q1 without AVP output.** This is the hard gate.
- **Don't proceed past Q5c without an industry profile.** This is the second hard gate. There is no silent fallback to industrial mid-cap — every financial number in the dashboard depends on the composite. If the user resists, ask one targeted question to identify the closest profile and proceed from there.
- **Don't assume HEAVY is wrong.** It's the default. Tighten only with explicit confirmation.
- **Don't proceed past scope restatement without user confirmation.** The biggest source of rework is misaligned scope.

---

## Question 18 — Financial structure

**Ask:** *"What is the organization's financial structure? This determines the tax rate, hurdle rate, and how we frame credibility."*

| Option | Tax rate | Hurdle guidance | Action |
|---|---|---|---|
| For-profit corporation (default) | 22–30% | WACC + 3–5% (default 10.5%) | Use defaults |
| Tax-exempt nonprofit (501(c)(3), foundation) | 0% | Tax-exempt bond cost + 1–2% | Override both; activate P(NPV>0) caveat |
| Government / public sector | 0% | OMB A-94 or jurisdiction equivalent | Override both; activate caveat |
| Cooperative / mutual (credit union, member-owned) | 0% or reduced | Member cost of capital | Override both; activate caveat if tax < 10% AND hurdle < 8% |
| Other | Capture specifics | Capture specifics | Document in engagement config |

**If tax = 0% AND hurdle < 8%:** Inform the user that P(NPV>0) will be structurally near 100% and that the dashboard will shift credibility emphasis to payback and realization factor. Get explicit confirmation of the hurdle rate source (e.g., "AA+/Aa1 bond rating yields 3.5%; we use 6% with a 2% risk premium").

**Writes to:** `engagement-config.md` — 13 (Financial structure override)

---

## Question 19 — Benefit class naming

**Ask:** *"The default benefit classes are: Hard cost reduction, Productivity savings, Cost avoidance, Revenue assurance, Incremental revenue. Do any of these need different labels for this audience?"*

**When to probe:** Ask this when the organization is:
- Nonprofit (likely override "Incremental revenue")
- Government ("Revenue" framing may not resonate)
- Sensitive to "cost cutting" language (may prefer "Operational efficiency")
- Using sector-specific terminology the audience expects

**Common overrides by context:**

| Audience context | Default term | Better term |
|---|---|---|
| Health system (nonprofit) | Incremental revenue | Access & capacity utilization |
| Government agency | Incremental revenue | Constituent service capacity |
| Credit union / cooperative | Incremental revenue | Member value growth |
| Any nonprofit | Hard cost reduction | Stewardship savings |
| Union-heavy workforce | Hard cost reduction | Operational efficiency |
| Regulated utility | Revenue assurance | Rate-base protection |

**If user says "defaults are fine":** Skip overrides.

**Writes to:** `engagement-config.md` — 14 (Benefit class overrides)

---

## Question 20 — Non-financial value

**Ask:** *"Does this portfolio include use cases where the primary justification is non-financial — outcomes that matter to this audience beyond ROI?"*

**Examples to offer (based on sector):**
- Healthcare: patient outcomes, clinician wellbeing, health equity, community benefit
- Manufacturing: worker safety, zero-harm programs
- Financial services: regulatory compliance (mandatory, not ROI-driven)
- Energy: grid reliability, environmental impact, community safety
- Government: constituent equity, access, public safety
- Any: ESG commitments, DEI outcomes

**If yes, follow up:**
1. *"What should we call this category?"* → e.g., "Mission & patient outcomes"
2. *"How much weight should it carry in portfolio selection — enough to keep a break-even UC in the portfolio?"* → Recommend 0.20 for healthcare/nonprofit/government; 0.15 for regulated; 0.10 for ESG-committed commercial
3. *"What badge should flagged UCs carry?"* → e.g., "Mission & outcomes" *(text only — emoji badges are a QA hard-fail per `client-language.md`)*

**If no:** Set weight to 0.00. The composite ranking is financial + strategic only.

**Writes to:** `engagement-config.md` — 15 (Non-financial value weight)

---

## Question 21 — In-flight treatment mode

**Ask only when in-flight items exist** (from Phase 2 acceleration plays or client-shared backlog):

*"You have [N] AI initiatives already in flight. How should the dashboard handle them?"*

| Mode | Description | Best when |
|---|---|---|
| **Mode A** (acknowledge) | In-flight items appear as context on Why Now tab. Portfolio numbers are net-new only. | Cold prospecting; audience hasn't shared internal data; clean separation of "what they have" vs. "what Slalom proposes" |
| **Mode C** (include in analysis) | In-flight items are in the full analysis — charts, table, MC — with visual distinction (dashed borders, badges). Headline numbers include both but scope card distinguishes "N + M." | Audience owns the in-flight work; they want the complete picture; client has shared internal data (backlog slides, etc.) |

**Default:** Mode A (consistent with the skill's original posture).

**If the user says "include them":** Confirm Mode C and note: in-flight items will carry implementation costs of $0 (or the client-stated investment) and annual benefits sized from whatever information is available. They will have "In flight" badges throughout.

**Writes to:** `engagement-config.md` — 7 (In-flight statuses) + a new `inflight_mode: A | C` field

---

## Question 22 — Design variant (optional, ask once)

**Ask:** *"Should this build use the canonical Slalom design, or a named variant? Three options:*

- ***Canonical (default)*** — *the standard Slalom design system per `design.md` and the golden master at `references/golden-master.md`. Slalom Blue palette, sentence-case nav, 7-tab structure.*
- ***Multifile variant*** — *DM Sans / DM Mono typography, external multi-file CSS, `data-theme="multifile"` styling lineage. Apply only on explicit user request. See `references/design-variants/multifile.md`.*
- ***Extended variant*** — *extended palette with greens, custom dark navy, system font stack, includes Strategy and Monte Carlo as additional tabs. Apply only on explicit user request. See `references/design-variants/extended.md`.*
- ***Custom override*** — *new variant for this engagement. We'll capture the overlay in a new file in `references/design-variants/`.*"

**Default:** Canonical. Pick a named variant only when (a) the client matches the named variant's reference engagement, OR (b) the user explicitly wants the variant's styling lineage.

**When the user picks canonical:** confirm: *"Got it — canonical Slalom design. I'll compare the first render against the golden master at `references/golden-master.md` and flag any drift."*

**When the user picks a named variant:** confirm: *"Got it — applying the [variant] overlay from `references/design-variants/[variant].md`. The canonical Slalom rules in `design.md` still apply where the overlay is silent."*

**When the user picks a custom override:** ask: *"What's the new variant called, and what are the deltas from canonical — palette, typography, tab structure, layout? I'll write `references/design-variants/[name].md` so it's available for future builds too."*

**Writes to:** `engagement-config.md` — 16 (Design variant) — `design_variant: canonical | multifile | extended | <custom>`
