from __future__ import annotations

import json
from pathlib import Path

from .models import ScorecardRow


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def render_report(path: Path, quarter: str, rows: list[ScorecardRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# SovereignCompute feasibility scorecard - {quarter}",
        "",
        "Fixture-backed scorecard comparing announced GW with the lowest feasible axis.",
        "The numbers are screening inputs for review, not policy advice.",
        "",
        "## ranked programs",
        "",
        "| rank | program | announced GW | projected GW | ratio | binding |",
        "|---:|---|---:|---:|---:|---|",
    ]
    for index, row in enumerate(rows, start=1):
        lines.append(
            f"| {index} | {row.country}: {row.program_name} | {row.announced_gw:.2f} | "
            f"{row.projected_real_gw:.2f} | {row.feasibility_ratio:.2f} | "
            f"{row.binding_constraint} |"
        )
    lines.extend(["", "## program notes", ""])
    for row in rows:
        axes = ", ".join(
            f"{item.axis} {item.projected_real_gw:.2f} GW" for item in row.axis_results
        )
        lines.extend(
            [
                f"### {row.program_name}",
                "",
                f"{row.country} has {row.announced_gw:.2f} GW announced and "
                f"{row.projected_real_gw:.2f} GW projected under the lowest axis. "
                f"Axis view: {axes}.",
                "",
                f"References: {', '.join(row.references[:3])}",
                "",
            ]
        )
    lines.extend(
        [
            "## methodology",
            "",
            "The scorecard takes the minimum of silicon, power, water, and talent axis estimates. "
            "If two axes sit within five percent of the minimum, the binding label becomes multiple.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

