import networkx as nx
import time
from backend.graph.builder import get_graph


def detect_cycle(graph, from_account, to_account):
    try:
        cycle_edges = nx.find_cycle(graph, orientation='original')
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


def get_connections(graph, account):
    if account not in graph:
        return 0
    return len(list(graph.successors(account)))


def detect_high_frequency(graph, account, window=30, threshold=5):
    current_time = time.time()
    count = 0
    if account not in graph:
        return False
    for _, _, data in graph.out_edges(account, data=True):
        tx_time = data.get("timestamp")
        if tx_time and (current_time - tx_time) <= window:
            count += 1
    return count >= threshold


def trace_funds(graph, account, max_depth=4):
    paths = []

    def dfs(current, path, depth):
        if depth > max_depth:
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


def generate_signals(from_account, to_account, amount):
    g = get_graph()

    g.add_edge(from_account, to_account, timestamp=time.time(), amount=amount)

    cycle, cycle_path = detect_cycle(g, from_account, to_account)
    high_frequency = detect_high_frequency(g, from_account)
    connections = get_connections(g, from_account)
    is_hub = connections >= 5

    trace = trace_funds(g, from_account)
    long_paths = [p for p in trace["paths"] if len(p) >= 4]
    suspicious_chain = len(long_paths) >= 1 and not is_hub

    score = 0
    if cycle:
        score += 40
    if high_frequency:
        score += 25
    if is_hub:
        score += 20
    if suspicious_chain:
        score += 15

    signals = {
        "cycle": cycle,
        "cycle_path": cycle_path,
        "high_frequency": high_frequency,
        "is_hub": is_hub,
        "connections": connections,
        "suspicious_chain": suspicious_chain,
        "amount": amount,
        "has_cycle": cycle,
        "suspicious_connections": is_hub or suspicious_chain,
        "rapid_transactions": high_frequency,
        "score": score,
    }

    return {
        "signals": signals,
        "risk_score": score,
        "risk_level": "HIGH" if score >= 70 else "MEDIUM" if score >= 30 else "LOW",
        "explanation": [],
        "action": "BLOCK" if score >= 70 else "REVIEW" if score >= 30 else "ALLOW"
    }
