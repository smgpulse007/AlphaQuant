from fastapi import APIRouter, Query

router = APIRouter(prefix="/documents")


@router.get("/search")
def search(q: str = Query("")):
    # TODO: call vec/doc store for results
    return {"query": q, "results": []}

