.PHONY: run bonus clean lint install build clean-build

run:
	# Run the DFS version with config.txt
	python -m a_maze_ing config.txt


clean:
	# Remove Python bytecode caches
	rm -rf __pycache__ */__pycache__ *.pyc .mypy_cache

.ONESHELL:

install:
	# Create venv and install dependencies + editable package
	python -m venv myenv
	myenv/bin/pip install --upgrade pip
	myenv/bin/pip install -r requirements.txt
	myenv/bin/pip install -e .

build:
	# Build wheel and sdist using the venv Python
	myenv/bin/python -m build

lint:
	# Run flake8 and mypy checks
	flake8
	mypy .

clean-build:
	# Remove build artifacts
	rm -rf dist build *.egg-info