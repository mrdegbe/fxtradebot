# analysis/mtf/timeframe_map.py

from dataclasses import dataclass
from typing import Dict
import MetaTrader5 as mt5


@dataclass(frozen=True)
class TimeframeConfig:
    name: str  # Logical name
    code: str  # Broker / data provider code
    rank: int  # Higher = higher timeframe
    role: str  # "context", "setup", "entry"
    update_on_close: bool  # Only update after candle close?


# ---------------------------
# Your Trading Hierarchy
# ---------------------------

TIMEFRAMES: Dict[str, TimeframeConfig] = {
    "weekly": TimeframeConfig(
        name="weekly",
        code=mt5.TIMEFRAME_W1,
        rank=5,
        role="context",
        update_on_close=True,
    ),
    "daily": TimeframeConfig(
        name="daily",
        code=mt5.TIMEFRAME_D1,
        rank=4,
        role="context",
        update_on_close=True,
    ),
    "h4": TimeframeConfig(
        name="h4", code=mt5.TIMEFRAME_H4, rank=3, role="setup", update_on_close=True
    ),
    "h1": TimeframeConfig(
        name="h1",
        code=mt5.TIMEFRAME_H1,
        rank=2,
        role="refinement",
        update_on_close=True,
    ),
    "m15": TimeframeConfig(
        name="m15", code=mt5.TIMEFRAME_M15, rank=1, role="entry", update_on_close=True
    ),
}
