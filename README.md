# 🔬 ARS — Autonomous Research Scientist

> 🚧 **Work in Progress** — core pipeline runs end-to-end. Several modules are actively being developed.

ARS is a pipeline that can read research papers, pull out key assumptions, suggest hypotheses, run experiments, and interpret results — mostly on its own. The goal is to see if a system can reason scientifically, not just perform computations.

---

## What It Does

Most machine learning systems focus on optimizing a metric. ARS tries a bigger question: given a set of scientific assumptions, which hypotheses should we test, and what do the results actually mean?

Currently, ARS can:

- Fetch papers from ArXiv or use local PDFs
- Extract assumptions from text
- Generate hypotheses and link them semantically
- Run experiments (simulated or real)
- Make evidence-based conclusions
- Visualize the reasoning process in a knowledge graph

---

## Architecture
```
ArXiv API / Local PDFs
         ↓
   ingestion/parser.py         # Extracts text and assumptions
         ↓
   hypothesis/engine.py        # Links assumptions → hypotheses
         ↓
   knowledge/graph.py          # Tracks assumptions, hypotheses, results
         ↓
   experiments/adapter.py      # Routes to simulation or real mode
         ↓
   core/reasoning.py           # Evaluates results and gives verdicts
         ↓
   reflection/reflect.py       # Stores results back in the graph
         ↓
   reports/generator.py + ui/dashboard.py
                                # Generates reports + interactive dashboard
```

---

## Features

- 📄 **ArXiv ingestion** — fetch papers automatically, fallback to local PDFs
- 🔍 **Assumption extraction** — pulls out key sentences from papers
- 🔗 **Hypothesis generation** — links assumptions to hypotheses using semantic embeddings
- 🧪 **Experiment modes** — simulation with statistical rigor or real (guarded) execution
- 📊 **Bootstrap confidence intervals** — quantifies uncertainty in results
- ⚖️ **Epistemic verdict engine** — categorizes results as Negative, No Effect, Weak, Moderate, or Strong Signal
- 🗂 **Knowledge graph** — directed graph tracking assumptions → hypotheses → results
- 🌐 **Interactive dashboard** — visualize the reasoning process using Streamlit + PyVis
- 💾 **JSON persistence** — saves each run for reproducibility

---

## Epistemic Verdicts

| Verdict | Condition |
|---|---|
| `NEGATIVE RESULT` | Effect contradicts hypothesis |
| `NO MEANINGFUL EFFECT` | Relative effect < 5% |
| `WEAK SIGNAL` | Relative effect 5–15% |
| `MODERATE SIGNAL` | Relative effect 15–30% |
| `STRONG SIGNAL` | Relative effect > 30% |

If the confidence interval overlaps zero, the verdict is automatically downgraded to Weak or Negative.

---

## 🛠 Tech Stack

| Category | Tools |
|---|---|
| **Ingestion** | feedparser, PyPDF2, requests |
| **Embeddings** | Sentence-Transformers (MiniLM) |
| **Statistics** | NumPy, bootstrap CI |
| **Knowledge Graph** | NetworkX |
| **UI** | Streamlit, PyVis |
| **Persistence** | JSON |
| **Core** | Python, dataclasses |

---

## 📂 Project Structure
```
ars/
├── main.py
├── core/
│   ├── schemas.py
│   └── reasoning.py
├── experiments/
│   ├── adapter.py
│   ├── config.py
│   ├── runner.py
│   ├── real_runner.py
│   └── evaluate.py
├── hypothesis/
│   ├── engine.py
│   └── failure_engine.py
├── ingestion/
│   ├── arxiv_utils.py
│   └── parser.py
├── knowledge/
│   └── graph.py
├── reflection/
│   └── reflect.py
├── reports/
│   └── generator.py
├── ui/
│   └── dashboard.py
├── runs/          # JSON outputs (gitignored)
└── papers/        # Downloaded PDFs (gitignored)
```

---

## ⚙️ Installation & Running
```bash
git clone https://github.com/SWARNIM-TIWARI/autonomous-research-scientist.git
cd autonomous-research-scientist
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python main.py
streamlit run ui/dashboard.py
```

---

## ⚠️ Current Limitations

- Hypothesis text is still a placeholder — semantic generation from paper content is in progress
- `real_runner.py` simulates real experiments — actual execution is not yet implemented
- `failure_engine.py` is a stub for alternative hypothesis generation
- Knowledge graph is not persistent across runs — it is rebuilt each session

---

## 🔭 Planned Development

- True hypothesis generation from extracted assumptions using LLMs
- Real experiment execution with model training
- Persistent knowledge graph across runs
- Automated literature review to trigger new hypotheses
- Multi-agent architecture for ingestion, reasoning, and reflection

---

## 📄 License

MIT License

---

*Built to explore whether a system can conduct scientific reasoning autonomously — not just run experiments, but decide what to test, interpret what it found, and know when it doesn't know.*
