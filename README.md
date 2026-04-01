# Finance Portfolio

Hello, welcome to my repository containing a portfolio of finance and algorithmic trading projects completed by me for career, academic, self-learning, and hobby purposes. These projects are presented in the form of iPython Notebooks, and have been completed using Python 3.14 along with various libraries and tools such as Pandas, Matplotlib, and the QuantConnect Lean Engine.

I am always willing to meet new people in hopes of doing business together. I can be reached via email at drewrglov@gmail.com.


## Contents

### Optimization

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


### Technology & Library Stack

- ***Language***: Python
- ***Core Libraries***: Pandas, NumPy, Matplotlib, SciPy
- ***Finance-Specific***: yfinance (for data acquisition), arch (for GARCH modeling), statsmodels (for statistical tests)
- ***Environment***: Jupyter Notebook
