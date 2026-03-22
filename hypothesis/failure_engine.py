def generate_alternatives(negative_hypotheses):
    new = []
    for h in negative_hypotheses:
        new.append(
            f"Relaxing or reversing intervention in: {h}"
        )
    return new
