SOURCE?=src/glide examples
TESTS?=tests

.PHONY: help

help:
	@echo "🔧 Glide Python Client: Commands"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

lint-check: ## Check source code without modifying it
	@echo "🧹 Ruff"
	@pdm run ruff $(SOURCE) $(TESTS)
	@echo "🧹 Black"
	@pdm run black --check $(SOURCE) $(TESTS)
	@echo "🧽 MyPy"
	@pdm run mypy --pretty $(SOURCE) $(TESTS)

lint: ## Lint source code
	@echo "🧹 Ruff"
	@pdm run ruff --fix $(SOURCE) $(TESTS)
	@echo "🧹 Black"
	@pdm run black $(SOURCE) $(TESTS)
	@echo "🧹 Ruff"
	@ruff --fix $(SOURCE) $(TESTS)
	@echo "🧽 MyPy"
	@pdm run mypy --pretty $(SOURCE) $(TESTS)

build: ## Build the package
	@pdm build

publish: ## Publish the package
	@pdm publish
