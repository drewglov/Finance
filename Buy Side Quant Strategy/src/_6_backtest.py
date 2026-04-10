from __future__ import annotations
import pandas as pd
import numpy as np

def monthly_rebalance_dates(prices: pd.DataFrame) -> pd.DatetimeIndex:
    month_end_trading_days = (
        prices.index.to_series()
        .groupby(prices.index.to_period("M"))
        .last()
    )
    return pd.DatetimeIndex(month_end_trading_days.values)

def quarterly_rebalance_dates(prices: pd.DataFrame) -> pd.DatetimeIndex:
    quarter_end_trading_days = (
        prices.index.to_series()
        .groupby(prices.index.to_period("Q"))
        .last()
    )
    return pd.DatetimeIndex(quarter_end_trading_days.values)

def rebalance_dates_for_frequency(prices: pd.DataFrame, frequency: str) -> pd.DatetimeIndex:
    f = frequency.lower().strip()
    if f == "monthly":
        return monthly_rebalance_dates(prices)
    if f == "quarterly":
        return quarterly_rebalance_dates(prices)
    raise ValueError(f"frequency must be 'monthly' or 'quarterly', got {frequency!r}")

def _hold_spy_fallback(pos: pd.DataFrame, d, columns: pd.Index) -> None:
    """100% SPY when no momentum sleeve qualifies; cash if SPY not in universe."""
    if "SPY" in columns:
        pos.loc[d, :] = 0.0
        pos.loc[d, "SPY"] = 1.0
    else:
        pos.loc[d, :] = 0.0

def compute_positions(
    signal: pd.DataFrame,
    rebalance_dates,
    top_n: int,
    *,
    weight_by_momentum: bool = True,
    absolute_momentum: bool = True,
    defensive_benchmark: str | None = None,
    exclude_from_ranking: frozenset[str] | None = None,
) -> pd.DataFrame:
    """
    Optional SPY defensive cash; positive-momentum filter; top N by momentum.
    Weights: momentum strength or equal. If no names qualify, hold 100% SPY.
    exclude_from_ranking: tickers omitted from momentum sleeve (e.g. SPY when using S&P 500 stocks).
    """
    pos = pd.DataFrame(np.nan, index=signal.index, columns=signal.columns)
    spy_in = defensive_benchmark and defensive_benchmark in signal.columns
    cols = signal.columns
    excl = exclude_from_ranking or frozenset()

    for d in rebalance_dates:
        if d not in signal.index:
            continue
        row = signal.loc[d]
        scores = row.dropna()

        if spy_in:
            spy_m = scores.get(defensive_benchmark)
            if spy_m is None or not np.isfinite(spy_m) or spy_m <= 0:
                pos.loc[d, :] = 0.0
                continue

        if excl:
            drop_ix = [x for x in excl if x in scores.index]
            if drop_ix:
                scores = scores.drop(index=drop_ix)

        if absolute_momentum:
            scores = scores[scores > 0]
        if scores.empty:
            _hold_spy_fallback(pos, d, cols)
            continue

        scores = scores.sort_values(ascending=False).head(top_n)
        picks = scores.index.tolist()
        if not picks:
            _hold_spy_fallback(pos, d, cols)
            continue

        pos.loc[d, :] = 0.0
        if weight_by_momentum:
            s = scores.loc[picks].astype(float)
            s_pos = s.clip(lower=0.0)
            total = float(s_pos.sum())
            if total <= 0:
                _hold_spy_fallback(pos, d, cols)
                continue
            for t in picks:
                pos.loc[d, t] = float(s_pos.loc[t]) / total
        else:
            w = 1.0 / len(picks)
            pos.loc[d, picks] = w

    pos = pos.ffill().fillna(0.0)
    return pos

def backtest_long_only(
    prices: pd.DataFrame,
    signal: pd.DataFrame,
    top_n: int = 5,
    cost_bps: float = 10.0,
    *,
    rebalance_frequency: str = "quarterly",
    weight_by_momentum: bool = True,
    absolute_momentum: bool = True,
    defensive_benchmark: str | None = None,
    exclude_from_ranking: frozenset[str] | None = None,
) -> pd.DataFrame:
    rets = prices.pct_change().fillna(0.0)
    rebal_dates = rebalance_dates_for_frequency(prices, rebalance_frequency)
    pos = compute_positions(
        signal,
        rebal_dates,
        top_n,
        weight_by_momentum=weight_by_momentum,
        absolute_momentum=absolute_momentum,
        defensive_benchmark=defensive_benchmark,
        exclude_from_ranking=exclude_from_ranking,
    )

    turnover = pos.diff().abs().sum(axis=1)
    cost = turnover * (cost_bps / 1e4)
    port_ret = (pos.shift(1) * rets).sum(axis=1) - cost
    equity = (1 + port_ret).cumprod()

    return pd.DataFrame({
        "portfolio_return": port_ret,
        "equity": equity,
        "turnover": turnover,
        "cost": cost,
    })
