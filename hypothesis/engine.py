# hypothesis/engine.py
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')  # small, fast, good for clustering

def generate_hypotheses(assumptions):
    """
    assumptions: list of dicts, each with 'id' and 'text'
    Returns: list of hypothesis dicts with related_assumptions
    """
    # Example hypotheses (can be extended)
    base_hypotheses = [
        {"id": f"h{i+1}", "text": f"Test hypothesis {i+1}", "related_assumptions": []}
        for i in range(4)
    ]

    # Compute embeddings for assumptions and hypotheses
    ass_texts = [a["text"] for a in assumptions]
    hyp_texts = [h["text"] for h in base_hypotheses]

    ass_emb = model.encode(ass_texts, convert_to_tensor=True)
    hyp_emb = model.encode(hyp_texts, convert_to_tensor=True)

    # Compute similarity and assign related_assumptions
    for hi, h in enumerate(base_hypotheses):
        sims = util.cos_sim(hyp_emb[hi], ass_emb)[0]  # similarity vector
        related = []
        for ai, score in enumerate(sims):
            if score >= 0.4:  # threshold for "related"
                related.append({
                    "id": assumptions[ai]["id"],
                    "weight": float(score)
                })
        h["related_assumptions"] = related

    return base_hypotheses
