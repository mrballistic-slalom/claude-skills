---
name: meetingviewer
description: Transform a meeting transcript into a polished single-page HTML report with executive summary, themes, sentiment, action items, and Slalom brand styling. Use when the user asks to analyse a meeting, summarise a transcript, or turn a meeting recording/transcript into a report. Accepts pasted VTT, Markdown, or plain-text transcript content. Delivers a complete self-contained HTML file as a downloadable artifact.
---

# Meeting Visualizer — `/meetingviewer`

You are an expert at analysing meeting transcripts and producing executive-quality HTML reports. When invoked, follow every step below precisely.

---

## Step 1 — Get the Transcript

Ask the user to paste their transcript directly into the chat. Accept any of these formats:

- **WebVTT (`.vtt`)** — timestamped cues with `<v SpeakerName>` tags
- **Markdown** — speaker blocks formatted as `**Speaker** *[timestamp]*`
- **Plain text** — unformatted dialogue (do your best to infer speakers)

If the user has already pasted transcript content in the same message that invoked the skill, skip asking and proceed immediately to Step 2.

---

## Step 2 — Parse the Transcript

Work entirely in memory — no files are read or written.

If the content is WebVTT:
- Strip all `WEBVTT` headers, UUID cue identifiers, and `-->` timestamp lines.
- Extract each `<v SpeakerName>text</v>` cue with its timestamp.
- Sort cues by timestamp.
- Merge consecutive cues from the same speaker into a single block.
- Build a structured list: `[{ timestamp, speaker, text }, ...]`

If the content is Markdown (already formatted with `**Speaker** *[timestamp]*`):
- Parse speaker names and their paragraphs directly.

If the content is plain text:
- Infer speaker turns from line breaks, names, or conversational cues as best you can.
- Note in your output summary if speaker attribution is uncertain.

---

## Step 3 — Analyse the Transcript

Perform ALL of the following analysis passes:

### 3a — Meeting Metadata
Extract or infer:
- **Meeting title** (from content clues or topic)
- **Date** (from content, or "unknown")
- **Duration** (difference between first and last timestamp, if available)
- **Attendees** with their affiliations (Slalom vs client, if determinable)
- **Approximate speaking time per speaker** (% breakdown)

### 3b — Executive Summary
Write 3–4 concise paragraphs (≈120 words each) suitable for a senior executive who was not present. Cover:
- Why the meeting happened and who was involved
- The most important things discussed or decided
- Any key tensions, risks, or open questions
- Where things stand at the end of the meeting

### 3c — Key Themes
Identify 4–7 major thematic threads. For each theme:
- Short title and one-sentence description
- 2–3 illustrative direct quotes with speaker attribution
- Resolution status: resolved / unresolved / deferred

### 3d — Sentiment Analysis
- **Overall meeting tone** (0–10 score) with a 2-sentence rationale
- **Per-speaker sentiment** — score and a 1-sentence characterisation
- **Tension moments** — exchanges showing friction, confusion, or disagreement
- **Positive highlights** — moments of alignment, enthusiasm, or breakthrough

### 3e — Action Items
For each action item or commitment:
- Owner (or "TBD")
- Description (1 sentence)
- Urgency: High / Medium / Low
- Due date if mentioned, otherwise "TBD"

### 3f — Notable Quotes
Select 5–8 of the most insightful or important verbatim quotes. Include speaker and approximate timestamp.

---

## Step 4 — Generate the HTML

Produce a complete, self-contained single-page HTML file. All CSS and JS must be inline — no external CDN links.

### CSS Design Tokens (Slalom Brand)
```css
:root {
  /* Primary core */
  --blue:        #0C62FB;
  --dark-blue:   #002FAF;
  /* Secondary core */
  --cyan:        #1BE1F2;
  --coral:       #FF4D5F;
  --purple:      #C7B9FF;
  --chart:       #DEFF4D;
  /* Tones */
  --cyan-dark:   #0ED3EB;
  --coral-dark:  #F53958;
  --purple-dark: #B6ACF9;
  --chart-dark:  #CBEB0F;
  /* Tints */
  --cyan-light:  #D1F9FC;
  --coral-light: #FFE0E3;
  --purple-light:#F4F1FF;
  --chart-light: #F8FFDB;
  /* Neutrals */
  --black:       #000000;
  --dark-gray:   #666666;
  --light-gray:  #E6E6E6;
  --white:       #FFFFFF;
}
```

> **Brand rule**: `--blue` MUST be visually present in every composition.
> Use `--dark-blue` for the sidebar and heavy headers.
> Use `--cyan` as the accent/highlight colour on dark backgrounds.

### Required Page Sections (in this order)

| Section ID | Nav Label | Content |
|---|---|---|
| `#exec-summary` | Executive Summary | Blue callout box with 3–4 paragraph summary + key stats bar |
| `#meeting-details` | Meeting Details | Date, duration, attendees (badges: badge-slalom / badge-client), speaking time breakdown |
| `#themes` | Themes | 4–7 theme cards with quotes and resolution status |
| `#transcript` | Full Transcript | Collapsible `<details>` per speaker block; timestamps shown |
| `#sentiment` | Sentiment | Per-speaker sentiment cards + tension/highlight lists |
| `#action-items` | Action Items | Table of all action items with owner, urgency pill, due date |
| `#quotes` | Notable Quotes | Quote-block display of 5–8 best quotes |

### Left-Hand Navigation
- Fixed sidebar, 220 px wide, `background: var(--dark-blue)`.
- Logo block at top: "SLALOM" bold + meeting date in muted subtitle.
- Scrollspy JS: highlight active section as user scrolls.
- Responsive: on ≤640px collapse to horizontal top bar.

### Card / UI Components
```html
<span class="section-label">Label Text</span>
<div class="exec-box">...</div>
<div class="card card-accent-blue|cyan|coral|purple|chart">...</div>
<span class="pill pill-resolved|pill-unresolved|pill-deferred|pill-high|pill-medium|pill-low">Text</span>
<div class="quote-block quote-blue|quote-coral|quote-cyan|quote-chart">
  <p>"Quote text"</p>
  <span class="quote-attr">— Speaker Name</span>
</div>
<details>
  <summary>Speaker Name <span class="pill pill-slalom|pill-client">Slalom|Client</span> · 4 min 12 sec</summary>
  <div class="details-body">
    <p><span class="ts">0:04:31</span> ... dialogue text ...</p>
  </div>
</details>
<div class="sentiment-card">
  <div class="sentiment-label">Speaker Name</div>
  <div class="sentiment-score" style="color:var(--blue)">7.5</div>
  <div class="bar-wrap"><div class="bar-fill" style="width:75%;background:var(--blue)"></div></div>
  <div class="sentiment-desc">Characterisation sentence.</div>
</div>
<span class="badge badge-slalom|badge-client"><span class="badge-dot"></span>Name — Role</span>
<tr>
  <td>Owner</td><td>Description</td>
  <td><span class="pill pill-high">High</span></td>
  <td>Due date</td>
</tr>
```

### Full CSS Block
```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: system-ui,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif; font-size: 16px; line-height: 1.6; color: var(--black); background: var(--white); }
.layout { display: flex; min-height: 100vh; }
nav { position: fixed; top: 0; left: 0; width: 220px; height: 100vh; background: var(--dark-blue); display: flex; flex-direction: column; z-index: 200; overflow-y: auto; scrollbar-width: thin; scrollbar-color: rgba(255,255,255,.2) transparent; box-shadow: 2px 0 12px rgba(0,0,0,.25); }
nav::-webkit-scrollbar { width: 4px; }
nav::-webkit-scrollbar-thumb { background: rgba(255,255,255,.2); border-radius: 2px; }
.nav-logo { display: block; color: var(--white); font-size: .75rem; font-weight: 800; letter-spacing: .15em; text-transform: uppercase; padding: 1.25rem 1.25rem .75rem; border-bottom: 1px solid rgba(255,255,255,.12); margin-bottom: .5rem; flex-shrink: 0; }
.nav-logo span { display: block; font-size: .65rem; font-weight: 400; letter-spacing: .05em; color: rgba(255,255,255,.5); text-transform: none; margin-top: .2rem; }
nav a { display: flex; align-items: center; gap: .6rem; color: rgba(255,255,255,.65); text-decoration: none; font-size: .78rem; font-weight: 500; padding: .55rem 1.25rem; border-left: 3px solid transparent; transition: color .15s, background .15s, border-color .15s; line-height: 1.3; }
nav a:hover { color: var(--white); background: rgba(255,255,255,.07); border-left-color: rgba(255,255,255,.3); }
nav a.active { color: var(--cyan); background: rgba(12,98,251,.25); border-left-color: var(--cyan); font-weight: 700; }
.nav-section-group { padding: .4rem 1.25rem .2rem; font-size: .6rem; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; color: rgba(255,255,255,.3); margin-top: .5rem; }
.main-content { margin-left: 220px; flex: 1; min-width: 0; }
.hero { background: linear-gradient(135deg, var(--dark-blue) 0%, #0039c7 60%, var(--blue) 100%); color: var(--white); padding: 3.5rem 2rem 3rem; }
.hero-inner { max-width: 960px; margin: 0 auto; }
.hero-eyebrow { display: inline-block; background: var(--cyan); color: var(--dark-blue); font-size: .7rem; font-weight: 800; letter-spacing: .15em; text-transform: uppercase; padding: .25rem .75rem; border-radius: 2px; margin-bottom: 1rem; }
.hero h1 { font-size: clamp(1.6rem,3.5vw,2.5rem); font-weight: 800; line-height: 1.15; margin-bottom: .75rem; }
.hero-meta { font-size: .875rem; color: rgba(255,255,255,.75); margin-bottom: 1.5rem; }
.hero-attendees { display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1.25rem; }
.badge { display: inline-flex; align-items: center; gap: .35rem; font-size: .78rem; padding: .3rem .7rem; border-radius: 20px; font-weight: 500; }
.badge-slalom { background: rgba(27,225,242,.18); color: var(--cyan); border: 1px solid rgba(27,225,242,.4); }
.badge-client { background: rgba(255,255,255,.12); color: rgba(255,255,255,.9); border: 1px solid rgba(255,255,255,.2); }
.badge-dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }
.page { max-width: 960px; margin: 0 auto; padding: 0 2rem; }
section { padding: 3rem 0; }
section + section { border-top: 1px solid var(--light-gray); }
.section-label { display: inline-block; font-size: .68rem; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; color: var(--blue); margin-bottom: .5rem; }
h2 { font-size: clamp(1.3rem,2.5vw,1.75rem); font-weight: 800; color: var(--dark-blue); margin-bottom: 1.25rem; line-height: 1.2; }
h3 { font-size: 1.05rem; font-weight: 700; color: var(--dark-blue); margin-bottom: .6rem; margin-top: 1.5rem; }
p { margin-bottom: .85rem; color: #222; }
.cards { display: grid; grid-template-columns: repeat(auto-fit,minmax(280px,1fr)); gap: 1.25rem; margin-top: 1.5rem; }
.card { background: var(--white); border: 1px solid var(--light-gray); border-radius: 6px; padding: 1.25rem 1.5rem; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.card-accent-blue  { border-top: 4px solid var(--blue); }
.card-accent-cyan  { border-top: 4px solid var(--cyan); }
.card-accent-coral { border-top: 4px solid var(--coral); }
.card-accent-purple{ border-top: 4px solid var(--purple); }
.card-accent-chart { border-top: 4px solid var(--chart-dark); }
.card h3 { margin-top: 0; }
.exec-box { background: var(--blue); color: var(--white); border-radius: 8px; padding: 2rem 2.25rem; margin-bottom: 1.5rem; }
.exec-box .section-label { color: var(--cyan); }
.exec-box h2 { color: var(--white); margin-bottom: 1rem; }
.exec-box p { color: rgba(255,255,255,.88); margin-bottom: .75rem; }
.exec-box p:last-child { margin-bottom: 0; }
.exec-stats { display: flex; flex-wrap: wrap; gap: 1.5rem; margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,.2); }
.exec-stat-num  { display: block; font-size: 2rem; font-weight: 800; line-height: 1; color: var(--cyan); }
.exec-stat-label{ display: block; font-size: .78rem; color: rgba(255,255,255,.7); margin-top: .2rem; }
.quote-block { border-left: 4px solid var(--blue); background: #f0f5ff; padding: 1rem 1.25rem; margin: 1.25rem 0; border-radius: 0 4px 4px 0; }
.quote-block p { margin-bottom: .25rem; font-style: italic; color: #333; }
.quote-attr { font-size: .8rem; font-weight: 700; color: var(--blue); font-style: normal; }
.quote-coral  { border-left-color: var(--coral);     background: #fff5f6; }
.quote-coral .quote-attr { color: var(--coral-dark); }
.quote-cyan   { border-left-color: var(--cyan);      background: #f0fdff; }
.quote-cyan .quote-attr { color: #059eac; }
.quote-chart  { border-left-color: var(--chart-dark); background: #f9ffe6; }
.quote-chart .quote-attr { color: #5c7200; }
.quote-purple { border-left-color: var(--purple-dark); background: var(--purple-light); }
.quote-purple .quote-attr { color: #4a3285; }
#sentiment { background: var(--purple-light); }
.sentiment-grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(220px,1fr)); gap: 1rem; margin-top: 1.5rem; }
.sentiment-card { background: var(--white); border-radius: 8px; padding: 1.25rem; box-shadow: 0 1px 4px rgba(0,0,0,.07); }
.sentiment-label { font-size: .7rem; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; margin-bottom: .35rem; }
.sentiment-score { font-size: 2rem; font-weight: 800; line-height: 1; margin-bottom: .35rem; }
.sentiment-desc { font-size: .85rem; color: var(--dark-gray); }
.bar-wrap { height: 6px; background: var(--light-gray); border-radius: 3px; margin: .5rem 0 .75rem; }
.bar-fill { height: 6px; border-radius: 3px; }
details { margin-bottom: .75rem; }
summary { cursor: pointer; list-style: none; display: flex; justify-content: space-between; align-items: center; padding: .65rem 1rem; background: #f0f5ff; border-radius: 5px; font-weight: 600; color: var(--dark-blue); font-size: .9rem; border: 1px solid rgba(12,98,251,.12); }
summary::-webkit-details-marker { display: none; }
summary::after { content: '+'; font-size: 1.1rem; color: var(--blue); }
details[open] summary::after { content: '−'; }
details[open] summary { border-radius: 5px 5px 0 0; border-bottom: none; }
.details-body { border: 1px solid rgba(12,98,251,.12); border-top: none; border-radius: 0 0 5px 5px; padding: 1rem 1.25rem; background: var(--white); font-size: .9rem; }
.details-body p { margin-bottom: .5rem; }
.ts { font-size: .75rem; font-weight: 700; color: var(--blue); font-family: monospace; margin-right: .5rem; }
.pill { display: inline-block; font-size: .7rem; font-weight: 700; padding: .2rem .55rem; border-radius: 12px; letter-spacing: .04em; text-transform: uppercase; }
.pill-resolved   { background: #e6faf0; color: #1a6b3a; }
.pill-unresolved { background: var(--coral-light); color: #b0001a; }
.pill-deferred   { background: #fff7e0; color: #8a6200; }
.pill-high       { background: var(--coral-light); color: #b0001a; }
.pill-medium     { background: #fff7e0; color: #8a6200; }
.pill-low        { background: var(--purple-light); color: #4a3285; }
.pill-slalom     { background: rgba(27,225,242,.15); color: #0a7a84; }
.pill-client     { background: var(--light-gray); color: var(--dark-gray); }
.action-table { width: 100%; border-collapse: collapse; margin-top: 1.25rem; font-size: .9rem; }
.action-table th { background: var(--dark-blue); color: var(--white); padding: .65rem 1rem; text-align: left; font-weight: 600; font-size: .8rem; }
.action-table td { padding: .6rem 1rem; border-bottom: 1px solid var(--light-gray); vertical-align: top; }
.action-table tr:nth-child(even) td { background: #f7f9ff; }
.action-table tr:hover td { background: #eef3ff; }
.speak-bar-wrap { margin-top: 1.5rem; }
.speak-bar-row { display: flex; align-items: center; gap: 1rem; margin-bottom: .6rem; font-size: .85rem; }
.speak-bar-name { min-width: 160px; font-weight: 600; }
.speak-bar-track { flex: 1; height: 8px; background: var(--light-gray); border-radius: 4px; }
.speak-bar-fill { height: 8px; border-radius: 4px; }
.speak-bar-pct { min-width: 40px; text-align: right; color: var(--dark-gray); font-size: .8rem; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
footer { background: var(--dark-blue); color: rgba(255,255,255,.7); text-align: center; padding: 2rem 1.5rem; font-size: .8rem; border-top: 3px solid var(--blue); }
footer strong { color: var(--cyan); }
.mt-sm { margin-top: .75rem; }
.mt-md { margin-top: 1.25rem; }
code { background: #f0f5ff; color: var(--dark-blue); padding: .1em .4em; border-radius: 3px; font-size: .88em; font-family: 'Cascadia Code','Fira Mono',Consolas,monospace; }
@media (max-width:900px){ nav{width:180px} .main-content{margin-left:180px} }
@media (max-width:700px){ .two-col{grid-template-columns:1fr} }
@media (max-width:640px){
  nav{position:relative;width:100%;height:auto;flex-direction:row;flex-wrap:wrap;padding-bottom:.5rem;box-shadow:0 2px 8px rgba(0,0,0,.25)}
  .nav-logo{border-bottom:none;border-right:1px solid rgba(255,255,255,.12);padding:.75rem 1rem}
  nav a{border-left:none;border-bottom:3px solid transparent;padding:.5rem .75rem}
  nav a.active{border-left:none;border-bottom-color:var(--cyan)}
  .nav-section-group{display:none}
  .main-content{margin-left:0}
}
@media print{
  nav{display:none} .main-content{margin-left:0}
  .hero,.exec-box,#sentiment{print-color-adjust:exact;-webkit-print-color-adjust:exact}
}
```

### Scrollspy JavaScript
```js
document.addEventListener('DOMContentLoaded', function () {
  const links = document.querySelectorAll('nav a[href^="#"]');
  const sections = Array.from(links).map(l => document.querySelector(l.getAttribute('href'))).filter(Boolean);
  function onScroll() {
    const scrollY = window.scrollY + 80;
    let current = sections[0];
    for (const s of sections) { if (s.offsetTop <= scrollY) current = s; }
    links.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + current.id));
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
});
```

---

## Step 5 — Deliver the Output

Deliver the complete HTML as a downloadable artifact. Name the file:
```
YYYY-MM-DD-<kebab-case-meeting-topic>-report.html
```

After delivering the artifact, provide a 2-sentence summary covering: who attended, the key outcome, and the number of action items found.

---

## Rules

- NEVER link to external CSS/JS/fonts — everything must be self-contained.
- Every section in the table MUST appear in the HTML.
- The sidebar MUST be present and scrollspy MUST work.
- Slalom Blue (`#0C62FB`) MUST appear visually somewhere on every screen of the page.
- Action items with no clear owner should be labelled "TBD".
- Quotes must be verbatim from the transcript — do not paraphrase.
- If the transcript is very short or inconclusive, still produce all sections but note where data is thin.
- Use a consistent 0–10 scale for sentiment and briefly explain the rationale.
