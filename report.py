import pandas as pd

def make_report(df: pd.DataFrame) -> dict:
    """
    Desk-style summary metrics.
    Requires: pnl_equity, execution_pnl, notional, position, trade_qty
    """
    total_pnl = float(df["pnl_equity"].iloc[-1])
    total_exec = float(df["execution_pnl"].sum())
    total_notional = float(df["notional"].sum()) if "notional" in df else 0.0

    exec_bps = float(1e4 * (total_exec / total_notional)) if total_notional > 0 else 0.0

    return {
        "Total PnL": total_pnl,
        "Execution PnL": total_exec,
        "Execution (bps)": exec_bps,
        "Turnover (notional)": total_notional,
        "Max |Position|": float(df["position"].abs().max()),
        "Trades": int((df["trade_qty"] != 0).sum()),
        "PnL identity check (last pnl_diff)": float(df["pnl_diff"].iloc[-1]),
    }
