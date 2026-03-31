# Project 01: Portfolio Optimization & Asset Pricing (MPT & CAPM)

**Author:** Jitesh Vegad

**Date Created:** August 17, 2025

---

### **1. Overview & Problem Statement**

This project provides a comprehensive, end-to-end implementation of two foundational models of modern finance: Modern Portfolio Theory (MPT) and the Capital Asset Pricing Model (CAPM).

The objective is to solve two fundamental problems faced by any portfolio manager:
*   **The Allocation Problem (MPT):** How do we systematically allocate capital across a set of risky assets to construct a portfolio that offers the highest possible expected return for a given level of risk? This is the science of **diversification**.
*   **The Asset Pricing Problem (CAPM):** How do we determine a theoretical "fair" expected return for an individual stock based on its non-diversifiable market risk? This is the theory of **pricing risk**.

This notebook provides the complete workflow, from data acquisition and preprocessing to model implementation, numerical optimization, and final visualization.

### **2. Key Concepts & Skills Demonstrated**

*   **Financial Modeling:** Modern Portfolio Theory, The Efficient Frontier, The Capital Asset Pricing Model (CAPM), The Security Market Line (SML).
*   **Statistical Analysis:** Expected Return (Mean), Volatility (Standard Deviation), Variance, Covariance, Correlation, Beta, Jensen's Alpha.
*   **Numerical Methods:** Monte Carlo Simulation (for generating the Efficient Frontier), Numerical Optimization (using `scipy.optimize` to find the Optimal Portfolio).
*   **Python for Data Science:** `pandas` for time-series manipulation, `numpy` for numerical and matrix computation, `yfinance` for data acquisition, `matplotlib` for visualization, `scipy` for statistical regression and optimization.
*   **Object-Oriented Programming (OOP):** The entire logic is professionally refactored into a clean, reusable `PortfolioOptimizer` class.

---

### 3. The Mathematical Foundations

This section details the core mathematical formulas that power the analysis.

#### A. Foundational Formulas

**1. Logarithmic Return:** Used to transform non-stationary price series into stationary return series.
$$

R_t = \ln\left(\frac{P_t}{P_{t-1}}\right)

$$
Where:
*   $R_t$ is the log return at time $t$.
*   $P_t$ is the price at time $t$.

**2. Expected Return (Mean):** The average return of a single asset.
$$

E(R_i) = \mu_i = \frac{1}{N} \sum_{t=1}^{N} R_{i,t}

$$
This is annualized by multiplying by the number of trading days.

**3. Variance:** A measure of a single asset's risk (volatility squared).
$$
\sigma_i^2 = \frac{1}{N-1} \sum_{t=1}^{N} (R_{i,t} - \mu_i)^2
$$

**4. Covariance:** A measure of how two assets move in relation to each other.
$$
\text{Cov}(R_i, R_j) = \sigma_{ij} = \frac{1}{N-1} \sum_{t=1}^{N} (R_{i,t} - \mu_i)(R_{j,t} - \mu_j)
$$

#### B. Modern Portfolio Theory (MPT) Formulas

**1. Portfolio Expected Return:** The weighted average of the individual asset returns.
$$
E(R_p) = \sum_{i=1}^{n} w_i E(R_i)
$$
In matrix notation:
$$
E(R_p) = \mathbf{w}^T \mathbf{\mu}
$$
Where:
*   $w_i$ is the weight of asset $i$ in the portfolio.
*   $\mathbf{w}^T$ is the transposed vector of weights.
*   $\mathbf{\mu}$ is the vector of expected returns.

**2. Portfolio Variance:** The risk of the overall portfolio. This formula is the heart of diversification.
$$
\sigma_p^2 = \mathbf{w}^T \mathbf{\Sigma} \mathbf{w}
$$
Where:
*   $\mathbf{\Sigma}$ is the covariance matrix of the assets.

**3. Sharpe Ratio:** The primary metric for risk-adjusted return.
$$
\text{Sharpe Ratio} = \frac{E(R_p) - R_f}{\sigma_p}
$$
Where:
*   $R_f$ is the risk-free rate.
*   $\sigma_p$ is the portfolio's standard deviation (volatility).

#### C. Capital Asset Pricing Model (CAPM) Formulas

**1. Beta ($\beta$):** The measure of an asset's systematic (non-diversifiable) risk.
$$
\beta_i = \frac{\text{Cov}(R_i, R_m)}{\sigma_m^2}
$$
Where:
*   $R_m$ is the return of the overall market.
*   $\sigma_m^2$ is the variance of the market's returns.

**2. The CAPM Formula:** Defines the theoretical expected return for an asset.
$$
E(R_i) = R_f + \beta_i (E(R_m) - R_f)
$$

**3. Jensen's Alpha ($\alpha$):** Measures the historical performance of an asset relative to the return predicted by the CAPM.
$$
\alpha_i = R_{i, \text{actual}} - [R_f + \beta_i (E(R_m) - R_f)]
$$
---

### **4. How to Use This Notebook**

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/jvskillup/quant-finance-projects.git
    ```
2.  **Open the Notebook:** Open the `01_Portfolio_Optimization_OOP.ipynb` file in Google Colab or a local Jupyter Lab environment.
3.  **Run All Cells:** From the menu, select `Runtime -> Run all`. The notebook will execute the entire analysis from data download to final plots and results.

---

### **5. Project Workflow & Code Structure**

The project is structured within a reusable `PortfolioOptimizer` class.

*   **Initialization (`__init__`):** The class is initialized with a list of stocks, a market index, start/end dates, and a risk-free rate.
*   **Internal Methods (`_`):** Helper methods handle the data pipeline: `_download_data`, `_calculate_returns`, `_calculate_mpt_inputs`, and `_calculate_capm_metrics`.
*   **Public Methods:**
    *   `run_mpt_simulation()`: Runs a Monte Carlo simulation to generate thousands of random portfolios.
    *   `find_optimal_portfolio()`: Uses `scipy.optimize.minimize` to find the portfolio with the maximum Sharpe Ratio.
    *   `plot_efficient_frontier()`: Visualizes the MPT results.
    *   `analyze_and_plot_capm()`: Calculates Beta/Alpha and plots the Security Market Line (SML).

---

### **6. Results & Conclusion**

*   **MPT Results:** Based on data from 2018-2023 for the specified stocks, the optimal portfolio was found to be allocated as follows: **[List your optimal weights here, e.g., UNH: 21.56%, AMD: 67.88%, etc.]**. This portfolio offered a historical annualized Sharpe Ratio of approximately **[Your Sharpe Ratio Here, e.g., 0.63]**. The generated plot clearly visualizes the Efficient Frontier.

*   **CAPM Results:** The analysis identified `AMD` as a massive historical outperformer, with a Jensen's Alpha of **+32.32%**. This indicates its returns were far greater than what its high market risk (Beta of 1.61) would have predicted. The SML plot visually confirms which stocks outperformed (plotted above the line) and underperformed (plotted below the line).

*   **Key Learning:** The project successfully demonstrates the implementation of these foundational models. However, it also highlights their critical real-world limitation: their reliance on **historical data as a forecast for the future.** A professional quant would use these models as a baseline but spend the majority of their time developing more sophisticated methods for forecasting the input parameters.
