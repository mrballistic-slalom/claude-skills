# Benefit Classification

How to classify each UC's annual benefit by type, and how to surface the classification in a way a CFO can defend.

The legacy `primary_benefit` field on AVP Use Case Generation rows (OPERATIONAL_EFFICIENCY / RISK_COMPLIANCE / etc.) describes *what kind of business outcome* the UC produces. **It does not answer the question a CFO actually asks**, which is:

> *"Of the $X total annual benefit, how much is real cost reduction, how much is revenue, how much is productivity-converted-to-dollars, and how much is something else?"*

Without this classification, the headline "$X annual benefit" reads as inflated. With it, the same number is defensible.

---

## The five detail classes

Every UC's annual benefit falls into one of these:

| Class | Definition | Hits the P&L as |
|---|---|---|
| **Hard cost reduction** | A real expense line that goes down. Fuel, electricity, contractor spend, contact-centre cost, storm O&M. | Direct GAAP-style cost reduction |
| **Productivity savings** | Time saved × loaded cost. The hours go away even if positions don't. | Cost-side savings only when positions are reduced or work expands. Otherwise capacity gain. |
| **Cost avoidance** | A future cost that doesn't get incurred. Avoided peaker investment, avoided regulatory fine, avoided customer attrition. | Counterfactual — never appears in actuals; defended through engineering / actuarial calculation |
| **Revenue assurance** | Recovering revenue the company is *owed* but not currently capturing. Billing accuracy, theft detection, lost-claim recovery, churn reduction in legacy contracts. | Top-line; sometimes called "revenue protection" or "leakage prevention" in industry vernacular |
| **Incremental revenue** | New revenue that wouldn't exist without the AI. Capacity factor uplift on renewables, new product personalization lift, expanded segment penetration. | Top-line, net new |

**Rule:** Every UC's annual benefit must classify into exactly one of these five. If a UC has mixed sources (e.g., 60% productivity + 40% revenue assurance), pick the dominant category and note the split in the modal's basis text. Don't double-count.

---

## The three executive buckets

For executive presentation, roll up the five into three:

| Executive bucket | Rolls up | What it means to a CFO |
|---|---|---|
| **Cost-side savings** | Hard cost reduction + Productivity savings + Cost avoidance | "We will spend less or avoid spending" |
| **Revenue assurance** | Revenue assurance | "We will collect more of what we're already owed" |
| **Incremental revenue** | Incremental revenue | "We will generate net-new top line" |

These three are the *anchor* for the value section. The five-class detail lives behind a disclosure / on the Assumptions tab.

---

## Why this matters for the executive narrative

If a client has a stated savings target (most do — "$XM in AI savings by Year N"), the question is whether the portfolio meets it. The three-bucket framing lets you answer cleanly:

- *"Cost-side savings + revenue assurance = $97M, aligned with the client's $100M savings target."*
- *"$6M in incremental revenue is additional upside outside the savings target."*

Without the breakdown, the same numbers read as either:
- **Inflated** ($103M total benefit looks like all-savings, which a CFO will challenge)
- **Hidden** (the revenue and cost-avoidance components are buried, and a CFO who wants traceability can't get it)

---

## Display patterns

### Value section on the executive tab

```
TOTAL ANNUAL BENEFIT AT FULL DEPLOYMENT
$103M

[Cost-side savings $72M]   [Revenue assurance $25M]   [Incremental revenue $6M]
 Hard cost · productivity   Billing accuracy · theft   Renewable performance
 · cost avoidance           / leakage detection        optimization

▶ See the 5-category breakdown
   [discloses: $34M Hard cost · $30M Productivity · $8M Avoidance · $25M Revenue assurance · $6M Incremental]

$X (cost-side savings + revenue assurance) is aligned with [client]'s stated $XM savings ambition.
$Y in incremental revenue is additional upside outside the savings target.
```

The total is the dominant visual element. Buckets sit subordinate. Five-category detail is one click away for the analytical reader.

### Per-UC modal

A small `benefit_type_class` pill under the UC title, with a 1-line description:

> **HARD COST REDUCTION** — Reduces fuel and purchased-power overruns; hits the P&L directly.

Or:

> **PRODUCTIVITY SAVINGS** — Productivity gain across N FTEs; only hits P&L if positions are reduced or work expands.

This single pill tells the reader what *kind* of benefit they're looking at, which contextualises the dollar figure that follows.

### Assumptions tab — definitions block

Three of the six "What we mean by these numbers" definitions cover this:

- **Gross benefit** — sum across UCs of all five classes
- **Cost-side savings** — the bucket aligned with most clients' "savings" targets
- **Incremental revenue** — net-new revenue, framed as upside outside any savings target

---

## Multi-industry examples

| Industry | UC | Class | Notes |
|---|---|---|---|
| Utilities | Outage prediction & ETR | Hard cost reduction | Storm O&M reduction is a real expense line |
| Utilities | Field worker copilots | Productivity savings | Hours saved by linework crews; counts as savings only if crew size adjusts or scope expands |
| Utilities | DER orchestration | Cost avoidance | Avoided peaker investment is a counterfactual |
| Utilities | Meter-to-cash | Revenue assurance | Recovering unbilled energy and billing-error losses |
| Utilities | Wind/solar optimization | Incremental revenue | Net-new generation revenue |
| Mortgage origination | Underwriter copilot | Productivity savings | If FTE count holds, this is capacity gain, not savings |
| Mortgage origination | Pre-approved at listing | Incremental revenue | New pull-through that wouldn't exist without AI |
| Mortgage origination | Fair-lending monitoring | Cost avoidance | Avoided regulatory fine + remediation cost |
| Specialty pharma | MSL HCP-engagement copilot | Revenue assurance | Protecting share-of-voice in existing accounts |
| Specialty pharma | Trial-design optimiser | Incremental revenue | Faster time-to-NDA → earlier launch revenue |
| HR transformation | Talent-acquisition automation | Hard cost reduction | Reduces external recruiter spend |
| HR transformation | Learning-content personalization | Productivity savings | Time-to-competency gain; counts as savings if training budget reduces |

The taxonomy is industry-agnostic; the *examples* should be drawn from whichever industry the engagement targets. When writing a new PoV, populate the modal `benefit_type_class` per UC using the table above as a template.

---

## Per-engagement class name overrides

The five default class names work for most for-profit engagements. When the audience's context makes a default name misleading or tone-deaf, override the label — not the underlying classification logic.

### Override rules

1. **The override changes the label everywhere it appears:** hero buckets, KPI strip, per-UC modal pill, phasing benefit composition cards, Assumptions tab definitions. No exceptions — a partial rename creates confusion.
2. **The financial math is unchanged.** "Access & capacity utilization" is calculated identically to "Incremental revenue." The override is cosmetic.
3. **The 3-bucket executive roll-up inherits the override.** If "Incremental revenue" becomes "Access & capacity utilization," the third executive bucket changes name too.
4. **Document the override in the Assumptions tab:** *"Benefit class 'Incremental revenue' is labeled 'Access & capacity utilization' in this analysis to reflect [organization name]'s nonprofit mission framing. The underlying calculation is identical to the standard revenue methodology."*

### Override registry (growing list — add new overrides as they're used)

| Default class | Override | When used |
|---|---|---|
| Incremental revenue | Access & capacity utilization | Nonprofit health systems |
| Incremental revenue | Constituent service capacity | Government / public sector |
| Incremental revenue | Member value growth | Cooperatives, credit unions |
| Incremental revenue | Mission delivery expansion | Foundations, NGOs |
| Hard cost reduction | Stewardship savings | Nonprofits sensitive to "cost cutting" |
| Hard cost reduction | Operational efficiency | Union/labor-sensitive environments |
| Revenue assurance | Reimbursement integrity | Health systems |
| Revenue assurance | Rate-base protection | Regulated utilities |
| Revenue assurance | Fund recovery | Government |

Capture the active overrides in `engagement-config.md` — 14.

---

## Anti-patterns

- **Calling everything "savings."** Inflates the headline; loses CFO trust on first scrutiny.
- **Calling productivity savings "GAAP cost reduction."** Productivity gain that doesn't reduce headcount or expand scope is *capacity*, not savings.
- **Hiding revenue assurance as "savings"** without disclosure. Many utilities do count revenue protection as savings internally — that's defensible — but only if the disclosure layer surfaces it.
- **Skipping the cost-avoidance label.** A counterfactual benefit is real but easier to challenge; calling it out invites the conversation rather than triggering it later.
- **Mixing classes within a single UC's headline number** without disclosing the split in the basis text.
- **Using "Incremental revenue" for a nonprofit health system.** A 501(c)(3) doesn't pursue "revenue growth" — it serves patients, which generates revenue as a consequence. "Access & capacity utilization" frames the same math correctly.
- **Overriding without documenting.** The Assumptions tab must explain the override. An unexplained non-standard label looks like a mistake, not a deliberate choice.

---

## Quick cheat sheet

```
For each UC:
  1. Classify the annual benefit into one of 5 detail classes
  2. Add benefit_type_class field to the data model
  3. Surface as a pill under the UC title in the modal
  4. Roll up to 3 executive buckets for the value section
  5. Anchor the headline (total) above the buckets
  6. Push 5-detail behind a disclosure
  7. Caption: "$X (cost-side + revenue assurance) aligned with [client]'s stated target;
     $Y in incremental revenue is additional upside"
  8. Check for class name overrides per engagement-config.md — 14
```
