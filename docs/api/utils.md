---
title: Utility Functions
---

# Utility Functions

Helper functions for comparing graphs and working with iterables. Available in `networkxr.utils` and directly from `networkxr`.

---

## `nodes_equal`

```python
nx.utils.nodes_equal(nodes1, nodes2) -> bool
```

Check if two node sequences are equal (order-independent).

```python
from networkxr.utils import nodes_equal

nodes_equal([1, 2, 3], [3, 1, 2])  # True
nodes_equal([1, 2], [1, 2, 3])     # False
```

---

## `edges_equal`

```python
nx.utils.edges_equal(edges1, edges2, *, directed=False) -> bool
```

Check if two edge sequences are equal (order-independent).

For undirected comparison (`directed=False`), `(u, v)` equals `(v, u)`.

```python
from networkxr.utils import edges_equal

edges_equal([(1, 2), (2, 3)], [(2, 1), (3, 2)])  # True (undirected)
edges_equal([(1, 2)], [(2, 1)], directed=True)    # False (directed)
```

---

## `graphs_equal`

```python
nx.utils.graphs_equal(g1, g2) -> bool
```

Check if two graphs are structurally equal: same nodes, same edges, and same graph-level attributes.

```python
import networkxr as nx
from networkxr.utils import graphs_equal

G1 = nx.path_graph(3)
G2 = nx.path_graph(3)
graphs_equal(G1, G2)  # True

G2.add_node(99)
graphs_equal(G1, G2)  # False
```

---

## `pairwise`

```python
nx.utils.pairwise(iterable) -> zip
```

Return successive overlapping pairs: `s → (s0, s1), (s1, s2), (s2, s3), ...`

```python
from networkxr.utils import pairwise

list(pairwise([1, 2, 3, 4]))  # [(1, 2), (2, 3), (3, 4)]
list(pairwise("abc"))          # [('a', 'b'), ('b', 'c')]
```

---

## `flatten`

```python
nx.utils.flatten(obj, result=None) -> tuple
```

Return a flattened version of a (possibly nested) iterable.

```python
from networkxr.utils import flatten

flatten([[1, 2], [3, [4, 5]]])  # (1, 2, 3, 4, 5)
flatten([(1, 2), (3,)])          # (1, 2, 3)
```

!!! note
    Strings are not flattened — they are treated as atomic values.
