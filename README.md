# Finance Portfolio

Hello, welcome to my repository containing a portfolio of finance and algorithmic trading projects completed by me for career, academic, self-learning, and hobby purposes. These projects are presented in the form of iPython Notebooks, and have been completed using Python 3.14 along with various libraries and tools such as Pandas, Matplotlib, and the QuantConnect Lean Engine.

I am always willing to meet new people in hopes of doing business together. I can be reached via email at drewrglov@gmail.com.


## Contents

### Full Research Pipeline

##### Quantitative Momentum Strategy & Backtesting Pipeline
   • [Quantitative Momentum Strategy & Backtesting Pipeline](https://github.com/drewglov/Finance/tree/main/Buy%20Side%20Quant%20Strategy) - This project is a quantitative research pipeline that uses Yahoo Finance data to backtest momentum-based investment strategies across the S&P 500 or specific ETF universes. It automates the entire workflow from live data ingestion and quality auditing to portfolio simulation and performance reporting. It utilizes:

- **Automated Pipeline Development**: Uses Python’s argparse and pathlib for a flexible command-line interface, allowing for rapid parameter tuning and strategy iteration.
- **Data Engineering**: Features a modular ETL (Extract, Transform, Load) pipeline that performs automated data validation, cleaning, and storage using the Parquet format.
- **Quantitative Momentum Trading**: Implements "Relative Momentum" to rank assets and "Absolute Momentum" (trend following) to filter out losing positions.
- **Risk Management**: Includes a defensive market switch to move to cash during broad market downturns and accounts for realistic transaction slippage.
- **Performance Analytics**: Calculates institutional-grade metrics including CAGR, Sharpe Ratio, and Maximum Drawdown to evaluate risk-adjusted returns.


### Strategy and Optimization

##### Quantitative Portfolio Construction
   • [Quantitative Portfolio Construction](https://github.com/drewglov/Finance/tree/main/Quantitative%20Portfolio%20Construction) - This project seeks to construct portfolios using quantitative analysis/modelling techniques of technical indicators as features, rebalancing the portfolio of stocks every month. The project focuses on the following indicators:

- Garman-Klass Volatility
- RSI
- Bollinger Bands
- ATR
- MACD
- Fama-French 5 Factors
  -  Mkt-RF: Market excess return
  -  SMB (Small Minus Big): Size premium (small vs large caps)
  - HML (High Minus Low): Value premium (high vs low book-to-market)
  - RMW (Robust Minus Weak): Profitability premium (profitable vs unprofitable firms)
  - CMA (Conservative Minus Aggressive): Investment premium (low vs high asset growth)

##### Multiple Technical Indicator Trading Strategy
   • [Multiple Technical Indicator Trading Strategy](https://github.com/drewglov/Finance/blob/main/Multiple%20Technical%20Analysis%20Strategy/multiple-ta-strategy.ipynb) - In this project, I use Python to explore a specific trading strategy based on a combination of 7 of the most commonly used technical analysis indicators. I generate trading signals based on a defined set of rules, backtest the strategy, and form an optimally weighted portfolio. The goal is to outperform a standard buy-and-hold strategy of the SPY ETF over a defined period of time. I have selected 7 technical indicators to explore in this project:

- Simple Moving Average (Price)
- Simple Moving Average (Volume)
- Average True Range
- Stochastic Oscillator
- Relative Strength Index
- Moving Average Convergence/Divergence (MACD)
- Bollinger Bands

##### Crypto Portfolio Optimization
   • [Crypto Portfolio Optimization](https://github.com/drewglov/Finance/blob/main/Crypto%20Optimization/crypto-portfolio-optmization.ipynb) - A crypto portfolio optimization tool leveraging quantitative methods to balance risk and return, with a focus on mitigating market risks using custom strategies, utilizing and demonstrating:

   - Efficient Frontier
   - Expected Returns
   - Risk (Volatility)
   - Sharpe Ratio
   - Optimization functions

##### Portfolio Optimization and Asset Pricing (MPT & CAPM)
   • [Portfolio Optimization and Asset Pricing (MPT & CAPM)](https://github.com/drewglov/Finance/blob/main/Portfolio%20Optimization%20%26%20Asset%20Pricing%20(MPT%20%26%20CAPM)/Portfolio_Optimization_MPT_CAPM_OOP.ipynb) - This project tackles the two foundational questions of modern finance: how to optimally allocate capital and how to price risk. It provides a complete, end-to-end workflow for analyzing a portfolio of equities, utilizing and demonstrating:

- Modern Portfolio Theory (MPT) & The Efficient Frontier
- Capital Asset Pricing Model (CAPM) & The Security Market Line (SML)
- Monte Carlo Simulation for generating portfolio possibilities
- Numerical Optimization (SciPy) for finding the max Sharpe Ratio portfolio
- Statistical Analysis (Beta, Jensen's Alpha, Covariance)
- Object-Oriented Programming: The entire analysis is encapsulated in a professional PortfolioOptimizer class.


### Volitility and Options Pricing

##### Volatility Modeling with GARCH
   • [Volatility Modeling with GARCH](https://github.com/drewglov/Finance/blob/main/Volatility%20Modeling/Volatility_Modelling_with_GARCH_OOP.ipynb) - This project builds an industry-standard tool for analyzing and forecasting the time-varying volatility of a financial asset, the most common measure of risk. It utilizes and demonstrates:

- GARCH(1,1) Model for forecasting volatility - Tool for turning past market behavior into a dynamic, time-updating measure of risk using recent market shocks and recent levels of volatility.
- Time Series Analysis (Logarithmic Returns, Stationarity)
- Statistical Justification (Augmented Dickey-Fuller & Engle's ARCH tests)
- Model Validation via Residual Analysis
- Maximum Likelihood Estimation
- Object-Oriented Programming: The analysis is built into a reusable VolatilityModeler class that can be applied to any stock.

##### Options Pricing
   • [Options Pricing](https://github.com/drewglov/Finance/blob/main/Options%20Pricing/options-pricing.ipynb) - This project implements and analyzes options pricing models, including the Black-Scholes-Merton model and binomial tree methods. It incorporates implied volatility calculations and Greeks analysis for financial derivatives. It utilizes and demonstrates:

- Black-Scholes-Merton
- Binomial Trees
- Implied Volatility
- Options Greeks (Delta, Gamma, Theta, Vega, Rho)


### Credit Risk

##### Credit Risk Analysis
   • [Credit Risk Analysis](https://github.com/drewglov/Finance/blob/main/Credit%20Risk%20Analysis/credit-risk-analysis.ipynb) - A comprehensive credit risk analysis of a loan portfolio. The project focuses on evaluating the credit risk of loans in the US market by analyzing exposure at default (EAD), probability of default (PD), recovery rate, loss given default (LGD), and expected loss. It utilizes and demonstrates:

- Probability of Default (PD)
- Exposure at Default (EAD)
- Loss Given Default (LGD)
- Portfolio Metrics
- Risk Management
- Credit Portfolio Management


### Technology & Library Stack

- ***Language***: Python
- ***Core Libraries***: Pandas, NumPy, Matplotlib, SciPy
- ***Finance-Specific***: yfinance (for data acquisition), arch (for GARCH modeling), statsmodels (for statistical tests)
- ***Environment***: Jupyter Notebook
