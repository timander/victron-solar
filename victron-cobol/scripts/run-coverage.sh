#!/bin/bash
# run-coverage.sh - Execute COBOL program and collect coverage data
set -e

echo "======================================"
echo "Running with Coverage Collection"
echo "======================================"

# Check if executable exists
if [ ! -f "./output/SOLARCOST" ]; then
    echo "ERROR: Coverage-enabled executable not found."
    echo "Please run ./scripts/build-coverage.sh first."
    exit 1
fi

# Run the compiled COBOL program in container with coverage collection
# Mount output directory as working directory so .gcda files are written there
# Set GCOV environment variables to ensure coverage data is captured
podman run --rm \
    -v "$(pwd)/../data:/app/data:ro" \
    -v "$(pwd)/output:/app/output:rw" \
    -w /app/output \
    -e CSV_INPUT=/app/data/SolarHistory.csv \
    -e REPORT_OUTPUT=/app/output/solar_cost_report.txt \
    -e GCOV_PREFIX=/app/output \
    -e GCOV_PREFIX_STRIP=3 \
    victron-cobol:latest \
    /app/output/SOLARCOST

echo ""
echo "✓ Program completed with coverage data"
echo "✓ Coverage files: ./output/*.gcda"
echo ""
echo "Generate HTML report: ./scripts/generate-coverage-report.sh"
