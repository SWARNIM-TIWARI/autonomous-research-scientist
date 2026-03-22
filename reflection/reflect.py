# reflection/reflect.py

def reflect(result, knowledge_graph):
    verdict = result["verdict"]
    hypothesis = result["hypothesis"]

    knowledge_graph.record_result(hypothesis, verdict=result["verdict"], delta=result["delta"])

    print("[REFLECTION]")
    print(f"Hypothesis: {hypothesis}")
    print(f"Delta: {result['delta']}")
    print(f"Verdict: {verdict}")
