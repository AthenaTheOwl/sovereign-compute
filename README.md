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


v0.1 shipped and runs end to end. `python -m sovereign_compute` shows the
committed scorecard; `python -m sovereign_compute scorecard` regenerates the
report and JSONL from the five program fixtures in `programs/`.

## try it

No arguments. Reads the committed `data/scorecards/2026q2.jsonl` and prints a
ranked summary, offline and read-only:

```
$ python -m sovereign_compute
sovereign AI compute feasibility - 2026q2
5 national programs scored on silicon / power / water / talent

rank program                            announced   real    gap binding
1    United Kingdom: AI Safety Instit..     0.80G  0.50  0.30 talent
2    European Union: AI Factories pro..     2.00G  1.10  0.90 talent
3    India: IndiaAI compute capacity        1.50G  0.80  0.70 silicon
4    United Arab Emirates: G42 AI com..     5.00G  1.90  3.10 water
5    Saudi Arabia: HUMAIN sovereign A..     6.00G  1.60  4.40 water

announced across all programs : 15.30 GW
projected real capacity       : 5.90 GW
phantom GW (announced - real) : 9.40 GW (61% of announced)

weakest program : Saudi Arabia: HUMAIN sovereign AI buildout (27% of announced is feasible, binding on water)
most common binding constraint : talent (2 of 5 programs)
```

The phantom-GW line is the point: across five announced national build-outs,
61% of the headline gigawatts disappear once silicon, power, water, and talent
limits are applied, and the table shows which constraint binds each program.

## How to run

```bash
python -m sovereign_compute            # show the committed scorecard (default)
python -m sovereign_compute scorecard  # regenerate the report + JSONL from fixtures
python -m sovereign_compute validate   # check committed scorecards stay within bounds
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
