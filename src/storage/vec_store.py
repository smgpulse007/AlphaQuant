from typing import List, Tuple


class VecStore:
    def __init__(self, url: str, collection: str = "alpha"):
        self.collection = collection

    def upsert(self, items: List[Tuple[str, list[float], dict]]):
        # TODO: upsert to Qdrant/OpenSearch k-NN
        return len(items)

    def search(self, query: list[float], top_k: int = 5):
        # TODO: nearest neighbors
        return []

