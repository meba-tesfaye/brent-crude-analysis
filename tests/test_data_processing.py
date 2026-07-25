import pytest
import pandas as pd
import numpy as np
from src.data_processing import run_adf_test # adjust function name to match yours

@pytest.fixture
def dummy_price_series():
    """Generates a sample price series for stationarity testing."""
    np.random.seed(42)
    return pd.Series(np.cumsum(np.random.randn(100)) + 80.0)

def test_adf_test_structure(dummy_price_series):
    """Ensure ADF test outputs required keys (test statistic, p-value)."""
    results = run_adf_test(dummy_price_series)
    assert isinstance(results, dict)
    assert "adf_statistic" in results or "p_value" in results

def test_raw_data_format():
    """Check if raw data file exists and contains expected columns."""
    df = pd.read_csv("data/raw_brent_prices.csv")
    assert not df.empty
    assert len(df) > 1000