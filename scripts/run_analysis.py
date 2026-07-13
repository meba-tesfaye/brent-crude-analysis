import os
import json
import pandas as pd
from src.data_processing import run_adf_test
from src.model_building import run_bayesian_change_point

def main():
    # Setup structural relative paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "raw_brent_prices.csv")
    output_path = os.path.join(base_dir, "data", "model_output.json")
    
    print(f"Loading raw price data from {data_path}...")
    df = pd.read_csv(data_path)
    df['Date'] = pd.to_datetime(df['Date'], format='mixed')
    df = df.sort_values('Date').reset_index(drop=True)
    
    print("\n--- Executing Stage 1: Stationarity Verification ---")
    is_stationary = run_adf_test(df['Price'])
    
    print("\n--- Executing Stage 2: Bayesian Change Point Sampling ---")
    try:
        metrics, model, trace = run_bayesian_change_point(df['Price'])
        
        # Map discrete tau index back to the exact calendar date
        tau_idx = metrics["inferred_tau_index"]
        break_date = df.loc[tau_idx, 'Date'].strftime('%Y-%m-%d')
        metrics["inferred_break_date"] = break_date
        
        print("\nInference Complete! Results Summary:")
        print(f"  - Structural Break Date: {break_date} (Index {tau_idx})")
        print(f"  - Pre-Break Mean Price: ${metrics['mu_before']:.2f} (R-hat: {metrics['diagnostics']['rhat_mu1']:.2f})")
        print(f"  - Post-Break Mean Price: ${metrics['mu_after']:.2f} (R-hat: {metrics['diagnostics']['rhat_mu2']:.2f})")
        print(f"  - Model Convergence Verified: {metrics['diagnostics']['chains_converged']}")
        
        # Write out updated parameter dictionary to disk
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(metrics, f, indent=4)
            
        print(f"\nSuccessfully materialized model parameters to: {output_path}")
        
    except Exception as e:
        print(f"\n[CRITICAL RUNTIME ERROR] Sampling pipeline failed: {str(e)}")
        raise e

if __name__ == "__main__":
    main()