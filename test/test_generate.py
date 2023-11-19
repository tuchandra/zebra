import pytest

from src.clues import (
    beside,
    consecutive,
    found_at,
    not_at,
    same_house,
)
from src.elements import PuzzleElement
from src.generate import (
    Solution,
    _generate_consecutive_beside,
    _generate_found_at,
    _generate_same_house,
)
from src.puzzle import Puzzle


class Cat(PuzzleElement):
    luna = "Luna"
    ruby = "Ruby"
    acorn = "Acorn"


class OtherCat(PuzzleElement):
    max = "Max"
    maui = "Maui"
    stranger = "Stranger"


type SolvedPuzzle = tuple[Puzzle, Solution]


@pytest.fixture()
def puzzle() -> SolvedPuzzle:
    """Small (3x3) puzzle and solution to use for testing."""

    solution: dict[PuzzleElement, int] = {
        Cat.ruby: 1,
        Cat.luna: 2,
        Cat.acorn: 3,
        OtherCat.stranger: 1,
        OtherCat.maui: 2,
        OtherCat.max: 3,
    }
    puzzle = Puzzle(
        element_types=[Cat, OtherCat],
        elements=[Cat.luna, Cat.ruby, Cat.acorn, OtherCat.max, OtherCat.maui, OtherCat.stranger],
    )

    return puzzle, solution


def test_generate_found_at(puzzle: SolvedPuzzle):
    """Test that _generate_found_at generates correct clues."""

    assert _generate_found_at(puzzle[0], puzzle[1]) == {
        found_at(Cat.ruby, 1),
        found_at(Cat.luna, 2),
        found_at(Cat.acorn, 3),
        found_at(OtherCat.stranger, 1),
        found_at(OtherCat.maui, 2),
        found_at(OtherCat.max, 3),
        # this function also includes the not_at clues
        not_at(Cat.luna, 1),
        not_at(Cat.acorn, 1),
        not_at(OtherCat.maui, 1),
        not_at(OtherCat.max, 1),
        not_at(Cat.ruby, 2),
        not_at(Cat.acorn, 2),
        not_at(OtherCat.stranger, 2),
        not_at(OtherCat.max, 2),
        not_at(Cat.ruby, 3),
        not_at(Cat.luna, 3),
        not_at(OtherCat.stranger, 3),
        not_at(OtherCat.maui, 3),
    }


def test_generate_same_house(puzzle: SolvedPuzzle):
    """Test that _generate_same_house generates correct clues."""

    houses = (1, 2, 3)
    assert _generate_same_house(puzzle[0], puzzle[1]) == {
        same_house(Cat.ruby, OtherCat.stranger, houses),
        same_house(OtherCat.stranger, Cat.ruby, houses),
        same_house(Cat.luna, OtherCat.maui, houses),
        same_house(OtherCat.maui, Cat.luna, houses),
        same_house(Cat.acorn, OtherCat.max, houses),
        same_house(OtherCat.max, Cat.acorn, houses),
    }


def test_generate_consecutive_beside(puzzle: SolvedPuzzle):
    """
    Test that _generate_consecutive_beside generates correct clues.

    This is harder to test because the output of _generate_consecutive_beside is randomized -
    consecutive(x, y) & beside(x, y) are mostly redundant so we don't include both.

    To test this, we have to check that the output is a subset of the expected output ... and we
    do this a few times to make sure we're not just getting lucky.
    """

    houses = (1, 2, 3)
    all_possible_clues = {
        # consecutive is ordered; here are the clues with the same PuzzleElement
        consecutive(Cat.ruby, Cat.luna, houses),
        consecutive(Cat.luna, Cat.acorn, houses),
        consecutive(OtherCat.stranger, OtherCat.maui, houses),
        consecutive(OtherCat.maui, OtherCat.max, houses),
        # and here are the different PuzzleElement clues
        consecutive(Cat.ruby, OtherCat.maui, houses),
        consecutive(Cat.luna, OtherCat.max, houses),
        consecutive(OtherCat.stranger, Cat.luna, houses),
        consecutive(OtherCat.maui, Cat.acorn, houses),
        # house 1 / house 2; all combinations of (ruby, stanger) x (luna, maui)
        beside(Cat.ruby, Cat.luna, houses),
        beside(Cat.luna, Cat.ruby, houses),
        beside(Cat.ruby, OtherCat.maui, houses),
        beside(OtherCat.maui, Cat.ruby, houses),
        beside(OtherCat.stranger, Cat.luna, houses),
        beside(Cat.luna, OtherCat.stranger, houses),
        beside(OtherCat.stranger, OtherCat.maui, houses),
        beside(OtherCat.maui, OtherCat.stranger, houses),
        # house 2 / house 3; all combinations of (luna, maui) x (acorn, max)
        beside(Cat.luna, Cat.acorn, houses),
        beside(Cat.acorn, Cat.luna, houses),
        beside(Cat.luna, OtherCat.max, houses),
        beside(OtherCat.max, Cat.luna, houses),
        beside(OtherCat.maui, OtherCat.max, houses),
        beside(OtherCat.max, OtherCat.maui, houses),
        beside(Cat.acorn, OtherCat.maui, houses),
        beside(OtherCat.maui, Cat.acorn, houses),
    }
    for _ in range(5):
        output = _generate_consecutive_beside(puzzle[0], puzzle[1])
        # output.issubset(all_possible_clues) is not as useful for seeing a failure
        for clue in output:
            assert clue in all_possible_clues
