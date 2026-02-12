import time
from models.continuation import detect_continuation_setup
import mt5
import state
from utils.alerts import send_telegram_alert
from utils.mt5_connector import get_data

print("Bot running (candle-close mode)...")

while True:

    # Get fresh data
    df_15m = get_data("EURUSDm", mt5.TIMEFRAME_M15, 300)

    # Use second-to-last candle
    closed_time = df_15m["Time"].iloc[-2]

    # Check if new candle closed
    if state.last_processed_time == closed_time:
        time.sleep(5)
        continue

    state.last_processed_time = closed_time

    print(f"\nNew 15M candle closed at {closed_time}")

    # Run your full logic here
    # sweep detection
    # choch detection
    # continuation model
    # telegram alerts

    # signal = detect_continuation_setup(
    #     df_15m, structure_m15, sweep_index, sweep_price, choch_index, swings_15
    # )

    if signal:
        send_telegram_alert(...)
        print("Signal sent")

    else:
        print("No setup on this candle")

    time.sleep(5)
