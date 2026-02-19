from core.models.analysis import Bias, StructureSnapshot, TopdownSnapshot
from infra.config.timeframes import analyze_timeframe
import MetaTrader5 as mt5


from dataclasses import dataclass
from typing import Optional, List

# timeframes = [mt5.TIMEFRAME_W1, mt5.TIMEFRAME_D1, mt5.TIMEFRAME_H4, mt5.TIMEFRAME_M15]


@dataclass
class TimeframeBias:
    timeframe: str
    direction: str  # "bullish", "bearish", "neutral"
    momentum_score: int
    structure_state: str  # "continuation", "pullback", "reversal"
    supply_zone: Optional[tuple]
    demand_zone: Optional[tuple]


@dataclass
class TopDownContext:
    overall_bias: str
    weekly: TimeframeBias
    daily: TimeframeBias
    h4: TimeframeBias
    entry_timeframe: str


def build_market_context(symbol=None):

    # For simplicity, we will just call the analyze_timeframe function for each timeframe

    """
    Builds a comprehensive market context snapshot for the given symbol.
    If symbol is None, returns a default snapshot with empty data.
    """

    if symbol is None:
        snapshots = {}
        for tf in timeframes:
            snapshots[tf] = analyze_timeframe(symbol, tf)
        return TopdownSnapshot(symbol=symbol, snapshots=snapshots)

    # In a real implementation, this would involve more complex logic and data fetching
    weekly_snapshot = analyze_timeframe(symbol, "weekly")
    daily_snapshot = analyze_timeframe(symbol, "daily")
    h4_snapshot = analyze_timeframe(symbol, "h4")
    m15_snapshot = analyze_timeframe(symbol, "m15")

    # Determine dominant bias (simplified logic)
    dominant_bias = weekly_snapshot.bias.external or daily_snapshot.bias.external

    # Build the topdown snapshot
    topdown_snapshot = TopdownSnapshot(
        symbol=symbol,
        weekly=weekly_snapshot,
        daily=daily_snapshot,
        h4=h4_snapshot,
        m15=m15_snapshot,
        dominant_bias=dominant_bias,
        alignment_score=0,  # Placeholder
        trade_context="",  # Placeholder
        trade_allowed=False,  # Placeholder
    )

    return topdown_snapshot
