# Brent Crude Oil Structural Break Analysis & Dashboard

![Python Continuous Integration](https://github.com/meba-tesfaye/brent-crude-analysis/actions/workflows/unittests.yml/badge.svg)

An end-to-end data analytics and advanced statistical pipeline that detects structural regime shifts in historical Brent Crude Oil spot prices. The project couples a classical econometric exploratory framework with a **Bayesian Switchpoint Architecture** in PyMC, serving the final insights through an interactive **Flask & Chart.js** dashboard.

---

## 💼 Business Problem
Commodities trading desks and risk management teams face severe financial exposure when macroeconomic regime shifts occur. Standard econometric models often treat permanent baseline price level adjustments as temporary volatility, leading to mispriced derivatives, inaccurate Value-at-Risk (VaR) estimates, and poor hedging strategies.

Identifying the exact date and magnitude of a structural break enables energy risk managers to recalibrate baseline price expectations and portfolio exposure accurately.

---

## 🛠️ Solution Overview
To solve this, we engineered an automated Bayesian regime detection pipeline:
1. **Econometric Diagnostics**: Performed Augmented Dickey-Fuller (ADF) stationarity testing on historical daily spot prices.
2. **Probabilistic Modeling**: Formulated a PyMC Bayesian Switchpoint model utilizing MCMC sampling to infer structural shift parameters without human bias.
3. **Parameter Materialization**: Serialized posterior probability estimates into a lightweight JSON schema for low-latency web consumption.
4. **Interactive Risk Dashboard**: Served results through a Flask backend and dark-mode Tailwind CSS + Chart.js analytical interface.

---

## 📊 Key Results
The model analyzed **9,011 daily market trading entries** from May 1987 to November 2022 and successfully captured a massive macroeconomic regime shift:
* **Inferred Structural Break Date:** `2005-02-24`
* **Pre-Break Baseline Mean Price:** `$21.41 / bbl`
* **Post-Break Baseline Mean Price:** `$75.61 / bbl`
* **Long-Term Regime Shift Magnitude:** `+253.1%` upward shift
* **MCMC Convergence Quality:** $\hat{R} = 1.00$ with zero divergent transitions

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
```

## 🚀 Quick Start

### 1. Prerequisites & Setup
```bash
# Clone the repository
git clone https://github.com/meba-tesfaye/brent-crude-analysis.git
cd brent-crude-analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Execution & Testing
```bash
# Run unit tests
pytest tests/

# Run Bayesian analysis pipeline
python -m scripts.run_analysis

# Launch interactive Flask dashboard
python src/app.py
```

## 🖥️ Demo
Launch the interactive web service using `python src/app.py` and navigate to `http://127.0.0.1:5000`:

* **Interactive Dashboard URL**: [http://127.0.0.1:5000](http://127.0.0.1:5000)
* **Visual Artifacts**:
  * **Interactive Regime Chart**: Real-time Chart.js rendering of daily spot prices overlaid with the inferred Bayesian baseline shift.
  * **Risk Desk KPI Cards**: Instant visibility into pre-break (\$21.41) vs. post-break (\$75.61) baseline parameters.
  * **Convergence Diagnostics**: Direct inspection of MCMC trace statistics ($\hat{R}$ metrics).

---

## 🔬 Technical Details

* **Data**: 
  * **Source**: Historical Brent Crude Oil daily spot prices (May 1987 – November 2022, 9,011 observations).
  * **Preprocessing**: Parsed date indices, handled missing daily trading logs, and executed Augmented Dickey-Fuller (ADF) stationarity diagnostics ($p > 0.05$).
* **Model**: 
  * **Algorithm**: PyMC Bayesian Switchpoint Architecture using Markov Chain Monte Carlo (MCMC) sampling.
  * **Priors**: Switchpoint $\tau \sim \text{DiscreteUniform}(1, N)$, Pre-break baseline $\mu_1 \sim \text{Exponential}(1)$, Post-break baseline $\mu_2 \sim \text{Exponential}(1)$.
* **Evaluation**: 
  * **Metrics & Validation**: Gelman-Rubin convergence diagnostic ($\hat{R} = 1.00$), Effective Sample Size ($\text{ESS} > 1,000$), and zero divergent transitions during sampling chains.

---

## 🔮 Future Improvements
1. **Multi-Break Hierarchical Model**: Extend the single-switchpoint PyMC model to a Markov Switching / Multi-Break model to detect secondary historical shocks (e.g., 2008 Financial Crisis, 2020 COVID shock).
2. **Exogenous Macro Driver Integration**: Incorporate global supply/demand indicators (OPEC production quotas, US Dollar Index) as covariates in a Bayesian Structural Time Series (BSTS) framework.
3. **Automated Risk API Hooks**: Expose REST endpoints to directly stream updated baseline parameters into corporate Value-at-Risk (VaR) calculation engines.

---

## 📝 Technical Report / Blog Post

### Title: Quantifying Macroeconomic Regime Shifts in Crude Oil via Bayesian Switchpoint Models

**Abstract & Executive Summary**  
Macroeconomic uncertainty and geopolitical instability make global energy commodities notoriously volatile. When analyzing historical Brent Crude spot prices spanning 35 years (9,011 daily observations), standard linear regression models fall short because they assume a single continuous price mean.

This technical report details an engineering approach to detecting structural regime shifts using PyMC's Bayesian Switchpoint modeling architecture.

**Methodology & Engineering Lifecycle**
1. **Stationarity Diagnostics**: An Augmented Dickey-Fuller (ADF) test confirmed non-stationarity ($p > 0.05$), validating that raw price series could not be reliably modeled using simple mean-reverting techniques without accounting for regime changes.
2. **Bayesian Framework**: We specified a discrete uniform prior over the entire time vector $t \in [1, N]$ for the switchpoint $\tau$, alongside Exponential priors for pre-break mean $\mu_1$ and post-break mean $\mu_2$.
3. **Inference & Results**: MCMC sampling converged on **February 24, 2005**, as the exact structural pivot date. Prior to this date, Brent Crude maintained an average baseline of **$21.41/bbl**. Following the break, the structural baseline shifted upward by **253.1%** to **$75.61/bbl**.

**Financial Risk Implications & Lessons Learned**  
By embedding this inference framework into an automated Flask UI, commodities trading desks can dynamically recalibrate risk exposure models (such as Value-at-Risk limits and options volatility surfaces) relative to structural market regimes rather than arbitrary historical rolling averages.

---

## 🎙️ Presentation Slide Deck Outline (Finance Sector Focus)

* **Slide 1: Title Slide**  
  * **Title**: Structural Break Analysis & Risk Decision Framework for Brent Crude Oil  
  * **Subtitle**: A Production-Grade Bayesian Approach to Commodity Regime Detection  
  * **Presenter**: Meba Tesfaye | Systems & Data Engineer  

* **Slide 2: The Financial Challenge**  
  * Unmodeled regime shifts lead to severe risk mispricing in commodities portfolios.  
  * Standard rolling averages fail during structural macro shocks.  
  * **Goal**: Provide trading and risk teams with transparent, automated break-detection tools.

* **Slide 3: Data & Engineering Rigor**  
  * 9,011 daily trading records analyzed (May 1987 – Nov 2022).  
  * Fully modular Python architecture (`src/` package layout).  
  * Automated testing & continuous integration (`pytest` + GitHub Actions CI badge).

* **Slide 4: Analytical Findings & Macro Insights**  
  * **Inferred Break Date**: February 24, 2005.  
  * **Regime Transition**: $21.41/bbl → $75.61/bbl (+253.1%).  
  * Alignment with fundamental macroeconomic drivers (rapid emerging market demand expansion).

* **Slide 5: Interactive Risk Dashboard & Live Artifacts**  
  * Live Flask + Tailwind CSS dashboard demonstration.  
  * Materialized Bayesian posterior parameters for real-time risk decision support.  
  * Full open-source proof of work on GitHub.
---

## 👤 Author

* **Name:** Meba Tesfaye
* **Role:** Systems & Data Engineer
* **GitHub:** [https://github.com/meba-tesfaye](https://github.com/meba-tesfaye)
* **Project Repository:** [https://github.com/meba-tesfaye/brent-crude-analysis](https://github.com/meba-tesfaye/brent-crude-analysis)