from __future__ import annotations

from collections.abc import Generator, Iterable, Mapping, Sequence
from contextlib import contextmanager
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

        self.solution = solution
        self.element_classes: Sequence[type[PuzzleElement]] = list(element_types)
        self.elements_by_class: Mapping[type[PuzzleElement], list[PuzzleElement]] = {
            el_type: [el for el in elements if isinstance(el, el_type)] for el_type in self.element_classes
        }
        self.elements: Sequence[PuzzleElement] = list(elements)

        self.size = len(self.elements) // len(self.element_classes)
        self.houses = tuple(range(1, self.size + 1))

        self.clues: set[Clue] = set()
        self.constraints = self._get_constraints()

    def _get_constraints(self) -> list[Clause]:
        constraints: list[Clause] = []

        # each house gets exactly one value from each set of literals
        for house in self.houses:
            for _element_type, elements in self.elements_by_class.items():
                constraints.extend(sat_utils.one_of([comb(value, house) for value in elements]))

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

    def format_elements(self) -> str:
        """
        Format the puzzle components for printing.

        The puzzle input on CC requires a pure HTML string, <br> tags and all. The newlines that
        we include are for readability and so we can print the whole thing to the console.
        """

        lines = [
            "<u>Puzzle Components</u>",
            f"There are {self.size} nests, (numbered 1 on the left, {self.size} on the right), from the perspective of someone standing across from them.",
            "Our job is to help Traptop figure out who visited each nest.",
        ]

        for el_type in self.element_classes:  # should be sorted
            class_description = el_type.description()
            elements = ", ".join(el.name.title() for el in self.elements_by_class[el_type])
            line = f"- {class_description} ({elements})"

            lines.append(line)

        s = " <br>\n".join(lines) + " <br><br>\n"
        return s

    def format_clues(self) -> str:
        """
        Format the clues for printing.

        The puzzle input on CC requires a pure HTML string, <br> tags and all. The newlines that
        we include are for readability and so we can print the whole thing to the console. The
        clues are just a title and a numbered list, but we don't bother with a <ol> tag.
        """

        lines = ["<u>Clues</u>"]

        for i, clue in enumerate(self.clues, 1):
            clue_description = clue.__repr__().replace("house", "nest")
            lines.append(f"{i}. {clue_description}")

        s = " <br>\n".join(lines) + " <br><br>\n"
        return s
