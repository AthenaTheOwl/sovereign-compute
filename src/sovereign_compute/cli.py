from __future__ import annotations

import argparse
import json
from pathlib import Path

from .loader import load_programs
from .report import render_report, write_jsonl
from .scorecard import build_scorecard
from .validation import validate_scorecard

ROOT = Path(__file__).resolve().parents[2]


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
    sub = parser.add_subparsers(dest="command", required=True)
    scorecard = sub.add_parser("scorecard")
    scorecard.add_argument("--quarter", default="2026q2")
    sub.add_parser("validate")
    args = parser.parse_args(argv)
    if args.command == "scorecard":
        paths = build(args.quarter)
        print(json.dumps({key: value.relative_to(ROOT).as_posix() for key, value in paths.items()}, sort_keys=True))
        return 0
    validate_all()
    print("valid: scorecards")
    return 0

