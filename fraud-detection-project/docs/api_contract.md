# Fraud Guard Pro: Backend API Contract (Elite)

Version: 1.2.1
Engine: Hybrid Graph-ML Real-Time Scoring

## 1. Primary Transaction Intake
`POST /transaction`
Processes a real-time transaction through the integrated intelligence pipeline.

**Request Schema:**
```json
{
  "sender_id": "string (Required)",
  "receiver_id": "string (Required)",
  "amount": "float (Required, >0)",
  "device_id": "string (Optional, default 'unknown')",
  "location": "string (Optional, default 'unknown')",
  "channel": "string (Optional, default 'web')",
  "timestamp": "string (Optional, epoch)"
}
```

**Response Schema:**
```json
{
  "transaction_id": "string (UUID)",
  "risk_score": "float (0-100)",
  "risk_level": "string ('low', 'medium', 'high')",
  "decision": "string ('APPROVE', 'MFA', 'BLOCK')",
  "reasons": ["string"],
  "reason_categories": {
    "behavior": ["string"],
    "device": ["string"],
    "ml": ["string"],
    "graph": ["string"],
    "fraud_chain": ["string"]
  },
  "score_breakdown": {
     "graph_risk": "float",
     "ml_risk": "float",
     "behavior_risk": "float",
     "device_risk": "float"
  },
  "anomaly_score": "float (0.0-1.0)",
  "confidence": "float (0.0-1.0)",
  "fraud_chain_detected": "boolean",
  "alert": "boolean",
  "alert_id": "string"
}
```

## 2. Alerts & Monitoring
`GET /alerts`
Returns a chronologically reversed list of all flagged suspicious transactions.

## 3. Investigation & Tracing
`GET /trace/{account_id}`
Returns a full recursive fund flow graph for forensic investigation.

## 4. Scenario Simulation
`POST /simulation/run/{scenario_name}`
Triggers a predefined fraud replay scenario (normal_user, cycle_fraud, layering_chain, etc.) to test system response.

`POST /simulation/reset`
Wipes all behavioral profiles, graph state, and DB records for a clean demonstration.

## 5. System Health
`GET /health`
Returns system status, ML model version, and uptime.
