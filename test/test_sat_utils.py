import pytest

from src.sat_utils import Clause, SATLiteral, make_translate, negate


@pytest.mark.parametrize(
    ("input", "output"),
    [
        ("x", "~x"),
        ("~x", "x"),
        ("chai", "~chai"),
        ("~chai", "chai"),
    ],
)
def test_negate(input: str, output: str):
    assert negate(input) == output


@pytest.mark.parametrize(
    ("clue_literals", "lit_to_num", "num_to_lit"),
    [
        (
            [("~P", "Q", "R")],
            {"P": 1, "~P": -1, "Q": 2, "~Q": -2, "R": 3, "~R": -3},
            {1: "P", 2: "Q", 3: "R", -1: "~P", -2: "~Q", -3: "~R"},
        ),
        (
            [("~P", "Q"), ("~P", "R")],
            {"P": 1, "~P": -1, "Q": 2, "~Q": -2, "R": 3, "~R": -3},
            {1: "P", 2: "Q", 3: "R", -1: "~P", -2: "~Q", -3: "~R"},
        ),
    ],
)
def test_make_translate(clue_literals: list[tuple[str]], lit_to_num: dict[str, int], num_to_lit: dict[int, str]):
    clues: list[Clause] = [tuple(SATLiteral(x) for x in clause) for clause in clue_literals]

    assert make_translate(clues) == (lit_to_num, num_to_lit)
