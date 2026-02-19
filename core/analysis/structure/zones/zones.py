from core.analysis.structure.zones.displacement import (
    calculate_displacement_strength,
    is_displacement_candle,
)
from core.analysis.structure.zones.imbalances import detect_imbalance


def build_zone_from_base(data, base_index, zone_type):
    """
    Builds zone from base candle.
    """

    high = data["High"].iloc[base_index]
    low = data["Low"].iloc[base_index]

    if zone_type == "demand":
        return {
            "type": "demand",
            "proximal": high,
            "distal": low,
            "base_index": base_index,
        }

    else:
        return {
            "type": "supply",
            "proximal": low,
            "distal": high,
            "base_index": base_index,
        }


def build_zone(data, base_index, imbalance, strength):
    base_high = data["High"].iloc[base_index]
    base_low = data["Low"].iloc[base_index]

    timestamp = data.index[base_index]

    if imbalance["type"] == "bullish":
        zone_type = "demand"
        proximal = base_high
        distal = base_low
    else:
        zone_type = "supply"
        proximal = base_low
        distal = base_high

    return {
        "type": zone_type,
        "base_candle_index": int(base_index),
        "proximal": float(proximal),
        "distal": float(distal),
        "imbalance_range": {
            "low": float(imbalance["low"]),
            "high": float(imbalance["high"]),
        },
        "displacement_strength": float(strength),
        "timestamp": timestamp,
    }


def detect_base_zones(data):
    zones = []

    for i in range(len(data)):

        imbalance = detect_imbalance(data, i)
        if not imbalance:
            continue

        if not is_displacement_candle(data, i):
            continue

        base_index = i - 1
        if base_index < 0:
            continue

        strength = calculate_displacement_strength(data, i)

        zone = build_zone(
            data,
            base_index,
            imbalance,
            strength,
        )

        zones.append(zone)

    return {"zones": zones}
