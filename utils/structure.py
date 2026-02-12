# utils/structure.py

import numpy as np


# ---------------------------------------------------
# 1️⃣ Swing Detection With Tolerance
# ---------------------------------------------------
def find_swings(data, lookback=3, tolerance=0.0):
    swings = []

    for i in range(lookback, len(data) - lookback):
        high = data["High"].iloc[i]
        low = data["Low"].iloc[i]

        left_highs = data["High"].iloc[i - lookback : i]
        right_highs = data["High"].iloc[i + 1 : i + lookback + 1]

        left_lows = data["Low"].iloc[i - lookback : i]
        right_lows = data["Low"].iloc[i + 1 : i + lookback + 1]

        is_swing_high = all(high >= h * (1 - tolerance) for h in left_highs) and all(
            high >= h * (1 - tolerance) for h in right_highs
        )

        is_swing_low = all(low <= l * (1 + tolerance) for l in left_lows) and all(
            low <= l * (1 + tolerance) for l in right_lows
        )

        if is_swing_high:
            swings.append((data.index[i], high, "high"))

        if is_swing_low:
            swings.append((data.index[i], low, "low"))

    return swings


# ---------------------------------------------------
# 2️⃣ Direction Detection
# ---------------------------------------------------
def get_direction(swings):
    highs = [s for s in swings if s[2] == "high"]
    lows = [s for s in swings if s[2] == "low"]

    if len(highs) < 2 or len(lows) < 2:
        return "neutral"

    last_high, prev_high = highs[-1], highs[-2]
    last_low, prev_low = lows[-1], lows[-2]

    if last_high[1] > prev_high[1] and last_low[1] > prev_low[1]:
        return "bullish"

    if last_high[1] < prev_high[1] and last_low[1] < prev_low[1]:
        return "bearish"

    return "neutral"


# ---------------------------------------------------
# 3️⃣ BOS Detection (Close-Based)
# ---------------------------------------------------
def detect_bos(data, swings):
    if len(swings) < 2:
        return None

    last_swing = swings[-1]
    last_price = last_swing[1]
    last_type = last_swing[2]

    current_close = data["Close"].iloc[-1]

    if last_type == "high" and current_close > last_price:
        return {"type": "bullish_bos", "level": last_price, "index": data.index[-1]}

    if last_type == "low" and current_close < last_price:
        return {"type": "bearish_bos", "level": last_price, "index": data.index[-1]}

    return None


# ---------------------------------------------------
# 4️⃣ Structural Momentum Score
# ---------------------------------------------------
def calculate_momentum(swings):
    highs = [s[1] for s in swings if s[2] == "high"]
    lows = [s[1] for s in swings if s[2] == "low"]

    score = 0

    if len(highs) >= 3 and highs[-1] > highs[-2] > highs[-3]:
        score += 1

    if len(lows) >= 3 and lows[-1] > lows[-2] > lows[-3]:
        score += 1

    if len(highs) >= 3 and highs[-1] < highs[-2] < highs[-3]:
        score -= 1

    if len(lows) >= 3 and lows[-1] < lows[-2] < lows[-3]:
        score -= 1

    return score


# ---------------------------------------------------
# 5️⃣ Master Structure Engine
# ---------------------------------------------------
def analyze_structure(
    data, internal_lookback=3, external_lookback=7, tolerance=0.00005
):

    # Internal swings
    internal_swings = find_swings(data, internal_lookback, tolerance)
    internal_direction = get_direction(internal_swings)

    # External swings
    external_swings = find_swings(data, external_lookback, tolerance)
    external_direction = get_direction(external_swings)

    # BOS detection (based on internal)
    bos = detect_bos(data, internal_swings)

    # Momentum score
    momentum = calculate_momentum(internal_swings)

    # Structural state logic
    if internal_direction == external_direction:
        if internal_direction == "bullish":
            state = "bullish_continuation"
        elif internal_direction == "bearish":
            state = "bearish_continuation"
        else:
            state = "range"
    else:
        if internal_direction == "bullish":
            state = "bullish_transition"
        elif internal_direction == "bearish":
            state = "bearish_transition"
        else:
            state = "range"

    return {
        "external_direction": external_direction,
        "internal_direction": internal_direction,
        "state": state,
        "bos": bos,
        "momentum_score": momentum,
        "external_swings": external_swings,
        "internal_swings": internal_swings,
    }
