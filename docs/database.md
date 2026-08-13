# Phase 5 — SQL Database Integration

## Purpose

The cleaned customer dataset is loaded into a PostgreSQL `customers` table so downstream analytics and ML workflows can query a durable relational data source.

## Schema

The table preserves the customer identifier and business fields from the supplied CSV:

- `customer_id`
- `age`
- `gender`
- `tenure`
- `usage_frequency`
- `support_calls`
- `payment_delay`
- `subscription_type`
- `contract_length`
- `total_spend`
- `last_interaction`
- `churn`

## Local setup

1. Start PostgreSQL using the project's Docker Compose setup.
2. Install dependencies with `pip install -r requirements.txt`.
3. Set `DATABASE_URL` if your credentials differ from the local default.
4. Run:

```bash
python -m src.database.loader
```

## Design decision

The database stores the cleaned Phase 3 dataset. Raw CSV files remain in `data/raw`, while SQL is used for persistent analytics and later model-serving workflows.

The ML train/test split is not performed in this phase; that belongs to model development.
