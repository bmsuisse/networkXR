---
title: DiGraph
---

# DiGraph

`networkxr.DiGraph` — a directed simple graph.

Implemented in **Rust** via PyO3. Maintains both forward (`succ`) and reverse (`pred`) adjacency maps for O(1) predecessor lookups. Self-loops are allowed but parallel edges are not — use [`MultiDiGraph`](multigraph.md) for that.

---

## Constructor

```python
DiGraph(incoming_graph_data=None, **attr)
```

Create a directed graph.

```python
import networkxr as nx

D = nx.DiGraph()
D = nx.DiGraph([(1, 2), (2, 3)])
D = nx.DiGraph({1: {2: {"weight": 1.0}}})
```

---

## Adding & Removing

### `add_node`

```python
D.add_node(node_for_adding, **attr)
```

### `add_nodes_from`

```python
D.add_nodes_from(nodes_for_adding, **attr)
```

### `remove_node`

```python
D.remove_node(n)
```

Remove node `n` and all incident edges (both in and out).

### `add_edge`

```python
D.add_edge(u_of_edge, v_of_edge, **attr)
```

Add a directed edge from `u` to `v`. Nodes are auto-created.

### `add_edges_from`

```python
D.add_edges_from(ebunch_to_add, **attr)
```

### `add_weighted_edges_from`

```python
D.add_weighted_edges_from(ebunch_to_add, weight="weight")
```

### `remove_edge`

```python
D.remove_edge(u, v)
```

---

## Directed Queries

### `successors`

```python
D.successors(n) -> list
```

Return a list of successor nodes of `n` (nodes reachable via outgoing edges).

```python
D.add_edges_from([("a", "b"), ("a", "c")])
D.successors("a")  # ['b', 'c']
```

### `predecessors`

```python
D.predecessors(n) -> list
```

Return a list of predecessor nodes of `n` (nodes with edges pointing to `n`).

```python
D.predecessors("c")  # ['a']
```

### `neighbors`

```python
D.neighbors(n) -> list
```

Alias for `successors(n)`.

### `in_edges`

```python
D.in_edges(nbunch=None, data=False) -> EdgeView
```

Return incoming edges. If `data=True`, returns `(u, v, attr_dict)` tuples.

### `out_edges`

```python
D.out_edges(nbunch=None, data=False) -> EdgeView
```

Return outgoing edges. If `data=True`, returns `(u, v, attr_dict)` tuples.

---

## Degree

### `degree`

```python
D.degree(nbunch=None) -> int | DegreeView
```

Total degree (in-degree + out-degree).

### `in_degree`

```python
D.in_degree(nbunch=None) -> int | DegreeView
```

Number of incoming edges.

### `out_degree`

```python
D.out_degree(nbunch=None) -> int | DegreeView
```

Number of outgoing edges.

```python
D.add_edges_from([(1, 2), (1, 3), (2, 3)])
D.in_degree(3)   # 2
D.out_degree(1)  # 2
D.degree(1)      # 2  (out only, no incoming)
```

---

## Querying

### `has_node`

```python
D.has_node(n) -> bool
```

### `has_edge`

```python
D.has_edge(u, v) -> bool
```

### `nodes`

```python
D.nodes(data=False) -> NodeView
```

### `edges`

```python
D.edges(data=False, default=None) -> EdgeView
```

### `get_edge_data`

```python
D.get_edge_data(u, v, default=None) -> dict | None
```

### `adjacency`

```python
D.adjacency() -> list
```

### `nbunch_iter`

```python
D.nbunch_iter(nbunch=None) -> list
```

---

## Graph Properties

| Property / Method | Returns |
|---|---|
| `D.number_of_nodes()` | `int` |
| `D.order()` | `int` |
| `D.number_of_edges()` | `int` |
| `D.size(weight=None)` | `int` or weighted `float` |
| `D.name` | Graph name (get/set) |
| `D.is_directed()` | `True` |
| `D.is_multigraph()` | `False` |

---

## Transformation

### `reverse`

```python
D.reverse(copy=True) -> DiGraph
```

Return a graph with all edges reversed. If `copy=False`, reverses in place.

```python
D.add_edge(1, 2)
R = D.reverse()
R.has_edge(2, 1)  # True
R.has_edge(1, 2)  # False
```

### `to_undirected`

```python
D.to_undirected() -> Graph
```

Return an undirected copy of the digraph.

### `copy`

```python
D.copy() -> DiGraph
```

### `clear`

```python
D.clear()
```

### `clear_edges`

```python
D.clear_edges()
```

### `subgraph`

```python
D.subgraph(nodes) -> DiGraph
```

Return an induced subgraph on the given nodes, preserving edge direction.

---

## Dunder Methods

| Method | Description |
|--------|-------------|
| `n in D` | Check if node exists |
| `len(D)` | Number of nodes |
| `iter(D)` | Iterate over nodes |
| `D[n]` | Adjacency dict for node `n` (successors) |
