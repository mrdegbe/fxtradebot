from dataclasses import dataclass
from typing import List, Tuple, Optional
import pandas as pd

Swing = Tuple[pd.Timestamp, float, str]


@dataclass
class Bias:
    external: str
    internal: str


@dataclass
class StructureSnapshot:
    symbol: str
    timeframe: Optional[str]

    bias: Bias
    state: str

    bos_event: Optional[dict]
    momentum: int

    external_swings: List[Swing]
    internal_swings: List[Swing]


@dataclass
class TopdownSnapshot:
    symbol: str

    weekly: StructureSnapshot
    daily: StructureSnapshot
    h4: StructureSnapshot
    m15: StructureSnapshot

    dominant_bias: str
    alignment_score: int
    trade_context: str
    trade_allowed: bool
