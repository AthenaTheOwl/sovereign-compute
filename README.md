# sovereign-compute

Five governments announced 15.3 gigawatts of sovereign AI capacity. Run the numbers
against silicon, power, water, and talent and 9.4 of those gigawatts vanish — 61% of
the headline lives on a press release, not a wire.

## What it does

Every G20 government has put out a sovereign-AI compute plan since 2024. Most cannot
be built at the announced scale: CoWoS packaging is rationed, HBM is rationed,
transformers run years out, and a desert datacenter still needs water it does not
have. The announcements compete for the same scarce parts, and nobody has put the
programs in one table to see whose number survives contact with the supply chain.

sovereign-compute is that table. It takes a national program, scores its announced
capacity against four binding inputs — silicon, power, water, talent — and prints the
real gigawatts left over plus the one constraint that kills the rest. The UAE's G42
program loses 3.1 GW to water. Saudi HUMAIN loses 4.4 the same way, down to 27% of
what it announced. The UK and EU don't run out of grid or chips; they run out of
people. The program-shape data model and the cross-country comparison are the work
here. The per-axis numbers come from the sibling repos.

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

## live demo

An interactive Streamlit page wrapping the same `show` result: ranked programs, the
phantom-GW headline, and per-axis detail. It reads the committed
`data/scorecards/2026q2.jsonl` directly — no network, no secrets.

local:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

deploy on Streamlit Community Cloud -> New app -> repo
`AthenaTheOwl/sovereign-compute`, branch `main`, main file `streamlit_app.py`.

<!-- live url: https://<your-app>.streamlit.app -->

## How it connects

sovereign-compute sits on top of the per-axis models. It pulls their numbers and adds
the program shape and the country-by-country comparison.

- [grid-silicon](https://github.com/AthenaTheOwl/grid-silicon) — the power axis:
  announced-vs-energized megawatts on the actual grid.
- [wafer-to-watt](https://github.com/AthenaTheOwl/wafer-to-watt) — the silicon axis:
  how many of the announced chips the packaging line can actually deliver.
- [interconnect-alpha](https://github.com/AthenaTheOwl/interconnect-alpha) — queue
  survival: the odds a queued project ever reaches commercial operation.
- [robust-siting-lab](https://github.com/AthenaTheOwl/robust-siting-lab) — the
  optimization layer for where the capacity should actually go.

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
    feasibility/silicon.py        # consumes wafer-to-watt-style data
    feasibility/power.py          # consumes grid-silicon-style data
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
