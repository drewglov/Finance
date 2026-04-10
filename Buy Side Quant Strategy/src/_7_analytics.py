from __future__ import annotations
import pandas as pd
import numpy as np

TRADING_DAYS = 252

def performance_metrics(port_ret: pd.Series) -> dict:
    equity = (1 + port_ret).cumprod()
    total_return = equity.iloc[-1] - 1

    cagr = equity.iloc[-1] ** (TRADING_DAYS / len(port_ret)) - 1
    vol = port_ret.std() * np.sqrt(TRADING_DAYS)
    sharpe = cagr / vol if vol > 0 else np.nan

    running_max = equity.cummax()
    drawdown = equity / running_max - 1
    max_dd = drawdown.min()

    return {
        "CAGR": cagr,
        "Volatility": vol,
        "Sharpe": sharpe,
        "MaxDrawdown": max_dd,
        "TotalReturn": total_return,
    }
