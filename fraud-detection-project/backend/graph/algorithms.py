from backend.graph.graph_store import get_graph
from backend.graph.builder import add_transaction_to_graph


def process_graph(tx) -> dict:
    G = get_graph()

    add_transaction_to_graph(G, tx)

    from_acc = tx.from_account
    to_acc = tx.to_account

    # Cycle detection
    cycle = False
    try:
        import networkx as nx
        cycles = list(nx.simple_cycles(G))
        for c in cycles:
            if from_acc in c or to_acc in c:
                cycle = True
                break
    except Exception:
        cycle = False

    # Connection count
    connections = G.degree(from_acc) if from_acc in G else 0

    # Rapid chain: from_acc's neighbor also sends to another
    rapid_chain = False
    if from_acc in G:
        for neighbor in G.successors(from_acc):
            if G.out_degree(neighbor) > 1:
                rapid_chain = True
                break

    # Graph risk base
    graph_risk = 0
    if cycle:
        graph_risk += 40
    if rapid_chain:
        graph_risk += 20
    if connections > 5:
        graph_risk += 15

    # Related accounts
    related = []
    if from_acc in G:
        related = list(G.successors(from_acc))

    return {
        "cycle": cycle,
        "connections": connections,
        "rapid_chain": rapid_chain,
        "graph_risk": graph_risk,
        "related_accounts": related
    }