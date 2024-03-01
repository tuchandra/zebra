import logging
import random
from collections.abc import Iterable, Mapping
from itertools import product

from src.clues import (
    Clue,
    beside,
    consecutive,
    found_at,
    left_of,
    not_at,
    one_between,
    right_of,
    same_house,
    two_between,
)
from src.elements import PuzzleElement
from src.puzzle import Puzzle
from src.sat_utils import itersolve

type Clues = set[Clue]
type ElementPairs = set[tuple[PuzzleElement, PuzzleElement]]
type Solution = Mapping[PuzzleElement, int]


logger = logging.getLogger(__name__)


class UnsolvablePuzzleError(Exception):
    """Raised when a puzzle has no solutions."""

    ...


def _generate_found_at(puzzle: Puzzle, solution: Solution) -> Clues:
    """Generate the `found_at` / `not_at` Clue instances"""

    clues: Clues = set()
    for element, loc in solution.items():
        clues.add(found_at(element, loc))

        for house in puzzle.houses:
            if house != loc:
                clues.add(not_at(element, house))

    return clues


def _generate_same_house(puzzle: Puzzle, solution: Solution) -> Clues:
    """Generate the `same_house` Clue instances"""

    clues: Clues = set()
    for house in puzzle.houses:
        items_at_house = {item: loc for item, loc in solution.items() if loc == house}
        pairs: ElementPairs = {(item1, item2) for item1, item2 in product(items_at_house, repeat=2) if item1 != item2}
        for pair in pairs:
            clues.add(same_house(pair[0], pair[1], puzzle.houses))

    return clues


def _generate_consecutive_beside(puzzle: Puzzle, solution: Solution) -> Clues:
    """Generate the `consecutive` / `beside` Clue instances

    (Note that consecutive is just a more informative version of beside. Since they have the same
    structure, for every possible combination we'll just keep one.)
    """

    clues: Clues = set()
    for left, right in zip(puzzle.houses, puzzle.houses[1:], strict=False):
        items_left = {item: loc for item, loc in solution.items() if loc == left}
        items_right = {item: loc for item, loc in solution.items() if loc == right}
        pairs: ElementPairs = set(product(items_left, items_right))
        for pair in pairs:
            # Prefer beside over consecutive
            if random.random() > 0.8:
                clues.add(consecutive(pair[0], pair[1], puzzle.houses))
            else:
                clues.add(beside(pair[0], pair[1], puzzle.houses))

    return clues


def _generate_left_right_of(puzzle: Puzzle, solution: Solution) -> Clues:
    """Generate the `left_of` / `right_of` Clue instances

    Note that since (x left-of y) is guaranteed to be redundant with (b right-of a), we only add
    one of these clues to the final set.
    """

    clues: Clues = set()
    for left, right in product(puzzle.houses, puzzle.houses):
        if left >= right:
            continue

        items_left = {item: loc for item, loc in solution.items() if loc == left}
        items_right = {item: loc for item, loc in solution.items() if loc == right}
        pairs: ElementPairs = set(product(items_left, items_right))
        for pair in pairs:
            if random.randint(0, 1) == 0:
                clues.add(left_of(pair[0], pair[1], puzzle.houses))
            else:
                clues.add(right_of(pair[1], pair[0], puzzle.houses))

    return clues


def _generate_one_between(puzzle: Puzzle, solution: Solution) -> Clues:
    """Generate the `one_between` Clue instances"""

    clues: Clues = set()
    for left, right in zip(puzzle.houses, puzzle.houses[2:], strict=False):
        items_left = {item: loc for item, loc in solution.items() if loc == left}
        items_right = {item: loc for item, loc in solution.items() if loc == right}
        pairs: ElementPairs = set(product(items_left, items_right))
        for pair in pairs:
            clues.add(one_between(pair[0], pair[1], puzzle.houses))

    return clues


def _generate_two_between(puzzle: Puzzle, solution: Solution) -> Clues:
    """Generate the `two_between` Clue instances"""

    clues: Clues = set()
    for left, right in zip(puzzle.houses, puzzle.houses[3:], strict=False):
        items_left = {item: loc for item, loc in solution.items() if loc == left}
        items_right = {item: loc for item, loc in solution.items() if loc == right}
        pairs: ElementPairs = set(product(items_left, items_right))
        for pair in pairs:
            clues.add(two_between(pair[0], pair[1], puzzle.houses))

    return clues


def generate_all_clues(puzzle: Puzzle, solution: Solution) -> Clues:
    """Generate all clues by invoking all of the `generate_x` functions."""

    clues: Clues = set()
    for generate_function in (
        _generate_found_at,
        _generate_same_house,
        _generate_consecutive_beside,
        _generate_left_right_of,
        _generate_one_between,
        _generate_two_between,
    ):
        clues = clues.union(generate_function(puzzle, solution))

    return clues


def has_unique_solution(puzzle: Puzzle, clues: Iterable[Clue]) -> bool:
    """Test if a puzzle has a unique solution under a given set of clues; return bool or raise UnsolvablePuzzleError."""

    with puzzle.with_clues(clues):
        logger.debug(f"Testing puzzle with {len(puzzle.clues)} clues")
        solutions = itersolve(puzzle.as_cnf())
        try:
            next(solutions)
        except StopIteration:
            logger.debug("Puzzle has no solutions at all.")
            raise UnsolvablePuzzleError("Puzzle has no solutions!") from None

    # test if second solution exists or not; if it doesn't, uniquely solvable
    has_another = next(solutions, None) is None
    logger.debug(f"Puzzle has another solution: {has_another}")
    return has_another


def reduce_batch(puzzle: Puzzle, clues: Clues, n: int) -> Clues:
    """
    Attempt to remove `n` clues from a set of candidate clues. If so, return the new, smaller set
    of clues. If not, return the original set.
    """

    def weight(clue: Clue) -> float:
        """Relative probabilities of each type of clue being selected for removal; lower = more likely to be in the puzzle."""

        weights: dict[type[Clue], float] = {
            not_at: 1,
            same_house: 2,
            one_between: 2,
            beside: 3,
            found_at: 4,
            two_between: 5,
            left_of: 5,
            right_of: 5,
        }

        return weights.get(type(clue), 1)

    candidates: Clues = set(random.choices(list(clues), [weight(clue) for clue in clues], k=n))

    clues = clues.difference(candidates)
    try:
        uniquely_solvable = has_unique_solution(puzzle, clues)
    except UnsolvablePuzzleError:
        uniquely_solvable = False

    if uniquely_solvable:
        logger.debug(f"Removed {len(candidates)} clues.")
        return clues

    # We removed too many clues; add them back and let the caller take care of it.
    clues = clues | candidates
    return clues


def reduce_individually(puzzle: Puzzle, clues: Clues, removed: Clues) -> tuple[Clues, Clues]:
    """
    Attempt to remove each candidate clue one by one.

    The sets `clues` and `removed` are modified in-place. Unnecessary clues get removed from `clues`
    and added to `removed`. If no clues can be removed, we return the original two sets.
    """

    candidates = random.sample(tuple(clues), len(clues))
    for clue in candidates:
        clues.remove(clue)
        try:
            uniquely_solvable = has_unique_solution(puzzle, clues)
        except UnsolvablePuzzleError:
            uniquely_solvable = False

        if uniquely_solvable:
            logger.info(f"Removed {clue=}; {len(clues)} remaining")
            removed.add(clue)
            continue  # we were fine to remove this clue
        clues.add(clue)

    return clues, removed


def reduce_clues(puzzle: Puzzle, clues: Clues) -> tuple[Clues, Clues]:
    """
    Reduce a set of clues to a minimally solvable set.

    A minimally solvable 5-house, 4-attribute puzzle takes between 10 and 20 clues to solve. The
    original set of clues will likely be in the hundreds, and the majority are likely to be
    redundant. We can quickly reduce the set of clues by batch removing clues from the large
    candidate pool.

    The algorithm for batch reduction:
     1. shuffle all the clues
     2. attempt to remove 10% of the clues; with this 90%-clue set, test if the puzzle is solvable.
     3a. if yes: keep them removed, go back to 2 and repeat
     3b. if no: add them back, keep going to 4
     4. the same as step (3), but this time trying to remove 5% of the clues
     5. the same as step (3), but this time trying to remove a single clue

    After we've tried and failed to remove a *single* clue, then the (first part of the) reduction
    algorithm is done; having that clue was necessary for us to have a unique solution. This doesn't
    necessarily mean that *all* the clues are need, though, which is what the secondary reduction
    is for.

    The *secondary reduction process* is much simpler: now that the set is narrowed substantially,
    we can be more brute-forcey. Attempt to remove each clue and see if the puzzle is still
    solvable.

    However, the secondary reduction process can result in a puzzle that is *too hard* to solve
    (though technically uniquely solvable by a computer or sufficiently skilled human). This
    algorithm returns a second set of clues that were removed during the secondary reduction
    process. These can be thought of as extra clues to add or hints to give to anyone solving the
    puzzle.
    """

    # this is a stupid way to shuffle the set of clues without modifying it
    minimal_clues = set(random.sample(tuple(clues), k=len(clues)))

    logger.info(f"Starting to reduce clues from maximal set of {len(clues)}.")
    while True:
        logger.debug(f"Testing puzzle with {len(minimal_clues)} clues.")

        # If the size of minimal_clues before we try to remove some clues is greater than the size
        # after, then those clues were fine to remove. Go back to the top of the loop and keep
        # removing more. But if the size is the same, we needed some of those clues. Try to remove
        # a smaller amount.
        #
        # We use the walrus operator to update minimal_clues in place during the comparison. It'll
        # either be a reduced set of clues or the original set of clues.
        if len(minimal_clues) > len(minimal_clues := reduce_batch(puzzle, minimal_clues, len(minimal_clues) // 10)):
            continue

        if len(minimal_clues) != len(minimal_clues := reduce_batch(puzzle, minimal_clues, len(minimal_clues) // 20)):
            continue

        if len(minimal_clues) == len(minimal_clues := reduce_batch(puzzle, minimal_clues, 1)):
            break

    # secondary reduction time! While we can still remove clues, do so; then we're done.
    logger.info(f"Reached {len(minimal_clues)} clues; attempting to reduce further.")
    removed_clues: Clues = set()
    while True:
        minimal_clues_size = len(minimal_clues)
        # minimal_clues, removed_clues = reduce_individually(puzzle, minimal_clues, removed_clues)
        if len(minimal_clues) == minimal_clues_size:
            break

    return minimal_clues, removed_clues
