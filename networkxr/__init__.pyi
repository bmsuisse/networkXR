"""Type stubs for networkxr — drop-in replacement for NetworkX (Rust-accelerated)."""

from networkxr.classes.digraph import DiGraph as DiGraph
from networkxr.classes.graph import Graph as Graph
from networkxr.convert import (
    from_dict_of_dicts as from_dict_of_dicts,
    from_dict_of_lists as from_dict_of_lists,
    to_dict_of_dicts as to_dict_of_dicts,
    to_dict_of_lists as to_dict_of_lists,
    to_edgelist as to_edgelist,
    to_networkx_graph as to_networkx_graph,
)
from networkxr.exception import (
    AmbiguousSolution as AmbiguousSolution,
    ExceededMaxIterations as ExceededMaxIterations,
    HasACycle as HasACycle,
    NetworkXAlgorithmError as NetworkXAlgorithmError,
    NetworkXError as NetworkXError,
    NetworkXException as NetworkXException,
    NetworkXNoCycle as NetworkXNoCycle,
    NetworkXNoPath as NetworkXNoPath,
    NetworkXPointlessConcept as NetworkXPointlessConcept,
    NetworkXUnbounded as NetworkXUnbounded,
    NetworkXUnfeasible as NetworkXUnfeasible,
    NodeNotFound as NodeNotFound,
    PowerIterationFailedConvergence as PowerIterationFailedConvergence,
)
from networkxr.generators.classic import (
    barbell_graph as barbell_graph,
    complete_graph as complete_graph,
    cycle_graph as cycle_graph,
    empty_graph as empty_graph,
    path_graph as path_graph,
    star_graph as star_graph,
)
from networkxr.generators.fake import (
    fake_org_chart as fake_org_chart,
    fake_social_network as fake_social_network,
    fake_transaction_network as fake_transaction_network,
)
from networkxr.isomorphism import is_isomorphic as is_isomorphic
from networkxr.multigraph import MultiDiGraph as MultiDiGraph, MultiGraph as MultiGraph
from networkxr.relabel import (
    convert_node_labels_to_integers as convert_node_labels_to_integers,
    relabel_nodes as relabel_nodes,
)
from networkxr.removed import random_tree as random_tree
from networkxr.utils.misc import (
    edges_equal as edges_equal,
    flatten as flatten,
    graphs_equal as graphs_equal,
    nodes_equal as nodes_equal,
    pairwise as pairwise,
)

__version__: str
__all__: list[str]
