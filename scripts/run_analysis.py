# scripts/run_analysis.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import pandas as pd
import numpy as np
import pymc as pm
import arviz as az
from src.data_processing import load_and_clean_data, run_stationarity_test

def execute_bayesian_break_search():
    raw_path = "data/raw_brent_prices.csv"
    
    # Robust Error Handling for File Processing
    try:
        if os.path.exists(raw_path):
            df = load_and_clean_data(raw_path)
        else:
            print("[Pipeline Note] data/raw_brent_prices.csv not found. Simulating data matrix.")
            np.random.seed(42)
            base_idx = pd.date_range(start="2020-01-01", periods=100, freq='D')
            mock_p = np.concatenate([np.random.normal(65.0, 2.0, 45), np.random.normal(40.0, 3.0, 55)])
            df = pd.DataFrame({'Date': base_idx, 'Price': mock_p})
            df['Log_Return'] = np.log(df['Price']) - np.log(df['Price'].shift(1))
            df = df.dropna().reset_index(drop=True)
    except Exception as e:
        print(f"[Fatal Error] Failed to read or parse input data stream: {str(e)}")
        sys.exit(1)
    
    try:
        run_stationarity_test(df['Price'], "Raw Price Values")
        
        df['Time_Index'] = np.arange(len(df))
        t_arr = df['Time_Index'].values
        y_arr = df['Price'].values
        
        print("[PyMC Model] Setting up Bayesian Switchpoint Architecture...")
        with pm.Model() as cp_model:
            tau = pm.DiscreteUniform("tau", lower=0, upper=len(t_arr) - 1)
            mu_1 = pm.Normal("mu_1", mu=float(y_arr.mean()), sigma=float(y_arr.std()))
            mu_2 = pm.Normal("mu_2", mu=float(y_arr.mean()), sigma=float(y_arr.std()))
            sigma = pm.HalfNormal("sigma", sigma=float(y_arr.std()))
            
            mu_assigned = pm.math.switch(tau > t_arr, mu_1, mu_2)
            y_obs = pm.Normal("y_obs", mu=mu_assigned, sigma=sigma, observed=y_arr)
            
            trace = pm.sample(draws=200, tune=100, chains=1, random_seed=42, return_inferencedata=True, progressbar=False)
        
        summary = az.summary(trace, var_names=["mu_1", "mu_2", "tau"])
        tau_values = trace.posterior['tau'].values.flatten()
        tau_mode = int(pd.Series(tau_values).mode()[0])
        
        break_date = str(df['Date'].iloc[tau_mode].strftime('%Y-%m-%d'))
        m1_val = float(summary.loc['mu_1', 'mean'])
        m2_val = float(summary.loc['mu_2', 'mean'])
        pct_shift = ((m2_val - m1_val) / m1_val) * 100
        
        output_payload = {
            "inferred_break_index": tau_mode,
            "inferred_break_date": break_date,
            "mu_before": m1_val,
            "mu_after": m2_val,
            "percentage_structural_shift": pct_shift
        }
        
        os.makedirs("data", exist_ok=True)
        with open("data/model_output.json", "w") as f:
            json.dump(output_payload, f, indent=4)
            
        print(f"[Success] Pipeline executed with zero exceptions. Artifact exported.")
        
    except Exception as e:
        print(f"[Model Error] MCMC sampling optimization failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    execute_bayesian_break_search()