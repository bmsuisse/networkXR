---
title: Relabeling Functions
---

# Relabeling Functions

Functions for relabeling graph nodes. Available in `networkxr.relabel` and directly from `networkxr`.

---

## `relabel_nodes`

```python
nx.relabel_nodes(G, mapping, copy=True) -> Graph
```

Relabel the nodes of a graph.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `G` | Graph | Input graph |
| `mapping` | dict or callable | A dictionary or function mapping old labels to new labels |
| `copy` | bool | If `True` (default), return a new graph. If `False`, modify in place. |

**Examples:**

```python
import networkxr as nx

G = nx.path_graph(3)  # nodes: 0, 1, 2

# Relabel with a dictionary
H = nx.relabel_nodes(G, {0: "a", 1: "b", 2: "c"})
print(list(H.nodes()))  # ['a', 'b', 'c']

# Relabel with a function
H = nx.relabel_nodes(G, lambda x: x + 10)
print(list(H.nodes()))  # [10, 11, 12]

# In-place relabeling
nx.relabel_nodes(G, {0: "start"}, copy=False)
```

!!! note "Circular Mappings"
    In-place relabeling handles overlapping mappings using topological ordering.
    If a true cycle is detected (e.g., `{1: 2, 2: 1}`), a `NetworkXUnfeasible` exception is raised.

---

## `convert_node_labels_to_integers`

```python
nx.convert_node_labels_to_integers(
    G,
    first_label=0,
    ordering="default",
    label_attribute=None,
) -> Graph
```

Return a copy of `G` with nodes relabeled as consecutive integers.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `G` | Graph | Input graph |
| `first_label` | int | Starting integer label (default: `0`) |
| `ordering` | str | Node ordering strategy |
| `label_attribute` | str, optional | If set, stores the old label as a node attribute |

**Ordering Options:**

| Value | Description |
|-------|-------------|
| `"default"` | Insertion order |
| `"sorted"` | Sorted by node label |
| `"increasing degree"` | Sorted by degree (ascending) |
| `"decreasing degree"` | Sorted by degree (descending) |

**Examples:**

```python
G = nx.Graph()
G.add_edges_from([("a", "b"), ("b", "c")])

# Default ordering
H = nx.convert_node_labels_to_integers(G)
print(list(H.nodes()))  # [0, 1, 2]

# Preserve old labels
H = nx.convert_node_labels_to_integers(G, label_attribute="old_label")
print(H.nodes(data=True))
# [(0, {'old_label': 'a'}), (1, {'old_label': 'b'}), (2, {'old_label': 'c'})]

# Custom ordering
H = nx.convert_node_labels_to_integers(G, ordering="decreasing degree")
```
