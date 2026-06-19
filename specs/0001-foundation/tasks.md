# Spec 0001 — Foundation tasks

Ordered task list for the first 2-3 PRs after the scaffold.

## PR 1 — package skeleton plus program schema

- [ ] Add `pyproject.toml` declaring `sovereign-compute` and CLI.
- [ ] Add `src/sovereign_compute/__init__.py` with `__version__`.
- [ ] Add `src/sovereign_compute/cli.py` with no-op `version` command.
- [ ] Add `schemas/program.schema.json` matching R-SC-002.
- [ ] Add `src/sovereign_compute/program/schema.py`.
- [ ] Add `src/sovereign_compute/program/loader.py`.
- [ ] Add three seed program YAMLs: `programs/uae-g42.yaml`,
      `programs/saudi-humain.yaml`, `programs/eu-ai-factories.yaml`
      (each with at least three primary-source citations).
- [ ] Add `tests/test_program_loader.py`.
- [ ] Add `decisions/DEC-SC-001-axis-rubric.md`.

## PR 2 — silicon and power axes plus aggregator

- [ ] Add `schemas/feasibility_result.schema.json`.
- [ ] Add `schemas/scorecard.schema.json`.
- [ ] Add `data/silicon_allocations_2026q2.json` seed.
- [ ] Add `data/grid_capacity_by_country.json` seed.
- [ ] Add `src/sovereign_compute/feasibility/silicon.py`.
- [ ] Add `src/sovereign_compute/feasibility/power.py`.
- [ ] Add `src/sovereign_compute/scorecard/aggregate.py`.
- [ ] Add `src/sovereign_compute/scorecard/binding_constraint.py`.
- [ ] Add `tests/test_silicon_axis.py`, `test_power_axis.py`,
      `test_aggregator.py`.
- [ ] Add `scripts/voice_lint.py`.
- [ ] Add `scripts/validate_schemas.py`.

## PR 3 — water and talent axes, full report, gates

- [ ] Add `programs/indiaai.yaml`, `programs/uk-aisi.yaml`.
- [ ] Add `data/water_basin_by_site.json`,
      `data/fte_supply_by_country.json`.
- [ ] Add `src/sovereign_compute/feasibility/water.py`,
      `talent.py`.
- [ ] Add `src/sovereign_compute/report/render.py`.
- [ ] Generate `reports/2026-Q3-scorecard.md` end to end.
- [ ] Add `eval/sanity_bounds.py`.
- [ ] Add `docs/dev/adding-a-program.md`.
