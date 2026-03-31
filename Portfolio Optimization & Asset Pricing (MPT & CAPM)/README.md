# Project 01: Portfolio Optimization & Asset Pricing (MPT & CAPM)

**Author:** Drew Glover
**Date:** March 31, 2026

---

## 1. Project Overview

This project delivers a full implementation of two cornerstone models in quantitative finance: **Modern Portfolio Theory (MPT)** and the **Capital Asset Pricing Model (CAPM)**.

It focuses on addressing two key challenges in portfolio management:

* **Portfolio Construction (MPT):** Determining how to allocate capital across multiple risky assets in a way that maximizes expected return for a chosen level of risk. This is fundamentally a problem of **diversification**.
* **Asset Valuation (CAPM):** Estimating the appropriate expected return of an individual asset based on its exposure to overall market risk. This forms the basis of **risk pricing**.

The notebook walks through the entire pipeline, including data collection, transformation, model implementation, optimization, and visualization of results.

---

## 2. Concepts and Technical Skills

This project demonstrates both financial theory and practical implementation:

* **Financial Theory:** Efficient Frontier, Modern Portfolio Theory, CAPM, Security Market Line (SML)
* **Statistical Tools:** Mean return, volatility, variance, covariance, correlation, beta, Jensen’s alpha
* **Computational Methods:** Monte Carlo simulation for portfolio generation, optimization via `scipy.optimize`
* **Python Stack:**

  * `pandas` for time series handling
  * `numpy` for numerical operations
  * `yfinance` for market data retrieval
  * `matplotlib` for plotting
  * `scipy` for optimization and regression
* **Software Design:** Object-oriented structure using a reusable `PortfolioOptimizer` class

---

## 3. Mathematical Framework

### A. Core Definitions

**Log Returns**
Used to convert price series into a more stable return series:
$$
R_t = \ln\left(\frac{P_t}{P_{t-1}}\right)
$$

**Expected Return**
$$
E(R_i) = \frac{1}{N} \sum_{t=1}^{N} R_{i,t}
$$

**Variance**
$$
\sigma_i^2 = \frac{1}{N-1} \sum_{t=1}^{N} (R_{i,t} - \mu_i)^2
$$

**Covariance**
$$
\text{Cov}(R_i, R_j) = \frac{1}{N-1} \sum (R_{i,t} - \mu_i)(R_{j,t} - \mu_j)
$$

---

### B. Modern Portfolio Theory

**Portfolio Return**
$$
E(R_p) = \sum w_i E(R_i)
$$

**Portfolio Variance**
$$
\sigma_p^2 = \mathbf{w}^T \mathbf{\Sigma} \mathbf{w}
$$

**Sharpe Ratio**
$$
\text{Sharpe} = \frac{E(R_p) - R_f}{\sigma_p}
$$

---

### C. CAPM

**Beta**
$$
\beta_i = \frac{\text{Cov}(R_i, R_m)}{\sigma_m^2}
$$

**Expected Return (CAPM)**
$$
E(R_i) = R_f + \beta_i (E(R_m) - R_f)
$$

**Jensen’s Alpha**
$$
\alpha_i = R_{actual} - E(R_i)
$$

---

## 4. Running the Project

1. Clone the repository:

```bash
git clone https://github.com/jvskillup/quant-finance-projects.git
```

2. Open the notebook `01_Portfolio_Optimization_OOP.ipynb` using Jupyter or Google Colab

3. Execute all cells (`Runtime → Run all`) to reproduce the full analysis

---

## 5. Code Structure

The implementation is organized into a single class: `PortfolioOptimizer`.

* **Initialization:** Accepts asset list, market benchmark, date range, and risk-free rate
* **Helper Methods:** Handle data ingestion and preprocessing (`_download_data`, `_calculate_returns`, etc.)
* **Main Methods:**

  * `run_mpt_simulation()` → generates random portfolios
  * `find_optimal_portfolio()` → identifies the maximum Sharpe ratio portfolio
  * `plot_efficient_frontier()` → visualizes risk-return tradeoffs
  * `analyze_and_plot_capm()` → computes CAPM metrics and plots SML

---

## 6. Results and Insights

* **MPT Findings:**
  Using historical data (2018–2023), the optimized portfolio achieved the highest risk-adjusted return with weights approximately:
  **[Insert weights here]**
  The corresponding Sharpe ratio was around **[Insert value]**, and the Efficient Frontier illustrates the tradeoff between risk and return.

* **CAPM Findings:**
  The analysis shows that `AMD` significantly outperformed expectations, producing a Jensen’s Alpha of **+32.32%**. Despite its high beta (1.61), actual returns exceeded model predictions. The SML visualization highlights which assets over- and under-performed.

---

## 7. Key Takeaways

This project highlights how classical financial models can be implemented in practice. At the same time, it underscores an important limitation: both MPT and CAPM rely heavily on historical data as a proxy for future expectations.

In real-world quantitative finance, these models often serve as a starting point, with more advanced techniques used to improve forecasting and decision-making.
