import networkx as nx
import time
from backend.graph.builder import get_graph

# -------------------------------
# 1. CYCLE DETECTION
# -------------------------------
def detect_cycle(graph, account: str):
    """
    Detects if 'account' is involved in a circular movement path.
    Finds a simple cycle that includes 'account'.
    """
    if account not in graph:
        return False, []
        
    try:
        # Convert MultiDiGraph to DiGraph for cycle detection as simple_cycles only supports DiGraph.
        # This keeps the logic consistent.
        dg = nx.DiGraph(graph)
        cycles = list(nx.simple_cycles(dg))
        for cycle in cycles:
            if account in cycle:
                # Close the cycle for visualization
                return True, cycle + [cycle[0]]
        return False, []
    except Exception:
        return False, []

# -------------------------------
# 2. CONNECTION COUNT
# -------------------------------
def get_connections(graph, account: str):
    """
    Returns unique degree (combined in-neighbors and out-neighbors).
    """
    if account not in graph:
        return 0
    in_nb = set(graph.predecessors(account))
    out_nb = set(graph.successors(account))
    return len(in_nb.union(out_nb))

# -------------------------------
# 3. HIGH FREQUENCY DETECTION
# -------------------------------
def detect_high_frequency(graph, account: str, window: int = 60, threshold: int = 5):
    """
    Check if account made too many transactions in the last hour.
    """
    current_time = time.time()
    count = 0
    if account not in graph:
        return False
    # MultiDiGraph out_edges handles multiple edges correctly
    for _, _, data in graph.out_edges(account, data=True):
        tx_time = float(data.get("timestamp", 0))
        if tx_time and (current_time - tx_time) <= window:
            count += 1
    return count >= threshold

# -------------------------------
# 4. TRACE FUNDS
# -------------------------------
def trace_funds(graph, account: str, max_depth: int = 4):
    """
    DFS retrieval of fund flow paths starting at 'account'.
    """
    paths = []
    def dfs(current, path, depth):
        if depth >= max_depth:
            return
        for neighbor in graph.successors(current):
            if neighbor in path:
                continue # avoid infinite recursion in small cycles
            new_path = path + [neighbor]
            paths.append(new_path)
            dfs(neighbor, new_path, depth + 1)

    if account in graph:
        dfs(account, [account], 0)
    return {"account": account, "paths": paths}

# -------------------------------
# 5. GENERATE SIGNALS (The Orchestrator)
# -------------------------------
def generate_signals(from_account: str, to_account: str, amount: float):
    """
    Primary API for Relationship Intelligence (Member 1).
    Fulfillment of the frozen contract.
    """
    g = get_graph()
    
    cycle, cycle_path = detect_cycle(g, from_account)
    connections = get_connections(g, from_account)
    is_hub = connections >= 5
    
    trace_res = trace_funds(g, from_account)
    long_paths = [p for p in trace_res["paths"] if len(p) >= 4]
    suspicious_chain = len(long_paths) >= 1 and not is_hub
    
    high_freq = detect_high_frequency(g, from_account)
    
    # Calculate M1 risk contribution
    # Score 0 to 100 based on standard project weights
    graph_score = 0
    explanations = []
    
    if cycle:
        graph_score += 40
        explanations.append(f"Cycle detected involving this account: {' -> '.join(map(str, cycle_path))}")
    if is_hub:
        graph_score += 25
        explanations.append(f"High connection account ({connections} neighbors)")
    if suspicious_chain:
        graph_score += 20
        explanations.append(f"Suspicious chain detected starting from this account ({len(long_paths[0])} hops)")
    if high_freq:
        graph_score += 15
        explanations.append("High transaction frequency from this wallet")
    
    signals = {
        "cycle": cycle,
        "cycle_path": cycle_path,
        "connections": connections,
        "is_hub": is_hub,
        "suspicious_chain": suspicious_chain,
        "long_paths": long_paths,
        "amount": amount,
        "has_cycle": cycle,
        "suspicious_connections": is_hub or suspicious_chain,
        "rapid_transactions": high_freq,
        "score": graph_score,
        "graph_risk": graph_score,
        "graph_explanations": explanations
    }
    
    return {"signals": signals}
