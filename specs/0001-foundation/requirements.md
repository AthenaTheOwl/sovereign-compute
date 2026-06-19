# Spec 0001 — Foundation requirements

The first spec for SovereignCompute. Names the program schema, the
four feasibility axes, the scorecard schema, and the binding-constraint
discipline.

## Requirements

- **R-SC-001** — The repo MUST expose a `sovereign-compute` Python
  package with `__version__` and a CLI entry point.

- **R-SC-002** — A program spec MUST conform to
  `schemas/program.schema.json` with fields: `program_id`,
  `country`, `program_name`, `announced_gw`, `announced_horizon_year`,
  `announced_accelerator_count`, `announced_sites[]`,
  `announced_funding_usd`, `references[]` (URLs to primary sources).

- **R-SC-003** — Each feasibility axis (silicon, power, water,
  talent) MUST be a pure function from `(program_spec, input_data)`
  to a `FeasibilityResult` conforming to
  `schemas/feasibility_result.schema.json` with fields: `axis`,
  `program_id`, `projected_real_gw`, `confidence_low`,
  `confidence_high`, `rationale_text`, `evidence_refs[]`.

- **R-SC-004** — The aggregator MUST combine the four axis results
  by taking the minimum projected-real-GW (the binding constraint)
  and emitting a `Scorecard` record conforming to
  `schemas/scorecard.schema.json`.

- **R-SC-005** — The scorecard MUST name the binding constraint by
  axis and include the per-axis numbers (not just the min). A program
  with no clear single binding axis (within 5% of the min on two or
  more axes) MUST be flagged `multiple_binding`.

- **R-SC-006** — The repo MUST include at minimum five program specs
  in `programs/`: UAE G42, Saudi HUMAIN, EU AI Factories, India
  IndiaAI Mission, UK AISI.

- **R-SC-007** — Each program spec MUST cite at least three primary
  sources in `references[]`. Citation-faithfulness gate fails on any
  program with fewer.

- **R-SC-008** — The input data files (`data/silicon_allocations_*`,
  `data/grid_capacity_by_country.json`) MUST be schema-validated and
  every numeric entry MUST carry a `source_url` field.

- **R-SC-009** — The report renderer MUST emit
  `reports/<year>-Q<n>-scorecard.md` containing: a ranked table of
  programs by feasibility ratio (`projected_real_gw / announced_gw`),
  a per-program one-paragraph rationale, and a per-program
  binding-constraint badge.

- **R-SC-010** — Voice gate: the report MUST pass voice_lint and MUST
  NOT contain advocacy language (no "should", no "must", no
  "ought to" in the narrative; the format is descriptive scorecard,
  not policy recommendation).

- **R-SC-011** — No live network access at gate time. Every input is
  a checked-in file with a `source_url` plus a retrieval timestamp.

- **R-SC-012** — The repo MUST include `decisions/DEC-SC-001-axis-
  rubric.md` documenting how each axis converts program-spec input
  into a feasibility number.
