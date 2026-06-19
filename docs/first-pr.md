# First PR after the scaffold

Branch: `feat/0001-program-schema`

## Scope

Land the package skeleton, the program JSON schema, the program
loader, and three seed program YAMLs with proper citations.

### Files added

- `pyproject.toml` — declares `sovereign-compute`, CLI entry
  `sovereign-compute = "sovereign_compute.cli:main"`, dev deps
  (pytest, jsonschema, pyyaml, click).
- `src/sovereign_compute/__init__.py` — `__version__ = "0.0.1"`.
- `src/sovereign_compute/cli.py` — Click app with `version` command.
- `src/sovereign_compute/program/__init__.py`
- `src/sovereign_compute/program/schema.py` — dataclasses for
  `ProgramSpec`, `SiteRef`, `Reference`.
- `src/sovereign_compute/program/loader.py` —
  `load_programs(directory)` returns `list[ProgramSpec]`.
- `schemas/program.schema.json` — per R-SC-002.
- `programs/uae-g42.yaml` — with at least three references to
  primary G42 / UAE government announcements.
- `programs/saudi-humain.yaml` — with at least three references to
  HUMAIN / PIF announcements.
- `programs/eu-ai-factories.yaml` — with at least three references
  to the EuroHPC JU and EC announcements.
- `tests/test_program_loader.py` — three tests: all three seed
  programs load and validate, a malformed YAML raises, a YAML with
  zero references fails citation count check.
- `decisions/DEC-SC-001-axis-rubric.md` — names how each of the four
  feasibility axes converts inputs into a GW number, and where the
  rubric is borrowed from RobustSiting.

### Files NOT touched

- `src/sovereign_compute/feasibility/` — empty until PR 2.
- `src/sovereign_compute/scorecard/` — empty until PR 2.
- `src/sovereign_compute/report/` — empty until PR 3.
- `data/` — empty until PR 2.
- `reports/` — empty until PR 3.
- `eval/` — empty until PR 3.

## Verification

```bash
uv pip install -e .[dev]
python -m sovereign_compute version
# expect: sovereign-compute 0.0.1

uv run pytest
# expect: 3 tests in tests/test_program_loader.py pass

python -c "
from sovereign_compute.program.loader import load_programs
ps = load_programs('programs/')
for p in ps:
    print(p.program_id, p.country, p.announced_gw, len(p.references))
"
# expect: 3 programs printed, each with >= 3 references
```

## Out of scope for this PR

- The feasibility axis modules.
- The aggregator or binding-constraint logic.
- The report renderer.
- The voice_lint and sanity-bounds scripts.
- Any actual scoring or numeric output.
