# Phase 12 — Testing & CI/CD

## Test layers

### Unit tests

Validate deterministic business logic such as risk-tier classification and intervention rules.

```bash
pytest tests/unit -q
```

### API tests

Validate FastAPI endpoints without requiring a live server.

```bash
pytest tests/api -q
```

### Full test suite

```bash
pytest -q
```

## CI

GitHub Actions runs on pushes and pull requests targeting `main`.

The workflow:

1. Checks out the repository.
2. Installs Python 3.12.
3. Installs project dependencies.
4. Runs the project structure/compilation check.
5. Runs the pytest suite.

## Important limitation

The CI workflow tests application logic and the API health endpoint. It does not retrain the ML models on every commit. Model training is computationally heavier and should be handled by a dedicated training/release workflow when needed.
