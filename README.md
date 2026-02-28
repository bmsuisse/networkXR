# networkXR

> [!CAUTION]
> 🚧 **Under Heavy Construction** 🚧
>
> This project is in early development. APIs may change without notice. Not yet ready for production use.

## Goal

**networkXR** is a Rust-backed, drop-in replacement for [NetworkX](https://networkx.org/) — the popular Python library for graph creation, manipulation, and analysis.

By leveraging [PyO3](https://pyo3.rs/) and Rust's performance characteristics, networkXR aims to provide a **fully compatible NetworkX API** with significantly improved speed for compute-intensive graph operations, while remaining a seamless swap for existing Python codebases.

## Installation

```bash
pip install networkxr

# With interactive plotting support (optional)
pip install networkxr[plot]
```

## Quick Start

```python
# Just swap the import — everything else stays the same
import networkxr as nx

G = nx.Graph()
G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)])
G.add_node(5, role="isolated")

print(G.number_of_nodes())   # 5
print(G.number_of_edges())   # 5
print(list(G.neighbors(1)))  # [2, 3, 4]
```

## Plotting

networkXR natively supports **Plotly** for interactive graph visualization:

```python
import networkxr as nx

G = nx.barbell_graph(5, 1)
nx.draw(G, node_color="#6366f1", title="Barbell Graph")
```

Customise layout, colours, and export to HTML:

```python
G = nx.cycle_graph(12)

fig = nx.draw(
    G,
    layout="circular",
    node_color="#06b6d4",
    title="Cycle C₁₂",
    show=False,
)
fig.write_html("graph.html")
```

> **Note:** Plotting requires `plotly` — install with `pip install networkxr[plot]`.
