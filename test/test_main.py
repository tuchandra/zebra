import random
from collections.abc import Iterable, Mapping

import pytest

from src.elements import PuzzleElement
from src.generate import generate_all_clues, reduce_clues
from src.main import shuffle
from src.puzzle import Puzzle
from src.sat_utils import itersolve
from src.traptor_elements import (
    Bottlecap,
    MythicalTraptorPrimary,
    MythicalTraptorSecondary,
    MythicalTraptorTertiary,
    Smoothie,
    TropicalTraptorPrimary,
    TropicalTraptorSecondary,
    TropicalTraptorTertiary,
)


@pytest.mark.parametrize("n_houses", [2, 3, 4, 5])
@pytest.mark.parametrize("n_element_types", [2, 3, 4, 5, 6])  # can be larger, but slower to run
def test_constructed_puzzle_can_be_solved(n_houses: int, n_element_types: int):
    """Test that we can construct a puzzle of different sizes and uniquely solve it."""

    def pick[T](seq: Iterable[T]) -> list[T]:
        return random.sample(list(seq), n_houses)

    elements_superset = {
        Smoothie: pick(Smoothie.__members__.values()),
        Bottlecap: pick(Bottlecap.__members__.values()),
        MythicalTraptorPrimary: pick(MythicalTraptorPrimary.__members__.values()),
        MythicalTraptorSecondary: pick(MythicalTraptorSecondary.__members__.values()),
        MythicalTraptorTertiary: pick(MythicalTraptorTertiary.__members__.values()),
        TropicalTraptorPrimary: pick(TropicalTraptorPrimary.__members__.values()),
        TropicalTraptorSecondary: pick(TropicalTraptorSecondary.__members__.values()),
        TropicalTraptorTertiary: pick(TropicalTraptorTertiary.__members__.values()),
    }

    # Choose `n_element_types` random items from the dictionary (then convert back to dict)
    elements = dict(shuffle(list(elements_superset.items()), n_element_types))
    element_types = elements.keys()
    solution: Mapping[PuzzleElement, int] = {
        element: loc
        for _eltype, elements_of_type in elements.items()
        for loc, element in enumerate(shuffle(elements_of_type), start=1)
    }

    puzzle = Puzzle(
        element_types=element_types,
        elements=[e for els in elements.values() for e in els],
        solution=solution,
    )

    # Generate the clues and assert that the counts are vaguely reasonable
    clues = generate_all_clues(puzzle, solution)
    reduced, extras = reduce_clues(puzzle, clues)
    assert 1 < len(reduced) < len(clues)

    # Can the puzzle be solved under the basic set of clues?
    for clue in reduced:
        puzzle.add_clue(clue)

    assert len(list(itersolve(puzzle.as_cnf()))) == 1

    # Can adding (each of) the extra clues maintain the unique solution?
    for clue in extras:
        puzzle.add_clue(clue)
        assert len(list(itersolve(puzzle.as_cnf()))) == 1
