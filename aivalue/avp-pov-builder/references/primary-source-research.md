# Primary Source Research

**Phase 2 — runs before bundling, every time, regardless of mode.**

Its output directly informs financial sizing, archetype framing, assumption classification, and the Assumptions and Sources tabs. Do not skip this phase even when the user provides pre-bundled use cases — the research grounds the financial parameters.

---

## Research sequence

### Step 1 — Identify the company or sector

Determine whether the PoV target is a **named public company**, a **named private company**, or a **generic sector/process** (no named company).

| Target type | Go to |
|---|---|
| Named public company | Step 2 — direct pull |
| Named private company | Step 2 (partial) → Step 3 (comp logic) |
| Generic sector / process | Step 3 (comp logic) + Step 4 (analyst) |

---

### Step 2 — Public company primary source pull

For named public companies, pull all of the following:

**SEC filings**
- Most recent **10-K** (annual): Revenue, gross margin, operating expense breakdown, stated strategic priorities, any AI/digital transformation language in MD&A, risk factors, and capital allocation commentary.
- Most recent **10-Q** (quarterly): Any updated guidance, cost initiative updates, or AI investment commentary since the 10-K.
- Source: SEC EDGAR (`https://www.sec.gov/cgi-bin/browse-edgar`) or the company's investor relations page.

**Earnings call transcripts**
- Most recent full-year or quarterly earnings call. Search Seeking Alpha, The Motley Fool, or the company's IR site.
- Extract: management commentary on AI, automation, efficiency initiatives, headcount or cost targets, and any named technology investments.
- Verbatim management quotes are valuable — note them with source and date.

**Press releases (last 12 months)**
- Search for press releases mentioning: AI, automation, digital transformation, cost reduction, efficiency, or platform investments.
- Note any announced programs, partnerships, or vendor relationships relevant to the PoV topic.

**Key financial parameters to extract:**
- Total revenue + YoY growth rate
- Gross margin %
- Operating expense total + breakdown by line (SG&A, R&D, COGS, supply chain) — pull whichever lines map to the PoV topic
- Headcount (if disclosed)
- Any stated cost reduction targets or transformation investment budgets
- Capital expenditure breakdown if relevant

---

### Step 3 — Private company / generic sector comp logic

If the target is private or generic, identify **2-3 public comparables** in the same industry, segment, and approximate size band.

**Comp selection criteria:**
- Same primary industry (GICS or SIC code alignment)
- Revenue within ~2x of the estimated target company size (if known), or representative of the sector if generic
- Similar business model (e.g., B2B vs. B2C, asset-heavy vs. asset-light)
- Preference for companies that have spoken publicly about AI or digital transformation investment

**State the comp selection rationale explicitly** in the Research Brief and in the Sources tab. Format: *"[Comp ticker] selected as comparable: same [industry], similar [revenue band / model], publicly disclosed [AI/automation investment] in [year]."*

Run the full Step 2 pull on each selected comp. Flag all financial parameters derived from comps with `[COMP: {ticker}]` in the basis string.

---

### Step 4 — Analyst and industry context

Search for recent (last 18 months) credible secondary sources covering AI adoption in the topic's domain.

**Preferred sources (in order):**
1. McKinsey Global Institute, BCG, Bain, Deloitte (top-tier consulting research)
2. Gartner, Forrester, IDC (analyst reports)
3. Industry associations relevant to the topic (e.g., MBA for mortgage, HIMSS for healthcare, SHRM for HR)
4. HBR, MIT Sloan Management Review (practitioner academic)
5. Trade press specific to the industry (Fierce Healthcare, American Banker, Upstream, etc.)

**Also search for:**
- Slalom thought leadership on the topic (blog, case study, executive perspectives page) — check for alignment with the PoV narrative before building
- Any published AI benchmark specific to the process or function being analyzed

---

### Step 4.5 — Three mandatory research outputs

Before producing the Research Brief in Step 5, the research must explicitly produce these three outputs. Each becomes a direct input to bundling and writing.

#### Output 1 — Acceleration play discovery

Identify any AI capability the client has *already in flight* (in deployment, in build, or announced for launch). Search for:

- CIO / CTO interviews naming AI programs, vendors, or pilots
- Investor day presentations naming internal AI platforms
- Press releases announcing AI feature launches
- Earnings call mentions of AI deployment or named partners
- Vendor case studies with the client named (e.g., a Microsoft customer story, a Publicis Sapient case study)

For each found, record:

```
acceleration_play_id: AP-001
public_capability_name: [e.g., "[vendor] copilot scale-out"]
deployment_status: in production / in deployment / active collaboration / in build / announced for launch
named_partners: [list]
named_scope: [e.g., "N users → thousands"]
source: [URL + date]
supporting_anchor: [which strategic anchor (from the Phase 2 framework) this in-flight initiative supports — used for the in-flight section's anchor mapping, NOT for joining a Slalom bundle]
```

Each acceleration play feeds the dashboard's **in-flight acknowledgment section** — context for the audience, not a Slalom-proposed bundle. Sized at the play level for transparency. Per the bundling-logic rule, the Slalom proposal portfolio is always net-new use cases on top of the in-flight set (see `bundling-logic.md` — Step 1).

If no acceleration plays exist, document the absence. Don't manufacture them. If the client also has no internal AI backlog to share, the in-flight section is omitted with a small disclosure (per `structural-rules.md` — In-flight section).

#### Output 2 — Public-language hygiene lists

Produce two lists for the bundler and writer to enforce hygiene downstream:

**Use these names** (in primary disclosures):
- Partners — vendors, agencies, consultants the client has publicly disclosed
- Products — branded products, services, programs in 10-K / press releases
- Programs — named initiatives (e.g., a published transformation program, a published sustainability program, a named loyalty program)
- Leaders — executives named in earnings calls or investor materials
- Technologies — public tech stack mentions (e.g., "Microsoft Azure", "Snowflake", "Salesforce")

**Avoid these names** (internal-but-not-public):
- Internal codenames the client doesn't use externally (e.g., a project codename only seen in employee documentation, an internal system name absent from filings)
- Trade-press shorthand the client doesn't actually use about itself
- Names from training-data recall that don't appear in current primary sources

The "Avoid" list prevents the dashboard from referencing systems by names the company doesn't publicly use. **This list often catches the most credibility-damaging mistakes** — generic platform language (e.g., "core operating platform migration," "customer data platform consolidation") is far stronger than naming an internal codename the client never publicly uses.

#### Output 3 — Freshness check

Every quantitative number cited from primary sources should be from filings published within the last 12 months. For each material number (revenue, member count, headcount, capex, market share, etc.):

```
metric: [e.g., "loyalty member count"]
value: [N]M
source: [filing or release]
publication_date: [YYYY-MM-DD]
freshness_flag: GREEN (≤6 mo) / AMBER (6-12 mo) / RED (>12 mo)
```

Numbers flagged AMBER or RED must either be refreshed (find a more recent disclosure) or explicitly noted as "as of [date]" in the dashboard. This catches stale figures (e.g., outdated member counts, prior-period revenue) before they land in the headline.

---

### Step 5 — Synthesize into a Research Brief

Before proceeding to bundling or financial sizing, produce a **Research Brief**. This is an internal working document — not rendered directly in HTML — but it becomes the source-of-truth for the Assumptions and Sources tabs.

**Research Brief format:**

| Field | Content |
|---|---|
| Company / Sector | Name, ticker (if public), or "Generic [sector]" |
| Comp companies | Names + tickers if used; rationale for selection |
| Revenue | Most recent annual + YoY growth |
| Gross Margin | If available |
| OpEx relevant to topic | Which lines, amounts, as of which filing |
| AI/Digital signals | Direct signals from earnings calls, 10-K MD&A, press releases — with source and date |
| Stated strategic priorities | Management's disclosed transformation agenda |
| Key benchmarks found | Benchmark name, value, source, date |
| Research gaps | What couldn't be found; what was estimated instead |
| Classification implications | Which financial parameters are CLIENT_DATA vs. BENCHMARK vs. INFERRED as a result |

Share the Research Brief with the user for review before building the HTML if time permits. If the build is time-pressured, embed the brief directly into the Assumptions and Sources tabs without a separate review step — but note the tradeoff.

---

## Classification upgrade from research

The existing classification system (`classification-rules.md`) uses CLIENT_DATA / BENCHMARK / INFERRED. Primary source research adds precision within CLIENT_DATA:

**CLIENT_DATA** — unchanged definition, but now explicitly includes:
- Numbers extracted from 10-K, 10-Q, or earnings call (direct pull, public company)
- Numbers derived from public comp filings with comp identified

**BENCHMARK** — unchanged. Anchored to published industry research (consulting, analyst, association).

**INFERRED** — unchanged. Slalom reasoned estimate. The Research Brief's gaps section explains what fell into INFERRED and why.

**In basis strings**, add specificity to CLIENT_DATA citations:
- `(CLIENT_DATA: 10-K FY2024 Item 7, revenue = $4.2B)`
- `(CLIENT_DATA: Q3 2024 earnings call, CEO commentary on 15% SG&A reduction target)`
- `(CLIENT_DATA: COMP:TGT 10-K FY2024, gross margin 28.4% applied as sector proxy)`

**Disclaimer posture:** A PoV with meaningful CLIENT_DATA sourcing (from primary research, not just user-provided client data) may shift from HEAVY toward STANDARD — but only for the specific line items that are CLIENT_DATA-sourced. Overall posture remains HEAVY unless the majority of financial parameters are CLIENT_DATA or BENCHMARK. See `classification-rules.md` for full disclaimer language by mode.

---

## Common failure modes

- **Skipping Step 2 for a named public company.** If the company is publicly traded, their filings are available and there's no excuse to use INFERRED where CLIENT_DATA is achievable.
- **Picking comps by name recognition alone.** The comp must be genuinely comparable — same model, similar size, same industry. A Fortune 500 brand in a vaguely adjacent sector is not a comp.
- **Using earnings call quotes without noting the date.** Management strategy shifts quarter to quarter. A 2022 earnings quote about automation investment doesn't reflect 2025 priorities.
- **Confusing analyst report summaries with benchmarks.** A McKinsey report that quotes "up to 30% cost reduction potential" is a benchmark only if the report's methodology is credible and the figure applies to the PoV topic. A blog post summarizing that report is not a benchmark.
- **Treating the Research Brief as optional.** If it's not produced, the Assumptions and Sources tabs will be thin. The brief is the QA artifact for both tabs.
