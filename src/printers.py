"""
printers.py

Code to format the puzzle and solution for two different purposes:
- Inspecting in the console so that we can spot-check the outputs
- Copying into the CC puzzle input for use on the site

In particular, CC requires "pure HTML" that includes <br> tags. We construct all the different
parts of the puzzle and print it using the rich Console. This was easier than fighting an HTML
templating library like Jinja to do exactly what I need.
"""

from src.puzzle import Puzzle


def format_elements(self: Puzzle) -> str:
    """
    Format the puzzle components for printing.

    The puzzle input on CC requires a pure HTML string, <br> tags and all. The newlines that
    we include are for readability and so we can print the whole thing to the console.
    """

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


def format_clues(self: Puzzle) -> str:
    """
    Format the clues for printing.

    The puzzle input on CC requires a pure HTML string, <br> tags and all. The newlines that
    we include are for readability and so we can print the whole thing to the console. The
    clues are just a title and a numbered list, but we don't bother with a <ol> tag.
    """

    lines = ["<u>Clues</u>"]

    for i, clue in enumerate(self.clues, 1):
        clue_description = clue.__repr__().replace("house", "nest")
        lines.append(f"{i}. {clue_description}")

    s = " <br>\n".join(lines) + " <br><br>\n"
    return s
