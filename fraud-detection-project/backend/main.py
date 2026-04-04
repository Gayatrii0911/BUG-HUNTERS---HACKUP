import typing
import time # Added time here if needed
# Python 3.13 Compatibility Patch for Pydantic v1 / FastAPI
if hasattr(typing, 'ForwardRef'):
    _old_evaluate = typing.ForwardRef._evaluate
    def _new_evaluate(self, globalns, localns, recursive_guard=None):
        return _old_evaluate(self, globalns, localns, recursive_guard=recursive_guard)
    typing.ForwardRef._evaluate = _new_evaluate

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.transaction import router as transaction_router
from backend.routes.alerts import router as alerts_router
from backend.routes.simulation import router as simulation_router
from backend.routes.trace import router as trace_router
from backend.routes.account import router as account_router
from backend.db.database import init_db
from backend.ml.model_loader import warmup

START_TIME = time.time()

app = FastAPI(
    title="Elite Real-Time Fraud Intelligence API",
    description="Graph-ML Hybrid Transaction Scoring & Decisioning Engine",
    version="1.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    from backend.db.repositories import rebuild_graph_from_db
    init_db()
    rebuild_graph_from_db()
    warmup()

@app.get("/health")
def health():
    from backend.services.transaction_service import get_training_status
    return {
        "status": "healthy",
        "version": "1.2.0",
        "uptime_seconds": int(time.time() - START_TIME),
        "engine": "Sentinel-X Elite Hybrid",
        "training": get_training_status(),
        "model_loaded": True
    }



@app.get("/")
def root():
    return {
        "project": "Graph-Based Real-Time Fraud Detection & Fund Flow Tracking",
        "status": "online",
        "api_docs": "/docs",
        "system_health": "/health"
    }

app.include_router(transaction_router)
app.include_router(alerts_router)
app.include_router(simulation_router)
app.include_router(trace_router)
app.include_router(account_router)
