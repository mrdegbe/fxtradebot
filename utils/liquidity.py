# -----------------------------
# Detect Liquidity Sweeps
# -----------------------------
def detect_liquidity_sweep(df, swings, lookback=30):
    """
    Scan last N candles for most recent liquidity sweep.
    """

    if len(swings) < 1:
        return None, None

    last_swing_time, last_swing_price, last_swing_type = swings[-1]

    recent_data = df.iloc[-lookback:]

    sweep_type = None
    sweep_index = None

    for i in range(len(recent_data)):
        candle = recent_data.iloc[i]
        actual_index = len(df) - lookback + i

        # Bullish sweep
        if last_swing_type == "low":
            if candle["Low"] < last_swing_price and candle["Close"] > last_swing_price:
                sweep_type = "bullish_sweep"
                sweep_index = actual_index

        # Bearish sweep
        if last_swing_type == "high":
            if candle["High"] > last_swing_price and candle["Close"] < last_swing_price:
                sweep_type = "bearish_sweep"
                sweep_index = actual_index

    return sweep_type, sweep_index
