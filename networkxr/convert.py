"""Convert between graph representations — NetworkX-compatible API."""

from __future__ import annotations

from typing import Any


def to_dict_of_dicts(
    G: Any,
    nodelist: list[Any] | None = None,
    edge_data: Any = None,
) -> dict[Any, dict[Any, Any]]:
    """Return adjacency representation of graph as a dict of dicts."""
    if nodelist is None:
        nodelist = list(G.nodes())

    dod: dict[Any, dict[Any, Any]] = {}
    for u in nodelist:
        dod[u] = {}
        for v in G.neighbors(u):
            if v in nodelist or (nodelist is None):
                pass
            # Check if v is in nodelist
            in_nodelist = False
            for n in nodelist:
                if n == v:
                    in_nodelist = True
                    break
            if not in_nodelist:
                continue
            if edge_data is not None:
                dod[u][v] = edge_data
            else:
                data = G.get_edge_data(u, v)
                if isinstance(data, dict):
                    # For multigraphs, data is dict of key->attr_dict
                    # Check if this is a multigraph
                    if hasattr(G, "is_multigraph") and G.is_multigraph():
                        dod[u][v] = data
                    else:
                        dod[u][v] = data
                else:
                    dod[u][v] = data if data is not None else {}
    return dod


def from_dict_of_dicts(
    d: dict[Any, dict[Any, Any]],
    create_using: Any = None,
    multigraph_input: bool = False,
) -> Any:
    """Return a graph from a dict of dicts."""
    from networkxr import Graph

    if create_using is None:
        G = Graph()
    elif isinstance(create_using, type):
        G = create_using()
    else:
        G = create_using

    is_multi = hasattr(G, "is_multigraph") and G.is_multigraph()

    if is_multi and multigraph_input:
        # d[u][v] = {key: attr_dict}
        for u, nbrs in d.items():
            G.add_node(u)
            for v, keydict in nbrs.items():
                G.add_node(v)
                if isinstance(keydict, dict):
                    for key, attr in keydict.items():
                        if isinstance(attr, dict):
                            G.add_edge(u, v, key=key, **attr)
                        else:
                            G.add_edge(u, v, key=key)
    else:
        for u, nbrs in d.items():
            G.add_node(u)
            for v, data in nbrs.items():
                G.add_node(v)
                if isinstance(data, dict):
                    # Check for 3-level nesting (multigraph: {key: {attr}})
                    first_inner = next(iter(data.values()), None) if data else None
                    if isinstance(first_inner, dict):
                        merged: dict[str, Any] = {}
                        for _key, attr_dict in data.items():
                            merged.update(attr_dict)
                        G.add_edge(u, v, **merged)
                    else:
                        G.add_edge(u, v, **data)
                else:
                    G.add_edge(u, v)

    return G


def to_dict_of_lists(
    G: Any,
    nodelist: list[Any] | None = None,
) -> dict[Any, list[Any]]:
    """Return adjacency representation of graph as a dict of lists."""
    if nodelist is None:
        nodelist = list(G.nodes())

    dol: dict[Any, list[Any]] = {n: [] for n in nodelist}
    for u in nodelist:
        for v in G.neighbors(u):
            in_nodelist = False
            for n in nodelist:
                if n == v:
                    in_nodelist = True
                    break
            if in_nodelist:
                dol[u].append(v)
    return dol


def from_dict_of_lists(
    d: dict[Any, list[Any]],
    create_using: Any = None,
) -> Any:
    """Return a graph from a dict of lists."""
    from networkxr import Graph

    if create_using is None:
        G = Graph()
    elif isinstance(create_using, type):
        G = create_using()
    else:
        G = create_using

    is_directed = hasattr(G, "is_directed") and G.is_directed()
    seen: set[tuple[Any, Any]] = set()

    for node, nbrs in d.items():
        G.add_node(node)
        for nbr in nbrs:
            if not is_directed:
                if (nbr, node) in seen:
                    continue
                seen.add((node, nbr))
            G.add_edge(node, nbr)

    return G


def to_networkx_graph(
    data: Any,
    create_using: Any = None,
    multigraph_input: bool = False,
) -> Any:
    """Convert various data formats to a NetworkX graph."""
    from networkxr import Graph, NetworkXError

    if create_using is None:
        G = Graph()
    elif isinstance(create_using, type):
        G = create_using()
    else:
        G = create_using

    # Already a graph?
    if hasattr(data, "adj") and hasattr(data, "nodes"):
        # Copy graph data
        for n_data in data.nodes(data=True):
            if isinstance(n_data, tuple):
                n, dd = n_data
                G.add_node(n, **dd)
            else:
                G.add_node(n_data)
        for edge_data in data.edges(data=True):
            if isinstance(edge_data, tuple) and len(edge_data) == 3:
                u, v, dd = edge_data
                G.add_edge(u, v, **dd)
            elif isinstance(edge_data, tuple) and len(edge_data) == 2:
                u, v = edge_data
                G.add_edge(u, v)
        return G

    # adj attribute but no nodes — probably a broken graph-like object
    if hasattr(data, "adj"):
        msg = "Input is not a valid graph-like object"
        raise NetworkXError(msg)

    # pygraphviz AGraph?
    if hasattr(data, "is_strict"):
        msg = "Input is not a valid graph-like object"
        raise NetworkXError(msg)

    # Dict of dicts or dict of lists?
    if isinstance(data, dict):
        # Check if dict of dicts vs dict of lists
        try:
            first_val = next(iter(data.values()))
        except StopIteration:
            return G

        if isinstance(first_val, dict):
            return from_dict_of_dicts(data, create_using=G, multigraph_input=multigraph_input)
        elif isinstance(first_val, list):
            return from_dict_of_lists(data, create_using=G)
        else:
            msg = "Input is not a known data type for conversion"
            raise TypeError(msg)

    # Check for "next" attribute (generator-like objects that aren't iterables)
    if hasattr(data, "next") and not hasattr(data, "__iter__"):
        msg = "Input is not a valid edge list"
        raise NetworkXError(msg)

    # Edgelist? (iterable of tuples)
    if hasattr(data, "__iter__"):
        # Could be an edge list
        try:
            for item in data:
                if isinstance(item, (tuple, list)):
                    if len(item) >= 2:
                        u, v = item[0], item[1]
                        G.add_node(u)
                        G.add_node(v)
                        if len(item) >= 3 and isinstance(item[2], dict):
                            G.add_edge(u, v, **item[2])
                        else:
                            G.add_edge(u, v)
                    else:
                        msg = "Input is not a valid edge list"
                        raise NetworkXError(msg)
                else:
                    msg = "Input is not a valid edge list"
                    raise NetworkXError(msg)
            return G
        except (TypeError, NetworkXError):
            raise

    msg = f"Input is not a known data type for conversion: {type(data)}"
    raise NetworkXError(msg)


def to_edgelist(G: Any, nodelist: list[Any] | None = None) -> list[tuple[Any, ...]]:
    """Return a list of edges in the graph."""
    if nodelist is None:
        return list(G.edges(data=True))
    else:
        result = []
        for u, v, d in G.edges(data=True):
            if u in nodelist and v in nodelist:
                result.append((u, v, d))
        return result
