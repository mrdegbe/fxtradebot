import MetaTrader5 as mt5
import pandas as pd
import mplfinance as mpf
import numpy as np

from utils.dataframe import format_dataframe
from utils.mt5_connector import connect, get_data, shutdown
from utils.structure import determine_structure, find_swings
from utils.liquidity import detect_liquidity_sweep
from utils.choch_bos import detect_choch
from models.continuation import detect_continuation_setup

symbol = "USDJPYm"

# ---------------------------------
# 1️⃣ CONNECT
# ---------------------------------
if not connect():
    quit()

# ---------------------------------
# 2️⃣ GET DATA
# ---------------------------------
df_h4 = get_data(symbol, mt5.TIMEFRAME_H4)
df_m15 = get_data(symbol, mt5.TIMEFRAME_M15)

# Format early (important)
df_h4 = format_dataframe(df_h4)
df_m15 = format_dataframe(df_m15)

# ---------------------------------
# 3️⃣ STRUCTURE
# ---------------------------------
swings_h4 = find_swings(df_h4)
structure_h4 = determine_structure(swings_h4)

swings_m15 = find_swings(df_m15)
structure_m15 = determine_structure(swings_m15)

# ---------------------------------
# 4️⃣ LIQUIDITY
# ---------------------------------
liquidity_signal, sweep_index = detect_liquidity_sweep(df_m15, swings_m15)

sweep_price = None
if liquidity_signal and sweep_index is not None:
    if "bullish" in liquidity_signal:
        sweep_price = df_m15['Low'].iloc[sweep_index]
    elif "bearish" in liquidity_signal:
        sweep_price = df_m15['High'].iloc[sweep_index]

# ---------------------------------
# 5️⃣ CHOCH
# ---------------------------------
choch_signal, reasons, choch_index = detect_choch(
    df_m15,
    swings_m15,
    structure_m15,
    sweep_index
)

# ---------------------------------
# 6️⃣ CONTINUATION MODEL
# ---------------------------------
signal = detect_continuation_setup(
    df_m15,
    structure_m15,
    sweep_index,
    sweep_price,
    choch_index,
    swings_m15
)

# ---------------------------------
# 7️⃣ OUTPUT
# ---------------------------------
print("\n============================")
print("4H Bias:", structure_h4)
print("15M Structure:", structure_m15)
print("Liquidity:", liquidity_signal)
print("CHoCH:", choch_signal)

if structure_h4 != structure_m15:
    print("\nHTF and LTF not aligned → no continuation trade")
    shutdown()
    quit()


if signal:
    print("\n🔥 TRADE SIGNAL 🔥")
    for k, v in signal.items():
        print(f"{k}: {v}")
else:
    print("\nNo valid continuation setup")

print("============================\n")

shutdown()

# ---------------------------------
# 8️⃣ PLOT
# ---------------------------------
# Create empty series
swing_highs = pd.Series(np.nan, index=df_m15.index)
swing_lows = pd.Series(np.nan, index=df_m15.index)

for swing in swings_m15:
    time, price, swing_type = swing
    if swing_type == "high":
        swing_highs.loc[time] = price
    else:
        swing_lows.loc[time] = price

apds = [
    mpf.make_addplot(swing_highs, type='scatter', marker='v', markersize=100),
    mpf.make_addplot(swing_lows, type='scatter', marker='^', markersize=100)
]

mpf.plot(
    df_m15,
    type='candle',
    addplot=apds,
    title=f"{symbol} M15 Structure ({structure_m15.upper()})",
    style='charles',
    volume=False
)



# import MetaTrader5 as mt5
# import pandas as pd
# import mplfinance as mpf
# import numpy as np

# from utils.dataframe import format_dataframe
# from utils.mt5_connector import connect, get_data, shutdown
# from utils.structure import determine_structure, find_swings
# from utils.liquidity import detect_liquidity_sweep
# from utils.choch_bos import detect_choch
# from utils.zones import check_zone_retrace, detect_zone_from_choch


# symbol = "EURUSDm"

# if not connect():
#     quit()

# # --- Get Data ---
# df_h4 = get_data(symbol, mt5.TIMEFRAME_H4)
# df_m15 = get_data(symbol, mt5.TIMEFRAME_M15)

# # --- Structure ---
# swings_h4 = find_swings(df_h4)
# structure_h4 = determine_structure(swings_h4)

# swings_m15 = find_swings(df_m15)
# structure_m15 = determine_structure(swings_m15)

# # --- Liquidity ---
# liquidity_signal, sweep_index = detect_liquidity_sweep(df_m15, swings_m15)

# # --- CHoCH ---
# choch_signal, reasons, choch_index = detect_choch(
#     df_m15,
#     swings_m15,
#     structure_m15,
#     sweep_index
# )

# zone = None
# retrace = False

# if choch_signal:
#     zone = detect_zone_from_choch(df_m15, choch_index, choch_signal)

#     if zone:
#         retrace = check_zone_retrace(df_m15, zone)

# if zone:
#     print("Zone detected:", zone)

# if retrace:
#     print("Price retraced into zone → Entry condition met")


# print("4H Bias:", structure_h4)
# print("15M Structure:", structure_m15)
# print("Liquidity:", liquidity_signal)
# print("CHoCH:", choch_signal)

# shutdown()



# df_m15 = format_dataframe(df_m15)
# df_h4 = format_dataframe(df_h4)

# # -----------------------------
# # 3. Plot Candlestick Chart
# # -----------------------------
# # Create empty series full of NaN
# swing_highs = pd.Series(np.nan, index=df_m15.index)
# swing_lows = pd.Series(np.nan, index=df_m15.index)

# # Populate swing points
# for swing in swings_m15:
#     time, price, swing_type = swing
#     if swing_type == "high":
#         swing_highs.loc[time] = price
#     else:
#         swing_lows.loc[time] = price

# apds = [
#     mpf.make_addplot(swing_highs, type='scatter', marker='v', markersize=100),
#     mpf.make_addplot(swing_lows, type='scatter', marker='^', markersize=100)
# ]

# mpf.plot(
#     df_m15,
#     type='candle',
#     addplot=apds,
#     title=f"{symbol} M15 Structure ({structure_m15.upper()})",
#     style='charles',
#     volume=False
# )
