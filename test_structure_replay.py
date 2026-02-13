from utils.mt5_connector import get_data
from utils.structure import analyze_structure, reset_structure_memory
from utils.dataframe import format_dataframe
import MetaTrader5 as mt5
import pandas as pd


symbol = "USDCHFm"

if not mt5.initialize():
    print("MT5 initialize() failed")
    quit()

df_h4 = get_data(symbol, mt5.TIMEFRAME_H4)
df = format_dataframe(df_h4)

# print("Data range:", df.index.min(), "→", df.index.max())
# print("Total candles:", len(df))

print("===== REPLAY START =====")

# Proper datetime filtering
start_date = pd.Timestamp("2026-02-01 23:59")
end_date = pd.Timestamp("2026-02-10 23:59")

reset_structure_memory()

for i in range(10, len(df)):

    partial = df.iloc[:i]

    structure = analyze_structure(
        partial,
        internal_lookback=3,
        external_lookback=7,
        symbol=symbol,
    )

    current_time = partial.index[-1]

    # Correct datetime comparison
    if start_date <= current_time <= end_date:

        print(
            current_time,
            " | Ext:",
            structure["external_direction"],
            " | Int:",
            structure["internal_direction"],
            " | BOS:",
            structure["bos"],
            " | State:",
            structure["state"],
        )
