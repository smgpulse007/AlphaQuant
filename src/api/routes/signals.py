from fastapi import APIRouter

router = APIRouter(prefix="/signals")


@router.get("/status")
def status():
    return {"ok": True}


@router.get("/logs")
def logs():
    # TODO: stream or page logs from Loki or local buffer
    return {"entries": []}


# v1-compatible endpoints expected by frontend
@router.get("")
def signals_overview():
    # Minimal counts; could aggregate from analysis state in a real run
    return {"total_count": 12, "active": 9, "recent_change": 3}


@router.get("/politicians")
def signals_politicians():
    # Placeholder data for UI cards
    return {
        "total_count": 8,
        "trades": [
            {"politician": "Rep. Johnson", "ticker": "NVDA", "action": "buy", "amount_range": "$15,001-$50,000", "trade_date": "2025-01-07"},
            {"politician": "Sen. Williams", "ticker": "TSM", "action": "sell", "amount_range": "$50,001-$100,000", "trade_date": "2025-01-05"},
            {"politician": "Rep. Davis", "ticker": "GOOGL", "action": "buy", "amount_range": "$1,001-$15,000", "trade_date": "2025-01-06"},
        ],
        "sector_exposure": {"Technology": 0.45, "Healthcare": 0.23, "Finance": 0.18, "Other": 0.14},
    }
