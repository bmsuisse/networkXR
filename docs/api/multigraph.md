---
title: MultiGraph & MultiDiGraph
---

# MultiGraph & MultiDiGraph

Pure Python implementations supporting parallel (multi) edges.

---

## MultiGraph

`networkxr.MultiGraph` — an undirected multigraph allowing parallel edges.

### Constructor

```python
MultiGraph(incoming_graph_data=None, **attr)
```

```python
import networkxr as nx

M = nx.MultiGraph()
M = nx.MultiGraph(name="multi")
```

### Adding & Removing

#### `add_node` / `add_nodes_from`

```python
M.add_node(1, color="red")
M.add_nodes_from([2, 3, 4])
```

#### `add_edge`

```python
M.add_edge(u, v, key=None, **attr) -> key
```

Add an edge between `u` and `v`. Returns the edge key (auto-incremented integer if not specified).

```python
k1 = M.add_edge(1, 2, weight=1.0)          # key=0
k2 = M.add_edge(1, 2, weight=2.0)          # key=1
k3 = M.add_edge(1, 2, key="custom", weight=3.0)  # key="custom"
```

#### `add_edges_from`

```python
M.add_edges_from(ebunch, **attr)
```

Accepts `(u, v)`, `(u, v, key)`, `(u, v, data_dict)`, or `(u, v, key, data_dict)` tuples.

#### `add_weighted_edges_from`

```python
M.add_weighted_edges_from(ebunch, weight="weight")
```

#### `remove_node`

```python
M.remove_node(n)
```

#### `remove_edge`

```python
M.remove_edge(u, v, key=None)
```

If `key` is `None`, removes the edge with the lowest key.

### Querying

#### `has_node` / `has_edge`

```python
M.has_node(n) -> bool
M.has_edge(u, v, key=None) -> bool
```

If `key` is specified, checks for that specific parallel edge.

#### `get_edge_data`

```python
M.get_edge_data(u, v, key=None, default=None)
```

If `key` is `None`, returns dict of all keys: `{key: attr_dict, ...}`.
If `key` is specified, returns that edge's attribute dict.

```python
M.add_edge(1, 2, weight=1.0)
M.add_edge(1, 2, weight=2.0)

M.get_edge_data(1, 2)     # {0: {'weight': 1.0}, 1: {'weight': 2.0}}
M.get_edge_data(1, 2, 0)  # {'weight': 1.0}
```

#### `nodes` / `edges`

```python
M.nodes(data=False)
M.edges(data=False, keys=False)
```

When `keys=True`, edge tuples include the key: `(u, v, key)` or `(u, v, key, data)`.

#### `neighbors` / `degree`

```python
M.neighbors(n) -> list
M.degree(nbunch=None) -> list[tuple] | int
```

Degree counts parallel edges — an edge with 3 keys contributes 3 to the degree.

### Properties

| Property / Method | Returns |
|---|---|
| `M.number_of_nodes()` | `int` |
| `M.number_of_edges()` | `int` (counts each parallel edge) |
| `M.name` | Graph name (get/set) |
| `M.adj` | Adjacency dict |
| `M.is_directed()` | `False` |
| `M.is_multigraph()` | `True` |

### Transformation

```python
M.copy() -> MultiGraph
M.clear()
M.to_undirected() -> MultiGraph
M.subgraph(nodes) -> MultiGraph
```

---

## MultiDiGraph

`networkxr.MultiDiGraph` — a directed multigraph allowing parallel edges.

### Constructor

```python
MultiDiGraph(incoming_graph_data=None, **attr)
```

### Directed Methods

In addition to all `MultiGraph` methods, `MultiDiGraph` adds:

#### `successors` / `predecessors`

```python
MD.successors(n) -> list
MD.predecessors(n) -> list
```

#### `in_degree` / `out_degree`

```python
MD.in_degree(nbunch=None)
MD.out_degree(nbunch=None)
```

#### `in_edges` / `out_edges`

```python
MD.in_edges(data=False, keys=False)
MD.out_edges(data=False, keys=False)
```

#### `reverse`

```python
MD.reverse(copy=True) -> MultiDiGraph
```

Return a graph with all edges reversed.

#### `to_undirected`

```python
MD.to_undirected() -> MultiGraph
```

### Properties

| Property / Method | Returns |
|---|---|
| `MD.is_directed()` | `True` |
| `MD.is_multigraph()` | `True` |

### Example

```python
import networkxr as nx

MD = nx.MultiDiGraph()
MD.add_edge("a", "b", key="route1", distance=10)
MD.add_edge("a", "b", key="route2", distance=15)
MD.add_edge("b", "a", key="return", distance=12)

print(list(MD.successors("a")))     # ['b']
print(list(MD.predecessors("b")))   # ['a']
print(MD.in_degree("b"))            # 2  (route1 + route2)
print(MD.out_degree("b"))           # 1  (return)
```
