# -----------------------------
# 2. Structure Logic (Swings)
# -----------------------------


def find_swings(data, lookback=3):
    swings = []

    for i in range(lookback, len(data) - lookback):
        high = data["High"].iloc[i]
        low = data["Low"].iloc[i]

        is_swing_high = all(
            high > data["High"].iloc[i - j] for j in range(1, lookback + 1)
        ) and all(high > data["High"].iloc[i + j] for j in range(1, lookback + 1))

        is_swing_low = all(
            low < data["Low"].iloc[i - j] for j in range(1, lookback + 1)
        ) and all(low < data["Low"].iloc[i + j] for j in range(1, lookback + 1))

        if is_swing_high:
            swings.append((data.index[i], high, "high"))

        if is_swing_low:
            swings.append((data.index[i], low, "low"))

    # print(f"Swings {swings[0]}")

    return swings


# -----------------------------
# 4. Determine market structure
# -----------------------------


def determine_structure(swings):
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


# def find_swings(data, lookback=3):
#     swings = []

#     for i in range(lookback, len(data) - lookback):
#         high = data['High'].iloc[i]
#         low = data['Low'].iloc[i]

#         is_swing_high = all(high > data['High'].iloc[i - j] for j in range(1, lookback + 1)) and \
#                         all(high > data['High'].iloc[i + j] for j in range(1, lookback + 1))

#         is_swing_low = all(low < data['Low'].iloc[i - j] for j in range(1, lookback + 1)) and \
#                        all(low < data['Low'].iloc[i + j] for j in range(1, lookback + 1))

#         if is_swing_high:
#             swings.append((data.index[i], high, "high"))

#         if is_swing_low:
#             swings.append((data.index[i], low, "low"))

#     return swings
