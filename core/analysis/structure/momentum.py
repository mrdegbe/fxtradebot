
# ===================================================
# 5️⃣ STRUCTURAL MOMENTUM
# ===================================================
def calculate_momentum(swings):
    """
    Calculate structural momentum score based on progression
    of recent swing highs and lows.

    Returns:
        int: Momentum score
             +2 = strong bullish momentum
             +1 = bullish momentum
              0 = neutral / mixed
             -1 = bearish momentum
             -2 = strong bearish momentum
    """

    # ---------------------------------------------------
    # Extract swing highs and lows
    # ---------------------------------------------------
    highs = [price for _, price, t in swings if t == "high"]
    lows = [price for _, price, t in swings if t == "low"]

    score = 0

    # ---------------------------------------------------
    # Higher Highs → Bullish Strength
    # ---------------------------------------------------
    if len(highs) >= 3:
        if highs[-3] < highs[-2] < highs[-1]:
            score += 1

    # ---------------------------------------------------
    # Higher Lows → Bullish Strength
    # ---------------------------------------------------
    if len(lows) >= 3:
        if lows[-3] < lows[-2] < lows[-1]:
            score += 1

    # ---------------------------------------------------
    # Lower Highs → Bearish Strength
    # ---------------------------------------------------
    if len(highs) >= 3:
        if highs[-3] > highs[-2] > highs[-1]:
            score -= 1

    # ---------------------------------------------------
    # Lower Lows → Bearish Strength
    # ---------------------------------------------------
    if len(lows) >= 3:
        if lows[-3] > lows[-2] > lows[-1]:
            score -= 1

    return score
