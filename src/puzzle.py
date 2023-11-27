from __future__ import annotations

from collections.abc import Generator, Iterable, Mapping
from contextlib import contextmanager
from random import shuffle
from typing import Self

from src.clues import Clue, ClueCNF, comb
from src.elements import PuzzleElement
from src.sat_utils import Clause

from . import sat_utils


class Puzzle:
    """
    A Puzzle is defined in terms of:
    - its size, the element types, and elements
    - a *solution*, which is a mapping between each location & the puzzle elements at that location
    - a collection of *constraints*
    - a collection of *clues*

    A puzzle may or may not be solvable under a given set of clues.

    clues vs. constraints
    ---------------------
    Both of these are boolean clauses. We express both as CNFs. The difference is a domain question,
    not a mathematical one.

    Constraints are structural properties of the puzzle. They do not depend on the solution. We can
    describe the constraints, and express them as CNFs, when creating the puzzle.

    A `Clue` contains information about the puzzle's soultion. It's a description, yes, but it also
    depends on the puzzle having a solution in the first place.
    """

    def __init__(
        self,
        *,
        size: int = 5,
        element_types: Iterable[type[PuzzleElement]],
        elements: Iterable[PuzzleElement],
        solution: Mapping[PuzzleElement, int],
    ) -> None:
        """
        Initialize a puzzle with different kinds of elements. The puzzle is initialized with two lists:
        - `element_types`, which describes the kinds of literals we're using (Smoothie, FavoriteFood, ...)
        - `elements`, which describes -- for each element type -- the literals themselves (Lilac, Earth, ...)

        We compute the puzzle _size_ from total number of elements divided by the number of element types;
        this tells us how many of each element type there are, and since each must be in a different location,
        that's exactly the number of houses.
        """

        self.size = size
        self.houses = tuple(range(1, self.size + 1))

        self.element_classes = list(element_types)
        self.elements = list(elements)
        self.solution = solution

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
