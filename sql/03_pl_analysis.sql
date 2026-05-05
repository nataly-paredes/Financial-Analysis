-- ============================================================
-- 03_pl_analysis.sql
-- P&L breakdown and margin analysis
-- ============================================================

-- ── Full P&L Summary by Year ──────────────────────────────────
SELECT
    year,
    ROUND(SUM(revenue), 0)                                      AS total_revenue,
    ROUND(SUM(cogs), 0)                                         AS total_cogs,
    ROUND(SUM(gross_profit), 0)                                 AS total_gross_profit,
    ROUND(AVG(gross_margin_pct), 2)                             AS avg_gross_margin_pct,
    ROUND(SUM(total_opex), 0)                                   AS total_opex,
    ROUND(SUM(ebitda), 0)                                       AS total_ebitda,
    ROUND(AVG(ebitda_margin_pct), 2)                            AS avg_ebitda_margin_pct,
    ROUND(SUM(net_income), 0)                                   AS total_net_income,
    ROUND(AVG(net_margin_pct), 2)                               AS avg_net_margin_pct
FROM pl_data
GROUP BY year
ORDER BY year;


-- ── YoY Revenue & Margin Variance ────────────────────────────
WITH yearly AS (
    SELECT
        year,
        SUM(revenue)        AS total_revenue,
        AVG(gross_margin_pct) AS gross_margin,
        AVG(net_margin_pct)   AS net_margin
    FROM pl_data
    GROUP BY year
)
SELECT
    curr.year,
    curr.total_revenue,
    ROUND((curr.total_revenue - prev.total_revenue) / prev.total_revenue * 100, 1) AS revenue_yoy_pct,
    ROUND(curr.gross_margin - prev.gross_margin, 2)             AS gross_margin_chg_pts,
    ROUND(curr.net_margin - prev.net_margin, 2)                 AS net_margin_chg_pts
FROM yearly curr
LEFT JOIN yearly prev ON curr.year = prev.year + 1
ORDER BY curr.year;


-- ── Monthly P&L Trend ─────────────────────────────────────────
SELECT
    month,
    ROUND(SUM(revenue), 0)              AS revenue,
    ROUND(SUM(gross_profit), 0)         AS gross_profit,
    ROUND(AVG(gross_margin_pct), 2)     AS gross_margin_pct,
    ROUND(SUM(ebitda), 0)               AS ebitda,
    ROUND(AVG(ebitda_margin_pct), 2)    AS ebitda_margin_pct,
    ROUND(SUM(net_income), 0)           AS net_income,
    -- Rolling 3-month avg margin
    ROUND(AVG(AVG(gross_margin_pct)) OVER (
        ORDER BY month
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2)                               AS rolling_3mo_gross_margin
FROM pl_data
GROUP BY month
ORDER BY month;


-- ── P&L by Business Unit (2023) ───────────────────────────────
SELECT
    business_unit,
    ROUND(SUM(revenue), 0)              AS revenue,
    ROUND(SUM(gross_profit), 0)         AS gross_profit,
    ROUND(AVG(gross_margin_pct), 2)     AS gross_margin_pct,
    ROUND(SUM(net_income), 0)           AS net_income,
    ROUND(AVG(net_margin_pct), 2)       AS net_margin_pct,
    RANK() OVER (ORDER BY AVG(net_margin_pct) DESC) AS margin_rank
FROM pl_data
WHERE year = 2023
GROUP BY business_unit
ORDER BY net_margin_pct DESC;


-- ── COGS Growth vs Revenue Growth ────────────────────────────
WITH monthly_totals AS (
    SELECT
        month,
        SUM(revenue)      AS revenue,
        SUM(cogs)         AS cogs
    FROM pl_data
    GROUP BY month
)
SELECT
    month,
    revenue,
    cogs,
    ROUND(cogs / revenue * 100, 2)                              AS cogs_ratio_pct,
    ROUND(LAG(revenue) OVER (ORDER BY month), 0)                AS prev_revenue,
    ROUND((revenue - LAG(revenue) OVER (ORDER BY month))
          / LAG(revenue) OVER (ORDER BY month) * 100, 1)        AS revenue_mom_pct,
    ROUND((cogs - LAG(cogs) OVER (ORDER BY month))
          / LAG(cogs) OVER (ORDER BY month) * 100, 1)           AS cogs_mom_pct
FROM monthly_totals
ORDER BY month;
