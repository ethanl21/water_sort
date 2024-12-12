# Water Sort

## Authors

- Ethan Lew
- Henry Dinh
- Dulce Funez Chinchilla

## Description

This project implements a solver for the water sort puzzle using the A* search algorithm.

## Usage

To run the program, [Poetry](https://python-poetry.org) is required.

In the root of the repository, run the following commands:

```bash
poetry install
poetry run python3 water_sort/main.py
```

You may need to replace `python3` with `python` depending on your system's configuration.

The initial state of the puzzle should be specified in `puzzle.json`. A sample puzzle file is provided. In order for the file to be read, it should be placed in the root of the repository.

## Code Layout

- `puzzle.json`
	- Initial state of the puzzle
- `water_sort.py`
	- Functions used to solve the water sort puzzle
- `main.py`
	- Frontend used to view the solution, powered by `arcade`