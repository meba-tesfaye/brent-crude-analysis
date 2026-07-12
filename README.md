# Brent Crude Structural Break Analysis Engine

An end-to-end data processing, diagnostic, and Bayesian inference pipeline built to identify structural breaks and macroeconomic switch-points in crude oil time series data.

---

## Task 1a: Analysis Workflow, Event Dataset, & Assumptions

### 1. Analysis Workflow Architecture
The system processes raw, non-stationary market inputs through a multi-stage analytical framework:
1. **Ingestion & Type Alignment:** Converts raw input fields to high-precision datetime formats and standardized continuous floating-point prices.
2. **Variance Control & Stationarity Transformation:** Computes daily log returns ($R_t = \ln(P_t / P_{t-1})$) to isolate sudden architectural clustering shifts and break down variance volatility.
3. **Statistical Diagnostic Tests:** Submits the data arrays to an Augmented Dickey-Fuller (ADF) unit-root test to determine data stationarity.
4. **Bayesian Inversion Modeling:** Feeds structural metrics directly into a Markov Chain Monte Carlo (MCMC) sampler utilizing mixed discrete and continuous state-spaces to pinpoint the break date window.

### 2. Event Dataset & Simulating Break Contexts
The workflow evaluates asset behaviors surrounding distinct macroeconomic structural events. In the absence of an external dataset file, the data sub-system instantiates a controlled structural break vector array representing a severe market liquidity shock:
* **Pre-Break Phase (Days 0–44):** Simulates a stable global economic landscape centering at a baseline mean price ($\mu_1$) of **$64.50**.
* **Post-Break Phase (Days 45–100):** Simulates an abrupt demand destruction event or macro supply shock, dropping the baseline mean price ($\mu_2$) directly down to **$39.96**.

### 3. Core Analytical Assumptions
* **Independent Identically Distributed Errors ($i.i.d.$):** Price deviations around the localized phase means are assumed to follow a normal distribution ($\epsilon \sim N(0, \sigma^2)$).
* **Single Structural Discontinuity:** The structural shift is modeled as an instantaneous step change controlled by an isolated temporal switch-point parameter ($\tau$).

---

## Task 1b: Time Series EDA & Change Point Model Understanding

### 1. Exploratory Data Analysis & Diagnostics
When evaluating raw time-series data levels, standard price indices show high levels of path dependency and non-stationarity. Our pipeline diagnostic output confirms this:
* **ADF Statistic:** `-1.3612`
* **p-value:** `0.6007` (`Stationary: False`)

Because the $p$-value is significantly greater than the 5% threshold ($\alpha = 0.05$), we fail to reject the null hypothesis of a unit root. This formally justifies transforming the raw inputs into log returns or tracking variance shifts directly via an explicit step change framework to handle non-stationary historical paths cleanly.

### 2. Bayesian Change Point Mathematical Model Design
The structural breakpoint is captured using a PyMC conditional mapping layout. The temporal trajectory transitions instantly at index parameter $\tau$:

$$\mu = \begin{cases} \mu_1 & \text{if } t < \tau \\ \mu_2 & \text{if } t \geq \tau \end{cases}$$

Our uninformative and weakly informative structural priors are specified as:
* **Switch-point Prior ($\tau$):** $\tau \sim \text{DiscreteUniform}(0, T-1)$ — gives every observation window index an equal likelihood of containing the structural transition.
* **Phase Mean Priors ($\mu_1, \mu_2$):** $\mu_i \sim \text{Normal}(\bar{y}, \sigma_y)$ — centers distributions directly over the observed baseline boundaries while allowing wide search flexibility.
* **Global Volatility Prior ($\sigma$):** $\sigma \sim \text{HalfNormal}(\sigma_y)$ — restricts variances strictly to real positive numbers.

---

## Repository & Code Best Practices

### 1. Production Folder Structure
```text
brent-crude-analysis/
├── data/                  # Standardized data landing zone
│   └── model_output.json  # Inferred model configuration artifact
├── scripts/               # Runtime execution workflows
│   └── run_analysis.py    # PyMC Bayesian inference script
├── src/                   # Reusable source modules
│   └── data_processing.py # Functional engineering & statistical tests
├── env/                   # Isolated local virtual environment (ignored)
├── requirements.txt       # Strict package pinning
└── README.md              # Project documentation
* **Correlation vs Causal Impact Disclaimers:** The change point model isolates structural discontinuities strictly as mathematical shifts across time. These calculations represent chronological correlation and data-level variance partition points. They do not automatically imply or prove direct standalone causality without corresponding validation against external narrative events (such as those outlined in `data/events.csv`).