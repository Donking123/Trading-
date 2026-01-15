import numpy as np
import pandas as pd

from execution import add_quotes, execution_attribution
from ledger import build_ledger
from pnl import pnl_decomposition


def test_pnl_identity_holds_with_fees():
    # Minimal synthetic dataset (small, deterministic)
    df = pd.DataFrame({
        "t": pd.date_range("2026-01-01 09:30", periods=8, freq="min"),
        "mid": [100.00, 100.20, 100.10, 100.30, 100.25, 100.40, 100.35, 100.50],
        "trade_qty": [0, +10, 0, -4, 0, 0, +2, 0],
        "fill_price": [np.nan, 100.21, np.nan, 100.28, np.nan, np.nan, 100.36, np.nan],
    })

    # Execution first (so fee_pnl exists), then ledger (so fees hit cash), then PnL
    df = add_quotes(df, base_spread=0.02, k=5.0, window=3)
    df = execution_attribution(df, fee_bps=0.5)
    df = build_ledger(df)              # includes fee_pnl in cash_flow
    df = pnl_decomposition(df)

    # Identity check: equity-based PnL equals sum of components (inventory + execution)
    assert abs(df["pnl_diff"].iloc[-1]) < 1e-9
