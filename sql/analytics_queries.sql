-- Phase 5: baseline SQL analytics

-- Overall churn rate
SELECT
    ROUND(AVG(churn)::numeric * 100, 2) AS churn_rate_pct
FROM customers;

-- Churn count by contract length
SELECT
    contract_length,
    COUNT(*) AS customers,
    SUM(churn) AS churned_customers,
    ROUND(AVG(churn)::numeric * 100, 2) AS churn_rate_pct
FROM customers
GROUP BY contract_length
ORDER BY churn_rate_pct DESC;

-- Churn by subscription type
SELECT
    subscription_type,
    COUNT(*) AS customers,
    SUM(churn) AS churned_customers,
    ROUND(AVG(churn)::numeric * 100, 2) AS churn_rate_pct
FROM customers
GROUP BY subscription_type
ORDER BY churn_rate_pct DESC;

-- Support-call bands
SELECT
    CASE
        WHEN support_calls <= 2 THEN '0-2'
        WHEN support_calls <= 5 THEN '3-5'
        WHEN support_calls <= 8 THEN '6-8'
        ELSE '9+'
    END AS support_call_band,
    COUNT(*) AS customers,
    ROUND(AVG(churn)::numeric * 100, 2) AS churn_rate_pct
FROM customers
GROUP BY support_call_band
ORDER BY support_call_band;
