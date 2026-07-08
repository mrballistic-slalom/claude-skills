# Anchor Specificity

How to ground each strategic anchor in named public references so the artefact reads as authored on this client, not re-skinnable to any other client in the same industry.

The strategic anchors framework (see `primary-source-research.md`) maps every UC to a stated business objective. **Anchor specificity is what separates a credible "we started with your goals" claim from generic consulting structure.**

If a reader could replace the client name in your anchor section and have it still make sense, the anchors are too generic.

---

## The specificity test

For each anchor card / cluster, you should be able to point to *at least one of these*:

1. A specific filing or docket name (with case identifier where applicable)
2. A specific commitment, target, or program name disclosed publicly
3. A named event or incident that drove the priority
4. A specific named asset, region, or sub-fleet
5. A specific dated quote or line from earnings transcripts / annual reports

Generic phrases that **fail** the specificity test:

| Generic | Why it fails |
|---|---|
| "Multi-state regulatory burden" | True for every utility; identifies nothing |
| "Aging workforce challenge" | Industry-wide platitude |
| "Customer affordability pressure" | Doesn't ground in this client's specific stance |
| "Storm hardening priorities" | Every utility says this |
| "Capital deployment velocity" | Generic finance language |
| "ESG commitments" | Universal; says nothing about this client |

Specific replacements that **pass**:

| Specific | Why it passes |
|---|---|
| "NCUC E-7 / E-2 / E-100 Sub 179 (Carbon Plan biennial filings)" | Named state docket, specific case identifier |
| "Aging workforce in linework, generation operators, and switching procedures" | Named functions; not just "people" |
| "Active rate cases in NC E-7 + parallel proceedings in SC, FL, IN" | Specific dockets and jurisdictions |
| "Hurricane Helene (Sep 2024) Western NC recovery" | Named event with date |
| "$73B+ five-year capital plan announced Q3 2024 earnings call" | Sourced quantification |
| "HB 951 — 70% emissions reduction by 2030" | Named legislation with target |

---

## Multi-industry application of the rule

The rule is **the same across industries** — the substance differs.

### Utilities

Specifics to seek:
- State commission docket numbers (NCUC, SCPSC, FPSC, IURC, PUCO, KPSC, CPUC, etc.)
- IRP filing identifiers and biennial Carbon Plan / clean-energy filings
- Named coal retirements (Belews Creek, Marshall, Cayuga)
- Named storm events (Helene, Milton, Ida) and dates
- Specific renewable fleet sizing (~5GW solar + ~2GW battery per IRP)
- HB / SB legislation by state
- NERC compliance posture
- Named substation, transmission, or generation programs

### Mortgage origination

Specifics to seek:
- Specific CFPB enforcement focus areas of the past 12 months
- Named MISMO data standards adoption status
- Specific HMDA compliance posture (volume, jurisdictions)
- Named LOS / POS systems (Encompass, Blue Sage, ICE Mortgage Technology)
- Recent acquisitions or warehouse-line changes
- Named MBA performance benchmarks (cost-to-originate, cycle time)
- State-specific licensing (NMLS) burden

### Specialty pharma

Specifics to seek:
- Specific therapeutic area (rare disease, oncology, GI, neuro)
- Named compounds in pipeline (clinical trial NCT numbers)
- FDA AI/ML guidance compliance posture (named pre-cert, advisory committees)
- 21 CFR Part 11 / GxP audit history
- Named partnerships (CROs, manufacturing CMOs)
- Specific commercial-readiness milestones tied to NDA timelines

### Health systems / payers

Specifics to seek:
- Named CMS regulations (Stars rating cycle, MACRA, Interoperability rule)
- HEDIS measure performance
- Specific value-based contracts and quality metrics
- Named EHR (Epic, Cerner) and data warehouse vendor
- ACO / MA enrolment specifics
- State Medicaid contract specifics

### HR transformation / talent

Specifics to seek:
- EEOC enforcement focus area
- Named EEO-1 compliance posture
- Specific HRIS vendor (Workday, SuccessFactors, BambooHR)
- Recent organizational change (M&A, RIF, geographic expansion)
- Named industry talent benchmarks (SHRM cost-per-hire, time-to-fill)
- Specific union / Works Council relationships

### Retail / consumer goods

Specifics to seek:
- Named omnichannel program
- Specific category P&L pressure (margin compression in X category)
- Named loyalty program + tier structure
- Specific seasonal or geographic exposure
- Named ERP / POS / inventory systems
- Recent acquisition or DTC pivot

---

## How to source the specifics

Per `primary-source-research.md`, the Phase 2 protocol pulls from:

1. **10-K** — strategic priorities section, risk factors, MD&A
2. **10-Q** — recent updates, capital plan changes
3. **Earnings call transcripts** — direct quotes from management
4. **Investor day decks** — multi-year strategic frameworks
5. **Regulatory filings** — depending on industry (FERC, NCUC, FDA, CMS, OCC, etc.)
6. **Industry publications and analyst reports** — for context
7. **Recent press releases** — incident response, program launches, partnerships

Save citations with:
- Source name
- Date (YYYY-MM-DD)
- Specific identifier (docket, case number, filing ID, transcript page)
- Direct quote where possible

These become the `[S1]`, `[S2]`, ... primary-source citations on the dashboard.

**Citation routing rule:** `[S#]` and `[B#]` body refs route to the Sources tab (scroll to row); `[I#]` body refs route to the Assumptions tab (scroll to row).

---

## How specifics surface in the artefact

### Anchor target line (the gray subtitle under each anchor heading)

Compress the specifics into a `·`-separated list. **Aim for 2–4 named specifics per anchor.**

| Generic version | Specific version |
|---|---|
| "Methane & carbon emissions reduction · coal retirement · renewable scale-up" | "NC Carbon Plan (HB 951) · 70% emissions reduction by 2030 · coal retirements at Allen, Belews Creek, Marshall · ~7GW solar + ~2GW battery storage per IRP" |
| "Multi-state rate filings · bill management · smart-meter value capture" | "Active rate cases NCUC E-7 + E-2, parallel proceedings in SC / FL / IN · AMI (Itron) deployment near-complete in Carolinas · revenue assurance under affordability scrutiny" |

### Anchor "why this matters" body paragraph

Reference one specific event, target, or named asset in the first sentence. The reader should know after one sentence that this is about *this* client, not a category.

| Generic | Specific |
|---|---|
| "Storm response is a major focus driven by recent weather events." | "Hurricane Helene (Sep 2024) caused over 1M [utility] customer outages, with sustained 7+ day restorations across [region]." |

### Citation chips

Every quantification or commitment claim should carry a citation chip linking to the corresponding row in the Sources tab. **No specific = no chip earned.** The chip system enforces specificity.

---

## Anti-patterns

- **Adding specifics that aren't checkable.** "10–12k field workforce" is a defensible inferred estimate (cite as INFERRED with reasoning chain). "[utility]'s exact field-worker headcount of 11,247" with no source is fabrication.
- **Naming systems / dockets you're not certain about.** Better to say "NCUC E-7 docket family ([utility name])" than to fabricate a sub-number ("E-7 Sub 1213") that may not exist.
- **Using one client's specifics as a template** for another. Especially dangerous when re-purposing PoVs across utilities — strip and re-source from scratch.
- **Substituting generic industry vernacular for actual specifics.** "Multi-jurisdictional regulatory burden" is the kind of phrase that AI generation produces; "NCUC + SCPSC + FPSC + IURC + PUCO + KPSC + FERC + NERC" is what a human consultant writes.

---

## Quick cheat sheet

```
For each anchor:
  1. Identify the client's stated priority (10-K, earnings call, investor day, regulatory)
  2. Find at least one of: docket name, named target, specific event,
     named asset/region, dated public quote
  3. Compress 2–4 specifics into the anchor target line
  4. Open the body paragraph with a specific event or commitment
  5. Cite via chip system; ensure source row exists in the Sources tab

Specificity test: replace client name with "Acme Corp." Does it still make sense?
  Yes → too generic; rewrite
  No  → specific enough
```
