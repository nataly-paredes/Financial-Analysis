"""
generate_mock_data.py
Generates synthetic P&L and budget data for the Financial Performance Analyzer.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

np.random.seed(7)

MONTHS = pd.date_range("2022-01-01", "2023-12-31", freq="MS")

BUSINESS_UNITS = ["Northeast Distribution", "Southeast Distribution",
                  "Mid-Atlantic Distribution", "Midwest Distribution"]

COST_CENTERS = {
    "Labor - Regular":   {"budget_base": 280000, "overrun_factor": 1.00},
    "Labor - Overtime":  {"budget_base":  45000, "overrun_factor": 1.38},  # problem
    "Freight":           {"budget_base": 190000, "overrun_factor": 1.31},  # problem
    "Facilities":        {"budget_base":  95000, "overrun_factor": 1.12},  # problem
    "Technology":        {"budget_base":  40000, "overrun_factor": 0.97},
    "SG&A":              {"budget_base": 130000, "overrun_factor": 1.11},
    "Maintenance":       {"budget_base":  30000, "overrun_factor": 0.99},
    "Other OpEx":        {"budget_base":  25000, "overrun_factor": 1.02},
}


def generate_pl_data():
    records = []
    for month in MONTHS:
        for bu in BUSINESS_UNITS:
            # Revenue grows ~8% YoY with seasonality
            base_revenue = 1_200_000
            yoy_growth = 1.08 if month.year == 2023 else 1.0
            seasonality = 1 + 0.12 * np.sin((month.month - 3) * np.pi / 6)
            noise = np.random.normal(1.0, 0.03)
            revenue = base_revenue * yoy_growth * seasonality * noise

            # COGS grows faster (13% YoY) — margin squeeze
            cogs_ratio_base = 0.62
            cogs_growth = 1.13 if month.year == 2023 else 1.0
            cogs = revenue * cogs_ratio_base * cogs_growth * np.random.normal(1.0, 0.02)

            gross_profit = revenue - cogs

            # OpEx by cost center
            total_opex = 0
            for cc, cfg in COST_CENTERS.items():
                budget = cfg["budget_base"]
                # Overtime and freight spike Q3-Q4
                seasonal_factor = 1.0
                if cc in ["Labor - Overtime", "Freight"] and month.month in [7, 8, 9, 10, 11, 12]:
                    seasonal_factor = 1.25
                actual = budget * cfg["overrun_factor"] * seasonal_factor * np.random.normal(1.0, 0.04)
                total_opex += actual

            ebitda = gross_profit - total_opex
            net_income = ebitda * np.random.normal(0.82, 0.02)  # taxes/interest

            records.append({
                "month":            month.strftime("%Y-%m"),
                "year":             month.year,
                "quarter":          f"Q{month.quarter}",
                "business_unit":    bu,
                "revenue":          round(revenue, 0),
                "cogs":             round(cogs, 0),
                "gross_profit":     round(gross_profit, 0),
                "gross_margin_pct": round((gross_profit / revenue) * 100, 2),
                "total_opex":       round(total_opex, 0),
                "ebitda":           round(ebitda, 0),
                "ebitda_margin_pct": round((ebitda / revenue) * 100, 2),
                "net_income":       round(net_income, 0),
                "net_margin_pct":   round((net_income / revenue) * 100, 2),
            })

    df = pd.DataFrame(records)
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/pl_data_raw.csv", index=False)
    print(f"✅ P&L data: {len(df)} rows → data/raw/pl_data_raw.csv")
    return df


def generate_budget_data():
    records = []
    for month in MONTHS:
        for bu in BUSINESS_UNITS:
            for cc, cfg in COST_CENTERS.items():
                budget = cfg["budget_base"] * np.random.normal(1.0, 0.01)
                actual = budget * cfg["overrun_factor"] * np.random.normal(1.0, 0.04)
                if cc in ["Labor - Overtime", "Freight"] and month.month in [7,8,9,10,11,12]:
                    actual *= 1.25
                variance = actual - budget
                records.append({
                    "month":         month.strftime("%Y-%m"),
                    "year":          month.year,
                    "quarter":       f"Q{month.quarter}",
                    "business_unit": bu,
                    "cost_center":   cc,
                    "budget":        round(budget, 0),
                    "actual":        round(actual, 0),
                    "variance":      round(variance, 0),
                    "variance_pct":  round((variance / budget) * 100, 2),
                    "over_budget":   actual > budget,
                })

    df = pd.DataFrame(records)
    df.to_csv("data/raw/budget_targets.csv", index=False)
    print(f"✅ Budget data: {len(df)} rows → data/raw/budget_targets.csv")
    return df


if __name__ == "__main__":
    pl = generate_pl_data()
    bud = generate_budget_data()

    print("\n📊 P&L Summary by Year:")
    print(pl.groupby("year")[["revenue","gross_profit","ebitda","net_income"]].sum().applymap(lambda x: f"${x:,.0f}"))

    print("\n📊 Over-budget cost centers (2023):")
    over = bud[bud["year"] == 2023].groupby("cost_center").agg(
        budget=("budget","sum"), actual=("actual","sum")
    )
    over["variance_pct"] = ((over["actual"] - over["budget"]) / over["budget"] * 100).round(1)
    print(over.sort_values("variance_pct", ascending=False).to_string())
