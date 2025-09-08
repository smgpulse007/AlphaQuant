from typing import Optional


def fetch_series(series_id: str, api_key: Optional[str] = None):
    # TODO: implement real FRED API client with caching
    return {"series": series_id, "latest": None}

