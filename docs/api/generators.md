---
title: Graph Generators
---

# Graph Generators

Classic graph generators available in `networkxr.generators.classic`. All are also accessible directly from `networkxr`.

---

## `empty_graph`

```python
nx.empty_graph(n=0, create_using=None) -> Graph
```

Return a graph with `n` nodes and zero edges.

```python
import networkxr as nx

G = nx.empty_graph(5)
print(G.number_of_nodes())  # 5
print(G.number_of_edges())  # 0
```

---

## `path_graph`

```python
nx.path_graph(n, create_using=None) -> Graph
```

Return a path graph `P_n` — `n` nodes connected linearly: `0-1-2-..-(n-1)`.

```python
P = nx.path_graph(5)
print(list(P.edges()))  # [(0,1), (1,2), (2,3), (3,4)]
```

---

## `cycle_graph`

```python
nx.cycle_graph(n, create_using=None) -> Graph
```

Return a cycle graph `C_n` — like a path graph with an additional edge from `n-1` to `0`.

```python
C = nx.cycle_graph(5)
print(list(C.edges()))  # [(0,1), (1,2), (2,3), (3,4), (4,0)]
```

---

## `complete_graph`

```python
nx.complete_graph(n, create_using=None) -> Graph
```

Return the complete graph `K_n` — every pair of nodes has an edge.

```python
K = nx.complete_graph(4)
print(K.number_of_edges())  # 6
```

---

## `star_graph`

```python
nx.star_graph(n, create_using=None) -> Graph
```

Return a star graph with `n+1` nodes: center node `0` connected to nodes `1` through `n`.

```python
S = nx.star_graph(5)
print(S.degree(0))  # 5
print(S.degree(1))  # 1
```

---

## `barbell_graph`

```python
nx.barbell_graph(m1, m2, create_using=None) -> Graph
```

Return a barbell graph: two complete graphs `K_{m1}` connected by a path of `m2` nodes.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `m1` | `int` | Size of each clique (must be ≥ 2) |
| `m2` | `int` | Length of the connecting path (must be ≥ 0) |

```python
B = nx.barbell_graph(5, 1)
print(B.number_of_nodes())  # 11
```

---

## `create_using` Parameter

All generators accept a `create_using` parameter to specify the graph type:

```python
# Create as directed graph
D = nx.path_graph(5, create_using=nx.DiGraph)

# Use existing graph instance (clears it first)
G = nx.Graph(name="my graph")
nx.cycle_graph(5, create_using=G)
```
