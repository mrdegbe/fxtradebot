def detect_zone_from_choch(data, choch_index, choch_type):
    """
    Zone = candle immediately before displacement candle.
    """

    if choch_index is None or choch_index < 1:
        return None

    base_candle = data.iloc[choch_index - 1]

    zone = {
        "type": "demand" if choch_type == "bullish_choch" else "supply",
        "high": base_candle['High'],
        "low": base_candle['Low'],
        "created_at": data.index[choch_index - 1]
    }

    return zone


def check_zone_retrace(data, zone):
    """
    Checks if price has retraced into zone.
    """

    if zone is None:
        return False

    current_price = data.iloc[-1]['Close']

    if zone["type"] == "demand":
        return zone["low"] <= current_price <= zone["high"]

    if zone["type"] == "supply":
        return zone["low"] <= current_price <= zone["high"]

    return False
