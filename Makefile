# Filename: Makefile

PYLINT := pylint3
PYTHON := python3

PIP_INSTALL_FLAGS := -r requirements.txt

.PHONY: help
help:
	@printf "Usage: make [options] [target] ...\n"
	@printf "\n"
	@printf "Valid targets:\n"
	@printf "\n"
	@printf "    help            Display this help message\n"
	@printf "    test            Run unit test suite\n"
	@printf "    lint            Run lint checks\n"
	@printf "    cover           Collect coverage\n"
	@printf "    html            Build Sphinx documentation\n"

.PHONY: test
test:
	@$(PYTHON) setup.py nosetests --with-doctest

.PHONY: lint
lint:
	@$(PYLINT) myeda --rcfile .pylintrc

.PHONY: cover
cover:
	@$(PYTHON) setup.py nosetests --with-doctest --with-coverage --cover-html --cover-package=myeda

.PHONY: html
html:
	@$(PYTHON) setup.py build_sphinx
