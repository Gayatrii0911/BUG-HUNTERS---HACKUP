from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.transaction import router as transaction_router
from backend.routes.debug import router as debug_router
from backend.routes.alerts import router as alerts_router
from backend.routes.simulation import router as simulation_router
from backend.routes.trace import router as trace_router
from backend.db.database import init_db
from backend.ml.model_loader import warmup

app = FastAPI(title="Fraud Detection API")

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

app.include_router(transaction_router)
app.include_router(debug_router)
app.include_router(alerts_router)
app.include_router(simulation_router)
app.include_router(trace_router)

@app.get("/health")
def health():
    return {"status": "ok", "message": "API is running"}

@app.get("/")
def root():
    return {"status": "ok", "message": "Fraud Detection API is running"}
