"""Faker-powered graph generators for realistic test / example data.

All functions require the ``faker`` package (dev dependency).
Each generator accepts an optional ``seed`` for reproducibility
and an optional ``locale`` for localised fake data.
"""

from __future__ import annotations

import random
from typing import Any


def _make_faker(seed: int | None = None, locale: str = "en_US") -> Any:
    """Create a seeded Faker instance (lazy import to keep faker optional)."""
    try:
        from faker import Faker
    except ImportError as exc:
        msg = (
            "faker is required for fake graph generators. "
            "Install it with: pip install faker"
        )
        raise ImportError(msg) from exc

    fake = Faker(locale)
    if seed is not None:
        Faker.seed(seed)
        fake.seed_instance(seed)
    return fake


# ── Social Network ──────────────────────────────────────────────


def fake_social_network(
    n: int = 20,
    p: float = 0.15,
    seed: int | None = None,
    locale: str = "en_US",
    create_using: Any = None,
) -> Any:
    """Generate a random social network graph with realistic user data.

    Parameters
    ----------
    n : int
        Number of people (nodes).
    p : float
        Probability that any two people are connected (Erdős–Rényi model).
    seed : int or None
        Random seed for reproducibility.
    locale : str
        Faker locale (e.g. ``"de_DE"``, ``"fr_FR"``).
    create_using : graph constructor or None
        Use a specific graph type (default: ``Graph``).

    Returns
    -------
    Graph
        Undirected graph where each node has attributes:
        ``name``, ``email``, ``username``, ``company``.
        Each edge has a ``since`` attribute (ISO date string).

    Examples
    --------
    >>> import networkxr as nx
    >>> G = nx.fake_social_network(10, seed=42)
    >>> G.number_of_nodes()
    10
    >>> G.nodes[0]["name"]  # random fake name
    '...'
    """
    from networkxr import Graph

    fake = _make_faker(seed, locale)
    rng = random.Random(seed)

    if create_using is not None:
        G = create_using() if isinstance(create_using, type) else create_using
    else:
        G = Graph()

    # -- nodes --
    for i in range(n):
        G.add_node(
            i,
            name=fake.name(),
            email=fake.email(),
            username=fake.user_name(),
            company=fake.company(),
        )

    # -- edges (Erdős–Rényi) --
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                G.add_edge(i, j, since=fake.date())

    return G


# ── Org Chart ───────────────────────────────────────────────────


def fake_org_chart(
    depth: int = 3,
    breadth: int = 3,
    seed: int | None = None,
    locale: str = "en_US",
    create_using: Any = None,
) -> Any:
    """Generate a tree-shaped directed org chart.

    Parameters
    ----------
    depth : int
        Number of management levels below the root.
    breadth : int
        Number of direct reports per manager.
    seed : int or None
        Random seed for reproducibility.
    locale : str
        Faker locale.
    create_using : graph constructor or None
        Use a specific graph type (default: ``DiGraph``).

    Returns
    -------
    DiGraph
        Directed tree where each node has attributes:
        ``name``, ``job``, ``email``, ``department``.
        Edge direction is manager → report.

    Examples
    --------
    >>> import networkxr as nx
    >>> G = nx.fake_org_chart(depth=2, breadth=2, seed=42)
    >>> G.is_directed()
    True
    """
    from networkxr import DiGraph

    fake = _make_faker(seed, locale)

    if create_using is not None:
        G = create_using() if isinstance(create_using, type) else create_using
    else:
        G = DiGraph()

    node_id = 0

    def _add_person() -> int:
        nonlocal node_id
        nid = node_id
        node_id += 1
        G.add_node(
            nid,
            name=fake.name(),
            job=fake.job(),
            email=fake.email(),
            department=fake.bs(),
        )
        return nid

    def _build(parent: int, level: int) -> None:
        if level >= depth:
            return
        for _ in range(breadth):
            child = _add_person()
            G.add_edge(parent, child)
            _build(child, level + 1)

    root = _add_person()
    _build(root, 0)
    return G


# ── Transaction Network ────────────────────────────────────────


def fake_transaction_network(
    n_people: int = 15,
    n_transactions: int = 30,
    seed: int | None = None,
    locale: str = "en_US",
    create_using: Any = None,
) -> Any:
    """Generate a directed transaction network.

    Parameters
    ----------
    n_people : int
        Number of people (nodes).
    n_transactions : int
        Number of financial transactions (edges).
    seed : int or None
        Random seed for reproducibility.
    locale : str
        Faker locale.
    create_using : graph constructor or None
        Use a specific graph type (default: ``DiGraph``).

    Returns
    -------
    DiGraph
        Directed graph where each node has attributes:
        ``name``, ``address``.
        Each edge has attributes:
        ``amount`` (float), ``currency`` (str), ``date`` (ISO date str).

    Examples
    --------
    >>> import networkxr as nx
    >>> G = nx.fake_transaction_network(10, 20, seed=42)
    >>> G.is_directed()
    True
    """
    from networkxr import DiGraph

    fake = _make_faker(seed, locale)
    rng = random.Random(seed)

    if create_using is not None:
        G = create_using() if isinstance(create_using, type) else create_using
    else:
        G = DiGraph()

    # -- nodes --
    for i in range(n_people):
        G.add_node(
            i,
            name=fake.name(),
            address=fake.address(),
        )

    # -- edges --
    currencies = ["USD", "EUR", "GBP", "CHF", "JPY"]
    for _ in range(n_transactions):
        sender = rng.randint(0, n_people - 1)
        receiver = rng.randint(0, n_people - 1)
        if sender == receiver:
            receiver = (receiver + 1) % n_people
        G.add_edge(
            sender,
            receiver,
            amount=round(rng.uniform(10.0, 10_000.0), 2),
            currency=rng.choice(currencies),
            date=fake.date(),
        )

    return G
