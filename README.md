# Brent Crude Oil Structural Break Analysis & Dashboard

![Python Continuous Integration](https://github.com/meba-tesfaye/brent-crude-analysis/actions/workflows/unittests.yml/badge.svg)

An end-to-end data analytics and advanced statistical pipeline that detects structural regime shifts in historical Brent Crude Oil spot prices. The project couples a classical econometric exploratory framework with a **Bayesian Switchpoint Architecture** in PyMC, serving the final insights through an interactive **Flask & Chart.js** dashboard.

---

## 💼 Business Problem
Commodities trading desks and risk management teams face severe financial exposure when macroeconomic regime shifts occur. Standard econometric models often treat permanent baseline price level adjustments as temporary volatility, leading to mispriced derivatives, inaccurate Value-at-Risk (VaR) estimates, and poor hedging strategies.

Identifying the exact date and magnitude of a structural break enables energy risk managers to recalibrate baseline price expectations and portfolio exposure accurately.

---

## 📊 Key Analytical Insights
The model analyzed **9,011 daily market trading entries** from May 1987 to November 2022 and successfully captured a massive macroeconomic regime shift:
* **Inferred Structural Break Date:** `2005-02-24`
* **Pre-Break Baseline Mean Price:** `$21.41`
* **Post-Break Baseline Mean Price:** `$75.61`
* **Long-Term Regime Shift Magnitude:** `+253.1%`

This shift perfectly mirrors the mid-2000s commodities boom, capturing the permanent transition of global crude prices driven by surging demand from emerging markets and tightening global capacity.

---

## 📁 Project Structure

```text
brent-crude-analysis/
├── .github/
│   └── workflows/
│       └── unittests.yml          # CI/CD workflow running pytest on push
├── .vscode/                       # VS Code workspace configurations
├── data/
│   ├── raw_brent_prices.csv      # Full historical dataset (9,011 rows)
│   └── model_output.json         # Materialized Bayesian inference parameters
├── frontend/                      # Decoupled React analytical dashboard UI
├── notebooks/                     # Exploratory analysis & PyMC prototyping
├── scripts/
│   └── run_analysis.py            # Core execution orchestration runner
├── src/
│   ├── __init__.py
│   ├── data_processing.py        # Stationarity diagnostics (ADF Test)
│   ├── model_building.py         # PyMC Switchpoint framework configuration
│   └── app.py                    # Flask API web server
├── templates/
│   └── dashboard.html            # Tailwind CSS & Chart.js analytical UI
├── tests/
│   ├── __init__.py
│   └── test_data_processing.py   # Unit tests for data pipeline & ADF test
├── .gitignore                    # Git tracking exclusion rules
├── ANALYSIS_WORKFLOW.md          # Workflow execution guide
├── README.md                     # Technical documentation & project guide
└── requirements.txt              # Pin-locked project dependencies