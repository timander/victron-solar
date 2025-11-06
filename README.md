# Victron Solar: Polyglot Modernization Demo

A practical demonstration comparing modern Python with containerized COBOL for processing Victron MPPT solar charge controller data.

## Purpose

This project shows two approaches to the same problem:

1. **victron-python/** - Modern Python with Polars, Pydantic, and pytest
2. **victron-cobol/** - Legacy COBOL containerized with GnuCOBOL + coverage tooling

Both modules process `data/SolarHistory.csv` and generate equivalent cost analysis reports, demonstrating that legacy code can be modernized through containerization while preserving proven business logic.

## Structure

```
victron-solar/
├── data/SolarHistory.csv    # Solar panel CSV data
├── victron-python/          # Modern Python implementation
└── victron-cobol/           # Containerized COBOL implementation
```

## Quick Start

### Python Module
```bash
cd victron-python
make install    # Setup venv and dependencies
make run        # Generate cost analysis report
make test       # Run pytest suite
```

### COBOL Module
```bash
cd victron-cobol
make build      # Build container and compile
make run        # Generate cost analysis report
make coverage   # View IBM 3270-styled coverage report
```

## Key Insights

**When to containerize legacy code:**
- ✅ Complex, well-tested business logic
- ✅ Regulatory requirements for proven code
- ✅ Limited budget for full rewrite

**When to rewrite:**
- ✅ Requirements changed significantly
- ✅ Need modern APIs/microservices
- ✅ No legacy language expertise available

## Documentation

- **[victron-python/README.md](victron-python/README.md)** - Python pipeline details
- **[victron-cobol/README.md](victron-cobol/README.md)** - COBOL containerization and coverage

---

**Purpose**: Educational demonstration of legacy modernization strategies  
**Author**: Tim Anderson | November 2025
