import numpy as np
import pandas as pd

def normalize_series(s: pd.Series) -> pd.Series:
    s = s.astype(float)
    mn, mx = s.min(), s.max()
    if np.isclose(mx - mn, 0):
        return pd.Series(np.zeros(len(s)), index=s.index)
    return (s - mn) / (mx - mn)

def classify_quantiles(s: pd.Series, q: int = 5, labels=None) -> pd.Series:
    if labels is None:
        labels = list(range(1, q+1))
    return pd.qcut(s, q=q, labels=labels, duplicates="drop")
