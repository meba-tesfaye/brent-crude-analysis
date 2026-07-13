# Brent Crude Oil Structural Break Analysis & Dashboard

An end-to-end data analytics and advanced statistical pipeline that detects structural regime shifts in historical Brent Crude Oil spot prices. The project couples a classical econometric exploratory framework with a **Bayesian Switchpoint Architecture** in PyMC, serving the final insights through an interactive **Flask & Chart.js** dashboard.

---

## 📊 Key Analytical Insights
The model analyzed **9,011 daily market trading entries** from May 1987 to November 2022 and successfully captured a massive macroeconomic regime shift:
* **Inferred Structural Break Date:** `2005-02-24`
* **Pre-Break Baseline Mean Price:** `$21.42`
* **Post-Break Baseline Mean Price:** `$75.61`
* **Long-Term Regime Shift Magnitude:** `+252.9%`

This shift perfectly mirrors the mid-2000s commodities boom, capturing the permanent transition of global crude prices driven by surging demand from emerging markets and tightening global capacity.

---

## 🛠️ Repository Architecture
The repository follows standard modular software engineering patterns:

```text
brent-crude-analysis/
├── data/
│   ├── raw_brent_prices.csv      # Full historical dataset (9,011 rows)
│   └── model_output.json         # Materialized Bayesian inference parameters
├── scripts/
│   └── run_analysis.py           # Core execution orchestration runner
├── src/
│   ├── __init__.py
│   ├── data_processing.py        # Stationarity diagnostics (ADF Test)
│   ├── model_building.py         # PyMC Switchpoint framework configuration
│   └── app.py                    # Flask API web server
└── templates/
    └── dashboard.html            # Tailwind CSS & Chart.js analytical UI