# Spec 0001 — Foundation design

## Shape

A Python CLI plus four feasibility-axis modules plus an aggregator
plus a renderer. The pipeline is pure: program specs and input data
files in, scorecard markdown plus JSON sidecar out.

## Components

### Program loader (`src/sovereign_compute/program/`)

- `schema.py` — dataclass for `ProgramSpec`.
- `loader.py` — `load_programs(dir)` reads every YAML under
  `programs/`, validates each against `schemas/program.schema.json`,
  returns a list of `ProgramSpec`.

### Feasibility axes (`src/sovereign_compute/feasibility/`)

Each axis is one module exposing `evaluate(program, input_data) ->
FeasibilityResult`. Pure function, no IO.

- `silicon.py` — given announced accelerator count and the global
  CoWoS / HBM allocation table, compute the program's plausibly
  allocated share. Returns a projected-deliverable accelerator count
  converted to GW via a per-accelerator GW divisor.
- `power.py` — given announced sites and the country's grid
  capacity-build forecast, compute deliverable GW by the announced
  horizon year.
- `water.py` — given site geographies and water-rights / scarcity
  data per geography, compute the GW supportable by cooling water.
- `talent.py` — given announced site count and the country's
  qualified-FTE (data-center engineering, ML platform) supply
  forecast, compute the GW supportable by FTE.

### Aggregator (`src/sovereign_compute/scorecard/`)

- `aggregate.py` — given four `FeasibilityResult` per program,
  computes `projected_real_gw = min(...)` and selects the binding
  axis.
- `binding_constraint.py` — finds the lowest axis; flags
  `multiple_binding` when two or more axes are within 5% of the
  minimum.

### Renderer (`src/sovereign_compute/report/render.py`)

Reads scorecard JSON, writes:

- `reports/<year>-Q<n>-scorecard.md` — narrative + ranked table.
- `reports/<year>-Q<n>-scorecard.json` — machine-readable sidecar.

### Sanity bounds (`eval/sanity_bounds.py`)

Walks every scorecard record. Fails if any `projected_real_gw`
exceeds the program's `announced_gw`, if any axis is missing, or if
any program has fewer than three citations in `references[]`.

## Data model

```
ProgramSpec
  program_id (slug), country, program_name
  announced_gw, announced_horizon_year
  announced_accelerator_count
  announced_sites[]: { site_id, country, region, water_basin? }
  announced_funding_usd
  references[]: { url, retrieved_at, citation_text }

FeasibilityResult
  axis ∈ {silicon, power, water, talent}
  program_id
  projected_real_gw, confidence_low, confidence_high
  rationale_text, evidence_refs[]

Scorecard
  generated_at, input_data_hashes
  programs[]: {
    program_id, announced_gw, projected_real_gw, feasibility_ratio,
    binding_axis, per_axis_results[], notes
  }
```

## Input data files

- `data/silicon_allocations_2026q2.json` — per-vendor CoWoS / HBM
  share, with `source_url` on each entry.
- `data/grid_capacity_by_country.json` — per-country
  capacity-build forecasts.
- `data/water_basin_by_site.json` — per-announced-site water-basin
  status.
- `data/fte_supply_by_country.json` — per-country qualified-FTE
  forecast.

## Out of scope for spec 0001

- An interactive scorecard frontend.
- Predictions about future program changes.
- Country-specific advocacy.
- A live API. Operator runs the CLI.
