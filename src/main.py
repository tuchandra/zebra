"""
main.py

CLI for the puzzle generator. This is intended to supersede generate.py, but
we'll see.
"""

import random
from collections.abc import Sequence
from dataclasses import dataclass

import questionary
from rich import print

from src.clues import Clue
from src.elements import PuzzleElement
from src.generate import (
    generate_consecutive_beside,
    generate_found_at,
    generate_left_right_of,
    generate_one_between,
    generate_same_house,
    generate_two_between,
    print_puzzle,
    reduce_clues,
)
from src.puzzle import Puzzle
from src.traptor_elements import (
    Bottlecap,
    MythicalTraptorPrimary,
    MythicalTraptorSecondary,
    MythicalTraptorTertiary,
    Smoothie,
    TropicalTraptorPrimary,
    TropicalTraptorSecondary,
    TropicalTraptorTertiary,
)


@dataclass
class Choice[T]:
    label: str
    value: T


def select[T](question: str, choices: Sequence[Choice[T]]) -> T:
    """Typed wrapper around questionary.select."""

    q = questionary.select(question, choices=[c.label for c in choices])
    answer = q.ask()
    return next(c.value for c in choices if c.label == answer)


def checkbox[T](question: str, choices: Sequence[Choice[T]]) -> list[T]:
    """Typed wrapper around questionary.checkbox."""

    q = questionary.checkbox(question, choices=[c.label for c in choices], validate=lambda x: len(x) == 5)
    answers = q.ask()
    return [c.value for c in choices if c.label in answers]


def sort_randomly[T](seq: Sequence[T]) -> Sequence[T]:
    """Shuffle a list in place."""

    return random.sample(seq, len(seq))


if __name__ == "__main__":
    random.seed(20231112)

    puzzle_elements: dict[type[PuzzleElement], Sequence[PuzzleElement]] = {}
    traptor_type = select(
        "Choose a Traptor type",
        [Choice("🌴 Tropical", TropicalTraptorPrimary), Choice("🏰 Mythical", MythicalTraptorPrimary)],
    )
    if traptor_type == TropicalTraptorPrimary:
        puzzle_elements = puzzle_elements | {
            TropicalTraptorPrimary: sort_randomly(list(TropicalTraptorPrimary.__members__.values())),
            TropicalTraptorSecondary: sort_randomly(list(TropicalTraptorSecondary.__members__.values())),
            TropicalTraptorTertiary: sort_randomly(list(TropicalTraptorTertiary.__members__.values())),
        }
    elif traptor_type == MythicalTraptorPrimary:
        puzzle_elements = puzzle_elements | {
            MythicalTraptorPrimary: sort_randomly(list(MythicalTraptorPrimary.__members__.values())),
            MythicalTraptorSecondary: sort_randomly(list(MythicalTraptorSecondary.__members__.values())),
            MythicalTraptorTertiary: sort_randomly(list(MythicalTraptorTertiary.__members__.values())),
        }
    else:
        raise ValueError("Invalid choice - what?")

    print(traptor_type)

    # add smoothies?
    use_smoothies = select("Should the puzzle include smoothies?", [Choice("Yes", True), Choice("No", False)])
    print(use_smoothies)

    # Which smoothies?
    if use_smoothies:
        smoothies = checkbox(
            "Which smoothies should be included? (Choose 5)",
            [Choice(smoothie.value, smoothie) for smoothie in Smoothie],
        )
        print(smoothies)

        puzzle_elements[Smoothie] = sort_randomly(smoothies)

    # add bottlecaps? (there are only 5, so no need to choose which colors)
    use_bottlecaps = select("Should the puzzle include bottlecaps?", [Choice("Yes", True), Choice("No", False)])
    if use_bottlecaps:
        puzzle_elements[Bottlecap] = sort_randomly(list(Bottlecap.__members__.values()))

    print(puzzle_elements)

    # Construct solution; positions already randomized
    solution: dict[PuzzleElement, int] = {
        # Smoothie.lilac: 1,
        # Smoothie.earth: 2,
        # ...,
        # TraptorPrimary.marvellous: 1,
        # TraptorPrimary.heroic: 2,
        # ...,
        el: house
        for el_class in puzzle_elements
        for house, el in enumerate(puzzle_elements[el_class], 1)
    }

    # Construct the puzzle
    puzzle = Puzzle(
        element_types=puzzle_elements.keys(),
        elements=[e for els in puzzle_elements.values() for e in els],
        n_houses=5,
    )

    print(puzzle)

    # generate all the clues
    clues: set[Clue] = set()
    for generate_function in (
        generate_found_at,
        generate_same_house,
        generate_consecutive_beside,
        generate_left_right_of,
        generate_one_between,
        generate_two_between,
    ):
        clues = clues.union(generate_function(puzzle, solution))

    print(f"\nStarting puzzle reduction ...\n{'-' * 30}")
    reduced, extras = reduce_clues(puzzle, clues)
    for clue in reduced:
        puzzle.add_clue(clue)

    print_puzzle(puzzle_elements, puzzle, extras)
