"""
printers.py

Code to format the puzzle and solution for two different purposes:
- Inspecting in the console so that we can spot-check the outputs
- Copying into the CC puzzle input for use on the site

In particular, CC requires "pure HTML" that includes <br> tags. We construct all the different
parts of the puzzle and print it using the rich Console. This was easier than fighting an HTML
templating library like Jinja to do exactly what I need.
"""

from pathlib import Path

from rich.console import Console
from rich.rule import Rule
from rich.table import Table

from src.puzzle import Puzzle


def print_puzzle(puzzle: Puzzle):
    templates_path = Path(__file__).parent / "templates"

    puzzle_parts = [
        Rule(),
        """<div style="max-width:800px; margin-left:auto; margin-right:auto width:60% text-align:left">""",
        (templates_path / "preamble.html").read_text(),
        _format_elements(puzzle),
        _format_clues(puzzle),
        (templates_path / "answer_format.html").read_text(),
        "</div>",
        Rule(),
        "<pre>",
        _format_solution(puzzle),
        "</pre>",
    ]

    console = Console()
    for section in puzzle_parts:
        console.print(section)


def _format_elements(self: Puzzle) -> str:
    """Format the puzzle components (descriptions & enumeration of elements)."""

    lines = [
        "<u>Puzzle Components</u>",
        f"There are {self.size} nests, (numbered 1 on the left, {self.size} on the right), from the perspective of someone standing across from them.",
        "Our job is to help Traptop figure out who visited each nest.",
    ]

    for el_type in self.element_classes:  # should be sorted
        class_description = el_type.description()
        elements = ", ".join(el.name.title() for el in self.elements_by_class[el_type])
        line = f"- {class_description} ({elements})"

        lines.append(line)

    s = " <br>\n".join(lines) + " <br><br>\n"
    return s


def _format_clues(self: Puzzle) -> str:
    """Format the clues (essentially making a list without <ol>)"""

    lines = ["<u>Clues</u>"]

    for i, clue in enumerate(self.clues, 1):
        clue_description = clue.__repr__().replace("house", "nest")
        lines.append(f"{i}. {clue_description}")

    s = " <br>\n".join(lines) + " <br><br>\n"
    return s


def _format_solution(puzzle: Puzzle) -> Table:
    """
    Print a tabular representation of the puzzle solution.

        ┏━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━┓
        ┃ Nest ┃ Primary  ┃ Secondary ┃ Tertiary ┃  Smoothie   ┃ Bottlecap ┃
        ┡━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━┩
        │    1 │  fierce  │  volcano  │ crawler  │ dragonfruit │   blue    │
        │    2 │ greater  │   cave    │ stalker  │  midnight   │    red    │
        │    3 │ restless │ mountain  │ snapper  │    lemon    │   green   │
        │    4 │ ancient  │   swamp   │ hoarder  │   glacier   │   black   │
        │    5 │  lesser  │   lake    │ dweller  │  chocolate  │  yellow   │
        └──────┴──────────┴───────────┴──────────┴─────────────┴───────────┘

    Using Rich, we define the columns up front (easy; that's just an attribute of Puzzle)
    and define the rows as we go.

    Each row is a list of puzzle elements at some nest where:
    - the length is the number of element classes in the puzzle
    - item `i` has the element of type `puzzle.element_classes[i]`
    - every element's location is that same nest

    To do this, we can use a list comprehension with a generator expression inside it (Copilot).
    - The list comprehension is over `puzzle.element_classes`, which guarantees the order
    - The generator expression pulls out the correct element from the solution, checking both
      the element type and the location

    This is "inefficient" big-O wise, but this isn't an interview and practicality matters -- the
    puzzle is small enough that this is plenty good.
    """

    table = Table(title="Solution")

    table.add_column("Nest", justify="right", style="cyan")
    for element_type in puzzle.element_classes:
        # Shorten headers for compactness
        column_name = element_type.__name__.removeprefix("MythicalTraptor").removeprefix("TropicalTraptor")
        table.add_column(column_name, justify="center")

    for house in puzzle.houses:
        elements_at_house = [
            next(
                (
                    el.name.title()
                    for el, loc in puzzle.solution.items()
                    if isinstance(el, element_type) and loc == house
                )
            )
            for element_type in puzzle.element_classes
        ]
        table.add_row(str(house), *elements_at_house)

    return table
