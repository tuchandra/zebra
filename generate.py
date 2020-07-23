"""
puzzle_generator.py

This is a driver script that can be used to generate new zebra puzzles.
"""

from itertools import product
from random import choices, randint, sample
from typing import Dict, Iterable, List, Set, Tuple, Type

from clues import (
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
from literals import *
from puzzle import Puzzle
from sat_utils import itersolve


def generate_found_at(puzzle: Puzzle, solution: Dict[Literal, int]) -> Set[Clue]:
    """Generate the `found_at` / `not_at` Clue instances"""

    clues: Set[Clue] = set()
    for element, loc in solution.items():
        clues.add(found_at(element, loc))

        for house in puzzle.houses:
            if house != loc:
                clues.add(not_at(element, house))

    return clues


def generate_same_house(puzzle: Puzzle, solution: Dict[Literal, int]) -> Set[Clue]:
    """Generate the `same_house` Clue instances"""

    clues: Set[Clue] = set()
    for house in puzzle.houses:
        items_at_house = {item: loc for item, loc in solution.items() if loc == house}
        pairs: Set[Tuple[Literal, Literal]] = {
            (item1, item2) for item1, item2 in product(items_at_house, repeat=2) if item1 != item2
        }
        for pair in pairs:
            clues.add(same_house(pair[0], pair[1], puzzle.houses))

    return clues


def generate_consecutive_beside(puzzle: Puzzle, solution: Dict[Literal, int]) -> Set[Clue]:
    """Generate the `consecutive` / `beside` Clue instances

    (Note that consecutive is just a more informative version of beside. Since they have the same
    structure, for every possible combination we'll just keep one.
    """

    clues: Set[Clue] = set()
    for left, right in zip(puzzle.houses, puzzle.houses[1:]):
        items_left = {item: loc for item, loc in solution.items() if loc == left}
        items_right = {item: loc for item, loc in solution.items() if loc == right}
        pairs: Set[Tuple[Literal, Literal]] = {
            (item1, item2) for item1, item2 in product(items_left, items_right)
        }
        for pair in pairs:
            # consecutive is just a more informative version of beside, but they have same structure
            # because of this, don't include both
            if randint(0, 1) == 0:
                clues.add(consecutive(pair[0], pair[1], puzzle.houses))
            else:
                clues.add(beside(pair[0], pair[1], puzzle.houses))

    return clues


def generate_left_right_of(puzzle: Puzzle, solution: Dict[Literal, int]) -> Set[Clue]:
    """Generate the `left_of` / `right_of` Clue instances
    
    Note that since (x left-of y) is guaranteed to be redundant with (b right-of a), we only add
    one of these clues to the final set.
    """

    clues: Set[Clue] = set()
    for left, right in product(puzzle.houses, puzzle.houses):
        if left >= right:
            continue

        items_left = {item: loc for item, loc in solution.items() if loc == left}
        items_right = {item: loc for item, loc in solution.items() if loc == right}
        pairs: Set[Tuple[Literal, Literal]] = {
            (item1, item2) for item1, item2 in product(items_left, items_right)
        }
        for pair in pairs:
            if randint(0, 1) == 0:
                clues.add(left_of(pair[0], pair[1], puzzle.houses))
            else:
                clues.add(right_of(pair[1], pair[0], puzzle.houses))

    return clues


def generate_one_between(puzzle: Puzzle, solution: Dict[Literal, int]) -> Set[Clue]:
    """Generate the `one_between` Clue instances"""

    clues: Set[Clue] = set()
    for left, right in zip(puzzle.houses, puzzle.houses[2:]):
        items_left = {item: loc for item, loc in solution.items() if loc == left}
        items_right = {item: loc for item, loc in solution.items() if loc == right}
        pairs: Set[Tuple[Literal, Literal]] = {
            (item1, item2) for item1, item2 in product(items_left, items_right)
        }
        for pair in pairs:
            clues.add(one_between(pair[0], pair[1], puzzle.houses))

    return clues


def generate_two_between(puzzle: Puzzle, solution: Dict[Literal, int]) -> Set[Clue]:
    """Generate the `two_between` Clue instances"""

    clues: Set[Clue] = set()
    for left, right in zip(puzzle.houses, puzzle.houses[3:]):
        items_left = {item: loc for item, loc in solution.items() if loc == left}
        items_right = {item: loc for item, loc in solution.items() if loc == right}
        pairs: Set[Tuple[Literal, Literal]] = {
            (item1, item2) for item1, item2 in product(items_left, items_right)
        }
        for pair in pairs:
            clues.add(two_between(pair[0], pair[1], puzzle.houses))

    return clues


def has_unique_solution(puzzle: Puzzle, clues: Iterable[Clue]) -> bool:
    """Test if a puzzle has a unique solution under a given set of clues."""

    with puzzle.with_clues(clues):
        print(f"Testing puzzle with {len(puzzle.clues)} clues")
        solutions = itersolve(puzzle.as_cnf())
        _first_solution = next(solutions)

        # test if second solution exists or not; if it doesn't, uniquely solvable
        if next(solutions, None) is None:
            return True
        else:
            return False


def try_to_remove(puzzle: Puzzle, clues: Set[Clue], n: int) -> Set[Clue]:
    """
    Attempt to remove n clues from a set of candidate clues; if we are able to, return the new,
    smaller set of clues. If not, return the original set.
    """

    def weight(clue: Clue) -> float:
        # relative probabilities of each type of clue being selected for removal
        weights: Dict[Type[Clue], float] = {
            not_at: 0.5,
            found_at: 1,
            left_of: 1.5,
            right_of: 1.5,
            one_between: 2,
            two_between: 2,
        }

        return weights.get(type(clue), 1)

    weights = [weight(clue) for clue in clues]
    candidates: Set[Clue] = set(choices(list(clues), weights, k=n))

    clues = clues.difference(candidates)
    if has_unique_solution(puzzle, clues):
        print(f"Removed {len(candidates)} clues.")
        return clues

    # we needed at least one of those, add them all back
    clues = clues | candidates
    return clues


def reduce_individually(puzzle: Puzzle, clues: Set[Clue]) -> Set[Clue]:
    """
    Attempt to remove each candidate clue one by one. If the puzzle remains uniquely solvable,
    return the reduced set. If not, return the original.
    """

    candidates = sample(clues, len(clues))
    for clue in candidates:
        clues.remove(clue)
        if has_unique_solution(puzzle, clues):
            print(f"Removed {clue=}")
            continue  # we were fine to remove this clue
        clues.add(clue)

    return clues


def reduce_clues(puzzle: Puzzle, clues: Set[Clue]) -> Set[Clue]:
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

    """

    # this is a stupid way to shuffle the set of clues without modifying it
    minimal_clues = set(sample(clues, k=len(clues)))

    while True:
        print(f"There are {len(minimal_clues)} clues in ba sing se")

        # Walrus time!
        #
        # If the size of minimal_clues before we try to remove some clues is greater than the size
        # after, then those clues were fine to remove. Go back to the top of the loop and keep
        # removing more. But if the size is the same, we needed some of those clues. Try to remove
        # a smaller amount.
        #
        # We use the walrus operator to update minimal_clues in place during the comparison. It'll
        # either be a reduced set of clues or the original set of clues.
        if len(minimal_clues) > len(
            (minimal_clues := try_to_remove(puzzle, minimal_clues, len(minimal_clues) // 10))
        ):
            continue

        if len(minimal_clues) != len(
            (minimal_clues := try_to_remove(puzzle, minimal_clues, len(minimal_clues) // 20))
        ):
            continue

        if len(minimal_clues) == len((minimal_clues := try_to_remove(puzzle, minimal_clues, 1))):
            break

    # secondary reduction time! While we can still remove clues, do so; then we're done.
    print(f"Starting the secondary reduction.")
    while len(minimal_clues) > len((minimal_clues := reduce_individually(puzzle, minimal_clues))):
        pass

    return minimal_clues


import random

if __name__ == "__main__":
    random.seed(12)
    elements = [Kaya, Smoothie, Tribe, FavoriteGame]

    # this will be the solution
    solution: Dict[Literal, int] = {
        Smoothie.blueberry: 1,
        Smoothie.butterscotch: 2,
        Smoothie.phantom_spring: 3,
        Smoothie.lemon: 4,
        Smoothie.sakura: 5,
        FavoriteGame.quality_assurance: 1,
        FavoriteGame.dirt_digger: 2,
        FavoriteGame.fishing_fever: 3,
        FavoriteGame.wonder_wheel: 4,
        FavoriteGame.guess_the_number: 5,
        Tribe.quake: 1,
        Tribe.cursed: 2,
        Tribe.storm: 3,
        Tribe.forest: 4,
        Tribe.volcano: 5,
        Kaya.life: 1,
        Kaya.joy: 2,
        Kaya.wisdom: 3,
        Kaya.love: 4,
        Kaya.harmony: 5,
    }

    # set up the puzzle with default constraints
    puzzle = Puzzle(element_types=elements, elements=solution.keys(), n_houses=5).set_constraints()
    print(puzzle)

    # generate all the clues
    clues: Set[Clue] = set()
    for generate_function in (
        generate_found_at,
        generate_same_house,
        generate_consecutive_beside,
        generate_left_right_of,
        generate_one_between,
        generate_two_between,
    ):
        clues = clues.union(generate_function(puzzle, solution))

    reduced = reduce_clues(puzzle, clues)
    for clue in reduced:
        puzzle.add_clue(clue)

    print(puzzle)
