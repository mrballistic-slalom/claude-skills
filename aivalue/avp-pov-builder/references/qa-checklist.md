# QA Checklist

Run before delivery. Every PoV passes this sweep in full. If any check fails, fix before delivering — do not deliver and hope.

**Visual spec source of truth:** CSS values referenced in this checklist (colours, font sizes, padding, chart heights) must match `design.md`. If a value here conflicts with `design.md`, the `design.md` value is canonical — update this checklist.

---

## 1. JS syntax (mandatory — zero tolerance)

Extract the inline script block from the HTML, write to `/tmp/pov.js`, run:

```bash
node --check /tmp/pov.js
```

Must exit 0 with no output. A syntax error means the entire dashboard is broken.

**Critical:** Never insert HTML panel content mid-script-block. Template literals inside JS data arrays contain `<div>` strings — naive string search will produce false insertion points. Always confirm panel div positions using Python with character-position arithmetic, not grep.

---

## 2. Div balance (script-stripped HTML only)

Strip **all** `<script>...</script>` blocks (both external and inline) before counting — template literals in JS data arrays contain `<div>` strings that produce false positives.

```python
import re

# Remove all script blocks first
scripts = [(m.start(), m.end()) for m in re.finditer(r'<script[^>]*>.*?</script>', html, re.DOTALL)]
clean = html
for start, end in reversed(scripts):
    clean = clean[:start] + clean[end:]

opens  = len(re.findall(r'<div', clean))
closes = len(re.findall(r'</div>', clean))
assert opens == closes, f"Imbalance: {opens} open / {closes} close"
```

If the original source file had a pre-existing imbalance, note it explicitly — do not count it as a new error, but do not introduce additional imbalance.

---

## 3. Panel placement (prevents blank tabs)

Confirm that every tab panel `<div id="tab-*">` is:
- Positioned **after** the closing `</script>` tag
- Positioned **before** `</body>`
- **NOT inside** any script block

```python
script_close = html.rfind('</script>')
body_close   = html.find('</body>')

# 7-tab canonical default; for 5-tab variant, drop 'whynow' and 'avpanalysis'
# AVP Analysis is always optional; skip if no value-chain images were provided.
panel_ids = ['summary', 'whynow', 'aiportfolio', 'avpanalysis', 'roadmap', 'assumptions', 'sources']

for pid in panel_ids:
    idx = html.find(f'id="tab-{pid}"')
    if idx == -1:
        # Tab may be intentionally absent (5-tab variant or no AVP image).
        continue
    assert idx > script_close, f"tab-{pid} is inside or before script close"
    assert idx < body_close,   f"tab-{pid} is after </body>"
```

A panel inside the script block renders as blank — the browser parses it as JS, not HTML.

Tab IDs are case-folded slugs of the tab name (`tab-summary`, `tab-whynow`, `tab-aiportfolio`, `tab-avpanalysis`, `tab-roadmap`, `tab-assumptions`, `tab-sources`). Legacy IDs (`tab-overview`, `tab-phasing`, `tab-archetypes`, `tab-context`, `tab-portfolio`, `tab-avp`, `tab-risks`) should be migrated/removed.

---

## 4. Structural integrity

- 7-tab default present (`summary`, `whynow`, `aiportfolio`, `avpanalysis`, `phasing`, `assumptions`, `sources`); 5-tab variant drops `whynow` (folded into `aiportfolio`) and `avpanalysis`
- AVP Analysis (`avpanalysis`) tab present only if value-chain images were provided at intake; otherwise absent (no placeholder)
- All nav buttons present and wired to `showTab()`
- Tab button order matches the build's variant: 7-tab → Summary → Why Now → AI Portfolio → AVP Analysis (if present) → Roadmap → Assumptions → Sources; 5-tab → Summary → AI Portfolio → Roadmap → Assumptions → Sources
- Tab button labels match the canonical names: **Summary · Why Now · AI Portfolio · AVP Analysis · Roadmap · Assumptions · Sources** (sentence case in the nav, no numeric prefixes)
- All UCs in the data model are clickable (`openUcModal('ID')` for each)
- All `getElementById()` calls in JS resolve to existing IDs in the HTML
- All `onclick` handlers reference defined functions
- All canvases have a corresponding draw function called from `showTab()`
- No malformed closing tags (`</div\n` — missing `>` before newline)

---

## 5. Disclaimer checks

- **Disclaimer band present on every tab panel** — not just the Summary tab
- Amber background (#FFF3CD), amber left border (#F5A623)
- Includes "illustrative analysis only"
- Includes "do not represent actual cost commitments"
- Includes "validation through discovery required"
- "Note on scope:" is inline — no carriage return or `<br>` between the label and the text that follows
- "Currency note:" is inline — same rule
- Language matches classification mix per `classification-rules.md`

---

## 6. Hero composition

- **Title** present with one of three forms: aspirational tagline, growth narrative, or financial framing — chosen by the user from skill-generated options
- **Tagline** below title, single sentence, scope-framing
- **Big-one metric** present, sized larger than the supporting strip (88–100px font), with timing-modifier sub-text
- **Supporting 2×3 KPI strip** below the big-one — top row "What it delivers", bottom row "What it costs"
- **Phase strip** (Phase 0/1/2/3) at the bottom of the hero
- **No diagonal watermark** — the watermark was removed; disclaimer band on every tab carries the illustrative status
- If the user opted for the legacy single-ratio hero, format is "$X.XX : $1" with after-tax label

**Narrative cohesion check:** read title → tagline → big-one in sequence. They must form a coherent claim. See `editorial-rules.md` — Narrative cohesion. If the three pull in different directions (e.g., title implies platform unification, tagline pivots to cost reduction, big-one is incremental revenue), flag and rebuild.

---

## 7. ILLUSTRATIVE suffix on scored sec-eyes

Any `sec-eye` element that makes a scored, quantified, or modelled claim must end with **"— ILLUSTRATIVE"**.

Applies to: Readiness scorecard sec-eye, Vulnerability assessment sec-eye, AVP heatmap sec-eye, exit value thesis sec-eye.

Does not apply to: pure descriptive labels (Industry Context, Assumptions & Sources, etc.).

---

## 8. Nav bar standard

```
background: #0C62FB  (Slalom Blue — NOT #002FAF dark blue)
tab padding: 10px top/bottom, 18px left/right
active underline: #fff (white)
inactive text: rgba(255,255,255,.7)
nav brand padding: 0 20px
logo: inline SVG with fill:#ffffff — NOT a text span
```

---

## 9. Financial reconciliation

- Σ bundle NPVs = portfolio NPV displayed in hero (within $0.5M rounding)
- Σ bundle investments = portfolio investment displayed (within $0.2M)
- Σ phase NPVs = portfolio NPV (every UC in exactly one phase)
- Hero ratio = portfolio NPV / portfolio investment (within $0.05)
- After-tax NPV = pre-tax NPV × (1 − tax_rate) within rounding
- Conservative case footnote matches 50% sensitivity calculation

---

## 10. Classification audit

Count across all UC financial lines:
```
CLIENT_DATA lines / BENCHMARK lines / INFERRED lines
```

Verify:
- Every UC financial line has a classification tag
- Disclaimer language matches the mix (see `classification-rules.md`)
- Every BENCHMARK line has a source citation with year
- Every INFERRED line has a reasoning chain — "industry standard" alone is not acceptable
- Every COMP-tagged line names the comparable company in the basis string

---

## 11. Canvas wrapper check (prevents Chart.js stretching bug)

Every `<canvas>` must sit inside a parent `<div>` with an explicit pixel height in its inline style. `<canvas height="...">` alone is not sufficient — Chart.js with `responsive:true` + `maintainAspectRatio:false` overrides it.

```python
import re
canvases = re.findall(r'<canvas[^>]*id="(\w+)"', html)
for cid in canvases:
    pat = re.compile(rf'<div[^>]*height:\s*\d+(?:px|vh)[^>]*>\s*<canvas[^>]*id="{cid}"', re.DOTALL)
    if not pat.search(html):
        pat2 = re.compile(rf'<div[^>]*aspect-ratio[^>]*>\s*<canvas[^>]*id="{cid}"', re.DOTALL)
        if not pat2.search(html):
            raise AssertionError(f'#{cid} missing explicit-height wrapper')
```

---

## 12. Stale content scan

Search for and remove any of the following if present:

| Pattern | Action |
|---|---|
| "Here is what the portfolio looks like." | Remove |
| "AVP Enhance (EnhanceIQ)" | Replace with "AVP (AI Value Platform)" |
| Months 0–6 / 0–12 months / 12–24 months / 24–36 months in phase headers | Remove |
| Phase 0/1/2/3 numeric labels in EI grid column headers | Remove |
| Engagement Intensity by Phase grid (unless explicitly requested) | Remove |
| Specific durations: "8 weeks", "8-week discovery" | Replace with open language |
| Foundation dollar figures (any concrete dollar on foundation cost) | Replace with TBC |
| Prior-client-isms — any named system, brand, leader, or initiative belonging to a client other than the current engagement target (often bled in from training-data recall or prior Slalom engagements) | Strip |
| Client-specific stats from prior pursuits bleeding into a generic PoV | Strip |

---

## 12b. Banned vocabulary scan

Strip script blocks and base64 image data; scan body text for the banned-words list in `editorial-rules.md` — Banned vocabulary. Zero tolerance.

```python
banned = [
    'plays', 'AI plays', 'play (when meaning AI-play)',
    'moat', 'moats',
    'named publicly', 'publicly named', 'has named publicly',
    'Slalom-additive', 'additive PoV', 'additive proposal',
    'C-suite (in body)',
    'Plan→Scale', 'Execute Initial', 'Execute Deepen',
]
```

Use word boundaries; allow `display(s)`, `acceleration_play` as a data-model field name (but not as a user-visible label). Allow `executive` and `executives` (the substitute). The check fails on ANY hit in user-visible body text.

---

## 13. Print / PDF panel containment

**Symptom:** the same section appears in every tab's PDF export, despite being intended for one tab. Cause: a section sits between panel `<div>`s rather than inside one, so `display:none` doesn't cascade.

**Check:** for each section element on a tab, confirm it's nested INSIDE its panel `<div>` (depth ≥ 1 from the panel root). Walk the script-stripped HTML:

```python
import re
clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
for pid in ['summary','whynow','aiportfolio','avpanalysis','roadmap','assumptions','sources']:  # adjust to actual tab IDs (drop whynow/avpanalysis for 5-tab variant or no AVP image)
    panel_start = clean.find(f'<div class="panel" id="tab-{pid}"')
    if panel_start == -1:
        panel_start = clean.find(f'<div class="panel active" id="tab-{pid}"')
    next_panel = clean.find('<div class="panel', panel_start + 5)
    if next_panel == -1:
        next_panel = clean.find('</body>', panel_start)
    chunk = clean[panel_start:next_panel]
    # Every section in this chunk should appear inside the panel — depth check:
    depth = 0
    section_starts = []
    for m in re.finditer(r'<div\b|</div>|<section\b', chunk):
        if m.group(0) == '<div':
            depth += 1
        elif m.group(0) == '</div>':
            depth -= 1
        elif m.group(0).startswith('<section'):
            section_starts.append((m.start(), depth))
    for pos, d in section_starts:
        assert d >= 1, f"Section in tab-{pid} at depth {d} — should be inside panel"
```

Optionally add `@media print { .panel:not(.active) { display:none !important } }` as belt-and-braces, but the structural check is the real fix.

---

## 14. Monte Carlo presence and consistency

If the engagement is HEAVY-disclaimer (default):

- MC results stored in the data model (P10 / P50 / P90 / mean for annual benefit, NPV, payback per UC and portfolio)
- Per-UC modal renders the three range bars + P(NPV>0) badge
- Assumptions tab carries the portfolio-level confidence section with the four key probability metrics
- "Sensitivity, not precision" caveat present on both per-UC modal and portfolio confidence section
- Probability of clearing the client's stated target (if any) surfaced visibly

If STANDARD or TIGHT disclaimer mode, three-scenario sensitivity remains acceptable.

---

## 15. Benefit classification consistency

For each UC:
- `benefit_type_class` field present and one of: Hard cost reduction / Productivity savings / Cost avoidance / Revenue assurance / Incremental revenue
- `benefit_type_desc` field present (1-line description)
- Modal renders the classification pill under the title
- Portfolio total reconciles to the 5-class sum *and* the 3-bucket roll-up
- Value section on executive tab anchors total + 3 buckets + 5-detail in disclosure (not all 5 inline)

---

## 16. Anchor specificity audit

For each anchor, the target line and the body paragraph must include at least one named specific (docket, named target, dated event, named asset, named legislation). The "specificity test" from `anchor-specificity.md`:

- Replace the client's name with "Acme Corp" mentally
- If the section still makes sense, the anchors are too generic — flag and rewrite
- If it stops making sense, the anchors are specific enough

Spot-check 2 anchors per audit. Flag failures.

---

## 17. AVP trace check

Pick 2–3 bundles at random. For each:
- Bundle has a recorded `parent_tasks` list and `constituent_features` list
- Each `wbs_identifier` in `parent_tasks` exists in the Task Generation / Task Analysis source
- Each constituent feature exists in Use Case Generation source
- Bundle narrative is recognizably a roll-up of constituent feature descriptions

If the trace fails, the bundle violates the AVP-rooted contract. Revisit.

---

## 18. Citation integrity

- All `[N]` superscript references in body have a corresponding source in Assumptions & Sources
- All sources in Assumptions & Sources are referenced at least once in body
- All citation links use `target="_blank" rel="noopener"`
- Slalom 2024 Executive Perspectives + leading consulting research both cited (no competitor names)

---

## 19. Brand compliance

- Slalom Blue (#0C62FB) + Dark Blue (#002FAF) + Coral Red (#FF4D5F) primary
- Warning amber (#F5A623, #FFF3CD) ONLY in disclaimer block
- **Logo: inline SVG from `assets/slalom-logo-white-RGB.svg`** — not a text span, not base64, not external URL
- Read `/mnt/skills/user/slalom-brand-guide/SKILL.md` if any uncertainty

---

## 20. KPI strip ordering (top row "What it delivers", bottom row "What it costs")

The hero KPI strip and any equivalent dashboard-level KPI block must put **value first, cost second** — the audience reads "what we get" before "what we spend." Check:

- Top row labeled "What it delivers" with primary value metric, secondary financial metric, scope
- Bottom row labeled "What it costs" with total investment, annual run cost, payback
- Both row labels visible (not just card content)

If the order is reversed (costs on top), fix before delivery.

---

## 21. Timing modifier on every monetary metric

Every monetary value displayed in the dashboard must be unambiguous about whether it is one-time, recurring annual, cumulative, or a duration. Audit:

- Hero KPI strip — every $ value carries explicit timing in the value itself ($XM/yr) or sub-text ("one-time, phased")
- Per-UC modal KPI strip — same rule
- Phase cards — same rule
- Three-callout strip on cost-vs-benefit chart (Roadmap tab) — Year 0 ask (one-time), breakeven (months), Net by Year N (cumulative)
- Bundle table — annual values labeled /yr, cumulative NPV labeled

A monetary value with no timing modifier is a QA fail. CFOs should never have to infer.

---

## 22. Strategic-fit tier vocabulary

Every use case carries one of: HIGHEST / HIGH / MEDIUM-HIGH / MEDIUM. No alternative tier names invented.

- Tier appears as a header pill in the modal (section 1)
- Tier appears as a sortable column in the portfolio table
- HIGHEST tier is reserved for direct CEO-quote-level alignment to the company's most-named priority — should be a small fraction of the portfolio (typically 20–35%), not the majority

---

## 23. Citation ID system ([S#] / [B#] / [I#]) — with tab routing

Every quantitative claim in the body has a citation reference using one of three prefixes, and each prefix routes to its assigned tab on click:

- `[S#]` for primary sources → routes to **Sources tab**
- `[B#]` for benchmarks → routes to **Sources tab**
- `[I#]` for inferred assumptions → routes to **Assumptions tab**

Audit:

- Numbering is sequential within each prefix
- Every `[S#]` and `[B#]` reference in the body has a corresponding row in the **Sources tab** with `id="ref-S#"` / `id="ref-B#"`
- Every `[I#]` reference in the body has a corresponding row in the **Assumptions tab** with `id="ref-I#"`
- Clicking `[S#]` or `[B#]` jumps to the Sources tab AND scrolls to the row, with brief CSS-animation highlight
- Clicking `[I#]` jumps to the Assumptions tab AND scrolls to the row
- No orphan citations (in body but not in destination tab) and no orphan sources (in tab but never referenced)
- Routing must match: an `[I#]` row mistakenly placed in the Sources tab is a fail; an `[S#]` or `[B#]` row in the Assumptions tab is a fail

---

## 24. In-flight acknowledgment surfaced where applicable

If the Phase 2 research found acceleration plays (publicly disclosed AI capabilities the client has deployed or is deploying), AND/OR the client shared an internal AI backlog at intake:

- The Why Now tab "What [client] has in flight" section renders at the top of the tab (per `structural-rules.md` — In-flight section)
- Each in-flight initiative is a card (NOT a modal-clickable bundle) with status pill, name, named partners, scope, anchor mapping, sized annual value, citation chip(s)
- Sub-total card at end of grid showing aggregate sized value
- The Slalom proposal portfolio (AI Portfolio tab matrices, table, modals) excludes everything in the in-flight set
- Optional in-flight strip above the matrix block is muted in styling
- Sources tab methodology mentions the in-flight inputs sourced (research / backlog / both)

If neither inputs source yielded anything, the in-flight section is **absent entirely** and the Sources tab methodology carries the disclosure: *"Client AI work in flight: not surfaced in this PoV; to be discovered during validation."*

Verify no Slalom-proposed bundle is framed as a "scale-out play" of an existing client capability — that's the conflation anti-pattern from `bundling-logic.md` — Anti-patterns.

---

## 25. Public-language hygiene

Run two scans against the dashboard body (not the methodology gap callout, which intentionally references the absence):

**Use list confirmation:** every named partner / product / program / leader cited in the body appears on the Phase 2 "Use these names" list.

**Avoid list violation scan:** no internal-but-not-public terminology from the "Avoid these names" list appears in the body. Common offenders:
- Internal codenames the company doesn't use externally
- Trade-press shorthand that's not in primary sources
- Names from training-data recall not in current filings

If any "Avoid" item appears, replace with generic platform language and re-render.

---

## 26. Phase plan default — Phase 0 / 1 / 2 / 3

Default phasing is four phases. Verify on the Roadmap tab:

- Four phase cards present (Phase 0 / Phase 1 / Phase 2 / Phase 3) — not three
- Phase 0 carries TBC dollar figures, never a concrete number
- Phase 1 use cases deploy Year 0 with 5-year ramp
- Phase 2 use cases deploy Year 1 with 4-year ramp
- Phase 3 use cases deploy Year 2 with 3-year ramp
- Cost-vs-benefit chart reflects all three deploying phases

If user explicitly requested three phases (Phase 0 + 1 + 2 only), document the exception and confirm Phase 2 absorbs what would otherwise be Phase 3 work. Default is four.

### Tab count rule

7-tab default (Summary · Why Now · AI Portfolio · AVP Analysis · Phasing · Assumptions · Sources) is canonical; 5-tab variant (Summary · AI Portfolio with Why Now folded in · Phasing · Assumptions · Sources) is acceptable when restraint matters most. AVP Analysis is optional regardless of variant. Assumptions and Sources tabs are never dropped.

---

## 27. Summary tab is single-screen executive summary only

The Summary tab carries hero only — no other content. Verify:

- Disclaimer band ✓
- Hero with title + tagline + big-one + 2×3 supporting KPIs + Phase 0/1/2/3 strip + 1-line context bridge ✓
- **Nothing else.** No bridge waterfall, no Why Now content, no Strategic alignment, no AI Success Patterns, no full phase deep-dive on this tab.

Those sections all live on the Why Now tab (in the 7-tab default) or fold into AI Portfolio (in the 5-tab variant). If any of them appear on the Summary tab, move them.

A Summary tab that requires scrolling past the hero violates the "tell the story with less, not more content" principle.

---

## 28. AVP Analysis tab — image(s) embedded if provided

If the user provided value-chain image(s) at intake:

- AVP Analysis tab is present in the nav (label: "AVP Analysis"; tab ID `tab-avpanalysis`)
- Section eyebrow inside the tab is "AVP TASK ANALYSIS · AI readiness across the value chain"
- Image(s) base64-embedded inline (no external URL, no local file path)
- Tab content: section eyebrow + heading + 1-paragraph framing + image card(s) + reading-the-coloring legend + 1-paragraph implication
- Image(s) display at full container width with preserved aspect ratio

**If multi-image mode used:**
- Verify image count = function count (per intake confirmation)
- Each image inside its own function section, in function-number order
- `loading="lazy"` attribute present on each `<img>` tag

If no image was provided, the AVP Analysis tab is **absent entirely** — no placeholder, no empty tab. Verify both states behave correctly.

---

## 29. Hero options were presented to the user

The hero (title, tagline, big-one) is not auto-generated — the skill presents 3–5 options per element with rationale and waits for user selection. Verify:

- The build log or chat transcript shows the skill presented title options with recommendation
- The build log shows the skill presented tagline options under the chosen title
- The build log shows the skill presented big-one + supporting metric options based on audience

If the skill auto-selected without user confirmation, that's a process failure. The output may still be acceptable, but flag the deviation.

---

## 30. The Big-One metric — sized, positioned, truthful

- Big-one present in the hero, above the 2×3 supporting strip
- Visually larger than the supporting KPIs (88–100px font vs. ~28px)
- Sub-text below the big-one carries timing modifier + qualifier (e.g., "5-year cumulative, after-tax · @ 12% hurdle")
- The big-one number is defensible against the financial model (run reconciliation against Σ UC NPVs, Σ UC annual benefits, etc. depending on which metric was chosen)
- The big-one does not overclaim (no rounding up >5%, no combining across timing without label, no pre-tax dressed as after-tax)

---

## 31. Freshness check — primary-source numbers

Every quantitative number cited from primary sources has a publication date attached in the Sources tab. Audit:

- Material numbers (revenue, member count, headcount, capex, market share) cited within 12 months of build date are GREEN
- Numbers between 6–12 months old are AMBER and should carry an "as of [date]" note in the body
- Numbers >12 months old are RED — refresh or note explicitly as historical context, not current state

A stale figure without explicit dating is a QA fail.

---

## 32. Cuts panel present when cut count > 0

If `bundles_considered_but_cut > 0`, verify the AI Portfolio tab cuts panel renders with the cut count, all rows present, and the why-cut column populated for each row.

If cuts panel renders without why-cut text, fail.

---

## 33. Asterisk system consistency (when realization factor applied)

If `meta.portfolio_realization_factor < 1.0`:

- Every benefit-derived metric in body has an asterisk
- No cost-side metric carries an asterisk
- One asterisk-definition line per tab, no more, no less
- Asterisk-definition language matches the locked text in `editorial-rules.md`

If `meta.portfolio_realization_factor == 1.0` (no factor applied), no asterisks expected anywhere.

---

## 34. File size sanity (multi-image builds)

If image count >= 4, expected HTML file size is 20–35MB (PNG embeds). Above 50MB suggests an image wasn't compressed when it should have been. Below 5MB with 4+ images suggests images aren't actually embedded. Either is a flag.

---

## 35. AI Portfolio matrix block (≥1 matrix, ≤5 matrices)

**Hard rule per `structural-rules.md` and `portfolio-matrices.md`.** Verify:

- The AI Portfolio tab renders **at least one matrix** (a Chart.js scatter/bubble canvas with two named axes, not the filterable table or the deprioritized panel). Zero matrices = fail.
- **No more than five matrices** on the tab. Six or more = fail (dilutes the story).
- Each matrix is its own section with a title (≤8 words, sentence case), a subtitle (2–3 takeaways, ≤180 chars), the chart, and a read-out paragraph (≤80 words). A bare canvas without title/subtitle/read-out = fail.
- Each matrix canvas wrapper has explicit pixel height of 480px (per — 11 canvas-wrapper check).
- Every matrix carries the **classification overlay**: bundles with ≥1 INFERRED line render with a striped/dashed bubble border; all-BENCHMARK/CLIENT_DATA bundles render with a solid border. Legend in the chart footer. **No overlay = fail** (credibility landmine).
- Every matrix carries the **deprioritized treatment**: Phase 7 deprioritized bundles render as 50% opacity / neutral grey / dashed border on every matrix. "Considered but cut" candidates from Phase 3 do NOT appear on any matrix.
- **Axes follow natural orientation, win quadrant labeled per matrix.** Don't invert axes to force top-right = win. Short payback / low LOE / fast break-even sit on the LEFT (natural). The win quadrant therefore varies — top-left for "Y up, X less = good" matrices (Annual Benefit × Relative LOE, NPV × Payback, Cost Savings × Break-Even, Benefit × Break-Even, EBITDA × Time-to-Value); top-right for "both more = good" matrices (Strategic Anchor × Annual Benefit, P(NPV>0) × P50 NPV). Each matrix must visibly mark its win quadrant (small ★ glyph or accent fill on the win-corner label). Axis inverted under the hood = fail. Win-quadrant label missing = fail.
- Matrices show **only Slalom-proposed (net-new) bundles**. In-flight initiatives never appear as live data points.
- The single filter row controls all matrices simultaneously.

If only one matrix renders, verify it's a sensible default (Annual Benefit × Relative LOE, or Annual Benefit × Payback). A degenerate single matrix that doesn't tell a story (e.g., Phase × Cumulative Investment without a financial pair) is acceptable only if the audience explicitly required it — flag it.

---

## 36. Per-UC modal Section 7B — LOE rationale block

Per `structural-rules.md` — Per-UC modal. For every Slalom-proposed bundle modal, verify Section 7B contains:

- Headline: *"Relative LOE: [N] / 100 ([percentile descriptor])"*
- Component breakdown table with five rows (Implementation cost, Change burden, Tech maturity, Data readiness, Regulatory/org friction), each with Score / Weight / Contribution columns
- Reasoning paragraph (≤120 words) referencing AVP feature evidence and bundle-level scope
- Key assumptions bullet list (≤5 items), `[I#]` tagged where material

If Section 7B is missing or incomplete = fail. The categorical LOE tier (Quick Win / Standard / Major Initiative) in the header pill (Section 1) must remain — the percentile in 7B is **additional**, not a replacement.

Spot-check 3 modals minimum. If the relative LOE percentile shown in Section 7B doesn't match what's plotted on the matrix axes for that bundle, that's a data-integrity fail.

---

## 37. Benefit-sum reconciliation (per function and portfolio)

For every function pane (`all` + each function in scope), verify the benefit-class breakdown reconciles to the displayed run-rate total:

```python
import re
from collections import defaultdict
groups = defaultdict(list)
for m in re.finditer(r'<strong>(Cost savings|Cost avoidance|Revenue uplift)</strong> · \$([\d.]+)M/yr \(([\d.]+)%\)', html):
    back = html[max(0, m.start()-3000):m.start()]
    fnm = re.findall(r'data-fn="([^"]+)"', back)
    fn = fnm[-1] if fnm else 'NONE'
    groups[fn].append((m.group(1), float(m.group(2)), float(m.group(3))))

displayed = {}
for m in re.finditer(r'data-fn="([^"]+)">.*?<div class="hero-bigone-num">([^<]+)</div>', html, re.DOTALL):
    fn, val = m.group(1), m.group(2)
    if fn not in displayed:
        displayed[fn] = val

for fn, items in groups.items():
    parts_total = sum(v for _, v, _ in items)
    pct_total = sum(p for _, _, p in items)
    disp = displayed.get(fn, '?')
    disp_num = float(re.search(r'([\d.]+)', disp).group(1))
    assert abs(parts_total - disp_num) < 0.05, f"{fn}: parts {parts_total} ≠ displayed {disp_num}"
    assert abs(pct_total - 100.0) < 0.5, f"{fn}: percentages sum to {pct_total} (≠100)"

# Function subtotals must sum to portfolio
fn_sum = sum(sum(v for _, v, _ in groups.get(fn, [])) for fn in groups if fn != 'all')
all_sum = sum(v for _, v, _ in groups.get('all', []))
assert abs(fn_sum - all_sum) < 0.05, f"Function subtotals {fn_sum} ≠ portfolio {all_sum}"
```

Three-axis reconciliation: parts → function total → portfolio total. Any miss = fail.

---

## 38. Function color palette uniqueness — and no benefit-class collision

Per `engagement-config.md` — 8, every function pane has a unique color, and no function color collides with a benefit-class color (`Cost savings` / `Cost avoidance` / `Revenue uplift`).

```python
import re
from collections import Counter
fn_colors = {}
for m in re.finditer(r'data-fn="(\w+)"[^>]*onclick="setFilter\([^)]+\)"\s+style="--fn-color:\s*([^;"]+)', html):
    fn_colors[m.group(1)] = m.group(2).strip()

# Uniqueness — all distinct
counter = Counter(fn_colors.values())
dups = [c for c, n in counter.items() if n > 1]
assert not dups, f"Duplicate function colors: {dups}"

# Collision with benefit-class colors (defaults from engagement-config)
benefit_colors = {'#0C62FB', '#0e7a86', '#FF4D5F'}  # cost-savings / cost-avoidance / revenue-uplift
collisions = [(fn, c) for fn, c in fn_colors.items() if c in benefit_colors]
assert not collisions, f"Function color collides with benefit-class color: {collisions}"
```

Default for `se` (Sales Enablement) is `#1F6FBF` — distinct from `#0C62FB` Cost-savings blue and from `#002FAF` HR dark blue. Any new function color must pass both uniqueness and benefit-class checks.

---

## 39. Phase-narrative uniqueness across function panes

Per `editorial-rules.md` — Narrative uniqueness, Phase 1 / 2 / 3 descriptions must be **unique per function** (Phase 0 is intentionally shared).

```python
import re
expected_unique = {'0': 1, '1': 7, '2': 7, '3': 7}
for phase_label, expect in [
    ('Foundation', 0),
    ('Quick wins (Year 0)', 1),
    ('Scale (Year 1)', 2),
    ('Backlog (Year 2+)', 3),
]:
    descs = re.findall(rf'<h3>{re.escape(phase_label)}</h3><p class="muted small">([^<]{{20,300}})</p>', html)
    n_total = len(descs)
    n_unique = len(set(descs))
    expect_count = expected_unique[str(expect)]
    assert n_unique >= expect_count, f"Phase {expect} ({phase_label}): {n_unique}/{n_total} unique — boilerplate"
```

7 cards × 1 unique description = boilerplate. Rewrite per `editorial-rules.md` — Narrative uniqueness.

---

## 40. Internal authoring notes — zero leakage

Internal labels and authoring notes must not appear in the rendered body. A prior build shipped with `Required HEAVY disclaimer posture` in an Assumptions table cell — caught only on a downstream QC pass.

```python
# Strip script + base64 first to avoid false positives
import re
clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
clean = re.sub(r'data:image/[^"]+', '', clean)
clean = re.sub(r'data:application/[^"]+', '', clean)

internal_leaks = [
    'Required HEAVY',
    'disclaimer posture',
    'TBD by Slalom',
    'Internal note:',
    'TODO',
    'FIXME',
    'XXX:',  # XXX as marker, not as base64 noise
    '[redacted',
    'Slalom internal',
    'pre-engagement only',
]
for leak in internal_leaks:
    if leak in clean:
        # surface offending context
        idx = clean.find(leak)
        ctx = clean[max(0, idx-60):idx+len(leak)+60]
        raise AssertionError(f"Internal note leaked: '{leak}' in body. Context: ...{ctx}...")
```

---

## 41. Filesystem path leakage — public copy is path-clean

Filesystem paths from the build pipeline (e.g., `enhance/01-sales-enablement/avp-output.xlsx`) must not appear in the rendered body. Replace with public-friendly text per `engagement-config.md` — 10.

```python
import re
clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
# Strip data: URIs (download links carry filenames intentionally; the path-leak we care about is in body text)
clean = re.sub(r'data:[^"]+', '', clean)
forbidden_path_patterns = [
    r'\benhance/\d+-[a-z\-]+/',
    r'\bavp-output\.xlsx\b',
    r'/Users/[\w\-.]+/',
    r'\bcalculate/[a-z\-]+/',
]
for pat in forbidden_path_patterns:
    for m in re.finditer(pat, clean):
        raise AssertionError(f"Path leaked into body: {m.group(0)}")
```

`download="..."` filename attributes on inline-XLSX `<a>` tags are user-facing and intended — they're not path leaks.

---

## 42. Anchor-tooltip coverage

Every reference to an anchor code in the body (`Anchor: A1`, `Anchor: A2, A3`, etc.) must carry a `title` attribute populated from the engagement's anchor table. See `engagement-config.md` — 5 and `structural-rules.md` — Anchor tooltips.

```python
import re
total = len(re.findall(r'<div class="inflight-anchor"[^>]*>Anchor:\s*A\d', html))
with_title = len(re.findall(r'<div class="inflight-anchor" title="[^"]+">Anchor:\s*A\d', html))
assert total == with_title, f"Anchor tooltip coverage: {with_title}/{total}"
```

Same rule applies anywhere anchor codes appear — UC modal sidebar tags, in-flight cards, AVP feature rows, table cells.

---

## 43. Glossary panel presence and discoverability

Per `structural-rules.md` — Glossary panel, the Summary tab carries a glossary panel as `<details open class="glossary-panel">` with at least the universal acronyms covered.

```python
import re
panel = re.search(r'<details[^>]*class="glossary-panel"[^>]*>(.*?)</details>', html, re.DOTALL)
assert panel, "Glossary panel missing from Summary tab"
# Must be open by default
assert ' open' in panel.group(0) or '<details open' in panel.group(0), "Glossary panel not open by default"
# Cover the universal acronyms
body = panel.group(1)
required_terms = ['NPV', 'IRR', 'WACC', 'AVP', 'L3', 'WBS', 'LOE', 'P50']
missing = [t for t in required_terms if t not in body]
assert not missing, f"Glossary missing universal terms: {missing}"
```

---

## 44. Phase 0 dollar anchoring — no `TBC` in financial cells

Per `engagement-config.md` — 4 and `editorial-rules.md` banned vocabulary, Phase 0 cells must show an order-of-magnitude anchor (e.g., `~$8–12M*`), never `TBC`.

```python
import re
# Strip script + base64 to avoid false positives
clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
clean = re.sub(r'data:[^"]+', '', clean)
# In phase-fig cells (One-time / Run-rate)
phase_tbc = re.findall(r'<strong>TBC</strong>', clean)
assert not phase_tbc, f"Phase 0 (or any phase-fig) still contains TBC literal: {len(phase_tbc)} instances"
# In Phase 0 card titles
title_tbc = re.findall(r'<h3>Foundation \(TBC\)</h3>', clean)
assert not title_tbc, f"Phase 0 card titles still contain '(TBC)': {len(title_tbc)} instances"
```

---

## 45. Heatmap 10-band consistency

Per `chart-conventions.md` — 6, heatmap score chips and the legend use a 10-band scheme matched to the AVP image. Verify:

```python
import re
score_pairs = re.findall(r'class="ta-swatch (ta-[a-z0-9]+)"[^>]*></span>(\d+)', html)
expected_buckets = ['ta-r1', 'ta-r2', 'ta-ro', 'ta-o', 'ta-yo', 'ta-y', 'ta-yg', 'ta-gl', 'ta-g', 'ta-gd']

# Every score lands in a defined bucket from the 10-band scheme
bad = [b for b, _ in score_pairs if b not in expected_buckets]
assert not bad, f"Score chips using non-10-band classes: {set(bad)}"

# Spot-check: 78 should be ta-gl (light green); 65 should be ta-y (yellow); 85 should be ta-g (green)
for score, expected in [('78', 'ta-gl'), ('85', 'ta-g'), ('65', 'ta-y')]:
    actual = {b for b, s in score_pairs if s == score}
    if actual:  # only check if score exists in data
        assert actual == {expected}, f"Score {score}: bucket {actual} ≠ expected {expected}"
```

If the engagement uses a non-default heatmap stop set (per `engagement-config.md` — 6), update the expected-bucket assertion accordingly.

---

## 46. Break-even framing consistency

Per `chart-conventions.md` — 1–5, the phasing chart annotation, the break-even callout, and the matrix annotation line must all reference the **same elapsed-month break-even** (= `(breakeven + 1) × 12`).

```python
import re, json
m = re.search(r'<script id="phasing-data"[^>]*>([\s\S]*?)</script>', html)
data = json.loads(m.group(1))
all_rec = next(d for d in data if d['id'] == 'all')
expected_months = (all_rec['breakeven'] + 1) * 12

# The break-even callout's static fallback must use the same arithmetic
callout = re.search(r'id="break-even-value"[^>]*>([^<]+)</span>', html)
assert callout, "break-even-value span missing"
m2 = re.search(r'month\s+(\d+)', callout.group(1))
assert m2, f"Callout missing 'month N' format: {callout.group(1)!r}"
fallback_months = int(m2.group(1))
assert abs(fallback_months - round(expected_months)) <= 1, \
    f"Callout fallback says month {fallback_months}; expected ~{expected_months:.0f}"
```

If JS-driven dynamic update is wired, the page will replace the fallback on load — but the fallback should be correct on its own in case JS fails.

---

## 47. Regex-replace base64 hygiene

Whenever a build step does a global text replacement, filter regex matches by HTML context to avoid corrupting embedded base64 data. A prior build had 23 raw `TBC` matches but only 20 were real — 3 were inside `data:image/...` payloads. A naive replacement would have corrupted the heatmap PNGs.

When automating substitutions, use this guard:

```python
def is_in_base64(text, pos):
    """Heuristic: a position is inside base64 if the surrounding chars contain no
    HTML tags or whitespace (base64 is dense and continuous)."""
    s = text[max(0, pos-30):pos+30]
    return '<' not in s and '>' not in s and ' ' not in s

# Apply replacement only to non-base64 hits
for m in pattern.finditer(html):
    if is_in_base64(html, m.start()):
        continue
    # ... apply replacement at this position
```

Surface any skipped matches in the QA log so silent skips can't hide.

---

## 48. JSON data block validates

The phasing-data script element (`<script id="phasing-data" type="application/json">`) must parse as valid JSON.

```python
import re, json
m = re.search(r'<script id="phasing-data"[^>]*>([\s\S]*?)</script>', html)
assert m, "phasing-data script element missing"
try:
    data = json.loads(m.group(1))
except json.JSONDecodeError as e:
    raise AssertionError(f"phasing-data JSON invalid: {e}")
assert isinstance(data, list) and data, "phasing-data is not a non-empty list"
required_keys = {'id', 'cum_cost', 'cum_benefit', 'breakeven'}
for rec in data:
    missing = required_keys - set(rec.keys())
    assert not missing, f"phasing-data record missing keys: {missing}"
```

If invalid, the phasing chart silently fails to render. JSON validation catches this before delivery.

---

## QA output format

Present a single summary block after running all checks:

```
═══ QA Summary ═══
✅ JS syntax: clean (node --check exit 0)
✅ Div balance: XXX/XXX (script-stripped HTML)
✅ Panel placement: all N panels after </script>, before </body>
✅ Print containment: all sections nested inside their panel
✅ Structural: N tabs, XX/XX UCs clickable, all chart functions wired
✅ Disclaimer: present on all N tabs, inline notes, amber styling
✅ No diagonal watermark (removed in v2.5 — disclaimer band on every tab carries illustrative status)
✅ ILLUSTRATIVE suffix: on all scored sec-eyes
✅ Nav bar: #0C62FB, brand logo (PNG/SVG embedded as base64 + filter:invert)
✅ Financial reconciliation: $XX.XM = Σ phases = Σ use cases
✅ Cost narrative: phased Y0/Y1 + ongoing + cumulative shown
✅ Cost-vs-benefit chart: present on Roadmap tab with crossover annotation
✅ Classification: X% BENCHMARK / Y% INFERRED → HEAVY disclaimer
✅ Benefit classification: 5 classes assigned per UC; 3-bucket roll-up reconciles
✅ Monte Carlo: P10/P50/P90 in modals; portfolio confidence section present
✅ Matrix block: N matrices on AI Portfolio tab (1≤N≤5); classification overlay + deprioritized greyed on each; win quadrant labeled per matrix
✅ LOE rationale (Section 7B): present in all modals; percentile matches matrix axis placement
✅ Anchor specificity: spot-checked anchors carry named docket / target / event
✅ Canvas wrappers: all N canvases have explicit-height parent divs
✅ Stale content: clean
✅ Editorial: ≤9 type sizes, ≤2 card patterns, sentence case, no dup eyebrows
✅ AVP trace: 3/3 spot-checked bundles trace to source
✅ Citations: N/N sources referenced in body
✅ Brand: Slalom palette only, brand logo confirmed
✅ Benefit reconciliation: parts → function totals → portfolio total all balance
✅ Function color palette: all distinct, no benefit-class collision
✅ Phase narratives: 7 unique × 3 phases (no boilerplate)
✅ Internal note leakage: clean
✅ Filesystem path leakage: clean (download attrs preserved)
✅ Anchor tooltips: N/N references covered
✅ Glossary panel: present, open by default, universal terms covered
✅ Phase 0 anchored: ~$X–YM* shown; no TBC literals
✅ Heatmap 10-band: score chips and legend agree
✅ Break-even framing: callout, chart annotation, matrix line all use elapsed-month convention
✅ phasing-data JSON: validates

Ready for delivery.
```

If any check fails, surface it explicitly and fix before delivering.

---

## 49. Accessibility (WCAG 2.1 AA) — per `design.md` — 27

### Semantic structure
- [ ] Tab bar uses `role="tablist"` / `role="tab"` / `role="tabpanel"` pattern with `aria-selected` and `aria-controls`
- [ ] No `<div onclick>` or `<span onclick>` — all interactive elements are `<button>` or `<a>`
- [ ] All data tables use `<thead>`, `<th scope="col">`, and `<th scope="row">`
- [ ] Heading hierarchy does not skip levels (`h1` → `h2` → `h3`)

### Keyboard & focus
- [ ] Skip link present (`<a href="#main-content" class="skip-link">`) and visible on focus
- [ ] Tab buttons activatable with Enter/Space
- [ ] Modals use `role="dialog"` + `aria-modal="true"` + focus trap (Tab wraps inside modal; Escape closes)
- [ ] On modal close, focus returns to the trigger element

### Charts & images
- [ ] Every `<canvas>` has `role="img"` + descriptive `aria-label` summarizing the chart takeaway
- [ ] Slalom logo SVG has `role="img"` + `aria-label="Slalom"`
- [ ] AVP Analysis value-chain images have descriptive `alt` text
- [ ] Decorative elements (arrows, accent borders) have `aria-hidden="true"`

### Colour contrast
- [ ] No body text (≤18px regular, ≤14px bold) on a background with contrast ratio below 4.5:1
- [ ] No large text (>18px regular, >14px bold) on a background with contrast ratio below 3:1
- [ ] Specifically: white text on `--slalom-blue` (#0C62FB) used only for ≥14px bold or ≥18px regular
- [ ] Specifically: `--coral` (#FF4D5F) not used as body-text color on white
- [ ] Specifically: `--teal` (#1BE1F2) not used as text color on white (use `--teal-deep` #0e7a86 instead)

### Motion & print
- [ ] `@media (prefers-reduced-motion: reduce)` rule present, zeroing animation/transition durations
- [ ] Print output renders all text in high contrast (no light-grey-on-white disappearing on paper)

---

## 50. Portfolio View Toggle — per `portfolio-view-toggle.md`

Run only when the rendered HTML includes the Prioritized ↔ All Evaluated toggle (i.e., downselect ratio < 1.0).

- [ ] `<body>` opens with both a `view-*` class and a `filter-*` class (e.g., `class="view-prio filter-ALL"`)
- [ ] Default view on load is `view-prio` (not `view-all`)
- [ ] Two view buttons present at the top of the function-filter sidebar, above the function-filter controls
- [ ] `FN_DATA` is emitted as a single inline JS `const` keyed by `{view: {fn: {...}}}` with views `prio` and `all`
- [ ] No inline `style="display:none"` controls deprio-bubble visibility — driven by `body.view-prio .deprio-bubble { display: none }` CSS only
- [ ] Matrix SVG axes (X = relative LOE percentile, Y = annual value) are computed from the **union** of both pools (Y-max and X-range don't shift between views)
- [ ] Deprioritized bubbles carry class `uc-bubble deprio-bubble` and have **no** `onclick` handler
- [ ] `setView(view)` calls `filterFn(CURRENT_FN)` so view + function filter compose cleanly
- [ ] Deprioritized panel wrapper carries class `deprio-panel`; styled `opacity: 0.85` under `body.view-prio`, `2px solid var(--slalom-blue)` under `body.view-all`
- [ ] Sources tab MC paragraph reads *"10,000 trials on all {broad-pool} candidates,"* not *"on the {final} portfolio"*
- [ ] If downselect ratio = 1.0, the toggle is **suppressed entirely** — sidebar opens directly to the function filter
- [ ] Decisions log — 3a captures the toggle state (rendered | suppressed) with the downselect ratio
