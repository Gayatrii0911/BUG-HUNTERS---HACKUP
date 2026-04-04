# Sentinel-X Graph Intelligence Contract (Member 1)

This document locks the API and internal response schemas for the Graph/Relationship module.

## 1. Internal `generate_signals` Output
The `backend.graph.algorithms.generate_signals` function returns a dictionary with a `signals` key.

**Keys in `signals`**:
- `has_cycle` (bool): `True` if the transaction completes a loop.
- `cycle_path` (list): Ordered list of account IDs forming the loop (ex: `["A", "B", "C", "A"]`).
- `is_hub` (bool): `True` if the sender has >= 5 unique connections.
- `is_relay` (bool): `True` if account redistributes funds rapidly (high in-degree and out-degree).
- `suspicious_chain` (bool): `True` if part of a multi-hop (4+) flow or high-velocity layering.
- `chain_paths` (list): Top 2 longest or high-velocity paths found during tracing.
- `is_smurfing` (bool): `True` if multiple small transactions between same nodes in short window.
- `is_cluster` (bool): `True` if node is part of a dense network clique.
- `score` (int/float): Aggregated graph risk sub-score (0-100).
- `graph_risk` (int/float): Alias for score (for internal use).
- `connections` (int): Total unique predecessors + successors.

## 2. Trace API Response (`GET /trace/{account_id}`)
Located at `backend/routes/trace.py`.

**Response Schema**:
```json
{
  "account_id": "string",
  "paths_found": 0,
  "depth_limit": 4,
  "trace_paths": [
    ["A", "B", "C"],
    ["A", "X", "Y"]
  ],
  "is_suspicious": bool,
  "summary": {
    "max_hop": 3,
    "unique_destinations": 2,
    "has_cycle": false
  }
}
```

## 3. Graph Payload for Frontend (`formatter.py`)
Used for Cytoscape.js visualization.

**Response Schema**:
```json
{
  "nodes": [
    { "data": { "id": "A", "label": "A", "risk_score": 0, "is_fraudulent": false } }
  ],
  "edges": [
    { "data": { "id": "A-B-0", "source": "A", "target": "B", "amount": 100, "timestamp": 1234.56 } }
  ]
}
```

## 4. Integration Verification status
- [x] Trace router mounted in `main.py`
- [x] Contract consumed by `risk/scoring.py`
- [x] Graph updated in real-time by `services/transaction_service.py`
- [x] Formatter compatible with Cytoscape JSON spec
