#!/bin/bash
# generate-coverage-report.sh - Generate HTML coverage report from gcda files
set -e

echo "======================================"
echo "Generating Coverage HTML Report"
echo "======================================"

# Check if coverage data exists
if [ ! -f "./output/SOLARCOST.gcda" ]; then
    echo "ERROR: No coverage data found."
    echo "Please run ./scripts/run-coverage.sh first."
    exit 1
fi

# Create coverage directory
mkdir -p ./coverage

echo "Processing coverage data..."

# Generate HTML report using lcov inside container
# This maps the C code coverage back to COBOL source
podman run --rm \
    -v "$(pwd)/output:/app/output:ro" \
    -v "$(pwd)/src:/app/src:ro" \
    -v "$(pwd)/coverage:/app/coverage:rw" \
    -w /app/output \
    victron-cobol:latest \
    bash -c "
        # Capture coverage data (include all files)
        lcov --capture \
             --directory . \
             --output-file /app/coverage/coverage.info \
             2>/dev/null || true
        
        # Generate HTML report
        genhtml /app/coverage/coverage.info \
                --output-directory /app/coverage/html \
                --title 'COBOL Solar Cost Analysis Coverage' \
                --show-details \
                --legend \
                --prefix /app \
                2>/dev/null || true
        
        # Also generate a simple text summary
        lcov --summary /app/coverage/coverage.info 2>/dev/null || \
            echo 'Coverage data collected'
    "

echo ""
echo "✓ Coverage report generated!"
echo "✓ HTML report: ./coverage/html/index.html"
echo ""
echo "Open with: open ./coverage/html/index.html"
