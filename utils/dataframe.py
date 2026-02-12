# -----------------------------
# Data Formatting
# -----------------------------
def format_dataframe(df):
    df.rename(
        columns={
            "time": "Time",
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "tick_volume": "Volume",
        },
        inplace=True,
    )
    return df
