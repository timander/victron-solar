#!/bin/bash
# build.sh - Compile COBOL program inside container
set -e

echo "======================================"
echo "Building GnuCOBOL Solar Cost Analysis"
echo "======================================"

# Build the container image
echo "Building container image..."
podman build -t victron-cobol:latest -f Containerfile .

echo ""
echo "Compiling COBOL source..."

# Compile the COBOL program inside a temporary container
mkdir -p ./output
podman run --rm \
    -v "$(pwd)/src:/app/src:ro" \
    -v "$(pwd)/output:/app/bin:rw" \
    victron-cobol:latest \
    cobc -x -o /app/bin/SOLARCOST /app/src/SOLARCOST.cbl

echo ""
echo "✓ Build complete!"
echo "✓ Executable: ./output/SOLARCOST"
echo ""
echo "Usage: ./scripts/run.sh"
