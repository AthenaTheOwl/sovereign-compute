---
id: DEC-SC-001-axis-rubric
spec: specs/0002-design/
requirement: R-SC-017
date: 2026-06-20
status: approved
reversible: true
decision: |
  Compute projected real GW as the minimum of silicon, power, water, and
  talent axis estimates for each sovereign compute program.
alternatives:
  - label: average the axes
    rejected_because: |
      An average can hide a hard bottleneck. A compute campus cannot exceed
      the lowest binding input.
  - label: publish axes without a rollup
    rejected_because: |
      The scorecard needs one ranked value so readers can compare programs.
rationale: |
  The minimum-axis rule is easy to audit and matches the constraint logic used
  by the sibling grid and silicon repos.
evidence:
  - kind: spec
    ref: specs/0002-design/
rollback: |
  Replace the minimum rule with an optimization model after the program specs
  carry site-level inputs.
---

