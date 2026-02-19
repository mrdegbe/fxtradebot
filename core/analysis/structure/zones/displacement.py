# def is_displacement_candle(data, index, multiplier=1.5, lookback=20):

#     candle_range = data["High"].iloc[index] - data["Low"].iloc[index]
#     avg_range = (data["High"] - data["Low"]).iloc[index - lookback : index].mean()

#     if avg_range == 0:
#         return False

#     return candle_range > multiplier * avg_range

# def is_displacement_candle(data, index, multiplier=1.5, lookback=5):
#     """
#     Checks if candle represents displacement.
#     """

#     if index < lookback:
#         return False

#     body = abs(
#         data["Close"].iloc[index] - data["Open"].iloc[index]
#     )

#     avg_body = (
#         abs(data["Close"].iloc[index - lookback:index] -
#             data["Open"].iloc[index - lookback:index])
#         .mean()
#     )

#     return body > avg_body * multiplier


def calculate_displacement_strength(data, index, lookback=5):
    if index < lookback:
        return 0

    body = abs(data["Close"].iloc[index] - data["Open"].iloc[index])

    avg_body = abs(
        data["Close"].iloc[index - lookback : index]
        - data["Open"].iloc[index - lookback : index]
    ).mean()

    if avg_body == 0:
        return 0

    return body / avg_body


def is_displacement_candle(data, index, threshold=1.5):
    strength = calculate_displacement_strength(data, index)
    return strength >= threshold
