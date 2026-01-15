import pandas as pd
import numpy as np

def build_ledger(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build trading ledger state for a single instrument.

    Required columns:
      - trade_qty: +buy, -sell, 0 none
      - fill_price: fill price when trade occurs, NaN otherwise
      - mid: mid price

    Adds columns:
      - position
      - cash_flow
      - cash
      - equity
    """
    out = df.copy()

    # Position (inventory)
    out["position"] = out["trade_qty"].cumsum()

    # Cash flow from executed trades (0 if no trade)
    out["cash_flow"] = - out["trade_qty"] * out["fill_price"]
    out["cash_flow"] = out["cash_flow"].fillna(0.0)

    # NEW: include fees in cash (fees are negative numbers)
    if "fee_pnl" in out.columns:
        out["cash_flow"] = out["cash_flow"] + out["fee_pnl"].fillna(0.0)

    # Cash balance
    out["cash"] = out["cash_flow"].cumsum()

    # Mark-to-market equity
    out["equity"] = out["cash"] + out["position"] * out["mid"]

    return out
