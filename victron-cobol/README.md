# Victron COBOL Module

Containerized COBOL implementation with GnuCOBOL 4 and coverage tooling featuring IBM 3270 mainframe styling.

## Tech Stack

- **GnuCOBOL 4** (COBOL-85/2002/2014 compliant)
- **Podman/Docker** containers
- **gcov/lcov** coverage tools
- **Python** custom coverage renderer

## Quick Start

```bash
# Build container and compile
make build

# Run program
make run

# View IBM 3270-styled coverage report
make coverage
open coverage/html/index.html
```

## Makefile Targets

| Target | Description |
|--------|-------------|
| `build` | Build container and compile COBOL |
| `run` | Execute program |
| `coverage` | Full coverage workflow |
| `coverage-build` | Compile with gcov instrumentation |
| `coverage-run` | Execute and collect coverage data |
| `coverage-report` | Generate HTML report |
| `coverage-clean` | Remove coverage artifacts |
| `clean` | Remove compiled artifacts |

## Architecture

```
src/
└── SOLARCOST.cbl     # Main program (580+ lines)

scripts/
├── build.sh                    # Standard build
├── build-coverage.sh           # Build with instrumentation
├── run.sh                      # Execute program
├── run-coverage.sh             # Execute with coverage
├── generate-coverage-report.sh # lcov + HTML generation
└── render-cobol-coverage.py    # Custom COBOL renderer

output/
├── SOLARCOST                   # Compiled executable
├── solar_cost_report.txt       # Generated report
└── *.gcda / *.gcno            # Coverage data files

coverage/
├── coverage.info               # lcov tracefile
├── cobol-coverage.json         # JSON snapshot
└── html/index.html            # IBM 3270-styled report
```

## Coverage Features

**IBM 3270 Terminal Styling:**
- Pure green-on-black color scheme
- IBM 3270 / IBM Plex Mono fonts
- Authentic mainframe aesthetics

**COBOL Syntax Highlighting:**
- Divisions (yellow): `IDENTIFICATION DIVISION`, `DATA DIVISION`
- Keywords (cyan): `PERFORM`, `MOVE`, `IF`, `SELECT`
- PIC clauses (orange): `PIC X(100)`, `PIC 9(5)V99`
- Comments (dim green): Lines starting with `*`

**Coverage Indicators:**
- **Covered** - Dark green background + green left border
- **Partial** - Dark amber background + yellow left border
- **Missed** - Dark red background + red left border
- **Non-executable** - Black background + gray left border

## COBOL Program Structure

```
SOLARCOST.cbl
├── IDENTIFICATION DIVISION
├── ENVIRONMENT DIVISION (file I/O)
├── DATA DIVISION
│   ├── FILE SECTION
│   └── WORKING-STORAGE
└── PROCEDURE DIVISION
    ├── 000-MAIN-CONTROL
    ├── 100-INITIALIZE-PROGRAM
    ├── 200-PROCESS-CSV-FILE
    ├── 300-CALCULATE-COSTS
    ├── 400-GENERATE-REPORT
    └── 900-CLEANUP-AND-EXIT
```

## Output

All generated files go to `output/` and `coverage/`:
- `output/solar_cost_report.txt` - Cost analysis report
- `coverage/html/index.html` - Coverage report with syntax highlighting
- `coverage/cobol-coverage.json` - Coverage data snapshot

## Development

```bash
# Make changes
vim src/SOLARCOST.cbl

# Rebuild and test
make clean && make build && make run

# Check coverage
make coverage
```

---

**See [../README.md](../README.md) for project overview**
