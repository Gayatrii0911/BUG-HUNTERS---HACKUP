import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.transaction import router as transaction_router
from backend.routes.debug import router as debug_router
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()
    warmup()

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "version": "1.2.0",
        "uptime_seconds": int(time.time() - START_TIME),
        "engine": "Hybrid-Graph-ML",
        "ml_model": "IsolationForest-v1"
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
app.include_router(debug_router)
app.include_router(alerts_router)
app.include_router(simulation_router)
app.include_router(trace_router)
app.include_router(account_router)
