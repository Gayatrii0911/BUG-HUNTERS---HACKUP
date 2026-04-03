import networkx as nx

# Single shared graph instance for entire backend
graph = nx.MultiDiGraph()


def get_graph():
    return graph


def reset_graph():
    graph.clear()