# def has_imb(data, index):

#     if index < 2:
#         return False

#     c1_high = data["High"].iloc[index - 2]
#     c3_low = data["Low"].iloc[index]

#     bullish_fvg = c1_high < c3_low

#     c1_low = data["Low"].iloc[index - 2]
#     c3_high = data["High"].iloc[index]

#     bearish_fvg = c1_low > c3_high

#     return bullish_fvg or bearish_fvg

# def detect_imbalance(data, index):
#     """
#     Detects inefficiency gap at given candle index.

#     Returns:
#         dict | None
#     """

#     if index < 2:
#         return None

#     prev_high = data["High"].iloc[index - 2]
#     prev_low = data["Low"].iloc[index - 2]

#     current_high = data["High"].iloc[index]
#     current_low = data["Low"].iloc[index]

#     # Bullish imbalance
#     if current_low > prev_high:
#         return {
#             "type": "bullish",
#             "gap_low": prev_high,
#             "gap_high": current_low,
#         }

#     # Bearish imbalance
#     if current_high < prev_low:
#         return {
#             "type": "bearish",
#             "gap_low": current_high,
#             "gap_high": prev_low,
#         }

#     return None


def detect_imbalance(data, index):
    if index < 2:
        return None

    prev_high = data["High"].iloc[index - 2]
    prev_low = data["Low"].iloc[index - 2]

    current_high = data["High"].iloc[index]
    current_low = data["Low"].iloc[index]

    # Bullish imbalance
    if current_low > prev_high:
        return {
            "type": "bullish",
            "low": prev_high,
            "high": current_low,
        }

    # Bearish imbalance
    if current_high < prev_low:
        return {
            "type": "bearish",
            "low": current_high,
            "high": prev_low,
        }

    return None
