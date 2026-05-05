"""
forecasting.py
2-quarter revenue and cost forecast using statsmodels (Holt-Winters).
Falls back to linear trend if statsmodels not available.
Outputs forecast_results.csv and forecast charts.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = "python/eda_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

BLUE   = "#1F4E79"
ORANGE = "#C55A11"
GRAY   = "#AAAAAA"


def load_data():
    df = pd.read_csv("data/cleaned/pl_data_clean.csv")
    monthly = df.groupby("month").agg(
        revenue=("revenue", "sum"),
        cogs=("cogs", "sum"),
        total_opex=("total_opex", "sum"),
        gross_profit=("gross_profit", "sum"),
        net_income=("net_income", "sum"),
    ).reset_index()
    monthly["month"] = pd.to_datetime(monthly["month"])
    monthly = monthly.sort_values("month").reset_index(drop=True)
    return monthly


def linear_forecast(series, n_periods=6):
    """Simple linear regression forecast as fallback."""
    x = np.arange(len(series))
    coeffs = np.polyfit(x, series.values, 1)
    future_x = np.arange(len(series), len(series) + n_periods)
    forecast = np.polyval(coeffs, future_x)
    return forecast


def holt_winters_forecast(series, n_periods=6):
    """Exponential smoothing forecast."""
    try:
        from statsmodels.tsa.holtwinters import ExponentialSmoothing
        model = ExponentialSmoothing(series, trend="add", seasonal="add",
                                     seasonal_periods=12).fit(optimized=True)
        return model.forecast(n_periods).values
    except Exception:
        print("statsmodels not available — using linear trend fallback.")
        return linear_forecast(series, n_periods)


def run_forecast(monthly):
    N = 6  # 2 quarters forward

    future_months = pd.date_range(
        monthly["month"].iloc[-1] + pd.DateOffset(months=1),
        periods=N, freq="MS"
    )

    results = {"month": future_months}
    for col in ["revenue", "total_opex", "gross_profit"]:
        results[f"{col}_forecast"] = holt_winters_forecast(monthly[col], N)

    forecast_df = pd.DataFrame(results)
    forecast_df.to_csv("data/cleaned/forecast_results.csv", index=False)
    print(f"✅ Forecast saved → data/cleaned/forecast_results.csv")
    return forecast_df


def plot_forecast(monthly, forecast_df):
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle("2-Quarter Forward Forecast", fontsize=14, fontweight="bold", color=BLUE)

    metrics = [
        ("revenue", "revenue_forecast", "Revenue ($)", BLUE),
        ("total_opex", "total_opex_forecast", "Total OpEx ($)", ORANGE),
        ("gross_profit", "gross_profit_forecast", "Gross Profit ($)", BLUE),
    ]

    for ax, (hist_col, fc_col, title, color) in zip(axes, metrics):
        # Historical
        ax.plot(monthly["month"], monthly[hist_col],
                color=color, linewidth=2, label="Actual")
        # Forecast
        ax.plot(forecast_df["month"], forecast_df[fc_col],
                color=color, linewidth=2, linestyle="--", label="Forecast")
        # Confidence band (±5%)
        fc_vals = forecast_df[fc_col].values
        ax.fill_between(forecast_df["month"],
                         fc_vals * 0.95, fc_vals * 1.05,
                         alpha=0.15, color=color, label="±5% band")
        ax.axvline(monthly["month"].iloc[-1], color=GRAY, linestyle=":", linewidth=1)
        ax.set_title(title, fontsize=10, color=BLUE)
        ax.legend(fontsize=8)
        ax.tick_params(axis="x", rotation=45, labelsize=7)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))

    plt.tight_layout()
    path = f"{OUTPUT_DIR}/06_forecast.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path}")


def plot_margin_trend(monthly):
    monthly["gross_margin_pct"] = (monthly["gross_profit"] / monthly["revenue"] * 100).round(2)
    monthly["net_margin_pct"] = (monthly["net_income"] / monthly["revenue"] * 100).round(2)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(monthly["month"], monthly["gross_margin_pct"],
            color=BLUE, linewidth=2, marker="o", markersize=3, label="Gross Margin %")
    ax.plot(monthly["month"], monthly["net_margin_pct"],
            color=ORANGE, linewidth=2, marker="o", markersize=3, label="Net Margin %")
    ax.axhline(monthly["gross_margin_pct"].iloc[:12].mean(),
               color=BLUE, linestyle="--", alpha=0.4, label="2022 Gross Margin Avg")
    ax.set_title("Margin Erosion Over Time", fontsize=13, fontweight="bold", color=BLUE)
    ax.set_ylabel("Margin (%)")
    ax.legend()
    ax.tick_params(axis="x", rotation=45)

    path = f"{OUTPUT_DIR}/07_margin_trend.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path}")


if __name__ == "__main__":
    monthly = load_data()
    forecast_df = run_forecast(monthly)
    plot_forecast(monthly, forecast_df)
    plot_margin_trend(monthly)
    print("\n✅ Forecasting complete.")
