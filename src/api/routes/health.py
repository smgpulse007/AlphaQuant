from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/health/detailed")
def health_detailed():
    return {
        "status": "ok",
        "services": [
            {"name": "api", "status": "ok"},
            {"name": "worker", "status": "ok"},
            {"name": "postgres", "status": "ok"},
            {"name": "redis", "status": "ok"},
            {"name": "qdrant", "status": "ok"},
            {"name": "minio", "status": "ok"},
        ],
    }

