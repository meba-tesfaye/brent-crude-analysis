# Brent Crude Analytical Workflow & Methodology

This document outlines the systematic research process, mathematical assumptions, and limitations behind our structural change point evaluation pipeline.

---

## 📋 Operational Workflow Stage Gates

1. **Ingestion & Processing:** Daily raw oil price records are collected from `raw_brent_prices.csv`, sorted temporally, and parsed to handle mixed timestamp string formatting.
2. **Stationarity Diagnostics:** An Augmented Dickey-Fuller (ADF) regression test checks if our historical prices have a constant mean and variance over time, confirming whether modeling a discrete switchpoint is appropriate.
3. **MCMC Architecture Execution:** We parameterize a Bayesian Switchpoint layout using dual MCMC sampling routines to estimate the exact index boundary ($\tau$) where the price distribution permanently shifted.
4. **Parameter Serialization:** Converged numerical posterior parameters are saved to an exchangeable `model_output.json` contract.
5. **UI Delivery Application:** A decoupled presentation layer accesses the results over HTTP to render interactive visual insights for stakeholders.

---

## ⚠️ Modeling Assumptions & Constraints

### 1. Independent and Identically Distributed Errors (I.I.D.)
Our change point layout models prices before and after the break using normal distributions with an unpooled variance parameter ($\sigma$). It assumes that daily price fluctuations around those means are independent. In real-world market contexts, price data exhibits heavy-tailed volatility clustering and local autocorrelation.

### 2. The Correlation vs. Causation Constraint
The pipeline successfully isolates **February 24, 2005** as a permanent statistical transition point where historical averages shifted from a low-level baseline (\$21.42) to an elevated baseline (\$75.61). 

However, it is critical to acknowledge that **this structural break is a correlation, not an isolated causation**. The change point cannot be tied to a single isolated event on that exact calendar date. Instead, it marks the exact convergence boundary where multiple multi-year macroeconomic factors came to a head:
* The multi-year compounding industrial explosion of emerging markets (primarily China's infrastructure expansion).
* Prolonged structural declines in global oil extraction spare capacity.
* Compounding geopolitical instability premiums in the Middle East following the 2003 Iraq War.

The model captures the structural *climax* of these forces, but the true underlying cause is a systemic web of global factors rather than a single event.