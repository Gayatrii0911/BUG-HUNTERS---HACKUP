import os
from typing import List, Dict

def explain_fraud_scenario(reasons: List[Dict], risk_score: float, decision: str) -> str:
    """
    Simulated LLM Forensic Explainer for Demo.
    In a production environment, this would call Gemini/Vertex AI.
    For the hackathon demo, it generates a high-fidelity 'Smart Summary'.
    """
    
    # 1. Identify primary threat vectors
    r_msgs = [r["message"] for r in reasons]
    has_graph = any("Cycle" in m or "Relay" in m or "Chain" in m for m in r_msgs)
    has_behavior = any("Dormant" in m or "deviation" in m.lower() for m in r_msgs)
    has_identity = any("travel" in m.lower() or "device" in m.lower() for m in r_msgs)
    
    # 2. Construct Professional Narrative
    summary = f"SCENARIO ANALYSIS: [Risk Score: {risk_score}% | Decision: {decision}]\n\n"
    
    if decision == "BLOCK":
        summary += "FORENSIC VERDICT: Critical Fraud signature detected. "
    else:
        summary += "FORENSIC VERDICT: Suspicious Activity observed. "

    if has_graph and has_identity:
        summary += "The system has identified a 'Coordinated Identity Strike'. "
    elif has_graph:
        summary += "A 'Network Topology Attack' is underway using sophisticated layering patterns. "
    elif has_identity:
        summary += "High confidence 'Account Takeover' signature detected via identity metadata. "

    summary += "Specifically: " + "; ".join(r_msgs[:3]) + ".\n\n"
    
    summary += "INVESTIGATOR RECOMMENDATION: "
    if decision == "BLOCK":
        summary += "Reject transaction immediately and transition account to 'Restricted' state for manual review."
    elif decision == "MFA":
        summary += "Challenge transaction with biometric multi-factor authentication (MFA) to verify identity."
    else:
        summary += "Monitor account for further deviations; baseline risk remains within manageable limits."

    return summary
