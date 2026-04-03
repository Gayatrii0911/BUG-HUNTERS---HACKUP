import networkx as nx
from datetime import datetime
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