# core/reasoning.py

def epistemic_verdict(delta, baseline, ci=None, expected_direction="increase"):
    """
    Conservative, direction-aware epistemic judgment.
    """

    # Direction check
    signed_delta = delta if expected_direction == "increase" else -delta

    if signed_delta < 0:
        return "NEGATIVE RESULT — CONTRADICTS HYPOTHESIS"

    relative = signed_delta / max(abs(baseline), 1e-6)

    # CI check (if provided)
    if ci is not None:
        low, high = ci
        if high <= 0:
            return "NEGATIVE RESULT — CI EXCLUDES POSITIVE EFFECT"
        if low <= 0 <= high:
            return "WEAK SIGNAL — CI OVERLAPS ZERO"

    if relative < 0.05:
        return "NO MEANINGFUL EFFECT"
    elif relative < 0.15:
        return "WEAK SIGNAL — INCONCLUSIVE"
    elif relative < 0.30:
        return "MODERATE SIGNAL — REQUIRES REPLICATION"
    else:
        return "STRONG SIGNAL — CONDITIONAL SUPPORT"
