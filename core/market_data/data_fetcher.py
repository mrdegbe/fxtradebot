import MetaTrader5 as mt5
import pandas as pd


def get_data(symbol: str, timeframe: int, bars: int = 120) -> pd.DataFrame | None:
    """
    Fetch OHLCV data from MetaTrader5 and return as a cleaned DataFrame.

    Args:
        symbol: Trading symbol (e.g. 'EURUSD')
        timeframe: MT5 timeframe constant
        bars: Number of bars to retrieve

    Returns:
        Pandas DataFrame indexed by Time or None if request fails
    """

    # Ensure symbol is available
    if not mt5.symbol_select(symbol, True):
        print(f"Failed to select symbol: {symbol}")
        return None

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)

    if rates is None:
        print(f"Failed to get rates: {mt5.last_error()}")
        return None

    df = pd.DataFrame(rates)

    # Format dataframe
    df = (
        df.rename(
            columns={
                "time": "Time",
                "open": "Open",
                "high": "High",
                "low": "Low",
                "close": "Close",
                "tick_volume": "Volume",
            }
        )
        .assign(Time=lambda x: pd.to_datetime(x["Time"], unit="s"))
        .loc[:, ["Time", "Open", "High", "Low", "Close", "Volume"]]
        .set_index("Time")
    )

    return df
