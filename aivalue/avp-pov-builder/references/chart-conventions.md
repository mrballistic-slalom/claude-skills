# Chart Conventions

Universal rules for every chart, axis label, and visual reference to a numeric value across the dashboard. **These are agnostic of client and industry.** Per-engagement values (specific break-even months, heatmap stops, dollar anchors) live in `engagement-config.md`.

The rules in this file exist because the absence of them produced real bugs in shipped work — break-even labeled `Year 2.8` in one chart and `month 20` in another, heatmap legend bands that didn't match the source AVP image, matrix axes that hid the win-zone use cases. Treat as load-bearing.

---

## 1. Time framing — pick one convention and stay with it

Every chart that shows time-from-project-start must use the **same convention** end-to-end. Pick one of:

| Convention | What `x = N` means | Used by |
|---|---|---|
| **Elapsed years (1-indexed)** | `x = 1` is end of operating year 1 (= 1 year elapsed); `x = 0` is project start | The cumulative cost-vs-benefit phasing chart |
| **Elapsed months from project start** | `x = N` months from the project start date | The per-UC payback matrix |

**Both conventions agree** on the underlying time but differ in tick units. The hazard is in the *break-even arithmetic* — see — 3.

---

## 2. Roadmap chart — cumulative cost vs cumulative benefit

The phasing-tab cumulative chart uses **elapsed years (1-indexed)**.

- Data array index `i` represents **end of year `i+1`** (i.e., `cum_cost[0]` is cumulative cost through end-of-year-1).
- Plotted as `(x, y) = (i + 1, value)`.
- X-axis: `min: 0`, `max: cum_cost.length` (typically 5).
- X-axis title: `"Years from deployment"`.

The `breakeven` value in `phasing-data` JSON is in **array-index space** (linear interpolation across the index axis where the curves cross). To convert to elapsed years for display, **add 1**:

```
elapsed_years = breakeven + 1
elapsed_months = (breakeven + 1) * 12
```

So a JSON `breakeven: 1.80` displays as `"Year 2.8"` (= 2.8 years elapsed from project start, ≈ 34 months elapsed).

This is the canonical break-even value referenced by the in-page break-even callout (see 4) and the per-UC matrix annotation line (see 5).

**Annotation line on the chart:** vertical at `x = breakeven + 1`, label `"Break-even Year " + (breakeven + 1).toFixed(1)`.

---

## 3. Per-UC matrix (`matrix-npv-payback`) — payback in elapsed months

The AI Portfolio per-UC scatter uses **elapsed months from project start**.

- Each UC's `x_payback` is its own payback in months (already 0-indexed from project start — no shift needed).
- X-axis title: `"Payback (months from project start)"`. *Do not* claim the axis "starts near break-even" unless the math actually matches — see — 5.

### xMin formula — `min(UC payback) − 2` per function

The literal recipe `xMin = portfolio_break_even − 1` **fails** in practice: portfolio break-even (in shifted months ≈ 30–40) is often *above* the median UC payback, so cutting the axis at break-even − 1 hides the win-zone (fast-payback) UCs.

The correct formula is per-function:

```js
xMin[fnId] = max(0, floor(min(uc_payback_for_fn) - 2))
```

This zooms the axis into where UCs cluster while keeping every UC visible (2-month lead-in for breathing room). Compute at runtime from the rebuilt scatter datasets so it tracks the filter:

```js
function _computeMinPaybackByFn() {
  const out = { all: Infinity };
  // ...iterate over scatter datasets, track min x per function key...
  Object.keys(out).forEach(k => {
    out[k] = isFinite(out[k]) ? Math.max(0, Math.floor(out[k] - 2)) : 0;
  });
  return out;
}
```

When the user filters by function, push the new xMin into the chart options and re-render:

```js
chart.options.scales.x.min = newMin;
chart.options.scales.x.beginAtZero = (newMin === 0);
```

`beginAtZero` must flip to `false` whenever `xMin > 0` — Chart.js otherwise overrides the explicit `min`.

---

## 4. Break-even callout (Roadmap tab — adjacent to cumulative chart)

A live, function-aware callout sits between the phasing-tab lead and the chart container:

```html
<div id="break-even-callout" style="...green-tinted callout...">
  <strong>Break-even:</strong>
  <span id="break-even-value">Year 2.8 (month 34) — portfolio</span>
</div>
```

Wired to the function filter via `setFilter()` → `updateBreakEvenCallout(fnId)`. The function reads `phasing-data` JSON, applies the **`+ 1` shift** (per — 2), and renders both the year and month forms together so the framing is unambiguous regardless of which chart the reader is looking at.

```js
window.updateBreakEvenCallout = function(fnId) {
  const rec = phasingData.find(d => d.id === fnId);
  if (!rec || rec.breakeven == null) { el.textContent = '—'; return; }
  const yrs = (rec.breakeven + 1).toFixed(1);
  const months = Math.round((rec.breakeven + 1) * 12);
  el.textContent = `Year ${yrs} (month ${months}) — ${labels[fnId]}`;
};
```

The static fallback text inside the `<span>` is a safety net for the no-JS case; JS replaces it on page load (`updateBreakEvenCallout('all')` in the chart-init block).

**Why this matters:** the break-even number is the single most-quoted figure from the dashboard. If different surfaces report different month values for the same break-even, the dashboard's defensibility erodes immediately.

---

## 5. Break-even annotation on the per-UC matrix

The per-UC matrix carries a vertical annotation line at the **elapsed-month** break-even — same arithmetic as the callout (`(breakeven + 1) * 12`). The line is informative without gating visibility:

```js
function _applyBreakEvenAnnotation(fnId) {
  const beMonths = window._breakEvenMonthsByFn[fnId];  // pre-computed: (breakeven + 1) * 12
  chart.options.plugins.annotation = {
    annotations: {
      breakeven: {
        type: 'line', xMin: beMonths, xMax: beMonths,
        borderColor: '#1f7a1f', borderWidth: 2, borderDash: [6, 4],
        label: {
          display: true,
          content: 'Break-even · month ' + Math.round(beMonths),
          position: 'start',
          backgroundColor: 'rgba(31, 122, 31, 0.92)',
          color: '#fff',
          font: { size: 10 },
          padding: 4,
        }
      }
    }
  };
}
```

Hooked into `updateMatrices(fnId)` so the line moves when the user filters.

**Naming convention:** `'Break-even · month N'` — never `'Year M.M'` on the matrix. The matrix axis is in months; the callout shows both. Keep each surface in its own unit.

---

## 6. Heatmap color bucketing — 10 stops matched to source image

The AVP Task Analysis heatmap uses a **10-band gradient** matched to the AVP scoring image's actual gradient stops. The default convention (validated against AVP's standard heatmap render) is bands at:

```
0 / 40 / 46 / 52 / 58 / 65 / 71 / 77 / 83 / 90 / 100
```

Per-engagement override: **always extract the gradient stops from the supplied AVP heatmap image** and update bands at intake (see `engagement-config.md` — Heatmap stops). Different engagements may use different rendering settings; do not assume the default is correct without checking.

### CSS class names — ten bucket classes

Use this naming, ordered low → high:

| Class | Band | Default color |
|---|---|---|
| `.ta-r1` | 0–39 | `#B23A3A` (deep red) |
| `.ta-r2` | 40–45 | `#D85A5A` (red) |
| `.ta-ro` | 46–51 | `#E07849` (red-orange) |
| `.ta-o`  | 52–57 | `#E89F4F` (orange) |
| `.ta-yo` | 58–64 | `#ECB94A` (yellow-orange) |
| `.ta-y`  | 65–70 | `#F4C430` (yellow) |
| `.ta-yg` | 71–76 | `#C9CC4D` (yellow-green) |
| `.ta-gl` | 77–82 | `#8FBC57` (light green) |
| `.ta-g`  | 83–89 | `#5BA85B` (green) |
| `.ta-gd` | 90–100 | `#3E8E47` (deep green) |

Score chips use `<span class="ta-swatch <bucket>"></span>NN` where bucket is selected by the score:

```js
function bucket(score) {
  if (score < 40)  return 'ta-r1';
  if (score < 46)  return 'ta-r2';
  if (score < 52)  return 'ta-ro';
  if (score < 58)  return 'ta-o';
  if (score < 65)  return 'ta-yo';
  if (score < 71)  return 'ta-y';
  if (score < 77)  return 'ta-yg';
  if (score < 83)  return 'ta-gl';
  if (score < 90)  return 'ta-g';
  return 'ta-gd';
}
```

### Heatmap legend — 10-band gradient bar

The legend renders as a horizontal 10-segment gradient bar with tick labels at 0 / 40 / 52 / 65 / 77 / 90 / 100, plus a one-line interpretation (`<52 = human-in-the-loop required · ≥77 = AI-ready`). This replaces the 4-band legacy legend (red/orange/yellow/green at <40/40-59/60-79/≥80) — that legend produces score chips that don't match the heatmap image.

**Why this matters:** when the legend says a 78 should be yellow but the heatmap image shows that band as green, the dashboard contradicts its own evidence. Readers who notice trust nothing else.

---

## 7. Asterisk on benefit-derived axis labels

Per `editorial-rules.md` — Asterisk system, when a portfolio realization factor is applied, every benefit-derived metric in user-visible body text carries `*`. Chart axis labels follow the same rule:

- Benefit-derived axis (NPV, annual benefit, EBITDA impact, ROI): label includes `*`
- Cost-side axis (LOE, payback, break-even, investment): no asterisk

Example: `"5-yr NPV ($M, P50)*"` vs `"Payback (months from project start)"` — first carries the realization modifier, second is 100% as modeled.

---

## 8. Function-color usage in chart elements

When a chart element (line, bubble, segment) is tied to a specific function pane, source the color from the engagement's function palette (see `engagement-config.md` — Function color palette) rather than hard-coding a hex. Function colors are guaranteed unique by intake validation; chart code references them via `--fn-color` CSS variables on the parent function pane.

**Cost-side benefit category colors** (Cost savings / Cost avoidance / Revenue uplift) must NOT collide with any function color. The default Cost savings color `#0C62FB` (Slalom blue) collides with a default Sales Enablement color of `#0C62FB`. Resolution: see `engagement-config.md` — Function palette.

---

## 9. Tick formatting

| Axis type | Format |
|---|---|
| Dollar values ≥ $1M | `$XM` (one decimal if needed; rarely two) |
| Dollar values < $1M | `$XK` |
| Months | `N` (integer; no `mo` suffix on ticks) |
| Years | `N` (integer) |
| Percentages | `N%` |
| Scores (0–100) | `N` |

Use a callback function on `ticks` to apply consistent formatting; don't rely on Chart.js defaults which add commas in awkward places.

---

## 10. Chart-construction checklist

When building any new chart, walk this checklist:

- [ ] Time framing — elapsed years (chart) or elapsed months (matrix) — declared in axis title
- [ ] If chart references break-even, the `+1` shift is applied where the JSON value enters
- [ ] xMin formula appropriate to the data: `0` for cumulative charts, `min(value) − 2` for clustered scatters
- [ ] `beginAtZero: false` whenever `xMin > 0` (Chart.js gotcha)
- [ ] Annotation line at break-even when relevant; consistent label format
- [ ] Tick formatter set explicitly
- [ ] Asterisk rule applied to axis label per — 7
- [ ] Wrapper `<div>` carries explicit pixel height for Chart.js (per `qa-checklist.md` — 11)
- [ ] Filter sync: when `setFilter(fnId)` is called, the chart's xMin, annotation, and dataset all update

---

## 11. Anti-patterns

| Pattern | Why it fails |
|---|---|
| Reading `breakeven` directly as months without the `+1` shift | Off by 12 months — the most expensive arithmetic bug in the dashboard |
| Setting `xMin = breakeven − 1` on the per-UC matrix | Cuts off win-zone UCs whose paybacks are below the portfolio break-even |
| Forgetting `beginAtZero: false` after setting `min` | Chart.js silently ignores `min` and forces `0` |
| 4-band heatmap legend (<40/40-59/60-79/≥80) | Doesn't match AVP heatmap image gradient — score chips and legend disagree |
| Hard-coded function colors in chart datasets | Drifts from the engagement's palette; collisions sneak back in |
| Two charts referencing the same break-even with different month values | Reader sees `month 22` and `month 34` for the same line; defensibility gone |
