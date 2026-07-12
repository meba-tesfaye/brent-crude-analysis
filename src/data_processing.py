import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller

def load_and_clean_data(filepath):
    """Loads, cleans, and computes daily log returns for Brent Crude data."""
    print(f"[Pipeline] Processing raw time series data: {filepath}")
    df = pd.read_csv(filepath)
    
    # Clean dates
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date']).sort_values('Date').reset_index(drop=True)
    
    # Clean numeric prices
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df = df.dropna(subset=['Price']).reset_index(drop=True)
    
    # Compute daily log returns to control for variance clustering
    df['Log_Return'] = np.log(df['Price']) - np.log(df['Price'].shift(1))
    
    return df.dropna().reset_index(drop=True)

def run_stationarity_test(series_data, name="Series"):
    """Performs the Augmented Dickey-Fuller diagnostic test."""
    print(f"[Diagnostics] Running Augmented Dickey-Fuller Test on: {name}")
    res = adfuller(series_data.values)
    
    metrics = {
        'ADF Statistic': res[0],
        'p-value': res[1],
        'Stationary': bool(res[1] < 0.05)
    }
    
    print(f" -> ADF Stat: {metrics['ADF Statistic']:.4f}, p-value: {metrics['p-value']:.4e}")
    print(f" -> Stationary: {metrics['Stationary']}")
    return metrics
