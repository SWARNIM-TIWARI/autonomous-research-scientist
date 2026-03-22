# main.py
import json
import os
from datetime import datetime
from sentence_transformers import SentenceTransformer, util
import numpy as np
from experiments.adapter import execute_intervention, ExperimentMode

# -----------------------------
# CONFIG
# -----------------------------
RUNS_DIR = "runs"
os.makedirs(RUNS_DIR, exist_ok=True)
RUN_ID = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
RUN_PATH = os.path.join(RUNS_DIR, "run_latest.json")
DOMAIN = "synthetic reasoning"

# -----------------------------
# 1️⃣ Load assumptions (dict-only)
# -----------------------------
assumptions = [
    {"id": f"A{i+1}", "text": txt}
    for i, txt in enumerate([
        "Features are independent in the input data.",
        "Temporal coherence in the dataset is preserved.",
        "Data is IID over time.",
        "Model weights are properly initialized.",
        "Loss function is differentiable."
    ])
]
print(f"[INGESTION] Loaded {len(assumptions)} assumptions")

# -----------------------------
# 2️⃣ Generate hypotheses (SentenceTransformers)
# -----------------------------
def generate_hypotheses(assumptions, top_k=2):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [a["text"] for a in assumptions]
    embeddings = model.encode(texts, convert_to_tensor=True)
    
    hypotheses = []
    for i, a in enumerate(assumptions):
        # pick top_k most similar assumptions (excluding self)
        cos_scores = util.cos_sim(embeddings[i], embeddings)[0]
        related = []
        for j, score in enumerate(cos_scores):
            if i != j:
                related.append({"id": assumptions[j]["id"], "weight": float(score)})
        # keep top_k
        related = sorted(related, key=lambda x: x["weight"], reverse=True)[:top_k]

        hyp = {
            "id": f"H{i+1}",
            "text": f"Test hypothesis {i+1}",
            "related_assumptions": related
        }
        hypotheses.append(hyp)
    return hypotheses

hypotheses = generate_hypotheses(assumptions)
print(f"[HYPOTHESES] Generated {len(hypotheses)} hypotheses")

# -----------------------------
# 3️⃣ Run SIM experiments (always safe)
# -----------------------------
for h in hypotheses:
    print(f"\n[SIMULATION] Testing hypothesis: '{h['text']}'")
    sim_result = execute_intervention(h, ExperimentMode.SIMULATION)
    h["sim_result"] = sim_result
    print(f"SIM result: {sim_result}")

# -----------------------------
# 4️⃣ Attempt REAL experiments (guarded)
# -----------------------------
for h in hypotheses:
    print(f"\n[REAL] Running real experiment for hypothesis: '{h['text']}'")
    try:
        real_result = execute_intervention(h, ExperimentMode.REAL)
    except Exception as e:
        real_result = {"error": str(e)}
        print(f"[REAL] Experiment failed safely: {e}")
    h["real_result"] = real_result
    print(f"REAL result: {real_result}")

# -----------------------------
# 5️⃣ Save JSON for dashboard
# -----------------------------
run_data = {
    "run_id": RUN_ID,
    "timestamp": datetime.now().isoformat(),
    "domain": DOMAIN,
    "papers_ingested": len(assumptions),
    "assumptions": assumptions,
    "hypotheses": hypotheses
}

with open(RUN_PATH, "w", encoding="utf-8") as f:
    json.dump(run_data, f, indent=2)

print(f"\n[RUN SAVED] {RUN_PATH}")
print("[INFO] You can now run: streamlit run ui/dashboard.py")
