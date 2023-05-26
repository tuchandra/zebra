"""solver.py

Solve the Einstein puzzle using Raymond Hettinger's approach.
"""

from __future__ import annotations

from collections.abc import Generator, Iterable
from contextlib import contextmanager
from random import shuffle

from . import sat_utils
from .clues import Clue, comb
from .literals import SATLiteral


class Puzzle:
    """
    A Puzzle is defined as a collection of constraints and clues.

    Clues are subclassess of Clue. They represent information about the puzzle that can be used by
    a human to solve it, like "the man who drinks tea owns a cat." Clues aren't converted to CNF
    until the `as_cnf` method is called.

    Constraints are structural properties of the puzzle, given to us in CNF to start. They're
    things like "each house gets exactly one type of flower" and "each flower must be assigned
    to one house." These will be the same for every Puzzle, so we have a default `set_constraints`
    method that takes care of them.

    We can add clues with `add_clue`. This returns the instance, so they can be chained together.

    Since in constraint satisfaction land, clues and constraints are the same thing (they're just
    logical clauses), we lump them all together at solve time.
    """

    def __init__(
        self,
        *,
        element_types: Iterable[type[SATLiteral]],
        elements: Iterable[SATLiteral] | None = None,
        n_houses: int = 5,
    ) -> None:
        """
        Initialize a puzzle with different kinds of elements. The `element_types` is a list of the
        *kinds* of literals we're using, i.e., Smoothie, FavoriteFood, FavoriteColor, etc. The
        `elements` is a list of the literals themselves, since some of the literal types have more
        than `n_houses` elements.

        If `elements` is not provided, we assume that every member of each of `element_types` is
        part of the puzzle. This is the case in example puzzles, but rarely the case for generated
        ones.
        """

        self.element_classes = list(element_types)
        if elements is None:
            self.literals = [el for el_class in self.element_classes for el in el_class]
        else:
            self.literals = list(elements)

        self.houses = tuple(range(1, n_houses + 1))
        self.clues: set[Clue] = set()
        self.constraints: list[tuple[str]] = []

    def _add_constraint(self, constraints: list[tuple[str]]) -> Puzzle:
        self.constraints.extend(constraints)
        return self

    def set_constraints(self) -> Puzzle:
        # each house gets exactly one value from each set of literals
        for house in self.houses:
            for element_type in self.element_classes:
                literals_of_that_type = [l for l in self.literals if isinstance(l, element_type)]  # noqa: E741
                self._add_constraint(sat_utils.one_of(comb(value, house) for value in literals_of_that_type))

        # each value gets assigned to exactly one house
        for literal in self.literals:
            self._add_constraint(sat_utils.one_of(comb(literal, house) for house in self.houses))

        return self

    def add_clue(self, clue: Clue) -> Puzzle:
        self.clues.add(clue)
        return self

    def remove_clue(self, clue: Clue) -> Puzzle:
        self.clues.remove(clue)
        return self

    @contextmanager
    def with_clues(self, clues: Iterable[Clue]) -> Generator[Puzzle]:
        """Create a context in which this Puzzle temporarily has clues added to it"""

        clues = list(clues)  # so we don't accidentally exhaust the iterable
        for clue in clues:
            self.add_clue(clue)

        yield self
        for clue in clues:
            self.remove_clue(clue)

        return self

    def as_cnf(self) -> list[tuple[str]]:
        """Express puzzle as solvable CNF"""

        # this would be a comprehension if we could use iterable unpacking
        cnf = []
        for clue in self.clues:
            cnf.extend(clue.as_cnf())

        cnf.extend(self.constraints)
        return cnf

    def __repr__(self) -> str:
        s = "This is a logic puzzle. "
        s += f"There are {len(self.houses)} houses (numbered {self.houses[0]} on the left, "
        s += f"{self.houses[-1]} on the right), from the perspective of someone standing across "
        s += "the street from them. Each has a different person in them. "
        s += "They have different characteristics:\n"
        for element_type in self.element_classes:
            literals = [l for l in self.literals if isinstance(l, element_type)]  # noqa: E741
            shuffle(literals)
            s += f" - {element_type.description()}: " + ", ".join(e.name for e in literals) + "\n"

        s += "\n"
        for i, clue in enumerate(self.clues):
            s += f"{i + 1}. {clue}\n"

        return s
