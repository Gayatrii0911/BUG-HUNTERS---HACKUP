import time
import networkx as nx
from backend.graph.builder import get_graph
from backend.services.risk_engine import calculate_risk_score


# -------------------------------
# 1. CYCLE DETECTION
# -------------------------------
def detect_cycle(graph, from_account: str = None, to_account: str = None):
    """
    Detect whether the current graph contains a cycle.
    Returns:
        (True/False, cycle_path)
    """
    try:
        cycle_edges = nx.find_cycle(graph, orientation="original")

        path = []
        for u, v, *_ in cycle_edges:
            if not path:
                path.append(u)
            path.append(v)

        if path and path[0] != path[-1]:
            path.append(path[0])

        return True, path

    except nx.NetworkXNoCycle:
        return False, []


# -------------------------------
# 2. CONNECTION COUNT
# -------------------------------
def get_connections(graph, account: str):
    """
    Returns number of unique outgoing connections from an account.
    """
    if account not in graph:
        return 0

    return len(set(graph.successors(account)))


# -------------------------------
# 3. HIGH FREQUENCY DETECTION
# -------------------------------
def detect_high_frequency(graph, account: str, window: int = 30, threshold: int = 5):
    """
    Detect if an account has made too many outgoing transactions
    within a short time window.
    """
    current_time = time.time()
    count = 0

    if account not in graph:
        return False

    for _, _, data in graph.out_edges(account, data=True):
        tx_time = data.get("timestamp")
        if tx_time and (current_time - tx_time) <= window:
            count += 1

    print(f"HF DEBUG: {account} -> {count} transactions in {window}s")
    return count >= threshold


# -------------------------------
# 4. TRACE FUNDS
# -------------------------------
def trace_funds(graph, account: str, max_depth: int = 4):
    """
    DFS-style tracing of outgoing fund paths.
    """
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

    return {
        "account": account,
        "paths": paths
    }


# -------------------------------
# 5. RAPID / SUSPICIOUS CHAIN DETECTION
# -------------------------------
def detect_suspicious_chain(trace_result, min_length: int = 4):
    """
    Detect whether there is at least one long transaction path.
    """
    long_paths = [p for p in trace_result["paths"] if len(p) >= min_length]
    return len(long_paths) >= 1, long_paths


# -------------------------------
# 6. BUILD GRAPH SIGNALS
# -------------------------------
def build_graph_signals(graph, from_account: str, to_account: str, amount: float):
    """
    Build graph-based fraud signals after transaction is added.
    """
    cycle, cycle_path = detect_cycle(graph, from_account, to_account)
    high_frequency = detect_high_frequency(graph, from_account)
    connections = get_connections(graph, from_account)

    is_hub = connections >= 5

    trace = trace_funds(graph, from_account)
    suspicious_chain, long_paths = detect_suspicious_chain(trace)

    # if it is a hub, don't over-label as simple chain
    if is_hub:
        suspicious_chain = False

    signals = {
        "cycle": cycle,
        "cycle_path": cycle_path,
        "high_frequency": high_frequency,
        "is_hub": is_hub,
        "connections": connections,
        "suspicious_chain": suspicious_chain,
        "long_paths": long_paths,
        "amount": amount
    }

    return signals


# -------------------------------
# 7. MAIN PIPELINE USED BY CURRENT ROUTE
# -------------------------------
def generate_signals(from_account: str, to_account: str, amount: float):
    """
    Current project route uses this function directly.
    So we keep this compatible with your existing ZIP structure.
    """
    graph = get_graph()

    # Add transaction first (important for current flow)
    graph.add_node(from_account, type="account")
    graph.add_node(to_account, type="account")
    graph.add_edge(
        from_account,
        to_account,
        timestamp=time.time(),
        amount=amount
    )

    signals = build_graph_signals(graph, from_account, to_account, amount)

    print("Processing:", from_account, to_account, amount)
    print("Signals:", signals)

    score, level, reasons, action = calculate_risk_score(signals)

    return {
        "signals": signals,
        "risk_score": score,
        "risk_level": level,
        "explanation": reasons,
        "action": action
    }