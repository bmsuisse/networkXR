"""Utility functions for comparing graph structures."""

from __future__ import annotations

from typing import Any


def nodes_equal(nodes1: Any, nodes2: Any) -> bool:
    """Check if two node sequences are equal (unordered)."""
    try:
        return sorted(nodes1) == sorted(nodes2)
    except TypeError:
        return set(map(id, nodes1)) == set(map(id, nodes2))


def edges_equal(edges1: Any, edges2: Any, *, directed: bool = False) -> bool:
    """Check if two edge sequences are equal (unordered).

    For undirected graphs, (u,v) == (v,u).
    """

    def _canonicalize(e: Any, directed: bool) -> tuple[Any, ...]:
        t = tuple(e)
        if not directed and len(t) >= 2:
            key = tuple(sorted(t[:2]))
            return key + t[2:]
        return t

    try:
        s1 = sorted(_canonicalize(e, directed) for e in edges1)
        s2 = sorted(_canonicalize(e, directed) for e in edges2)
        return s1 == s2
    except TypeError:
        return False


def graphs_equal(g1: Any, g2: Any) -> bool:
    """Check if two graphs are structurally equal."""
    if not nodes_equal(sorted(g1.nodes()), sorted(g2.nodes())):
        return False
    if not edges_equal(sorted(g1.edges()), sorted(g2.edges())):
        return False
    # Compare graph attributes
    if hasattr(g1, "graph") and hasattr(g2, "graph"):
        g1_graph = g1.graph if isinstance(g1.graph, dict) else {}
        g2_graph = g2.graph if isinstance(g2.graph, dict) else {}
        if g1_graph != g2_graph:
            return False
    return True


def pairwise(iterable: Any) -> Any:
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    import itertools

    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def flatten(obj: Any, result: list[Any] | None = None) -> Any:
    """Return flattened version of (possibly nested) iterable."""
    if result is None:
        result = []
    for item in obj:
        if hasattr(item, "__iter__") and not isinstance(item, str):
            flatten(item, result)
        else:
            result.append(item)
    return tuple(result)
