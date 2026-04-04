import networkx as nx
import time
from backend.graph.graph_store import get_graph

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
# 7. RELAY NODE DETECTION (Professional Laundering)
# -------------------------------
def detect_relay(graph, account: str, threshold: int = 3):
    """Detects nodes that act as pass-through relays (High in and out)."""
    if account not in graph: return False
    in_degree = graph.in_degree(account)
    out_degree = graph.out_degree(account)
    return in_degree >= threshold and out_degree >= threshold

# -------------------------------
# 8. CONNECTION COUNT
# -------------------------------
def get_connections(graph, account: str):
    if account not in graph: return 0
    return len(set(graph.predecessors(account)) | set(graph.successors(account)))

# -------------------------------
# 9. GENERATE SIGNALS (The Orchestrator)
# -------------------------------
def generate_signals(from_account: str, to_account: str, amount: float):
    g = get_graph()
    
    # Temporarily add current edge to graph for "look-ahead" cycle/hub/chain detection
    # This ensures the current transaction's impact on topology is analyzed in real-time
    temp_edge_key = g.add_edge(from_account, to_account, amount=amount, timestamp=time.time())
    
    has_cycle, cycle_path = False, []
    is_hub = False
    is_relay = False
    long_chain = False
    high_velocity = False
    long_paths = []
    is_cluster = False
    is_kingpin = False
    is_isolated_ring = False
    is_smurfing = False
    connections = 0

    try:
        has_cycle, cycle_path = detect_cycle(g, from_account)
        connections = get_connections(g, from_account)
        is_hub = connections >= 5
        is_relay = detect_relay(g, from_account) or detect_relay(g, to_account)
        is_smurfing = detect_smurfing(g, from_account, to_account)
        
        # Comprehensive Chain Detection: Trace from current account and its immediate ancestors
        all_paths = []
        # Successor paths (forward)
        all_paths.extend(trace_funds(g, from_account, max_depth=4)["paths"])
        # Ancestor paths (backward check)
        for ancestor in g.predecessors(from_account):
            all_paths.extend(trace_funds(g, ancestor, max_depth=5)["paths"])
            
        long_paths = [p for p in all_paths if len(p) >= 4]
        long_chain = len(long_paths) > 0
        high_velocity = any(analyze_path_velocity(g, p) for p in all_paths)
        
        is_cluster = detect_dense_cluster(g, from_account)
        
        # ELITE: Strategic Centrality (PageRank) - Identifies 'Master Nodes' in laundering rings
        # On a massive graph, we would cache this; for a demo, we do it live.
        try:
            centrality = nx.pagerank(g, alpha=0.85)
            is_kingpin = centrality.get(from_account, 0) > 0.05 # Top 5% of network influence
        except:
            is_kingpin = False
            
        # ELITE: Isolation Discovery (Connected Components)
        # Finds localized fraud rings that are disconnected from the 'Main' economy
        ug = g.to_undirected()
        components = list(nx.connected_components(ug))
        node_group = next((comp for comp in components if from_account in comp), set())
        is_isolated_ring = len(node_group) > 2 and len(node_group) < 10 # Small, closed-loop rings
        
    finally:
        # 4. Final Aggregation (Calibrated weights)
        graph_score = 0
        if has_cycle: graph_score += 40
        if is_hub: graph_score += 20
        if is_relay: graph_score += 30
        if long_chain: graph_score += 25
        if is_smurfing: graph_score += 15
        if is_cluster: graph_score += 15
        if is_kingpin: graph_score += 35 # High strategic risk
        if is_isolated_ring: graph_score += 20
        
        # ALWAYS remove the temp edge so it doesn't double-count when add_transaction is called later
        g.remove_edge(from_account, to_account, key=temp_edge_key)
        
        return {
            "signals": {
                "has_cycle": has_cycle,
                "cycle_path": cycle_path,
                "is_hub": is_hub,
                "is_relay": is_relay,
                "is_kingpin": is_kingpin,
                "is_isolated_ring": is_isolated_ring,
                "suspicious_chain": long_chain or high_velocity,
                "chain_paths": long_paths[:2],
                "is_smurfing": is_smurfing,
                "is_cluster": is_cluster,
                "score": min(100, graph_score),
                "graph_risk": min(100, graph_score), 
                "connections": connections
            }
        }
