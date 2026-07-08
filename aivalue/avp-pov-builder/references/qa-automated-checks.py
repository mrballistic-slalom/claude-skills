"""Phase 10 QA automated checks — block delivery on hard fails.

Run before declaring Phase 11 delivery:
    python3 qa-automated-checks.py <rendered.html> [--client-hq US]

Exit 0 = pass (or warnings only — surface to user, OK to deliver).
Exit 1 = fail (block delivery, return to failing phase, fix).

Calibrated against three internal reference builds:
  - Canonical golden master build: PASS (with known-deviation warnings)
  - Reference broken build (emojis, British, raw [I#], untagged matrix bubbles): FAIL
  - Reference corrected build: PASS clean

Re-calibrate by editing thresholds in run_qa() and running the in-file
test corpus via `python3 qa-automated-checks.py --test`.

See `references/client-language.md` for the rules this script enforces.
"""
import re
import sys
from pathlib import Path


def run_qa(html_path, client_hq='US', audience_technical=False):
    """Return (failures, warnings) tuple of strings.

    Failures block Phase 11 delivery. Warnings surface to user.
    """
    html = Path(html_path).read_text()

    # Strip non-visible content for body-text checks
    no_assets = re.sub(r'data:image/[^"]+', '', html)
    no_assets = re.sub(r'<script.*?</script>', '', no_assets, flags=re.DOTALL)
    no_assets = re.sub(r'<style.*?</style>', '', no_assets, flags=re.DOTALL)
    no_assets = re.sub(r'<svg.*?</svg>', '', no_assets, flags=re.DOTALL)
    visible = re.sub(r'<[^>]+>', ' ', no_assets)

    failures, warnings = [], []

    # ============================================================
    # STRUCTURAL — always fail (HTML must be well-formed and self-consistent)
    # ============================================================

    # S1: DIV depth trace ends at 0, no excessive negative excursions
    depth, min_depth = 0, 0
    for m in re.finditer(r'<(/?)div(?:\s[^>]*)?(/?)>', no_assets):
        if m.group(1):
            depth -= 1
        elif not m.group(2):
            depth += 1
        min_depth = min(min_depth, depth)
    if depth != 0:
        failures.append(f"DIV unbalanced: ends at depth {depth} (expected 0)")
    if min_depth < -3:
        failures.append(f"DIV depth went to {min_depth} mid-document — extra closes")

    # S2: CSS variables referenced via var() must be defined in <style>
    style_m = re.search(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
    if style_m:
        style = style_m.group(1)
        defined_vars = {v[2:] for v in re.findall(r'(--[\w-]+)\s*:', style)}
        referenced = set(re.findall(r'var\(--([\w-]+)\)', html))
        missing = referenced - defined_vars
        if missing:
            failures.append(f"CSS variables referenced but undefined: {sorted(missing)}")

    # S3: Substantive class names used in HTML body must be defined in CSS
    if style_m:
        defined_classes = set(re.findall(r'\.([a-zA-Z][\w-]+)', style))
        body_html = html[html.find('</style>'):]
        # Strip <script> blocks before class extraction — JS string templates
        # contain partial class name fragments that produce false positives
        body_html = re.sub(r'<script\b[^>]*>.*?</script>', '', body_html, flags=re.DOTALL)
        used = set()
        for m in re.finditer(r'class="([^"]+)"', body_html):
            for c in m.group(1).split():
                used.add(c)
        allow = {'active', 'open', 'st0', 'hidden-row', 'new'}
        substantive = {c for c in used
                       if c not in allow
                       and not c.startswith(('filter-', 'src-', 'view-', 'anchor-', 'phase-', 'fn-', 'sort-'))
                       and len(c) > 2}
        undef = substantive - defined_classes
        if len(undef) > 5:
            failures.append(f"{len(undef)} classes used but undefined in CSS: {sorted(undef)[:8]}")
        elif undef:
            warnings.append(f"{len(undef)} classes used but undefined: {sorted(undef)}")

    # S4: No unfilled template placeholders.
    # As of v2.8 the skeleton preamble was extracted to a sibling guide file,
    # so {{}} markers in the file are real placeholders only. We still strip
    # HTML comments defensively (a built output should never have stray {{}}
    # in comments, but if Claude pasted something unusual we want to be sure).
    html_no_comments = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    placeholders = re.findall(r'\{\{[A-Z_]+\}\}', html_no_comments)
    if placeholders:
        failures.append(f"Unfilled template placeholders ({len(set(placeholders))}): {sorted(set(placeholders))[:8]}")

    # S7: Generation-vs-transformation canary.
    # The skeleton is ~1,640 lines. A real engagement fill grows the file
    # by ~30-80% (more UCs, more anchors, denser tabs). Anything > 2.2× the
    # skeleton baseline indicates HTML was generated in Python strings rather
    # than filled into section markers — the Dollar Tree failure mode.
    skeleton_path = Path(__file__).parent / 'build-skeleton.html'
    if skeleton_path.exists():
        with open(skeleton_path, 'r', encoding='utf-8') as f:
            skeleton_lines = f.read().count('\n') + 1
        output_lines = html.count('\n') + 1
        ratio = output_lines / skeleton_lines if skeleton_lines else 0
        if ratio > 2.2:
            failures.append(
                f"Output is {output_lines:,} lines vs skeleton {skeleton_lines:,} "
                f"({ratio:.2f}× — exceeds 2.2× ceiling). Likely generated in "
                f"Python strings instead of filled into skeleton sections. "
                f"Use references/transform.py."
            )
        elif ratio > 1.9:
            warnings.append(
                f"Output is {ratio:.2f}× skeleton size — close to generation "
                f"ceiling. Review fill_section() argument sizes."
            )

    # ============================================================
    # CONTENT — escalate severity by volume (per client-language.md thresholds)
    # ============================================================

    # C0: Competitor names — ANY appearance fails
    competitors = ['McKinsey', 'BCG', 'Boston Consulting', 'Deloitte', 'Accenture', 'Bain & Company',
                   ' Bain ', 'Ernst & Young', 'PricewaterhouseCoopers', 'KPMG']
    # 'EY' and 'PwC' are too short to safely word-boundary against; check carefully
    competitor_hits = []
    for comp in competitors:
        cnt = visible.count(comp)
        if cnt > 0:
            competitor_hits.append(f"{comp}({cnt})")
    # Word-boundary check for short acronyms
    for comp in ['EY', 'PwC']:
        cnt = len(re.findall(rf'\b{comp}\b', visible))
        if cnt > 0:
            competitor_hits.append(f"{comp}({cnt})")
    if competitor_hits:
        failures.append(f"Competitor names in visible content: {competitor_hits} — never name Slalom competitors")

    # C1: Value-badge emojis — ANY appearance fails
    bad_emojis = ['♥', '☮', '🎓', '★', '✓', '✗']
    total_emoji = sum(visible.count(e) for e in bad_emojis)
    if total_emoji > 0:
        emoji_breakdown = [f"{e}({visible.count(e)})" for e in bad_emojis if visible.count(e) > 0]
        failures.append(f"Value-badge emojis in visible content ({total_emoji}× — {emoji_breakdown}) — use text labels")

    # C2: 'bundle' word — > 10 fails, > 0 warns
    bundle_count = len(re.findall(r'\bbundle\b', visible, re.IGNORECASE))
    if bundle_count > 10:
        failures.append(f"'bundle' in visible content {bundle_count}× — convention is 'Use Case'")
    elif bundle_count > 0:
        warnings.append(f"'bundle' in visible content {bundle_count}× — convention is 'Use Case'")

    # C3: British English on US-HQ client
    if client_hq == 'US':
        brit_total = 0
        brit_examples = []
        for brit in ['realisation', 'prioritis', 'organis', 'behaviou', 'analyse']:
            cnt = len(re.findall(rf'\b{brit}', visible, re.IGNORECASE))
            brit_total += cnt
            if cnt > 0:
                brit_examples.append(f"{brit}*({cnt})")
        if brit_total > 50:
            failures.append(f"British spellings on US-HQ client: {brit_total}× — sweep to US English ({brit_examples[:3]})")
        elif brit_total > 0:
            warnings.append(f"British spellings on US-HQ client: {brit_total}× — {brit_examples}")

    # C4: Raw [S#]/[I#]/[B#] inline brackets in body — > 30 fails, > 5 warns
    raw_total = sum(len(re.findall(rf'\[{tag}\d+\]', visible)) for tag in 'SIB')
    raw_threshold_fail = 100 if audience_technical else 30
    if raw_total > raw_threshold_fail:
        failures.append(f"Raw [S#]/[I#]/[B#] inline brackets in body: {raw_total}× — use styled spans (<span class=\"s-ref\">)")
    elif raw_total > 5:
        warnings.append(f"Raw [S#]/[I#]/[B#] inline brackets in body: {raw_total}×")

    # C5: HEAVY mode label leak (per editorial-rules.md line 86)
    if re.search(r'\bHEAVY mode\b', visible):
        warnings.append("'HEAVY mode' label visible in body — internal authoring note that leaked (per editorial-rules.md)")

    # C6: Technical language for non-technical audiences
    if not audience_technical:
        if re.search(r'\bMonte Carlo\b', visible):
            warnings.append("'Monte Carlo' in body — consider 'probabilistic sensitivity analysis' for non-quant audiences")
        if 'P(NPV>0)' in visible or 'P(NPV&gt;0)' in visible:
            warnings.append("'P(NPV>0)' in body — consider 'Probability of positive return' for non-quant audiences")

    # ============================================================
    # INTERACTIVE — always fail when applicable
    # ============================================================

    # I1: SVG matrix bubbles must have <g data-fn=...> wrappers to participate in filters
    bubble_circles = re.findall(r'<circle[^>]*r="\d+"[^>]*fill="#', html)
    bubble_groups_tagged = re.findall(r'<g[^>]*data-fn=', html)
    if len(bubble_circles) > 20 and not bubble_groups_tagged and 'chart.js' not in html.lower():
        failures.append(f"{len(bubble_circles)} matrix bubbles but no <g data-fn=...> wrappers — won't filter in sidebar")

    # I2: JS functions called via onclick must be defined
    for fn in ['setFilter', 'setView', 'setSource', 'setAnchor', 'setPhase', 'showTab', 'openModal', 'closeModal']:
        if f'onclick="{fn}(' in html and f'function {fn}' not in html:
            failures.append(f"JS function {fn} called via onclick but not defined")

    # I3: Canonical tab IDs (allow legacy IDs per golden-master.md)
    canonical = ['tab-summary', 'tab-whynow', 'tab-aiportfolio',
                 'tab-avpanalysis', 'tab-roadmap',
                 'tab-assumptions', 'tab-sources']
    bms_legacy = ['tab-portfolio', 'tab-avp', 'tab-phasing', 'tab-risks']
    missing_tabs = [t for t in canonical if f'id="{t}"' not in html]
    has_legacy = any(f'id="{t}"' in html for t in bms_legacy)
    if missing_tabs and not has_legacy:
        warnings.append(f"Missing canonical tab IDs (canonical per structural-rules.md): {missing_tabs}")

    # I4: Slalom logo must be inline SVG (not base64, not approximated)
    if 'class="slalom-logo"' in html or 'class="nav-brand"' in html:
        # Some inline SVG should be present
        if not re.search(r'<svg[^>]*viewBox="0 0 216 56\.1"', html):
            warnings.append("Slalom logo: canonical inline SVG viewBox not found — verify logo is inline, not base64")

    # I5: Portfolio View Toggle — warn if absent without suppression note
    # Required when broad pool > final portfolio (downselect ratio < 1.0).
    # Pass --portfolio-toggle=required to hard-fail; pass --portfolio-toggle=suppressed to skip.
    has_set_view_fn = 'function setView' in html
    has_set_view_call = 'setView(' in html
    has_suppression = 'portfolio-toggle-suppressed' in html
    toggle_mode = getattr(run_qa, '_portfolio_toggle_mode', 'auto')
    if toggle_mode == 'required':
        if not has_set_view_fn:
            failures.append("Portfolio View Toggle required (--portfolio-toggle=required) but setView function absent — add toggle per references/portfolio-view-toggle.md")
    elif toggle_mode != 'suppressed':
        # auto mode: warn if neither toggle nor suppression comment is present
        if not has_set_view_fn and not has_suppression:
            warnings.append("Portfolio View Toggle absent and no suppression comment — required when broad pool > final portfolio; add <!-- portfolio-toggle-suppressed: ratio=1.0 --> if intentionally suppressed")

    # ============================================================
    # STRUCTURAL v2.5 — attribution footer and CSS variable discipline
    # ============================================================

    # S5: Skill attribution footer must appear on every tab panel (hard fail when absent; warn on count mismatch)
    tab_panels = re.findall(r'<div[^>]+id="tab-[^"]*"[^>]*class="[^"]*tab-panel', html) + \
                 re.findall(r'<div[^>]+class="[^"]*tab-panel[^"]*"[^>]*id="tab-', html)
    # Also match simplified pattern: class="tab-panel"
    if not tab_panels:
        tab_panels = re.findall(r'class="tab-panel[^"]*"', html)
    tab_count = len(set(tab_panels)) or len(re.findall(r'<!-- END TAB ', html))
    attribution_divs = re.findall(r'class="skill-attribution"', html)
    attr_count = len(attribution_divs)
    if tab_count > 0 and attr_count == 0:
        failures.append(f"Skill attribution footer absent — 0 'skill-attribution' divs found ({tab_count} tab panels detected) — mandatory on every tab per SKILL.md — Phase 9")
    elif tab_count > 0 and attr_count < tab_count:
        failures.append(f"Skill attribution footer missing from {tab_count - attr_count} of {tab_count} tab panels — must appear on every tab")

    # S6: Hardcoded hex values in CSS outside :root variable definitions (color drift)
    # Goal: catch colors that should be var() references (e.g. #0a3a8a, #888, #5a4000)
    # while tolerating #fff/#000 (pure white/black used on dark backgrounds) and a small
    # number of intentional component-tint colors (probability badges, tier chips, etc.)
    # The canonical build-skeleton.html v2.5 uses ~15 non-white hex values for tints;
    # > 20 non-white instances is a strong signal of color drift from the palette.
    if style_m:
        style_text = style_m.group(1)
        # Strip the :root block (where variable values are legitimately defined)
        style_no_root = re.sub(r':root\s*\{[^}]*\}', '', style_text, flags=re.DOTALL)
        # Strip comments
        style_no_root = re.sub(r'/\*.*?\*/', '', style_no_root, flags=re.DOTALL)
        # Find hex values in property values; exclude pure white (#fff/#ffffff) and black (#000/#000000)
        all_hex = re.findall(r':\s*(#[0-9a-fA-F]{3,6})\s*[;,)]', style_no_root)
        hex_in_rules = [h for h in all_hex if h.lower() not in ('#fff', '#ffffff', '#000', '#000000')]
        if hex_in_rules:
            unique_hex = sorted(set(hex_in_rules))[:8]
            if len(hex_in_rules) > 20:
                # > 20 non-white hex values = likely pervasive color drift, hard fail
                failures.append(f"Hardcoded hex values in CSS outside :root ({len(hex_in_rules)} non-white instances: {unique_hex}…) — use var(--variable); palette variables include --hero-end:#0a3a8a, --muted:#6b7588, --ink:#0e1422")
            elif len(hex_in_rules) > 8:
                # 9–20 = elevated drift, warn
                warnings.append(f"Hardcoded hex values in CSS outside :root ({len(hex_in_rules)} non-white instances: {unique_hex}) — prefer var(--variable) from the canonical palette")
            elif len(hex_in_rules) > 3:
                warnings.append(f"Hardcoded hex values in CSS outside :root: {unique_hex} — prefer var(--variable)")

    return failures, warnings


def report(name, html_path, expected_pass, client_hq='US', audience_technical=False):
    print(f"\n{'='*70}\nTEST: {name}")
    print(f"Expected: {'PASS' if expected_pass else 'FAIL'}\n{'='*70}")
    fails, warns = run_qa(html_path, client_hq=client_hq, audience_technical=audience_technical)
    print(f"  Failures: {len(fails)}")
    for f in fails:
        print(f"    FAIL: {f}")
    print(f"  Warnings: {len(warns)}")
    for w in warns:
        print(f"    WARN: {w}")
    actual_pass = len(fails) == 0
    verdict = 'OK ' if actual_pass == expected_pass else 'WRONG'
    print(f"  Verdict: {verdict} (got {'PASS' if actual_pass else 'FAIL'})")
    return actual_pass == expected_pass


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == '--test':
        # In-file calibration test.
        # CALIBRATION_PASS and CALIBRATION_FAIL must point to local builds on your machine.
        # The skeleton is expected to FAIL on S4 (276 unfilled placeholders by design).
        SKILL_DIR = Path(__file__).parent
        CALIBRATION_PASS = str(SKILL_DIR / '..' / 'calibration' / 'clean-build.html')   # replace with your clean passing build
        CALIBRATION_FAIL = str(SKILL_DIR / '..' / 'calibration' / 'broken-build.html')  # replace with your broken build
        results = []
        results.append(report(
            "Calibration build — clean (no competitors, no emojis, no British) — must PASS",
            CALIBRATION_PASS,
            expected_pass=True
        ))
        results.append(report(
            "Calibration build — broken (emojis, British, untagged bubbles) — must FAIL",
            CALIBRATION_FAIL,
            expected_pass=False
        ))
        results.append(report(
            "Canonical skeleton — expected FAIL on S4 (276 unfilled placeholders by design)",
            str(SKILL_DIR / 'build-skeleton.html'),
            expected_pass=False
        ))
        print(f"\n{'='*70}\nCALIBRATION: {sum(results)}/{len(results)} matched expectation\n{'='*70}")
        sys.exit(0 if all(results) else 1)

    # Real QA run
    html_path = sys.argv[1]
    client_hq = 'US'
    audience_technical = False
    portfolio_toggle = 'auto'   # auto | required | suppressed
    for arg in sys.argv[2:]:
        if arg.startswith('--client-hq='):
            client_hq = arg.split('=', 1)[1]
        elif arg == '--audience-technical':
            audience_technical = True
        elif arg.startswith('--portfolio-toggle='):
            portfolio_toggle = arg.split('=', 1)[1]

    # Attach portfolio_toggle mode to run_qa so I5 can read it (avoids signature churn)
    run_qa._portfolio_toggle_mode = portfolio_toggle

    print(f"Running QA on: {html_path}")
    print(f"  client_hq={client_hq}, audience_technical={audience_technical}, portfolio_toggle={portfolio_toggle}")
    fails, warns = run_qa(html_path, client_hq=client_hq, audience_technical=audience_technical)

    if fails:
        print(f"\nFAILURES ({len(fails)}) — block Phase 11 delivery:")
        for f in fails:
            print(f"  FAIL: {f}")

    if warns:
        print(f"\nWARNINGS ({len(warns)}) — surface to user, OK to deliver:")
        for w in warns:
            print(f"  WARN: {w}")

    if not fails and not warns:
        print("\nQA PASSED — clean.")

    sys.exit(0 if not fails else 1)


if __name__ == "__main__":
    main()
