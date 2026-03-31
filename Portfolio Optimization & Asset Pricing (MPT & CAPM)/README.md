# Project 01: Portfolio Optimization & Asset Pricing (MPT & CAPM)

**Author:** Drew Glover

**Date:** March 31, 2026

---

## 1. Project Overview

This project implements two foundational models in quantitative finance: **Modern Portfolio Theory (MPT)** and the **Capital Asset Pricing Model (CAPM)**.

It addresses two core problems:

* **Portfolio Construction (MPT):** How to allocate capital across assets to maximize return for a given level of risk (diversification).
* **Asset Pricing (CAPM):** How to estimate the expected return of an asset based on its exposure to market risk.

The notebook walks through the full workflow: data collection, processing, modeling, optimization, and visualization.

---

## 2. Concepts and Skills

* **Financial Models:** MPT, Efficient Frontier, CAPM, Security Market Line (SML)
* **Statistics:** Mean return, volatility, variance, covariance, correlation, beta, Jensen’s alpha
* **Methods:** Monte Carlo simulation, numerical optimization (`scipy.optimize`)
* **Python Tools:** `pandas`, `numpy`, `yfinance`, `matplotlib`, `scipy`
* **Design:** Object-oriented programming with a reusable `PortfolioOptimizer` class

---

## 3. Mathematical Framework

### A. Core Definitions

**Log Return**
`R_t = ln(P_t / P_(t-1))`

**Expected Return**
`E(R_i) = (1 / N) * Σ R_(i,t)`

**Variance**
`σ_i^2 = (1 / (N - 1)) * Σ (R_(i,t) - μ_i)^2`

**Covariance**
`Cov(R_i, R_j) = (1 / (N - 1)) * Σ (R_(i,t) - μ_i)(R_(j,t) - μ_j)`

---

### B. Modern Portfolio Theory (MPT)

**Portfolio Return**
`E(R_p) = Σ w_i * E(R_i)`

**Portfolio Variance**
`σ_p^2 = w^T Σ w`

**Sharpe Ratio**
`Sharpe = (E(R_p) - R_f) / σ_p`

---

### C. Capital Asset Pricing Model (CAPM)

**Beta**
`β_i = Cov(R_i, R_m) / σ_m^2`

**Expected Return (CAPM)**
`E(R_i) = R_f + β_i * (E(R_m) - R_f)`

**Jensen’s Alpha**
`α_i = R_actual - [R_f + β_i * (E(R_m) - R_f)]`

---

## 4. Running the Project

1. Clone the repository:

```bash
git clone https://github.com/jvskillup/quant-finance-projects.git
```

2. Open `01_Portfolio_Optimization_OOP.ipynb` in Jupyter or Google Colab

3. Run all cells to reproduce the full analysis

---

## 5. Code Structure

The project is organized around a `PortfolioOptimizer` class:

* **Initialization:** Inputs include asset list, benchmark, date range, and risk-free rate
* **Helper Methods:** Handle data processing (`_download_data`, `_calculate_returns`, etc.)
* **Core Methods:**

  * `run_mpt_simulation()` → generates random portfolios
  * `find_optimal_portfolio()` → maximizes Sharpe ratio
  * `plot_efficient_frontier()` → visualizes results
  * `analyze_and_plot_capm()` → computes CAPM metrics and plots SML

---

## 6. Results and Insights

* **MPT Results:**
  Using 2018–2023 data, the optimal portfolio weights were:
  **[Insert weights here]**
  with a Sharpe ratio of approximately **[Insert value]**.
  The Efficient Frontier illustrates the tradeoff between risk and return.

* **CAPM Results:**
  `AMD` showed strong outperformance with a Jensen’s Alpha of **+32.32%**, exceeding expectations given its beta (1.61).
  The Security Market Line highlights relative performance across assets.

---

## 7. Key Takeaways

This project demonstrates how classic financial models can be implemented in practice. It also highlights a major limitation: both MPT and CAPM depend on historical data, which may not accurately predict future performance.

In practice, these models are often used as a baseline, with more advanced methods applied for forecasting and optimization.
