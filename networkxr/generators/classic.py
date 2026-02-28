"""Classic graph generators — NetworkX-compatible API."""

from __future__ import annotations

from typing import Any


def empty_graph(n: int = 0, create_using: Any = None) -> Any:
    """Return the empty graph with n nodes and zero edges."""
    from networkxr import Graph

    if create_using is not None:
        if isinstance(create_using, type):
            G = create_using()
        else:
            G = create_using
            G.clear()
    else:
        G = Graph()

    if n > 0:
        G.add_nodes_from(range(n))
    return G


def path_graph(n: int, create_using: Any = None) -> Any:
    """Return the path graph P_n of n nodes linearly connected."""
    G = empty_graph(n, create_using)
    edges = [(i, i + 1) for i in range(n - 1)]
    G.add_edges_from(edges)
    return G


def cycle_graph(n: int, create_using: Any = None) -> Any:
    """Return the cycle graph C_n of n cyclically connected nodes."""
    G = path_graph(n, create_using)
    if n > 1:
        G.add_edge(n - 1, 0)
    return G


def complete_graph(n: int, create_using: Any = None) -> Any:
    """Return the complete graph K_n."""
    G = empty_graph(n, create_using)
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    G.add_edges_from(edges)
    return G


def barbell_graph(m1: int, m2: int, create_using: Any = None) -> Any:
    """Return the barbell graph: two complete graphs connected by a path."""
    from networkxr import Graph

    if create_using is not None and isinstance(create_using, type):
        G = create_using()
    elif create_using is not None:
        G = create_using
        G.clear()
    else:
        G = Graph()

    if m1 < 2:
        msg = "Invalid graph description, m1 should be >= 2"
        raise ValueError(msg)
    if m2 < 0:
        msg = "Invalid graph description, m2 should be >= 0"
        raise ValueError(msg)

    n = 2 * m1 + m2
    G.add_nodes_from(range(n))

    # Left clique
    for i in range(m1):
        for j in range(i + 1, m1):
            G.add_edge(i, j)

    # Path
    for i in range(m1, m1 + m2 - 1):
        G.add_edge(i, i + 1)
    if m2 > 0:
        G.add_edge(m1 - 1, m1)
        G.add_edge(m1 + m2 - 1, m1 + m2)
    else:
        G.add_edge(m1 - 1, m1)

    # Right clique
    for i in range(m1 + m2, 2 * m1 + m2):
        for j in range(i + 1, 2 * m1 + m2):
            G.add_edge(i, j)

    return G


def star_graph(n: int, create_using: Any = None) -> Any:
    """Return the star graph with n+1 nodes: center 0 connected to 1..n."""
    G = empty_graph(n + 1, create_using)
    for i in range(1, n + 1):
        G.add_edge(0, i)
    return G
