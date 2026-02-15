
# ===================================================
# 1️⃣ SWING DETECTION
# ===================================================
def find_swings(data, lookback: int = 3, tolerance: float = 0.0):
    """
    Detect swing highs and swing lows using symmetric lookback confirmation.

    Args:
        data: OHLC dataframe with 'High' and 'Low' columns
        lookback: Number of candles to check on each side
        tolerance: Percentage tolerance for near-equal highs/lows

    Returns:
        List of tuples:
        (timestamp, price, 'high' or 'low')
    """

    swings = []

    highs = data["High"]
    lows = data["Low"]
    index = data.index

    for i in range(lookback, len(data) - lookback):

        current_high = highs.iloc[i]
        current_low = lows.iloc[i]

        left_highs = highs.iloc[i - lookback : i]
        right_highs = highs.iloc[i + 1 : i + lookback + 1]

        left_lows = lows.iloc[i - lookback : i]
        right_lows = lows.iloc[i + 1 : i + lookback + 1]

        is_swing_high = all(
            current_high >= h * (1 - tolerance) for h in left_highs
        ) and all(current_high >= h * (1 - tolerance) for h in right_highs)

        is_swing_low = all(
            current_low <= l * (1 + tolerance) for l in left_lows
        ) and all(current_low <= l * (1 + tolerance) for l in right_lows)

        if is_swing_high:
            swings.append((index[i], current_high, "high"))

        if is_swing_low:
            swings.append((index[i], current_low, "low"))

    return swings


# ===================================================
# 2️⃣ STRICT FRACTAL ALTERNATION
# ===================================================
def strict_alternation_structure(swings):
    """
    Enforce strict alternation between swing highs and lows.

    Removes consecutive swings of the same type by keeping
    only the most extreme one.

    Args:
        swings: List of tuples -> (timestamp, price, type)

    Returns:
        Cleaned list of alternating swings.
    """

    if not swings:
        return []

    cleaned = [swings[0]]

    for swing in swings[1:]:
        last = cleaned[-1]

        swing_time, swing_price, swing_type = swing
        _, last_price, last_type = last

        # If swing type alternates → valid structure
        if swing_type != last_type:
            cleaned.append(swing)
            continue

        # Same type → keep the more extreme swing
        if swing_type == "low" and swing_price < last_price:
            cleaned[-1] = swing

        elif swing_type == "high" and swing_price > last_price:
            cleaned[-1] = swing

    return cleaned
