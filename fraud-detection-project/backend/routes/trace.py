from fastapi import APIRouter
from backend.graph.builder import get_graph
from backend.graph.algorithms import trace_funds

router = APIRouter()


@router.get("/trace/{account}")
def trace_account(account: str, max_depth: int = 4):
    graph = get_graph()

    # Check if 'account' is actually a transaction_id on an edge
    for u, v, k, data in graph.edges(data=True, keys=True):
        if data.get("transaction_id") == account:
            # We found the specific transaction, trace from its source
            account = str(u)
            break

    if account not in graph:
        return {
            "status": "not_found",
            "message": f"Account '{account}' not found in graph",
            "account": account,
            "paths": []
        }

    result = trace_funds(graph, account, max_depth=max_depth)

    from backend.graph.formatter import build_subgraph_for_account
    graph_payload = build_subgraph_for_account(graph, account, depth=max_depth)

    # trace summarization
    paths = result["paths"]
    max_path_length = max([len(p) for p in paths]) if paths else 0
    suspicious_paths = [p for p in paths if len(p) >= 4]
    
    # gather all unique accounts in the trace
    related_accounts = set()
    for p in paths:
        related_accounts.update(p)

    return {
        "status": "success",
        "account": result["account"],
        "paths": paths,
        "path_count": len(paths),
        "max_path_length": max_path_length,
        "suspicious_paths": suspicious_paths,
        "related_accounts_summary": list(related_accounts),
        "max_depth": max_depth,
        "graph_payload": graph_payload
    }