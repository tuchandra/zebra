"""
puzzle_generator.py

This is a driver script that can be used to generate new zebra puzzles.
"""

from itertools import product
from typing import Dict, Iterable, Set, Sized, Tuple
from random import sample, randint

from puzzle import Puzzle
from sat_utils import solve_one

from clues import (
    Clue,
    comb,
    found_at,
    same_house,
    consecutive,
    beside,
    left_of,
    right_of,
    one_between,
    two_between,
)

from literals import (
    Literal,
    Kiro,
    Bottlecap,
    Smoothie,
    RecolorMedal,
)


elements = [Kiro, Bottlecap, Smoothie, RecolorMedal]

# set up the puzzle with default constraints
puzzle = Puzzle(elements=elements, n_houses=5).set_constraints()

# this will be the solution
solution: Dict[Literal, int] = {
    Kiro.kaya: 1,
    Kiro.sugar_sketch: 2,
    Kiro.skeleko: 3,
    Kiro.silosaur: 4,
    Kiro.traptor_costume: 5,
    Bottlecap.yellow: 1,
    Bottlecap.silver: 2,
    Bottlecap.red: 3,
    Bottlecap.green: 4,
    Bottlecap.blue: 5,
    Smoothie.watermelon: 1,
    Smoothie.dusk: 2,
    Smoothie.spring: 3,
    Smoothie.lilac: 4,
    Smoothie.cherry: 5,
    RecolorMedal.second_ed: 1,
    RecolorMedal.gold: 2,
    RecolorMedal.pink: 3,
    RecolorMedal.first: 4,
    RecolorMedal.ghost: 5,
}

# generate found-at clues
clues: Set[Clue] = set()
for element, loc in solution.items():
    clues.add(found_at(element, loc))


# generate same-house clues
for house in puzzle.houses:
    items_at_house = {item: loc for item, loc in solution.items() if loc == house}
    pairs: Set[Tuple[Literal, Literal]] = {
        (item1, item2) for item1, item2 in product(items_at_house, repeat=2) if item1 != item2
    }
    for pair in pairs:
        clues.add(same_house(pair[0], pair[1], puzzle.houses))

# generate consecutive and beside clues
for left, right in zip(puzzle.houses, puzzle.houses[1:]):
    items_left = {item: loc for item, loc in solution.items() if loc == left}
    items_right = {item: loc for item, loc in solution.items() if loc == right}
    pairs: Set[Tuple[Literal, Literal]] = {
        (item1, item2) for item1, item2 in product(items_left, items_right)
    }
    for pair in pairs:
        # consecutive is just a more informative version of beside, but they have same structure
        clues.add(consecutive(pair[0], pair[1], puzzle.houses))
        clues.add(beside(pair[0], pair[1], puzzle.houses))

# generate left-of and right-of clues
for left, right in product(puzzle.houses, puzzle.houses):
    if left >= right:
        continue

    items_left = {item: loc for item, loc in solution.items() if loc == left}
    items_right = {item: loc for item, loc in solution.items() if loc == right}
    pairs: Set[Tuple[Literal, Literal]] = {
        (item1, item2) for item1, item2 in product(items_left, items_right)
    }
    for pair in pairs:
        # (a left-of b) is guaranteed to be redundant with (b right-of a), so only add one
        if randint(0, 2) == 0:
            clues.add(left_of(pair[0], pair[1], puzzle.houses))
        else:
            clues.add(right_of(pair[1], pair[0], puzzle.houses))

print(*clues, sep="\n")

from sat_utils import itersolve


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


def reduce_clues(puzzle: Puzzle, clues: Set[Clue]) -> Set[Clue]:
    """
    Reduce a set of clues to a minimally solvable set.

    A minimally solvable 5-house, 4-attribute puzzle takes between 10 and 20 clues to solve. The
    original set of clues will likely be in the hundreds, and the majority are likely to be
    redundant. We can observe significant time gains by batch removing clues from a large candidate
    pool.

    The algorithm:
     - select a random ordering of the candidate clues
     - consider smaller_clues, which is clues without the first (random) candidate
     - if the puzzle is uniquely solvable under smaller_clues, continue
     - if the puzzle is not uniquely solvable, the candidate was necessary, so add it back and return

    The algorithm for batch reduction (not yet done!):
     - if there are more than 100 clues, remove a random 10% of them
     - with this 90%-clue set, test if the puzzle is solvable
     - if the puzzle is uniquely solvable, continue removing
     - if the puzzle is not uniquely solvable, one of the candidates in the set was necessary;
       add them all back and fall back to the one-by-one case
    
    """

    # this is a stupid way to shuffle the set of clues without modifying it
    minimal_clues = set(sample(clues, k=len(clues)))

    while True:
        print(f"There are {len(minimal_clues)} clues in ba sing se")
        candidate = minimal_clues.pop()
        if has_unique_solution(puzzle, minimal_clues):
            print(f"Removed clue: {candidate}")
            continue  # we were fine to remove this clue

        # removing that clue made the puzzle unsolvable; add it back in and we're done.
        print(f"Oops, that was a mistake! Adding it back. {candidate=}")
        minimal_clues.add(candidate)
        print(f"There are {len(minimal_clues)} clues in ba sing se")

        return minimal_clues


def secondary_reduction(puzzle: Puzzle, clues: Set[Clue]) -> Set[Clue]:
    """Try to remove a random clue to see if the puzzle is still solvable"""

    for candidate in sample(clues, len(clues)):
        smaller_clues = clues.difference(set([candidate]))
        if has_unique_solution(puzzle, smaller_clues):
            print(f"Removing {candidate=}")
            return smaller_clues  # we were fine to remove this clue

    # all clues were required to solve the puzzle
    print(f"All clues were required!")
    return clues


print(f"Puzzle has {len(puzzle.clues)} clues")
print(has_unique_solution(puzzle, clues))
reduced = reduce_clues(puzzle, clues)
for _ in range(20):
    reduced = secondary_reduction(puzzle, reduced)
