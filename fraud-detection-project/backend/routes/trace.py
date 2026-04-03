from fastapi import APIRouter
from backend.graph.builder import get_graph
from backend.graph.algorithms import trace_funds

router = APIRouter()


@router.get("/trace/{account}")
def trace_account(account: str, max_depth: int = 4):
    graph = get_graph()

    if account not in graph:
        return {
            "status": "not_found",
            "message": f"Account '{account}' not found in graph",
            "account": account,
            "paths": []
        }

    result = trace_funds(graph, account, max_depth=max_depth)

    return {
        "status": "success",
        "account": result["account"],
        "paths": result["paths"],
        "path_count": len(result["paths"]),
        "max_depth": max_depth
    }