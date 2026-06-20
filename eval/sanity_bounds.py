from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.sovereign_compute.validation import validate_scorecard  # noqa: E402


def main() -> int:
    for path in (ROOT / "data" / "scorecards").glob("*.jsonl"):
        validate_scorecard(path)
    print("sanity_bounds OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

