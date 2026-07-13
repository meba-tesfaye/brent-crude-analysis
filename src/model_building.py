import pymc as pm
import numpy as np
import pandas as pd
import arviz as az
import json
import os

def run_bayesian_change_point(price_series):
    """
    Builds and samples a Bayesian Switchpoint model on Brent Crude prices.
    Tracks structural break index (tau), pre/after means, and convergence diagnostics.
    """
    print(f"Initializing PyMC Change Point Architecture over {len(price_series)} intervals...")
    
    # Define time index vector
    t = np.arange(len(price_series))
    
    with pm.Model() as model:
        # 1. Prior Configurations
        tau = pm.DiscreteUniform("tau", lower=0, upper=len(price_series) - 1)
        mu_1 = pm.Normal("mu_1", mu=price_series.mean(), sigma=price_series.std())
        mu_2 = pm.Normal("mu_2", mu=price_series.mean(), sigma=price_series.std())
        sigma = pm.Uniform("sigma", lower=0, upper=price_series.std() * 2)
        
        # 2. Mathematical Switch Logic
        mu_latent = pm.math.switch(tau > t, mu_1, mu_2)
        
        # 3. Likelihood Function
        likelihood = pm.Normal("y", mu=mu_latent, sigma=sigma, observed=price_series.values)
        
        # 4. MCMC Chain Sampling (Metropolis for discrete tau, NUTS for continuous parameters)
        print("Executing MCMC sampling (4 chains, compound configuration)...")
        trace = pm.sample(
            draws=2000, 
            tune=1000, 
            chains=4, 
            step=[pm.Metropolis(vars=[tau]), pm.NUTS(vars=[mu_1, mu_2, sigma])],
            random_seed=42,
            return_inferencedata=True
        )
    
    print("\n--- Computing Posterior Summary & Convergence Diagnostics ---")
    # Generate summary tracking mean values and r_hat (Gelman-Rubin diagnostic)
    summary = pm.summary(trace, var_names=["tau", "mu_1", "mu_2", "sigma"])
    print(summary)
    
    # Extract exact parameter estimations
    inferred_tau = int(round(float(summary.loc["tau", "mean"])))
    mu_before_val = float(summary.loc["mu_1", "mean"])
    mu_after_val = float(summary.loc["mu_2", "mean"])
    pct_shift = ((mu_after_val - mu_before_val) / mu_before_val) * 100
    
    # Extract R-hat convergence diagnostics
    rhat_tau = float(summary.loc["tau", "r_hat"])
    rhat_mu1 = float(summary.loc["mu_1", "r_hat"])
    rhat_mu2 = float(summary.loc["mu_2", "r_hat"])
    
    metrics = {
        "inferred_tau_index": inferred_tau,
        "mu_before": mu_before_val,
        "mu_after": mu_after_val,
        "percentage_structural_shift": pct_shift,
        "diagnostics": {
            "rhat_tau": rhat_tau,
            "rhat_mu1": rhat_mu1,
            "rhat_mu2": rhat_mu2,
            "chains_converged": all(val <= 1.05 for val in [rhat_tau, rhat_mu1, rhat_mu2])
        }
    }
    
    return metrics, model, trace