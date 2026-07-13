import pandas as pd
from statsmodels.tsa.stattools import adfuller

def run_adf_test(series):
    """
    Executes an Augmented Dickey-Fuller test to evaluate timeseries stationarity.
    Returns True if stationary, False if non-stationary.
    """
    print("[Diagnostics] Running Augmented Dickey-Fuller Test on price series...")
    result = adfuller(series.dropna())
    
    adf_stat = result[0]
    p_value = result[1]
    
    print(f" -> ADF Statistic: {adf_stat:.4f}")
    print(f" -> p-value: {p_value:.4e}")
    
    # Critical threshold rejection at alpha = 5%
    if p_value <= 0.05:
        print(" -> Stationary: True")
        return True
    else:
        print(" -> Stationary: False (Unit root detected, series has trending properties)")
        return False
