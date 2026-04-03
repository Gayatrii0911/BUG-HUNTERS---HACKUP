import networkx as nx
import time

# Core Singleton Graph - Unified for Decisioning and Trace
graph = nx.MultiDiGraph()

def get_graph() -> nx.MultiDiGraph:
    return graph

def reset_graph():
    graph.clear()
    print("SENTINEL-X GRAPH STORAGE PURGED")

def add_transaction(from_account: str, to_account: str, amount: float, timestamp: float = None, is_fraud: bool = False, is_blocked: bool = False, transaction_id: str = None, decision: str = "APPROVE", risk_score: float = 0, reasons: str = None):
    """
    Unified entry point for transaction graph ingestion.
    Supports decision metadata and block status for investigator visualization.
    """
    if timestamp is None:
        timestamp = time.time()
    
    # Node Metadata Enrichment
    graph.add_node(from_account, is_fraudulent=is_fraud, is_blocked=is_blocked, risk_score=risk_score, reasons=reasons)
    graph.add_node(to_account)
    
    # Forensic Edge Creation
    graph.add_edge(
        from_account, 
        to_account, 
        amount=amount, 
        timestamp=timestamp, 
        is_fraud=is_fraud, 
        is_blocked=is_blocked, 
        transaction_id=transaction_id, 
        decision=decision
    )

def save_snapshot() -> dict:
    """Export current graph for persistence or replay."""
    return nx.node_link_data(graph)

def load_snapshot(data: dict):
    """Restore graph from external state."""
    global graph
    graph.clear()
    graph = nx.node_link_graph(data)
    print("SENTINEL-X GRAPH STORAGE RESTORED FROM SNAPSHOT")
