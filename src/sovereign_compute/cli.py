from __future__ import annotations

import argparse
import json
from pathlib import Path

from .loader import load_programs
from .report import render_report, write_jsonl
from .scorecard import build_scorecard
from .validation import read_jsonl, validate_scorecard

ROOT = Path(__file__).resolve().parents[2]


def format_show(quarter: str) -> str:
    """Read the committed scorecard JSONL and render a ranked, readable summary."""
    path = ROOT / "data" / "scorecards" / f"{quarter}.jsonl"
    if not path.is_file():
        return f"no scorecard found for {quarter}; run: sovereign-compute scorecard"
    rows = read_jsonl(path)
    rows.sort(key=lambda row: row["feasibility_ratio"], reverse=True)

    total_announced = sum(row["announced_gw"] for row in rows)
    total_projected = sum(row["projected_real_gw"] for row in rows)
    phantom = total_announced - total_projected

    lines = [
        f"sovereign AI compute feasibility - {quarter}",
        f"{len(rows)} national programs scored on silicon / power / water / talent",
        "",
        f"{'rank':<4} {'program':<34} {'announced':>9} {'real':>6} {'gap':>6} {'binding':<8}",
        f"{'-' * 4} {'-' * 34} {'-' * 9} {'-' * 6} {'-' * 6} {'-' * 8}",
    ]
    for index, row in enumerate(rows, start=1):
        name = f"{row['country']}: {row['program_name']}"
        if len(name) > 34:
            name = name[:32] + ".."
        gap = row["announced_gw"] - row["projected_real_gw"]
        lines.append(
            f"{index:<4} {name:<34} {row['announced_gw']:>8.2f}G "
            f"{row['projected_real_gw']:>5.2f} {gap:>5.2f} {row['binding_constraint']:<8}"
        )

    worst = min(rows, key=lambda row: row["feasibility_ratio"])
    constraints: dict[str, int] = {}
    for row in rows:
        constraints[row["binding_constraint"]] = constraints.get(row["binding_constraint"], 0) + 1
    top_constraint = max(constraints.items(), key=lambda item: item[1])

    lines.extend(
        [
            "",
            f"announced across all programs : {total_announced:.2f} GW",
            f"projected real capacity       : {total_projected:.2f} GW",
            f"phantom GW (announced - real) : {phantom:.2f} GW "
            f"({phantom / total_announced * 100:.0f}% of announced)",
            "",
            f"weakest program : {worst['country']}: {worst['program_name']} "
            f"({worst['feasibility_ratio'] * 100:.0f}% of announced is feasible, "
            f"binding on {worst['binding_constraint']})",
            f"most common binding constraint : {top_constraint[0]} "
            f"({top_constraint[1]} of {len(rows)} programs)",
        ]
    )
    return "\n".join(lines)


def build(quarter: str) -> dict[str, Path]:
    rows = build_scorecard(load_programs(ROOT / "programs"))
    scorecard_path = ROOT / "data" / "scorecards" / f"{quarter}.jsonl"
    report_path = ROOT / "reports" / f"{quarter}-scorecard.md"
    write_jsonl(scorecard_path, [row.to_dict() for row in rows])
    render_report(report_path, quarter, rows)
    validate_scorecard(scorecard_path)
    return {"scorecard_path": scorecard_path, "report_path": report_path}


def validate_all() -> None:
    for path in (ROOT / "data" / "scorecards").glob("*.jsonl"):
        validate_scorecard(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sovereign-compute")
    sub = parser.add_subparsers(dest="command")
    scorecard = sub.add_parser("scorecard")
    scorecard.add_argument("--quarter", default="2026q2")
    show = sub.add_parser("show", help="print the committed scorecard as a ranked summary")
    show.add_argument("--quarter", default="2026q2")
    sub.add_parser("validate")
    args = parser.parse_args(argv)
    if args.command == "scorecard":
        paths = build(args.quarter)
        print(json.dumps({key: value.relative_to(ROOT).as_posix() for key, value in paths.items()}, sort_keys=True))
        return 0
    if args.command in (None, "show"):
        quarter = getattr(args, "quarter", "2026q2")
        print(format_show(quarter))
        return 0
    validate_all()
    print("valid: scorecards")
    return 0

