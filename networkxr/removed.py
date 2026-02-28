"""Stubs for removed NetworkX functions — raise helpful deprecation messages."""

from __future__ import annotations


def random_tree(*args: object, **kwargs: object) -> None:
    """random_tree was removed in NetworkX 3.2."""
    msg = "random_tree is removed from NetworkX. Use `nx.random_labeled_tree` instead."
    raise AttributeError(msg)
