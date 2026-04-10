from __future__ import annotations
from pathlib import Path
import pandas as pd

def load_universe_prices(
    universe_csv: Path,
    curated_dir: Path,
    price_col: str = "Close",
) -> pd.DataFrame:
    """
    Load Close prices for all tickers in universe into a wide DataFrame.
    Rows: Date, Columns: tickers
    """
    uni = pd.read_csv(universe_csv)
    series = {}

    for tkr in uni["ticker"]:
        fp = curated_dir / f"{tkr}.parquet"
        df = pd.read_parquet(fp)
        series[tkr] = df[price_col]

    prices = pd.DataFrame(series).sort_index()
    return prices

def momentum_rolling(prices: pd.DataFrame, lookback: int = 126) -> pd.DataFrame:
    """
    Rolling total return momentum: Close(t) / Close(t-lookback) - 1.
    Default lookback 126 ≈ 6 calendar months of trading days.
    """
    return prices.pct_change(lookback)

# Backward-compatible alias
def momentum_1m(prices: pd.DataFrame, lookback: int = 21) -> pd.DataFrame:
    return momentum_rolling(prices, lookback=lookback)
