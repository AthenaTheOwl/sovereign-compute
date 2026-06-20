from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def validate_scorecard(path: Path) -> None:
    for row in read_jsonl(path):
        if row["projected_real_gw"] > row["announced_gw"]:
            raise ValueError(f"{row['program_id']} exceeds announced GW")
        if not row["binding_constraint"]:
            raise ValueError(f"{row['program_id']} missing binding constraint")
        if len(row["references"]) < 3:
            raise ValueError(f"{row['program_id']} has fewer than 3 references")

