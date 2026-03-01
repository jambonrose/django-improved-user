# Please type "make help" in your terminal for a list of make targets.

# DIU => Django Improved User
# DIU_VENV is the name of directory to store the virtual environment
DIU_VENV ?= .venv

.DEFAULT_GOAL:=help

.PHONY: bump-patch ## Bump patch version (e.g., 2.1.0 → 2.1.1)
bump-patch:
	uv version --bump patch

.PHONY: bump-minor ## Bump minor version (e.g., 2.1.0 → 2.2.0)
bump-minor:
	uv version --bump minor

.PHONY: bump-major ## Bump major version (e.g., 2.1.0 → 3.0.0)
bump-major:
	uv version --bump major

.PHONY: tag ## Create git tag from current version
tag:
	git tag v$$(uv version)
	@echo "Tag created. Push with: git push --tags"

.PHONY: test ## Run test suites
test:
	uv run nox

.PHONY: docs ## Build documentation
docs:
	uv sync --group docs
	uv run --directory docs make html

.PHONY: clean ## Remove build, deploy, and test artifacts
clean:
	rm -rf dist
	rm -rf example*_project/db.sqlite3
	rm -rf htmlcov
	rm -rf src/*.egg-info
	rm -rf src/*.eggs
	find -X . \( -path '*/.nox/*' -o -path '*/.git/*' -o -path '*/$(DIU_VENV)/*' \) -prune -o \( -name "*.py[co]" -type f -print0 \) | xargs -0 -I {} rm '{}'
	find -X . \( -path '*/.nox/*' -o -path '*/.git/*' -o -path '*/$(DIU_VENV)/*' \) -prune -o \( -name ".coverage" -type f -print0 \) | xargs -0 -I {} rm '{}'
	find -X . \( -path '*/.nox/*' -o -path '*/.git/*' -o -path '*/$(DIU_VENV)/*' \) -prune -o \( -name ".coverage.*" -type f -print0 \) | xargs -0 -I {} rm '{}'
	find -X . \( -path '*/.nox/*' -o -path '*/.git/*' -o -path '*/$(DIU_VENV)/*' \) -prune -o \( -name "__pycache__" -type d -print0 \) | xargs -0 -I {} rm -r '{}'

.PHONY: purge ## Clean + remove virtual environment
purge: clean
	rm -rf .nox
	rm -rf docs/.nox
	rm -rf $(DIU_VENV)

.PHONY: help ## List make targets with description
help:
	@printf "\nUsage: make <target>\nExample: make serve\n\nTargets:\n"
	@grep '^.PHONY: .* #' Makefile | sed 's/\.PHONY: \(.*\) ## \(.*\)/  \1	\2/' | expand -t16
