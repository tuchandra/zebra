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
 * `elements.py` (formerly `literals.py`) contains the different puzzle elements via a base `PuzzleElement` and subclasses (people, favorite types of tea, most-played video games, etc.)
 * `clues.py` contains the different classes of clues via a base `Clue` and subclasses ("x is at the same house as y", "x is somewhere to the left of z", etc.)
 * `generate.py` is the **main entry point** into this project, creating new puzzles.

There's a currently empty `tests/` dir.

## Requirements
- Python 3.12 (beta)
- Poetry

This uses the SAT solver [pycosat](https://pypi.org/project/pycosat/), but PySAT is listed as a dependency, too.)

Development uses *black*, *ruff*, and *pyright*, though we're not totally compliant yet; I created the repo in 2019, and have only made minor changes since adding the dev dependencies.

## Future work
- Create a better CLI (in-place updates during clue reduction, proper args for e.g., puzzle size)
- Try creating smaller size (4 houses) with, say, 6 categories; is that easier or harder?
- Consider web interface?
- Consider using another logic programming interface; PySAT, answer set programming, more discussion in this [HN thread](https://news.ycombinator.com/item?id=36087464) ...

These may happen. But the project is finally at a place that I'm happy with, and so I'm excited to share and write about it.

## Incomplete changelog
### 2023-06-05: typing improvements
Rename `SATLiteral` -> `PuzzleElement` (smoothie, cat, etc.); this clarifies that it's not a Literal in the boolean sense and is instead a name for e.g., characters in a puzzle.

Create a new type `SATLiteral` (which is a `str` in a trenchcoat); this represents the literal in the boolean-variable sense, like "Value *el* is at house *loc*" or "Value *el* is not at house *loc*." Internally, these are represented by some integer *i* and its negative counterpart *-i*.

Use (the new) `SATLiteral` as the return type of `comb(el: str, loc: int) -> SATLiteral`, mapping puzzle elements to literals, and `neg(el: SATLiteral) -> SATLiteral` to negate a literal.

Add `Clause: tuple[SATLiteral, ...]` representing a "∨" (boolean OR; disjunction) of literals; e.g., `(1, -5, 6)` is a disjunction stating that `x_1` is true, `x_5` is not true, or `x_6` is true.

Add `ClueCNF: list[Clause]`, representing a "∧" (boolean AND; conjunction) of `Clause`s. A puzzle in CNF is an "AND of ORs" ("∧ of ∨s" or "∧ of Clauses").

## Definitions
A CNF is an "∧ of ∨s," where the "∨" is over any Literal. Since an "∨ of Literals" is equivalently a Clause, a CNF is the "∧ of Clauses."

A DNF is a "∨ of ∧s." The DNF is the *answer* to a SAT problem; a DNF of "A or B or C" reads that A, B, and C are all valid (satisfying) assignments. Converting a CNF to a DNF is therefore NP-hard, since from the DNF you can read off solutions to the CNF.

> CNF is an ∧ of ∨s, where ∨ is over variables or their negations (literals); an ∨ of literals is also called a clause. DNF is an ∨ of ∧s; an ∧ of literals is called a term.
