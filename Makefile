.PHONY: install run debug build package clean lint

.venv/bin/python:
	python3 -m venv .venv

install: .venv/bin/python
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install -r requirements.txt
	.venv/bin/python -m pip install -e .

run: .venv/bin/python
	.venv/bin/python a_maze_ing.py config.txt

debug: .venv/bin/python
	.venv/bin/python -m pdb a_maze_ing.py config.txt

build: .venv/bin/python
	.venv/bin/python -m pip install --upgrade build
	.venv/bin/python -m build

package: build
	cp dist/mazegen-*.tar.gz mazegen.tar.gz

clean:
	rm -rf __pycache__ */__pycache__ .mypy_cache
	rm -rf mazegen.egg-info dist build

lint:
	.venv/bin/python -m flake8 . --exclude=.venv,venv,__pycache__,.mypy_cache
	.venv/bin/python -m mypy . --explicit-package-bases --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs