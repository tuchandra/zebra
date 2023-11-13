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

from src.elements import PuzzleElement
from src.generate import generate_all_clues, print_puzzle, reduce_clues
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


def shuffle[T](seq: Sequence[T]) -> Sequence[T]:
    """Shuffle a list and return the result."""

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
            TropicalTraptorPrimary: shuffle(list(TropicalTraptorPrimary.__members__.values())),
            TropicalTraptorSecondary: shuffle(list(TropicalTraptorSecondary.__members__.values())),
            TropicalTraptorTertiary: shuffle(list(TropicalTraptorTertiary.__members__.values())),
        }
    elif traptor_type == MythicalTraptorPrimary:
        puzzle_elements = puzzle_elements | {
            MythicalTraptorPrimary: shuffle(list(MythicalTraptorPrimary.__members__.values())),
            MythicalTraptorSecondary: shuffle(list(MythicalTraptorSecondary.__members__.values())),
            MythicalTraptorTertiary: shuffle(list(MythicalTraptorTertiary.__members__.values())),
        }
    else:
        raise ValueError("Invalid choice - what?")

    # Add smoothies? which ones?
    use_smoothies = select("Should the puzzle include smoothies?", [Choice("Yes", True), Choice("No", False)])
    if use_smoothies:
        smoothies = checkbox(
            "Which smoothies should be included? (Choose 5)",
            [Choice(smoothie.value, smoothie) for smoothie in Smoothie],
        )
        puzzle_elements[Smoothie] = shuffle(smoothies)

    # Add bottlecaps? (There are only 5, so no need to choose which colors)
    use_bottlecaps = select("Should the puzzle include bottlecaps?", [Choice("Yes", True), Choice("No", False)])
    if use_bottlecaps:
        puzzle_elements[Bottlecap] = shuffle(list(Bottlecap.__members__.values()))

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
    )

    print(puzzle)

    clues = generate_all_clues(puzzle, solution)

    print(f"\nStarting puzzle reduction ...\n{'-' * 30}")
    reduced, extras = reduce_clues(puzzle, clues)
    for clue in reduced:
        puzzle.add_clue(clue)

    print_puzzle(puzzle_elements, puzzle, extras)
