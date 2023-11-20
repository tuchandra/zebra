import pytest

from src.clues import (
    beside,
    consecutive,
    found_at,
    left_of,
    not_at,
    one_between,
    right_of,
    same_house,
)
from src.elements import PuzzleElement
from src.generate import (
    Solution,
    _generate_consecutive_beside,
    _generate_found_at,
    _generate_left_right_of,
    _generate_one_between,
    _generate_same_house,
    _generate_two_between,
)
from src.puzzle import Puzzle


class Cat(PuzzleElement):
    luna = "Luna"
    ruby = "Ruby"
    acorn = "Acorn"


class OtherCat(PuzzleElement):
    maxwell = "Max"
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
        OtherCat.maxwell: 3,
    }
    puzzle = Puzzle(
        element_types=[Cat, OtherCat],
        elements=[Cat.luna, Cat.ruby, Cat.acorn, OtherCat.maxwell, OtherCat.maui, OtherCat.stranger],
    )

    return puzzle, solution


def test_generate_found_at(puzzle: SolvedPuzzle):
    """Test that _generate_found_at generates the found_at & not_at clues."""

    assert _generate_found_at(puzzle[0], puzzle[1]) == {
        # found_at
        found_at(Cat.ruby, 1),
        found_at(Cat.luna, 2),
        found_at(Cat.acorn, 3),
        found_at(OtherCat.stranger, 1),
        found_at(OtherCat.maui, 2),
        found_at(OtherCat.maxwell, 3),
        # not_at, in order of houses
        not_at(Cat.luna, 1),
        not_at(Cat.acorn, 1),
        not_at(OtherCat.maui, 1),
        not_at(OtherCat.maxwell, 1),
        not_at(Cat.ruby, 2),
        not_at(Cat.acorn, 2),
        not_at(OtherCat.stranger, 2),
        not_at(OtherCat.maxwell, 2),
        not_at(Cat.ruby, 3),
        not_at(Cat.luna, 3),
        not_at(OtherCat.stranger, 3),
        not_at(OtherCat.maui, 3),
    }


def test_generate_same_house(puzzle: SolvedPuzzle):
    """Test that _generate_same_house generates the six clues."""

    houses = (1, 2, 3)
    assert _generate_same_house(puzzle[0], puzzle[1]) == {
        same_house(Cat.ruby, OtherCat.stranger, houses),
        same_house(OtherCat.stranger, Cat.ruby, houses),
        same_house(Cat.luna, OtherCat.maui, houses),
        same_house(OtherCat.maui, Cat.luna, houses),
        same_house(Cat.acorn, OtherCat.maxwell, houses),
        same_house(OtherCat.maxwell, Cat.acorn, houses),
    }


def test_generate_consecutive_beside(puzzle: SolvedPuzzle):
    """
    Test that _generate_consecutive_beside generates correct clues.

    Since the output of _generate_consecutive_beside is randomized, we will generate all possible
    clues and then test each output clue for membership in the superset. We repeat a few times to
    account for the randomness (and to reduce the chance of a flaky test).
    """

    houses = (1, 2, 3)
    all_possible_clues = {
        # consecutive, house 1 & 2
        consecutive(Cat.ruby, Cat.luna, houses),
        consecutive(Cat.ruby, OtherCat.maui, houses),
        consecutive(OtherCat.stranger, Cat.luna, houses),
        consecutive(OtherCat.stranger, OtherCat.maui, houses),
        # consecutive, house 2 & 3
        consecutive(Cat.luna, Cat.acorn, houses),
        consecutive(Cat.luna, OtherCat.maxwell, houses),
        consecutive(OtherCat.maui, Cat.acorn, houses),
        consecutive(OtherCat.maui, OtherCat.maxwell, houses),
        # beside, house 1 & 2
        beside(Cat.ruby, Cat.luna, houses),
        beside(Cat.ruby, OtherCat.maui, houses),
        beside(OtherCat.stranger, Cat.luna, houses),
        beside(OtherCat.stranger, OtherCat.maui, houses),
        # beside, house 2 & 1 (the reverse of the above)
        beside(Cat.luna, Cat.ruby, houses),
        beside(OtherCat.maui, Cat.ruby, houses),
        beside(Cat.luna, OtherCat.stranger, houses),
        beside(OtherCat.maui, OtherCat.stranger, houses),
        # beside, house 2 & 3
        beside(Cat.luna, Cat.acorn, houses),
        beside(Cat.luna, OtherCat.maxwell, houses),
        beside(OtherCat.maui, Cat.acorn, houses),
        beside(OtherCat.maui, OtherCat.maxwell, houses),
        # beside, house 3 & 2 (the reverse of the above)
        beside(Cat.acorn, Cat.luna, houses),
        beside(OtherCat.maxwell, Cat.luna, houses),
        beside(Cat.acorn, OtherCat.maui, houses),
        beside(OtherCat.maxwell, OtherCat.maui, houses),
    }
    for _ in range(5):
        output = _generate_consecutive_beside(puzzle[0], puzzle[1])
        # output.issubset(all_possible_clues) is not as useful for seeing a failure
        for clue in output:
            assert clue in all_possible_clues


def test_left_right_of(puzzle: SolvedPuzzle):
    """
    Test that _generate_left_right_of generates correct clues.

    Since the output of _generate_left_right_of is randomized, we will generate all possible
    clues and then test each output clue for membership in the superset. We repeat a few times to
    account for the randomness (and to reduce the chance of a flaky test).
    """

    houses = (1, 2, 3)
    all_possible_clues = {
        # left_of, house 1 & 2; product (ruby, stranger) x (luna, maui)
        left_of(Cat.ruby, Cat.luna, houses),
        left_of(Cat.ruby, OtherCat.maui, houses),
        left_of(OtherCat.stranger, Cat.luna, houses),
        left_of(OtherCat.stranger, OtherCat.maui, houses),
        # left_of, house 2 & 3; product (luna, maui) x (acorn, max)
        left_of(Cat.luna, Cat.acorn, houses),
        left_of(Cat.luna, OtherCat.maxwell, houses),
        left_of(OtherCat.maui, Cat.acorn, houses),
        left_of(OtherCat.maui, OtherCat.maxwell, houses),
        # left_of, house 1 & 3; product (ruby, stranger) x (acorn, max)
        left_of(Cat.ruby, Cat.acorn, houses),
        left_of(Cat.ruby, OtherCat.maxwell, houses),
        left_of(OtherCat.stranger, Cat.acorn, houses),
        left_of(OtherCat.stranger, OtherCat.maxwell, houses),
        # right_of, house 2 & 1; product (luna, maui) x (ruby, stanger)
        right_of(Cat.luna, Cat.ruby, houses),
        right_of(OtherCat.maui, Cat.ruby, houses),
        right_of(Cat.luna, OtherCat.stranger, houses),
        right_of(OtherCat.maui, OtherCat.stranger, houses),
        # right_of, house 3 & 2; product (acorn, max) x (luna, maui)
        right_of(Cat.acorn, Cat.luna, houses),
        right_of(OtherCat.maxwell, Cat.luna, houses),
        right_of(Cat.acorn, OtherCat.maui, houses),
        right_of(OtherCat.maxwell, OtherCat.maui, houses),
        # right_of, house 3 & 1; product (acorn, max) x (ruby, stranger)
        right_of(Cat.acorn, Cat.ruby, houses),
        right_of(OtherCat.maxwell, Cat.ruby, houses),
        right_of(Cat.acorn, OtherCat.stranger, houses),
        right_of(OtherCat.maxwell, OtherCat.stranger, houses),
    }
    for _ in range(5):
        output = _generate_left_right_of(puzzle[0], puzzle[1])
        # output.issubset(all_possible_clues) is not as useful for seeing a failure
        for clue in output:
            assert clue in all_possible_clues


def test_generate_one_between(puzzle: SolvedPuzzle):
    """Test that _generate_one_between creates the right clues."""

    houses = (1, 2, 3)
    assert _generate_one_between(puzzle[0], puzzle[1]) == {
        one_between(Cat.ruby, Cat.acorn, houses),
        one_between(Cat.ruby, OtherCat.maxwell, houses),
        one_between(OtherCat.stranger, Cat.acorn, houses),
        one_between(OtherCat.stranger, OtherCat.maxwell, houses),
    }


def test_generate_two_between_empty(puzzle: SolvedPuzzle):
    """Test that generate_two_between returns the empty set, because this puzzle only has 3 items."""

    assert _generate_two_between(puzzle[0], puzzle[1]) == set()
