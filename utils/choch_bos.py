# -----------------------------
# 6. Detect CHoCH
# -----------------------------


def detect_choch(
    data,
    swings,
    structure,
    sweep_index=None,
    range_multiplier=1.5,
    volume_multiplier=1.5,
    lookback=20,
):

    if sweep_index is None:
        return None, None, None

    if len(data) < lookback + 1:
        return None, None, None

    highs = [s for s in swings if s[2] == "high"]
    lows = [s for s in swings if s[2] == "low"]

    # Start checking only AFTER sweep
    for i in range(sweep_index + 1, len(data)):

        current = data.iloc[i]

        current_close = current["Close"]
        current_high = current["High"]
        current_low = current["Low"]
        current_open = current["Open"]
        current_volume = current["Volume"]

        # --- Displacement ---
        recent_ranges = (data["High"] - data["Low"]).iloc[i - lookback : i]
        avg_range = recent_ranges.mean()

        current_range = current_high - current_low
        body_size = abs(current_close - current_open)
        body_percent = body_size / current_range if current_range != 0 else 0

        displacement = (
            current_range > range_multiplier * avg_range and body_percent > 0.6
        )

        # --- Volume expansion ---
        avg_volume = data["Volume"].iloc[i - lookback : i].mean()
        volume_expansion = current_volume > volume_multiplier * avg_volume

        reasons = []

        # --- Bullish CHoCH ---
        if structure == "bearish" and highs:
            last_lower_high = highs[-1][1]

            if current_close > last_lower_high:
                reasons.append("Closed above last lower high")

                if displacement:
                    reasons.append("Displacement confirmed")

                if volume_expansion:
                    reasons.append("Volume expansion confirmed")

                if displacement and volume_expansion:
                    return "bullish_choch", reasons, i

        # --- Bearish CHoCH ---
        if structure == "bullish" and lows:
            last_higher_low = lows[-1][1]

            if current_close < last_higher_low:
                reasons.append("Closed below last higher low")

                if displacement:
                    reasons.append("Displacement confirmed")

                if volume_expansion:
                    reasons.append("Volume expansion confirmed")

                if displacement and volume_expansion:
                    return "bearish_choch", reasons, i

    return None, None, None


# -----------------------------
# 5. Detect Break of Structure
# -----------------------------


def detect_bos(data, swings, structure):
    if not swings:
        return None

    highs = [s for s in swings if s[2] == "high"]
    lows = [s for s in swings if s[2] == "low"]

    if structure == "bullish" and highs:
        last_swing_high = highs[-1][1]
        current_close = data["Close"].iloc[-1]

        if current_close > last_swing_high:
            return "bullish_bos"

    if structure == "bearish" and lows:
        last_swing_low = lows[-1][1]
        current_close = data["Close"].iloc[-1]

        if current_close < last_swing_low:
            return "bearish_bos"

    return None
