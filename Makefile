unit-tests:
	@pytest

unit-tests-cov:
	@pytest --cov=src --cov-report term-missing --cov-report=html

clean-cov:
	@rm -rf .coverage
	@rm -rf htmlcov

format-black:
	@black .

format-isort:
	@isort .

lint-black:
	@black . --check

lint-isort:
	@isort . --check

lint-flake8:
	@flake8 .

lint-mypy:
	@mypy --config-file pyproject.toml .

lint-mypy-report:
	@mypy --config-file pyproject.toml . --html-report ./mypy_html

format: format-black format-isort

lint: lint-black lint-isort lint-flake8 lint-mypy
