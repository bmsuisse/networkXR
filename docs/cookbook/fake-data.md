# Fake Data Generators

networkXR ships with **faker-powered graph generators** that create realistic
test and example graphs populated with fake user data. Perfect for prototyping,
demos, and unit tests.

> **Requires:** `pip install faker`

## Social Network

Generate a random social graph where each person has a name, email, username,
and company. Connections are formed using the Erdős–Rényi model.

```python
import networkxr as nx

G = nx.fake_social_network(n=20, p=0.15, seed=42)

# Inspect a node
print(G.nodes[0])
# {'name': 'John Smith', 'email': 'jsmith@example.com',
#  'username': 'jsmith', 'company': 'Acme Corp'}

# Inspect an edge
for u, v, data in G.edges(data=True):
    print(f"{G.nodes[u]['name']} ↔ {G.nodes[v]['name']} (since {data['since']})")
    break
```

## Organisation Chart

Generate a tree-shaped directed org chart with managers and reports.

```python
G = nx.fake_org_chart(depth=3, breadth=3, seed=42)

print(f"Employees: {G.number_of_nodes()}")
print(f"Reporting lines: {G.number_of_edges()}")

# CEO is always node 0
ceo = G.nodes[0]
print(f"CEO: {ceo['name']} — {ceo['job']}")

# Direct reports
for report_id in G.successors(0):
    print(f"  └── {G.nodes[report_id]['name']} ({G.nodes[report_id]['job']})")
```

## Transaction Network

Generate a directed graph of financial transactions between people.

```python
G = nx.fake_transaction_network(n_people=15, n_transactions=30, seed=42)

# Find the largest transaction
largest = max(G.edges(data=True), key=lambda e: e[2]["amount"])
u, v, data = largest
print(
    f"{G.nodes[u]['name']} → {G.nodes[v]['name']}: "
    f"{data['amount']} {data['currency']} on {data['date']}"
)
```

## Localisation

All generators accept a `locale` parameter to produce data in different languages:

```python
# German names and addresses
G = nx.fake_social_network(10, seed=42, locale="de_DE")

# French org chart
G = nx.fake_org_chart(depth=2, breadth=2, seed=42, locale="fr_FR")

# Japanese transactions
G = nx.fake_transaction_network(5, 10, seed=42, locale="ja_JP")
```

## Reproducibility

Pass a `seed` for deterministic output — ideal for snapshot tests:

```python
G1 = nx.fake_social_network(10, seed=123)
G2 = nx.fake_social_network(10, seed=123)
assert list(G1.nodes(data=True)) == list(G2.nodes(data=True))
```
