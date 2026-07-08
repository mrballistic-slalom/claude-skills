# Golden Master

The single visual reference every canonical build is compared against. Without this, "aesthetic consistency" is enforced only descriptively (via `design.md`), and small drifts accumulate across engagements.

---

## Working canon — canonical reference build

**Source:** `references/build-skeleton.html`
**Built:** 2026-05-27
**Skill version when built:** v2.5

Pinned as the working golden master based on three criteria:
1. **Recency** — most recent canonical-targeted build as of v2.5
2. **Feature coverage** — has the latest interactive patterns (filters, lens selector, sortable table)
3. **Palette fidelity** — all canonical CSS variables present and matching `design.md` exactly

---

## What the canonical build gets right (compare every new build against these)

### Palette — all 26 canonical CSS variables defined

```
--slalom-blue: #0C62FB   (primary accent — eyebrows, links, citations)
--dark-blue:   #002FAF   (hero gradient start)
--coral:       #FF4D5F   (Phase 3 / revenue-uplift accent)
--teal:        #1BE1F2   (Phase 1 / quick-win accent)
--teal-deep:   #0e7a86   (cost-avoidance accent, teal text on white)
--purple:      #7B61FF   (Phase 2 / foundational accent)
--amber:       #F5A623   (anchor A1 / warning accent)
--amber-bg:    #FFF3CD   (disclaimer band background)
--ink:         #0e1422   (primary type)
--ink-2:       #3b4458   (secondary type)
--muted:       #6b7588   (tertiary / phase badges)
--bg:          #F6F8FB   (page background)
--card:        #FFFFFF   (card background)
--surface-2:   #f6f7f9   (alternate surface)
--line:        #E3E7EE   (borders / dividers)
--rule:        #e3e6ec   (rule lines)
--pos:         #1f7a1f   (positive / success indicator)
--hero-end:    #0a3a8a   (hero gradient end)
--ph1:         #0C62FB   (phase 1 chart color)
--ph2:         #0e7a86   (phase 2 chart color)
--ph3:         #7B61FF   (phase 3 chart color)
--a1:          #F5A623   (anchor A1 color)
--a2:          #FF4D5F   (anchor A2 color)
--a3:          #0e7a86   (anchor A3 color)
--a4:          #7B61FF   (anchor A4 color)
--a5:          #5BA85B   (anchor A5 color)
```

Use these as the comparison source. Any new build with off-palette hex codes inline (rather than `var()` references) is drifting.

### Tab labels (sentence case, exact strings)

> Summary · Why Now · AI Portfolio · AVP Analysis · Roadmap · Assumptions · Sources

(AVP Analysis is optional — present only when heatmap images were provided at intake. Risks tab was added in v2.4 and subsequently dropped from canonical in v2.5; do not add it.)

### Component patterns

- ≤2 base card patterns (standard + compact)
- 4px accent borders (never 3px or 5px)
- 8px border-radius (consistent across cards)
- 480px height for portfolio matrices, 360px for other charts
- Nav bar: `#0C62FB` (Slalom Blue), white inline-SVG Slalom logo

---

## Known deviations in the canonical build (do NOT replicate)

The canonical build is the working reference, not a perfect render. These deviations should NOT be reproduced in future builds:

| Deviation | What the canonical build uses | Canonical (per `structural-rules.md`) |
|---|---|---|
| Competitor mentions in body | Legacy joint-research citation and HEAVY mode disclaimer label | Per v2.5 `client-language.md`: zero competitor mentions, no HEAVY mode label |

**Resolved in v2.5 patch (2026-05-27):** The following were previously deviations and have been fixed in `build-skeleton.html`:
- Tab ID for AI Portfolio was `tab-portfolio` → now `tab-aiportfolio`
- Tab ID for AVP Analysis was `tab-avp` → now `tab-avpanalysis`
- Skill attribution footer was absent → now present on all 7 canonical tab panels
- Hero gradient used `#0a3a8a` hardcoded → now `var(--hero-end)` (variable added to `:root`)
- Phase badge used `#888` hardcoded → now `var(--muted)`
- Disclaimer text used `#5a4000` hardcoded → now `var(--ink)`

The deviation list will be retired once a purpose-built canonical render with zero known deviations exists (planned for a future skill release).

---

## How to use the golden master

### During a build

After the first complete render at Phase 9 (per SKILL.md Cost Mode), open both files side by side:
1. New build → its rendered HTML at the engagement output path
2. Golden master → `references/build-skeleton.html`

Walk through the **design-lock checklist** below and flag any deviation. Deviations are allowed only when:
- The active engagement uses a named design variant (see `design-variants/` overlays)
- The user explicitly requests a deviation
- The deviation aligns the new build to canonical (i.e., fixing a known legacy deviation in a new build is correct)

### Design-lock checklist (visual diff)

- [ ] CSS variables: every variable from the 26-variable canonical palette is defined and used via `var()` — no inline hex outside the variable system
- [ ] Tab labels: exact strings, sentence case, in canonical 7-tab order
- [ ] Tab IDs: canonical IDs (`tab-aiportfolio`, `tab-avpanalysis`) — NOT the legacy shortcut IDs
- [ ] Nav bar: `#0C62FB` background, inline-SVG Slalom logo, white tab text
- [ ] Hero gradient: `#002FAF → #0a3a8a` only — no other gradient on the page
- [ ] Card system: ≤2 patterns (standard 16px padding / compact 14px padding), 8px radius, 4px accent borders
- [ ] Type scale: ≤9 sizes total (`10/11/12/13/14/18/22/28` + ≤3 hero display)
- [ ] Spacing: 4-base scale only — no 5/6/10/14/18/22/30 in section spacing
- [ ] Chart heights: 480px for portfolio matrices, 360px otherwise
- [ ] Disclaimer band: amber-bg + amber accent border on every tab

### After the design-lock check

If a deviation is found, decide:
1. **Drift** — fix the new build to match canonical, document in the decisions log
2. **Intentional variant** — confirm the variant is in `design-variants/`, document overlay applied
3. **Bug in canonical build** — fix the new build to canonical, do NOT propagate the known deviation; note as a pinned-but-imperfect-master observation here

---

## When to repin the golden master

Repin when:
- A purpose-built canonical render is created using clean tab IDs + the 7-tab canonical structure + a representative sample portfolio (planned)
- A future build supersedes the current reference on all three criteria (recency, feature coverage, palette fidelity) AND has zero known deviations

Until then, `build-skeleton.html` is the working canon. Future repins should be reflected in this file and announced in the SKILL.md version history.

---

## Files NOT to use as golden master

| File | Why not |
|---|---|
| Multifile variant build | Multi-file CSS + Google Fonts design system; not self-contained — see `design-variants/multifile.md` |
| Extended-palette variant build | Extended palette with greens/dark-navy; non-canonical tabs (Strategy, MonteCarlo) — see `design-variants/extended.md` |
| Older tab-proposal build | Uses `tab-proposal` (non-canonical); pre-current-tab-ID standard |
| Sector-level concept build | Sector framing (not client-specific); structural pattern differs from client PoV |
