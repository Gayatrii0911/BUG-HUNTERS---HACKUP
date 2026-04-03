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
        dg = nx.DiGraph(graph)
        cycles = list(nx.simple_cycles(dg))
        for cycle in cycles:
            if account in cycle:
                full_cycle = cycle + [cycle[0]]
                print(f"[Graph] Cycle detected involving {account}: {' -> '.join(map(str, full_cycle))}")
                return True, full_cycle
        return False, []
    except Exception as e:
        print(f"[Graph] Cycle check error: {e}")
        return False, []

# -------------------------------
# 2. CONNECTION COUNT
# -------------------------------
def get_connections(graph, account: str):
    if account not in graph:
        return 0
    in_nb = set(graph.predecessors(account))
    out_nb = set(graph.successors(account))
    return len(in_nb.union(out_nb))

# -------------------------------
# 3. HIGH FREQUENCY DETECTION
# -------------------------------
def detect_high_frequency(graph, account: str, window: int = 60, threshold: int = 5):
    current_time = time.time()
    count = 0
    if account not in graph:
        return False
    for _, _, data in graph.out_edges(account, data=True):
        tx_time = float(data.get("timestamp", 0))
        if tx_time and (current_time - tx_time) <= window:
            count += 1
    return count >= threshold

# -------------------------------
# 4. TRACE FUNDS
# -------------------------------
def trace_funds(graph, account: str, max_depth: int = 4):
    paths = []
    def dfs(current, path, depth):
        if depth >= max_depth:
            return
        for neighbor in graph.successors(current):
            if neighbor in path:
                continue
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
    g = get_graph()
    
    cycle, cycle_path = detect_cycle(g, from_account)
    connections = get_connections(g, from_account)
    is_hub = connections >= 5
    
    trace_res = trace_funds(g, from_account)
    long_paths = [p for p in trace_res["paths"] if len(p) >= 4]
    suspicious_chain = len(long_paths) >= 1 and not is_hub
    
    high_freq = detect_high_frequency(g, from_account)
    
    graph_score = 0
    explanations = []
    
    if cycle:
        graph_score += 40
        explanations.append(f"Cycle detected: {' -> '.join(map(str, cycle_path))}")
    if is_hub:
        graph_score += 25
        explanations.append(f"Hub account ({connections} neighbors)")
    if suspicious_chain:
        graph_score += 20
        explanations.append(f"Suspicious path detected ({len(long_paths[0])} hops)")
    if high_freq:
        graph_score += 15
        explanations.append("High transaction frequency")
    
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
