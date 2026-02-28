"""Benchmark suite — networkxr vs networkx at multiple scales.

Run:
    pytest tests/test_benchmarks.py -v --benchmark-only --benchmark-group-by=group
"""

from __future__ import annotations

import random
from typing import Any

import pytest

import networkx as real_nx
import networkxr as nxr
from networkxr.intgraph import IntGraph

# ─── Edge Lists ──────────────────────────────────────────────────

SEED = 42


def _edge_list(n: int, m: int) -> list[tuple[int, int]]:
    rng = random.Random(SEED)
    return [(rng.randint(0, n - 1), rng.randint(0, n - 1)) for _ in range(m)]


# Small: 1K nodes, 5K edges
E_1K = _edge_list(1_000, 5_000)
# Medium: 10K nodes, 50K edges
E_10K = _edge_list(10_000, 50_000)
# Large: 100K nodes, 500K edges
E_100K = _edge_list(100_000, 500_000)


def _build(cls: Any, edges: list[tuple[int, int]]) -> Any:
    g = cls()
    for u, v in edges:
        g.add_edge(u, v)
    return g


# Pre-built graphs for read benchmarks
NX_1K = _build(real_nx.Graph, E_1K)
NXR_1K = _build(nxr.Graph, E_1K)
NX_10K = _build(real_nx.Graph, E_10K)
NXR_10K = _build(nxr.Graph, E_10K)
NX_100K = _build(real_nx.Graph, E_100K)
NXR_100K = _build(nxr.Graph, E_100K)

# Rust IntGraph (pre-built)
RUST_1K = IntGraph(E_1K)
RUST_10K = IntGraph(E_10K)
RUST_100K = IntGraph(E_100K)


# ═══════════════════════════════════════════════════════════════
#  BUILD — Small (1K/5K)
# ═══════════════════════════════════════════════════════════════


class TestBuildSmall:
    @pytest.mark.benchmark(group="build_1K")
    def test_nx(self, benchmark: Any) -> None:
        benchmark(lambda: _build(real_nx.Graph, E_1K))

    @pytest.mark.benchmark(group="build_1K")
    def test_nxr(self, benchmark: Any) -> None:
        benchmark(lambda: _build(nxr.Graph, E_1K))

    @pytest.mark.benchmark(group="build_1K")
    def test_rust(self, benchmark: Any) -> None:
        benchmark(lambda: IntGraph(E_1K))


# ═══════════════════════════════════════════════════════════════
#  BUILD — Medium (10K/50K)
# ═══════════════════════════════════════════════════════════════


class TestBuildMedium:
    @pytest.mark.benchmark(group="build_10K")
    def test_nx(self, benchmark: Any) -> None:
        benchmark(lambda: _build(real_nx.Graph, E_10K))

    @pytest.mark.benchmark(group="build_10K")
    def test_nxr(self, benchmark: Any) -> None:
        benchmark(lambda: _build(nxr.Graph, E_10K))

    @pytest.mark.benchmark(group="build_10K")
    def test_rust(self, benchmark: Any) -> None:
        benchmark(lambda: IntGraph(E_10K))


# ═══════════════════════════════════════════════════════════════
#  BUILD — Large (100K/500K)
# ═══════════════════════════════════════════════════════════════


class TestBuildLarge:
    @pytest.mark.benchmark(group="build_100K")
    def test_nx(self, benchmark: Any) -> None:
        benchmark(lambda: _build(real_nx.Graph, E_100K))

    @pytest.mark.benchmark(group="build_100K")
    def test_nxr(self, benchmark: Any) -> None:
        benchmark(lambda: _build(nxr.Graph, E_100K))

    @pytest.mark.benchmark(group="build_100K")
    def test_rust(self, benchmark: Any) -> None:
        benchmark(lambda: IntGraph(E_100K))


# ═══════════════════════════════════════════════════════════════
#  ITER EDGES — all scales
# ═══════════════════════════════════════════════════════════════


class TestIterEdgesSmall:
    @pytest.mark.benchmark(group="iter_edges_1K")
    def test_nx(self, benchmark: Any) -> None:
        g = NX_1K
        benchmark(lambda: sum(1 for _ in g.edges()))

    @pytest.mark.benchmark(group="iter_edges_1K")
    def test_nxr(self, benchmark: Any) -> None:
        g = NXR_1K
        benchmark(lambda: sum(1 for _ in g.edges))

    @pytest.mark.benchmark(group="iter_edges_1K")
    def test_rust(self, benchmark: Any) -> None:
        g = RUST_1K
        benchmark(lambda: g.edges())


class TestIterEdgesMedium:
    @pytest.mark.benchmark(group="iter_edges_10K")
    def test_nx(self, benchmark: Any) -> None:
        g = NX_10K
        benchmark(lambda: sum(1 for _ in g.edges()))

    @pytest.mark.benchmark(group="iter_edges_10K")
    def test_nxr(self, benchmark: Any) -> None:
        g = NXR_10K
        benchmark(lambda: sum(1 for _ in g.edges))

    @pytest.mark.benchmark(group="iter_edges_10K")
    def test_rust(self, benchmark: Any) -> None:
        g = RUST_10K
        benchmark(lambda: g.edges())


class TestIterEdgesLarge:
    @pytest.mark.benchmark(group="iter_edges_100K")
    def test_nx(self, benchmark: Any) -> None:
        g = NX_100K
        benchmark(lambda: sum(1 for _ in g.edges()))

    @pytest.mark.benchmark(group="iter_edges_100K")
    def test_nxr(self, benchmark: Any) -> None:
        g = NXR_100K
        benchmark(lambda: sum(1 for _ in g.edges))

    @pytest.mark.benchmark(group="iter_edges_100K")
    def test_rust(self, benchmark: Any) -> None:
        g = RUST_100K
        benchmark(lambda: g.edges())


# ═══════════════════════════════════════════════════════════════
#  HAS_EDGE  (10K scale)
# ═══════════════════════════════════════════════════════════════


class TestHasEdge:
    @pytest.mark.benchmark(group="has_edge")
    def test_nx(self, benchmark: Any) -> None:
        g, edges = NX_10K, E_10K[:10_000]
        benchmark(lambda: sum(1 for u, v in edges if g.has_edge(u, v)))

    @pytest.mark.benchmark(group="has_edge")
    def test_nxr(self, benchmark: Any) -> None:
        g, edges = NXR_10K, E_10K[:10_000]
        benchmark(lambda: sum(1 for u, v in edges if g.has_edge(u, v)))

    @pytest.mark.benchmark(group="has_edge")
    def test_rust(self, benchmark: Any) -> None:
        g, edges = RUST_10K, E_10K[:10_000]
        benchmark(lambda: sum(1 for u, v in edges if g.has_edge(u, v)))


# ═══════════════════════════════════════════════════════════════
#  EDGE COUNT
# ═══════════════════════════════════════════════════════════════


class TestEdgeCount:
    @pytest.mark.benchmark(group="edge_count_10K")
    def test_nx(self, benchmark: Any) -> None:
        benchmark(NX_10K.number_of_edges)

    @pytest.mark.benchmark(group="edge_count_10K")
    def test_nxr(self, benchmark: Any) -> None:
        benchmark(NXR_10K.number_of_edges)

    @pytest.mark.benchmark(group="edge_count_10K")
    def test_rust(self, benchmark: Any) -> None:
        benchmark(RUST_10K.number_of_edges)


class TestEdgeCountLarge:
    @pytest.mark.benchmark(group="edge_count_100K")
    def test_nx(self, benchmark: Any) -> None:
        benchmark(NX_100K.number_of_edges)

    @pytest.mark.benchmark(group="edge_count_100K")
    def test_nxr(self, benchmark: Any) -> None:
        benchmark(NXR_100K.number_of_edges)

    @pytest.mark.benchmark(group="edge_count_100K")
    def test_rust(self, benchmark: Any) -> None:
        benchmark(RUST_100K.number_of_edges)


# ═══════════════════════════════════════════════════════════════
#  NEIGHBORS (10K scale)
# ═══════════════════════════════════════════════════════════════


class TestNeighbors:
    @pytest.mark.benchmark(group="neighbors")
    def test_nx(self, benchmark: Any) -> None:
        g = NX_10K
        benchmark(lambda: sum(1 for i in range(10_000) for _ in g.neighbors(i)))

    @pytest.mark.benchmark(group="neighbors")
    def test_nxr(self, benchmark: Any) -> None:
        g = NXR_10K
        benchmark(lambda: sum(1 for i in range(10_000) for _ in g.neighbors(i)))

    @pytest.mark.benchmark(group="neighbors")
    def test_rust(self, benchmark: Any) -> None:
        g = RUST_10K
        benchmark(lambda: sum(len(g.neighbors(i)) for i in range(10_000)))


# ═══════════════════════════════════════════════════════════════
#  COPY (10K scale)
# ═══════════════════════════════════════════════════════════════


class TestCopy:
    @pytest.mark.benchmark(group="copy")
    def test_nx(self, benchmark: Any) -> None:
        benchmark(NX_10K.copy)

    @pytest.mark.benchmark(group="copy")
    def test_nxr(self, benchmark: Any) -> None:
        benchmark(NXR_10K.copy)


# ═══════════════════════════════════════════════════════════════
#  CONSTRUCTOR from edge list (10K)
# ═══════════════════════════════════════════════════════════════


class TestConstructor:
    @pytest.mark.benchmark(group="constructor")
    def test_nx(self, benchmark: Any) -> None:
        benchmark(lambda: real_nx.Graph(E_10K))

    @pytest.mark.benchmark(group="constructor")
    def test_nxr(self, benchmark: Any) -> None:
        benchmark(lambda: nxr.Graph(E_10K))

    @pytest.mark.benchmark(group="constructor")
    def test_rust(self, benchmark: Any) -> None:
        benchmark(lambda: IntGraph(E_10K))


# ═══════════════════════════════════════════════════════════════
#  ADD_EDGES_FROM batch (10K)
# ═══════════════════════════════════════════════════════════════


class TestBatch:
    @pytest.mark.benchmark(group="add_edges_from")
    def test_nx(self, benchmark: Any) -> None:
        def fn() -> None:
            g = real_nx.Graph()
            g.add_edges_from(E_10K)

        benchmark(fn)

    @pytest.mark.benchmark(group="add_edges_from")
    def test_nxr(self, benchmark: Any) -> None:
        def fn() -> None:
            g = nxr.Graph()
            g.add_edges_from(E_10K)

        benchmark(fn)


# ═══════════════════════════════════════════════════════════════
#  Self-benchmarks (networkxr internal comparisons)
# ═══════════════════════════════════════════════════════════════


class TestSelfConstruction:
    @pytest.mark.benchmark(group="self_construction")
    def test_add_edge_loop(self, benchmark: Any) -> None:
        benchmark(lambda: _build(nxr.Graph, E_10K))

    @pytest.mark.benchmark(group="self_construction")
    def test_add_edges_from(self, benchmark: Any) -> None:
        def fn() -> Any:
            g = nxr.Graph()
            g.add_edges_from(E_10K)
            return g

        benchmark(fn)

    @pytest.mark.benchmark(group="self_construction")
    def test_constructor(self, benchmark: Any) -> None:
        benchmark(lambda: nxr.Graph(E_10K))
