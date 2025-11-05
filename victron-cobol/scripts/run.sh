#!/bin/bash
# run.sh - Execute COBOL program in container
set -e

echo "======================================"
echo "Running Solar Cost Analysis (COBOL)"
echo "======================================"

# Check if executable exists
if [ ! -f "./output/SOLARCOST" ]; then
    echo "ERROR: SOLARCOST executable not found."
    echo "Please run ./scripts/build.sh first."
    exit 1
fi

# Run the compiled COBOL program in container with volume mounts
mkdir -p ./output
podman run --rm \
    -v "$(pwd)/../data:/app/data:ro" \
    -v "$(pwd)/output:/app/output:rw" \
    -e CSV_INPUT=/app/data/SolarHistory.csv \
    -e REPORT_OUTPUT=/app/output/solar_cost_report.txt \
    victron-cobol:latest \
    /app/output/SOLARCOST

echo ""
echo "✓ Program completed"
echo "✓ Report: ./output/solar_cost_report.txt"
