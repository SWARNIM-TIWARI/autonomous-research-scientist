import networkx as nx
from core.schemas import InterventionSpec

class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_assumption(self, assumption: str, paper_id=None):
        self.graph.add_node(
            assumption,
            type="assumption",
            paper_id=paper_id,
            label=assumption
        )

    def add_hypothesis(self, hypothesis: str):
        self.graph.add_node(
            hypothesis,
            type="hypothesis",
            tested=False,
            verdict=None,
            confidence=None,
            label=hypothesis
        )

    def link(self, assumption: str, hypothesis: str):
        self.add_assumption(assumption)
        self.add_hypothesis(hypothesis)
        self.graph.add_edge(assumption, hypothesis, relation="tests")

    def record_result(self, hypothesis: str, verdict: str, delta: float):
        if hypothesis in self.graph.nodes:
            self.graph.nodes[hypothesis]["tested"] = True
            self.graph.nodes[hypothesis]["verdict"] = verdict
            self.graph.nodes[hypothesis]["confidence"] = delta

    def create_dummy_intervention(self, hypothesis_text: str) -> InterventionSpec:
        """
        Returns a placeholder intervention object for testing.
        """
        return InterventionSpec(
            intervention_type="perturbation",
            baseline_method="baseline",
            treatment_method="treatment",
            metric="metric",
            risk_level=0.1,
            expected_direction="increase"
        )

