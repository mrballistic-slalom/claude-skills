"""
Skeleton transformer for avp-pov-builder v3.2+.

What v3.2 enforces beyond v3.1:
  - Per-UC math validation: NPV/benefit ratio, payback range, IRR cap, UC ID format.
    Catches the v3.1 cross-environment variance where claude.ai and Claude Code
    produced 169% different portfolio NPVs from identical inputs.
  - Filename convention: `YYYYMMDD - Slalom AI PoV - <Client> - DRAFT v<#>.html`.
    write() refuses on mismatched filenames. next_output_path() auto-bumps version.
  - Required big_one_type metadata in engagement data (5yr_npv | annual_benefit | payback).

v3.0 architecture (still in effect):
  - All UC-bound HTML renders from <script id="portfolio-data"> JSON at DOMContentLoaded
  - Narrative content lives inline with Acme sample as design reference
  - Top-level identifiers are {{}} inline placeholders
  - HERO + 7 narrative sections (ANCHOR_CARDS, MARKET_TRENDS, COMPETITORS,
    FORCING_FUNCTIONS, AVP_PROCESS_STRIP, AVP_VALUE_CHAIN, SOURCES) use fill_section

Usage:

    from transform import Skeleton

    sk = Skeleton('references/build-skeleton.html')
    sk.set_engagement_data(engagement_data_dict)  # validates per-UC math
    sk.fill_inline('PAGE_TITLE', 'Client — AI Portfolio | Slalom')
    sk.fill_inline('NAV_TITLE', 'Client · AI Transformation PoV · May 2026')
    sk.fill_inline('CLIENT_NAME', 'Client Name')
    sk.fill_inline('ENGAGEMENT_DOMAIN', 'Industry/Domain')
    sk.fill_section('HERO', hero_html)
    # ... fill_section for each narrative block ...

    out_path = Skeleton.next_output_path('Dollar Tree', 'output/')
    # → 'output/20260528 - Slalom AI PoV - Dollar Tree - DRAFT v1.html'
    sk.write(out_path)

See references/skeleton-transformer-guide.md for the full contract.
"""

import datetime
import json
import re
from pathlib import Path


class TransformError(Exception):
    """Raised when the transform contract is violated."""


class Skeleton:
    # Output growth ceiling — output should be 1.0x-1.5x the skeleton.
    # >1.8x suggests HTML was generated in Python strings rather than
    # rendered through the engagement-data JSON block.
    GENERATION_GUARD_RATIO = 1.8

    # Sections that MUST be filled with non-empty content. If the engagement
    # has a use case for a section, the section must be filled; passing
    # empty content silently means "the dashboard is missing that piece."
    # As of v3.1, narrative sections that previously caused CLIENT_NAME
    # placeholder collision (resolution: customize via fill_section BEFORE
    # fill_inline('CLIENT_NAME', ...)) are also required.
    REQUIRED_SECTIONS = {
        'HERO',
        'ANCHOR_CARDS',
        'MARKET_TRENDS',
        'COMPETITORS',
        'FORCING_FUNCTIONS',
        'AVP_PROCESS_STRIP',
        'AVP_VALUE_CHAIN',
        'SOURCES',
    }

    def __init__(self, skeleton_path):
        self.skeleton_path = Path(skeleton_path)
        if not self.skeleton_path.exists():
            raise TransformError(f"Skeleton not found: {skeleton_path}")

        with open(self.skeleton_path, 'r', encoding='utf-8') as f:
            self.html = f.read()

        self._skeleton_lines = self.html.count('\n') + 1

        if '{{' not in self.html:
            raise TransformError(
                f"Skeleton has no {{{{}}}} markers — caller may have passed "
                f"an already-built output file ({skeleton_path})"
            )

        if not self.html.lstrip().startswith('<!DOCTYPE'):
            raise TransformError(
                f"Skeleton does not start with <!DOCTYPE> ({skeleton_path})"
            )

        # Sanity: skeleton must have the engagement-data block + renderers
        if '<script id="portfolio-data"' not in self.html:
            raise TransformError(
                "Skeleton missing <script id=\"portfolio-data\"> block — "
                "v3.0+ requires the engagement-data JSON injection point."
            )
        for required_fn in ('_renderUCTiles', '_renderMatrixBubbles'):
            if required_fn not in self.html:
                raise TransformError(
                    f"Skeleton missing {required_fn} JS function — v3.0+ "
                    f"requires the data-driven render path."
                )

        self._filled_sections = set()
        self._filled_inlines = set()
        self._engagement_data_set = False

    # ------------------------------------------------------------------ #
    # Section filling
    # ------------------------------------------------------------------ #

    def fill_section(self, name, content):
        """
        Replace the block between <!-- {{name_START}} --> and <!-- {{name_END}} -->
        with `content`. The START/END markers themselves are also removed.

        `name` is the bare section name (e.g. 'HERO'), not 'HERO_START'.
        """
        if not isinstance(content, str):
            raise TransformError(
                f"fill_section('{name}', ...): content must be str, got "
                f"{type(content).__name__}"
            )

        if not content.strip():
            raise TransformError(
                f"fill_section('{name}', ''): empty content. If you mean "
                f"to leave this section out, explicitly call "
                f"sk.fill_section('{name}', '<!-- intentionally empty -->')."
            )

        start_marker = '<!-- {{' + name + '_START}} -->'
        end_marker = '<!-- {{' + name + '_END}} -->'

        # Reject content that contains its own START/END markers — this is
        # the v2.8 "marker leak-back" bug where Claude wraps content with
        # the markers it was supposed to replace.
        if start_marker in content or end_marker in content:
            raise TransformError(
                f"fill_section('{name}', ...): content contains its own "
                f"{start_marker} or {end_marker} marker. Do not wrap your "
                f"content in the section markers — fill_section already "
                f"handles the markers. Just pass the inner HTML."
            )

        start_count = self.html.count(start_marker)
        end_count = self.html.count(end_marker)

        if start_count == 0:
            raise TransformError(
                f"fill_section('{name}', ...): marker {start_marker} not "
                f"found in skeleton — check spelling against the guide"
            )
        if start_count > 1:
            raise TransformError(
                f"fill_section('{name}', ...): marker {start_marker} appears "
                f"{start_count}× in skeleton — markers must be unique"
            )
        if end_count != 1:
            raise TransformError(
                f"fill_section('{name}', ...): {end_marker} appears "
                f"{end_count}× (expected 1)"
            )

        si = self.html.find(start_marker)
        ei = self.html.find(end_marker, si) + len(end_marker)
        self.html = self.html[:si] + content + self.html[ei:]
        self._filled_sections.add(name)

    # ------------------------------------------------------------------ #
    # Inline placeholder filling
    # ------------------------------------------------------------------ #

    def fill_inline(self, name, value):
        """
        Replace every occurrence of {{name}} with `value`. Inline placeholders
        may legitimately appear more than once (e.g. CLIENT_NAME at 19 sites).
        """
        marker = '{{' + name + '}}'
        count = self.html.count(marker)
        if count == 0:
            raise TransformError(
                f"fill_inline('{name}', ...): {marker} not found in "
                f"skeleton — check spelling against the guide"
            )
        self.html = self.html.replace(marker, str(value))
        self._filled_inlines.add(name)

    # ------------------------------------------------------------------ #
    # Per-UC math validation (v3.2)
    # ------------------------------------------------------------------ #

    # Sanity bounds on per-UC metrics. The two cross-environment runs that
    # motivated v3.2 violated these in opposite directions (claude.ai compressed
    # NPV/benefit to 1.0×; Claude Code inflated payback to 1.8 months and
    # IRR to 500% across the board). These bounds catch both failure modes.
    UC_MATH_BOUNDS = {
        # NPV / annual_benefit ratio for a 5-year horizon, 10% hurdle, 65% realization,
        # 25% tax: roughly 0.65 × 0.75 × 3.79 (5yr annuity factor) - (invest/benefit).
        # That puts a sane NPV/benefit ratio in [1.3, 2.5]. Tightening to [1.2, 2.6]
        # to absorb legitimate variance from differing realization (60%-75%) and
        # hurdle (8%-12%) within retail composite.
        'npv_to_benefit_min': 1.2,
        'npv_to_benefit_max': 2.6,
        # Payback in months. Less than 3 months = unrealistic for any enterprise AI
        # build that requires data + integration + change management. More than 60
        # months = wouldn't make the portfolio.
        'payback_min_months': 3,
        'payback_max_months': 60,
        # IRR sanity. Less than 0% means the UC shouldn't be in the portfolio.
        # More than 250% is a sign that the model is hitting a cap or computing
        # IRR on a degenerate cashflow (e.g., perpetual benefit / one-time invest).
        'irr_min_pct': 0,
        'irr_max_pct': 250,
        # Per-UC investment floor — too small means a coding-only effort, not a
        # platform deployment. Floor at $0.2M.
        'invest_min_M': 0.2,
        # Per-UC benefit ceiling as a fraction of revenue (engagement-level cap).
        # Default: 1% of revenue. Engagement-config can override.
        'benefit_to_revenue_max_pct': 1.0,
    }

    # Canonical UC ID format: UC-NN (two-digit zero-padded).
    UC_ID_PATTERN = re.compile(r'^UC-\d{2}$')

    def _validate_uc_math(self, ucs, revenue_M=None):
        """Run sanity bounds on per-UC metrics. Returns list of violations.

        Empty list = no violations. Caller decides whether to raise or warn.
        """
        violations = []
        bounds = self.UC_MATH_BOUNDS
        for uc_id, uc in ucs.items():
            # ID format check
            if not self.UC_ID_PATTERN.match(uc_id):
                violations.append(
                    f"UC ID '{uc_id}' does not match canonical UC-NN pattern "
                    f"(two-digit zero-padded, e.g. UC-01). Use UC-{int(re.sub(chr(92)+'D','',uc_id) or 0):02d}."
                )
                continue  # other checks can't be done on a malformed ID safely

            ben = uc.get('benefitNum')
            npv = uc.get('npvNum')
            inv = uc.get('investNum')
            pb = uc.get('paybackNum')
            irr = uc.get('irrNum')

            # Presence
            for field, val in [('benefitNum', ben), ('npvNum', npv),
                                ('investNum', inv), ('paybackNum', pb)]:
                if val is None:
                    violations.append(f"{uc_id}: missing required field '{field}'")
                    break
            if any(v is None for v in (ben, npv, inv, pb)):
                continue

            # NPV/benefit ratio
            if ben > 0:
                ratio = npv / ben
                if ratio < bounds['npv_to_benefit_min']:
                    violations.append(
                        f"{uc_id}: NPV/benefit ratio {ratio:.2f}× is below sanity floor "
                        f"{bounds['npv_to_benefit_min']}× — NPV looks undercounted "
                        f"(ben=${ben}M, npv=${npv}M). Check that NPV uses full 5-yr horizon, "
                        f"not 1-year benefit."
                    )
                if ratio > bounds['npv_to_benefit_max']:
                    violations.append(
                        f"{uc_id}: NPV/benefit ratio {ratio:.2f}× is above sanity ceiling "
                        f"{bounds['npv_to_benefit_max']}× — NPV looks inflated "
                        f"(ben=${ben}M, npv=${npv}M). Check that realization "
                        f"haircut + tax are applied."
                    )

            # Payback range
            if pb < bounds['payback_min_months']:
                violations.append(
                    f"{uc_id}: payback {pb}mo is below floor {bounds['payback_min_months']}mo — "
                    f"likely computed as invest/benefit*12 without realization haircut, ramp, "
                    f"or tax. invest=${inv}M, benefit=${ben}M/yr."
                )
            if pb > bounds['payback_max_months']:
                violations.append(
                    f"{uc_id}: payback {pb}mo is above ceiling {bounds['payback_max_months']}mo — "
                    f"UC likely shouldn't be in portfolio."
                )

            # IRR range
            if irr is not None:
                if irr < bounds['irr_min_pct']:
                    violations.append(f"{uc_id}: IRR {irr}% is negative — UC shouldn't be in portfolio.")
                if irr > bounds['irr_max_pct']:
                    violations.append(
                        f"{uc_id}: IRR {irr}% exceeds sanity cap {bounds['irr_max_pct']}% — "
                        f"likely hitting a model output ceiling. Cap at ≥{bounds['irr_max_pct']}% "
                        f"display value or recompute on a finite cashflow profile."
                    )

            # Invest floor
            if inv < bounds['invest_min_M']:
                violations.append(
                    f"{uc_id}: investment ${inv}M is below floor ${bounds['invest_min_M']}M — "
                    f"too small for a platform deployment (would be a coding task)."
                )

            # Benefit-to-revenue ceiling (engagement-level)
            if revenue_M and ben > revenue_M * bounds['benefit_to_revenue_max_pct'] / 100:
                violations.append(
                    f"{uc_id}: benefit ${ben}M exceeds "
                    f"{bounds['benefit_to_revenue_max_pct']}% of revenue (${revenue_M}M) — "
                    f"single UC capturing >1% of company revenue is unusually large."
                )

        return violations

    # ------------------------------------------------------------------ #
    # Engagement data JSON block
    # ------------------------------------------------------------------ #

    def set_engagement_data(self, data):
        """
        Replace the {{ENGAGEMENT_DATA_JSON}} marker inside the skeleton's
        <script id="portfolio-data"> block with the serialized engagement data.

        `data` may be a dict (will be JSON-serialized) or a pre-serialized
        JSON string. The dict shape (required keys):

            {
              "ucs": {
                "UC-01": {
                  "name": "...", "fn": "...", "goal": "...",
                  "loe": "Quick Win" | "Standard" | "Major investment",
                  "loeClass": "qw" | "std" | "mi",
                  "phase": "Phase 1" | "Phase 2" | "Phase 3" | "Deprioritized",
                  "pool": "prio" | "all",
                  "desc": "...",
                  "benefit": "$X.XM", "npv": "$X.XM", "payback": "XX mo",
                  "benefitNum": float, "npvNum": float, "paybackNum": int,
                  "irrNum": int, "investNum": float,
                  "matrices": {
                    "benefit-loe": {"x": pct, "y": pct, "size": px},
                    "npv-payback": {"x": pct, "y": pct, "size": px},
                    "irr-payback": {"x": pct, "y": pct, "size": px}
                  }
                },
                ...
              }
            }

        Matrix view IDs (e.g. "benefit-loe", "irr-payback") correspond to
        the .matrix-view elements' id="matrix-{key}" attributes in the
        skeleton. Each UC's matrices map specifies its position in each view.
        """
        if isinstance(data, dict):
            payload = json.dumps(data, indent=2, ensure_ascii=False)
        else:
            payload = str(data)

        # v3.2: validate per-UC math BEFORE injection.
        if isinstance(data, dict) and 'ucs' in data:
            revenue_M = None
            meta = data.get('meta', {})
            if isinstance(meta, dict):
                revenue_M = meta.get('revenue_M')
            violations = self._validate_uc_math(data['ucs'], revenue_M=revenue_M)
            if violations:
                # Show up to 5 violations to keep error readable
                preview = '\n  - '.join(violations[:5])
                more = f'\n  ... and {len(violations) - 5} more violations' if len(violations) > 5 else ''
                raise TransformError(
                    f"set_engagement_data: {len(violations)} UC math violations:\n  - "
                    + preview + more +
                    "\n\nFix the per-UC numbers (NPV/benefit ratio, payback, IRR, invest floor) "
                    "OR override the bounds via Skeleton.UC_MATH_BOUNDS before calling."
                )

            # v3.2: validate big_one_type is set if expected
            if meta and 'big_one_type' in meta:
                allowed = {'5yr_npv', 'annual_benefit', 'payback'}
                if meta['big_one_type'] not in allowed:
                    raise TransformError(
                        f"meta.big_one_type='{meta['big_one_type']}' not in {sorted(allowed)}"
                    )

        # The JSON goes inside the existing <script id="portfolio-data"> tag,
        # replacing the {{ENGAGEMENT_DATA_JSON}} placeholder.
        if '{{ENGAGEMENT_DATA_JSON}}' not in self.html:
            raise TransformError(
                "Skeleton missing {{ENGAGEMENT_DATA_JSON}} marker — cannot "
                "inject engagement data."
            )

        self.html = self.html.replace('{{ENGAGEMENT_DATA_JSON}}', payload)
        self._engagement_data_set = True

    # ------------------------------------------------------------------ #
    # Filename convention (v3.2)
    # ------------------------------------------------------------------ #

    # Canonical filename: `YYYYMMDD - Slalom AI PoV - <Client> - DRAFT v<#>.html`
    # Spaces around hyphens are intentional. Client name preserved as-given
    # (including spaces). Version is integer, starts at 1, never overwrites.
    FILENAME_PATTERN = re.compile(
        r'^(?P<date>\d{8}) - Slalom AI PoV - (?P<client>.+) - DRAFT v(?P<version>\d+)\.html$'
    )

    @staticmethod
    def next_output_path(client_name, output_dir, today_iso=None):
        """Return the next available canonical output path for this client + date.

        Scans `output_dir` for existing files matching the pattern with the
        same client and date; returns a path with version = max_existing + 1.

        Args:
            client_name: e.g. "Dollar Tree"
            output_dir:  e.g. "/Users/aaron.butler/claude-workspace/projects/Dollar Tree/"
            today_iso:   override the date (YYYYMMDD), defaults to today.

        Returns:
            Path object, e.g. "<dir>/20260528 - Slalom AI PoV - Dollar Tree - DRAFT v1.html"
        """
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        if today_iso is None:
            today_iso = datetime.date.today().strftime('%Y%m%d')

        # Scan for existing versions of this client + date
        max_v = 0
        for entry in out_dir.iterdir():
            if not entry.is_file():
                continue
            m = Skeleton.FILENAME_PATTERN.match(entry.name)
            if not m:
                continue
            if m.group('date') == today_iso and m.group('client') == client_name:
                max_v = max(max_v, int(m.group('version')))

        next_v = max_v + 1
        filename = f"{today_iso} - Slalom AI PoV - {client_name} - DRAFT v{next_v}.html"
        return out_dir / filename

    # ------------------------------------------------------------------ #
    # Write — the contract gate
    # ------------------------------------------------------------------ #

    def write(self, output_path):
        """
        Validate the contract and write. Raises TransformError on any
        violation; the caller must fix and retry.
        """
        # Check 1 — no unfilled {{PLACEHOLDER}} markers
        remaining = sorted(set(re.findall(r'\{\{[A-Z_]+\}\}', self.html)))
        if remaining:
            raise TransformError(
                f"Unfilled placeholders ({len(remaining)}): "
                f"{remaining[:8]}{'...' if len(remaining) > 8 else ''}. "
                f"Call fill_inline() or fill_section() for each."
            )

        # Check 2 — required sections were filled
        unfilled_required = self.REQUIRED_SECTIONS - self._filled_sections
        if unfilled_required:
            raise TransformError(
                f"Required section(s) not filled via fill_section(): "
                f"{sorted(unfilled_required)}. (If the marker was replaced "
                f"by inline editing rather than fill_section, you must call "
                f"fill_section explicitly so the contract is verified.)"
            )

        # Check 3 — engagement data was set
        if not self._engagement_data_set:
            raise TransformError(
                "set_engagement_data() was never called. The skeleton's "
                "UC tiles, table rows, matrix bubbles, and Assumptions "
                "rows all render from the portfolio-data JSON block — "
                "without it, the dashboard is empty of UC data."
            )

        # Check 4 — filter chips not HTML-commented out
        # The skeleton has multiple .filter-btn and .if-chip elements; if any
        # of them are wrapped in <!-- --> comments, the interactive UI is
        # silenced. Detect this anti-pattern.
        suppressed_chip = re.search(
            r'<!--\s*<button[^>]*class="[^"]*(?:filter-btn|if-chip|aim-filter-chip|func-filter-chip)',
            self.html
        )
        if suppressed_chip:
            raise TransformError(
                "Filter chip wrapped in HTML comment detected: "
                f"{suppressed_chip.group(0)[:120]}... "
                "Filter chips must stay live. Do not comment them out as a "
                "self-repair action — fix the underlying CSS/data issue."
            )

        # Check 5 — portfolio view toggle not suppressed
        suppressed_toggle = re.search(
            r'<!--\s*(?:portfolio[- ]toggle[- ]suppressed|view[- ]toggle[- ]suppressed)',
            self.html
        )
        if suppressed_toggle:
            raise TransformError(
                "Portfolio view toggle suppression comment found: "
                f"{suppressed_toggle.group(0)[:100]}. The toggle is part of "
                "the skeleton and must remain functional. If the engagement "
                "has only one pool (ratio=1.0), the toggle still renders as "
                "a single-state indicator — do not silence it."
            )

        # Check 6 — generation-vs-transformation canary (S7)
        output_lines = self.html.count('\n') + 1
        ratio = output_lines / self._skeleton_lines
        if ratio > self.GENERATION_GUARD_RATIO:
            raise TransformError(
                f"Output line count {output_lines:,} is {ratio:.2f}× the "
                f"skeleton ({self._skeleton_lines:,} lines) — exceeds "
                f"{self.GENERATION_GUARD_RATIO}× ceiling. v3.0 expects ratio "
                f"~1.0x because UC content is rendered by JS from the JSON "
                f"block. A high ratio means HTML was injected in fill_section "
                f"that should have come from the data block instead."
            )

        # Check 7 (v3.2) — filename convention.
        # Canonical: `YYYYMMDD - Slalom AI PoV - <Client> - DRAFT v<#>.html`
        out = Path(output_path)
        if not self.FILENAME_PATTERN.match(out.name):
            raise TransformError(
                f"Output filename '{out.name}' does not match canonical pattern:\n"
                f"  'YYYYMMDD - Slalom AI PoV - <Client> - DRAFT v<#>.html'\n"
                f"Use Skeleton.next_output_path(client_name, output_dir) to "
                f"generate a compliant path that auto-increments the version "
                f"and never overwrites prior versions."
            )

        # Check 8 (v3.2) — refuse to overwrite an existing file (versioning safety).
        if out.exists():
            raise TransformError(
                f"Output file '{out}' already exists. The versioning convention "
                f"forbids overwrite — use Skeleton.next_output_path() to get the "
                f"next available v<#> path instead."
            )

        # Write
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, 'w', encoding='utf-8') as f:
            f.write(self.html)

        return {
            'output_path': str(out),
            'output_lines': output_lines,
            'skeleton_lines': self._skeleton_lines,
            'ratio': round(ratio, 3),
            'sections_filled': sorted(self._filled_sections),
            'inlines_filled': sorted(self._filled_inlines),
            'engagement_data_set': self._engagement_data_set,
        }

    # ------------------------------------------------------------------ #
    # Introspection + post-edit cleanup helpers
    # ------------------------------------------------------------------ #

    def list_unfilled_sections(self):
        starts = re.findall(r'\{\{([A-Z_]+)_START\}\}', self.html)
        return sorted(set(starts))

    def list_unfilled_inlines(self):
        all_markers = set(re.findall(r'\{\{([A-Z_]+)\}\}', self.html))
        section_markers = set()
        for name in self.list_unfilled_sections():
            section_markers.add(name + '_START')
            section_markers.add(name + '_END')
        return sorted(all_markers - section_markers)

    @staticmethod
    def strip_leaked_markers(file_path):
        """Post-edit cleanup for the Claude Code `cp + Edit` workflow.

        When Claude Code uses `cp build-skeleton.html ...` and then Edit-tools
        the content between section markers, the `<!-- {{NAME_START}} -->` and
        `<!-- {{NAME_END}} -->` comments often remain in the output. This is
        cosmetically wrong (and inconsistent with the claude.ai path where
        fill_section removes them).

        Call this on the built output to strip leaked section markers:

            from transform import Skeleton
            Skeleton.strip_leaked_markers('output/client.html')

        Idempotent. Only touches whitespace-flanked marker comments — never
        touches the engagement-data block or any non-marker content.
        """
        path = Path(file_path)
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        before = html.count('{{')
        # Match `<!-- {{ANY_NAME_START}} -->` or `<!-- {{ANY_NAME_END}} -->`
        # plus any surrounding whitespace/newline so we don't leave blank lines
        cleaned = re.sub(
            r'[ \t]*<!--\s*\{\{[A-Z_]+(?:_START|_END)\}\}\s*-->\s*\n?',
            '',
            html
        )
        with open(path, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        after = cleaned.count('{{')
        return {'markers_stripped': before - after, 'path': str(path)}


# ---------------------------------------------------------------------- #
# Self-test
# ---------------------------------------------------------------------- #

if __name__ == '__main__':
    import sys

    here = Path(__file__).parent
    sk = Skeleton(here / 'build-skeleton.html')
    print(f"Loading skeleton: {sk.skeleton_path}")
    print(f"  skeleton lines: {sk._skeleton_lines:,}")
    print(f"  unfilled sections: {len(sk.list_unfilled_sections())}")
    print(f"  unfilled inlines:  {len(sk.list_unfilled_inlines())}")

    # Negative test 1: write() refuses on unfilled
    try:
        sk.write('/tmp/skeleton-selftest.html')
        print("FAIL: empty write should have raised")
        sys.exit(1)
    except TransformError as e:
        print(f"PASS: write() refused empty fill: {str(e)[:90]}...")

    # Negative test 2: fill_section typo
    try:
        sk.fill_section('HERO_TYPO', '<div>x</div>')
        print("FAIL: typo should have raised")
        sys.exit(1)
    except TransformError as e:
        print(f"PASS: fill_section refused typo: {str(e)[:90]}...")

    # Negative test 3: fill_inline typo
    try:
        sk.fill_inline('PAGE_TITLE_TYPO', 'x')
        print("FAIL: inline typo should have raised")
        sys.exit(1)
    except TransformError as e:
        print(f"PASS: fill_inline refused typo: {str(e)[:90]}...")

    # Negative test 4: marker leak-back
    try:
        sk.fill_section('HERO', '<!-- {{HERO_START}} --><div>x</div><!-- {{HERO_END}} -->')
        print("FAIL: marker leak should have raised")
        sys.exit(1)
    except TransformError as e:
        print(f"PASS: fill_section refused marker leak-back: {str(e)[:90]}...")

    # Negative test 5: empty content
    try:
        sk.fill_section('HERO', '')
        print("FAIL: empty content should have raised")
        sys.exit(1)
    except TransformError as e:
        print(f"PASS: fill_section refused empty content: {str(e)[:90]}...")

    # Negative test 6 (v3.2): per-UC math violation
    try:
        sk2 = Skeleton(here / 'build-skeleton.html')
        sk2.set_engagement_data({
            "ucs": {
                "UC-01": {
                    "name": "Bad UC", "fn": "Ops", "goal": "M", "loe": "Quick Win",
                    "loeClass": "qw", "phase": "Phase 1", "pool": "prio", "desc": "d",
                    "benefit": "$28M", "npv": "$28M", "payback": "1 mo",
                    "benefitNum": 28, "npvNum": 28, "paybackNum": 1,
                    "irrNum": 500, "investNum": 8,
                    "matrices": {"benefit-loe": {"x": 50, "y": 50, "size": 30}}
                }
            }
        })
        print("FAIL: bad UC math should have raised")
        sys.exit(1)
    except TransformError as e:
        print(f"PASS: set_engagement_data refused bad UC math: {str(e)[:90]}...")

    # Negative test 7 (v3.2): UC ID format violation
    try:
        sk3 = Skeleton(here / 'build-skeleton.html')
        sk3.set_engagement_data({
            "ucs": {
                "UC-001": {  # 3-digit instead of UC-01
                    "name": "x", "fn": "Ops", "goal": "M", "loe": "Quick Win",
                    "loeClass": "qw", "phase": "Phase 1", "pool": "prio", "desc": "d",
                    "benefit": "$10M", "npv": "$18M", "payback": "12 mo",
                    "benefitNum": 10, "npvNum": 18, "paybackNum": 12, "irrNum": 30,
                    "investNum": 2, "matrices": {}
                }
            }
        })
        print("FAIL: UC-001 should have raised")
        sys.exit(1)
    except TransformError as e:
        print(f"PASS: set_engagement_data refused UC-NNN format: {str(e)[:90]}...")

    # Negative test 8 (v3.2): filename convention violation
    # First build a fully-filled skeleton
    sk4 = Skeleton(here / 'build-skeleton.html')
    sk4.set_engagement_data({
        "ucs": {
            "UC-01": {
                "name": "Good UC", "fn": "Ops", "goal": "M", "loe": "Quick Win",
                "loeClass": "qw", "phase": "Phase 1", "pool": "prio", "desc": "d",
                "benefit": "$10M", "npv": "$18M", "payback": "12 mo",
                "benefitNum": 10, "npvNum": 18, "paybackNum": 12, "irrNum": 30,
                "investNum": 2, "matrices": {}
            }
        }
    })
    for sec in ('HERO', 'ANCHOR_CARDS', 'MARKET_TRENDS', 'COMPETITORS',
                'FORCING_FUNCTIONS', 'AVP_PROCESS_STRIP', 'AVP_VALUE_CHAIN', 'SOURCES'):
        sk4.fill_section(sec, '<div>x</div>')
    sk4.fill_inline('PAGE_TITLE', 'x')
    sk4.fill_inline('NAV_TITLE', 'x')
    sk4.fill_inline('CLIENT_NAME', 'x')
    sk4.fill_inline('ENGAGEMENT_DOMAIN', 'x')
    try:
        sk4.write('/tmp/bad_filename.html')
        print("FAIL: bad filename should have raised")
        sys.exit(1)
    except TransformError as e:
        print(f"PASS: write refused non-canonical filename: {str(e)[:90]}...")

    # Positive test (v3.2): next_output_path generates a valid filename
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        path1 = Skeleton.next_output_path('Test Client', tmpdir, today_iso='20260528')
        assert path1.name == '20260528 - Slalom AI PoV - Test Client - DRAFT v1.html', f"Unexpected: {path1.name}"
        # Touch the file, ensure next call returns v2
        path1.touch()
        path2 = Skeleton.next_output_path('Test Client', tmpdir, today_iso='20260528')
        assert path2.name == '20260528 - Slalom AI PoV - Test Client - DRAFT v2.html', f"Unexpected: {path2.name}"
        print(f"PASS: next_output_path returns v1 then v2: '{path1.name}' → '{path2.name}'")

    print("\nAll self-tests passed.")
