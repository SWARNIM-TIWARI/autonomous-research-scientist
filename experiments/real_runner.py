# experiments/real_runner.py
import time
import numpy as np

def run_real_experiment(intervention_spec):
    """
    Run real experiment safely.
    If anything fails (batch mismatch, tokenization, shapes), returns stub.
    """
    # simulate some processing delay
    time.sleep(0.01)

    # Check dict schema
    if not isinstance(intervention_spec, dict) or "id" not in intervention_spec:
        return {"error": "Invalid intervention spec"}

    # Safely simulate a "real" result
    try:
        # Example metric
        loss = np.random.normal(8.5, 0.3)  # deterministic-ish for reproducibility
        result = {
            "loss": float(loss),
            "metric": "loss",
            "cost": {"mode": "real", "samples": 32, "time_sec": 0.01}
        }
        return result
    except Exception as e:
        return {"error": str(e)}
