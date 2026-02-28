"""Type stubs for networkxr.relabel."""

from collections.abc import Callable, Mapping
from typing import Any

def relabel_nodes(
    G: Any,
    mapping: Mapping[Any, Any] | Callable[[Any], Any],
    copy: bool = True,
) -> Any: ...
def convert_node_labels_to_integers(
    G: Any,
    first_label: int = 0,
    ordering: str = "default",
    label_attribute: str | None = None,
) -> Any: ...
