# reports/generator.py

def generate_report(run):
    lines = ["=== AUTONOMOUS RESEARCH SCIENTIST REPORT ===\n"]

    lines.append("Hypotheses & Results:")
    for r in run.results:
        lines.append(
            f"- {r.hypothesis}\n"
            f"  Δ={r.delta}, CI={r.ci} → {r.verdict}"
        )

    lines.append("\nEpistemic Policy:")
    lines.append(run.notes.get("epistemic_policy", "N/A"))

    return "\n".join(lines)
