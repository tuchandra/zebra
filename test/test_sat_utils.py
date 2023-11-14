import pytest

from src.sat_utils import (
    ClueCNF,
    Q,
    SATLiteral,
    all_of,
    basic_fact,
    make_translate,
    negate,
    none_of,
    one_of,
    parse_cnf_description,
    some_of,
)


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


def test_quantifier():
    # I don't really understand why this is the case
    literals = [SATLiteral(x) for x in ["a", "b", "c"]]
    assert (Q(literals) <= 1) == [
        ("~a", "~b"),
        ("~a", "~c"),
        ("~b", "~c"),
    ]


@pytest.mark.parametrize(
    ("input", "output"),
    [
        ("~a", [("~a",)]),
        ("~a and b", [("~a",), ("b",)]),
        ("~a and ~b", [("~a",), ("~b",)]),
        ("a and b", [("a",), ("b",)]),
        ("a and b | c", [("a",), ("b", "c")]),
        ("a and b | ~c", [("a",), ("b", "~c")]),
        ("~a | ~b and c", [("~a", "~b"), ("c",)]),
    ],
)
def test_parse_cnf_description(input: str, output: ClueCNF):
    assert parse_cnf_description(input) == output


@pytest.mark.parametrize(
    ("input", "output"),
    [
        (["a"], "a"),
        (["~a"], "~a"),
        (["~a", "~b"], "~a and ~b"),
        (["a", "b", "c"], "a and b and c"),
        (["a", "b", "~c"], "a and b and ~c"),
        (["~a", "b", "c"], "~a and b and c"),
        (["~a", "~b", "~c"], "~a and ~b and ~c"),
        (["a", "~a", "b"], "a and ~a and b"),
    ],
)
def test_all_of(input: list[SATLiteral], output: str):
    """
    Tests for all_of. This tests that, given a sequence of literals that must all be satisfied,
    the output simply converts each literal to its own clause. That is, since the output is a CNF
    (an "and" of "ors"), the "and"s operate on each literal itself.

    a -> a
    ~a -> a
    a and b -> (a) and (b)
    a and b and ~c -> (a) and (b) and (~c)
    """

    assert all_of(input) == parse_cnf_description(output)


@pytest.mark.parametrize(
    ("input", "output"),
    [
        (["a"], "a"),
        (["a", "~a"], "a | ~a"),
        (["~a"], "~a"),
        (["a", "b"], "a | b"),
        (["~a", "~b"], "~a | ~b"),
        (["a", "~b"], "a | ~b"),
        (["a", "b", "c"], "a | b | c"),
    ],
)
def test_some_of(input: list[SATLiteral], output: str):
    assert some_of(input) == parse_cnf_description(output)


@pytest.mark.parametrize(
    ("input", "output"),
    [
        (
            ["a", "b", "~c"],
            [
                ("a", "b", "~c"),
                ("~a", "~b"),
                ("~a", "c"),
                ("~b", "c"),
            ],
        ),
        (
            ["a", "b", "c"],
            [
                ("a", "b", "c"),
                ("~a", "~b"),
                ("~a", "~c"),
                ("~b", "~c"),
            ],
        ),
    ],
)
def test_one_of(input: list[SATLiteral], output: ClueCNF):
    assert set(one_of(input)) == set(output)  # order doesn't matter


@pytest.mark.parametrize(
    ("input", "output"),
    [
        (["a"], "~a"),
        (["~a"], "a"),
        (["a", "b", "~c"], "~a and ~b and c"),
        (["a", "b", "c"], "~a and ~b and ~c"),
    ],
)
def test_none_of(input: list[SATLiteral], output: str):
    assert set(none_of(input)) == set(parse_cnf_description(output))


@pytest.mark.parametrize(
    ("input", "output"),
    [
        ("a", "a"),
        ("~a", "~a"),
        ("b", "b"),
        ("~b", "~b"),
    ],
)
def test_basic_fact(input: SATLiteral, output: str):
    assert basic_fact(input) == parse_cnf_description(output)
