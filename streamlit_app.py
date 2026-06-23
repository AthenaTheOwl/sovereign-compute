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

# ---------------------------------------------------------------------------
# Run the real feasibility engine live. This is not a viewer — the inputs below
# build a ProgramSpec and call sovereign_compute.scorecard.aggregate, the same
# function that produced the committed scorecard. Set announced GW and the four
# axis caps, watch feasibility and the binding constraint recompute.
# ---------------------------------------------------------------------------
st.divider()
st.subheader("score a program yourself")
st.caption(
    "drive the actual feasibility engine — `sovereign_compute.scorecard.aggregate` — "
    "with your own inputs. announced GW is the headline; the four axis caps are how "
    "much each constraint can actually deliver. the lowest cap binds."
)

try:
    import sys

    sys.path.insert(0, str(REPO / "src"))
    from sovereign_compute.models import ProgramSpec
    from sovereign_compute.scorecard import aggregate

    col_a, col_b = st.columns(2)
    with col_a:
        announced = st.number_input(
            "announced GW", min_value=0.1, max_value=50.0, value=5.0, step=0.5,
            help="headline figure the program announced",
        )
        silicon = st.slider(
            "silicon cap GW", 0.0, float(announced), min(1.0, float(announced)), step=0.1,
            help="accelerator-supply proxy: how much can actually be stood up",
        )
        power = st.slider(
            "power cap GW", 0.0, float(announced), min(3.0, float(announced)), step=0.1,
            help="grid-delivery proxy: how much can actually be energized",
        )
    with col_b:
        water = st.slider(
            "water cap GW", 0.0, float(announced), min(4.0, float(announced)), step=0.1,
            help="cooling-water proxy: usable campus footprint",
        )
        talent = st.slider(
            "talent cap GW", 0.0, float(announced), min(2.0, float(announced)), step=0.1,
            help="qualified-operations-staff proxy: ramp speed",
        )

    program = ProgramSpec(
        program_id="user-input",
        country="—",
        program_name="your program",
        announced_gw=announced,
        announced_horizon_year=2030,
        announced_accelerator_count=0,
        announced_funding_usd=0.0,
        references=["https://example/a", "https://example/b", "https://example/c"],
        silicon_gw=silicon,
        power_gw=power,
        water_gw=water,
        talent_gw=talent,
    )
    row = aggregate(program)
    feasible_pct = round(row.feasibility_ratio * 100)
    phantom_gw = round(announced - row.projected_real_gw, 2)

    m1, m2, m3 = st.columns(3)
    m1.metric("projected real", f"{row.projected_real_gw:,.2f} GW")
    m2.metric("phantom", f"{phantom_gw:,.2f} GW", help="announced minus projected-real")
    m3.metric("binding constraint", row.binding_constraint)

    if feasible_pct >= 70:
        st.success(
            f"{feasible_pct}% feasible — most announced capacity is deliverable. "
            f"binding axis: {row.binding_constraint}."
        )
    elif feasible_pct >= 40:
        st.warning(
            f"{feasible_pct}% feasible — meaningful phantom GW. {row.binding_constraint} "
            f"binds first at {row.projected_real_gw:,.2f} GW."
        )
    else:
        st.error(
            f"{feasible_pct}% feasible — mostly phantom. {row.binding_constraint} caps "
            f"delivery at {row.projected_real_gw:,.2f} GW of {announced:,.2f} announced."
        )

    st.dataframe(
        [
            {
                "axis": a.axis,
                "projected GW": round(a.projected_real_gw, 2),
                "conf low": round(a.confidence_low, 3),
                "conf high": round(a.confidence_high, 3),
                "rationale": a.rationale_text,
            }
            for a in row.axis_results
        ],
        use_container_width=True,
        hide_index=True,
    )
    st.caption(
        "lower any axis cap below the others and watch it become the binding "
        "constraint — it's the live engine, not a lookup."
    )
except Exception as exc:  # pragma: no cover - defensive for cloud import differences
    st.info(
        f"interactive scoring needs the package importable ({exc}). "
        "the committed scorecard above still renders."
    )

st.caption(
    "v0.1 ships one fixture quarter. the model + scoring live in "
    "`src/sovereign_compute/`; the table reads the committed "
    "`data/scorecards/*.jsonl` and the scorer above is the real engine. "
    "screening inputs for review, not policy advice. "
    "repo: github.com/AthenaTheOwl/sovereign-compute"
)
