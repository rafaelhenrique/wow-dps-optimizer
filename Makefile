.PHONY: help

PROJECT_NAME=wow-dps-optimizer

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

run:  ## Run project
	poetry run python -m dps_optimizer

test:  ## Run tests
	poetry run pytest -sx

pre-commit:  ## Run all hooks of pre-commit
	poetry run pre-commit run -a -v

full-check: pre-commit  ## Run pre-commit and plugins and tests
	poetry run pytest -sx --dead-fixtures
	poetry run pytest -sx --validate-envvars
	poetry run pytest -sx --cov-report=term-missing --cov dps_optimizer

clean:  ## Clean temp/compiled/binary files
	@find . -iname '*.pyc' -delete
	@find . -iname '*.pyo' -delete
	@find . -iname '*~' -delete
	@find . -iname '*.swp' -delete
	@find . -iname '__pycache__' -delete

