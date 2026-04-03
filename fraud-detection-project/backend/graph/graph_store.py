import networkx as nx
graph = nx.MultiDiGraph()

_graph = nx.DiGraph()

def get_graph() -> nx.DiGraph:
    return _graph

def reset_graph():
    global _graph
    _graph = nx.DiGraph()
