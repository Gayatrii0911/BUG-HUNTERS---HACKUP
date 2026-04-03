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
                return True, cycle + [cycle[0]]
        return False, []
    except: return False, []

# -------------------------------
# 2. PATH VELOCITY ANALYSIS
# -------------------------------
def analyze_path_velocity(graph, path: list, threshold_sec: int = 300):
    """
    Checks if money is moving through the path too fast (Layering).
    If a hop happens within 5 mins of the previous, it's 'High Velocity'.
    """
    if len(path) < 3: return False
    
    velocity_hops = 0
    for i in range(len(path) - 2):
        u, v, w = path[i], path[i+1], path[i+2]
        
        # Get edges between hops
        e1 = graph.get_edge_data(u, v)
        e1_time = float(e1[0]['timestamp']) if e1 else 0
        
        e2 = graph.get_edge_data(v, w)
        e2_time = float(e2[0]['timestamp']) if e2 else 0
        
        if e1_time and e2_time and (e2_time - e1_time) < threshold_sec:
            velocity_hops += 1
            
    return velocity_hops >= 1

# -------------------------------
# 3. STRUCTURING (SMURFING)
# -------------------------------
def detect_smurfing(graph, u: str, v: str, window: int = 1800, count_threshold: int = 3):
    """Detects multiple small transactions between the same pair in 30 mins."""
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
    """Identify if user belongs to a small, highly connected fraud cluster."""
    if account not in graph: return False
    sub = graph.subgraph(list(graph.neighbors(account)) + [account])
    # If density > 0.6 and size > 2, it's a suspicious cluster
    if len(sub.nodes) >= 3:
        edges = len(sub.edges)
        nodes = len(sub.nodes)
        density = edges / (nodes * (nodes - 1))
        return density > 0.5
    return False

# -------------------------------
# 5. CORE ORCHESTRATOR (Refined)
# -------------------------------
def generate_signals(from_account: str, to_account: str, amount: float):
    g = get_graph()
    
    has_cycle, cycle_path = detect_cycle(g, from_account)
    connections = len(set(g.predecessors(from_account)) | set(g.successors(from_account)))
    is_hub = connections >= 5
    
    # Path/Chain Analysis
    paths = []
    def dfs(c, p, d):
        if d >= 4: return
        for n in g.successors(c):
            if n not in p:
                new_p = p + [n]; paths.append(new_p); dfs(n, new_p, d+1)
    
    if from_account in g: dfs(from_account, [from_account], 0)
    
    long_chain = any(len(p) >= 4 for p in paths)
    high_velocity = any(analyze_path_velocity(g, p) for p in paths)
    
    # New Elite Patterns
    is_smurfing = detect_smurfing(g, from_account, to_account)
    is_cluster = detect_dense_cluster(g, from_account)
    
    graph_score = 0
    explanations = []
    
    if has_cycle:
        graph_score += 40
        explanations.append("Circular fund flow (Laundering Ring)")
    if high_velocity:
        graph_score += 25
        explanations.append("High-velocity layering detected (Automated Flow)")
    elif long_chain:
        graph_score += 15
        explanations.append("Long money-laundering chain (4+ hops)")
        
    if is_hub:
        graph_score += 20
        explanations.append(f"Mule Hub Account ({connections} connections)")
    if is_smurfing:
        graph_score += 15
        explanations.append("Structuring/Smurfing pattern detected")
    if is_cluster:
        graph_score += 10
        explanations.append("Node part of highly-interconnected fraud cluster")

    return {
        "signals": {
            "has_cycle": has_cycle,
            "is_hub": is_hub,
            "suspicious_chain": long_chain or high_velocity,
            "is_smurfing": is_smurfing,
            "is_cluster": is_cluster,
            "score": min(100, graph_score),
            "graph_risk": graph_score,
            "explanations": explanations
        }
    }
