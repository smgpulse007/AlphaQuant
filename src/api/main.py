from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.runbook import router as run_router
from src.api.routes.signals import router as sig_router
from src.api.routes.documents import router as doc_router
from src.api.routes.health import router as health_router


app = FastAPI(title="Agentic Alpha Engine", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(run_router)
app.include_router(sig_router)
app.include_router(doc_router)

# Also expose API under /api/v1 for frontend compatibility
app.include_router(health_router, prefix="/api/v1")
app.include_router(run_router, prefix="/api/v1")
app.include_router(sig_router, prefix="/api/v1")
app.include_router(doc_router, prefix="/api/v1")
