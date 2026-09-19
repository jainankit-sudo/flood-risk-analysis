import pandas as pd
from src.risk_model import normalize_series

def test_normalize_series_basic():
    s = pd.Series([0, 5, 10])
    out = normalize_series(s)
    assert out.iloc[0] == 0.0
    assert out.iloc[-1] == 1.0
    assert round(out.iloc[1],2) == 0.5
