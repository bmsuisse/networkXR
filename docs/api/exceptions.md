---
title: Exceptions
---

# Exceptions

networkXR provides a 1:1 compatible exception hierarchy with NetworkX. All exceptions are available in `networkxr.exception` and directly from `networkxr`.

---

## Hierarchy

```
Exception
└── NetworkXException
    ├── NetworkXError
    ├── NetworkXPointlessConcept
    ├── NodeNotFound
    ├── HasACycle
    ├── AmbiguousSolution
    └── NetworkXAlgorithmError
        ├── NetworkXUnfeasible
        │   ├── NetworkXNoPath
        │   └── NetworkXNoCycle
        ├── NetworkXUnbounded
        ├── PowerIterationFailedConvergence
        └── ExceededMaxIterations
```

---

## Exception Classes

### `NetworkXException`

Base class for all NetworkX exceptions.

### `NetworkXError`

Exception for a serious error in NetworkX. Raised for invalid operations like removing a non-existent node or edge.

```python
import networkxr as nx

G = nx.Graph()
try:
    G.remove_node(999)
except nx.NetworkXError as e:
    print(e)  # "The node 999 is not in the graph."
```

### `NetworkXPointlessConcept`

Raised when a null graph is drawn without a layout algorithm.

### `NetworkXAlgorithmError`

Base class for unexpected algorithm termination.

### `NetworkXUnfeasible`

Raised when an algorithm has no feasible solution.

```python
try:
    nx.relabel_nodes(G, {1: 2, 2: 1}, copy=False)
except nx.NetworkXUnfeasible as e:
    print(e)  # Circular mapping detected
```

### `NetworkXNoPath`

Raised when no path exists between requested nodes.

### `NetworkXNoCycle`

Raised when no cycle exists in a graph where one was expected.

### `NetworkXUnbounded`

Raised when an optimization problem is unbounded.

### `NodeNotFound`

Raised when a requested node is not present in the graph.

### `HasACycle`

Raised when a graph has a cycle but an algorithm expects it not to.

### `PowerIterationFailedConvergence`

Raised when power iteration fails to converge.

```python
PowerIterationFailedConvergence(num_iterations)
```

Has a `num_iterations` attribute storing the number of iterations attempted.

### `ExceededMaxIterations`

Raised when a loop exceeds the maximum number of iterations.

### `AmbiguousSolution`

Raised when more than one valid solution exists for an intermediary step of an algorithm.
