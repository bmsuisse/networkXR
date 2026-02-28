"""Node relabeling functions — NetworkX-compatible API."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any


def relabel_nodes(
    G: Any,
    mapping: Mapping[Any, Any] | Callable[[Any], Any],
    copy: bool = True,
) -> Any:
    """Relabel the nodes of the graph G."""
    if callable(mapping) and not isinstance(mapping, Mapping):
        _map_func = mapping
        mapping = {n: _map_func(n) for n in G}

    if not isinstance(mapping, Mapping):
        msg = "'mapping' must be a Mapping or Callable"
        raise AttributeError(msg)

    def map_func(n: Any) -> Any:
        return mapping.get(n, n)  # type: ignore[union-attr]

    if copy:
        return _relabel_copy(G, mapping, map_func)
    return _relabel_inplace(G, mapping, map_func)


def _relabel_copy(
    G: Any,
    mapping: Mapping[Any, Any],
    map_func: Callable[[Any], Any],
) -> Any:
    """Relabel by creating a new graph."""
    H = G.__class__()
    if hasattr(G, "graph") and isinstance(G.graph, dict):
        H.graph.update(G.graph)

    for n, dd in G.nodes(data=True):
        H.add_node(map_func(n), **dd)

    if hasattr(G, "is_multigraph") and G.is_multigraph():
        for u, v, key, dd in G.edges(data=True, keys=True):
            nu, nv = map_func(u), map_func(v)
            # Check key conflict
            if nu in H._adj and nv in H._adj.get(nu, {}) and key in H._adj[nu].get(nv, {}):
                H.add_edge(nu, nv, **dd)  # auto-generate key
            else:
                H.add_edge(nu, nv, key=key, **dd)
    else:
        for u, v, dd in G.edges(data=True):
            H.add_edge(map_func(u), map_func(v), **dd)
    return H


def _relabel_inplace(
    G: Any,
    mapping: Mapping[Any, Any],
    map_func: Callable[[Any], Any],
) -> Any:
    """Relabel nodes in place, preserving node order.

    Strategy: rebuild _node and _adj (and _pred for digraphs) dicts
    with the new labels, preserving insertion order.
    """
    from networkxr import NetworkXUnfeasible

    # Filter to only nodes that exist and actually change
    mapping = {old: new for old, new in mapping.items() if old in G and old != new}
    if not mapping:
        return G

    old_labels = set(mapping.keys())
    new_labels = set(mapping.values())

    # Check for true circular dependencies (e.g., {0: 1, 1: 0})
    if old_labels & new_labels:
        # Topological sort to find valid ordering
        deps: dict[Any, set[Any]] = {old: set() for old in old_labels}
        for old, new in mapping.items():
            if new in old_labels:
                deps[old].add(new)

        from collections import deque

        in_degree: dict[Any, int] = {n: 0 for n in old_labels}
        reverse_deps: dict[Any, list[Any]] = {n: [] for n in old_labels}
        for old, dep_set in deps.items():
            for dep in dep_set:
                if dep in reverse_deps:
                    reverse_deps[dep].append(old)
                    in_degree[old] += 1

        queue = deque([n for n in old_labels if in_degree[n] == 0])
        order: list[Any] = []
        while queue:
            n = queue.popleft()
            order.append(n)
            for dependent in reverse_deps.get(n, []):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        if len(order) < len(old_labels):
            msg = "The node label sets are overlapping and no ordering can resolve this."
            raise NetworkXUnfeasible(msg)

        # Process swaps sequentially in topo order
        for old in order:
            _swap_node_ordered(G, old, mapping[old])
        return G

    # Non-overlapping: check if full or partial mapping
    is_full = len(mapping) == len(G._node)
    if is_full:
        # Full mapping: use rebuild to preserve node order
        _rebuild_graph(G, mapping)
    else:
        # Partial mapping: sequential swap (order not preserved, matches NetworkX)
        for old, new in mapping.items():
            if G.has_node(old):
                _swap_node_ordered(G, old, new)
    return G


def _rebuild_graph(G: Any, mapping: Mapping[Any, Any]) -> None:
    """Rebuild G's internal dicts with new labels, preserving node order."""

    def m(n: Any) -> Any:
        return mapping.get(n, n)

    is_multi = hasattr(G, "is_multigraph") and G.is_multigraph()
    is_di = hasattr(G, "is_directed") and G.is_directed()

    # Snapshot old state
    old_node = G._node
    old_adj = G._adj
    old_pred = G._pred if is_di else None

    # Create new dicts preserving order
    new_node: dict[Any, Any] = {}
    new_adj: dict[Any, Any] = {}
    new_pred: dict[Any, Any] | None = {} if is_di else None

    for n in old_node:
        nn = m(n)
        new_node[nn] = old_node[n]
        new_adj[nn] = {}
        if new_pred is not None:
            new_pred[nn] = {}

    if is_multi:
        for u in old_adj:
            for v in old_adj[u]:
                nu, nv = m(u), m(v)
                if nv not in new_adj[nu]:
                    new_adj[nu][nv] = {}
                for key, dd in old_adj[u][v].items():
                    if key in new_adj[nu][nv]:
                        # Merge: find next available key
                        k = key
                        while k in new_adj[nu][nv]:
                            k = k + 1 if isinstance(k, int) else 0
                        new_adj[nu][nv][k] = dd
                    else:
                        new_adj[nu][nv][key] = dd
        if is_di and old_pred is not None and new_pred is not None:
            for v in old_pred:
                for u in old_pred[v]:
                    nv, nu = m(v), m(u)
                    if nu not in new_pred[nv]:
                        new_pred[nv][nu] = {}
                    for key, dd in old_pred[v][u].items():
                        if key in new_pred[nv][nu]:
                            k = key
                            while k in new_pred[nv][nu]:
                                k = k + 1 if isinstance(k, int) else 0
                            new_pred[nv][nu][k] = dd
                        else:
                            new_pred[nv][nu][key] = dd
    else:
        for u in old_adj:
            for v, dd in old_adj[u].items():
                nu, nv = m(u), m(v)
                if nv not in new_adj[nu]:
                    new_adj[nu][nv] = dd
                else:
                    new_adj[nu][nv].update(dd)
        if is_di and old_pred is not None and new_pred is not None:
            for v in old_pred:
                for u, dd in old_pred[v].items():
                    nv, nu = m(v), m(u)
                    if nu not in new_pred[nv]:
                        new_pred[nv][nu] = dd
                    else:
                        new_pred[nv][nu].update(dd)

    G._node = new_node
    G._adj = new_adj
    if is_di and new_pred is not None:
        G._pred = new_pred


def _swap_node_ordered(G: Any, old: Any, new: Any) -> None:
    """Replace node old→new using remove+re-add (doesn't preserve order)."""
    if old == new:
        return

    is_multi = hasattr(G, "is_multigraph") and G.is_multigraph()

    node_data = dict(G._node.get(old, {}))

    if is_multi:
        edges = []
        for u, v, key, dd in G.edges(data=True, keys=True):
            if u == old or v == old:
                edges.append((u, v, key, dict(dd)))

        G.remove_node(old)
        if new not in G:
            G.add_node(new, **node_data)
        else:
            G._node[new].update(node_data)

        for u, v, key, dd in edges:
            nu = new if u == old else u
            nv = new if v == old else v
            # Check if this key already exists on the target pair
            if nu in G._adj and nv in G._adj.get(nu, {}) and key in G._adj[nu].get(nv, {}):
                # Key conflict: let auto-generate
                G.add_edge(nu, nv, **dd)
            else:
                G.add_edge(nu, nv, key=key, **dd)
    else:
        edges = []
        for u, v, dd in G.edges(data=True):
            if u == old or v == old:
                edges.append((u, v, dict(dd)))

        G.remove_node(old)
        G.add_node(new, **node_data)

        for u, v, dd in edges:
            nu = new if u == old else u
            nv = new if v == old else v
            G.add_edge(nu, nv, **dd)


def convert_node_labels_to_integers(
    G: Any,
    first_label: int = 0,
    ordering: str = "default",
    label_attribute: str | None = None,
) -> Any:
    """Return a copy of G with node labels replaced by integers."""
    from networkxr import NetworkXError

    if ordering == "default":
        nodes = list(G)
    elif ordering == "sorted":
        nodes = sorted(G)
    elif ordering == "increasing degree":
        dlist = list(G.degree)
        dlist.sort(key=lambda x: (x[1], x[0]))
        nodes = [n for n, _d in dlist]
    elif ordering == "decreasing degree":
        dlist = list(G.degree)
        dlist.sort(key=lambda x: (-x[1], x[0]))
        nodes = [n for n, _d in dlist]
    else:
        msg = f"Unknown node ordering: {ordering}"
        raise NetworkXError(msg)

    mapping = {n: i + first_label for i, n in enumerate(nodes)}
    H = relabel_nodes(G, mapping, copy=True)

    if label_attribute is not None:
        for old, new_label in mapping.items():
            H.nodes[new_label][label_attribute] = old

    if hasattr(G, "graph") and isinstance(G.graph, dict):
        H.graph.update(G.graph)

    return H
