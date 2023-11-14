"""
Utility functions that humanize interaction wtih pycosat. Originally written by Raymond Hettinger.

My modifications include adding type hints, renaming variables and methods, and removing unused code.
Other parts of the codebase shouldn't need to interact with pycosat directly, and instead should use
this module as an interface; this also lets us localize the `pyright: ignore` comments in one place.
"""

from collections.abc import Iterable, Sequence
from functools import cache
from itertools import combinations
from typing import Any, NewType

import pycosat  # pyright: ignore[reportMissingImports]

SATLiteral = NewType("SATLiteral", str)
type Clause = Sequence[SATLiteral]
type ClueCNF = Sequence[Clause]


@cache
def negate(element: SATLiteral) -> SATLiteral:
    """Negate a literal; that is, X -> not X, not X -> X. Represented as X and ~X, respectively."""

    return SATLiteral(element[1:] if element.startswith("~") else "~" + element)


def make_translate(cnf: ClueCNF) -> tuple[dict[SATLiteral, int], dict[int, SATLiteral]]:
    """
    Create translation tables between symbolic CNF literals and pycosat's numeric literals, since
    the pycosat solver expects literals as numbers. Return two lookup dictionaries.

    >>> make_translate([['~a', 'b', '~c'], ['a', '~c']])
    => (
      {'a': 1, 'c': 3, 'b': 2, '~a': -1, '~b': -2, '~c': -3},
      {1: 'a', 2: 'b', 3: 'c', -1: '~a', -3: '~c', -2: '~b'},
    )

    Here, we distinguish between literals (a, ~a, b, ~b, ...) and variables (a, b, c, ...); each
    variable `x` can be either true or false, and we express these as the literals `x` and `~x`.

    This function iterates over the CNF (containing literals like `a` and `~b`) and, for each
    variable, adds the literal and its negation to the translation tables. We keep track of 'true'
    variables with positive integers and 'false' variables with negative ones.
    """

    literals_to_numbers: dict[SATLiteral, int] = {}
    for clause in cnf:
        for literal in clause:
            # Skip literals that we've seen (or whose negation we've seen)
            if literal in literals_to_numbers:
                continue

            num = max(literals_to_numbers.values(), default=0) + 1

            # Get the 'true' and 'false' literals from the input, which could be either
            if literal.startswith("~"):
                true_literal, false_literal = negate(literal), literal
            else:
                true_literal, false_literal = literal, negate(literal)

            literals_to_numbers[true_literal] = num
            literals_to_numbers[false_literal] = -num

    numbers_to_literals = {num: lit for lit, num in literals_to_numbers.items()}

    return literals_to_numbers, numbers_to_literals


def translate(cnf: ClueCNF, uniquify: bool = False) -> tuple[list[tuple[int, ...]], dict[int, SATLiteral]]:
    """Translate a symbolic CNF to a numbered CNF and return reverse mapping.

    >>> translate([['~P', 'Q'],['~P', 'R']])
    [(-1, 2), (-1, 3)], {-3: '~R', -2: '~Q', -1: '~P', 1: 'P', 2: 'Q', 3: 'R'}
    """

    # DIMACS CNF file format:
    # http://people.sc.fsu.edu/~jburkardt/data/cnf/cnf.html
    if uniquify:
        cnf = list(dict.fromkeys(cnf))

    lit2num, num2var = make_translate(cnf)
    numbered_cnf = [tuple([lit2num[lit] for lit in clause]) for clause in cnf]

    return numbered_cnf, num2var


def itersolve(symbolic_cnf: ClueCNF):
    numbered_cnf, num2var = translate(symbolic_cnf)

    for solution in pycosat.itersolve(numbered_cnf):  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        yield [num2var[n] for n in solution if n > 0]  # pyright: ignore[reportUnknownVariableType, reportUnknownArgumentType]


def compare_cnfs(cnf1: ClueCNF, cnf2: ClueCNF) -> bool:
    """Helper to compare two CNFs, since the clauses are unordered."""

    return set(map(frozenset, cnf1)) == set(map(frozenset, cnf2))


def comb(value: Any, loc: int) -> SATLiteral:
    """Format how a value is shown at a given location"""

    return SATLiteral(f"{value} {loc}")


def from_dnf(groups: Iterable[Clause]) -> ClueCNF:
    """Convert from or-of-ands to and-of-ors

    >>> from_dnf([['~P'], ['Q', 'R']])
    [('~P', 'Q'), ('~P', 'R')]
    """

    cnf: set[frozenset[SATLiteral]] = {frozenset()}
    for group in groups:
        nl = {frozenset([literal]): negate(literal) for literal in group}
        # The "clause | literal" prevents dup lits: {x, x, y} -> {x, y}
        # The nl check skips over identities: {x, ~x, y} -> True
        cnf = {clause | literal for literal in nl for clause in cnf if nl[literal] not in clause}
        # The sc check removes clauses with superfluous terms:
        #     {{x}, {x, z}, {y, z}} -> {{x}, {y, z}}
        # Should this be left until the end?
        sc = min(cnf, key=len)  # XXX not deterministic
        cnf -= {clause for clause in cnf if clause > sc}

    return [tuple(clause) for clause in cnf]


class Q:
    """Quantifier for the number of elements that are true

    >>> Q(['A', 'B', 'C']) <= 1
    [('~A', '~B'),
    ('~A', '~C'),
    ('~B', '~C')]
    """

    def __init__(self, elements: Sequence[SATLiteral]):
        self.elements = tuple(elements)

    def __lt__(self, n: int) -> ClueCNF:
        return list(combinations(map(negate, self.elements), n))

    def __le__(self, n: int) -> ClueCNF:
        return self < n + 1

    def __gt__(self, n: int) -> ClueCNF:
        return list(combinations(self.elements, len(self.elements) - n))

    def __ge__(self, n: int) -> ClueCNF:
        return self > n - 1

    def __eq__(self, n: int) -> ClueCNF:  # pyright: ignore[reportIncompatibleMethodOverride]
        return (self <= n) + (self >= n)

    def __ne__(self, n: Any) -> ClueCNF:  # pyright: ignore[reportIncompatibleMethodOverride]
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(elements={self.elements!r})"


def parse_cnf_description(input: str) -> ClueCNF:
    """
    Parse a CNF description into a list of clauses.

    a and b -> [("a",), ("b",)]
    ~a and ~b -> [("~a",), ("~b",)]
    a and b | c -> [("a",), ("b", "c")]
    a and b | ~c -> [("a",), ("b", "~c")]

    We accomplish this by splitting on " and " to get the clauses, then splitting on " | " to get
    the literals in each clause.
    """

    literals = [x.split(" | ") for x in input.split(" and ")]
    return [tuple(SATLiteral(x) for x in clause) for clause in literals]


def all_of(elements: Sequence[SATLiteral]) -> ClueCNF:
    return Q(elements) == len(elements)


def some_of(elements: Sequence[SATLiteral]) -> ClueCNF:
    return Q(elements) >= 1


def one_of(elements: Sequence[SATLiteral]) -> ClueCNF:
    return Q(elements) == 1


def none_of(elements: Sequence[SATLiteral]) -> ClueCNF:
    return Q(elements) == 0


def basic_fact(element: SATLiteral) -> ClueCNF:
    """Assert that this one element always matches"""
    return Q([element]) == 1
