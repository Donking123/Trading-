import numpy as np
import pandas as pd

def add_quotes(
    df: pd.DataFrame,
    base_spread: float = 0.02,
    k: float = 5.0,
    window: int = 3
) -> pd.DataFrame:
    """
    Add modeled bid/ask quotes around mid.
    Spread widens with a simple volatility proxy based on rolling abs(mid diff).

    Requires: mid, trade_qty
    Adds: abs_dmid, spread, bid, ask, expected_fill
    """
    out = df.copy()

    out["abs_dmid"] = out["mid"].diff().abs().fillna(0.0)
    vol_proxy = out["abs_dmid"].rolling(window, min_periods=1).mean()
    denom = float(vol_proxy.mean()) + 1e-12

    out["spread"] = base_spread * (1 + k * (vol_proxy / denom))
    out["bid"] = out["mid"] - out["spread"] / 2
    out["ask"] = out["mid"] + out["spread"] / 2

    out["expected_fill"] = np.where(
        out["trade_qty"] > 0, out["ask"],
        np.where(out["trade_qty"] < 0, out["bid"], np.nan)
    )

    return out


def execution_attribution(df: pd.DataFrame, fee_bps: float = 0.5) -> pd.DataFrame:
    """
    Attribute execution PnL into:
      - spread_pnl: mid - expected_fill (crossing spread)
      - slippage_pnl: expected_fill - fill_price (price improvement / worse fill)
      - fee_pnl: proportional fee on notional

    Requires: trade_qty, fill_price, mid, expected_fill
    Adds: notional, spread_pnl, slippage_pnl, fee_pnl, execution_pnl
    """
    out = df.copy()

    out["notional"] = (out["trade_qty"].abs() * out["fill_price"]).fillna(0.0)

    out["spread_pnl"] = (out["trade_qty"] * (out["mid"] - out["expected_fill"])).fillna(0.0)
    out["slippage_pnl"] = (out["trade_qty"] * (out["expected_fill"] - out["fill_price"])).fillna(0.0)

    out["fee_pnl"] = - (fee_bps / 1e4) * out["notional"]
    out["execution_pnl"] = out["spread_pnl"] + out["slippage_pnl"] + out["fee_pnl"]

    return out
