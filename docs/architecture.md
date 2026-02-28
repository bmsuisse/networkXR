---
title: Architecture
---

# Architecture

networkXR is a **hybrid Rust + Python** library. Performance-critical graph data structures are implemented in Rust and exposed to Python via [PyO3](https://pyo3.rs), while higher-level functionality is implemented in pure Python.

---

## Layer Diagram

```
┌─────────────────────────────────────────────────┐
│                  Python API                      │
│  networkxr.Graph  ·  networkxr.DiGraph           │
│  networkxr.MultiGraph  ·  networkxr.MultiDiGraph │
│  generators  ·  convert  ·  relabel  ·  utils    │
├─────────────────────────────────────────────────┤
│               PyO3 Bindings                      │
│         networkxr._networkxr module              │
├─────────────────────────────────────────────────┤
│                Rust Core                         │
│     graph.rs  ·  digraph.rs  ·  views.rs         │
│          IndexMap-based adjacency                │
└─────────────────────────────────────────────────┘
```

---

## Rust Core

The Rust core lives in `src/` and provides the foundational graph data structures.

### Data Structures

Both `Graph` and `DiGraph` use [`IndexMap`](https://docs.rs/indexmap/) for:

- **Node storage**: `IndexMap<PyObject, Py<PyDict>>` — maps node keys to attribute dicts
- **Adjacency**: `IndexMap<PyObject, IndexMap<PyObject, Py<PyDict>>>` — maps node → neighbor → edge attributes

`IndexMap` preserves insertion order (like Python's `dict`) while providing O(1) average-case lookups.

### Files

| File | Description |
|------|-------------|
| `src/graph.rs` | `Graph` — undirected simple graph (~716 lines) |
| `src/digraph.rs` | `DiGraph` — directed simple graph (~849 lines) |
| `src/views.rs` | `NodeView`, `EdgeView`, `DegreeView` — lazy view objects |
| `src/lib.rs` | PyO3 module registration |

### Key Design Decisions

- **Hash-based equality**: Node keys are compared using Python's `__hash__` and `__eq__` protocols via `py_hash_eq()` helper functions.
- **Symmetric adjacency**: `Graph` maintains symmetric adjacency — adding edge `(u, v)` updates both `adj[u][v]` and `adj[v][u]` with the **same** `Py<PyDict>` reference.
- **Predecessor tracking**: `DiGraph` maintains both `succ` (forward adjacency) and `pred` (reverse adjacency) maps for O(1) predecessor lookups.

---

## Python Layer

Pure Python modules extend the Rust core with higher-level functionality.

### Files

| File | Description |
|------|-------------|
| `networkxr/multigraph.py` | `MultiGraph`, `MultiDiGraph` — parallel edge support |
| `networkxr/convert.py` | Conversion functions (dict ↔ graph) |
| `networkxr/relabel.py` | Node relabeling and integer conversion |
| `networkxr/generators/classic.py` | Classic graph generators (path, cycle, complete, etc.) |
| `networkxr/exception.py` | Full NetworkX exception hierarchy |
| `networkxr/isomorphism.py` | Simple graph isomorphism check (VF2-lite) |
| `networkxr/utils/misc.py` | Utility functions (equality checks, pairwise, flatten) |

### MultiGraph Implementation

`MultiGraph` and `MultiDiGraph` are implemented in pure Python (not Rust) because they require key-based edge indexing with auto-incrementing integer keys — a pattern that's naturally expressed in Python. They follow the same API patterns as `Graph` and `DiGraph`.

---

## Build System

networkXR uses [maturin](https://www.maturin.rs/) as the build backend:

```toml
[build-system]
requires = ["maturin>=1.9.4,<2"]
build-backend = "maturin"

[tool.maturin]
features = ["pyo3/extension-module"]
module-name = "networkxr._networkxr"
```

The compiled Rust extension is installed as `networkxr._networkxr`, and the Python `Graph` and `DiGraph` classes are imported from this module in `networkxr/__init__.py`.
