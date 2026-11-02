SRC_DIR = src
FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs
RUN_FLAGS = --fast_forward --visualisation

install:
	uv sync

run:
	uv run python3 -m $(SRC_DIR)

faster:
	uv run python3 -m $(SRC_DIR) $(RUN_FLAGS)

debug:
	uv run python3 -m pdb -m $(SRC_DIR)

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache
	rm -rf $(SRC_DIR)/__pycache__
	find . -type f -name "*.pyc" -delete

lint:
	uv run flake8 $(SRC_DIR)
	uv run mypy $(FLAGS) $(SRC_DIR)

lint-strict:
	uv run flake8 $(SRC_DIR)
	uv run mypy --strict $(SRC_DIR)

.PHONY: install run debug faster clean lint lint-strict
