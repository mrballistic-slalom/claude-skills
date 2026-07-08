# Client Language

Single source of truth for what clients see versus what stays internal to Slalom. Hard-coded in the skill so every user gets consistent output regardless of memory state.

The accompanying QA script (`qa-automated-checks.py`) enforces the **hard fails** in this file at the Phase 10 QA gate. Build cannot proceed to delivery while any hard fail is present.

---

## Hardcoded defaults — apply unconditionally unless overridden at intake

| Default | Value | Override condition |
|---|---|---|
| Language | US English | Client HQ is non-US (sets via intake Q8) |
| Emojis as value badges | Forbidden in visible content | Never — use text labels instead |
| "bundle" / "bundles" word | Forbidden in visible content | Never — convention is "Use Case" / "Use Cases" |
| Anchor codes alone (`A1`, `A2`, ...) | Forbidden as standalone chip text or button labels | Never — accompany with full name (e.g., `A1 — Margin recovery` is OK, `A1` alone is not) |
| Raw citation brackets (`[S5]`, `[I3]`) | Forbidden as inline plaintext in body | Always render citations as styled spans (`<span class="s-ref">S5</span>`) |
| Disclaimer label | "Illustrative analysis." | Match `editorial-rules.md` exactly |
| `HEAVY mode` label | Forbidden in body content | Never — it's an internal authoring note (per `editorial-rules.md` line 86) |

---

## Hard fails (block Phase 10 → 11)

The Phase 10 QA script (`qa-automated-checks.py`) blocks delivery when any of these are present in rendered HTML visible body content (with the rendered HTML stripped of `<script>`, `<style>`, `<svg>`, base64-encoded asset data, and HTML tags themselves).

| Hard fail | Threshold | Why |
|---|---|---|
| Competitor names in visible content | Any of `McKinsey`, `BCG`, `Boston Consulting`, `Deloitte`, `Accenture`, `Bain`, `EY`, `Ernst & Young`, `PwC`, `PricewaterhouseCoopers`, `KPMG` (≥1) | Never name Slalom's competitors in client-facing deliverables. Use neutral language ("a third-party assessment", "competing analyses", "industry-leading research"). |
| Value-badge emoji in visible content | Any of `♥ ☮ 🎓 ★ ✓ ✗` (≥1) | These are kindergarten-grade visual elements in a consulting deliverable. Text labels only. |
| `bundle` word in visible content | >10 occurrences | Convention is "Use Case". Occasional metaphorical use OK; systematic use fails. |
| British spelling on US-HQ client | >50 total across `realisation`, `prioritis*`, `organis*`, `behaviou*`, `analyse` | US clients see US English. Sweep at runtime per `runtime-translation-sweep.py`. |
| Raw `[S#]`/`[I#]`/`[B#]` brackets in body text | >30 occurrences | Citations should render as styled spans, not raw plaintext markup. The canonical golden master uses ~16 such styled refs without raw brackets in body — threshold 30 keeps that valid. |
| Matrix SVG `<circle>` elements without `<g data-fn=...>` wrapper | ≥20 circles ungrouped | Without `data-fn`/`data-anchors`/`data-phase` on a wrapping `<g>`, the matrix bubbles do not participate in sidebar filters. |
| JS function called via `onclick` but not defined | Any (`setFilter`, `showTab`, `openModal`, etc.) | Dead interactive UI fails silently in browsers; QA catches it before delivery. |
| Unfilled `{{PLACEHOLDER}}` template markers | Any | Skeleton-clone artifacts that weren't replaced with client data. |
| CSS variables referenced via `var()` but not defined | Any | Silently breaks visual styling — a known failure mode that ships unstyled UC cards. |
| Substantive class names used in HTML but not in `<style>` | >5 (excluding state classes) | Same failure mode — render helpers reference classes the CSS doesn't define. |
| DIV depth trace ends ≠ 0 or goes < -3 mid-document | Any deviation | Structural HTML corruption from over-eager string replacement. |

---

## Warnings (surface but don't block)

| Warning | Threshold | Action |
|---|---|---|
| `bundle` word | 1–10 occurrences | Surface to user; convention is "Use Case" but isolated metaphorical use may be intentional |
| British spelling | 1–50 total | Surface; some may be intentional in quoted material |
| Raw `[S#]` etc. | 6–30 | Surface |
| `HEAVY mode` label | Any | Surface (canonical golden master has this known leak; new builds should fix) |
| Missing canonical tab IDs | Any | Surface (canonical golden master has legacy `tab-portfolio` / `tab-avp` — see `golden-master.md`) |

---

## Translation table — apply at runtime in build script

Every build's `main()` must call `apply_client_language_sweep(html_out, client_hq=...)` before writing the output file. This catches data-file content (derivation chains, classification labels, Monte Carlo trial counts) that flows through render helpers unfiltered.

**British → American (when client_hq == "US"):**

| British | American |
|---|---|
| realisation | realization |
| prioritis | prioritiz |
| organis | organiz |
| behaviou | behavio |
| analyse | analyze |
| categoris | categoriz |
| recognis | recogniz |
| standardis | standardiz |
| maximis | maximiz |
| minimis | minimiz |
| utilis | utiliz |
| optimis | optimiz |

(Case-preserving — `Realis` → `Realiz`, `realis` → `realiz`, etc.)

**Internal → Client-facing:**

| Internal | Client-facing |
|---|---|
| `INFERRED: ` (prefix) | `Estimated: ` |
| `INFERRED` (token) | `estimated` (in body); leave uppercase in audit tables OK |
| `BENCHMARK` | `industry benchmark` |
| `HEAVY mode` | `illustrative analysis` |
| `AVP Enhance` | `task analysis` |
| `AVP (AI Value Platform)` | `structured task analysis` |
| `composite-rank` | `ranked` |
| `Monte Carlo` | `probabilistic sensitivity analysis` (default) — keep `Monte Carlo` only when intake Q4 audience is "technical / quant-comfortable" |
| `P(NPV>0)` | `Probability of positive return` |
| `EBITDA-equivalent` | `operating margin` |
| `derivation chain` (parenthetical) | removed |
| `broad pool` | `candidate pool` |
| `McKinsey-counter` / `Slalom-counter` | `differentiated` |

**`bundle` → `Use Case` substitution rules:**

| Pattern | Replace with |
|---|---|
| `bundle` (alone) | `Use Case` |
| `bundles` (plural) | `Use Cases` |
| `Bundle` (capitalized) | `Use Case` |
| `Bundles` (capitalized plural) | `Use Cases` |
| `bundle` as Python keyword arg (`bundles=...`) | **do not touch** — internal identifier |
| `bundle_meta`, `bundles_v1`, `phase1a_bundles` (Python identifiers) | **do not touch** |

Apply via word-boundary regex (`\b`) on rendered HTML only, NOT on Python source identifiers.

---

## Audience override — intake Q4

If intake Q4 ("target audience") explicitly indicates a sophisticated technical audience (e.g., "CFO + quant team", "data science leadership", "internal AI committee"), the user may opt to retain some technical language by setting:

```
engagement-config.md — 17 (NEW):
  audience_technical_default: true
```

When set, the QA script demotes these specific failures to warnings:
- `Monte Carlo` → still surface but don't block
- `P(NPV>0)` → still surface but don't block
- `[S#]/[I#]/[B#]` raw bracket threshold → raise to >100

This is opt-IN. Default is the client-friendly translation.

---

## Calibration test

The QA script was calibrated against three internal reference builds:

| Reference | Expected | Result |
|---|---|---|
| Canonical golden master | PASS | 0 failures, 2 known-deviation warnings (`HEAVY mode` leak, legacy tab IDs) |
| Reference broken build (emojis, British spellings, untagged matrix bubbles) | FAIL | 4 failures caught |
| Reference corrected build | PASS | 0 failures, 0 warnings |

Test script: `qa-automated-checks.py` includes the `--test` flag to re-run this calibration against a corpus of past builds.

---

## What this prevents (in plain English)

If a future user skips reading the references and lets the build draft from training-data conventions:
- Emoji badges → caught at QA, blocked
- British spellings → caught at QA, blocked
- "bundle" word → caught at QA, blocked
- Unstyled raw `[S5]` text in body → caught at QA, blocked
- Matrix bubbles that don't filter → caught at QA, blocked
- Undefined CSS classes / variables → caught at QA, blocked

If the user has a sophisticated audience and wants to keep `Monte Carlo` and similar technical language, the intake Q4 override path is available.

The skill stops shipping the known failure patterns without depending on user-specific memory.
