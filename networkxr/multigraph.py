"""MultiGraph and MultiDiGraph — pure Python implementations."""

from __future__ import annotations

from typing import Any

from networkxr.classes.views import MultiEdgeView, NodeView


class MultiGraph:
    """Undirected multigraph allowing parallel edges."""

    def __init__(self, incoming_graph_data: Any = None, **attr: Any) -> None:
        self.graph: dict[str, Any] = dict(attr)
        self._node: dict[Any, dict[str, Any]] = {}
        self._adj: dict[Any, dict[Any, dict[Any, dict[str, Any]]]] = {}
        self._key_count: dict[tuple[Any, Any], int] = {}

        if incoming_graph_data is not None:
            self._init_from_data(incoming_graph_data)

    def _init_from_data(self, data: Any) -> None:
        if isinstance(data, (MultiGraph, MultiDiGraph)):
            for n, dd in data.nodes(data=True):
                self.add_node(n, **dd)
            for u, v, key, dd in data.edges(data=True, keys=True):
                self.add_edge(u, v, key=key, **dd)
            self.graph.update(data.graph)
        elif hasattr(data, "nodes") and hasattr(data, "edges"):
            # Regular graph
            for n_data in data.nodes(data=True):
                if isinstance(n_data, tuple):
                    n, dd = n_data
                    self.add_node(n, **dd)
                else:
                    self.add_node(n_data)
            for e in data.edges(data=True):
                if isinstance(e, tuple) and len(e) == 3:
                    u, v, dd = e
                    self.add_edge(u, v, **dd)
                elif isinstance(e, tuple) and len(e) == 2:
                    self.add_edge(e[0], e[1])
            if hasattr(data, "graph") and isinstance(data.graph, dict):
                self.graph.update(data.graph)
        elif isinstance(data, dict):
            # Add all nodes first
            for u in data:
                self.add_node(u)
            for u, nbrs in data.items():
                if isinstance(nbrs, dict):
                    for v, edata in nbrs.items():
                        self.add_node(v)
                        if isinstance(edata, dict):
                            # Check if this is a keyed multi-edge dict {key: {attr...}}
                            first_inner = next(iter(edata.values()), None) if edata else None
                            if isinstance(first_inner, dict):
                                # 3-level: {u: {v: {key: {attr}}}}
                                for key, attr_dict in edata.items():
                                    self.add_edge(u, v, key=key, **attr_dict)
                            else:
                                self.add_edge(u, v, **edata)
                        else:
                            self.add_edge(u, v)
                elif isinstance(nbrs, list):
                    # Dict-of-lists format — dedup for undirected
                    for v in nbrs:
                        self.add_node(v)
                        if not self.is_directed():
                            if self.has_edge(u, v):
                                continue
                        self.add_edge(u, v)
        elif hasattr(data, "__iter__"):
            for item in data:
                if isinstance(item, (tuple, list)) and len(item) >= 2:
                    u, v = item[0], item[1]
                    dd = item[2] if len(item) >= 3 and isinstance(item[2], dict) else {}
                    self.add_edge(u, v, **dd)

    def is_multigraph(self) -> bool:
        return True

    def is_directed(self) -> bool:
        return False

    def add_node(self, n: Any, **attr: Any) -> None:
        if n not in self._node:
            self._node[n] = {}
            self._adj[n] = {}
        self._node[n].update(attr)

    def add_nodes_from(self, nodes: Any, **attr: Any) -> None:
        for item in nodes:
            if isinstance(item, tuple) and len(item) == 2:
                n, dd = item
                self.add_node(n, **dd, **attr)
            else:
                self.add_node(item, **attr)

    def remove_node(self, n: Any) -> None:
        if n not in self._node:
            msg = f"Node {n} not in graph"
            raise KeyError(msg)
        # Remove edges
        for nbr in list(self._adj[n]):
            if nbr in self._adj and n in self._adj[nbr]:
                del self._adj[nbr][n]
        del self._adj[n]
        del self._node[n]

    def add_edge(self, u: Any, v: Any, key: Any = None, **attr: Any) -> Any:
        self.add_node(u)
        self.add_node(v)

        if v not in self._adj[u]:
            self._adj[u][v] = {}
        if u not in self._adj[v]:
            self._adj[v][u] = {}

        if key is None:
            try:
                key = max((k for k in self._adj[u][v] if isinstance(k, int)), default=-1) + 1
            except (TypeError, ValueError):
                key = 0

        dd = dict(attr)
        self._adj[u][v][key] = dd
        if u != v:
            self._adj[v][u][key] = dd  # Share same dict reference

        return key

    def add_edges_from(self, ebunch: Any, **attr: Any) -> None:
        for e in ebunch:
            if isinstance(e, (tuple, list)):
                ne = len(e)
                if ne == 3:
                    u, v, dd = e
                    if isinstance(dd, dict):
                        self.add_edge(u, v, **{**attr, **dd})
                    else:
                        self.add_edge(u, v, **attr)
                elif ne == 2:
                    self.add_edge(e[0], e[1], **attr)
                elif ne == 4:
                    u, v, key, dd = e
                    if isinstance(dd, dict):
                        self.add_edge(u, v, key=key, **{**attr, **dd})
                    else:
                        self.add_edge(u, v, key=key, **attr)

    def add_weighted_edges_from(self, ebunch: Any, weight: str = "weight") -> None:
        for e in ebunch:
            u, v, w = e[0], e[1], e[2]
            self.add_edge(u, v, **{weight: w})

    def remove_edge(self, u: Any, v: Any, key: Any = None) -> None:
        if u in self._adj and v in self._adj[u]:
            if key is not None:
                if key in self._adj[u][v]:
                    del self._adj[u][v][key]
                    if u != v and u in self._adj[v]:
                        if key in self._adj[v][u]:
                            del self._adj[v][u][key]
            else:
                # Remove first key
                first_key = next(iter(self._adj[u][v]))
                del self._adj[u][v][first_key]
                if u != v and first_key in self._adj[v].get(u, {}):
                    del self._adj[v][u][first_key]

    def has_node(self, n: Any) -> bool:
        return n in self._node

    def has_edge(self, u: Any, v: Any, key: Any = None) -> bool:
        if u not in self._adj or v not in self._adj[u]:
            return False
        if key is not None:
            return key in self._adj[u][v]
        return len(self._adj[u][v]) > 0

    @property
    def nodes(self) -> NodeView:
        return NodeView(self)

    @property
    def edges(self) -> MultiEdgeView:
        return MultiEdgeView(self, directed=False)

    def degree(self, nbunch: Any = None) -> Any:
        if nbunch is not None:
            if nbunch in self._node:
                count = sum(len(keys) for keys in self._adj[nbunch].values())
                return count
            raise KeyError(f"Node {nbunch} not in graph")
        return [(n, sum(len(keys) for keys in self._adj[n].values())) for n in self._node]

    def neighbors(self, n: Any) -> list[Any]:
        if n not in self._adj:
            raise KeyError(f"Node {n} not in graph")
        return list(self._adj[n].keys())

    def number_of_nodes(self) -> int:
        return len(self._node)

    def number_of_edges(self) -> int:
        return len(self.edges())

    def copy(self) -> MultiGraph:
        G = MultiGraph()
        G.graph = dict(self.graph)
        for n, dd in self._node.items():
            G._node[n] = dict(dd)
            G._adj[n] = {}
        for u in self._adj:
            for v in self._adj[u]:
                G._adj[u][v] = {k: dict(dd) for k, dd in self._adj[u][v].items()}
        return G

    def clear(self) -> None:
        self._node.clear()
        self._adj.clear()
        self.graph.clear()

    def get_edge_data(self, u: Any, v: Any, key: Any = None, default: Any = None) -> Any:
        if u in self._adj and v in self._adj[u]:
            if key is not None:
                return self._adj[u][v].get(key, default)
            return dict(self._adj[u][v])
        return default

    @property
    def name(self) -> str:
        return self.graph.get("name", "")

    @name.setter
    def name(self, val: str) -> None:
        self.graph["name"] = val

    @property
    def adj(self) -> dict[Any, dict[Any, dict[Any, dict[str, Any]]]]:
        return self._adj

    def __contains__(self, n: Any) -> bool:
        return n in self._node

    def __len__(self) -> int:
        return len(self._node)

    def __iter__(self) -> Any:
        return iter(self._node)

    def __getitem__(self, n: Any) -> Any:
        if n not in self._adj:
            raise KeyError(f"Node {n} not in graph")
        return self._adj[n]

    def to_undirected(self) -> MultiGraph:
        return self.copy()

    def subgraph(self, nodes: Any) -> MultiGraph:
        node_set = set(nodes)
        G = MultiGraph()
        G.graph = dict(self.graph)
        for n in node_set:
            if n in self._node:
                G._node[n] = dict(self._node[n])
                G._adj[n] = {}
        for u in node_set:
            if u in self._adj:
                for v in self._adj[u]:
                    if v in node_set:
                        G._adj[u][v] = {k: dict(dd) for k, dd in self._adj[u][v].items()}
        return G


class MultiDiGraph:
    """Directed multigraph allowing parallel edges."""

    def __init__(self, incoming_graph_data: Any = None, **attr: Any) -> None:
        self.graph: dict[str, Any] = dict(attr)
        self._node: dict[Any, dict[str, Any]] = {}
        self._adj: dict[Any, dict[Any, dict[Any, dict[str, Any]]]] = {}
        self._pred: dict[Any, dict[Any, dict[Any, dict[str, Any]]]] = {}

        if incoming_graph_data is not None:
            self._init_from_data(incoming_graph_data)

    def _init_from_data(self, data: Any) -> None:
        if isinstance(data, (MultiGraph, MultiDiGraph)):
            for n, dd in data.nodes(data=True):
                self.add_node(n, **dd)
            if hasattr(data, "is_multigraph") and data.is_multigraph():
                for u, v, key, dd in data.edges(data=True, keys=True):
                    self.add_edge(u, v, key=key, **dd)
            else:
                for e in data.edges(data=True):
                    if len(e) == 3:
                        self.add_edge(e[0], e[1], **e[2])
                    else:
                        self.add_edge(e[0], e[1])
            self.graph.update(data.graph)
        elif hasattr(data, "nodes") and hasattr(data, "edges"):
            for n_data in data.nodes(data=True):
                if isinstance(n_data, tuple):
                    n, dd = n_data
                    self.add_node(n, **dd)
                else:
                    self.add_node(n_data)
            for e in data.edges(data=True):
                if isinstance(e, tuple) and len(e) == 3:
                    self.add_edge(e[0], e[1], **e[2])
                elif isinstance(e, tuple) and len(e) == 2:
                    self.add_edge(e[0], e[1])
            if hasattr(data, "graph") and isinstance(data.graph, dict):
                self.graph.update(data.graph)
        elif isinstance(data, dict):
            for u in data:
                self.add_node(u)
            for u, nbrs in data.items():
                if isinstance(nbrs, dict):
                    for v, edata in nbrs.items():
                        self.add_node(v)
                        if isinstance(edata, dict):
                            first_inner = next(iter(edata.values()), None) if edata else None
                            if isinstance(first_inner, dict):
                                for key, attr_dict in edata.items():
                                    self.add_edge(u, v, key=key, **attr_dict)
                            else:
                                self.add_edge(u, v, **edata)
                        else:
                            self.add_edge(u, v)
        elif hasattr(data, "__iter__"):
            for item in data:
                if isinstance(item, (tuple, list)) and len(item) >= 2:
                    u, v = item[0], item[1]
                    dd = item[2] if len(item) >= 3 and isinstance(item[2], dict) else {}
                    self.add_edge(u, v, **dd)

    def is_multigraph(self) -> bool:
        return True

    def is_directed(self) -> bool:
        return True

    def add_node(self, n: Any, **attr: Any) -> None:
        if n not in self._node:
            self._node[n] = {}
            self._adj[n] = {}
            self._pred[n] = {}
        self._node[n].update(attr)

    def add_nodes_from(self, nodes: Any, **attr: Any) -> None:
        for item in nodes:
            if isinstance(item, tuple) and len(item) == 2:
                n, dd = item
                self.add_node(n, **dd, **attr)
            else:
                self.add_node(item, **attr)

    def remove_node(self, n: Any) -> None:
        if n not in self._node:
            raise KeyError(f"Node {n} not in graph")
        for succ in list(self._adj[n]):
            if n in self._pred.get(succ, {}):
                del self._pred[succ][n]
        for pred in list(self._pred[n]):
            if n in self._adj.get(pred, {}):
                del self._adj[pred][n]
        del self._adj[n]
        del self._pred[n]
        del self._node[n]

    def add_edge(self, u: Any, v: Any, key: Any = None, **attr: Any) -> Any:
        self.add_node(u)
        self.add_node(v)

        if v not in self._adj[u]:
            self._adj[u][v] = {}
        if u not in self._pred[v]:
            self._pred[v][u] = {}

        if key is None:
            try:
                key = max((k for k in self._adj[u][v] if isinstance(k, int)), default=-1) + 1
            except (TypeError, ValueError):
                key = 0

        self._adj[u][v][key] = dict(attr)
        self._pred[v][u][key] = dict(attr)
        return key

    def add_edges_from(self, ebunch: Any, **attr: Any) -> None:
        for e in ebunch:
            if isinstance(e, (tuple, list)):
                ne = len(e)
                if ne == 3:
                    u, v, dd = e
                    if isinstance(dd, dict):
                        self.add_edge(u, v, **{**attr, **dd})
                    else:
                        self.add_edge(u, v, **attr)
                elif ne == 2:
                    self.add_edge(e[0], e[1], **attr)
                elif ne == 4:
                    u, v, key, dd = e
                    if isinstance(dd, dict):
                        self.add_edge(u, v, key=key, **{**attr, **dd})
                    else:
                        self.add_edge(u, v, key=key, **attr)

    def add_weighted_edges_from(self, ebunch: Any, weight: str = "weight") -> None:
        for e in ebunch:
            self.add_edge(e[0], e[1], **{weight: e[2]})

    def remove_edge(self, u: Any, v: Any, key: Any = None) -> None:
        if u in self._adj and v in self._adj[u]:
            if key is not None:
                if key in self._adj[u][v]:
                    del self._adj[u][v][key]
                    if u in self._pred[v] and key in self._pred[v][u]:
                        del self._pred[v][u][key]
            else:
                first_key = next(iter(self._adj[u][v]))
                del self._adj[u][v][first_key]
                if first_key in self._pred[v].get(u, {}):
                    del self._pred[v][u][first_key]

    def has_node(self, n: Any) -> bool:
        return n in self._node

    def has_edge(self, u: Any, v: Any, key: Any = None) -> bool:
        if u not in self._adj or v not in self._adj[u]:
            return False
        if key is not None:
            return key in self._adj[u][v]
        return len(self._adj[u][v]) > 0

    @property
    def nodes(self) -> NodeView:
        return NodeView(self)

    @property
    def edges(self) -> MultiEdgeView:
        return MultiEdgeView(self, directed=True)

    def degree(self, nbunch: Any = None) -> Any:
        if nbunch is not None:
            if nbunch in self._node:
                out_deg = sum(len(keys) for keys in self._adj[nbunch].values())
                in_deg = sum(len(keys) for keys in self._pred[nbunch].values())
                return out_deg + in_deg
            raise KeyError(f"Node {nbunch} not in graph")
        return [
            (
                n,
                sum(len(keys) for keys in self._adj[n].values())
                + sum(len(keys) for keys in self._pred[n].values()),
            )
            for n in self._node
        ]

    def in_degree(self, nbunch: Any = None) -> Any:
        if nbunch is not None:
            if nbunch in self._node:
                return sum(len(keys) for keys in self._pred[nbunch].values())
            raise KeyError(f"Node {nbunch} not in graph")
        return [(n, sum(len(keys) for keys in self._pred[n].values())) for n in self._node]

    def out_degree(self, nbunch: Any = None) -> Any:
        if nbunch is not None:
            if nbunch in self._node:
                return sum(len(keys) for keys in self._adj[nbunch].values())
            raise KeyError(f"Node {nbunch} not in graph")
        return [(n, sum(len(keys) for keys in self._adj[n].values())) for n in self._node]

    def successors(self, n: Any) -> list[Any]:
        return list(self._adj[n].keys())

    def predecessors(self, n: Any) -> list[Any]:
        return list(self._pred[n].keys())

    def neighbors(self, n: Any) -> list[Any]:
        return self.successors(n)

    def number_of_nodes(self) -> int:
        return len(self._node)

    def number_of_edges(self) -> int:
        return sum(len(keys) for nbrs in self._adj.values() for keys in nbrs.values())

    def copy(self) -> MultiDiGraph:
        G = MultiDiGraph()
        G.graph = dict(self.graph)
        for n, dd in self._node.items():
            G._node[n] = dict(dd)
            G._adj[n] = {}
            G._pred[n] = {}
        for u in self._adj:
            for v in self._adj[u]:
                G._adj[u][v] = {k: dict(dd) for k, dd in self._adj[u][v].items()}
        for v in self._pred:
            for u in self._pred[v]:
                G._pred[v][u] = {k: dict(dd) for k, dd in self._pred[v][u].items()}
        return G

    def clear(self) -> None:
        self._node.clear()
        self._adj.clear()
        self._pred.clear()
        self.graph.clear()

    def get_edge_data(self, u: Any, v: Any, key: Any = None, default: Any = None) -> Any:
        if u in self._adj and v in self._adj[u]:
            if key is not None:
                return self._adj[u][v].get(key, default)
            return dict(self._adj[u][v])
        return default

    @property
    def name(self) -> str:
        return self.graph.get("name", "")

    @name.setter
    def name(self, val: str) -> None:
        self.graph["name"] = val

    @property
    def adj(self) -> dict[Any, dict[Any, dict[Any, dict[str, Any]]]]:
        return self._adj

    def reverse(self, copy: bool = True) -> MultiDiGraph:
        if copy:
            G = MultiDiGraph()
            G.graph = dict(self.graph)
            for n, dd in self._node.items():
                G._node[n] = dict(dd)
                G._adj[n] = {}
                G._pred[n] = {}
            for u in self._adj:
                for v in self._adj[u]:
                    G._adj[v][u] = {k: dict(dd) for k, dd in self._adj[u][v].items()}
                    G._pred[u][v] = {k: dict(dd) for k, dd in self._adj[u][v].items()}
            return G
        else:
            self._adj, self._pred = self._pred, self._adj
            return self

    def to_undirected(self) -> MultiGraph:
        G = MultiGraph()
        G.graph = dict(self.graph)
        for n, dd in self._node.items():
            G._node[n] = dict(dd)
            G._adj[n] = {}
        for u in self._adj:
            for v in self._adj[u]:
                for key, dd in self._adj[u][v].items():
                    G.add_edge(u, v, key=key, **dd)
        return G

    def __contains__(self, n: Any) -> bool:
        return n in self._node

    def __len__(self) -> int:
        return len(self._node)

    def __iter__(self) -> Any:
        return iter(self._node)

    def __getitem__(self, n: Any) -> Any:
        if n not in self._adj:
            raise KeyError(f"Node {n} not in graph")
        return self._adj[n]
