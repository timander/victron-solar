.PHONY: help build run clean test coverage coverage-build coverage-run coverage-report coverage-clean

.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "COBOL Solar Cost Analysis - Make targets:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build container image and compile COBOL program
	@./scripts/build.sh

run: build ## Execute COBOL program in container (build if needed)
	@./scripts/run.sh

report: run ## Build and run to generate cost report
	@echo ""
	@echo "Report generated successfully:"
	@cat ./output/solar_cost_report.txt

coverage-build: ## Build COBOL program with coverage instrumentation
	@./scripts/build-coverage.sh

coverage-run: coverage-build ## Run coverage-enabled program and collect data (build if needed)
	@./scripts/run-coverage.sh

coverage-report: coverage-run ## Generate HTML coverage report (ensures coverage data exists)
	@./scripts/generate-coverage-report.sh

coverage: coverage-report ## Full coverage workflow: build, run, report
	@echo ""
	@echo "======================================"
	@echo "Coverage Analysis Complete!"
	@echo "======================================"
	@echo "View report: open ./coverage/html/index.html"

coverage-clean: ## Remove coverage data and reports
	@echo "Cleaning coverage data..."
	@rm -rf ./coverage
	@rm -f ./output/*.gcda ./output/*.gcno ./output/*.gcov
	@echo "✓ Coverage data cleaned"

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
