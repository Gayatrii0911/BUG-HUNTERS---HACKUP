import networkx as nx
import time

graph = nx.MultiDiGraph()

def add_transaction(from_account: str, to_account: str, amount: float, timestamp: float = None):
    if timestamp is None:
        timestamp = time.time()
    graph.add_node(from_account)
    graph.add_node(to_account)
    graph.add_edge(from_account, to_account, amount=amount, timestamp=timestamp)

def get_graph():
    return graph

def reset_graph():
    graph.clear()
    print("GRAPH RESET SUCCESSFULLY")

def add_transaction_to_graph(G, tx):
    # Compatibility shim if needed for other parts of the code
    from_acc = tx.from_account
    to_acc = tx.to_account
    amount = tx.amount
    timestamp = str(tx.timestamp)

    if not G.has_node(from_acc):
        G.add_node(from_acc, user_id=tx.user_id)
    if not G.has_node(to_acc):
        G.add_node(to_acc)

    if G.has_edge(from_acc, to_acc):
        G[from_acc][to_acc]["count"] += 1
        G[from_acc][to_acc]["total_amount"] += amount
    else:
        G.add_edge(from_acc, to_acc, amount=amount, timestamp=timestamp, count=1, total_amount=amount)
