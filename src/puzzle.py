from __future__ import annotations

from collections.abc import Generator, Iterable
from contextlib import contextmanager
from random import shuffle
from typing import Self

from src.clues import Clue, ClueCNF, comb
from src.elements import PuzzleElement
from src.sat_utils import Clause

from . import sat_utils


class Puzzle:
    """
    A Puzzle is defined as a collection of constraints and clues. A Puzzle has a solution.

    Clues are subclassess of Clue. They represent information about the puzzle that can be used by
    a human to solve it, like "the man who drinks tea owns a cat." Clues aren't converted to CNF
    until the `as_cnf` method is called.

    Constraints are structural properties of the puzzle, given to us in CNF to start. They're
    things like "each house gets exactly one type of flower" and "each flower must be assigned
    to one house." These will be the same for every Puzzle, so we initialize the puzzle with the
    constraints appropriate to its structure.

    We can add clues with `add_clue`. This returns the instance, so they can be chained together.

    Since in constraint satisfaction land, clues and constraints are the same thing (they're just
    logical clauses), we lump them all together at solve time.
    """

    def __init__(
        self,
        *,
        element_types: Iterable[type[PuzzleElement]],
        elements: Iterable[PuzzleElement],
    ) -> None:
        """
        Initialize a puzzle with different kinds of elements. The puzzle is initialized with two lists:
        - `element_types`, which describes the kinds of literals we're using (Smoothie, FavoriteFood, ...)
        - `elements`, which describes -- for each element type -- the literals themselves (Lilac, Earth, ...)

        We compute the puzzle _size_ from total number of elements divided by the number of element types;
        this tells us how many of each element type there are, and since each must be in a different location,
        that's exactly the number of houses.
        """

        self.element_classes = list(element_types)
        self.elements = list(elements)

        self.size = len(self.elements) // len(self.element_classes)
        self.houses = tuple(range(1, self.size + 1))

        self.clues: set[Clue] = set()
        self.constraints = self._get_constraints()

    def _get_constraints(self) -> list[Clause]:
        constraints: list[Clause] = []

        # each house gets exactly one value from each set of literals
        for house in self.houses:
            for element_type in self.element_classes:
                literals_of_that_type = [lit for lit in self.elements if isinstance(lit, element_type)]
                constraints.extend(sat_utils.one_of([comb(value, house) for value in literals_of_that_type]))

        # each value gets assigned to exactly one house
        for literal in self.elements:
            constraints.extend(sat_utils.one_of([comb(literal, house) for house in self.houses]))

        return constraints

    def add_clue(self, clue: Clue) -> Self:
        self.clues.add(clue)
        return self

    def remove_clue(self, clue: Clue) -> Self:
        self.clues.remove(clue)
        return self

    @contextmanager
    def with_clues(self, clues: Iterable[Clue]) -> Generator[Self, None, Self]:
        """Create a context in which this Puzzle temporarily has clues added to it"""

        clues = list(clues)  # so we don't accidentally exhaust the iterable
        for clue in clues:
            self.add_clue(clue)

        yield self
        for clue in clues:
            self.remove_clue(clue)

        return self

    def as_cnf(self) -> ClueCNF:
        """Express puzzle as solvable CNF"""

        cnf: list[Clause] = []
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
            literals = [l for l in self.elements if isinstance(l, element_type)]  # noqa: E741
            shuffle(literals)
            s += f" - {element_type.description()}: " + ", ".join(e.name for e in literals) + "\n"

        s += "\n"
        for i, clue in enumerate(self.clues):
            s += f"{i + 1}. {clue}\n"

        return s
