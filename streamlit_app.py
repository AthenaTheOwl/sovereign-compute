"""sovereign-compute — live demo (Streamlit Community Cloud).

Reads the committed scorecard under data/scorecards/2026q2.jsonl and shows the
same ranked feasibility result as `python -m sovereign_compute` (the no-arg show
verb): announced GW versus projected-real GW per national AI compute program,
the phantom-GW gap, and the binding constraint (silicon / power / water / talent).
No network, no secrets — runs entirely off the committed JSONL.

Deploy: Streamlit Community Cloud -> New app -> repo AthenaTheOwl/sovereign-compute,
branch main, main file streamlit_app.py.
"""
from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

REPO = Path(__file__).resolve().parent
SCORECARDS = REPO / "data" / "scorecards"


def load_rows() -> tuple[list[dict], str]:
    files = sorted(SCORECARDS.glob("*.jsonl"))
    if not files:
        return [], ""
    latest = files[-1]
    rows = [
        json.loads(line)
        for line in latest.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    return rows, latest.stem


st.set_page_config(page_title="sovereign-compute — feasibility scorecard", layout="wide")
st.title("sovereign-compute")
st.caption(
    "how much announced sovereign AI compute is actually feasible once silicon, "
    "power, water, and talent limits are applied — and which constraint binds each program."
)

rows, quarter = load_rows()
if not rows:
    st.warning("no scorecard found under data/scorecards/*.jsonl")
    st.stop()

rows.sort(key=lambda r: r.get("feasibility_ratio", 0), reverse=True)

st.subheader(f"national AI compute programs — {quarter}")

total_announced = sum(r.get("announced_gw", 0) for r in rows)
total_projected = sum(r.get("projected_real_gw", 0) for r in rows)
phantom = total_announced - total_projected
phantom_pct = (phantom / total_announced * 100) if total_announced else 0

c1, c2, c3 = st.columns(3)
c1.metric("announced", f"{total_announced:,.2f} GW")
c2.metric("projected real", f"{total_projected:,.2f} GW")
c3.metric(
    "phantom",
    f"{phantom:,.2f} GW",
    delta=f"{phantom_pct:.0f}% of announced",
    delta_color="inverse",
    help="announced minus projected-real, summed across all programs",
)

constraints = sorted({r.get("binding_constraint", "?") for r in rows})
pick = st.selectbox(
    "filter by binding constraint",
    ["all"] + constraints,
    help="show only programs whose lowest feasible axis is this constraint",
)
shown = [r for r in rows if pick == "all" or r.get("binding_constraint") == pick]

st.dataframe(
    [
        {
            "rank": i,
            "program": f"{r.get('country')}: {r.get('program_name')}",
            "announced GW": round(r.get("announced_gw", 0), 2),
            "projected GW": round(r.get("projected_real_gw", 0), 2),
            "gap GW": round(r.get("announced_gw", 0) - r.get("projected_real_gw", 0), 2),
            "feasible %": round(r.get("feasibility_ratio", 0) * 100),
            "binding": r.get("binding_constraint"),
        }
        for i, r in enumerate(shown, start=1)
    ],
    use_container_width=True,
    hide_index=True,
)

worst = min(rows, key=lambda r: r.get("feasibility_ratio", 1))
constraint_counts: dict[str, int] = {}
for r in rows:
    key = r.get("binding_constraint", "?")
    constraint_counts[key] = constraint_counts.get(key, 0) + 1
top_constraint = max(constraint_counts.items(), key=lambda kv: kv[1])

st.info(
    f"**{phantom_pct:.0f}% of announced gigawatts are phantom** across {len(rows)} programs. "
    f"weakest: {worst.get('country')}: {worst.get('program_name')} — only "
    f"{worst.get('feasibility_ratio', 0) * 100:.0f}% feasible, binding on "
    f"{worst.get('binding_constraint')}. most common binding constraint: "
    f"{top_constraint[0]} ({top_constraint[1]} of {len(rows)} programs)."
)

with st.expander("per-axis detail (silicon / power / water / talent)"):
    program_names = [f"{r.get('country')}: {r.get('program_name')}" for r in shown]
    if program_names:
        chosen = st.selectbox("program", program_names, key="axis_program")
        row = shown[program_names.index(chosen)]
        st.dataframe(
            [
                {
                    "axis": a.get("axis"),
                    "projected GW": round(a.get("projected_real_gw", 0), 2),
                    "conf low": round(a.get("confidence_low", 0), 3),
                    "conf high": round(a.get("confidence_high", 0), 3),
                    "rationale": a.get("rationale_text"),
                }
                for a in row.get("axis_results", [])
            ],
            use_container_width=True,
            hide_index=True,
        )
        st.caption("references: " + ", ".join(row.get("references", [])))

st.caption(
    "v0.1 ships one fixture quarter. the model + scoring live in "
    "`src/sovereign_compute/`; this page reads the committed "
    "`data/scorecards/*.jsonl`. screening inputs for review, not policy advice. "
    "repo: github.com/AthenaTheOwl/sovereign-compute"
)
