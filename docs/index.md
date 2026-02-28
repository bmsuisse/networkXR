---
title: networkXR — Rust-Powered Graph Computing
---

# networkXR

**A Rust-backed drop-in replacement for NetworkX.**

networkXR provides the familiar NetworkX API you already know, powered by a high-performance Rust core via PyO3. Get the same interface with dramatically faster graph operations.

---

## Key Features

<div class="grid cards" markdown>

- :material-lightning-bolt:{ .lg .middle } **Rust-Powered Performance**

    ---

    Core graph data structures (`Graph`, `DiGraph`) are implemented in Rust using `IndexMap` for insertion-order-preserving adjacency, exposed to Python via PyO3.

- :material-swap-horizontal:{ .lg .middle } **Drop-in Compatible**

    ---

    Same API as NetworkX — `add_node`, `add_edge`, `neighbors`, `degree`, `subgraph`, and more. Switch by changing one import.

- :material-graph:{ .lg .middle } **Full Graph Types**

    ---

    Supports undirected (`Graph`), directed (`DiGraph`), undirected multi (`MultiGraph`), and directed multi (`MultiDiGraph`) graphs.

- :material-tools:{ .lg .middle } **Batteries Included**

    ---

    Graph generators, converters, relabeling functions, and the full NetworkX exception hierarchy — all included.

</div>

---

## Quick Start

```python
import networkxr as nx

# Create a graph
G = nx.Graph()
G.add_edges_from([(1, 2), (2, 3), (3, 1)])

print(list(G.nodes()))   # [1, 2, 3]
print(list(G.edges()))   # [(1, 2), (1, 3), (2, 3)]
print(G.degree(1))       # 2

# Directed graph
D = nx.DiGraph()
D.add_edge("a", "b", weight=4.2)
print(list(D.successors("a")))  # ['b']
```

---

## Installation

=== "uv"

    ```bash
    uv add networkxr
    ```

=== "pip"

    ```bash
    pip install networkxr
    ```

---

## Why networkXR?

| Feature | NetworkX | networkXR |
|---------|----------|-----------|
| Language | Pure Python | Rust core + Python API |
| API | ✅ Full | ✅ Compatible subset |
| Graph types | Graph, DiGraph, Multi* | Graph, DiGraph, Multi* |
| Performance | Baseline | 🚀 Significantly faster |
| Drop-in replacement | — | ✅ Change one import |
