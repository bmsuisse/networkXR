---
title: Getting Started
---

# Getting Started

## Installation

networkXR requires **Python 3.12+** and includes a pre-compiled Rust extension.

=== "uv"

    ```bash
    uv add networkxr
    ```

=== "pip"

    ```bash
    pip install networkxr
    ```

### Build from Source

If you need to build from source (e.g., for development):

```bash
git clone https://github.com/bmsuisse/networkXR.git
cd networkXR
uv sync
uv run maturin develop --release
```

!!! note "Rust Toolchain Required"
    Building from source requires the [Rust toolchain](https://rustup.rs/) to be installed.

---

## Basic Usage

### Creating a Graph

```python
import networkxr as nx

G = nx.Graph()
```

### Adding Nodes

```python
# Single node
G.add_node(1)

# Multiple nodes
G.add_nodes_from([2, 3, 4])

# Node with attributes
G.add_node("server", role="backend", cpu=8)
```

### Adding Edges

```python
# Single edge
G.add_edge(1, 2)

# Multiple edges
G.add_edges_from([(2, 3), (3, 4)])

# Edge with attributes
G.add_edge(1, 3, weight=4.5)

# Weighted edges shorthand
G.add_weighted_edges_from([(1, 4, 2.0), (2, 4, 3.0)])
```

### Inspecting the Graph

```python
# Nodes and edges
print(G.number_of_nodes())  # 4
print(G.number_of_edges())  # 5
print(list(G.nodes()))      # [1, 2, 3, 4, 'server']
print(list(G.edges()))      # [(1, 2), (1, 3), ...]

# Neighbors and degree
print(list(G.neighbors(1)))  # [2, 3, 4]
print(G.degree(1))           # 3

# Edge data
print(G.get_edge_data(1, 3))  # {'weight': 4.5}
```

---

## Directed Graphs

```python
D = nx.DiGraph()
D.add_edges_from([("a", "b"), ("a", "c"), ("b", "c")])

# Directed-specific methods
print(list(D.successors("a")))    # ['b', 'c']
print(list(D.predecessors("c")))  # ['a', 'b']
print(D.in_degree("c"))           # 2
print(D.out_degree("a"))          # 2

# Reverse the graph
R = D.reverse()
print(list(R.successors("c")))    # ['a', 'b']

# Convert to undirected
U = D.to_undirected()
```

---

## Multi Graphs

```python
M = nx.MultiGraph()

# Parallel edges with auto-generated keys
M.add_edge(1, 2, weight=1.0)
M.add_edge(1, 2, weight=2.0)
M.add_edge(1, 2, weight=3.0)

# Edges with explicit keys
M.add_edge("a", "b", key="route1", distance=10)
M.add_edge("a", "b", key="route2", distance=15)

# Access edge data
print(M.get_edge_data(1, 2))  # {0: {'weight': 1.0}, 1: {'weight': 2.0}, ...}

# Directed multi graph
MD = nx.MultiDiGraph()
MD.add_edge("x", "y", key="fast", latency=5)
MD.add_edge("x", "y", key="slow", latency=50)
```

---

## Graph Generators

```python
# Classic graph generators
K5 = nx.complete_graph(5)
P10 = nx.path_graph(10)
C8 = nx.cycle_graph(8)
S6 = nx.star_graph(6)
B = nx.barbell_graph(5, 1)

# Empty graph
E = nx.empty_graph(10)
```

---

## Conversion & Relabeling

```python
# Convert to/from dict representations
dod = nx.to_dict_of_dicts(G)
G2 = nx.from_dict_of_dicts(dod)

dol = nx.to_dict_of_lists(G)
G3 = nx.from_dict_of_lists(dol)

# Relabel nodes
mapping = {1: "one", 2: "two", 3: "three"}
H = nx.relabel_nodes(G, mapping)

# Convert labels to integers
H_int = nx.convert_node_labels_to_integers(G)
```

---

## Migrating from NetworkX

networkXR is designed as a drop-in replacement. In most cases, you only need to change the import:

```diff
-import networkx as nx
+import networkxr as nx
```

!!! warning "API Coverage"
    networkXR implements a core subset of the NetworkX API. Advanced algorithms (shortest paths, centrality, community detection, etc.) are not yet available. Check the [API Reference](api/graph.md) for the full list of supported methods.
