# CSV path variable (override with `make run CSV=path/to/file.csv`)
CSV ?= ../data/SolarHistory.csv
# Set help as the default task
.DEFAULT_GOAL := help

# If using pyenv, ensure the correct Python version is selected before running 'make env'.
# Example: pyenv shell 3.13.9
.PHONY: help install env deactivate build test lint format type-check run viz clean

# Usage: make <target>
#
# Targets:
#   help        Show this help message
#   install     Install dependencies (in venv)
#   env         Create and activate Python venv (if not exists)
#   deactivate  Print deactivation instructions
#   build       Build the project (install + lint + type-check)
#   test        Run all tests
#   lint        Run ruff linter
#   format      Format code with ruff
#   type-check  Run mypy type checker
#   run         Run the main pipeline
#   viz         Run the visualization
#   clean       Remove cache and build artifacts

help:
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'

env: ## Create and activate Python venv (if not exists)
	@if [ ! -d ".venv" ]; then \
		echo "Creating venv..."; \
		python -m venv .venv; \
	fi; \
	echo "Activating venv..."; \
	. .venv/bin/activate; \
	echo "Venv activated. To deactivate, run 'deactivate' in your shell."

install: ## Install dependencies (in venv)
	. .venv/bin/activate && pip install -e .[dev]

deactivate: ## Print deactivation instructions
	@echo "To deactivate, run 'deactivate' in your shell."

build: install lint type-check ## Build the project (install + lint + type-check)

test: ## Run all tests
	. .venv/bin/activate && PYTHONPATH=. pytest tests/

lint: ## Run ruff linter
	. .venv/bin/activate && ruff check src/ tests/

format: ## Format code with ruff
	. .venv/bin/activate && ruff format src/ tests/

type-check: ## Run mypy type checker
	. .venv/bin/activate && mypy src/

run: ## Run the main pipeline
	PYTHONPATH=. python -c 'from src.pipeline import SolarPipeline; p=SolarPipeline("$(CSV)"); p.load(); print(p.summarize())'

viz: ## Run the visualization
	PYTHONPATH=. python -c 'from src.pipeline import SolarPipeline; from src.visualization import plot_yield_over_time; df=SolarPipeline("$(CSV)").load(); plot_yield_over_time(df)'

clean: ## Remove cache and build artifacts
	rm -rf __pycache__ .pytest_cache
