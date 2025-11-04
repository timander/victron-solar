.PHONY: help build run clean test

.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "COBOL Solar Cost Analysis - Make targets:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Build container image and compile COBOL program
	@./scripts/build.sh

run: ## Execute COBOL program in container
	@./scripts/run.sh

report: build run ## Build and run to generate cost report
	@echo ""
	@echo "Report generated successfully:"
	@cat ./output/solar_cost_report.txt

clean: ## Remove compiled artifacts and output files
	@echo "Cleaning artifacts..."
	@rm -f ./output/SOLARCOST
	@rm -f ./output/*.txt
	@echo "✓ Clean complete"

test: run ## Run program and verify output exists
	@if [ -f ./output/solar_cost_report.txt ]; then \
		echo "✓ Test passed: Report generated"; \
		wc -l ./output/solar_cost_report.txt; \
	else \
		echo "✗ Test failed: No report generated"; \
		exit 1; \
	fi
