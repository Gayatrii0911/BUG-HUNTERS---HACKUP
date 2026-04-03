from datetime import datetime
from backend.graph.graph_store import graph


def add_transaction(from_account: str, to_account: str, amount: float, timestamp: float = None):
    """
    Adds a transaction edge to the shared graph.

    :param from_account: sender account
    :param to_account: receiver account
    :param amount: transaction amount
    :param timestamp: unix timestamp, auto-generated if not provided
    """
    if timestamp is None:
        timestamp = datetime.utcnow().timestamp()

    # Ensure nodes exist
    graph.add_node(from_account, type="account")
    graph.add_node(to_account, type="account")

    # Add edge with metadata
    graph.add_edge(
        from_account,
        to_account,
        amount=amount,
        timestamp=timestamp
    )


def get_graph():
    return graph


def reset_graph():
    graph.clear()
    print("GRAPH RESET SUCCESSFULLY")