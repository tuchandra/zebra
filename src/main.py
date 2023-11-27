"""
main.py

CLI for the puzzle generator. This is intended to supersede generate.py, but
we'll see.
"""

import logging
import random
from collections.abc import Sequence
from dataclasses import dataclass

import questionary
from rich.logging import RichHandler

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

logging.basicConfig(level=logging.DEBUG, format="%(message)s", handlers=[RichHandler(level=logging.INFO)])
logger = logging.getLogger(__name__)


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

    element_types: set[type[PuzzleElement]]
    traptor_type = select(
        "Choose a Traptor type",
        [Choice("🌴 Tropical", TropicalTraptorPrimary), Choice("🏰 Mythical", MythicalTraptorPrimary)],
    )
    if traptor_type == TropicalTraptorPrimary:
        element_types = {TropicalTraptorPrimary, TropicalTraptorSecondary, TropicalTraptorTertiary}
    elif traptor_type == MythicalTraptorPrimary:
        element_types = {MythicalTraptorPrimary, MythicalTraptorSecondary, MythicalTraptorTertiary}
    else:
        raise ValueError("Invalid choice - what?")

    # Add smoothies?
    use_smoothies = select("🥤 Should the puzzle include smoothies?", [Choice("Yes", True), Choice("No", False)])
    if use_smoothies:
        element_types = element_types | {Smoothie}

    # Add bottlecaps?
    use_bottlecaps = select("🔵 Should the puzzle include bottlecaps?", [Choice("Yes", True), Choice("No", False)])
    if use_bottlecaps:
        element_types = element_types | {Bottlecap}

    logger.info(f"Puzzle element types: {element_types}")

    # Choose elements for each type randomly
    puzzle_elements: dict[type[PuzzleElement], Sequence[PuzzleElement]] = {}
    for el_type in element_types:
        puzzle_elements[el_type] = shuffle(list(el_type.__members__.values()))[:5]

    # Construct the puzzle
    puzzle = Puzzle(
        size=5,
        element_types=element_types,
        elements=[e for els in puzzle_elements.values() for e in els],
    )

    # Construct solution randomly
    solution: dict[PuzzleElement, int] = {
        # Smoothie.lilac: 1,
        # Smoothie.earth: 2,
        # ...,
        # TraptorPrimary.marvellous: 1,
        # TraptorPrimary.heroic: 2,
        # ...,
        el: house
        for _, elements in puzzle_elements.items()
        for house, el in enumerate(elements, 1)
    }

    clues = generate_all_clues(puzzle, solution)

    logger.info("Starting puzzle reduction!")
    reduced, extras = reduce_clues(puzzle, clues)
    for clue in reduced:
        puzzle.add_clue(clue)

    print_puzzle(puzzle_elements, puzzle, extras)
