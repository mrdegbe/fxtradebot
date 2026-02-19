from structure.bos import detect_bos
from structure.momentum import calculate_momentum
import MetaTrader5 as mt5

TIMEFRAME_TREE = {
    "weekly": mt5.TIMEFRAME_W1,
    "daily": mt5.TIMEFRAME_D1,
    "setup": mt5.TIMEFRAME_H4,
    "refinement": mt5.TIMEFRAME_H1,
    "entry": mt5.TIMEFRAME_M15,
}


def evaluate_timeframe(symbol, timeframe, data, swings):

    bos = detect_bos(symbol, data, swings)
    momentum = calculate_momentum(swings)

    direction = "neutral"
    structure_state = "range"

    if bos:
        if "bullish" in bos["type"]:
            direction = "bullish"
            structure_state = "continuation"
        else:
            direction = "bearish"
            structure_state = "continuation"

    return {
        "direction": direction,
        "momentum": momentum,
        "structure_state": structure_state,
        "bos": bos,
    }
