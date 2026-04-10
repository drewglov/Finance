"""
run_pipeline.py
Momentum backtest pipeline — data fetched live from Yahoo Finance.

Usage:
    python run_pipeline.py [options]

Options:
    --universe   STR    etfs (default) or sp500 — S&P 500 single names vs ETF sleeve
    --top-n      INT    Names to hold per rebalance (default: 5)
    --rebalance  STR    monthly or quarterly (default: quarterly)
    --cost-bps   FLOAT  One-way transaction cost in bps           (default: 10)
    --min-rows   INT    Min trading days required to enter universe (default: 750)
    --max-zero-vol-frac FLOAT  Max allowed zero-volume row fraction (default: 0.01)
    --max-bad-bar-frac  FLOAT  Max allowed bad high/low row fraction (default: 0.005)
    --max-nonpos-frac   FLOAT  Max allowed non-positive price row fraction (default: 0.0)
    --lookback   INT    Momentum lookback in days (default: 126 ≈ 6 months)
    --equal-weight       Use equal weights among top-N (default: weight by momentum)
    --no-absolute-momentum  Do not require positive momentum per name
    --defensive-spy        Go to cash when SPY momentum <= 0 (off by default)
    --period     STR    yfinance history period: max/10y/5y/2y/1y  (default: 10y)
    --tickers    STR    Space-separated list of tickers (overrides --universe)

Output files (written to outputs/):
    qc_summary.csv       — quality check results per ticker
    universe.csv         — tickers that passed QC filters
    backtest_results.csv — strategy + SPY benchmark daily returns/equity, turnover, cost
    equity_vs_spy.png    — equity curve chart: strategy vs SPY buy-and-hold
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

# ── make sure the repo root is on sys.path so `src.*` imports work ──────────
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src._1_io import fetch_ohlcv_bulk, fetch_one_ohlcv, DEFAULT_ETFS, fetch_sp500_ticker_list
from src._2_quality import qc_metrics
from src._4_universe import build_universe
from src._5_features import momentum_rolling
from src._6_backtest import backtest_long_only
from src._7_analytics import performance_metrics

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(it, **kwargs):
        return it


# ────────────────────────────────────────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Momentum backtest (ETFs or S&P 500 stocks)")
    p.add_argument(
        "--universe",
        type=str,
        default="sp500",
        choices=("etfs", "sp500"),
        help="etfs or sp500 (default: sp500)",
    )
    p.add_argument("--top-n",    type=int,   default=5,     help="Names to hold per rebalance")
    p.add_argument(
        "--rebalance",
        type=str,
        default="quarterly",
        choices=("monthly", "quarterly"),
        help="Rebalance schedule",
    )
    p.add_argument("--cost-bps", type=float, default=10.0,  help="One-way transaction cost in bps")
    p.add_argument("--min-rows", type=int,   default=750,   help="Min trading days to enter universe")
    p.add_argument("--max-zero-vol-frac", type=float, default=0.01, help="Max allowed zero-volume row fraction")
    p.add_argument("--max-bad-bar-frac", type=float, default=0.005, help="Max allowed bad high/low row fraction")
    p.add_argument("--max-nonpos-frac", type=float, default=0.0, help="Max allowed non-positive price row fraction")
    p.add_argument("--lookback", type=int,   default=126,   help="Momentum lookback in trading days (~126 = 6 months)")
    p.add_argument("--period",   type=str,   default="10y", help="yfinance history period (max/10y/5y/2y/1y)")
    p.add_argument("--tickers",  type=str,   nargs="+",     help="Override default ETF list")
    p.add_argument("--equal-weight", action="store_true", help="Equal top-N weights; default is momentum-weighted")
    p.add_argument("--no-absolute-momentum", action="store_true", help="Allow negative-momentum names in top-N")
    p.add_argument("--defensive-spy", action="store_true", help="Cash when SPY momentum <= 0 (optional)")
    return p.parse_args()


# ────────────────────────────────────────────────────────────────────────────
def step1_fetch_and_curate(
    tickers: list[str],
    period: str,
    curated_dir: Path,
    outputs_dir: Path,
) -> Path:
    """Fetch live OHLCV data from Yahoo Finance, run QC, save curated parquets."""
    print("\n── Step 1 / 4 : Fetch & Curate ──────────────────────────────────")
    curated_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir.mkdir(parents=True, exist_ok=True)

    print(f"  Fetching {len(tickers)} tickers from Yahoo Finance (period={period}) …")
    data = fetch_ohlcv_bulk(tickers, period=period)
    print(f"  Successfully downloaded: {len(data)} / {len(tickers)}")

    qc_rows = []
    for ticker in tqdm(tickers, desc="  curate"):
        if ticker not in data:
            qc_rows.append({"ticker": ticker, "error": "download failed"})
            continue
        try:
            df = data[ticker]
            qc = qc_metrics(df)
            qc["ticker"] = ticker
            df.to_parquet(curated_dir / f"{ticker}.parquet", index=True)
            qc_rows.append(qc)
        except Exception as exc:
            qc_rows.append({"ticker": ticker, "error": str(exc)})

    qc_df = pd.DataFrame(qc_rows)
    preferred = ["ticker", "rows", "start_date", "end_date",
                 "nonpos_price_rows", "bad_high_rows", "bad_low_rows",
                 "zero_volume_rows", "error"]
    cols = [c for c in preferred if c in qc_df.columns] + \
           [c for c in qc_df.columns if c not in preferred]
    qc_df = qc_df[cols].sort_values("ticker")

    qc_out = outputs_dir / "qc_summary.csv"
    qc_df.to_csv(qc_out, index=False)
    print(f"  QC summary → {qc_out}")
    return qc_out


def step2_universe(
    qc_csv: Path,
    outputs_dir: Path,
    min_rows: int,
    max_zero_vol_frac: float,
    max_bad_bar_frac: float,
    max_nonpos_frac: float,
) -> Path:
    """Filter QC summary to investable universe."""
    print("\n── Step 2 / 4 : Universe ────────────────────────────────────────")
    universe = build_universe(
        qc_csv,
        min_rows=min_rows,
        max_zero_vol_frac=max_zero_vol_frac,
        max_bad_bar_frac=max_bad_bar_frac,
        max_nonpos_price_frac=max_nonpos_frac,
    )
    print(f"  Universe size: {len(universe)} tickers")

    uni_out = outputs_dir / "universe.csv"
    universe[["ticker"]].to_csv(uni_out, index=False)
    print(f"  Universe CSV → {uni_out}")
    return uni_out


def step3_features(
    universe_csv: Path,
    curated_dir: Path,
    lookback: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Build aligned price panel and compute momentum signal."""
    print("\n── Step 3 / 4 : Features ────────────────────────────────────────")

    uni = pd.read_csv(universe_csv)
    series = {}
    for tkr in uni["ticker"]:
        fp = curated_dir / f"{tkr}.parquet"
        df = pd.read_parquet(fp)
        series[tkr] = df["Close"]

    prices = pd.DataFrame(series).sort_index()
    print(f"  Price panel  : {prices.shape[0]} days × {prices.shape[1]} tickers")

    signal = momentum_rolling(prices, lookback=lookback)
    print(f"  Signal shape : {signal.shape} (rolling return over {lookback} days)")
    return prices, signal


def step4_backtest(
    prices: pd.DataFrame,
    signal: pd.DataFrame,
    outputs_dir: Path,
    top_n: int,
    cost_bps: float,
    period: str,
    *,
    weight_by_momentum: bool,
    absolute_momentum: bool,
    defensive_benchmark: str | None,
    rebalance_frequency: str,
    exclude_from_ranking: frozenset[str] | None,
) -> None:
    """Run backtest and print performance metrics."""
    print("\n── Step 4 / 4 : Backtest & Analytics ───────────────────────────")
    def_bench = defensive_benchmark
    if def_bench and def_bench not in prices.columns:
        print(f"  Warning: {def_bench} not in price panel; defensive rule disabled.")
        def_bench = None
    print(
        f"  Rules: momentum-weighted={weight_by_momentum}, "
        f"positive-momentum filter={absolute_momentum}, "
        f"SPY defensive (cash if SPY mom<=0)={def_bench is not None}, "
        f"rebalance={rebalance_frequency}"
    )
    if exclude_from_ranking:
        print(f"  Excluded from momentum sleeve: {sorted(exclude_from_ranking)}")
    universe_size = prices.shape[1]
    effective_top_n = min(top_n, universe_size)
    if effective_top_n < top_n:
        print(f"  Warning: top_n={top_n} but universe has only {universe_size} tickers; using top_n={effective_top_n}.")
    results = backtest_long_only(
        prices,
        signal,
        top_n=effective_top_n,
        cost_bps=cost_bps,
        rebalance_frequency=rebalance_frequency,
        weight_by_momentum=weight_by_momentum,
        absolute_momentum=absolute_momentum,
        defensive_benchmark=def_bench,
        exclude_from_ranking=exclude_from_ranking,
    )

    # Build SPY benchmark aligned to strategy backtest dates.
    if "SPY" in prices.columns:
        spy_close = prices["SPY"].copy()
    else:
        spy_close = fetch_one_ohlcv("SPY", period=period)["Close"]

    spy_close = spy_close.reindex(results.index).ffill()
    spy_ret = spy_close.pct_change().fillna(0.0)
    spy_equity = (1 + spy_ret).cumprod()

    results["benchmark_return_spy"] = spy_ret
    results["benchmark_equity_spy"] = spy_equity

    results_out = outputs_dir / "backtest_results.csv"
    results.to_csv(results_out)
    print(f"  Backtest results → {results_out}")

    chart_out = outputs_dir / "equity_vs_spy.png"
    try:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(11, 6))
        ax.plot(results.index, results["equity"], label="Strategy", linewidth=2.0)
        ax.plot(
            results.index,
            results["benchmark_equity_spy"],
            label="SPY buy & hold",
            linewidth=2.0,
            alpha=0.9,
        )
        ax.set_title("Equity Curve: Strategy vs SPY Buy-and-Hold")
        ax.set_xlabel("Date")
        ax.set_ylabel("Growth of $1")
        ax.grid(True, alpha=0.25)
        ax.legend()
        fig.tight_layout()
        fig.savefig(chart_out, dpi=150)
        plt.close(fig)
        print(f"  Comparison chart → {chart_out}")
    except ImportError:
        print("  Skipped chart output (matplotlib is not installed).")

    metrics = performance_metrics(results["portfolio_return"])
    benchmark_metrics = performance_metrics(results["benchmark_return_spy"])
    print("\n  ── Performance ──────────────────────────────────────────────")
    for k, v in metrics.items():
        if k in ("CAGR", "Volatility", "MaxDrawdown", "TotalReturn"):
            print(f"  {k:<18}: {v:>8.2%}")
        else:
            print(f"  {k:<18}: {v:>8.4f}")

    print("\n  ── SPY Buy-and-Hold ────────────────────────────────────────")
    for k, v in benchmark_metrics.items():
        if k in ("CAGR", "Volatility", "MaxDrawdown", "TotalReturn"):
            print(f"  {k:<18}: {v:>8.2%}")
        else:
            print(f"  {k:<18}: {v:>8.4f}")


# ────────────────────────────────────────────────────────────────────────────
def main() -> None:
    args = parse_args()

    if args.tickers:
        tickers = list(args.tickers)
        curated_dir = Path("data/curated/custom")
    elif args.universe == "sp500":
        print("  Loading S&P 500 constituent list …")
        tickers = fetch_sp500_ticker_list()
        if "SPY" not in tickers:
            tickers = ["SPY"] + tickers
        curated_dir = Path("data/curated/SP500")
    else:
        tickers = list(DEFAULT_ETFS)
        curated_dir = Path("data/curated/ETFs")

    outputs_dir = Path("outputs")

    qc_csv       = step1_fetch_and_curate(tickers, args.period, curated_dir, outputs_dir)
    universe_csv = step2_universe(
        qc_csv,
        outputs_dir,
        min_rows=args.min_rows,
        max_zero_vol_frac=args.max_zero_vol_frac,
        max_bad_bar_frac=args.max_bad_bar_frac,
        max_nonpos_frac=args.max_nonpos_frac,
    )
    prices, signal = step3_features(universe_csv, curated_dir, lookback=args.lookback)
    defensive = "SPY" if args.defensive_spy else None
    exclude_rank = (
        frozenset({"SPY"}) if (args.universe == "sp500" and not args.tickers) else None
    )
    step4_backtest(
        prices,
        signal,
        outputs_dir,
        top_n=args.top_n,
        cost_bps=args.cost_bps,
        period=args.period,
        weight_by_momentum=not args.equal_weight,
        absolute_momentum=not args.no_absolute_momentum,
        defensive_benchmark=defensive,
        rebalance_frequency=args.rebalance,
        exclude_from_ranking=exclude_rank,
    )

    print("\n✓ Pipeline complete.\n")


if __name__ == "__main__":
    main()
