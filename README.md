# SovereignCompute

Decision-support for sovereign AI compute programs. Shows the joint
silicon-power-water-talent feasibility of every announced national
AI-infrastructure build-out: UAE G42, Saudi HUMAIN, EU AI factories,
India IndiaAI Mission, UK AISI, and the others.

## What this is

Every G20 government announced a sovereign-AI compute plan in
2024-2026. Most are infeasible at announced scale given CoWoS, HBM,
transformer, and power-grid constraints. Nobody has produced a
credible cross-country comparison. Programs are mis-allocating
multi-billion-dollar budgets against schedules the supply chain
cannot meet.

SovereignCompute is the cross-country feasibility scorecard. The
first artifact is a public report: "Top 10 Sovereign AI Compute
Programs — Feasibility Scorecard" with announced GW, projected real
GW given silicon-power-water-talent inputs, and the binding constraint
per program.

It composes inputs from sibling repos (GridSilicon for grid-side,
WaferToWatt for silicon-side, InterconnectAlpha for queue survival,
RobustSiting for the optimization layer). What it adds is the
sovereign-program-shape data model and the cross-country comparison.

Buyers: program managers and procurement leads at sovereign AI
initiatives, defense planners, sovereign wealth fund infrastructure
teams, World Bank / IMF advisors to emerging-market AI strategies.

## Status

v0 scaffold. No implementation. The repo holds the README, the
license, the agents contract, the foundation spec, and the literal
first PR plan. The first runnable PR after this scaffold lands the
program schema and the feasibility-axis stubs against one fixture
program.

## How to run

Placeholder. After implementation lands:

```bash
uv run sovereign-compute scorecard \
  --programs programs/ \
  --out reports/2026-Q3-scorecard.md
```

## Layout

```
sovereign-compute/
  README.md
  LICENSE
  AGENTS.md
  .gitignore
  specs/
    0001-foundation/
      requirements.md          # R-SC-NNN
      design.md
      tasks.md
      acceptance.md
  docs/
    first-pr.md
```

Downstream additions:

```
  src/sovereign_compute/
    program/loader.py
    program/schema.py
    feasibility/silicon.py        # consumes WaferToWatt-style data
    feasibility/power.py          # consumes GridSilicon-style data
    feasibility/water.py
    feasibility/talent.py
    scorecard/aggregate.py
    scorecard/binding_constraint.py
    report/render.py
  schemas/
    program.schema.json
    feasibility_result.schema.json
    scorecard.schema.json
  programs/
    uae-g42.yaml
    saudi-humain.yaml
    eu-ai-factories.yaml
    indiaai.yaml
    uk-aisi.yaml
    france-mistral-cluster.yaml
    japan-keidanren.yaml
    canada-canadian-ai.yaml
    singapore-aisg.yaml
    korea-k-cloud.yaml
  data/
    silicon_allocations_2026q2.json
    grid_capacity_by_country.json
  reports/
    2026-Q3-scorecard.md
  eval/
    sanity_bounds.py              # no program > 100% of announced
```

## License

MIT. See [LICENSE](LICENSE).
