# AGENTS.md — sovereign-compute

Operating contract for AI agents (Claude, Codex, Cursor) working in
this repo. Same conventions as the rest of the AthenaTheOwl
portfolio. An agent trained on GridSilicon or WaferToWatt will
recognize the shape.

## What this repo is

A cross-country feasibility scorecard for sovereign AI compute
programs. Input: a set of YAML program specs plus inputs from
silicon, power, water, and talent layers. Output: a per-program
projected-real-GW number, a binding-constraint identifier, and a
ranked scorecard report.

The novelty is the cross-country comparison plus the named
binding-constraint per program. The math layer is borrowed from
RobustSiting and the data layers are borrowed from GridSilicon,
WaferToWatt, and InterconnectAlpha.

## Roles you may see in tasks

| Role | What they do |
|---|---|
| `program-curator` | Authors and maintains the YAML program specs in `programs/` |
| `silicon-evaluator` | Maps program announced-accelerator count against allocated CoWoS / HBM share |
| `power-evaluator` | Computes deliverable GW given grid build-out in the program's geography |
| `water-evaluator` | Estimates cooling-water availability against announced footprint |
| `talent-evaluator` | Estimates qualified-FTE supply against program demand |
| `aggregator` | Joins per-axis results into a single program feasibility number |
| `binding-constraint-finder` | Picks the lowest axis as the named binding constraint |
| `report-renderer` | Produces the published scorecard |

## Voice constraints

- Plain assertions. No "leverage", "synergy", "seamless",
  "best-in-class", "demonstrates" as filler. The banned set lands in
  `scripts/voice_lint.py::BANNED_FAIL` in spec 0002.
- No antithetical reversals as a structural device.
- This repo touches geopolitically sensitive material. No advocacy.
  Cite primary sources (program announcements, government RFIs,
  ministry press releases) by URL.
- Every "projected real GW" number is reproducible from the
  checked-in program spec plus the checked-in input data files.

## Gates (will land in spec 0002)

```bash
uv run pytest
python scripts/voice_lint.py
python scripts/validate_schemas.py
python eval/sanity_bounds.py
```

The sanity-bounds gate fails if any program's projected-real-GW
exceeds its announced GW, or if any binding-constraint axis is
missing.

## Out of scope

- Recommendations on which sovereign program a country should join.
- Equity or sovereign-debt views.
- Classified or NDA program details. Public-disclosure-only.
- Predictions about geopolitical events (the scenario library is
  conditional, not predictive).
