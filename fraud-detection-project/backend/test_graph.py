import time
from backend.graph.builder import add_transaction, get_graph, reset_graph
from backend.graph.algorithms import generate_signals, trace_funds, detect_cycle, get_connections, detect_suspicious_chain, build_graph_signals

print("=== GRAPH TEST START ===")

def run_case_a():
    print("\n--- Case A ---")
    reset_graph()
    add_transaction("A", "B", 100)
    
    graph = get_graph()
    cycle, _ = detect_cycle(graph)
    conn = get_connections(graph, "A")
    print(f"Cycle: {cycle} (Expected: False)")
    print(f"Connections: {conn} (Expected: 1)")

def run_case_b():
    print("\n--- Case B ---")
    reset_graph()
    add_transaction("A", "B", 100)
    add_transaction("B", "C", 200)
    add_transaction("C", "A", 300)

    graph = get_graph()
    cycle, path = detect_cycle(graph)
    print(f"Cycle: {cycle} (Expected: True)")
    print(f"Cycle Path: {path}")

def run_case_c():
    print("\n--- Case C ---")
    reset_graph()
    add_transaction("A", "B", 100)
    add_transaction("A", "C", 100)
    add_transaction("A", "D", 100)
    add_transaction("A", "E", 100)
    add_transaction("A", "F", 100)

    graph = get_graph()
    conn = get_connections(graph, "A")
    is_hub = conn >= 5
    print(f"Connections: {conn} (Expected: high/5)")
    print(f"Is Hub: {is_hub} (Expected: True)")

def run_case_d():
    print("\n--- Case D ---")
    reset_graph()
    add_transaction("A", "B", 100)
    add_transaction("B", "C", 100)
    add_transaction("C", "D", 100)
    
    graph = get_graph()
    trace = trace_funds(graph, "A")
    suspicious, paths = detect_suspicious_chain(trace, min_length=4)
    print(f"Suspicious Chain: {suspicious} (Expected: True/False depending on logic)")
    print(f"Paths: {paths}")
    
run_case_a()
run_case_b()
run_case_c()
run_case_d()

print("\n=== GRAPH TEST END ===")