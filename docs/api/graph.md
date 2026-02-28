---
title: Graph
---

# Graph

`networkxr.Graph` — an undirected simple graph.

Implemented in **Rust** via PyO3 for maximum performance. Nodes can be any hashable Python object. Self-loops are allowed but parallel edges are not — use [`MultiGraph`](multigraph.md) for that.

---

## Constructor

```python
Graph(incoming_graph_data=None, **attr)
```

Create an undirected graph.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `incoming_graph_data` | various, optional | Data to initialize graph (edge list, dict of dicts, dict of lists, or another graph) |
| `**attr` | keyword arguments | Graph attributes, e.g. `name="my graph"` |

**Examples:**

```python
import networkxr as nx

G = nx.Graph()                          # Empty graph
G = nx.Graph(name="my graph")           # With attributes
G = nx.Graph([(1, 2), (2, 3)])          # From edge list
G = nx.Graph({1: {2: {}, 3: {}}, 2: {3: {}}})  # From dict of dicts
```

---

## Adding & Removing

### `add_node`

```python
G.add_node(node_for_adding, **attr)
```

Add a single node with optional attributes.

```python
G.add_node(1)
G.add_node("server", role="backend")
```

### `add_nodes_from`

```python
G.add_nodes_from(nodes_for_adding, **attr)
```

Add multiple nodes. Accepts an iterable of nodes or `(node, attr_dict)` tuples.

```python
G.add_nodes_from([1, 2, 3])
G.add_nodes_from([(4, {"color": "red"}), (5, {"color": "blue"})])
```

### `remove_node`

```python
G.remove_node(n)
```

Remove node `n` and all incident edges. Raises `NetworkXError` if node not found.

### `add_edge`

```python
G.add_edge(u_of_edge, v_of_edge, **attr)
```

Add an edge between `u` and `v`. Nodes are automatically added if not present.

```python
G.add_edge(1, 2)
G.add_edge("a", "b", weight=4.5)
```

### `add_edges_from`

```python
G.add_edges_from(ebunch_to_add, **attr)
```

Add edges from an iterable. Each element can be a `(u, v)` tuple or `(u, v, dict)` tuple.

```python
G.add_edges_from([(1, 2), (2, 3)])
G.add_edges_from([(1, 2, {"weight": 1.0})])
```

### `add_weighted_edges_from`

```python
G.add_weighted_edges_from(ebunch_to_add, weight="weight")
```

Add weighted edges from `(u, v, w)` tuples.

```python
G.add_weighted_edges_from([(1, 2, 3.0), (2, 3, 1.5)])
```

### `remove_edge`

```python
G.remove_edge(u, v)
```

Remove edge between `u` and `v`. Raises `NetworkXError` if edge not found.

---

## Querying

### `has_node`

```python
G.has_node(n) -> bool
```

Return `True` if node `n` is in the graph. Equivalent to `n in G`.

### `has_edge`

```python
G.has_edge(u, v) -> bool
```

Return `True` if an edge exists between `u` and `v`.

### `neighbors`

```python
G.neighbors(n) -> list
```

Return a list of all neighbors of node `n`.

### `nodes`

```python
G.nodes(data=False) -> NodeView
```

Return a view of the graph's nodes. If `data=True`, returns `(node, attr_dict)` tuples.

### `edges`

```python
G.edges(data=False, default=None) -> EdgeView
```

Return a view of the graph's edges. If `data=True`, returns `(u, v, attr_dict)` tuples.

### `degree`

```python
G.degree(nbunch=None) -> int | DegreeView
```

Return the degree of a node, or a `DegreeView` of `(node, degree)` pairs for all nodes.

### `get_edge_data`

```python
G.get_edge_data(u, v, default=None) -> dict | None
```

Return the attribute dictionary for the edge `(u, v)`.

### `adjacency`

```python
G.adjacency() -> list
```

Return an adjacency list representation.

---

## Graph Properties

### `number_of_nodes` / `order`

```python
G.number_of_nodes() -> int
G.order() -> int
```

### `number_of_edges` / `size`

```python
G.number_of_edges() -> int
G.size(weight=None) -> int | float
```

If `weight` is specified, returns the sum of edge weights.

### `name`

```python
G.name          # get
G.name = "foo"  # set
```

### `adj`

```python
G.adj -> dict
```

Return the adjacency dict.

### `is_directed`

```python
G.is_directed() -> bool  # Always False
```

### `is_multigraph`

```python
G.is_multigraph() -> bool  # Always False
```

---

## Transformation

### `copy`

```python
G.copy() -> Graph
```

Return a deep copy of the graph.

### `clear`

```python
G.clear()
```

Remove all nodes and edges.

### `clear_edges`

```python
G.clear_edges()
```

Remove all edges, keeping nodes.

### `subgraph`

```python
G.subgraph(nodes) -> Graph
```

Return an induced subgraph on the given nodes.

### `to_undirected`

```python
G.to_undirected() -> Graph
```

Return a copy (already undirected).

---

## Dunder Methods

| Method | Description |
|--------|-------------|
| `n in G` | Check if node exists (`__contains__`) |
| `len(G)` | Number of nodes (`__len__`) |
| `iter(G)` | Iterate over nodes (`__iter__`) |
| `G[n]` | Adjacency dict for node `n` (`__getitem__`) |
