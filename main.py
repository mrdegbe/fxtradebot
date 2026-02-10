import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 1. Load price data
# -----------------------------

# For now, we use a CSV file
# You will replace this later with MT5 data

df = pd.read_csv("data.csv")

# Ensure correct order
df = df.sort_values("timestamp").reset_index(drop=True)


# -----------------------------
# 2. Detect swing highs & lows
# -----------------------------

LOOKBACK = 2

def detect_swings(data, lookback):
    swings = []

    for i in range(lookback, len(data) - lookback):
        high = data.loc[i, "high"]
        low = data.loc[i, "low"]

        prev_highs = data.loc[i-lookback:i-1, "high"]
        next_highs = data.loc[i+1:i+lookback, "high"]

        prev_lows = data.loc[i-lookback:i-1, "low"]
        next_lows = data.loc[i+1:i+lookback, "low"]

        if high > prev_highs.max() and high > next_highs.max():
            swings.append((i, high, "high"))

        if low < prev_lows.min() and low < next_lows.min():
            swings.append((i, low, "low"))

    return swings


swings = detect_swings(df, LOOKBACK)


# -----------------------------
# 3. Plot price + structure
# -----------------------------

plt.figure(figsize=(14, 6))
plt.plot(df["close"], label="Close Price", color="black")

for index, price, swing_type in swings:
    if swing_type == "high":
        plt.scatter(index, price, color="red", s=50)
    else:
        plt.scatter(index, price, color="green", s=50)

plt.title("Market Structure – Swing Highs & Lows")
plt.legend()
plt.show()
