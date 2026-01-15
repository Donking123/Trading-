# Post-Trade PnL Decomposition & Execution Analysis (SPY)

This project implements a **post-trade analytics framework** for SPY that reconstructs trading ledger state and decomposes total PnL into **inventory**, **bid-ask spread**, **slippage**, and **transaction fee** components.

The objective is to diagnose strategy performance beyond headline returns by separating **market-driven PnL** from **execution-driven costs**, which is critical for high-turnover trading strategies.

---

## Motivation

In systematic trading, total PnL alone does not reveal whether performance is driven by:
- favorable market movements (inventory exposure), or
- execution quality and trading costs.

This project builds a post-trade framework to make these components explicit, enabling robust evaluation of strategy behavior and execution efficiency.

---

## Methodology

The framework follows a desk-style post-trade workflow:

1. **Ledger Reconstruction**
   - Track position, cash, and mark-to-market equity from executed trades
   - Ensure correct cash and fee accounting

2. **Execution Modeling**
   - Model bid–ask quotes around mid price
   - Allow bid–ask spreads to widen dynamically with short-term volatility
   - Apply per-trade transaction fees

3. **PnL Decomposition**
   - **Inventory PnL**: price movements on held positions  
   - **Execution PnL**, split into:
     - Bid–ask spread cost
     - Slippage relative to expected fills
     - Transaction fees

4. **Validation**
   - Enforce the PnL identity:
     > Equity-based PnL = Inventory PnL + Execution PnL
   - Verified via automated unit tests

---

## Execution Model

- **Instrument**: SPY (equity ETF)  
- **Prices**: mid prices with modeled bid–ask quotes  
- **Spreads**: widen as a function of recent price volatility  
- **Fees**: applied proportionally to trade notional  

This setup captures key execution frictions while remaining transparent and reproducible.

---

## Outputs

- Mark-to-market equity curve  
- Cumulative execution PnL (spread vs slippage vs fees)  
- Position and inventory exposure over time  
- Execution quality measured in **basis points (bps)**  
- Turnover and inventory-based risk proxies  
- PnL accounting consistency checks  

An interactive Plotly dashboard summarizes these results.

---
