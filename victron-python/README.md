# Victron Python Module

Modern Python pipeline for solar cost analysis using Polars, Pydantic, and pytest.

## Tech Stack

- **Python 3.11+** with type hints
- **Polars** - Fast DataFrame processing
- **Pydantic** - Data validation
- **Pytest** - Testing (95%+ coverage)
- **Ruff** - Linting and formatting
- **Mypy** - Static type checking

## Quick Start

```bash
# Install dependencies
make install

# Generate cost analysis report
make run

# Run tests
make test

# Generate visualization
make dashboard
```

## Makefile Targets

| Target | Description |
|--------|-------------|
| `install` | Setup venv and install dependencies |
| `test` | Run pytest suite |
| `lint` | Check code with ruff |
| `format` | Auto-format code |
| `type-check` | Validate types with mypy |
| `run` | Generate cost analysis report |
| `dashboard` | Create visualization dashboard |
| `clean` | Remove cache and output artifacts |

## Architecture

```
src/
├── models.py          # Pydantic data models
├── pipeline.py        # Data ingestion
├── cost_analysis.py   # Financial calculations
├── data_quality.py    # Validation
└── visualization.py   # Matplotlib charts

tests/
├── test_pipeline.py
├── test_cost_analysis.py
└── test_models.py
```

## Output

All generated files go to `output/`:
- `output/solar_cost_report.txt` - Cost analysis report
- `output/solar_dashboard.png` - Visualization dashboard

## Development

```bash
# Run full build
make build

# Test with coverage
make test

# Format and lint
make format
make lint
```

---

**See [../README.md](../README.md) for project overview**
