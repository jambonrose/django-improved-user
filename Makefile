# Please type "make help" in your terminal for a list of make targets.

# DIU => Django Improved User
# DIU_VENV is the name of directory to store the virtual environment
DIU_VENV ?= .venv
ROOT_PYTHON ?= python3
DIU_PYTHON ?= $(DIU_VENV)/bin/python3
DIU_COV ?= $(DIU_VENV)/bin/coverage

.DEFAULT_GOAL:=help

$(DIU_VENV)/bin/activate:
	mkdir -p $(DIU_VENV)
	$(ROOT_PYTHON) -m venv $(DIU_VENV)
	$(DIU_PYTHON) -m pip install --upgrade pip setuptools wheel
	$(DIU_PYTHON) -m pip install -r requirements.txt
	$(DIU_PYTHON) -m pip install -r doc-requirements.txt
	$(DIU_PYTHON) -m flit install --symlink

.PHONY: build ## Build artifacts meant for distribution
build: $(DIU_VENV)/bin/activate
	$(DIU_PYTHON) -m flit build

.PHONY: release ## Upload build artifacts to PyPI
release: $(DIU_VENV)/bin/activate
	git tag v`$(DIU_PYTHON) -m bumpversion --dry-run --list --new-version 0.0.0 patch | grep current | cut -d'=' -f 2`
	@echo "Verify new tag has been created. If the tag looks correct, push to git with: git push --tags ."

.PHONY: test ## Run test suite for current environment
test: $(DIU_VENV)/bin/activate
	$(DIU_PYTHON) -V
	$(DIU_PYTHON) -m pip -V
	$(DIU_COV) erase
	$(DIU_COV) run runtests.py
	$(DIU_COV) combine --append
	$(DIU_COV) report

.PHONY: tox ## Run test suite in different envs via tox
tox: $(DIU_VENV)/bin/activate
	$(DIU_VENV)/bin/tox

.PHONY: clean ## Remove build, deploy, and test artifacts
clean:
	rm -rf dist
	rm -rf example*_project/db.sqlite3
	rm -rf htmlcov
	rm -rf src/*.egg-info
	rm -rf src/*.eggs
	find -X . \( -path '*/.tox/*' -o -path '*/.git/*' -o -path '*/$(DIU_VENV)/*' \) -prune -o \( -name "*.py[co]" -type f -print0 \) | xargs -0 -I {} rm '{}'
	find -X . \( -path '*/.tox/*' -o -path '*/.git/*' -o -path '*/$(DIU_VENV)/*' \) -prune -o \( -name ".coverage" -type f -print0 \) | xargs -0 -I {} rm '{}'
	find -X . \( -path '*/.tox/*' -o -path '*/.git/*' -o -path '*/$(DIU_VENV)/*' \) -prune -o \( -name ".coverage.*" -type f -print0 \) | xargs -0 -I {} rm '{}'
	find -X . \( -path '*/.tox/*' -o -path '*/.git/*' -o -path '*/$(DIU_VENV)/*' \) -prune -o \( -name "__pycache__" -type d -print0 \) | xargs -0 -I {} rm -r '{}'

.PHONY: purge ## Clean + remove virtual environment
purge: clean
	rm -rf .tox
	rm -rf $(DIU_VENV)

.PHONY: help ## List make targets with description
help:
	@printf "\nUsage: make <target>\nExample: make serve\n\nTargets:\n"
	@grep '^.PHONY: .* #' Makefile | sed 's/\.PHONY: \(.*\) ## \(.*\)/  \1	\2/' | expand -t12
