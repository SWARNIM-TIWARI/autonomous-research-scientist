# 🔬 ARS — Autonomous Research Scientist

An autonomous agent pipeline that ingests research papers, extracts assumptions, generates hypotheses, runs experiments with statistical rigor, and reasons epistemically about results — all without human intervention.

> 🚧 **Work in Progress** — core pipeline runs end-to-end. Several modules are actively being developed. Published to document architecture and direction.

---

## What It Does

Most ML systems optimize a metric. ARS asks a harder question: **given a set of scientific assumptions, what hypotheses should be tested, and what do the results actually mean?**

The system fetches papers from ArXiv, extracts assumptions from text, generates semantically linked hypotheses, runs simulation and real experiments, applies conservative epistemic verdicts, and visualizes the full reasoning graph — all autonomously.

---

## 🏗 Architecture

```
ArXiv API / Local PDFs
         ↓
   ingestion/parser.py
   (PDF text extraction + assumption mining)
         ↓
   hypothesis/engine.py
   (SentenceTransformer semantic linking)
         ↓
   knowledge/graph.py
   (NetworkX knowledge graph — assumptions → hypotheses)
         ↓
   experiments/adapter.py
   (Simulation mode / Real mode routing)
         ↓
   core/reasoning.py
   (Epistemic verdict — direction-aware, CI-aware)
         ↓
   reflection/reflect.py
   (Record result back into knowledge graph)
         ↓
   reports/generator.py + ui/dashboard.py
   (Text report + PyVis interactive network)
```

---

## 🚀 Features

- 📄 **ArXiv ingestion** — fetches and downloads papers via ArXiv API, falls back to local PDFs
- 🧠 **Assumption extraction** — regex-based mining of assumption and hypothesis sentences from paper text
- 🔗 **Semantic hypothesis generation** — MiniLM embeddings link assumptions to hypotheses via cosine similarity
- 🧪 **Dual experiment modes** — simulation (bootstrap CI, controlled noise) and real (guarded execution)
- 📊 **Bootstrap confidence intervals** — proper statistical uncertainty quantification, not just point estimates
- ⚖️ **Epistemic verdict engine** — 5-tier conservative judgment: Negative / No Effect / Weak / Moderate / Strong Signal
- 🗂 **Knowledge graph** — directed NetworkX graph tracking assumption → hypothesis → result lineage
- 🌐 **Interactive dashboard** — PyVis network visualization of the full reasoning graph in Streamlit
- 💾 **JSON run persistence** — every run saved with full lineage for reproducibility

---

## 🧪 Epistemic Verdict System

Rather than binary pass/fail, ARS applies direction-aware, CI-aware verdicts:

| Verdict | Condition |
|---|---|
| `NEGATIVE RESULT` | Effect contradicts hypothesis direction |
| `NO MEANINGFUL EFFECT` | Relative effect < 5% |
| `WEAK SIGNAL — INCONCLUSIVE` | Relative effect 5–15% |
| `MODERATE SIGNAL — REQUIRES REPLICATION` | Relative effect 15–30% |
| `STRONG SIGNAL — CONDITIONAL SUPPORT` | Relative effect > 30% |

CI overlap with zero automatically downgrades any verdict to Weak Signal or Negative.

---

## 🛠 Tech Stack

| Category | Tools |
|---|---|
| **Ingestion** | feedparser, PyPDF2, requests |
| **Embeddings** | Sentence-Transformers (MiniLM) |
| **Statistics** | NumPy, Bootstrap CI |
| **Knowledge Graph** | NetworkX |
| **UI** | Streamlit, PyVis |
| **Persistence** | JSON |
| **Core** | Python, dataclasses |

---

## 📂 Project Structure

```
ars/
├── main.py                  # Entry point — full pipeline
├── core/
│   ├── schemas.py           # ARSRun, HypothesisResult, InterventionSpec dataclasses
│   └── reasoning.py         # Epistemic verdict engine
├── experiments/
│   ├── adapter.py           # Mode routing — simulation vs real
│   ├── config.py            # ExperimentMode enum
│   ├── runner.py            # Simulation runner with bootstrap CI
│   ├── real_runner.py       # Real experiment runner (guarded)
│   └── evaluate.py          # Result evaluation + matplotlib plot
├── hypothesis/
│   ├── engine.py            # Semantic hypothesis generation
│   └── failure_engine.py    # Alternative generation for negative results
├── ingestion/
│   ├── arxiv_utils.py       # ArXiv API fetch + local PDF fallback
│   └── parser.py            # PDF text extraction + assumption mining
├── knowledge/
│   └── graph.py             # NetworkX knowledge graph
├── reflection/
│   └── reflect.py           # Records results back into knowledge graph
├── reports/
│   └── generator.py         # Text report generation
├── ui/
│   └── dashboard.py         # Streamlit + PyVis interactive dashboard
├── runs/                    # Auto-generated JSON run outputs (gitignored)
└── papers/                  # Downloaded ArXiv PDFs (gitignored)
```

---

## ⚙️ Installation & Running

1. **Clone the repository**

```bash
git clone https://github.com/SWARNIM-TIWARI/ars.git
cd ars
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the pipeline**

```bash
python main.py
```

5. **Launch the dashboard**

```bash
streamlit run ui/dashboard.py
```

---

## ⚠️ Current Limitations

These are documented intentionally:

- Hypothesis text is currently placeholder — semantic generation from actual paper content is in progress
- `real_runner.py` simulates a real experiment with controlled noise — true model execution not yet wired
- `failure_engine.py` is a stub — alternative hypothesis generation is planned
- ArXiv ingestion requires network access — local PDF fallback available
- No persistent knowledge graph across runs yet — graph is rebuilt each session

---

## 🔭 Planned Development

- True hypothesis generation from extracted assumption text using LLM
- Real model experiment execution with actual training loops
- Persistent knowledge graph with cross-run memory
- Automated literature review loop — new papers trigger new hypotheses
- LLM-powered reflection and alternative generation
- Multi-agent architecture — separate agents for ingestion, reasoning, and reflection

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

*Built to explore whether a system can conduct scientific reasoning autonomously — not just run experiments, but decide what to test, interpret what it found, and know when it doesn't know.*