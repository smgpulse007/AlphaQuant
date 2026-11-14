from __future__ import annotations
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Preferences(BaseModel):
    avoid: List[str] = []
    focus: List[str] = []


class RunInput(BaseModel):
    mode: str = Field(pattern=r"^[AB]$")
    budget: Optional[float] = 0
    risk: Optional[str] = "Medium"
    horizon_months: Optional[List[int]] = [3, 12]
    current_positions: Optional[List[Dict[str, Any]]] = []
    preferences: Preferences = Preferences()


class Citation(BaseModel):
    url: str
    hash: Optional[str] = None


class Trade(BaseModel):
    ticker: str
    direction: str
    strategy: str
    expiry: Optional[str] = None
    strikes: Optional[List[float]] = None
    cost: Optional[float] = None
    delta: Optional[float] = None
    pop: Optional[float] = None
    confidence: Optional[int] = None
    thesis: Optional[str] = None
    key_levels: Optional[Dict[str, float]] = None
    catalysts: Optional[List[str]] = None
    hedge_alt: Optional[str] = None
    why_now: Optional[str] = None
    citations: Optional[List[Citation]] = None


class MarketScanSection(BaseModel):
    facts: Optional[List[str]] = None
    citations: Optional[List[Citation]] = None


class PoliticiansSection(BaseModel):
    highlights: List[str] = []
    contradictions: List[str] = []
    citations: Optional[List[Citation]] = None


class MarketScan(BaseModel):
    macro: Optional[MarketScanSection] = None
    cross_asset: Optional[MarketScanSection] = None
    sectors: Optional[MarketScanSection] = None
    technicals: Optional[MarketScanSection] = None
    flows: Optional[MarketScanSection] = None
    politicians: Optional[PoliticiansSection] = None
    event_map: Optional[List[str]] = None


class Regime(BaseModel):
    tag: str = "Unknown"
    notes: Optional[str] = None


class Audit(BaseModel):
    double_source: bool = False
    all_timestamps_pt: bool = False
    coverage_policy: str = "two_distinct_http_hosts_per_claim_item"
    citation_coverage: List[Dict[str, Any]] = Field(default_factory=list)
    source_content_verified: bool = False
    warnings: List[str] = Field(default_factory=list)


class Meta(BaseModel):
    started_at: str
    completed_at: Optional[str] = None
    warnings: List[str] = []
    synthetic: bool = False
    execution: str = "unknown"
    timestamp_zone: Optional[str] = None


class RunOutput(BaseModel):
    meta: Meta
    regime: Regime
    market_scan: MarketScan
    trades: List[Trade]
    audit: Audit

