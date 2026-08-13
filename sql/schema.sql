-- Phase 5: Customer churn database schema
-- PostgreSQL

CREATE TABLE IF NOT EXISTS customers (
    customer_id BIGINT PRIMARY KEY,
    age INTEGER,
    gender VARCHAR(50),
    tenure INTEGER,
    usage_frequency INTEGER,
    support_calls INTEGER,
    payment_delay INTEGER,
    subscription_type VARCHAR(50),
    contract_length VARCHAR(50),
    total_spend NUMERIC(14, 2),
    last_interaction INTEGER,
    churn SMALLINT NOT NULL CHECK (churn IN (0, 1))
);

CREATE INDEX IF NOT EXISTS idx_customers_churn
    ON customers (churn);

CREATE INDEX IF NOT EXISTS idx_customers_subscription_type
    ON customers (subscription_type);

CREATE INDEX IF NOT EXISTS idx_customers_contract_length
    ON customers (contract_length);

CREATE INDEX IF NOT EXISTS idx_customers_tenure
    ON customers (tenure);
