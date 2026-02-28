"""Type stubs for faker-powered graph generators."""

from typing import Any

def fake_social_network(
    n: int = 20,
    p: float = 0.15,
    seed: int | None = None,
    locale: str = "en_US",
    create_using: Any = None,
) -> Any: ...
def fake_org_chart(
    depth: int = 3,
    breadth: int = 3,
    seed: int | None = None,
    locale: str = "en_US",
    create_using: Any = None,
) -> Any: ...
def fake_transaction_network(
    n_people: int = 15,
    n_transactions: int = 30,
    seed: int | None = None,
    locale: str = "en_US",
    create_using: Any = None,
) -> Any: ...
