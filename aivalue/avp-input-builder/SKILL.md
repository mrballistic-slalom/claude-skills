---
name: avp-input-builder
version: "1.0"
updated: "2026-05-27"
description: "Build the AVP intake side of a client demo for Slalom's AI Value Platform — Demo Brief, client research, Business Function setup, Enhance input generation (process and role-based), and Business Context Questions. Stops at the Enhance hand-off; does not cover Use Case Generation review, Calculate upload, or benefit-formula population."
---

# AVP Input Builder Skill

This skill guides Claude through building the AVP intake artifacts for a client demo — Demo Brief through Business Context Questions, ending at the Enhance hand-off. Use Case Generation review, Calculate upload, and benefit-formula population are out of scope for this skill. Claude should move through phases in order, checking in with the user at key decision points before proceeding.

**Core principle: This is an input-driven workflow.** Claude should prompt the user for the inputs it needs at each phase — client details, audience context, any primary source materials (emails, PPTs, PDFs, call notes, RFPs) — rather than generating everything unprompted. Claude proposes; the user approves or adjusts.

---

## How this pairs with `avp-pov-builder`

This skill is one half of a paired Slalom workflow for AI PoV work on AVP:

- **`avp-input-builder`** *(this skill)* — Builds the inputs AVP needs: Demo Brief, client research, Business Function setup, Enhance Excel, Business Context Questions. Stops at the AVP Enhance hand-off.
- **`avp-pov-builder`** — Takes the resulting AVP Enhance outputs and builds a provocative HTML dashboard making a defensible AI-transformation case for the client.

**The sequence when paired:** `avp-input-builder` → *you run AVP Enhance externally* → AVP Enhance exports → `avp-pov-builder` → HTML dashboard.

**They don't have to run together.** Use this skill standalone when you only need AVP intake artifacts (e.g., a Calculate-led demo where a dashboard isn't part of the ask). Use `avp-pov-builder` standalone when you already have AVP Enhance outputs in hand and just need the dashboard. Most of the time, though, they run as a pair.

**Artifacts that carry forward.** When this skill is followed by `avp-pov-builder`, the Demo Brief, company description, financial parameters (discount/tax/hurdle), audience context, and business-function inventory built here all carry into the dashboard build. Save them somewhere the user can paste in later.

---

## How to use this skill

Most people running this skill are not AVP experts. Claude is the orientation guide as much as the artifact generator — never let the user feel they need to know AVP-internal terminology to make progress.

**What AVP is** — Slalom's AI Value Platform. AVP takes a Business Function description, runs an "Enhance" step that decomposes the function into subfunctions / processes / tasks based on an Excel file you upload, and then offers downstream Use Case Generation and Calculate phases for economic modeling. This skill stops at the Enhance hand-off.

**What this skill does for you** — Claude builds the inputs AVP needs. Specifically: drafts a Demo Brief, researches the client, proposes Business Functions, generates the Enhance Excel file(s), and drafts answers to AVP's Business Context Questions. You take those artifacts into AVP yourself.

**What you do in AVP yourself** — Create each Business Function in AVP (Title, Description, Analysis Type). Upload the Enhance Excel for each function. Paste in the Business Context Questions answers. Claude tells you exactly when and what each time, with a per-phase "In AVP — your turn" callout.

**The flow at a glance** — Demo Brief → company research → propose Business Functions → *you create functions in AVP* → Enhance Excel build → *you upload to AVP* → Business Context Questions draft → *you paste into AVP* → done.

**Working with Claude here** — Claude proposes, you approve or correct. You can interrupt any time ("pause," "redo that," "skip ahead," "I don't know what AVP is asking for"). If anything looks wrong or unfamiliar, say so — Claude will explain or redo.

---

## Overview of Phases

1. **Client Intake & Research** — Capture Demo Brief, declare input mode, build company description, identify business functions
2. **Business Function Setup** — Generate AVP Business Function titles and descriptions for the user to create in AVP
3. **Enhance Input Generation** — Process-based or role-based Excel upload files
4. **Business Context Questions** — AVP project setup fields

---

## Phase 1: Client Intake & Research

### Demo Brief
Before any research, capture the need driving this demo. The brief is the north star — every later phase (function selection, Enhance structure, business context) should answer *"does this serve the brief?"*

- **Purpose** — proactive/unsolicited PoV, response to a known opportunity (RFP / discovery call / kickoff), executive briefing, workshop, conference moment, etc.
- **Audience** — role, seniority, function, decision lens; attendees AND influencers
- **Knowledge depth** — secondary research only / primary inputs available / mixed. Primary inputs may include emails, PowerPoints, PDFs, call notes, RFP responses, kickoff materials, or any other documents from or about the client. Prompt the user to share whatever they have; declare which content is primary vs. inferred from secondary research.
- **Output role** — what the demo should *do*: open a door, validate an approach, align stakeholders, advance a sale

Present the brief back to the user for confirmation before moving on. If the user pushes ahead without a brief, ask once and accept "skip" — but record the gap so later phases know they're operating without one.

### Input Mode
Declare the mode at the start of Phase 1 and carry it through every subsequent step:

- **Named-client mode** (default): The user provides a specific client. Secondary research draws from that company's public materials — LinkedIn, job postings, career pages, proxy-statement org charts, leadership-team pages, 10-K, recent earnings.
- **Industry-archetype mode**: The user provides an industry or archetype (no named client). Secondary research draws from industry norms and 1-2 representative public companies in that industry as proxy. Flag all archetype-derived content as industry-typical, not client-specific, so the user can adjust later if a real client gets attached.

Later phases reference back to this declaration. When guidance says "search LinkedIn" or "use the company's effective tax rate," that's named-client mode — in archetype mode, substitute the equivalent (industry-typical role names; sector-average financials; an industry/archetype profile in place of a single-company description). The naming rules in this skill (no ampersand groupings, use real terminology, flag guesses) apply to **both** modes equally.

### Required Inputs (prompt user for these)
1. **Client name and industry** (named-client mode) **or industry/archetype label** (archetype mode)
2. **Brief description of what the client does** (Claude refines into a company description **under 500 characters — including spaces and punctuation**)
3. **Which business functions are in scope** (3-5 functions) — or ask if Claude should propose them based on research

Audience and additional meeting context are captured in the Demo Brief above; don't re-ask here.

After collecting inputs 1-2 and building the company description, Claude researches and presents **financial parameters** (discount rate, tax rate, hurdle rate) before proposing business functions. This skill doesn't consume these parameters directly — they're captured here as preload inputs for downstream use: the `avp-pov-builder` skill (when building a Slalom PoV on AI Transformation from the resulting Enhance outputs) and AVP's Calculate phase (run outside this skill).

### Company Description
Write a tight company description **under 500 characters (including spaces and punctuation)** focused on:
- Operations, products, services, and markets
- Scale and key metrics where available
- No company history, founding story, or leadership

**Run a character count before presenting.** AVP enforces this limit; descriptions over 500 chars force a mid-demo rewrite. If a draft runs long, cut history/leadership context first, then trim modifiers — preserve operational specifics and scale metrics.

**Bad:** "Founded in 2015, Amazon Air is Amazon's cargo airline..." (history-led)
**Good:** "Amazon Air is the in-house cargo airline of Amazon.com, operating ~95 aircraft across U.S. hubs to move freight between fulfillment centers and last-mile stations. ~110 daily departures partner with ATSG and Atlas Air, supporting Prime two-day and same-day commitments." (286 chars — fits comfortably)

### Financial Parameters
After the company description and before proposing business functions, research and present three financial parameters. These aren't consumed by this skill, but they're used downstream — by the `avp-pov-builder` skill (when building a Slalom PoV on AI Transformation from these Enhance outputs) and as preload values for AVP's Calculate phase (run outside this skill). Ground them in the client's actual financials, not industry defaults.

**Discount Rate**
- For public companies: use WACC sourced from recent filings or financial data providers
- For regulated utilities/infrastructure: also note the authorized overall rate of return from recent rate cases, as this is often more relevant than market WACC
- For PE-backed/private companies: use the fund's target return or comparable public company WACC
- Present as a range with a recommended point estimate

**Tax Rate**
- Use the company's effective tax rate from the most recent earnings release or 10-K, not the statutory federal rate (21%)
- Note if the effective rate is significantly below statutory (common for companies with large tax credit portfolios, e.g., clean energy ITC/PTC) and explain why
- This matters for downstream after-tax benefit calculations

**Hurdle Rate**
- The minimum return a project must clear to get funded
- For regulated utilities: typically at or slightly above authorized ROE, since AI projects compete with rate-base capital investments for internal capital allocation
- For PE-backed companies: typically the fund's target IRR (often 15-25%)
- For public corporates: often WACC + 2-4% risk premium, or a stated internal hurdle from investor presentations
- If not publicly available, estimate based on authorized ROE (regulated), stated capital allocation policy (public), or fund return targets (PE)

**Presentation format:**
Present all three in a tight table with the value, source, and a one-line rationale. Get user confirmation before proceeding to business functions — these numbers feed downstream skills and AVP phases.

### Business Functions
Identify 3-5 business functions for the demo. For each function, **explicitly declare analysis type (process-based or role-based) and write the description in that lens**. AVP requires the analysis-type choice at Business Function creation in Phase 2; deciding it here means the description reflects the chosen lens from the start rather than being a generic paragraph reframed later.

**Analysis-type lens for the description:**
- **Process-based** descriptions emphasize the workflow, planning cycles, operational hand-offs, and process boundaries. Example phrasing: *"This function operates as a continuous planning-to-fulfillment process spanning…"*
- **Role-based** descriptions emphasize the distinct professional roles, task ownership by role, and skill specialization. Example phrasing: *"This function comprises 6 professional roles — analysts, planners, controllers — each owning a distinct slice of the work…"*

For each function, present:
- **Title** (function name, sourced per the Input Mode declared above — client's actual internal terminology in named-client mode, industry-typical terminology in archetype mode. **Do not stitch two functions together with "&"** — e.g., "Sales & Marketing" is two discrete functions unless the client genuinely organizes them as one unit. If real terminology can't be sourced in either mode, make an educated guess grounded in industry and scale, and flag the assumption so the user can correct it.)
- **Analysis type: process-based | role-based** (explicit declaration, never implicit)
- **One-line rationale** for the analysis-type choice (e.g., *"work flows through a continuous planning cycle, not discrete role-owned slices"*)
- **Description** (~100 words, operationally specific, written in the declared analysis-type lens, covering what the function does, how it operates, key activities, and strategic context)

Distinguish front office vs back office functions. Present the list to the user for validation before moving on.

---

## Phase 2: Business Function Setup

**Before generating any Enhance input files**, provide the user with the AVP Business Function setup text for each function. The user needs these to create the Business Function in AVP before uploading the Enhance file.

Analysis type (process-based or role-based) was declared per function in Phase 1 and the description was written in that lens — confirm rather than re-decide. The description text itself must make the analysis-type framing visible (process flow language vs. role variation language); a generic paragraph that could fit either lens is a quality failure.

For each function, present:
- **Title:** The function name exactly as it should appear in AVP
- **Analysis type:** Process-based or Role-based (carried from Phase 1)
- **Description:** ~100 words written in the analysis-type lens — process flow language for process-based, role variation language for role-based. Operationally specific, covering what the function does, how it operates, key activities, and strategic context.

**Analysis type guidance:**
- **Process-based**: Operations, logistics, planning, commercial functions, technology delivery — anywhere the work flows through processes rather than discrete job roles
- **Role-based**: Functions with distinct professional roles where task ownership varies significantly by role (e.g., Finance, HR, Legal, specialized technical functions)

Present all function titles, descriptions, and analysis type recommendations together. Get user confirmation on both the setup text AND the analysis type for each function before they create the functions in AVP. Once confirmed, proceed directly to Enhance file generation in Phase 3 without re-asking analysis type.

### In AVP — your turn
Once the function titles, descriptions, and analysis types above are confirmed:
1. Open AVP and navigate to your project's Business Functions area
2. For each function, create a new Business Function — paste the Title, paste the Description, and set the Analysis Type (Process-based or Role-based as specified)
3. Save each function
4. Tell Claude when all functions are created; Claude then proceeds to Phase 3 (Enhance Excel generation)

If you can't find where to do this in AVP, just say so — Claude will help you orient.

---

## Phase 3: Enhance Input Generation

### Analysis Type
Analysis type was confirmed in Phase 2. Use the confirmed type for each function — do not re-ask. If for any reason it was not confirmed, refer to the guidance in Phase 2 before proceeding.

### Process-Based Structure
Columns required (9 columns, in order):
`wbs_identifier | subfunction | process | process_specifics | business_unit | role | role_specifics | task_title | task_description`

- `wbs_identifier`: **Always populated** as plain text string in `LL.PP.TT` format (e.g., `01.02.03`). Never blank. Never use formulas. Auto-compute from L1/L2/L3 counters by detecting when subfunction or process values change.
- `business_unit`: "[Client] - [Function Name]"
- `role`: Real client job titles sourced from LinkedIn/job postings — never generic titles
- `process_specifics`: 1-2 tight sentences describing what the process does and why it exists
- `task_description`: Single sentence starting with an action verb (not bullets, unless user requests bullets)

**Target volumes:**
- 7-10 L1 subfunctions per business function
- L2 and L3 counts should reflect the actual complexity of each subfunction — do not apply a uniform count across all nodes. Artificial symmetry is a quality failure.

**Validation before building:** Present L1 subfunctions to user for approval first, then run structural self-critique, then generate tasks.

### Role-Based Structure
Columns required: `wbs_identifier` (auto-populated as `LL.RR.TT`), `business_unit`, `role`, `role_specifics`, `subfunction` (blank), col F (blank), col G (blank), `task_title`, `task_description`

**Target volumes:**
- 5-8 roles per business function
- Task counts per role should reflect what that role actually does — do not normalize

### Structural Self-Critique (Mandatory)

After drafting L1 subfunctions and L2 processes — and before generating L3 tasks — Claude must perform a critical self-review. This is not optional.

**Critique checklist:**
1. **Artificial symmetry** — All functions/L1s suspiciously equal in count? More importantly: do all L1s have the same number of L2s? This is the most common quality failure. L2 counts must reflect the actual operational complexity of each L1 — not a uniform number applied for tidiness. If every L1 has 5 L2s, that is almost certainly wrong. Actively challenge any L1 whose L2 count matches its neighbors and ask: does this domain genuinely have this many distinct processes, or did I pad to match?
2. **Copy-paste mirroring** — Same names with domain prefix swapped?
3. **Boundary bleed** — Same activity in multiple functions?
4. **Missing realities** — Domain-specific work not represented?
5. **Misplaced hierarchy** — L2s that should be L1s or vice versa?
6. **Naming precision** — Phase labels vs. descriptions of actual work? Ampersand groupings ("X & Y") stitching two discrete subfunctions or processes into one? Source real names from client materials where possible; otherwise make an educated guess and flag it. Cut artificial groupings into separate nodes.
7. **Speculative content** — L2s that assume capabilities or market participation the client doesn't actually have? Flag and cut.

Present the critique and proposed revisions. Get user approval before generating tasks.

### Excel Generation Rules
- Use openpyxl. **NEVER use formulas in WBS column** — formula XML causes Excel repair errors
- WBS column: plain text strings in `LL.PP.TT` format, auto-computed, zero-padded, counters reset at L1/L2 boundaries
- Tab name must be under 31 characters
- Header row: dark blue fill (#1F4E79), white bold Arial 10pt text
- Body: Arial 9pt, alternating light blue (#EBF3FB) and white row fills
- Wrap text on process_specifics (col D) and task_description (col I)
- Row height 80pt for data rows
- Freeze panes at A2
- Column widths: WBS=8, subfunction/business_unit=28, role=28, process=30, process_specifics=45, task_title=32, task_description=55

### Validation After Building
Run a programmatic audit before delivering:
- WBS identifiers correctly sequenced with counter resets
- No subfunction with fewer than 3 processes
- Flag any process with only 1 task
- Flag artificial symmetry in L2 or L3 counts
- Report structure summary to user

### In AVP — your turn
Once Claude delivers the Enhance Excel file(s):
1. Open AVP and navigate to the Business Function you're working on
2. Find the Enhance upload area for that function
3. Upload the Excel file Claude generated
4. AVP processes the file (this can take a few minutes per function)
5. Repeat for each function's Excel file
6. Tell Claude when all uploads are complete; Claude proceeds to Phase 4 (Business Context Questions)

If an upload errors out, share the error message or a screenshot — Claude can usually diagnose from the file structure.

---

## Phase 4: Business Context Questions

Answer all questions using client research. Keep responses to 1-2 sentences each. Focus on operational specificity over generic statements.

**Categories:**
- **Business Objectives** — Top 3 strategic goals, critical operational priorities, innovation areas
- **Execution Planning** — Go-live framing, budget context
- **Governance and Compliance** — Safety protocols, regulatory frameworks (name specific ones)
- **Technology Landscape** — Current systems (name actual ones), future environment
- **AI Maturity and Strategy** — Strategy, current AI applications (be specific)

Present all answers for user review/editing.

### In AVP — your turn
Once Claude's Business Context Questions answers are confirmed:
1. Open AVP and navigate to your project's setup / Business Context area
2. Paste each answer into its corresponding field
3. Save

That's the end of what this skill covers. The next AVP steps — Use Case Generation review, Calculate upload, and benefit-formula population — are handled outside this skill, directly in AVP.

### What's next
- **Building a Slalom PoV on AI Transformation from these Enhance outputs?** Once AVP Enhance finishes processing your uploads and you have the Task Generation / Task Analysis / Use Case Generation exports, switch to the `avp-pov-builder` skill. It will reuse the Demo Brief, financial parameters, audience context, and business-function inventory from this run — paste them in or point to where they're saved.
- **Just need the AVP setup?** You're done. Continue inside AVP for whatever the engagement requires.

---

## Key Decisions to Check With User

1. **Financial parameters** (discount rate, tax rate, hurdle rate) — after company description, before proposing business functions
2. **Business functions list** — before building any Enhance inputs
3. **Business function titles, descriptions, and analysis type** — presented together in Phase 2; user confirms before creating functions in AVP
4. **L1 subfunctions or roles** — before generating tasks
5. **Structural self-critique** — mandatory before generating L3 tasks
---

## Known Issues & Workarounds

- **WBS must be populated** — AVP needs WBS identifiers as plain text in `LL.PP.TT` format. Never leave blank.
- **WBS formulas in openpyxl cause Excel repair errors** — always use plain text strings, never formulas
- **Tab names >31 characters** — causes warnings; always keep under 31 chars

---

## Notes on Tone & Style

- Company and function descriptions: operational, no fluff, similar length and style
- Business context answers: 1-2 sentences, specific over generic
- Task descriptions: action verb first, specific operational language, avoid consulting jargon
- **Narrate the journey for non-experts.** At the start of each phase: state where the user is in the overall arc, what's about to happen, and what "done" looks like for this phase. Mid-phase: surface progress on long-running steps (researching, generating the Excel, etc.) so the user isn't staring at silence. At each checkpoint: explicitly confirm before moving on, and tell the user what the next phase will require from them. Assume the user is not an AVP expert unless they signal otherwise.
- Overall: direct, specific, collaborative — thinking partner, not form processor

---

## Reference Demos

### Amazon Air Demo (February 2026)
- 4 business functions: Air Hub & Gateway Operations (process), Network Planning (process), Air Cargo Commercial (process), Fleet Aviation Sourcing & Technical Operations (role)
- 3 enhance input files; Fleet Aviation was role-based

### ULA MC-SDLC Demo (April 2026)
- 3 business functions: Flight Software Engineering (12 L1s), Ground Systems Software Engineering (13 L1s), Software Verification, Validation & Certification (9 L1s)
- All process-based; 34 total L1 subfunctions, ~200 L2 processes
- Self-critique caught artificial symmetry (11-11-11 → revised to 12-13-9)

### Caterpillar Digital Demo (April 2026)
- 4 business functions: Helios Platform Engineering & Cloud Operations (9 L1s), Salesforce CRM & Marketing Technology (8 L1s), Digital Commerce & Customer Experience (6 L1s), AI-Enabled SDLC (8 L1s)
- All process-based; 31 total L1 subfunctions, 93 L2 processes, 228 tasks
- Audience: VMO team managing ~$800M in annual Cat Digital vendor spend
