# 💰 Financial Performance & Profitability Analyzer
### P&L Analysis, Cost Center Identification & Forecasting | SQL + Python + Power BI

---

## 📖 The Business Story

A mid-size logistics and distribution company had a profitability problem, revenue was growing at 8% YoY, but **net margin was shrinking**. Leadership knew something was wrong but couldn't pinpoint where.

As the Data Analyst on this engagement, I was asked to:
1. Analyze P&L data across business units and cost centers
2. Identify where margin erosion was happening and why
3. Build a financial dashboard that told the story clearly, not just what happened, but what it means and what to do about it
4. Forecast the next two quarters using historical trend data

---

## 🔍 Pain Points Identified

| Finding | Detail |
|---|---|
| Gross margin declined 4.2 pts over 12 months | Revenue up 8%, but COGS grew 13% |
| 3 of 8 cost centers operating above budget | Facilities, Labor (Overtime), and Freight |
| Freight costs up 31% YoY | Carrier mix shifted to spot rates during peak season |
| Labor overtime surged Q3–Q4 | Tied to understaffing + demand spike, not planned |
| SG&A growing faster than revenue | 11% growth vs. 8% revenue growth |

---

## 💡 Recommendations & Projected Impact

| Recommendation | Projected Savings / Impact |
|---|---|
| Renegotiate carrier contracts, reduce spot rate reliance | $420K annual freight savings |
| Implement demand-based labor scheduling | $180K overtime cost reduction |
| Freeze non-essential SG&A until margin recovers | 1.5 pt margin recovery within 2 quarters |
| Monthly cost center variance reviews with accountability | Prevent budget overruns earlier |

---

## 📁 Project Structure

```
project2-financial-analyzer/
│
├── data/
│   ├── raw/
│   │   ├── pl_data_raw.csv                    # Mock P&L records
│   │   └── budget_targets.csv                 # Budget vs. actual targets
│   └── cleaned/
│       └── pl_data_clean.csv
│
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_data_quality_checks.sql
│   ├── 03_pl_analysis.sql                     # P&L breakdown queries
│   ├── 04_cost_center_variance.sql            # Budget vs. actual analysis
│   └── 05_margin_trend.sql                    # Margin erosion over time
│
├── python/
│   ├── generate_mock_data.py
│   ├── data_cleaning.py
│   ├── eda_analysis.py
│   └── forecasting.py                         # Prophet-based revenue + cost forecast
│
├── powerbi/
│   ├── dax_measures.md
│   └── dashboard_screenshots/
│
└── README.md
```

---

## 🛠️ Tools & Technologies

- **SQL Server**, P&L queries, variance analysis, window functions
- **Python (pandas, matplotlib, Prophet)**, EDA, trend analysis, forecasting
- **Power BI + DAX**, financial dashboard, waterfall charts, forecast visuals
- **DAX**, YoY variance, running totals, cost center budget flags

---

## 📊 Dashboard Pages

1. **P&L Summary**, Revenue, COGS, Gross Profit, EBITDA with YoY comparison
2. **Cost Center Drill-Down**, Budget vs. Actual by cost center with variance flags
3. **Margin Analysis**, Gross and net margin trend with contributing factors
4. **Freight & Labor Deep Dive**, The two biggest cost drivers analyzed in detail
5. **2-Quarter Forecast**, Revenue and cost forecast with confidence intervals

---

## 🔑 Key DAX Measures

See [`powerbi/dax_measures.md`](powerbi/dax_measures.md) for full documentation.

Highlights:
- `Gross Margin %`, dynamic with time intelligence
- `YoY Revenue Variance`, % and absolute change
- `Budget Variance`, actual vs. budget with over/under flag
- `Running Total Cost`, cumulative cost by month for waterfall
- `Forecast Revenue`, blended actual + forecasted value

---

## 📈 Key Outcomes (Simulated)

- Identified **$600K+ in avoidable costs** across freight and overtime
- Dashboard replaced monthly manual Excel P&L reports (**~20 hrs/month saved**)
- Margin forecast accuracy within **±1.2 pts** over validation period
- Cost center accountability improved, **2 of 3 over-budget centers corrected** within 60 days of dashboard deployment

---

## 🚀 How to Run

```bash
# 1. Generate mock P&L data
python python/generate_mock_data.py

# 2. Clean and enrich data
python python/data_cleaning.py

# 3. Run EDA
python python/eda_analysis.py

# 4. Run forecast model
python python/forecasting.py

# 5. Load into SQL and run queries 01 → 05
# 6. Connect Power BI to cleaned CSV or SQL Server
```

---

*This project uses fully synthetic data generated for portfolio demonstration purposes.*
