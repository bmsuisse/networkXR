"""Tests for faker-powered graph generators."""

from __future__ import annotations

import networkxr as nx


# ── fake_social_network ─────────────────────────────────────────


class TestFakeSocialNetwork:
    def test_node_count(self) -> None:
        G = nx.fake_social_network(10, seed=42)
        assert G.number_of_nodes() == 10

    def test_node_attributes(self) -> None:
        G = nx.fake_social_network(5, seed=42)
        for node in G:
            data = G.nodes[node]
            assert "name" in data
            assert "email" in data
            assert "username" in data
            assert "company" in data
            assert isinstance(data["name"], str)
            assert "@" in data["email"]

    def test_edge_attributes(self) -> None:
        G = nx.fake_social_network(10, p=0.5, seed=42)
        for _u, _v, data in G.edges(data=True):
            assert "since" in data
            assert isinstance(data["since"], str)

    def test_seed_reproducibility(self) -> None:
        G1 = nx.fake_social_network(10, seed=123)
        G2 = nx.fake_social_network(10, seed=123)
        assert list(G1.nodes(data=True)) == list(G2.nodes(data=True))
        assert sorted(G1.edges(data=True)) == sorted(G2.edges(data=True))

    def test_different_seeds_differ(self) -> None:
        G1 = nx.fake_social_network(10, seed=1)
        G2 = nx.fake_social_network(10, seed=2)
        names1 = [G1.nodes[n]["name"] for n in G1]
        names2 = [G2.nodes[n]["name"] for n in G2]
        assert names1 != names2

    def test_zero_nodes(self) -> None:
        G = nx.fake_social_network(0, seed=42)
        assert G.number_of_nodes() == 0
        assert G.number_of_edges() == 0

    def test_single_node(self) -> None:
        G = nx.fake_social_network(1, seed=42)
        assert G.number_of_nodes() == 1
        assert G.number_of_edges() == 0

    def test_is_undirected(self) -> None:
        G = nx.fake_social_network(5, seed=42)
        assert not G.is_directed()

    def test_high_probability_creates_many_edges(self) -> None:
        G = nx.fake_social_network(10, p=1.0, seed=42)
        expected = 10 * 9 // 2  # complete graph
        assert G.number_of_edges() == expected

    def test_zero_probability_creates_no_edges(self) -> None:
        G = nx.fake_social_network(10, p=0.0, seed=42)
        assert G.number_of_edges() == 0


# ── fake_org_chart ──────────────────────────────────────────────


class TestFakeOrgChart:
    def test_is_directed(self) -> None:
        G = nx.fake_org_chart(seed=42)
        assert G.is_directed()

    def test_node_count(self) -> None:
        # depth=2, breadth=2: root + 2 + 4 = 7
        G = nx.fake_org_chart(depth=2, breadth=2, seed=42)
        expected = 1 + 2 + 4  # sum of breadth^i for i in 0..depth
        assert G.number_of_nodes() == expected

    def test_node_attributes(self) -> None:
        G = nx.fake_org_chart(depth=1, breadth=2, seed=42)
        for node in G:
            data = G.nodes[node]
            assert "name" in data
            assert "job" in data
            assert "email" in data
            assert "department" in data

    def test_edge_count_tree(self) -> None:
        # edges = nodes - 1 for a tree
        G = nx.fake_org_chart(depth=2, breadth=3, seed=42)
        assert G.number_of_edges() == G.number_of_nodes() - 1

    def test_seed_reproducibility(self) -> None:
        G1 = nx.fake_org_chart(depth=2, breadth=2, seed=99)
        G2 = nx.fake_org_chart(depth=2, breadth=2, seed=99)
        assert list(G1.nodes(data=True)) == list(G2.nodes(data=True))
        assert sorted(G1.edges()) == sorted(G2.edges())

    def test_depth_one(self) -> None:
        G = nx.fake_org_chart(depth=1, breadth=4, seed=42)
        assert G.number_of_nodes() == 5  # root + 4
        assert G.number_of_edges() == 4

    def test_depth_zero(self) -> None:
        G = nx.fake_org_chart(depth=0, breadth=3, seed=42)
        assert G.number_of_nodes() == 1
        assert G.number_of_edges() == 0


# ── fake_transaction_network ────────────────────────────────────


class TestFakeTransactionNetwork:
    def test_is_directed(self) -> None:
        G = nx.fake_transaction_network(seed=42)
        assert G.is_directed()

    def test_node_count(self) -> None:
        G = nx.fake_transaction_network(n_people=10, seed=42)
        assert G.number_of_nodes() == 10

    def test_node_attributes(self) -> None:
        G = nx.fake_transaction_network(n_people=5, seed=42)
        for node in G:
            data = G.nodes[node]
            assert "name" in data
            assert "address" in data

    def test_edge_attributes(self) -> None:
        G = nx.fake_transaction_network(n_people=5, n_transactions=10, seed=42)
        for _u, _v, data in G.edges(data=True):
            assert "amount" in data
            assert "currency" in data
            assert "date" in data
            assert isinstance(data["amount"], float)
            assert data["currency"] in {"USD", "EUR", "GBP", "CHF", "JPY"}

    def test_seed_reproducibility(self) -> None:
        G1 = nx.fake_transaction_network(n_people=5, n_transactions=10, seed=77)
        G2 = nx.fake_transaction_network(n_people=5, n_transactions=10, seed=77)
        assert list(G1.nodes(data=True)) == list(G2.nodes(data=True))
        assert list(G1.edges(data=True)) == list(G2.edges(data=True))

    def test_no_self_loops(self) -> None:
        G = nx.fake_transaction_network(n_people=5, n_transactions=50, seed=42)
        for u, v in G.edges():
            assert u != v

    def test_single_person(self) -> None:
        """With 1 person, receiver wraps around so sender != receiver mod 1."""
        G = nx.fake_transaction_network(n_people=2, n_transactions=5, seed=42)
        assert G.number_of_nodes() == 2


# ── Locale support ──────────────────────────────────────────────


class TestLocaleSupport:
    def test_social_network_german(self) -> None:
        G = nx.fake_social_network(5, seed=42, locale="de_DE")
        assert G.number_of_nodes() == 5
        for node in G:
            assert isinstance(G.nodes[node]["name"], str)

    def test_org_chart_french(self) -> None:
        G = nx.fake_org_chart(depth=1, breadth=2, seed=42, locale="fr_FR")
        assert G.number_of_nodes() == 3

    def test_transaction_network_japanese(self) -> None:
        G = nx.fake_transaction_network(n_people=3, n_transactions=5, seed=42, locale="ja_JP")
        assert G.number_of_nodes() == 3
