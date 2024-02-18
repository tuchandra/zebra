"""
main.py - CLI for the puzzle generator superseding the previous generate.py.
"""

import logging
import random
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date

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


def shuffle[T](seq: Sequence[T], n: int | None = None) -> Sequence[T]:
    """Shuffle a list, optionally sample, and return the result."""

    return random.sample(seq, n or len(seq))


def integer_input(x: str) -> bool:
    """Validate that a string is a positive integer."""

    return x.isdigit()


if __name__ == "__main__":
    seed = questionary.text(
        "Choose a seed (to regenerate this puzzle later)",
        default=date.today().isoformat().replace("-", ""),
        validate=integer_input,
    ).ask()
    random.seed(seed)

    puzzle_size = select("How large is the puzzle?", choices=[Choice(str(i), i) for i in (5, 4, 3)])

    element_types: list[type[PuzzleElement]]
    traptor_type = select(
        "Choose a Traptor type",
        [Choice("🌴 Tropical", TropicalTraptorPrimary), Choice("🏰 Mythical", MythicalTraptorPrimary)],
    )
    if traptor_type == TropicalTraptorPrimary:
        element_types = [TropicalTraptorPrimary, TropicalTraptorSecondary, TropicalTraptorTertiary]
    elif traptor_type == MythicalTraptorPrimary:
        element_types = [MythicalTraptorPrimary, MythicalTraptorSecondary, MythicalTraptorTertiary]
    else:
        raise ValueError("Invalid choice - what?")

    # Add smoothies?
    use_smoothies = select("🥤 Should the puzzle include smoothies?", [Choice("Yes", True), Choice("No", False)])
    if use_smoothies:
        element_types += [Smoothie]

    # Add bottlecaps?
    use_bottlecaps = select("🔵 Should the puzzle include bottlecaps?", [Choice("Yes", True), Choice("No", False)])
    if use_bottlecaps:
        element_types += [Bottlecap]

    logger.info(f"Puzzle element types: {element_types}")

    # Choose elements for each type
    puzzle_elements: dict[type[PuzzleElement], list[PuzzleElement]] = {}
    for el_type in element_types:
        puzzle_elements[el_type] = random.sample(list(el_type.__members__.values()), puzzle_size)

    # Construct solution (shuffle again)
    solution = {
        element: loc
        for _eltype, elements in puzzle_elements.items()
        for loc, element in enumerate(shuffle(elements), 1)
    }

    # Construct the puzzle
    puzzle = Puzzle(
        element_types=element_types,
        elements=[e for els in puzzle_elements.values() for e in els],
        solution=solution,
    )

    clues = generate_all_clues(puzzle, solution)

    reduced, extras = reduce_clues(puzzle, clues)
    for clue in reduced:
        puzzle.add_clue(clue)

    print_puzzle(puzzle, extras)
