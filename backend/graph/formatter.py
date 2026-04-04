import networkx as nx

def build_full_graph_payload(graph):
    """
    Format the entire graph for Cytoscape.js
    """
    payload = {"nodes": [], "edges": []}
    
    for node, data in graph.nodes(data=True):
        payload["nodes"].append({
            "data": {
                "id": str(node),
                "label": str(node),
                "is_moderate_risk": 40 <= data.get("risk_score", 0) < 70,
                **data
            }
        })
        
    for u, v, k, data in graph.edges(data=True, keys=True):
        payload["edges"].append({
            "data": {
                "id": f"{u}-{v}-{k}",
                "source": str(u),
                "target": str(v),
                **data
            }
        })
        
    return payload

def build_subgraph_for_account(graph, account_id, depth=1):
    """
    Extract a subgraph around an account up to a certain depth and format it for Cytoscape.js
    """
    if account_id not in graph:
        return {"nodes": [], "edges": []}
        
    # Using bfs_edges to graph both incoming and outgoing for a better view
    undirected = graph.to_undirected()
    edges = list(nx.bfs_edges(undirected, source=account_id, depth_limit=depth))
    nodes = {account_id}
    for u, v in edges:
        nodes.add(u)
        nodes.add(v)
        
    subgraph = graph.subgraph(nodes)
    return build_full_graph_payload(subgraph)
