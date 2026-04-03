# Graph Output Contract (FROZEN)

This is the exact JSON structure that Member 2 and Member 3 can rely on from the graph module.

## 1. Graph Signals (Used by Member 2 for ML/Risk)
Generated upon transaction insertion.
```json
{
  "cycle": true,
  "cycle_path": ["A101", "B202", "C303", "A101"],
  "is_hub": false,
  "connections": 3,
  "suspicious_chain": true,
  "long_paths": [["A101", "B202", "C303", "D404", "E505"]],
  "high_frequency": false,
  "amount": 5000.0,
  "graph_risk": 60,
  "graph_explanations": [
    "Cycle path found: A101 -> B202 -> C303 -> A101",
    "Suspicious chain detected spanning 4 hops within limits"
  ]
}
```

## 2. Trace Response (Used by Member 3 for Frontend/Dashboard)
Returned from `GET /trace/{account}`.
```json
{
  "status": "success",
  "account": "A101",
  "paths": [["A101", "B202"]],
  "path_count": 1,
  "max_path_length": 2,
  "suspicious_paths": [],
  "related_accounts_summary": ["A101", "B202"],
  "max_depth": 4,
  "graph_payload": {
    "nodes": [{"data": {"id": "A101", "label": "A101", "type": "account"}}],
    "edges": [{"data": {"id": "A101-B202-0", "source": "A101", "target": "B202", "amount": 5000.0}}]
  }
}
```
