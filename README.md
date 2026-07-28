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
* **Pre-Break Baseline Mean Price:** `$21.42`
* **Post-Break Baseline Mean Price:** `$75.61`
* **Long-Term Regime Shift Magnitude:** `+252.9%`

This shift perfectly mirrors the mid-2000s commodities boom, capturing the permanent transition of global crude prices driven by surging demand from emerging markets and tightening global capacity.

---

## 🚀 Quick Start

### 1. Prerequisites & Setup
```bash
# Clone the repository
git clone [https://github.com/meba-tesfaye/brent-crude-analysis.git](https://github.com/meba-tesfaye/brent-crude-analysis.git)
cd brent-crude-analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
