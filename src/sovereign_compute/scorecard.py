from __future__ import annotations

from .models import AxisResult, ProgramSpec, ScorecardRow


def axis_results(program: ProgramSpec) -> list[AxisResult]:
    raw = {
        "silicon": (program.silicon_gw, "accelerator supply proxy limits initial buildout"),
        "power": (program.power_gw, "grid delivery proxy caps energized capacity"),
        "water": (program.water_gw, "cooling-water proxy caps usable campus footprint"),
        "talent": (program.talent_gw, "qualified operations staff proxy limits ramp speed"),
    }
    results: list[AxisResult] = []
    for axis, (value, rationale) in raw.items():
        results.append(
            AxisResult(
                axis=axis,
                program_id=program.program_id,
                projected_real_gw=round(value, 3),
                confidence_low=round(value * 0.85, 3),
                confidence_high=round(min(program.announced_gw, value * 1.15), 3),
                rationale_text=rationale,
                evidence_refs=program.references[:3],
            )
        )
    return results


def aggregate(program: ProgramSpec) -> ScorecardRow:
    results = axis_results(program)
    minimum = min(item.projected_real_gw for item in results)
    close_axes = [
        item.axis
        for item in results
        if abs(item.projected_real_gw - minimum) <= max(0.05 * minimum, 0.01)
    ]
    binding = "multiple" if len(close_axes) > 1 else close_axes[0]
    projected = minimum
    return ScorecardRow(
        program_id=program.program_id,
        country=program.country,
        program_name=program.program_name,
        announced_gw=program.announced_gw,
        projected_real_gw=projected,
        feasibility_ratio=round(projected / program.announced_gw, 3),
        binding_constraint=binding,
        multiple_binding=len(close_axes) > 1,
        axis_results=results,
        references=program.references,
    )


def build_scorecard(programs: list[ProgramSpec]) -> list[ScorecardRow]:
    return sorted(
        (aggregate(program) for program in programs),
        key=lambda row: row.feasibility_ratio,
        reverse=True,
    )

