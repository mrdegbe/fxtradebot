# utils/structure.py

import numpy as np
from utils.helper import get_pip_size


# ===================================================
# 1️⃣ SWING DETECTION
# ===================================================
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


# ===================================================
# 2️⃣ STRICT FRACTAL ALTERNATION
# ===================================================
def strict_alternation_structure(swings):
    if not swings:
        return []

    cleaned = [swings[0]]

    for swing in swings[1:]:
        last = cleaned[-1]

        # Alternate type
        if swing[2] != last[2]:
            cleaned.append(swing)
        else:
            # Replace with more extreme swing
            if swing[2] == "low" and swing[1] < last[1]:
                cleaned[-1] = swing
            elif swing[2] == "high" and swing[1] > last[1]:
                cleaned[-1] = swing

    return cleaned


# ===================================================
# 3️⃣ SEQUENTIAL STRUCTURE DIRECTION
# ===================================================
def get_direction(swings, tolerance=0.0):
    """
    Determine structural direction using sequential swing logic.
    Requires strictly alternating swings.
    """

    if len(swings) < 4:
        return "neutral"

    # Last 4 swings define latest structural cycle
    s1, s2, s3, s4 = swings[-4:]

    # Case 1: high → low → high → low
    if s1[2] == "high" and s2[2] == "low" and s3[2] == "high" and s4[2] == "low":

        prev_high = s1[1]
        prev_low = s2[1]
        last_high = s3[1]
        last_low = s4[1]

        if last_high > prev_high * (1 - tolerance) and last_low > prev_low * (
            1 - tolerance
        ):
            return "bullish"

        if last_high < prev_high * (1 + tolerance) and last_low < prev_low * (
            1 + tolerance
        ):
            return "bearish"

    # Case 2: low → high → low → high
    elif s1[2] == "low" and s2[2] == "high" and s3[2] == "low" and s4[2] == "high":

        prev_low = s1[1]
        prev_high = s2[1]
        last_low = s3[1]
        last_high = s4[1]

        if last_high > prev_high * (1 - tolerance) and last_low > prev_low * (
            1 - tolerance
        ):
            return "bullish"

        if last_high < prev_high * (1 + tolerance) and last_low < prev_low * (
            1 + tolerance
        ):
            return "bearish"

    return "neutral"


# ===================================================
# 4️⃣ REFINED BOS DETECTION (DISPLACEMENT REQUIRED)
# ===================================================
def detect_bos(
    symbol,
    data,
    swings,
    pip_buffer=2,
    displacement_multiplier=1.5,
    body_threshold=0.6,
    lookback=20,
):

    if len(swings) < 2 or len(data) < lookback + 2:
        return None

    highs = [s for s in swings if s[2] == "high"]
    lows = [s for s in swings if s[2] == "low"]

    if not highs or not lows:
        return None

    pip_value = get_pip_size(symbol)
    buffer = pip_buffer * pip_value

    last_high = highs[-1]
    last_low = lows[-1]

    # Use confirmed closed candle
    # Use confirmed closed candle
    current_close = data["Close"].iloc[-2]
    current_open = data["Open"].iloc[-2]
    current_high = data["High"].iloc[-2]
    current_low = data["Low"].iloc[-2]

    current_range = current_high - current_low
    avg_range = (data["High"] - data["Low"]).iloc[-lookback - 1 : -2].mean()

    if avg_range == 0:
        return None

    body = abs(current_close - current_open)
    body_percent = body / current_range if current_range != 0 else 0

    displacement = (
        current_range > displacement_multiplier * avg_range
        and body_percent > body_threshold
    )

    # Bullish BOS
    if (
        current_close > last_high[1] + buffer
        and displacement
        and current_close > current_open
    ):
        return {
            "type": "bullish_bos",
            "level": last_high[1],
            "break_price": current_close,
            "index": data.index[-2],
        }

    # Bearish BOS
    if (
        current_close < last_low[1] - buffer
        and displacement
        and current_close < current_open
    ):
        return {
            "type": "bearish_bos",
            "level": last_low[1],
            "break_price": current_close,
            "index": data.index[-2],
        }

    return None


# ===================================================
# 5️⃣ STRUCTURAL MOMENTUM
# ===================================================
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


def compress_structure_after_bos(swings, bos):
    """
    Compress swings after confirmed BOS.
    Keeps only the protected level and the new structural break.
    """

    if not bos or len(swings) < 2:
        return swings

    level = bos["level"]
    bos_type = bos["type"]

    # Find swing that was broken
    broken_index = None
    for i, s in enumerate(swings):
        if abs(s[1] - level) < 1e-10:
            broken_index = i
            break

    if broken_index is None:
        return swings

    if bos_type == "bullish_bos":
        # Keep last low before broken high
        for j in range(broken_index - 1, -1, -1):
            if swings[j][2] == "low":
                return [swings[j], swings[-1]]

    elif bos_type == "bearish_bos":
        # Keep last high before broken low
        for j in range(broken_index - 1, -1, -1):
            if swings[j][2] == "high":
                return [swings[j], swings[-1]]

    return swings


# ===================================================
# 6️⃣ MASTER STRUCTURE ENGINE (MULTI-PAIR SAFE)
# ===================================================
def analyze_structure(
    data,
    internal_lookback: int = 3,
    external_lookback: int = 7,
    tolerance: float = 0.00005,
    symbol: str | None = None,
):
    """
    Multi-pair market structure analyzer.
    Maintains persistent structural bias per symbol.
    """

    # ---------------------------------------------------
    # Validate symbol (required for multi-pair state)
    # ---------------------------------------------------
    if symbol is None:
        raise ValueError("Symbol must be provided for multi-pair structure tracking.")

    # ---------------------------------------------------
    # Initialize persistent state container
    # ---------------------------------------------------
    if not hasattr(analyze_structure, "_state"):
        analyze_structure._state = {}

    # Create symbol state if not existing
    if symbol not in analyze_structure._state:
        analyze_structure._state[symbol] = {
            "bias": None,
            "pending_bos": None,
            "pending_level": None,
            "awaiting_pullback": False,
        }

    state_memory = analyze_structure._state[symbol]

    # ---------------------------------------------------
    # External (macro) structure
    # ---------------------------------------------------
    external_swings = strict_alternation_structure(
        find_swings(data, external_lookback, tolerance)
    )

    # ---------------------------------------------------
    # Internal (micro) structure
    # ---------------------------------------------------
    internal_swings = strict_alternation_structure(
        find_swings(data, internal_lookback, tolerance)
    )

    internal_direction = get_direction(internal_swings)

    # ---------------------------------------------------
    # Detect Break of Structure (BOS)
    # ---------------------------------------------------
    bos = detect_bos(symbol, data, internal_swings)

    if bos:
        internal_swings = compress_structure_after_bos(internal_swings, bos)

    momentum = calculate_momentum(internal_swings)

    # ---------------------------------------------------
    # Structural baseline direction
    # ---------------------------------------------------
    structural_direction = get_direction(external_swings)

    # Initialize bias first time only
    if state_memory["bias"] is None:
        state_memory["bias"] = structural_direction

    # ---------------------------------------------------
    # Register BOS (but do not flip bias yet)
    # ---------------------------------------------------
    if bos:
        state_memory.update(
            {
                "pending_bos": bos["type"],
                "pending_level": bos["level"],
                "awaiting_pullback": True,
            }
        )

    # ---------------------------------------------------
    # Pullback confirmation logic
    # ---------------------------------------------------
    if state_memory["awaiting_pullback"]:

        last_close = data["Close"].iloc[-2]
        pending_type = state_memory["pending_bos"]
        pending_level = state_memory["pending_level"]

        # Bullish confirmation
        if (
            pending_type == "bullish_bos"
            and internal_direction == "bearish"
            and last_close > pending_level
        ):
            state_memory.update(
                {
                    "bias": "bullish",
                    "pending_bos": None,
                    "pending_level": None,
                    "awaiting_pullback": False,
                }
            )

        # Bearish confirmation
        elif (
            pending_type == "bearish_bos"
            and internal_direction == "bullish"
            and last_close < pending_level
        ):
            state_memory.update(
                {
                    "bias": "bearish",
                    "pending_bos": None,
                    "pending_level": None,
                    "awaiting_pullback": False,
                }
            )

    external_direction = state_memory["bias"]

    # ---------------------------------------------------
    # Structural state classification
    # ---------------------------------------------------
    state = "distribution"

    if external_direction == "bullish":
        if bos and bos["type"] == "bullish_bos":
            state = "bullish_expansion"
        elif internal_direction == "bearish":
            state = "bullish_correction"
        else:
            state = "bullish_expansion"

    elif external_direction == "bearish":
        if bos and bos["type"] == "bearish_bos":
            state = "bearish_expansion"
        elif internal_direction == "bullish":
            state = "bearish_correction"
        else:
            state = "bearish_expansion"

    else:
        state = "transition" if internal_direction != "neutral" else "distribution"

    return {
        "symbol": symbol,
        "external_direction": external_direction,
        "internal_direction": internal_direction,
        "state": state,
        "bos": bos,
        "momentum_score": momentum,
        "external_swings": external_swings,
        "internal_swings": internal_swings,
    }
