#!/usr/bin/env python3
"""gen_api_reference.py — Auto-generate docs/api-reference.md from Python docstrings.

Run from the repository root:
    uv run python scripts/gen_api_reference.py

Introspects the live ``networkxr`` package and emits a single Markdown file
with full signatures, docstrings, and type hints for every public symbol.
"""

from __future__ import annotations

import inspect
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.parent


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------


def _format_signature(obj: Any) -> str:
    """Return a clean function/class signature string."""
    try:
        sig = inspect.signature(obj)
        return str(sig)
    except (ValueError, TypeError):
        return "(...)"


def _format_symbol(name: str, obj: Any, *, level: int = 3) -> str:
    """Format a single symbol (function or class) as Markdown."""
    heading = "#" * level
    lines: list[str] = []

    if inspect.isclass(obj):
        lines.append(f"{heading} `class {name}`")
        lines.append("")
        doc = inspect.getdoc(obj) or ""
        if doc:
            lines.append(doc)
            lines.append("")

        # Document public methods
        methods = [
            (mname, mobj)
            for mname, mobj in inspect.getmembers(obj, predicate=inspect.isfunction)
            if not mname.startswith("_") or mname == "__init__"
        ]
        # Also include properties
        for mname in dir(obj):
            if mname.startswith("_"):
                continue
            attr = getattr(obj, mname, None)
            if isinstance(attr, property) or (
                hasattr(type(obj), mname) and isinstance(getattr(type(obj), mname), property)
            ):
                lines.append(f"{'#' * (level + 1)} `{name}.{mname}` *(property)*")
                lines.append("")
                pdoc = inspect.getdoc(attr.fget) if hasattr(attr, "fget") and attr.fget else ""
                if pdoc:
                    lines.append(pdoc)
                    lines.append("")

        for mname, mobj in methods:
            sig = _format_signature(mobj)
            lines.append(f"{'#' * (level + 1)} `{name}.{mname}{sig}`")
            lines.append("")
            mdoc = inspect.getdoc(mobj) or ""
            if mdoc:
                lines.append(mdoc)
                lines.append("")
    else:
        sig = _format_signature(obj)
        lines.append(f"{heading} `{name}{sig}`")
        lines.append("")
        doc = inspect.getdoc(obj) or ""
        if doc:
            lines.append(doc)
            lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main builder
# ---------------------------------------------------------------------------


def build_api_reference() -> str:
    """Build the full API reference Markdown document."""
    import networkxr
    import networkxr.convert as convert_mod
    import networkxr.exception as exc_mod
    import networkxr.generators.classic as gen_mod
    import networkxr.isomorphism as iso_mod
    import networkxr.relabel as relabel_mod
    import networkxr.utils.misc as utils_mod

    output_lines: list[str] = []
    output_lines.append("# API Reference")
    output_lines.append("")
    output_lines.append(
        "Auto-generated from the live `networkxr` package. "
        "All signatures, type hints, and docstrings are extracted at build time."
    )
    output_lines.append("")

    # ------------------------------------------------------------------
    # 1. Core Graph Types
    # ------------------------------------------------------------------
    output_lines.append("## Core Graph Types")
    output_lines.append("")

    graph_classes: list[tuple[str, Any]] = [
        ("Graph", networkxr.Graph),
        ("DiGraph", networkxr.DiGraph),
        ("MultiGraph", networkxr.MultiGraph),
        ("MultiDiGraph", networkxr.MultiDiGraph),
    ]
    for sym_name, obj in graph_classes:
        output_lines.append(_format_symbol(sym_name, obj, level=3))

    # ------------------------------------------------------------------
    # 2. Graph Generators
    # ------------------------------------------------------------------
    output_lines.append("## Graph Generators")
    output_lines.append("")

    generator_funcs: list[tuple[str, Any]] = [
        ("complete_graph", gen_mod.complete_graph),
        ("cycle_graph", gen_mod.cycle_graph),
        ("path_graph", gen_mod.path_graph),
        ("star_graph", gen_mod.star_graph),
        ("barbell_graph", gen_mod.barbell_graph),
        ("empty_graph", gen_mod.empty_graph),
    ]
    for sym_name, obj in generator_funcs:
        output_lines.append(_format_symbol(sym_name, obj, level=3))

    # ------------------------------------------------------------------
    # 3. Conversion Functions
    # ------------------------------------------------------------------
    output_lines.append("## Conversion Functions")
    output_lines.append("")

    convert_funcs: list[tuple[str, Any]] = [
        ("to_dict_of_dicts", convert_mod.to_dict_of_dicts),
        ("from_dict_of_dicts", convert_mod.from_dict_of_dicts),
        ("to_dict_of_lists", convert_mod.to_dict_of_lists),
        ("from_dict_of_lists", convert_mod.from_dict_of_lists),
        ("to_edgelist", convert_mod.to_edgelist),
        ("to_networkx_graph", convert_mod.to_networkx_graph),
    ]
    for sym_name, obj in convert_funcs:
        output_lines.append(_format_symbol(sym_name, obj, level=3))

    # ------------------------------------------------------------------
    # 4. Relabeling
    # ------------------------------------------------------------------
    output_lines.append("## Relabeling")
    output_lines.append("")

    relabel_funcs: list[tuple[str, Any]] = [
        ("relabel_nodes", relabel_mod.relabel_nodes),
        ("convert_node_labels_to_integers", relabel_mod.convert_node_labels_to_integers),
    ]
    for sym_name, obj in relabel_funcs:
        output_lines.append(_format_symbol(sym_name, obj, level=3))

    # ------------------------------------------------------------------
    # 5. Isomorphism
    # ------------------------------------------------------------------
    output_lines.append("## Isomorphism")
    output_lines.append("")

    iso_funcs: list[tuple[str, Any]] = [
        ("is_isomorphic", iso_mod.is_isomorphic),
    ]
    for sym_name, obj in iso_funcs:
        output_lines.append(_format_symbol(sym_name, obj, level=3))

    # ------------------------------------------------------------------
    # 6. Exceptions
    # ------------------------------------------------------------------
    output_lines.append("## Exceptions")
    output_lines.append("")
    output_lines.append(
        "networkXR provides the full NetworkX exception hierarchy for compatibility."
    )
    output_lines.append("")

    exception_classes: list[tuple[str, Any]] = [
        ("NetworkXException", exc_mod.NetworkXException),
        ("NetworkXError", exc_mod.NetworkXError),
        ("NetworkXAlgorithmError", exc_mod.NetworkXAlgorithmError),
        ("NetworkXNoPath", exc_mod.NetworkXNoPath),
        ("NetworkXNoCycle", exc_mod.NetworkXNoCycle),
        ("NetworkXUnfeasible", exc_mod.NetworkXUnfeasible),
        ("NetworkXUnbounded", exc_mod.NetworkXUnbounded),
        ("NetworkXPointlessConcept", exc_mod.NetworkXPointlessConcept),
        ("NodeNotFound", exc_mod.NodeNotFound),
        ("HasACycle", exc_mod.HasACycle),
        ("AmbiguousSolution", exc_mod.AmbiguousSolution),
        ("ExceededMaxIterations", exc_mod.ExceededMaxIterations),
        ("PowerIterationFailedConvergence", exc_mod.PowerIterationFailedConvergence),
    ]
    for sym_name, obj in exception_classes:
        output_lines.append(_format_symbol(sym_name, obj, level=3))

    # ------------------------------------------------------------------
    # 7. Utilities
    # ------------------------------------------------------------------
    output_lines.append("## Utilities")
    output_lines.append("")

    util_funcs: list[tuple[str, Any]] = [
        ("nodes_equal", utils_mod.nodes_equal),
        ("edges_equal", utils_mod.edges_equal),
        ("graphs_equal", utils_mod.graphs_equal),
        ("flatten", utils_mod.flatten),
        ("pairwise", utils_mod.pairwise),
    ]
    for sym_name, obj in util_funcs:
        output_lines.append(_format_symbol(sym_name, obj, level=3))

    return "\n".join(output_lines) + "\n"


def build_api_schema() -> str:
    """Build a JSON schema of the public API."""
    import networkxr
    import networkxr.convert as convert_mod
    import networkxr.generators.classic as gen_mod
    import networkxr.relabel as relabel_mod
    import networkxr.utils.misc as utils_mod

    def _get_type_str(annotation: Any) -> str:
        if annotation == inspect._empty:
            return "Any"
        return str(annotation).replace("typing.", "")

    def _serialize_func(obj: Any) -> dict[str, Any]:
        try:
            sig = inspect.signature(obj)
            params = {
                k: _get_type_str(v.annotation)
                for k, v in sig.parameters.items()
                if k not in ("self", "cls")
            }
            ret = _get_type_str(sig.return_annotation)
            doc = inspect.getdoc(obj) or ""
            return {"parameters": params, "returns": ret, "doc": doc.split("\n")[0]}
        except Exception:
            return {}

    def _serialize_class(cls: type) -> dict[str, Any]:
        methods: dict[str, Any] = {}
        for name, val in inspect.getmembers(cls, predicate=inspect.isroutine):
            if name.startswith("_") and name != "__init__":
                continue
            if name in cls.__dict__ or name == "__init__":
                methods[name] = _serialize_func(val)
        return {"methods": methods, "doc": (inspect.getdoc(cls) or "").split("\n")[0]}

    schema: dict[str, Any] = {"classes": {}, "functions": {}}

    # Classes
    class_names = ["Graph", "DiGraph", "MultiGraph", "MultiDiGraph"]
    for cn in class_names:
        schema["classes"][cn] = _serialize_class(getattr(networkxr, cn))

    # Functions
    func_map = {
        "complete_graph": gen_mod.complete_graph,
        "cycle_graph": gen_mod.cycle_graph,
        "path_graph": gen_mod.path_graph,
        "star_graph": gen_mod.star_graph,
        "barbell_graph": gen_mod.barbell_graph,
        "empty_graph": gen_mod.empty_graph,
        "to_dict_of_dicts": convert_mod.to_dict_of_dicts,
        "from_dict_of_dicts": convert_mod.from_dict_of_dicts,
        "to_dict_of_lists": convert_mod.to_dict_of_lists,
        "from_dict_of_lists": convert_mod.from_dict_of_lists,
        "to_edgelist": convert_mod.to_edgelist,
        "to_networkx_graph": convert_mod.to_networkx_graph,
        "relabel_nodes": relabel_mod.relabel_nodes,
        "convert_node_labels_to_integers": relabel_mod.convert_node_labels_to_integers,
        "nodes_equal": utils_mod.nodes_equal,
        "edges_equal": utils_mod.edges_equal,
        "graphs_equal": utils_mod.graphs_equal,
        "flatten": utils_mod.flatten,
        "pairwise": utils_mod.pairwise,
    }
    for fn_name, fn_obj in func_map.items():
        schema["functions"][fn_name] = _serialize_func(fn_obj)

    return json.dumps(schema, indent=2)


def main() -> None:
    target = ROOT / "docs" / "api-reference.md"
    schema_target = ROOT / "docs" / "schema.json"
    print("Generating API reference and JSON schema …")
    try:
        content = build_api_reference()
        schema_content = build_api_schema()
    except Exception as e:
        print(f"ERROR: Failed to generate docs: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)
    target.write_text(content, encoding="utf-8")
    schema_target.write_text(schema_content, encoding="utf-8")
    print(f"✔ Wrote {target.relative_to(ROOT)}  ({len(content):,} chars)")
    print(f"✔ Wrote {schema_target.relative_to(ROOT)}  ({len(schema_content):,} chars)")


if __name__ == "__main__":
    main()
