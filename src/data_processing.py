"""Data processing and econometric diagnostics module for Brent Crude price analysis.

Provides reusable utilities for loading market data, calculating rolling metrics,
and executing stationarity tests (Augmented Dickey-Fuller).
"""

from dataclasses import dataclass
from typing import Dict, Any, Tuple, Optional
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller


@dataclass
class StationarityResult:
    """Dataclass holding the structured output of an ADF stationarity test."""
    adf_statistic: float
    p_value: float
    is_stationary: bool
    used_lag: int
    n_obs: int
    critical_values: Dict[str, float]

    def to_dict(self) -> Dict[str, Any]:
        """Convert result parameters to a dictionary format."""
        return {
            "adf_statistic": float(self.adf_statistic),
            "p_value": float(self.p_value),
            "is_stationary": bool(self.is_stationary),
            "used_lag": int(self.used_lag),
            "n_obs": int(self.n_obs),
            "critical_values": {str(k): float(v) for k, v in self.critical_values.items()}
        }


def load_brent_data(file_path: str, date_col: str = "Date", price_col: str = "Price") -> pd.DataFrame:
    """Load Brent Crude historical dataset, clean date formatting, and sort chronologically.

    Args:
        file_path (str): Path to the CSV file.
        date_col (str): Column name representing trading dates. Defaults to "Date".
        price_col (str): Column name representing spot prices. Defaults to "Price".

    Returns:
        pd.DataFrame: Processed DataFrame indexed by DatetimeIndex with clean price float series.
    """
    df = pd.read_csv(file_path)
    
    if date_col not in df.columns or price_col not in df.columns:
        raise KeyError(f"Expected columns '{date_col}' and '{price_col}' in {file_path}")

    # Ensure clean date parsing & sort chronologically
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col]).sort_values(by=date_col).reset_index(drop=True)
    df[price_col] = pd.to_numeric(df[price_col], errors="coerce")
    df = df.dropna(subset=[price_col])

    return df


def calculate_rolling_stats(
    series: pd.Series, 
    window: int = 30
) -> Tuple[pd.Series, pd.Series]:
    """Calculate moving average and rolling standard deviation for volatility tracking.

    Args:
        series (pd.Series): Time series data (e.g., daily prices).
        window (int): Rolling window size in trading days. Defaults to 30.

    Returns:
        Tuple[pd.Series, pd.Series]: Tuple containing (rolling_mean, rolling_std).
    """
    rolling_mean = series.rolling(window=window).mean()
    rolling_std = series.rolling(window=window).std()
    return rolling_mean, rolling_std


def run_adf_test(
    series: pd.Series, 
    significance_level: float = 0.05
) -> Dict[str, Any]:
    """Execute Augmented Dickey-Fuller (ADF) test to evaluate time-series stationarity.

    Args:
        series (pd.Series): Price or log-return series to test.
        significance_level (float): Threshold p-value for hypothesis decision (default: 0.05).

    Returns:
        Dict[str, Any]: Dictionary containing ADF statistic, p-value, critical values,
                        and boolean stationarity decision.
    """
    clean_series = series.dropna()
    if clean_series.empty:
        raise ValueError("Cannot run ADF test on an empty or all-NaN series.")

    print("[Diagnostics] Running Augmented Dickey-Fuller Test on price series...")
    adf_stat, p_value, used_lag, n_obs, critical_values, _ = adfuller(clean_series)
    is_stationary = p_value < significance_level

    print(f" -> ADF Statistic: {adf_stat:.4f}")
    print(f" -> p-value: {p_value:.4e}")
    print(f" -> Stationary: {is_stationary} (p < {significance_level})")

    result = StationarityResult(
        adf_statistic=float(adf_stat),
        p_value=float(p_value),
        is_stationary=is_stationary,
        used_lag=int(used_lag),
        n_obs=int(n_obs),
        critical_values=critical_values
    )

    return result.to_dict()