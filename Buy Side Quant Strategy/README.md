# Quantitative Momentum Strategy & Backtesting Pipeline
### By: Drew Glover

An automated quantitative research suite built to simulate Dual Momentum strategies. This pipeline handles everything from live data ingestion via Yahoo Finance to rigorous data cleaning and performance analytics.

---

## Quick Start

1. Install Dependencies:
   pip install pandas yfinance tqdm matplotlib pyarrow fastparquet

2. Run Default Backtest (S&P 500, Quarterly Rebalancing, 10-Year History):
   python run_pipeline.py

3. Check Results:
   View the generated equity curves and CSV reports in the /outputs folder.

---

## The Investment Strategy

This pipeline implements a Dual Momentum framework, which combines Relative Momentum (buying what is strongest) and Absolute Momentum (ensuring the asset is in an uptrend).

1. Data Selection & Cleaning (The Universe)
- Default Universe: The S&P 500 (individual stocks).
- Quality Gate: Every ticker must pass a Quality Control check. The pipeline automatically rejects stocks with too much missing data, zero-volume days, or bad prints (where High < Low).

2. Signal Generation (The Lookback)
- Momentum Window: The system calculates the total return over the last 126 trading days (approx. 6 months).
- Ranking: All stocks are ranked. Only the top N (default: 5) are eligible for purchase.

3. Execution Logic
- Rebalancing: The portfolio is updated Monthly or Quarterly. This reduces churn and helps avoid chasing daily noise.
- Position Sizing:
    - Momentum Weighted: Assets with higher momentum scores get a larger share of the capital.
    - Equal Weighted: Every selected asset gets an equal cash allocation.
- Absolute Momentum Filter: If a top-ranked stock has a negative return over the lookback period, it is excluded from the portfolio.

4. Risk Management (Defensive Switch)
- Market Trend Filter: If --defensive-spy is enabled, the pipeline checks the trend of the broader market (SPY). If SPY's momentum is negative, the strategy exits all positions and moves to cash to protect against market crashes.

---

## Configuration & Flags

| Flag | Default | Description |
| :--- | :--- | :--- |
| --universe | sp500 | Target sp500 (500+ stocks) or etfs (8-10 major asset classes). |
| --top-n | 5 | How many winners to hold at once. |
| --lookback | 126 | Momentum window in trading days. |
| --rebalance | quarterly | Trade frequency: monthly or quarterly. |
| --defensive-spy | False | Moves to cash if the S&P 500 trend is negative. |
| --cost-bps | 10.0 | Transaction costs in basis points (0.1% per trade). |

Example Commands

Rotation between Asset Classes (ETFs):
python run_pipeline.py --universe etfs --top-n 3

Aggressive Stock Picking (Monthly):
python run_pipeline.py --universe sp500 --top-n 10 --rebalance monthly

---

## Analytics
The pipeline provides performance metrics and analytics for every run:
* CAGR: Compound Annual Growth Rate.
* Sharpe Ratio: Risk-adjusted return performance.
* Max Drawdown: The largest peak-to-trough decline.
* Turnover: Measures how frequently the portfolio is trading.

---

## Repository Map
- run_pipeline.py: The orchestrator for the entire workflow.
- src/: Modular logic for data I/O, cleaning, features, and backtesting.
- outputs/: Final performance reports and visualization plots.
