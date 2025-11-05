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

# Capture coverage information and produce gcov output inside the container
podman run --rm \
    -v "$(pwd)/output:/app/output:rw" \
    -v "$(pwd)/src:/app/src:ro" \
    -v "$(pwd)/coverage:/app/coverage:rw" \
    -w /app/output \
    victron-cobol:latest \
    bash -c "
        lcov --capture \
             --directory . \
             --output-file /app/coverage/coverage.info \
             2>/dev/null || true

        gcov -ablp -o . SOLARCOST.c >/dev/null 2>&1 || true

        lcov --summary /app/coverage/coverage.info 2>/dev/null || \
            echo 'Coverage data collected'
    "

# Render COBOL-first HTML (and JSON) using the gcov output
python3 ./scripts/render-cobol-coverage.py \
    --gcov ./output/SOLARCOST.c.gcov \
    --source ./src/SOLARCOST.cbl \
    --output ./coverage/html/index.html \
    --json ./coverage/cobol-coverage.json \
    --title "COBOL Solar Cost Analysis Coverage"

echo ""
echo "✓ Coverage report generated!"
echo "✓ HTML report: ./coverage/html/index.html"
echo "✓ JSON snapshot: ./coverage/cobol-coverage.json"
echo ""
echo "Open with: open ./coverage/html/index.html"
