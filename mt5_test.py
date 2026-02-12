import MetaTrader5 as mt5
import pandas as pd

# Initialize connection
# if not mt5.initialize():
#     print("MT5 initialization failed")
#     mt5.shutdown()
#     quit()

# print("MT5 initialized successfully")

path = r"C:\Program Files\MetaTrader 5 EXNESS\terminal64.exe"

# account = 298407903
# password = "Python_1"
# server = "Exness-MT5Trial9"

# if not mt5.initialize(path=path, login=account, password=password, server=server):
#     print("Initialization failed, error code =", mt5.last_error())
#     quit()

if not mt5.initialize(path):
    print("Initialization failed, error code =", mt5.last_error())
    quit()

print("MT5 initialized successfully")

symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_M15
bars = 100

# rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)

# if rates is None:
#     print("Failed to get rates")
# else:
#     df = pd.DataFrame(rates)
#     df['time'] = pd.to_datetime(df['time'], unit='s')
#     print(df.head())
#     print(f"\nTotal candles received: {len(df)}")

# mt5.shutdown()

rates = mt5.copy_rates_from_pos("EURUSDm", mt5.TIMEFRAME_M15, 0, 100)

if rates is None:
    print("Failed to get rates:", mt5.last_error())
else:
    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    print(df.head())
    print("Total candles:", len(df))

mt5.shutdown()
