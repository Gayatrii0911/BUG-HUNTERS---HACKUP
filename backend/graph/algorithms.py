import networkx as nx
import time
from backend.graph.builder import get_graph

# -------------------------------
# 1. CYCLE DETECTION
# -------------------------------
def detect_cycle(graph, account: str):
    if account not in graph: return False, []
    try:
        dg = nx.DiGraph(graph)
        cycles = list(nx.simple_cycles(dg))
        for cycle in cycles:
            if account in cycle:
                # Use Maximal Signal Strength to avoid diluting critical indicators
                return True, cycle + [cycle[0]]
        return False, []
    except: return False, []

# -------------------------------
# 2. PATH VELOCITY ANALYSIS
# -------------------------------
def analyze_path_velocity(graph, path: list, threshold_sec: int = 300):
    if len(path) < 3: return False
    
    velocity_hops = 0
    for i in range(len(path) - 2):
        u, v, w = path[i], path[i+1], path[i+2]
        
        txs1 = graph.get_edge_data(u, v)
        e1_time = float(txs1[max(txs1.keys())]['timestamp']) if txs1 else 0
        
        txs2 = graph.get_edge_data(v, w)
        e2_time = float(txs2[max(txs2.keys())]['timestamp']) if txs2 else 0
        
        if e1_time and e2_time and (e2_time - e1_time) < threshold_sec:
            velocity_hops += 1
            
    return velocity_hops >= 1

# -------------------------------
# 3. STRUCTURING (SMURFING)
# -------------------------------
def detect_smurfing(graph, u: str, v: str, window: int = 1800, count_threshold: int = 3):
    if not graph.has_edge(u, v): return False
    
    current_time = time.time()
    txs = graph.get_edge_data(u, v)
    recent_small = 0
    for key in txs:
        data = txs[key]
        if (current_time - float(data['timestamp'])) <= window:
            recent_small += 1
            
    return recent_small >= count_threshold

# -------------------------------
# 4. COMMUNITY / CLUSTER DETECTION
# -------------------------------
def detect_dense_cluster(graph, account: str):
    if account not in graph: return False
    neighbors = list(set(graph.predecessors(account)) | set(graph.successors(account)))
    sub = graph.subgraph(neighbors + [account])
    if len(sub.nodes) >= 3:
        edges = len(sub.edges)
        nodes = len(sub.nodes)
        density = edges / (nodes * (nodes - 1)) if nodes > 1 else 0
        return density > 0.5
    return False

# -------------------------------
# 5. FUND FLOW TRACING (Required for Trace API)
# -------------------------------
def trace_funds(graph, account: str, max_depth: int = 4):
    paths = []
    def dfs(current, path, depth):
        if depth >= max_depth: return
        for neighbor in graph.successors(current):
            if neighbor not in path:
                new_path = path + [neighbor]
                paths.append(new_path)
                dfs(neighbor, new_path, depth + 1)
    if account in graph: dfs(account, [account], 0)
    return {"account": account, "paths": paths}

# -------------------------------
# 6. CONNECTION COUNT
# -------------------------------
def get_connections(graph, account: str):
    if account not in graph: return 0
    return len(set(graph.predecessors(account)) | set(graph.successors(account)))

# -------------------------------
# 7. GENERATE SIGNALS (The Orchestrator)
# -------------------------------
def generate_signals(from_account: str, to_account: str, amount: float):
    g = get_graph()
    
    has_cycle, _ = detect_cycle(g, from_account)
    connections = get_connections(g, from_account)
    is_hub = connections >= 5
    
    trace_res = trace_funds(g, from_account)
    paths = trace_res["paths"]
    
    long_chain = any(len(p) >= 4 for p in paths)
    high_velocity = any(analyze_path_velocity(g, p) for p in paths)
    
    is_smurfing = detect_smurfing(g, from_account, to_account)
    is_cluster = detect_dense_cluster(g, from_account)
    
    graph_score = 0
    
    if has_cycle: graph_score += 40
    if high_velocity: graph_score += 25
    elif long_chain: graph_score += 15
        
    if is_hub: graph_score += 20
    if is_smurfing: graph_score += 15
    if is_cluster: graph_score += 10

    return {
        "signals": {
            "has_cycle": has_cycle,
            "is_hub": is_hub,
            "suspicious_chain": long_chain or high_velocity,
            "is_smurfing": is_smurfing,
            "is_cluster": is_cluster,
            "score": min(100, graph_score),
            "graph_risk": graph_score,
            "connections": connections
        }
    }
