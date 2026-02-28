"""Type stubs for networkxr.convert."""

from typing import Any

def to_dict_of_dicts(
    G: Any,
    nodelist: list[Any] | None = None,
    edge_data: Any = None,
) -> dict[Any, dict[Any, Any]]: ...
def from_dict_of_dicts(
    d: dict[Any, dict[Any, Any]],
    create_using: Any = None,
    multigraph_input: bool = False,
) -> Any: ...
def to_dict_of_lists(
    G: Any,
    nodelist: list[Any] | None = None,
) -> dict[Any, list[Any]]: ...
def from_dict_of_lists(
    d: dict[Any, list[Any]],
    create_using: Any = None,
) -> Any: ...
def to_networkx_graph(
    data: Any,
    create_using: Any = None,
    multigraph_input: bool = False,
) -> Any: ...
def to_edgelist(
    G: Any,
    nodelist: list[Any] | None = None,
) -> list[tuple[Any, ...]]: ...
