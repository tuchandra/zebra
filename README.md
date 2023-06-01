# Zebra Puzzles
*Today, in 2023, project is largely unmaintained. I'm using it as a playground for some things I want to try out, but I don't recommend anyone build off this.*

![Example puzzle](sample_grid.png)

Remember logic puzzles that looked like this? They had clues like:
 * *There is one house between Tushar and Maui.*
 * *Ruby's favorite video game is Pokemon.*
 * *The chai drinker does not like the color blue.*

I loved these as a kid, and watching Raymond Hettinger's [PyCon 2019 talk](https://www.youtube.com/watch?v=_GP9OpZPUYc) inspired me to revisit these problems. He showed us how to solve them; I wanted to learn how to generate them.

Using modern Python and constraint satisfaction (SAT) solvers, this project can be used to create random zebra puzzles.

## Structure
This project has five Python files in `src/`:
 * `sat_utils.py` is basic utilities for interacting with the SAT solver [pycosat](https://pypi.org/project/pycosat/); this code was almost entirely written by [Raymond Hettinger](https://rhettinger.github.io/einstein.html#essential-utilities-for-humanization)
 * `puzzle.py` contains the main `Puzzle` class and two sample puzzles that can be solved
 * `literals.py` contains the different puzzle elements via a base `Literal` and subclasses (people, favorite types of tea, most-played video games, etc.)
 * `clues.py` contains the different classes of clues via a base `Clue` and subclasses ("x is at the same house as y", "x is somewhere to the left of z", etc.)
 * `generate.py` is the **main entry point** into this project, creating new puzzles.

There's a currently empty `tests/` dir.

## Requirements
- Python 3.12 (beta)
- Poetry

This uses the SAT solver [pycosat](https://pypi.org/project/pycosat/), but PySAT is listed as a dependency, too.)

Development uses *black*, *ruff*, and *pyright*, though we're not totally compliant yet; I created the repo in 2019, and have only made minor changes since adding the dev dependencies.


## Future work
There are a few things I still want to do:
- configure random solution generation
- try out creating a smaller size (e.g., 4 houses) with more categories; that sounds like a fun puzzle!
- create a better CLI
- consider a web interface?

These may happen. But the project is finally at a place that I'm happy with, and so I'm excited to share and write about it.
