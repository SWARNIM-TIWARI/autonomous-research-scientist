# ui/dashboard.py
import json
import os
import streamlit as st
from pyvis.network import Network

RUN_PATH = "runs/run_latest.json"

st.set_page_config(page_title="Adaptive Reasoning System Dashboard", layout="wide")

if not os.path.exists(RUN_PATH):
    st.error(f"No JSON run file found at {RUN_PATH}")
    st.stop()

with open(RUN_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

st.title("Adaptive Reasoning System (ARS) Dashboard")
st.write(f"Run ID: {data['run_id']}")
st.write(f"Timestamp: {data['timestamp']}")
st.write(f"Papers ingested: {data['papers_ingested']}")

# -----------------------------
# Build PyVis network
# -----------------------------
net = Network(height="750px", width="100%", notebook=False, directed=True)
net.force_atlas_2based(gravity=-50)  # auto-layout

# Add nodes
for a in data["assumptions"]:
    net.add_node(
        a["id"],
        label=a["text"][:50] + ("..." if len(a["text"])>50 else ""),
        title=a["text"],
        color="#FFA500",  # orange for assumptions
        x=-300  # left
    )

for h in data["hypotheses"]:
    net.add_node(
        h["id"],
        label=h["text"][:50] + ("..." if len(h["text"])>50 else ""),
        title=h["text"],
        color="#00BFFF",  # blue for hypotheses
        x=300  # right
    )

# Add edges with semantic similarity weights
for h in data["hypotheses"]:
    for rel in h.get("related_assumptions", []):
        weight = rel.get("weight", 0.5)
        net.add_edge(
            rel["id"],
            h["id"],
            value=weight*10,  # thicker edge for higher similarity
            title=f"Weight: {weight:.2f}"
        )

# Physics layout for no overlaps, smooth
net.repulsion(node_distance=150, central_gravity=0.1,
              spring_length=200, spring_strength=0.05,
              damping=0.09)

# -----------------------------
# Render in Streamlit
# -----------------------------
net_path = os.path.join("runs", "run_network.html")
net.save_graph(net_path)

st.components.v1.html(open(net_path, "r", encoding="utf-8").read(), height=750, scrolling=True)
