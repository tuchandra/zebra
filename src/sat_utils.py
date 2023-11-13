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
type Clause = tuple[SATLiteral, ...]
type ClueCNF = list[Clause]


@cache
def negate(element: SATLiteral) -> SATLiteral:
    """Negate a literal; that is, X -> not X, not X -> X. Represented as X and ~X, respectively."""

    return SATLiteral(element[1:] if element.startswith("~") else "~" + element)


def make_translate(cnf: ClueCNF) -> tuple[dict[str, int], dict[int, str]]:
    """
    Create translation tables between symbolic CNF and pycosat's numbered clauses, since pycosat's
    solver expects literals as numbers. Return two lookup dictionaries.

    >>> make_translate([['~a', 'b', '~c'], ['a', '~c']])
    => (
      {'a': 1, 'c': 3, 'b': 2, '~a': -1, '~b': -2, '~c': -3},
      {1: 'a', 2: 'b', 3: 'c', -1: '~a', -3: '~c', -2: '~b'},
    )
    """

    literals_to_numbers: dict[str, int] = {}
    for clause in cnf:
        for literal in clause:
            if literal not in literals_to_numbers:
                var = literal[1:] if literal[0] == "~" else literal
                num = len(literals_to_numbers) // 2 + 1
                literals_to_numbers[var] = num
                literals_to_numbers["~" + var] = -num

    num2var = {num: lit for lit, num in literals_to_numbers.items()}

    return literals_to_numbers, num2var


def translate(cnf: ClueCNF, uniquify: bool = False) -> tuple[list[tuple[int, ...]], dict[int, str]]:
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


# Support for Building CNFs


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


def all_of(elements: Sequence[SATLiteral]) -> ClueCNF:
    """Forces inclusion of matching rows on a truth table"""
    return Q(elements) == len(elements)


def some_of(elements: Sequence[SATLiteral]) -> ClueCNF:
    """At least one of the elements must be true

    >>> some_of(['A', 'B', 'C'])
    [['A', 'B', 'C']]
    """
    return Q(elements) >= 1


def one_of(elements: Sequence[SATLiteral]) -> ClueCNF:
    """Exactly one of the elements is true

    >>> one_of(['A', 'B', 'C'])
    [('A', 'B', 'C'),
    ('~A', '~B'),
    ('~A', '~C'),
    ('~B', '~C')]
    """
    return Q(elements) == 1


def basic_fact(element: SATLiteral) -> ClueCNF:
    """Assert that this one element always matches"""
    return Q([element]) == 1


def none_of(elements: Sequence[SATLiteral]) -> ClueCNF:
    """Forces exclusion of matching rows on a truth table"""
    return Q(elements) == 0
