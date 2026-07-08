# Sidebar Icon Palette — Function & Strategic Goal filters

Used in Phase 9 (HTML render) when building the collapsible sidebar. Every filter button needs exactly one icon embedded as an inline Lucide SVG path inside `.fb-icon`.

## Format

```html
<span class="fb-icon">
  <svg viewBox="0 0 24 24">PASTE_PATH_DATA_HERE</svg>
</span>
```

CSS on `.fb-icon svg` sets `width:18px; height:18px; stroke:currentColor; fill:none; stroke-width:2; stroke-linecap:round; stroke-linejoin:round`. **Do not add those attributes to the SVG element itself.**

---

## Selection rules

### Step 1 — keyword match
Scan the filter item label (lowercase) against the keyword lists below. Use the **first match** in order. If multiple keywords match, prefer the more specific one (longer keyword string wins).

### Step 2 — fallback
If no keyword matches, use **`layers`** for functions and **`target`** for strategic goals.

### Step 3 — fixed icons (never change)
- **View › Prioritized** → always `star`
- **View › All evaluated** → always `list`
- **Function › All functions** → always `grid`
- **Strategic Goal › All goals** → always `target`
- Section labels (View, Function, Strategic Goal) have no icon — they use `.filter-label` text only

---

## Function keyword → icon map

| Keywords (any match) | Icon name | SVG path data |
|---|---|---|
| supply chain, logistics, distribution, warehouse, inventory, fulfillment | **truck** | `<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>` |
| manufacturing, production, plant, assembly, operations | **factory** | `<path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M17 18h1"/><path d="M12 18h1"/><path d="M7 18h1"/>` |
| field service, maintenance, repair, technician, service | **wrench** | `<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>` |
| quality, compliance, regulatory, audit, inspection, gxp, gmp | **shield-check** | `<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/><path d="m9 12 2 2 4-4"/>` |
| engineering, design, r&d, research, development, innovation, product development | **compass** | `<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>` |
| finance, accounting, treasury, fp&a, financial planning, cfo | **landmark** | `<line x1="3" x2="21" y1="22" y2="22"/><line x1="6" x2="6" y1="18" y2="11"/><line x1="10" x2="10" y1="18" y2="11"/><line x1="14" x2="14" y1="18" y2="11"/><line x1="18" x2="18" y1="18" y2="11"/><polygon points="12 2 20 7 4 7"/>` |
| hr, human resources, people, talent, workforce, employee | **users** | `<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>` |
| sales, commercial, revenue, business development, go-to-market | **briefcase** | `<rect width="20" height="14" x="2" y="7" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>` |
| customer service, customer support, customer success, cx, contact center | **headphones** | `<path d="M3 14h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a9 9 0 0 1 18 0v7a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3"/>` |
| it, technology, digital, software, platform, infrastructure, data | **cpu** | `<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/>` |
| procurement, sourcing, purchasing, vendor, supply | **shopping-cart** | `<circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/>` |
| clinical, medical, pharmacy, drug, patient, therapeutic | **clipboard-check** | `<rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/>` |
| marketing, brand, communications, demand generation | **megaphone** | `<path d="m3 11 19-9-9 19-2-8-8-2z"/>` |
| legal, risk, compliance (if not quality), regulatory affairs | **scale** | `<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>` |
| safety, ehs, environment, health, occupational | **hard-hat** | `<path d="M2 18a1 1 0 0 0 1 1h18a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v2z"/><path d="M10 10V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5"/><path d="M4 15v-3a6 6 0 0 1 6-6h0"/><path d="M14 6h0a6 6 0 0 1 6 6v3"/>` |
| underwriting, actuarial, insurance, risk (insurance context) | **file-text** | `<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>` |
| *(fallback)* | **layers** | `<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>` |

---

## Strategic Goal keyword → icon map

| Keywords (any match) | Icon name | SVG path data |
|---|---|---|
| margin, cost, efficiency, expense, savings, ebitda | **trending-up** | `<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>` |
| revenue, growth, sales, incremental, top-line | **bar-chart-2** | `<line x1="18" x2="18" y1="20" y2="4"/><line x1="12" x2="12" y1="20" y2="14"/><line x1="6" x2="6" y1="20" y2="9"/>` |
| throughput, speed, cycle time, capacity, output, volume, yield | **zap** | `<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>` |
| working capital, cash, inventory turn, days, receivable, payable, liquidity | **landmark** | `<line x1="3" x2="21" y1="22" y2="22"/><line x1="6" x2="6" y1="18" y2="11"/><line x1="10" x2="10" y1="18" y2="11"/><line x1="14" x2="14" y1="18" y2="11"/><line x1="18" x2="18" y1="18" y2="11"/><polygon points="12 2 20 7 4 7"/>` |
| productivity, field, workforce, labor, utilization, headcount | **users** | `<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>` |
| customer, nps, csat, experience, satisfaction, retention, churn | **heart** | `<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>` |
| quality, defect, error, accuracy, compliance rate | **award** | `<circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/>` |
| risk, safety, incident, audit, regulatory | **shield** | `<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/>` |
| innovation, digital, technology, platform, capability, transformation | **lightbulb** | `<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>` |
| sustainability, esg, carbon, emission, environmental | **leaf** | `<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>` |
| time, speed, delivery, lead time, on-time | **clock** | `<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>` |
| *(fallback)* | **target** | `<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>` |

---

## Fixed icons (always use these)

```
star     (View › Prioritized)
<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>

list     (View › All evaluated)
<line x1="8" x2="21" y1="6" y2="6"/><line x1="8" x2="21" y1="12" y2="12"/><line x1="8" x2="21" y1="18" y2="18"/><line x1="3" x2="3.01" y1="6" y2="6"/><line x1="3" x2="3.01" y1="12" y2="12"/><line x1="3" x2="3.01" y1="18" y2="18"/>

grid     (Function › All functions)
<rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/>

target   (Strategic Goal › All goals)
<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>
```

---

## Strategic Goal color swatches

Each strategic goal also gets a swatch `<span class="fb-swatch" style="background:COLOR">`. Assign colors from this palette in order, recycling if more than 5 goals:

```
1. #F5A623  (amber)
2. #FF4D5F  (coral)
3. #0e7a86  (teal-deep)
4. #7B61FF  (purple)
5. #5BA85B  (green)
```

The swatch replaces the SVG icon for individual strategic goal items (not "All goals"). Do NOT show both a swatch and an SVG for the same item.

```html
<!-- Strategic goal with swatch (not "All goals") -->
<span class="fb-icon"><span class="fb-swatch" style="background:#F5A623"></span></span>

<!-- "All goals" uses the target SVG, no swatch -->
<span class="fb-icon"><svg viewBox="0 0 24 24">...target paths...</svg></span>
```
