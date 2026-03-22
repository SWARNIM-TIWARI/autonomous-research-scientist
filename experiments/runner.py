# experiments/runner.py
import numpy as np

def bootstrap_ci(samples, n=1000, alpha=0.05):
    boots = np.random.choice(samples, (n, len(samples)), replace=True).mean(axis=1)
    low = np.percentile(boots, 100 * alpha / 2)
    high = np.percentile(boots, 100 * (1 - alpha / 2))
    return round(low, 4), round(high, 4)

def baseline_run(seed=42, size=30):
    rng = np.random.default_rng(seed)
    return rng.normal(0.50, 0.03, size=size)

def treatment_run(risk_level, seed=42, size=30):
    rng = np.random.default_rng(seed)
    true_effect = rng.normal(0.1 * (1 - risk_level), 0.05, size=size)
    baseline = rng.normal(0.50, 0.03, size=size)
    return baseline + true_effect

def run_simulation_experiment(intervention):
    risk_level = intervention.get('risk_level', 0.5)
    size = intervention.get('size', 30)

    baseline_samples = baseline_run(size=size)
    treatment_samples = treatment_run(risk_level=risk_level, size=size)

    baseline = baseline_samples.mean()
    treatment = treatment_samples.mean()
    delta = treatment - baseline
    ci = bootstrap_ci(treatment_samples - baseline_samples)

    return {
        "baseline": round(baseline, 4),
        "treatment": round(treatment, 4),
        "delta": round(delta, 4),
        "ci": ci,
        "metric": "accuracy",
        "cost": {"mode": "simulation", "samples": size, "time_sec": 0.01}
    }
