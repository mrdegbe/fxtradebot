from utils.helper import get_pip_size


# ------------------------------------------------
# REFINED BOS DETECTION (DISPLACEMENT REQUIRED)
# ------------------------------------------------
def detect_bos(
    symbol,
    data,
    swings,
    pip_buffer=2,
    displacement_multiplier=1.5,
    body_threshold=0.6,
    lookback=20,
):
    """
    Detect Break of Structure (BOS) using confirmed closed candles
    and displacement validation.
    """

    # ---------------------------------------------------
    # Guard Clauses
    # ---------------------------------------------------
    if len(swings) < 2:
        return None

    if len(data) < lookback + 2:
        return None

    # ---------------------------------------------------
    # Separate swing highs and lows
    # ---------------------------------------------------
    swing_highs = [s for s in swings if s[2] == "high"]
    swing_lows = [s for s in swings if s[2] == "low"]

    if not swing_highs or not swing_lows:
        return None

    last_high = swing_highs[-1]
    last_low = swing_lows[-1]

    # ---------------------------------------------------
    # Pip Buffer (prevents false micro breaks)
    # ---------------------------------------------------
    pip_value = get_pip_size(symbol)
    buffer = pip_buffer * pip_value

    # ---------------------------------------------------
    # Use Last CONFIRMED Closed Candle
    # ---------------------------------------------------
    candle = data.iloc[-2]

    current_open = candle["Open"]
    current_close = candle["Close"]
    current_high = candle["High"]
    current_low = candle["Low"]

    # ---------------------------------------------------
    # Displacement Calculation
    # ---------------------------------------------------
    current_range = current_high - current_low

    historical_ranges = (data["High"] - data["Low"]).iloc[-lookback - 1 : -2]
    avg_range = historical_ranges.mean()

    if avg_range == 0:
        return None

    body = abs(current_close - current_open)
    body_percent = body / current_range if current_range != 0 else 0

    displacement_confirmed = (
        current_range > displacement_multiplier * avg_range
        and body_percent > body_threshold
    )

    # ---------------------------------------------------
    # Bullish BOS Detection
    # ---------------------------------------------------
    if (
        current_close > last_high[1] + buffer
        and displacement_confirmed
        and current_close > current_open
    ):
        return {
            "type": "bullish_bos",
            "level": last_high[1],
            "break_price": current_close,
            "index": data.index[-2],
        }

    # ---------------------------------------------------
    # Bearish BOS Detection
    # ---------------------------------------------------
    if (
        current_close < last_low[1] - buffer
        and displacement_confirmed
        and current_close < current_open
    ):
        return {
            "type": "bearish_bos",
            "level": last_low[1],
            "break_price": current_close,
            "index": data.index[-2],
        }

    return None
