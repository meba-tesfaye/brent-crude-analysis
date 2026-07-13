import pymc as pm
import numpy as np
import pandas as pd

def run_bayesian_change_point(prices_series):
    """
    Builds and executes a Bayesian Switchpoint Architecture using PyMC.
    """
    y = np.array(prices_series)
    T = len(y)
    t = np.arange(T)
    
    mean_y = np.mean(y)
    std_y = np.std(y)
    
    print(f"Initializing PyMC Change Point Architecture over {T} intervals...")
    
    with pm.Model() as model:
        # Priors
        tau = pm.DiscreteUniform("tau", lower=0, upper=T - 1)
        mu_1 = pm.Normal("mu_1", mu=mean_y, sigma=std_y)
        mu_2 = pm.Normal("mu_2", mu=mean_y, sigma=std_y)
        sigma = pm.HalfNormal("sigma", sigma=std_y)
        
        # Structural breakpoint mapping logic
        mu_regime = pm.math.switch(tau > t, mu_1, mu_2)
        
        # Likelihood
        likelihood = pm.Normal("y_obs", mu=mu_regime, sigma=sigma, observed=y)
        
        print("Executing MCMC sampling (NUTS + Metropolis step configuration)...")
        trace = pm.sample(draws=2000, tune=1000, return_inferencedata=True, random_seed=42)
        
    # Extract posterior calculation estimates safely
    summary = pm.summary(trace, var_names=["tau", "mu_1", "mu_2"])
    
    inferred_tau = int(round(float(summary.loc["tau", "mean"])))
    inferred_mu1 = float(summary.loc["mu_1", "mean"])
    inferred_mu2 = float(summary.loc["mu_2", "mean"])
    pct_shift = ((inferred_mu2 - inferred_mu1) / inferred_mu1) * 100
    
    metrics = {
        "inferred_break_index": inferred_tau,
        "mu_before": inferred_mu1,
        "mu_after": inferred_mu2,
        "percentage_structural_shift": pct_shift
    }
    
    return metrics, model, trace