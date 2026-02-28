"""Built-in layout algorithms (zero-dependency)."""

from __future__ import annotations

import math
import random
from typing import Any, Hashable


def spring_layout(
    G: Any,
    *,
    k: float | None = None,
    iterations: int = 50,
    seed: int | None = None,
    scale: float = 1.0,
    center: tuple[float, float] = (0.0, 0.0),
) -> dict[Hashable, tuple[float, float]]:
    """Fruchterman-Reingold force-directed layout.

    A pure-Python implementation that requires no external dependencies.

    Parameters
    ----------
    G : Graph
        A networkxr graph.
    k : float, optional
        Optimal distance between nodes.  Defaults to ``1 / sqrt(n)``.
    iterations : int
        Number of iterations of the spring simulation.
    seed : int, optional
        Random seed for reproducibility.
    scale : float
        Scale factor applied to final positions.
    center : tuple[float, float]
        Center of the layout.

    Returns
    -------
    dict[Hashable, tuple[float, float]]
        Mapping of node → (x, y) position.
    """
    rng = random.Random(seed)
    nodes = list(G.nodes())
    n = len(nodes)

    if n == 0:
        return {}
    if n == 1:
        return {nodes[0]: center}

    # Initial random positions
    pos: dict[Hashable, list[float]] = {
        node: [rng.uniform(-1, 1), rng.uniform(-1, 1)] for node in nodes
    }

    if k is None:
        k = 1.0 / math.sqrt(n)

    t = 1.0  # temperature

    edges = list(G.edges())

    for _ in range(iterations):
        disp: dict[Hashable, list[float]] = {node: [0.0, 0.0] for node in nodes}

        # Repulsive forces between all pairs
        for i in range(n):
            for j in range(i + 1, n):
                u, v = nodes[i], nodes[j]
                dx = pos[u][0] - pos[v][0]
                dy = pos[u][1] - pos[v][1]
                dist = math.sqrt(dx * dx + dy * dy) + 1e-9
                force = (k * k) / dist
                fx = (dx / dist) * force
                fy = (dy / dist) * force
                disp[u][0] += fx
                disp[u][1] += fy
                disp[v][0] -= fx
                disp[v][1] -= fy

        # Attractive forces along edges
        for u, v in edges:
            dx = pos[u][0] - pos[v][0]
            dy = pos[u][1] - pos[v][1]
            dist = math.sqrt(dx * dx + dy * dy) + 1e-9
            force = (dist * dist) / k
            fx = (dx / dist) * force
            fy = (dy / dist) * force
            disp[u][0] -= fx
            disp[u][1] -= fy
            disp[v][0] += fx
            disp[v][1] += fy

        # Apply displacements (clamped by temperature)
        for node in nodes:
            dx, dy = disp[node]
            dist = math.sqrt(dx * dx + dy * dy) + 1e-9
            capped = min(dist, t)
            pos[node][0] += (dx / dist) * capped
            pos[node][1] += (dy / dist) * capped

        t *= 0.95  # cool down

    # Scale and center
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    span_x = max_x - min_x or 1.0
    span_y = max_y - min_y or 1.0

    result: dict[Hashable, tuple[float, float]] = {}
    for node, (x, y) in pos.items():
        nx_ = ((x - min_x) / span_x - 0.5) * 2.0 * scale + center[0]
        ny_ = ((y - min_y) / span_y - 0.5) * 2.0 * scale + center[1]
        result[node] = (nx_, ny_)

    return result


def circular_layout(
    G: Any,
    *,
    scale: float = 1.0,
    center: tuple[float, float] = (0.0, 0.0),
) -> dict[Hashable, tuple[float, float]]:
    """Arrange nodes uniformly on a circle.

    Parameters
    ----------
    G : Graph
        A networkxr graph.
    scale : float
        Radius of the circle.
    center : tuple[float, float]
        Center of the circle.

    Returns
    -------
    dict[Hashable, tuple[float, float]]
        Mapping of node → (x, y) position.
    """
    nodes = list(G.nodes())
    n = len(nodes)

    if n == 0:
        return {}
    if n == 1:
        return {nodes[0]: center}

    result: dict[Hashable, tuple[float, float]] = {}
    for i, node in enumerate(nodes):
        angle = 2.0 * math.pi * i / n
        x = center[0] + scale * math.cos(angle)
        y = center[1] + scale * math.sin(angle)
        result[node] = (x, y)

    return result
