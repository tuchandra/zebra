import pytest

from src.sat_utils import SATLiteral, make_translate, negate


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


def test_make_translate():
    literals = [["~P", "Q", "R"], ["S", "P", "~R"]]
    clue_cnf = [tuple(SATLiteral(x) for x in clause) for clause in literals]

    assert make_translate(clue_cnf) == (
        {"P": 1, "~P": -1, "Q": 2, "~Q": -2, "R": 3, "~R": -3, "S": 4, "~S": -4},
        {1: "P", 2: "Q", 3: "R", -1: "~P", -2: "~Q", -3: "~R", 4: "S", -4: "~S"},
    )


def test_make_translate_example():
    literals = [["~a", "b", "~c"], ["a", "~c"]]
    clue_cnf = [tuple(SATLiteral(x) for x in clause) for clause in literals]

    assert make_translate(clue_cnf) == (
        {"a": 1, "c": 3, "b": 2, "~a": -1, "~b": -2, "~c": -3},
        {1: "a", 2: "b", 3: "c", -1: "~a", -3: "~c", -2: "~b"},
    )
