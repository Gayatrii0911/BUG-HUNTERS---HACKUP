# Fraud Detection System: Implementation Checklist

This checklist is based directly on the architectural blueprint and team division plan. It assigns specific files and functions to each member to ensure decoupled, parallel development.

## Member 1 — Graph + Fraud Chains (The Relationship Brain)

**Core Responsibility:** Build NetworkX logic to track transaction paths, find cycles, and spot rapid money movement.

### `backend/graph/graph_store.py`
- [ ] Initialize standard in-memory NetworkX `DiGraph()`.
- [ ] `add_node(account_id, **kwargs)`: Ensure node exists.
- [ ] `add_edge(from_account, to_account, transaction_id, amount, timestamp)`: Track the transaction flow.
- [ ] `clear_graph()`: Helpful for testing and replay mode resets.

### `backend/graph/algorithms.py`
- [ ] `detect_cycle(graph, from_account, to_account)`: Uses `nx.simple_cycles` or a custom BFS to determine if money loops back.
- [ ] `get_connection_count(graph, account_id)`: Retrieve degree of the node (in/out edges). Flags "Hub" accounts.
- [ ] `detect_rapid_chain(graph, start_account, time_window)`: Walk outgoing edges to see if money moves instantly across hops.
- [ ] `trace_account_flow(graph, account_id, depth)`: Extract the sub-graph around a specific account for investigation.

### `backend/graph/builder.py`
- [ ] `build_graph_payload_for_frontend(subgraph)`: Convert NetworkX nodes/edges into Cytoscape.js compatible JSON format.

### `backend/routes/trace.py`
- [ ] `GET /trace/{account_id}`: Call `trace_account_flow()` and return Cytoscape-formatted JSON.

---

## Member 2 — ML + Behavior + Risk (The AI Decision Brain)

**Core Responsibility:** Evaluate transaction features against historical behavior, compute anomaly scores, and make the final Approve/MFA/Block decision.

### `backend/db/database.py` & `backend/db/models.py`
- [ ] Setup simple in-memory dictionaries or SQLite setup for `transactions`, `alerts`, and `behavior_profiles`.

### `backend/behavior/profile.py` 
- [ ] `get_user_profile(user_id)`: Retrieve historical averages (amount, frequency, common devices, etc.).
- [ ] `update_user_profile(user_id, transaction)`: Update running averages/sets for the user.
- [ ] `compute_behavior_risk(profile, transaction)`: Compare new tx against the profile. Returns deviation metrics.

### `backend/ml/anomaly.py`
- [ ] `compute_anomaly_score(features)`: Pass extracted feature array into Isolation Forest and return score.

### `backend/risk/scoring.py`
- [ ] `calculate_final_risk(behavior_result, ml_result, graph_result)`: Weight and merge inputs (e.g., 30% behavior, 35% ML, 35% graph).
- [ ] `make_decision(risk_score)`: Map the 0-100 score to `APPROVE` (0-29), `MFA` (30-59), or `BLOCK` (60+).

### `backend/alerts/generator.py`
- [ ] `create_alert_object(transaction, final_result)`: If decision is MFA or BLOCK, construct the alert document (with `reasons`).

### `backend/routes/alerts.py`
- [ ] `GET /alerts`: Return the list of generated alerts for the dashboard.

---

## Member 3 — Integration + APIs + Frontend (System Glue & UI)

**Core Responsibility:** Wire backend services together, handle API boundaries, and build the UI.

### Request / Response Schemas (`backend/schemas/transaction.py`)
- [ ] Define `TransactionRequest` model mapping the 8 inputs.
- [ ] Define `TransactionResponse` model mapping score, decision, reasons.

### `backend/services/transaction_service.py`
- [ ] `process_transaction(tx_data)`: Implement the core orchestration logic combining Member 1 and Member 2 functions.

### `backend/routes/transaction.py` & `backend/main.py`
- [ ] `POST /transaction`: Route logic.
- [ ] Central FastAPI app setup, CORS middleware.

### `frontend/src/services/api.js`
- [ ] Axios/Fetch wrappers.

### `frontend/src/pages/Dashboard.jsx` (and components)
- [ ] Implement `TransactionForm`, `AlertsTable`, and `Reasons` chips.

### `frontend/src/components/GraphView.jsx`
- [ ] Integrate Cytoscape.js and display graph traces.

### `frontend/src/pages/Simulation.jsx`
- [ ] Implement Demo Buttons: "Normal Tx", "Unusual Tx", "Cycle Fraud", "ATO/Chain".
