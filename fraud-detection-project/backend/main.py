from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.trace import router as trace_router
from backend.routes.transaction import router as tx_router

app = FastAPI(title="Campus Super App - Fraud Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trace_router)
app.include_router(tx_router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "API is running"}