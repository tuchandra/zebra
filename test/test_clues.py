import pytest

from src.clues import found_at, not_at, same_house
from src.elements import PuzzleElement
from src.sat_utils import ClueCNF, compare_cnfs


class Letter(PuzzleElement):
    a = "a"
    b = "b"
    c = "c"


class Cat(PuzzleElement):
    luna = "luna"
    ruby = "ruby"
    acorn = "acorn"


@pytest.mark.parametrize(
    ("element", "house", "expected"),
    [
        (Letter.a, 1, "a 1"),
        (Letter.b, 2, "b 2"),
        (Letter.c, 3, "c 3"),
        (Letter.c, 4, "c 4"),
        (Letter.c, 5, "c 5"),
        (Cat.luna, 1, "luna 1"),
        (Cat.ruby, 2, "ruby 2"),
        (Cat.acorn, 3, "acorn 3"),
    ],
)
def test_found_at(element: PuzzleElement, house: int, expected: str):
    clue = found_at(element, house)
    assert clue.as_cnf() == [(expected,)]


@pytest.mark.parametrize(
    ("element", "house", "expected"),
    [
        (Letter.a, 1, "~a 1"),
        (Letter.b, 2, "~b 2"),
        (Letter.c, 3, "~c 3"),
        (Cat.acorn, 1, "~acorn 1"),
        (Cat.luna, 2, "~luna 2"),
        (Cat.ruby, 3, "~ruby 3"),
        (Cat.ruby, 6, "~ruby 6"),
    ],
)
def test_not_at(element: PuzzleElement, house: int, expected: str):
    clue = not_at(element, house)
    assert clue.as_cnf() == [(expected,)]


@pytest.mark.parametrize(
    ("element1", "element2", "size", "expected"),
    [
        (Letter.a, Letter.b, 1, [("a 1",), ("b 1",)]),
        (Letter.a, Letter.b, 2, [("b 1", "a 2"), ("b 1", "b 2"), ("a 1", "a 2"), ("a 1", "b 2")]),
    ],
)
def test_same_house(element1: PuzzleElement, element2: PuzzleElement, size: int, expected: ClueCNF):
    clue = same_house(element1, element2, tuple(range(1, size + 1)))
    assert compare_cnfs(clue.as_cnf(), expected)


# the rest of these are very hard to test, so ... oh well
