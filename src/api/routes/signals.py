from fastapi import APIRouter

router = APIRouter(prefix="/signals")


@router.get("/status")
def status():
    return {"ok": True}


@router.get("/logs")
def logs():
    # TODO: stream or page logs from Loki or local buffer
    return {"entries": []}

