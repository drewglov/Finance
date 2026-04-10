from __future__ import annotations
import pandas as pd

def qc_metrics(df: pd.DataFrame) -> dict:
    """
    Compute basic QC metrics for a standardized OHLCV DataFrame.
    Assumes:
      - index is Date
      - columns: Open, High, Low, Close, Volume
    Returns a dict of metrics.
    """
    n_rows = len(df)

    # price validity
    nonpos_price_rows = (df[["Open", "High", "Low", "Close"]] <= 0).any(axis=1).sum()

    # OHLC consistency
    bad_high = (df["High"] < df[["Open", "Close"]].max(axis=1)).sum()
    bad_low  = (df["Low"]  > df[["Open", "Close"]].min(axis=1)).sum()

    # volume checks
    zero_volume_rows = (df["Volume"] <= 0).sum()

    # time span
    start_date = df.index.min()
    end_date = df.index.max()

    return {
        "rows": int(n_rows),
        "start_date": start_date,
        "end_date": end_date,
        "nonpos_price_rows": int(nonpos_price_rows),
        "bad_high_rows": int(bad_high),
        "bad_low_rows": int(bad_low),
        "zero_volume_rows": int(zero_volume_rows),
    }
