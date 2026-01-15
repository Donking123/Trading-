import pandas as pd

def pnl_decomposition(df: pd.DataFrame) -> pd.DataFrame:
    """
    Decompose total PnL into:
      - inventory_pnl: position_{t-1} * d_mid
      - execution_pnl: from execution attribution (must exist)

    Requires: mid, position, cash, execution_pnl
    Adds: d_mid, inventory_pnl, pnl_components, pnl_equity, pnl_diff
    """
    out = df.copy()

    out["d_mid"] = out["mid"].diff().fillna(0.0)

    out["inventory_pnl"] = out["position"].shift(1).fillna(0.0) * out["d_mid"]
    out["pnl_components"] = (out["inventory_pnl"] + out["execution_pnl"]).cumsum()

    out["equity"] = out["cash"] + out["position"] * out["mid"]
    out["pnl_equity"] = out["equity"] - out["equity"].iloc[0]

    out["pnl_diff"] = out["pnl_equity"] - out["pnl_components"]
    return out
