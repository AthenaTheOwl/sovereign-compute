from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from src.sovereign_compute.loader import load_programs
from src.sovereign_compute.scorecard import build_scorecard
from src.sovereign_compute.validation import read_jsonl, validate_scorecard

ROOT = Path(__file__).resolve().parents[1]


def test_loads_five_programs_with_references() -> None:
    programs = load_programs(ROOT / "programs")
    assert len(programs) == 5
    assert all(len(program.references) >= 3 for program in programs)


def test_scorecard_binding_constraint_is_min_axis() -> None:
    rows = build_scorecard(load_programs(ROOT / "programs"))
    for row in rows:
        minimum = min(axis.projected_real_gw for axis in row.axis_results)
        assert row.projected_real_gw == minimum
        assert row.projected_real_gw <= row.announced_gw


def test_cli_writes_scorecard_and_report() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "sovereign_compute", "scorecard", "--quarter", "2026q2"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    scorecard = ROOT / payload["scorecard_path"]
    report = ROOT / payload["report_path"]
    assert scorecard.is_file()
    assert report.is_file()
    validate_scorecard(scorecard)


def test_scorecard_jsonl_has_ranked_rows() -> None:
    rows = read_jsonl(ROOT / "data" / "scorecards" / "2026q2.jsonl")
    ratios = [row["feasibility_ratio"] for row in rows]
    assert ratios == sorted(ratios, reverse=True)


def test_show_default_command_is_readable() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "sovereign_compute"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    out = result.stdout
    assert "feasibility" in out
    assert "phantom GW" in out
    assert "binding" in out
    # ranked table: highest-ratio program (UK, rank 1) appears before lowest (Saudi, rank 5)
    assert out.index("United Kingdom") < out.index("Saudi Arabia")
    # not a raw JSON dump
    assert not out.lstrip().startswith("{")

