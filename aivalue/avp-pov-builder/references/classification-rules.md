# Classification Rules

Every revenue and cost line in the dashboard gets one of three classifications. The mix drives the disclaimer language. **HEAVY is the default posture** — downgrade only with explicit user confirmation.

---

## The three classifications

### CLIENT_DATA
**Definition:** Number provided directly by the prospect, or extracted verbatim from their public reporting (10-K, earnings release, investor day, regulatory filing).

**Required:** Source citation in the basis string. Format: `"... (CLIENT_DATA: 10-K FY2024 Item 7)"`.

**In PoV mode:** Rare. PoVs are generic prospecting tools, not client-specific. CLIENT_DATA appears occasionally when the user pulls a public-reporting number in to ground a revenue pool estimate.

---

### BENCHMARK
**Definition:** Number anchored to a published industry benchmark from a credible source.

**Credible sources include:**
- Top-tier consulting firms: McKinsey, BCG, Bain, Deloitte
- Industry associations: MBA (mortgage), HIMSS (healthcare), SHRM (HR), SIFMA (capital markets)
- Industry analysts: Gartner, Forrester, IDC, Cornerstone Advisors
- Academic research: peer-reviewed journals, university research centers
- Regulatory bodies: Fed, FDA, OCC, FCA
- Slalom's own published research
- Slalom AVP benchmark library (cost, benefit templates from prior engagements)

**Required:** Source citation in the basis string with year. Format: `"... (BENCHMARK: McKinsey State of AI 2024)"` or `"... (BENCHMARK: MBA Mortgage Performance Report 2024)"`.

**Anti-patterns:**
- "Industry standard" with no source → not a benchmark, mark INFERRED
- A vendor marketing page → not credible, mark INFERRED or omit
- An AVP-generated `estimated_cost` alone → treat as INFERRED unless a public source was cited in the AVP session

---

### INFERRED
**Definition:** Slalom's reasoned estimate without an external benchmark anchor. Reflects experience, comparable engagements, judgment.

**Required:** The basis string must explain *why* this estimate. What comparable engagement informs it? What logical chain leads to this number?

**Examples:**
- ✓ *"$3M one-time build for the recommendation engine. Comparable to similar e-commerce recommendation deployments at mid-market retailers in our delivery experience. (INFERRED)"*
- ✗ *"$3M build because that's what these usually cost. (INFERRED)"* — opaque
- ✓ *"30% reduction in cycle time. INFERRED based on observed AI-assisted decisioning impact in comparable lending workflows."*
- ✗ *"$5M revenue uplift. (INFERRED)"* — no reasoning chain

**The test:** Could a smart skeptic in the audience ask "where does that come from?" and get a coherent answer? If yes, INFERRED is fine. If no, do more work or mark the bundle as "financial sizing to be validated."

---

## Tracking the mix

The dashboard's data model carries classification per line. Compute the mix:

```
total_lines = revenue_lines_with_value + cost_red_lines_with_value (across all bundles)
client_data_pct = CLIENT_DATA / total_lines
benchmark_pct = BENCHMARK / total_lines
inferred_pct = INFERRED / total_lines
```

---

## Disclaimer scaling

**HEAVY is the default.** Start every PoV here. Downgrade only if the user affirmatively confirms validation status.

### HEAVY mode — default for every PoV

Use this unless the user explicitly says otherwise. Includes both the standard disclaimer and the additional "built without prospect data" language.

*"All use cases, financial estimates, implementation costs, benefit projections, ROI figures, and payback periods presented in this dashboard are illustrative. Use cases are rooted in Slalom's AVP Enhance methodology applied to the domain; financial estimates are developed by Slalom using industry experience, publicly available benchmarks, and working assumptions about [topic] economics. They do not represent actual cost commitments, guaranteed outcomes, or formal proposals. Benefit ramp factors have been applied by tier to reflect typical enterprise AI adoption curves, but actual realization rates will vary based on organizational readiness, data quality, integration complexity, and change management execution.*

*This PoV was built without specific prospect data. Numbers are largely directional — the use cases reflect Slalom's AVP analysis of the domain, but the financial sizing is anchored to industry experience and publicly available reference points rather than prospect-specific operating data. They are intended to demonstrate Slalom's perspective on where AI value lives in this domain and to start a conversation about validation against the prospect's specific operating context. Order-of-magnitude is the goal; precision will come from deeper discovery.*

*All figures require validation through detailed discovery, scoping, and mutual agreement before being relied upon for any investment or operational decision.*

***Note on scope:*** *AI capability foundation investment (platform extensions, MLOps tooling, responsible AI governance, talent build-out, change management) is excluded from the portfolio financial model and will be scoped during validation. Portfolio NPV and investment figures reflect use cases only.*

***This material is prepared for exploratory conversation purposes only.***"

### STANDARD mode — if user confirms "some validation"

Use this if the user affirmatively says *"Some of these financial parameters have been validated"* — either through prospect conversations, prior Slalom engagement work with a comparable client in the current quarter, or equivalent. Drop the "largely directional" paragraph; keep the rest.

### TIGHT mode — if user confirms "validated"

Use this only if the user affirmatively says the financials have been validated against the prospect's reality OR drawn from recent Slalom engagement work on a directly comparable client. Drop the "built without prospect data" framing entirely.

*"Estimates in this dashboard are validated against industry benchmarks and, where indicated, the prospect's own public reporting or comparable Slalom engagement work. Validation through deeper discovery will refine these numbers but is not expected to materially change the portfolio thesis. AI capability foundation investment is excluded from portfolio financials and will be scoped during validation."*

### Always, regardless of mode

Include the foundation-excluded note: *"Note on scope: AI capability foundation investment is excluded from the portfolio financial model and will be scoped during validation. Portfolio NPV and investment figures reflect use cases only."*

---

## When to challenge the user on classification

If the user says "validated" during intake but the bundles Claude sees are 80%+ INFERRED on financial lines, push back:

> *"You mentioned some financial parameters are validated — just confirming, the bundles I have are mostly INFERRED on the financial side, which would default to HEAVY disclaimer. Is the validation you're describing on specific bundles, or at the portfolio level? I want to make sure the disclaimer language matches the underlying evidence."*

Never let a user's casual "yeah, it's validated" override a heavily-inferred financial model. The classification mix is the objective check.

---

## When user provides numbers that feel aggressive

If the user says "make the portfolio NPV $200M" without backing math, don't comply silently. Ask:

> *"What's the basis? If we're inferring, we need a reasoning chain in the basis string. If there's a benchmark, give me the source. Otherwise this gets flagged INFERRED with a weak basis note, which weakens the overall story."*

The classification discipline only works if the skill enforces it.

---

## Format in the data model

Each bundle has:

```json
{
  "id": "UC-XXX",
  "name": "...",
  "revenue": 5.5,
  "rev_basis": "...explanation... (BENCHMARK: source 2024)",
  "rev_class": "BENCHMARK",
  "cost_red": 2.0,
  "cost_red_basis": "...explanation... (INFERRED)",
  "cost_red_class": "INFERRED",
  "ot": 2.2,
  "ot_basis": "...explanation... inherited from AVP Use Case Generation estimated_cost aggregation, refined for integration complexity. (INFERRED)",
  "ot_class": "INFERRED",
  "on": 0.6,
  "on_basis": "...explanation... (INFERRED)",
  "on_class": "INFERRED",
  ...
}
```

Every line carries a classification. The QA pass reads all `*_class` fields, computes the mix, and verifies disclaimer language matches.

---

## INFERRED derivation chains — mandatory

Every INFERRED estimate must trace to what informed it. A bare `(INFERRED)` tag without a derivation is no longer acceptable — it fails the "where does that come from?" test before it reaches the audience.

### Derivation categories

Every I# reference falls into one of three categories:

| Category | Format | Example |
|---|---|---|
| **Derived from disclosed data** | `Derived from S# [+ S#]` | "Derived from S1 (total supply costs $3.1B) — surgical supplies estimated at 22-28% per Vizient 2024 benchmarks" |
| **Informed by published benchmark** | `Informed by B#` | "Informed by B45: Healthcare Purchasing News 2024 reports AI demand forecasting reduces healthcare inventory by 18-30%" |
| **Professional judgment** | `Professional judgment — validate during discovery` | "Professional judgment based on comparable Slalom engagement experience. No published benchmark available for this specific parameter." |

### Required fields per I# reference

Every I# in the data model must carry:

```json
{
  "ref": "I25",
  "variable": "AI-driven denial prevention rate",
  "value": "25%",
  "derivation": "Informed by B43",
  "secondary_source": "HFMA 2024 Revenue Cycle Intelligence Report: AI-assisted pre-submission denial prediction prevents 20-30% of initial denials when integrated with the claims scrubbing workflow",
  "note": "Midpoint of published range; conservative given {client}'s disclosed claim volume",
  "uc": "UC-03"
}
```

The `derivation` field is mandatory. The `secondary_source` field is mandatory for "Derived from" and "Informed by" categories; omit only for "Professional judgment."

### Rendering

**Assumptions tab — Inferred Estimates table** (mandatory section, positioned before Model Methodology):

| Column | Content |
|---|---|
| Ref | [I#] |
| Variable | Human-readable variable name |
| Value | The estimate |
| Derivation | Which S# or B# it derives from, or "Professional judgment" |
| Secondary research source | Full citation of the published source that informed the range |
| Used in | UC ID |

**Sources tab — Benchmark Library table** (mandatory section, positioned after Primary Sources):

| Column | Content |
|---|---|
| Ref | [B#] |
| Source & finding | Full citation including publication, year, and the specific quantitative finding |
| Informs | Which I# variable(s) this benchmark supports |

This completes the audit chain: **UC modal → I# tag → Assumptions tab (derivation + secondary source) → Sources tab (full benchmark citation).**

### Per-UC modal — "How we sized this" section

Every UC modal must include a "How we sized this" section. See `design.md` — 24 for the visual template (formula, variable table, CSS tooltips, source legend). The formula and variable table are what make "illustrative" a feature rather than a disclaimer. A UC without this section cannot ship.

### Derivation anti-patterns

- **Bare `(INFERRED)` without derivation.** Every I# must trace to something. If nothing informed the estimate, it's "Professional judgment" — say so explicitly.
- **Citing a benchmark source but tagging as INFERRED.** If a published benchmark informed the range, create a B# reference and tag the derivation as "Informed by B#." The I# tag is for the *estimate itself* (which may sit at a specific point within the benchmark range); the B# tag is for the *published source* that established the range.
- **Secondary source without year.** Every benchmark citation must include the publication year. "McKinsey reports 30-40% improvement" is undated and uncheckable. "McKinsey 2024 AI in Healthcare Operations: 30-40% improvement" is verifiable.
- **Formulas that don't produce the stated number.** The variable table in the modal must approximately reproduce the annual benefit figure. If the multiplication doesn't check out, the formula has a gap — either add the missing variable or adjust the narrative.
