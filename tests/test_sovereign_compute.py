from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from src.sovereign_compute.cli import format_show
from src.sovereign_compute.loader import load_programs
from src.sovereign_compute.report import render_report
from src.sovereign_compute.scorecard import axis_results, build_scorecard
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


# Characterization tests below pin the current output of the engine to the values it
# produces from the committed 2026q2 fixture, so a flipped sign/operator fails the gate.


def test_format_show_phantom_headline_is_announced_minus_projected() -> None:
    out = format_show("2026q2")
    # totals from fixture: announced 15.30, projected 5.90, phantom 9.40 (61% of announced)
    assert "announced across all programs : 15.30 GW" in out
    assert "projected real capacity       : 5.90 GW" in out
    assert "phantom GW (announced - real) : 9.40 GW (61% of announced)" in out


def test_format_show_weakest_is_lowest_feasibility_program() -> None:
    out = format_show("2026q2")
    # lowest feasibility_ratio in the fixture is Saudi Arabia: HUMAIN at 0.267 -> 27%
    assert (
        "weakest program : Saudi Arabia: HUMAIN sovereign AI buildout "
        "(27% of announced is feasible, binding on water)"
    ) in out


def test_format_show_most_common_binding_constraint_tally() -> None:
    out = format_show("2026q2")
    # binding constraints in fixture: talent x2, silicon x1, water x2; max picks talent (first)
    assert "most common binding constraint : talent (2 of 5 programs)" in out


def test_feasibility_ratio_equals_projected_over_announced() -> None:
    # build live so a +0.1 shift in the ratio (which preserves sort order) is caught here
    rows = build_scorecard(load_programs(ROOT / "programs"))
    for row in rows:
        expected = round(row.projected_real_gw / row.announced_gw, 3)
        assert row.feasibility_ratio == expected


def test_axis_result_confidence_bands() -> None:
    programs = {p.program_id: p for p in load_programs(ROOT / "programs")}
    program = programs["sc-uk-aisi"]
    for axis in axis_results(program):
        value = axis.projected_real_gw
        assert axis.confidence_low == round(value * 0.85, 3)
        assert axis.confidence_high == round(min(program.announced_gw, value * 1.15), 3)


def test_render_report_ratio_column_matches_rows(tmp_path) -> None:
    rows = build_scorecard(load_programs(ROOT / "programs"))
    report_path = tmp_path / "check-scorecard.md"
    render_report(report_path, "2026q2", rows)
    text = report_path.read_text(encoding="utf-8")
    for index, row in enumerate(rows, start=1):
        line = (
            f"| {index} | {row.country}: {row.program_name} | {row.announced_gw:.2f} | "
            f"{row.projected_real_gw:.2f} | {row.feasibility_ratio:.2f} | "
            f"{row.binding_constraint} |"
        )
        assert line in text

