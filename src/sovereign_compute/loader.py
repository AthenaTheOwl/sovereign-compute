from __future__ import annotations

import json
from pathlib import Path

from .models import ProgramSpec


def load_programs(path: Path) -> list[ProgramSpec]:
    programs: list[ProgramSpec] = []
    for item in sorted(path.glob("*.json")):
        data = json.loads(item.read_text(encoding="utf-8"))
        if len(data.get("references", [])) < 3:
            raise ValueError(f"{item} has fewer than three references")
        programs.append(ProgramSpec(**data))
    if not programs:
        raise ValueError(f"no program specs under {path}")
    return programs

