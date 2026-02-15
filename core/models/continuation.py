import state


def detect_continuation_setup(
    data,
    structure,
    sweep_index,
    sweep_price,
    choch_index,
    swings,
    rr_min=2.5,
    buffer=0.0001,
):

    if sweep_index is None or choch_index is None:
        return None

    # ---------------------------------
    # 1️⃣ Displacement candle = CHoCH candle
    # ---------------------------------
    displacement_index = choch_index
    zone_index = displacement_index - 1

    if zone_index <= 0:
        return None

    zone_high = data["High"].iloc[zone_index]
    zone_low = data["Low"].iloc[zone_index]

    # ---------------------------------
    # 2️⃣ Entry = midpoint of zone
    # ---------------------------------
    entry = (zone_high + zone_low) / 2

    # ---------------------------------
    # 3️⃣ Stop below sweep
    # ---------------------------------
    if structure == "bullish":
        stop = sweep_price - buffer
    elif structure == "bearish":
        stop = sweep_price + buffer
    else:
        return None

    # ---------------------------------
    # 4️⃣ Target = previous opposing swing
    # ---------------------------------
    if structure == "bullish":
        opposing_swings = [s for s in swings if s[2] == "high"]
        if not opposing_swings:
            return None
        target = opposing_swings[-1][1]

        risk = entry - stop
        reward = target - entry

    else:  # bearish
        opposing_swings = [s for s in swings if s[2] == "low"]
        if not opposing_swings:
            return None
        target = opposing_swings[-1][1]

        risk = stop - entry
        reward = entry - target

    if risk <= 0:
        return None

    rr = reward / risk

    # ---------------------------------
    # 5️⃣ RR Filter
    # ---------------------------------
    if rr < rr_min:
        return None

    # ---------------------------------
    # 6️⃣ Return Signal
    # ---------------------------------
    signal = {
        "model": "continuation",
        "grade": "A",
        "direction": structure,
        "zone_high": zone_high,
        "zone_low": zone_low,
        "entry": round(entry, 5),
        "stop": round(stop, 5),
        "target": round(target, 5),
        "rr": round(rr, 2),
    }

    return signal
