#!/bin/bash
# build-coverage.sh - Compile COBOL program with coverage instrumentation
set -e

echo "======================================"
echo "Building with Coverage Instrumentation"
echo "======================================"

# Build the container image (if not exists)
echo "Ensuring container image exists..."
podman build -t victron-cobol:latest -f Containerfile . 2>&1 | grep -E "(STEP|Successfully tagged)" || true

echo ""
echo "Compiling COBOL with --coverage flag..."

# Clean old coverage data
rm -f ./output/*.gcda ./output/*.gcno ./output/*.gcov

# Compile with coverage instrumentation
# -A passes flags to C compiler: -fprofile-arcs -ftest-coverage for gcov
# -save-temps keeps .gcno file needed for coverage
# Work in /app/bin so .gcno is created in output directory
podman run --rm \
    -v "$(pwd)/src:/app/src:ro" \
    -v "$(pwd)/output:/app/bin:rw" \
    -w /app/bin \
    victron-cobol:latest \
    cobc -x \
         -g \
         -fdebugging-line \
         -A "-fprofile-arcs -ftest-coverage" \
         -Q "-lgcov" \
         -save-temps \
         -o /app/bin/SOLARCOST \
         /app/src/SOLARCOST.cbl

echo ""
echo "✓ Coverage-enabled build complete!"
echo "✓ Executable: ./output/SOLARCOST (with coverage instrumentation)"
echo ""
echo "Run with: ./scripts/run-coverage.sh"
