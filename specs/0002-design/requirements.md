# requirements - 0002-design

## scope

v0.1 ships a fixture-backed scorecard for five public sovereign compute
programs. It ranks programs by projected GW over announced GW and names
the binding axis.

## requirements

- R-SC-013: `python -m sovereign_compute scorecard --quarter 2026q2`
  writes scorecard JSONL and a markdown report.
- R-SC-014: At least five program specs load from `programs/`.
- R-SC-015: Each program carries at least three reference URLs.
- R-SC-016: Projected GW never exceeds announced GW.
- R-SC-017: Every scorecard row names a binding constraint.

