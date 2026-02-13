import MetaTrader5 as mt5
import pandas as pd


def connect():
    if not mt5.initialize():
        print("Initialization failed:", mt5.last_error())
        return False

    print("MT5 connected")
    return True


def get_data(symbol, timeframe, bars=60):

    if not mt5.symbol_select(symbol, True):
        print("Failed to select symbol")
        return None

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)

    if rates is None:
        print("Failed to get rates:", mt5.last_error())
        return None

    df = pd.DataFrame(rates)

    # Convert time column properly
    df["Time"] = pd.to_datetime(df["time"], unit="s")

    # Rename price columns
    df.rename(
        columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "tick_volume": "Volume",
        },
        inplace=True,
    )

    # Keep only what we need
    df = df[["Time", "Open", "High", "Low", "Close", "Volume"]]

    # Set datetime index
    df.set_index("Time", inplace=True)

    return df


def shutdown():
    mt5.shutdown()
