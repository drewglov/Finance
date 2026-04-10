"""
_1_io.py
Data ingestion layer — fetches live OHLCV data from Yahoo Finance via yfinance.
No local CSV/TXT files required.
"""

from __future__ import annotations

from typing import List
import pandas as pd
import yfinance as yf


def _yahoo_symbol(sym: str) -> str:
    """Wikipedia / CSV often use BRK.B; Yahoo Finance uses BRK-B."""
    return str(sym).strip().replace(".", "-")


def fetch_sp500_ticker_list() -> List[str]:
    """
    Current S&P 500 constituents (tickers as used by Yahoo Finance).
    Tries a public CSV first, then Wikipedia HTML.
    """
    csv_urls = (
        "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv",
        "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv",
    )
    last_err: Exception | None = None
    for url in csv_urls:
        try:
            df = pd.read_csv(url)
            col = next((c for c in df.columns if str(c).lower() == "symbol"), df.columns[0])
            syms = df[col].dropna().astype(str).str.strip()
            tickers = sorted({_yahoo_symbol(s) for s in syms if s})
            if len(tickers) < 400:
                raise ValueError(f"unexpected ticker count {len(tickers)}")
            return tickers
        except Exception as exc:
            last_err = exc

    try:
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        tables = pd.read_html(url, header=0)
        df = tables[0]
        syms = df["Symbol"].dropna().astype(str).str.strip()
        tickers = sorted({_yahoo_symbol(s) for s in syms if s})
        if len(tickers) < 400:
            raise ValueError(f"unexpected ticker count {len(tickers)}")
        return tickers
    except Exception as exc:
        raise RuntimeError(
            "Could not load S&P 500 constituents (network or pandas.read_html). "
            f"Last CSV error: {last_err!r}; wiki error: {exc!r}"
        ) from exc

# ── Default ETF universe ─────────────────────────────────────────────────────
# Edit this list or pass your own to fetch_ohlcv_bulk().
# US equity only — comparable to SPY as benchmark (no intl / sectors / REITs in default sleeve).
DEFAULT_ETFS: List[str] = [
    # Core US large / total market
    "SPY", "IVV", "VOO", "VTI", "SCHX",
    # Price-weighted / style breadth
    "DIA", "IWM",
    # Growth & tech-heavy (vs SPY tilt)
    "QQQ", "QQQM", "SPYG", "VOOG", "SCHG", "VUG", "IWF",
]

REQUIRED_COLS = ["Open", "High", "Low", "Close", "Volume"]


def fetch_one_ohlcv(
    ticker: str,
    period: str = "max",
    interval: str = "1d",
) -> pd.DataFrame:
    """
    Download OHLCV history for a single ticker from Yahoo Finance.

    Parameters
    ----------
    ticker   : Yahoo Finance ticker symbol, e.g. "SPY"
    period   : yfinance period string — "max", "10y", "5y", "2y", "1y", etc.
    interval : bar size — "1d" (daily) recommended for backtesting

    Returns
    -------
    DataFrame with DatetimeIndex and columns: Open, High, Low, Close, Volume
    Raises ValueError if the download fails or returns no data.
    """
    raw = yf.download(
        ticker,
        period=period,
        interval=interval,
        auto_adjust=True,   # adjusts for splits & dividends
        progress=False,
    )

    if raw.empty:
        raise ValueError(f"{ticker}: yfinance returned no data")

    # yfinance may return MultiIndex columns when downloading a single ticker
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)

    missing = [c for c in REQUIRED_COLS if c not in raw.columns]
    if missing:
        raise ValueError(f"{ticker}: missing columns {missing}")

    df = raw[REQUIRED_COLS].copy()

    # coerce types & drop any bad rows
    for c in REQUIRED_COLS:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=REQUIRED_COLS)

    df.index = pd.to_datetime(df.index)
    df.index.name = "Date"
    df = df.sort_index()

    return df


def fetch_ohlcv_bulk(
    tickers: List[str] | None = None,
    period: str = "max",
    interval: str = "1d",
) -> dict[str, pd.DataFrame]:
    """
    Fetch OHLCV data for a list of tickers.

    Parameters
    ----------
    tickers  : list of ticker symbols; defaults to DEFAULT_ETFS
    period   : passed through to fetch_one_ohlcv
    interval : passed through to fetch_one_ohlcv

    Returns
    -------
    dict mapping ticker -> DataFrame (only successful downloads included)
    """
    if tickers is None:
        tickers = DEFAULT_ETFS

    results: dict[str, pd.DataFrame] = {}
    for tkr in tickers:
        try:
            results[tkr] = fetch_one_ohlcv(tkr, period=period, interval=interval)
        except Exception:
            pass   # caller (curate step) handles errors via QC rows

    return results
