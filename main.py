import MetaTrader5 as mt5
import time as systime

import state
from utils.dataframe import format_dataframe
from utils.mt5_connector import connect, get_data, shutdown
from utils.structure import analyze_structure, find_swings
from utils.liquidity import detect_liquidity_sweep
from utils.choch_bos import detect_choch
from models.continuation import detect_continuation_setup
from utils.alerts import send_telegram_alert


# ===============================
# CONFIG
# ===============================

PAIRS = [
    # "EURUSDm",
    # "GBPUSDm",
    # "AUDUSDm",
    # "NZDUSDm",
    # "USDCHFm",
    # "USDCADm",
    # "USDJPYm",
]

symbol = "EURUSDm"

# print("Multi-pair scanner running (15M candle-close mode)...")

# ===============================
# CONNECT ONCE
# ===============================

if not connect():
    quit()

try:
    df_h4 = get_data(symbol, mt5.TIMEFRAME_H4)
    df_m15 = get_data(symbol, mt5.TIMEFRAME_M15)

    df_h4 = format_dataframe(df_h4)
    df_m15 = format_dataframe(df_m15)
    structure = analyze_structure(df_m15)

    print(structure)

    # print(structure["state"])
    # print(structure["momentum_score"])
    # print(structure["bos"])
    # while True:

    #     print("\n==============================")
    #     cycle_messages = []
    #     for symbol in PAIRS:

    #         print(f"Checking {symbol}")

    #         df_h4 = get_data(symbol, mt5.TIMEFRAME_H4)
    #         df_m15 = get_data(symbol, mt5.TIMEFRAME_M15)

    #         df_h4 = format_dataframe(df_h4)
    #         df_m15 = format_dataframe(df_m15)

    #         if df_m15 is None or len(df_m15) < 50:
    #             print(f"{symbol} → Not enough data")
    #             continue

    #         closed_time = df_m15.index[-2]  # candle close trigger only

    #         # Initialize memory for pair
    #         if symbol not in state.last_processed_time:
    #             state.last_processed_time[symbol] = None

    #         # Skip if already processed
    #         if state.last_processed_time[symbol] == closed_time:
    #             print(f"{symbol} → No new candle")
    #             continue

    #         state.last_processed_time[symbol] = closed_time

    #         print(f"{symbol} → New candle closed at {closed_time}")

    #         # STRUCTURE
    #         swings_h4 = find_swings(df_h4)
    #         structure_h4 = determine_structure(swings_h4)

    #         swings_m15 = find_swings(df_m15)
    #         structure_m15 = determine_structure(swings_m15)

    #         # LIQUIDITY
    #         liquidity_signal, sweep_index = detect_liquidity_sweep(df_m15, swings_m15)

    #         sweep_price = None
    #         if liquidity_signal and sweep_index is not None:
    #             if "bullish" in liquidity_signal:
    #                 sweep_price = df_m15["Low"].iloc[sweep_index]
    #             elif "bearish" in liquidity_signal:
    #                 sweep_price = df_m15["High"].iloc[sweep_index]

    #         # CHOCH
    #         choch_signal, reasons, choch_index = detect_choch(
    #             df_m15, swings_m15, structure_m15, sweep_index
    #         )

    #         # CONTINUATION
    #         signal = detect_continuation_setup(
    #             df_m15, structure_m15, sweep_index, sweep_price, choch_index, swings_m15
    #         )

    #         # ALERT SECTION
    #         if signal:

    #             message = f"""
    #         🚨 TRADE ALERT

    #         Pair: {symbol}
    #         Model: {signal['model']}
    #         Direction: {signal['direction'].upper()}
    #         Zone: {signal['zone_low']} - {signal['zone_high']}
    #         Entry: {signal['entry']}
    #         Stop: {signal['stop']}
    #         Target: {signal['target']}
    #         RR: {signal['rr']}
    #         """

    #         else:

    #             status = "Monitoring..."

    #             if liquidity_signal and not choch_signal:
    #                 status = "Liquidity sweep → waiting CHoCH"

    #             elif choch_signal:
    #                 status = "CHoCH detected → waiting retrace"

    #             elif structure_h4 != structure_m15:
    #                 status = "HTF / LTF not aligned"

    #             message = f"""
    #         📊 {symbol}
    #         4H: {structure_h4.upper()}
    #         15M: {structure_m15.upper()}
    #         Liquidity: {liquidity_signal}
    #         CHoCH: {choch_signal}
    #         Status: {status}
    #         """

    #         cycle_messages.append(message)

    #         # print(message)
    #     # send_telegram_alert(message)
    #     # if cycle_messages:
    #     #     final_message = "\n\n========================\n".join(cycle_messages)
    #     #     print(final_message)
    #     #     send_telegram_alert(final_message)

    #     # Sleep AFTER processing all pairs
    #     systime.sleep(10)

except KeyboardInterrupt:
    print("\nBot stopped manually.")
    shutdown()

# try:
#     while True:

#         for symbol in PAIRS:

#             # -------------------------
#             # GET DATA
#             # -------------------------
#             df_h4 = get_data(symbol, mt5.TIMEFRAME_H4)
#             df_m15 = get_data(symbol, mt5.TIMEFRAME_M15)

#             if df_h4 is None or df_m15 is None:
#                 print(f"{symbol} → No data returned")
#                 continue

#             if len(df_m15) < 50:
#                 continue

#             df_h4 = format_dataframe(df_h4)
#             df_m15 = format_dataframe(df_m15)

#             # -------------------------
#             # USE CLOSED CANDLE ONLY
#             # -------------------------
#             closed_time = df_m15.index[-2]

#             # Initialize pair memory
#             if symbol not in state.last_processed_time:
#                 state.last_processed_time[symbol] = None

#             # Skip if already processed
#             if state.last_processed_time[symbol] == closed_time:
#                 continue

#             # Update memory
#             state.last_processed_time[symbol] = closed_time

#             print(f"\n{symbol} → New 15M candle closed at {closed_time}")

#             # -------------------------
#             # STRUCTURE
#             # -------------------------
#             swings_h4 = find_swings(df_h4)
#             structure_h4 = determine_structure(swings_h4)

#             swings_m15 = find_swings(df_m15)
#             structure_m15 = determine_structure(swings_m15)

#             # -------------------------
#             # LIQUIDITY
#             # -------------------------
#             liquidity_signal, sweep_index = detect_liquidity_sweep(df_m15, swings_m15)

#             sweep_price = None
#             if liquidity_signal and sweep_index is not None:
#                 if "bullish" in liquidity_signal:
#                     sweep_price = df_m15["Low"].iloc[sweep_index]
#                 elif "bearish" in liquidity_signal:
#                     sweep_price = df_m15["High"].iloc[sweep_index]

#             # -------------------------
#             # CHOCH
#             # -------------------------
#             choch_signal, reasons, choch_index = detect_choch(
#                 df_m15, swings_m15, structure_m15, sweep_index
#             )

#             # -------------------------
#             # CONTINUATION MODEL
#             # -------------------------
#             signal = detect_continuation_setup(
#                 df_m15, structure_m15, sweep_index, sweep_price, choch_index, swings_m15
#             )

#             # -------------------------
#             # ALERT ONLY IF SIGNAL EXISTS
#             # -------------------------
#             if signal:

#                 message = f"""
#                                 🚨 *A-GRADE TRADE SETUP*

#                                 Pair: {symbol}
#                                 Model: {signal['model']}
#                                 Direction: {signal['direction'].upper()}

#                                 Zone: {signal['zone_low']} - {signal['zone_high']}
#                                 Entry: {signal['entry']}
#                                 Stop: {signal['stop']}
#                                 Target: {signal['target']}
#                                 RR: {signal['rr']}
#                                 """

#                 print(message)
#                 send_telegram_alert(message)
#                 print(f"{symbol} → Signal sent")

#             else:
#                 # print(f"{symbol} → No setup")
#                 # send_telegram_alert(f"{symbol} → No setup")
#                 status = "Monitoring..."

#                 if liquidity_signal and not choch_signal:
#                     status = "Liquidity sweep detected – waiting for CHoCH"

#                 elif choch_signal and not signal:
#                     status = "CHoCH detected – waiting for retrace into zone"

#                 elif structure_h4 != structure_m15:
#                     status = "HTF and LTF not aligned"

#                 elif structure_m15 == "bullish":
#                     status = "Bullish structure – no liquidity event"

#                 elif structure_m15 == "bearish":
#                     status = "Bearish structure – no liquidity event"

#                 message = f"""
#             📊 *MARKET STATE*

#             Pair: {symbol}

#             4H Bias: {structure_h4.upper()}
#             15M Structure: {structure_m15.upper()}
#             Liquidity: {liquidity_signal}
#             CHoCH: {choch_signal}

#             Status: {status}
#             """

#                 print(message)
#                 send_telegram_alert(message)

#         # Small delay to prevent CPU overuse
#         systime.sleep(5)

# except KeyboardInterrupt:
#     print("\nBot stopped manually.")
#     shutdown()

# ---------------------------------
# 8️⃣ PLOT
# ---------------------------------
# Create empty series
# swing_highs = pd.Series(np.nan, index=df_m15.index)
# swing_lows = pd.Series(np.nan, index=df_m15.index)

# for swing in swings_m15:
#     time, price, swing_type = swing
#     if swing_type == "high":
#         swing_highs.loc[time] = price
#     else:
#         swing_lows.loc[time] = price

# apds = [
#     mpf.make_addplot(swing_highs, type="scatter", marker="v", markersize=100),
#     mpf.make_addplot(swing_lows, type="scatter", marker="^", markersize=100),
# ]

# mpf.plot(
#     df_m15,
#     type="candle",
#     addplot=apds,
#     title=f"{symbol} M15 Structure ({structure_m15.upper()})",
#     style="charles",
#     volume=False,
# )
