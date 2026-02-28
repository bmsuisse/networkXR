---
title: Conversion Functions
---

# Conversion Functions

Functions for converting between graph representations. Available in `networkxr.convert` and also directly from `networkxr`.

---

## `to_dict_of_dicts`

```python
nx.to_dict_of_dicts(G, nodelist=None, edge_data=None) -> dict
```

Return adjacency representation as a dictionary of dictionaries.

```python
import networkxr as nx

G = nx.path_graph(3)
dod = nx.to_dict_of_dicts(G)
# {0: {1: {}}, 1: {0: {}, 2: {}}, 2: {1: {}}}
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `G` | Graph | Input graph |
| `nodelist` | list, optional | Use only nodes specified in `nodelist` |
| `edge_data` | any, optional | If specified, use this value for all edges instead of actual edge data |

---

## `from_dict_of_dicts`

```python
nx.from_dict_of_dicts(d, create_using=None, multigraph_input=False) -> Graph
```

Return a graph from a dict of dicts.

```python
d = {1: {2: {"weight": 1.0}}, 2: {3: {}}}
G = nx.from_dict_of_dicts(d)
```

When `multigraph_input=True` and `create_using` is a multigraph, the inner dict is `{key: attr_dict}`.

---

## `to_dict_of_lists`

```python
nx.to_dict_of_lists(G, nodelist=None) -> dict
```

Return adjacency as a dictionary of lists.

```python
G = nx.path_graph(3)
dol = nx.to_dict_of_lists(G)
# {0: [1], 1: [0, 2], 2: [1]}
```

---

## `from_dict_of_lists`

```python
nx.from_dict_of_lists(d, create_using=None) -> Graph
```

Return a graph from a dict of lists.

```python
d = {1: [2, 3], 2: [3]}
G = nx.from_dict_of_lists(d)
```

---

## `to_networkx_graph`

```python
nx.to_networkx_graph(data, create_using=None, multigraph_input=False) -> Graph
```

Convert various data formats to a graph. Automatically detects:

- **Graph-like objects** — objects with `adj` and `nodes` attributes
- **Dict of dicts** — adjacency representation
- **Dict of lists** — adjacency representation
- **Edge list** — iterable of `(u, v)` or `(u, v, data)` tuples

```python
# From edge list
G = nx.to_networkx_graph([(1, 2), (2, 3)])

# From dict of dicts
G = nx.to_networkx_graph({1: {2: {}, 3: {}}, 2: {3: {}}})

# From another graph
G2 = nx.to_networkx_graph(G, create_using=nx.DiGraph)
```

---

## `to_edgelist`

```python
nx.to_edgelist(G, nodelist=None) -> list[tuple]
```

Return a list of edges as `(u, v, data)` tuples.

```python
G = nx.Graph()
G.add_edge(1, 2, weight=3.0)
nx.to_edgelist(G)
# [(1, 2, {'weight': 3.0})]
```

If `nodelist` is specified, only edges between nodes in the list are returned.
