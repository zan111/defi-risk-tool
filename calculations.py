# ------------------------- calculations.py -------------------------
# Refactored, pure functions without Streamlit dependencies
import pandas as pd
import numpy as np


def general_calc(df_total):
    df_total["Price"] = pd.to_numeric(df_total["Price"], errors="coerce").fillna(0)
    df_total["liquidationThreshold"] = pd.to_numeric(df_total["liquidationThreshold"], errors="coerce").fillna(0)
    df_total["Amount"] = pd.to_numeric(df_total["Amount"], errors="coerce").fillna(0)
    
    df_total["Total_Value"] = df_total["Price"] * df_total["Amount"]
    df_total["Total_Value_Adjusted_Collateral"] = df_total["Total_Value"] * df_total["liquidationThreshold"]
    
    return df_total


def calculate_hf(df_total: pd.DataFrame):
    if df_total is None or df_total.empty:
        return None
    borrow_amount_total = df_total.loc[df_total['Type']=='Borrow','Total_Value'].sum()
    if borrow_amount_total == 0:
        return float('inf')
    amount_total_collateral_adjusted = df_total.loc[df_total['Type']=='Deposit','Total_Value_Adjusted_Collateral'].sum()
    health_factor = amount_total_collateral_adjusted / borrow_amount_total
    return round(float(health_factor), 3)


def hf_ratio_description(health_factor):
    if health_factor is None:
        return "No data"
    if health_factor == float('inf'):
        return "🟢 No borrows — fully safe."
    if health_factor > 2:
        return f"🟢 Health Factor: {health_factor} — Safe"
    elif 1.2 <= health_factor <= 2:
        return f"⚠️ Health Factor: {health_factor} — Warning"
    else:
        return f"🔴 Health Factor: {health_factor} — Critical"


def calculate_ltv(df_total: pd.DataFrame):
    if df_total is None or df_total.empty:
        return None
    borrow_amount_total = df_total.loc[df_total['Type']=='Borrow','Total_Value'].sum()
    supplied_total = df_total.loc[df_total['Type']=='Deposit','Total_Value'].sum()
    if supplied_total == 0:
        return None
    return round(float(borrow_amount_total / supplied_total), 3)


def stress_test_calculation_multiple(df, stress_inputs):
    df_stressed = df.copy()
    prices = {}

    for key, pct in stress_inputs.items():
        typ, coin = key.split("-")
        idx = df_stressed["symbol"] == coin
        old_price = df_stressed.loc[idx, "Price"].values[0]
        new_price = old_price * (1 - pct/100)
        df_stressed.loc[idx, "Price"] = new_price
        prices[coin] = {"old": old_price, "new": new_price}

    # Recalculate totals after price adjustments
    df_stressed = general_calc(df_stressed)

    return df_stressed, prices



def evaluate_row_risk(row, price_changes, hf_global):
    """
    Returns True if this row should be highlighted as risky.
    Conditions:
    - If HF < 1 after stress → everything is risky.
    - If asset price dropped > 20% (or custom threshold).
    - If deposit collateral has very low adjusted collateral value.
    - If borrow value compared to collateral pushes LTV high.
    """
    symbol = row.get("Coin")
    amount = float(row.get("Amount") or 0)

    # Global HF rule
    if hf_global is not None and hf_global < 1:
        return True

    # Price drop rule
    if symbol in price_changes:
        before, after = price_changes[symbol]
        if before > 0 and (before - after) / before > 0.20:  # 20% drop
            return True

    # Collateral rule (deposits table)
    if "Adjusted_Collateral_Value" in row:
        if float(row["Adjusted_Collateral_Value"]) < 1:
            return True

    # Loan rule (borrows table)
    if "Borrow_Value" in row and "Total_Collateral" in row:
        ltv = row["Borrow_Value"] / row["Total_Collateral"] if row["Total_Collateral"] > 0 else 0
        if ltv > 0.60:  # high LTV
            return True

    return False




