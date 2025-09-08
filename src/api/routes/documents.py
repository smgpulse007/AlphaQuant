from fastapi import APIRouter, Query

router = APIRouter(prefix="/documents")


@router.get("/search")
def search(q: str = Query("")):
    # TODO: call vec/doc store for results
    return {
        "query": q,
        "results": [
            {"id": "doc_1", "title": "Sample Document", "url": "https://example.com", "snippet": "Lorem ipsum..."}
        ],
    }


@router.get("/{doc_id}")
def get_document(doc_id: str):
    # TODO: fetch full doc from store
    return {
        "id": doc_id,
        "url": "https://example.com",
        "publisher": "Example",
        "content": "Full document content placeholder.",
        "citations": [],
    }
