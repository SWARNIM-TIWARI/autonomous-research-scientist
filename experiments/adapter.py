# experiments/adapter.py
from experiments.runner import run_simulation_experiment
from experiments.real_runner import run_real_experiment
from experiments.config import ExperimentMode

def execute_intervention(intervention_spec, mode: ExperimentMode):
    """
    Execute the intervention safely based on mode.
    Accepts intervention_spec as a dictionary.
    """
    if mode == ExperimentMode.SIMULATION:
        return run_simulation_experiment(intervention_spec)
    elif mode == ExperimentMode.REAL:
        return run_real_experiment(intervention_spec)
    else:
        raise ValueError(f"Unknown mode: {mode}")
