# core/schemas.py
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

# -------------------------
# Core Specs
# -------------------------
@dataclass
class InterventionSpec:
    intervention_type: str
    baseline_method: str
    treatment_method: str
    metric: str
    risk_level: float
    expected_direction: str

@dataclass
class HypothesisResult:
    hypothesis: str
    intervention: InterventionSpec
    baseline: float
    treatment: float
    delta: float
    ci: Optional[Tuple[float, float]]
    verdict: str
    cost: Dict[str, Any]

@dataclass
class ARSRun:
    run_id: str
    timestamp: str
    assumptions: List[str]
    hypotheses: List[str]
    results: List[HypothesisResult]
    notes: Dict[str, Any]

    # -------------------------
    # Serialization
    # -------------------------
    def to_dict(self):
        return {
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "assumptions": self.assumptions,
            "hypotheses": self.hypotheses,
            "results": [asdict(r) for r in self.results],
            "notes": self.notes
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ARSRun":
        results = []

        for r in data.get("results", []):
            # Backward compatibility for old runs
            intervention_data = r.get("intervention", {
                "intervention_type": "unknown",
                "baseline_method": "unknown",
                "treatment_method": "unknown",
                "metric": "accuracy",
                "risk_level": 0.0,
                "expected_direction": "increase"
            })

            results.append(
                HypothesisResult(
                    hypothesis=r.get("hypothesis", "UNKNOWN"),
                    intervention=InterventionSpec(**intervention_data),
                    baseline=r.get("baseline", 0.0),
                    treatment=r.get("treatment", 0.0),
                    delta=r.get("delta", 0.0),
                    ci=tuple(r["ci"]) if r.get("ci") else None,
                    verdict=r.get("verdict", "UNKNOWN"),
                    cost=r.get("cost", {})
                )
            )

        return ARSRun(
            run_id=data["run_id"],
            timestamp=data["timestamp"],
            assumptions=data.get("assumptions", []),
            hypotheses=data.get("hypotheses", []),
            results=results,
            notes=data.get("notes", {})
        )

# -------------------------
# Helpers
# -------------------------
def new_run_id(prefix="run") -> str:
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}"

def now() -> str:
    return datetime.utcnow().isoformat() + "Z"
