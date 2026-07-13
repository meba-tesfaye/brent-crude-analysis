import sys
import os
import json
import pandas as pd

# Automatically append repository root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_processing import run_stationarity_test
from src.model_building import run_bayesian_change_point

def main():
    # Define relative paths
    data_path = os.path.join("data", "raw_brent_prices.csv")
    output_json_path = os.path.join("data", "model_output.json")
    
    # Verify data asset presence
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Missing mandatory data file asset: {data_path}")
        
    print(f"Loading raw price data from {data_path}...")
    df = pd.read_csv(data_path)
    df['Date'] = pd.to_datetime(df['Date'], format='mixed')
    df = df.sort_values('Date').reset_index(drop=True)
    
    # Stage 1: Stationarity Verification
    print("\n--- Executing Stage 1: Stationarity Verification ---")
    run_stationarity_test(df['Price'])
    
    # Stage 2: Bayesian Change Point Sampling (Task 2)
    print("\n--- Executing Stage 2: Bayesian Change Point Sampling ---")
    try:
        metrics, model, trace = run_bayesian_change_point(df['Price'])
        
        # Map the inferred break index to an explicit calendar date
        break_idx = metrics["inferred_break_index"]
        inferred_date = str(df['Date'].iloc[break_idx].date())
        metrics["inferred_break_date"] = inferred_date
        
        print("\nInference Complete! Results Summary:")
        print(f"  - Structural Break Date: {inferred_date} (Index {break_idx})")
        print(f"  - Pre-Break Mean Price: ${metrics['mu_before']:.2f}")
        print(f"  - Post-Break Mean Price: ${metrics['mu_after']:.2f}")
        print(f"  - Change Magnitude: {metrics['percentage_structural_shift']:.2f}%")
        
        # Save output for the Task 3 Dashboard interface
        with open(output_json_path, 'w') as f:
            json.dump(metrics, f, indent=4)
        print(f"\nSuccessfully materialized model parameters to: {output_json_path}")
        
    except Exception as e:
        print(f"\n[CRITICAL RUNTIME ERROR] Sampling pipeline failed: {str(e)}")
        raise e

if __name__ == "__main__":
    main()