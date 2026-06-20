from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ProgramSpec:
    program_id: str
    country: str
    program_name: str
    announced_gw: float
    announced_horizon_year: int
    announced_accelerator_count: int
    announced_funding_usd: float
    references: list[str]
    silicon_gw: float
    power_gw: float
    water_gw: float
    talent_gw: float


@dataclass(frozen=True)
class AxisResult:
    axis: str
    program_id: str
    projected_real_gw: float
    confidence_low: float
    confidence_high: float
    rationale_text: str
    evidence_refs: list[str]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class ScorecardRow:
    program_id: str
    country: str
    program_name: str
    announced_gw: float
    projected_real_gw: float
    feasibility_ratio: float
    binding_constraint: str
    multiple_binding: bool
    axis_results: list[AxisResult]
    references: list[str]

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["axis_results"] = [item.to_dict() for item in self.axis_results]
        return payload

