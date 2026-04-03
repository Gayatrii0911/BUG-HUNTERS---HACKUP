import sys
import os
# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.graph.graph_store import reset_graph, get_graph, add_transaction
from backend.graph.algorithms import generate_signals, detect_cycle, get_connections, analyze_path_velocity
import time

def log_case(name, result):
    status = "PASS" if result else "FAIL"
    print(f"CASE {name}: [{status}]")

def test_graph_logic():
    print("=== STARTING GRAPH LOGIC VALIDATION ===")
    
    # CASE A: Simple Transaction (A -> B)
    reset_graph()
    add_transaction("A", "B", 100)
    signals = generate_signals("A", "B", 100)["signals"]
    log_case("A (no cycle, 1 conn)", signals["has_cycle"] == False and signals["connections"] == 1)
    
    # CASE B: Cycle (A -> B -> C -> A)
    # Note: add_transaction is called after generates_signals in the real service, 
    # but for testing algorithms directly, we simulate the state.
    reset_graph()
    add_transaction("A", "B", 100)
    add_transaction("B", "C", 100)
    # The third transaction (C -> A) should trigger the cycle detection
    signals = generate_signals("C", "A", 100)["signals"]
    log_case("B (cycle detected)", signals["has_cycle"] == True)
    
    # CASE C: Hub (A -> B, A -> C, A -> D, A -> E, A -> F)
    reset_graph()
    for target in ["B", "C", "D", "E"]:
        add_transaction("A", target, 100)
    # The 5th connection
    signals = generate_signals("A", "F", 100)["signals"]
    log_case("C (is_hub detected)", signals["is_hub"] == True and signals["connections"] >= 5)
    
    # CASE D: Suspicious Chain (A -> B -> C -> D)
    reset_graph()
    t = time.time()
    add_transaction("A", "B", 100, timestamp=t-20)
    add_transaction("B", "C", 100, timestamp=t-10)
    # D completes the chain
    signals = generate_signals("C", "D", 100)["signals"]
    log_case("D (suspicious_chain detected)", signals["suspicious_chain"] == True)

    print("=== GRAPH LOGIC VALIDATION COMPLETE ===")

if __name__ == "__main__":
    test_graph_logic()
