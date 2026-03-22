# experiments/evaluate.py
import matplotlib.pyplot as plt

def evaluate(results, plot=True):
    baseline = results["baseline"]
    treatment = results["treatment"]
    delta = treatment - baseline

    evaluation = {
        "baseline": baseline,
        "treatment": treatment,
        "delta": delta,
        "significant": delta > 0.05
    }

    if plot:
        plt.figure(figsize=(4,3))
        plt.bar(["Baseline", "Treatment"], [baseline, treatment], color=['gray','green'])
        plt.ylabel("Accuracy")
        plt.title("ARS Synthetic Experiment")
        plt.ylim(0,1)
        plt.show()

    return evaluation

# Test
if __name__ == "__main__":
    evaluate({"baseline":0.45,"treatment":0.53})