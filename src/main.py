"""
main.py

CLI for the puzzle generator. This is intended to supersede generate.py, but
we'll see.
"""

from collections.abc import Sequence
from dataclasses import dataclass

import questionary
from rich import print

from src.traptor_elements import MythicalTraptorPrimary, Smoothie, TropicalTraptorPrimary


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


if __name__ == "__main__":
    traptor_type = select(
        "Choose a Traptor type",
        [Choice("🌴 Tropical", TropicalTraptorPrimary), Choice("🏰 Mythical", MythicalTraptorPrimary)],
    )
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

    # add bottlecaps? (there are only 5, so no need to choose which colors)
    use_bottlecaps = select("Should the puzzle include bottlecaps?", [Choice("Yes", True), Choice("No", False)])
    print(use_bottlecaps)
