# Phase 11 — Productionization & Docker

## Services

| Service | Purpose | Port |
|---|---|---:|
| PostgreSQL | Persistent relational data | 5432 |
| FastAPI | Prediction API | 8000 |
| Streamlit | Retention dashboard | 8501 |

## Local Docker startup

From the project root:

```bash
docker compose build
docker compose up
```

API:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

Dashboard:

```text
http://localhost:8501
```

## Health check

```bash
curl http://localhost:8000/health
```

Expected:

```json
{"status":"ok"}
```

## Local non-Docker validation

```bash
sh scripts/check_project.sh
```

## Production limitations

This phase makes the project reproducible locally with containers. It does not claim full production readiness.

Still required for a real deployment:

- authentication and authorization
- HTTPS/TLS
- secrets management
- centralized logging
- metrics and alerting
- model registry/versioning
- CI/CD
- autoscaling
- backup and disaster recovery
- database migrations
- cloud deployment configuration
