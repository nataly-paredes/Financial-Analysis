# Power BI DAX Measures — Financial Performance Analyzer

---

## Page 1: P&L Summary

### Gross Margin %
```dax
Gross Margin % =
DIVIDE(SUM(pl_data[gross_profit]), SUM(pl_data[revenue]), 0) * 100
```

### YoY Revenue Variance (%)
```dax
Revenue YoY % =
VAR CurrentRevenue = CALCULATE(SUM(pl_data[revenue]), DATESYTD(pl_data[month]))
VAR PriorRevenue   = CALCULATE(SUM(pl_data[revenue]), DATESYTD(SAMEPERIODLASTYEAR(pl_data[month])))
RETURN
    DIVIDE(CurrentRevenue - PriorRevenue, PriorRevenue, 0) * 100
```

### YoY Revenue Variance ($)
```dax
Revenue YoY $ =
VAR CurrentRevenue = CALCULATE(SUM(pl_data[revenue]), DATESYTD(pl_data[month]))
VAR PriorRevenue   = CALCULATE(SUM(pl_data[revenue]), DATESYTD(SAMEPERIODLASTYEAR(pl_data[month])))
RETURN CurrentRevenue - PriorRevenue
```

### EBITDA Margin %
```dax
EBITDA Margin % =
DIVIDE(SUM(pl_data[ebitda]), SUM(pl_data[revenue]), 0) * 100
```

### Net Margin %
```dax
Net Margin % =
DIVIDE(SUM(pl_data[net_income]), SUM(pl_data[revenue]), 0) * 100
```

### Margin Status Flag
> Drives conditional formatting on margin KPI cards.
```dax
Gross Margin Status =
IF([Gross Margin %] >= 35, "Healthy", IF([Gross Margin %] >= 30, "Watch", "Critical"))
```

---

## Page 2: Cost Center Variance

### Budget Variance ($)
```dax
Budget Variance $ =
SUM(budget_data[actual]) - SUM(budget_data[budget])
```

### Budget Variance (%)
```dax
Budget Variance % =
DIVIDE(
    SUM(budget_data[actual]) - SUM(budget_data[budget]),
    SUM(budget_data[budget]),
    0
) * 100
```

### Over Budget Flag
```dax
Over Budget =
IF([Budget Variance $] > 0, "Over Budget", "On Budget")
```

### Cost Centers Over Budget Count
```dax
Cost Centers Over Budget =
CALCULATE(
    DISTINCTCOUNT(budget_data[cost_center]),
    budget_data[over_budget] = TRUE()
)
```

---

## Page 3: Margin Analysis

### Rolling 3-Month Gross Margin
```dax
Gross Margin 3M Rolling =
CALCULATE(
    [Gross Margin %],
    DATESINPERIOD(pl_data[month], LASTDATE(pl_data[month]), -3, MONTH)
)
```

### Gross Margin Change vs Prior Year (pts)
```dax
Gross Margin YoY Pts =
VAR CurrentMargin = CALCULATE([Gross Margin %], DATESYTD(pl_data[month]))
VAR PriorMargin   = CALCULATE([Gross Margin %], DATESYTD(SAMEPERIODLASTYEAR(pl_data[month])))
RETURN CurrentMargin - PriorMargin
```

### COGS as % of Revenue
```dax
COGS Ratio % =
DIVIDE(SUM(pl_data[cogs]), SUM(pl_data[revenue]), 0) * 100
```

---

## Page 5: Forecast

### Blended Revenue (Actual + Forecast)
> Combines actuals with forecast_results table for continuous line chart.
```dax
Blended Revenue =
IF(
    ISBLANK(SUM(pl_data[revenue])),
    SUM(forecast_results[revenue_forecast]),
    SUM(pl_data[revenue])
)
```

### Projected Savings from Recommendations
```dax
Projected Annual Savings =
VAR FreightSavings  = 420000
VAR OvertimeSavings = 180000
VAR SGASavings      = SUM(pl_data[revenue]) * 0.015  -- 1.5 pt margin recovery
RETURN FreightSavings + OvertimeSavings + SGASavings
```
